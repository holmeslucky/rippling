"""
ULTRA Demo Mode - Capitol Engineering Time Tracking System
Shows ALL future capabilities including cost tracking, alerts, and AI insights

Date created: 2025-10-30
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
from demo_data_generator import DemoDataGenerator
import pandas as pd
import os
import random

app = Flask(__name__)

# Initialize demo data generator
demo_generator = DemoDataGenerator()

# Generate demo data cache
demo_cache = {
    'employees': demo_generator.generate_sample_employees(),
    'projects': demo_generator.generate_sample_projects(),
    'time_entries': {},
    'generated_at': datetime.now()
}

def get_demo_time_entries(date_str: str):
    """Get or generate time entries for a specific date"""
    if date_str not in demo_cache['time_entries']:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        demo_cache['time_entries'][date_str] = demo_generator.generate_daily_time_entries(date)
    return demo_cache['time_entries'][date_str]

def calculate_project_costs(date: str):
    """Calculate real-time project costs"""
    entries = get_demo_time_entries(date)
    employee_map = {emp['id']: emp for emp in demo_cache['employees']}
    project_map = {proj['code']: proj for proj in demo_cache['projects']}

    costs = {}
    for entry in entries:
        emp = employee_map.get(entry['employee_id'], {})
        proj_code = entry['job_code']
        hours = entry['hours']
        rate = demo_generator.labor_rates.get(emp.get('role'), 30)

        if proj_code not in costs:
            proj = project_map.get(proj_code, {})
            costs[proj_code] = {
                'project': proj_code,
                'name': proj.get('name', 'Unknown'),
                'budget_hours': proj.get('budget_hours', 0),
                'hourly_rate': proj.get('hourly_rate', 85),
                'estimated_total': proj.get('estimated_total', 0),
                'actual_hours': 0,
                'labor_cost': 0,
                'employees': set()
            }

        costs[proj_code]['actual_hours'] += hours
        costs[proj_code]['labor_cost'] += (hours * rate)
        costs[proj_code]['employees'].add(entry['employee_id'])

    # Calculate percentages and status
    for code in costs:
        costs[code]['employee_count'] = len(costs[code]['employees'])
        costs[code]['employees'] = list(costs[code]['employees'])

        if costs[code]['budget_hours'] > 0:
            costs[code]['budget_used'] = round((costs[code]['actual_hours'] / costs[code]['budget_hours']) * 100, 1)
        else:
            costs[code]['budget_used'] = 0

        # Calculate billed amount (hourly_rate is billable rate, labor_cost is our cost)
        costs[code]['billed_amount'] = costs[code]['actual_hours'] * costs[code]['hourly_rate']
        costs[code]['profit'] = costs[code]['billed_amount'] - costs[code]['labor_cost']
        costs[code]['profit_margin'] = round((costs[code]['profit'] / costs[code]['billed_amount']) * 100, 1) if costs[code]['billed_amount'] > 0 else 0

        # Status based on budget usage
        if costs[code]['budget_used'] > 90:
            costs[code]['status'] = 'critical'
        elif costs[code]['budget_used'] > 75:
            costs[code]['status'] = 'warning'
        else:
            costs[code]['status'] = 'good'

    return list(costs.values())

def get_overtime_predictions():
    """Predict who will hit overtime this week"""
    # Get this week's data
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())

    predictions = []
    employee_hours = {}

    for i in range(5):  # Mon-Fri
        date = week_start + timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        entries = get_demo_time_entries(date_str)

        for entry in entries:
            emp_id = entry['employee_id']
            if emp_id not in employee_hours:
                employee_hours[emp_id] = 0
            employee_hours[emp_id] += entry['hours']

    employee_map = {emp['id']: emp for emp in demo_cache['employees']}

    for emp_id, hours in employee_hours.items():
        emp = employee_map.get(emp_id, {})
        if hours >= 35:  # Approaching overtime
            predictions.append({
                'employee': f"{emp.get('first_name')} {emp.get('last_name')}",
                'employee_id': emp.get('employee_id'),
                'hours_this_week': round(hours, 1),
                'hours_to_ot': round(40 - hours, 1),
                'risk_level': 'high' if hours >= 38 else 'medium',
                'recommendation': 'Reassign to light duties' if hours >= 38 else 'Monitor closely'
            })

    return sorted(predictions, key=lambda x: x['hours_this_week'], reverse=True)

def generate_smart_alerts():
    """Generate AI-powered alerts and insights"""
    alerts = []
    today_str = datetime.now().strftime('%Y-%m-%d')

    # Check for budget overruns
    costs = calculate_project_costs(today_str)
    for project in costs:
        if project['status'] == 'critical':
            alerts.append({
                'type': 'danger',
                'icon': '⚠️',
                'title': f"Budget Alert: {project['project']}",
                'message': f"{project['budget_used']}% of budget used. Action required.",
                'action': 'Review project scope or request budget increase'
            })
        elif project['status'] == 'warning':
            alerts.append({
                'type': 'warning',
                'icon': '⚡',
                'title': f"Budget Warning: {project['project']}",
                'message': f"{project['budget_used']}% of budget used. Monitor closely.",
                'action': 'Optimize crew allocation'
            })

    # Check overtime predictions
    ot_predictions = get_overtime_predictions()
    if len(ot_predictions) > 0:
        alerts.append({
            'type': 'warning',
            'icon': '⏰',
            'title': f"Overtime Risk: {len(ot_predictions)} Employees",
            'message': f"{ot_predictions[0]['employee']} at {ot_predictions[0]['hours_this_week']} hrs this week",
            'action': 'Rebalance workload to prevent OT costs'
        })

    # AI Insights
    total_profit_margin = sum(p['profit_margin'] for p in costs) / len(costs) if costs else 0
    alerts.append({
        'type': 'success',
        'icon': '💡',
        'title': 'AI Insight: Profitability',
        'message': f"Average profit margin today: {total_profit_margin:.1f}%",
        'action': 'Continue current crew allocation'
    })

    # Efficiency insight
    best_project = max(costs, key=lambda x: x['profit_margin']) if costs else None
    if best_project:
        alerts.append({
            'type': 'info',
            'icon': '🎯',
            'title': 'Performance Insight',
            'message': f"{best_project['project']} is most profitable at {best_project['profit_margin']:.1f}% margin",
            'action': 'Consider similar project opportunities'
        })

    return alerts

@app.route('/')
def index():
    """Main ultra demo dashboard"""
    return render_template('demo_ultra.html')

@app.route('/api/project-costs')
def get_project_costs():
    """Get project cost analysis"""
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    try:
        costs = calculate_project_costs(date)
        return jsonify({'costs': costs, 'date': date})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/overtime-predictions')
def get_ot_predictions():
    """Get overtime predictions"""
    try:
        predictions = get_overtime_predictions()
        return jsonify({'predictions': predictions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/smart-alerts')
def get_alerts():
    """Get AI-powered alerts"""
    try:
        alerts = generate_smart_alerts()
        return jsonify({'alerts': alerts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/future-features')
def get_future_features():
    """Get list of future features"""
    features = [
        {
            'category': 'Automation',
            'features': [
                {'name': 'Daily Email Reports', 'status': 'Ready', 'effort': '1-2 days'},
                {'name': 'Overtime Alerts', 'status': 'Ready', 'effort': '2-3 days'},
                {'name': 'Missing Timesheet Alerts', 'status': 'Ready', 'effort': '1-2 days'},
            ]
        },
        {
            'category': 'Analytics',
            'features': [
                {'name': 'Bid vs Actual Analysis', 'status': 'Planned', 'effort': '1 week'},
                {'name': 'Productivity Tracking', 'status': 'Planned', 'effort': '1 week'},
                {'name': 'AI-Powered Insights', 'status': 'Beta', 'effort': '2 weeks'},
            ]
        },
        {
            'category': 'Integration',
            'features': [
                {'name': 'QuickBooks Sync', 'status': 'Planned', 'effort': '1-2 weeks'},
                {'name': 'Customer Portal', 'status': 'Planned', 'effort': '1 week'},
                {'name': 'Slack Notifications', 'status': 'Ready', 'effort': '2-3 days'},
            ]
        },
        {
            'category': 'Mobile',
            'features': [
                {'name': 'Mobile App', 'status': 'Planned', 'effort': '2-3 months'},
                {'name': 'GPS Geofencing', 'status': 'Planned', 'effort': '2 weeks'},
                {'name': 'Voice Clock In', 'status': 'Beta', 'effort': '1-2 weeks'},
            ]
        }
    ]
    return jsonify({'features': features})

def create_ultra_html_template():
    """Create the ultra demo HTML template"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Capitol Engineering - ULTRA Demo (All Features)</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .demo-banner {
            background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            text-align: center;
            font-size: 1.3em;
            font-weight: bold;
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            animation: glow 2s ease-in-out infinite;
        }

        @keyframes glow {
            0%, 100% { box-shadow: 0 8px 16px rgba(245, 158, 11, 0.4); }
            50% { box-shadow: 0 8px 32px rgba(245, 158, 11, 0.8); }
        }

        .container { max-width: 1800px; margin: 0 auto; }

        .header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }

        .tabs {
            display: flex;
            gap: 10px;
            margin: 20px 0;
            flex-wrap: wrap;
        }

        .tab {
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 700;
            transition: all 0.3s;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        .tab:hover { transform: translateY(-3px); box-shadow: 0 6px 12px rgba(0,0,0,0.3); }
        .tab.active { background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%); }

        .tab-content { display: none; }
        .tab-content.active { display: block; }

        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
            transition: transform 0.3s;
        }

        .card:hover { transform: translateY(-5px); box-shadow: 0 12px 24px rgba(0,0,0,0.2); }

        .card h2 {
            color: #1e3c72;
            margin-bottom: 20px;
            border-bottom: 4px solid #667eea;
            padding-bottom: 12px;
            font-size: 1.4em;
        }

        .alert {
            padding: 15px;
            margin-bottom: 12px;
            border-radius: 10px;
            border-left: 5px solid;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .alert-danger { background: #fee; border-color: #ef4444; }
        .alert-warning { background: #fef3c7; border-color: #f59e0b; }
        .alert-success { background: #d1fae5; border-color: #10b981; }
        .alert-info { background: #dbeafe; border-color: #3b82f6; }

        .alert-icon { font-size: 2em; }
        .alert-content { flex: 1; }
        .alert-title { font-weight: bold; margin-bottom: 5px; }
        .alert-action { font-size: 0.9em; color: #666; margin-top: 5px; }

        .cost-card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 15px;
            border-left: 6px solid;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .cost-good { border-color: #10b981; }
        .cost-warning { border-color: #f59e0b; }
        .cost-critical { border-color: #ef4444; }

        .metric { display: flex; justify-content: space-between; margin: 8px 0; }
        .metric-label { color: #666; }
        .metric-value { font-weight: bold; font-size: 1.1em; }

        .progress-bar {
            width: 100%;
            height: 25px;
            background: #e5e7eb;
            border-radius: 12px;
            overflow: hidden;
            margin: 10px 0;
        }

        .progress-fill {
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
            transition: width 0.5s;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }

        .feature-card {
            background: #f9fafb;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }

        .feature-name { font-weight: bold; margin-bottom: 5px; }
        .feature-status {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }

        .status-ready { background: #d1fae5; color: #065f46; }
        .status-beta { background: #fef3c7; color: #92400e; }
        .status-planned { background: #dbeafe; color: #1e3a8a; }
    </style>
</head>
<body>
    <div class="container">
        <div class="demo-banner">
            🚀 ULTRA DEMO MODE - All Future Features Preview! 🚀
        </div>

        <div class="header">
            <h1>Capitol Engineering - Complete Business Intelligence Platform</h1>
            <p>Rippling API Integration + Advanced Analytics + AI Insights + Future Features</p>

            <div class="tabs">
                <button class="tab active" onclick="switchTab('alerts')">🔔 Smart Alerts</button>
                <button class="tab" onclick="switchTab('costs')">💰 Cost Tracking</button>
                <button class="tab" onclick="switchTab('overtime')">⏰ Overtime Prediction</button>
                <button class="tab" onclick="switchTab('future')">🔮 Future Features</button>
            </div>
        </div>

        <!-- Alerts Tab -->
        <div id="alerts-tab" class="tab-content active">
            <div class="card">
                <h2>AI-Powered Alerts & Insights</h2>
                <div id="alertsContent">Loading smart alerts...</div>
            </div>
        </div>

        <!-- Cost Tracking Tab -->
        <div id="costs-tab" class="tab-content">
            <div class="card">
                <h2>Real-Time Project Cost Analysis</h2>
                <div id="costsContent">Loading cost data...</div>
            </div>
        </div>

        <!-- Overtime Tab -->
        <div id="overtime-tab" class="tab-content">
            <div class="card">
                <h2>Overtime Prediction System</h2>
                <div id="overtimeContent">Loading predictions...</div>
            </div>
        </div>

        <!-- Future Features Tab -->
        <div id="future-tab" class="tab-content">
            <div class="card">
                <h2>Coming Soon: Full Feature Roadmap</h2>
                <div id="futureContent">Loading feature roadmap...</div>
            </div>
        </div>
    </div>

    <script>
        function switchTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));

            event.target.classList.add('active');
            document.getElementById(tabName + '-tab').classList.add('active');

            if (tabName === 'alerts') loadAlerts();
            if (tabName === 'costs') loadCosts();
            if (tabName === 'overtime') loadOvertime();
            if (tabName === 'future') loadFuture();
        }

        function loadAlerts() {
            fetch('/api/smart-alerts')
                .then(r => r.json())
                .then(data => {
                    let html = '';
                    data.alerts.forEach(alert => {
                        html += `<div class="alert alert-${alert.type}">
                            <div class="alert-icon">${alert.icon}</div>
                            <div class="alert-content">
                                <div class="alert-title">${alert.title}</div>
                                <div>${alert.message}</div>
                                <div class="alert-action">→ ${alert.action}</div>
                            </div>
                        </div>`;
                    });
                    document.getElementById('alertsContent').innerHTML = html;
                });
        }

        function loadCosts() {
            const date = new Date().toISOString().split('T')[0];
            fetch(`/api/project-costs?date=${date}`)
                .then(r => r.json())
                .then(data => {
                    let html = '';
                    data.costs.forEach(project => {
                        const statusClass = `cost-${project.status}`;
                        const fillColor = project.status === 'good' ? '#10b981' : project.status === 'warning' ? '#f59e0b' : '#ef4444';

                        html += `<div class="cost-card ${statusClass}">
                            <h3>${project.project}: ${project.name}</h3>
                            <div class="metric">
                                <span class="metric-label">Budget Hours:</span>
                                <span class="metric-value">${project.actual_hours.toFixed(1)} / ${project.budget_hours} hrs</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${Math.min(project.budget_used, 100)}%; background: ${fillColor}">
                                    ${project.budget_used}%
                                </div>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Labor Cost:</span>
                                <span class="metric-value">$${project.labor_cost.toFixed(2)}</span>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Billed Amount:</span>
                                <span class="metric-value">$${project.billed_amount.toFixed(2)}</span>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Profit:</span>
                                <span class="metric-value" style="color: ${project.profit > 0 ? '#10b981' : '#ef4444'}">
                                    $${project.profit.toFixed(2)} (${project.profit_margin}% margin)
                                </span>
                            </div>
                        </div>`;
                    });
                    document.getElementById('costsContent').innerHTML = html;
                });
        }

        function loadOvertime() {
            fetch('/api/overtime-predictions')
                .then(r => r.json())
                .then(data => {
                    let html = '<table style="width:100%"><thead><tr><th>Employee</th><th>ID</th><th>Hours This Week</th><th>To OT</th><th>Risk</th><th>Recommendation</th></tr></thead><tbody>';

                    data.predictions.forEach(pred => {
                        const riskColor = pred.risk_level === 'high' ? '#ef4444' : '#f59e0b';
                        html += `<tr>
                            <td><strong>${pred.employee}</strong></td>
                            <td>${pred.employee_id}</td>
                            <td>${pred.hours_this_week} hrs</td>
                            <td>${pred.hours_to_ot} hrs</td>
                            <td><span style="color: ${riskColor}; font-weight: bold">${pred.risk_level.toUpperCase()}</span></td>
                            <td>${pred.recommendation}</td>
                        </tr>`;
                    });

                    html += '</tbody></table>';

                    if (data.predictions.length === 0) {
                        html = '<div class="alert alert-success"><div class="alert-icon">✅</div><div class="alert-content"><div class="alert-title">No Overtime Risk</div>All employees are within normal hours this week.</div></div>';
                    }

                    document.getElementById('overtimeContent').innerHTML = html;
                });
        }

        function loadFuture() {
            fetch('/api/future-features')
                .then(r => r.json())
                .then(data => {
                    let html = '';
                    data.features.forEach(category => {
                        html += `<h3 style="margin-top: 25px; color: #1e3c72">${category.category}</h3>`;
                        html += '<div class="feature-grid">';
                        category.features.forEach(feature => {
                            const statusClass = feature.status === 'Ready' ? 'status-ready' : feature.status === 'Beta' ? 'status-beta' : 'status-planned';
                            html += `<div class="feature-card">
                                <div class="feature-name">${feature.name}</div>
                                <div><span class="feature-status ${statusClass}">${feature.status}</span> • ${feature.effort}</div>
                            </div>`;
                        });
                        html += '</div>';
                    });
                    document.getElementById('futureContent').innerHTML = html;
                });
        }

        loadAlerts();
    </script>
</body>
</html>"""

    with open(os.path.join(templates_dir, 'demo_ultra.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    create_ultra_html_template()

    port = int(os.environ.get('PORT', 5000))

    print("\n" + "="*80)
    print("CAPITOL ENGINEERING - ULTRA DEMO MODE")
    print("="*80)
    print("\nShowing ALL Future Capabilities:")
    print("  • Real-time project cost tracking")
    print("  • AI-powered smart alerts")
    print("  • Overtime prediction system")
    print("  • Complete feature roadmap")
    print("  • Budget vs actual analysis")
    print("  • Profit margin tracking")
    print(f"\nULTRA Dashboard: http://localhost:{port}")
    print("\nPress Ctrl+C to stop")
    print("="*80 + "\n")

    app.run(debug=False, host='0.0.0.0', port=port)
