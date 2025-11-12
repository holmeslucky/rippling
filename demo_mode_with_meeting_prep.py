"""
Demo Mode with Meeting Prep - Capitol Engineering Time Tracking System
Includes Meeting Preparation tab for Rippling API discussion

Date created: 2025-11-11
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

        costs[code]['billed_amount'] = costs[code]['actual_hours'] * costs[code]['hourly_rate']
        costs[code]['profit'] = costs[code]['billed_amount'] - costs[code]['labor_cost']
        costs[code]['profit_margin'] = round((costs[code]['profit'] / costs[code]['billed_amount']) * 100, 1) if costs[code]['billed_amount'] > 0 else 0

        if costs[code]['budget_used'] > 90:
            costs[code]['status'] = 'critical'
        elif costs[code]['budget_used'] > 75:
            costs[code]['status'] = 'warning'
        else:
            costs[code]['status'] = 'good'

    return list(costs.values())

def get_overtime_predictions():
    """Predict who will hit overtime this week"""
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
        if hours >= 35:
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

    ot_predictions = get_overtime_predictions()
    if len(ot_predictions) > 0:
        alerts.append({
            'type': 'warning',
            'icon': '⏰',
            'title': f"Overtime Risk: {len(ot_predictions)} Employees",
            'message': f"{ot_predictions[0]['employee']} at {ot_predictions[0]['hours_this_week']} hrs this week",
            'action': 'Rebalance workload to prevent OT costs'
        })

    total_profit_margin = sum(p['profit_margin'] for p in costs) / len(costs) if costs else 0
    alerts.append({
        'type': 'success',
        'icon': '💡',
        'title': 'AI Insight: Profitability',
        'message': f"Average profit margin today: {total_profit_margin:.1f}%",
        'action': 'Continue current crew allocation'
    })

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
    """Main demo dashboard with meeting prep"""
    return render_template('demo_meeting_prep.html')

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

def create_meeting_prep_html_template():
    """Create the meeting prep HTML template"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Capitol Engineering - Meeting Prep Demo</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
            padding: 20px;
        }

        .demo-banner {
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
            font-size: 1.2em;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(37,99,235,0.2);
        }

        .container { max-width: 1800px; margin: 0 auto; }

        .header {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            border-left: 4px solid #2563eb;
        }

        .tabs {
            display: flex;
            gap: 8px;
            margin: 20px 0;
            flex-wrap: wrap;
        }

        .tab {
            padding: 12px 24px;
            background: #e5e7eb;
            color: #374151;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.2s;
            box-shadow: none;
        }

        .tab:hover { background: #d1d5db; }
        .tab.active { background: #2563eb; color: white; }

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
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: none;
        }

        .card h2 {
            color: #111827;
            margin-bottom: 20px;
            border-bottom: 2px solid #2563eb;
            padding-bottom: 12px;
            font-size: 1.5em;
            font-weight: 600;
        }

        .card h3 {
            color: #1f2937;
            margin: 20px 0 10px 0;
            font-size: 1.2em;
            font-weight: 600;
        }

        .card h4 {
            color: #374151;
            margin: 15px 0 8px 0;
            font-size: 1.05em;
            font-weight: 600;
        }

        .card p, .card li {
            line-height: 1.8;
            color: #333;
            margin-bottom: 10px;
        }

        .card ul {
            margin-left: 25px;
        }

        .highlight-box {
            background: #eff6ff;
            border-left: 4px solid #2563eb;
            padding: 20px;
            margin: 20px 0;
            border-radius: 6px;
        }

        .warning-box {
            background: #fef9c3;
            border-left: 4px solid #eab308;
            padding: 20px;
            margin: 20px 0;
            border-radius: 6px;
        }

        .info-box {
            background: #f0f9ff;
            border-left: 4px solid #0284c7;
            padding: 20px;
            margin: 20px 0;
            border-radius: 6px;
        }

        .mockup-container {
            background: #f9fafb;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }

        .mockup-header {
            background: #1e40af;
            color: white;
            padding: 15px;
            border-radius: 6px 6px 0 0;
            text-align: center;
            font-weight: 600;
        }

        .mockup-project {
            background: white;
            padding: 15px;
            margin-top: 10px;
            border-radius: 6px;
            border-left: 4px solid #10b981;
        }

        .mockup-over-budget {
            border-left-color: #dc2626;
        }

        .question-list {
            background: #f3f4f6;
            padding: 15px 15px 15px 30px;
            margin: 10px 0;
            border-radius: 8px;
        }

        .question-list li {
            margin: 8px 0;
            color: #1f2937;
            font-weight: 500;
        }

        .code-block {
            background: #1f2937;
            color: #f3f4f6;
            padding: 15px;
            border-radius: 6px;
            margin: 15px 0;
            overflow-x: auto;
        }

        .alert {
            padding: 15px;
            margin-bottom: 12px;
            border-radius: 6px;
            border-left: 4px solid;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        .alert-danger { background: #fef2f2; border-color: #dc2626; }
        .alert-warning { background: #fef9c3; border-color: #eab308; }
        .alert-success { background: #f0fdf4; border-color: #10b981; }
        .alert-info { background: #eff6ff; border-color: #2563eb; }

        .alert-icon { font-size: 2em; }
        .alert-content { flex: 1; }
        .alert-title { font-weight: bold; margin-bottom: 5px; }
        .alert-action { font-size: 0.9em; color: #666; margin-top: 5px; }

        .cost-card {
            background: white;
            padding: 20px;
            border-radius: 6px;
            margin-bottom: 15px;
            border-left: 4px solid;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        .cost-good { border-color: #10b981; }
        .cost-warning { border-color: #eab308; }
        .cost-critical { border-color: #dc2626; }

        .metric { display: flex; justify-content: space-between; margin: 8px 0; }
        .metric-label { color: #666; }
        .metric-value { font-weight: bold; font-size: 1.1em; }

        .progress-bar {
            width: 100%;
            height: 24px;
            background: #e5e7eb;
            border-radius: 4px;
            overflow: hidden;
            margin: 10px 0;
        }

        .progress-fill {
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 0.85em;
            transition: width 0.3s;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }

        .feature-card {
            background: #f9fafb;
            padding: 15px;
            border-radius: 6px;
            border-left: 3px solid #2563eb;
        }

        .feature-name { font-weight: 600; margin-bottom: 5px; }
        .feature-status {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: 600;
        }

        .status-ready { background: #dcfce7; color: #166534; }
        .status-beta { background: #fef9c3; color: #854d0e; }
        .status-planned { background: #dbeafe; color: #1e40af; }

        table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #e5e7eb; }
        th { background: #f9fafb; font-weight: 600; color: #111827; }
        tr:hover { background: #f9fafb; }
    </style>
</head>
<body>
    <div class="container">
        <div class="demo-banner">
            📋 MEETING PREP MODE - Rippling API Discussion Ready! 📋
        </div>

        <div class="header">
            <h1>Capitol Engineering - Rippling API Meeting Preparation</h1>
            <p>Thursday Meeting: Everything You Need to Explain APIs and Project Budget Tracking</p>

            <div class="tabs">
                <button class="tab active" onclick="switchTab('meetingprep')">📋 Meeting Prep</button>
                <button class="tab" onclick="switchTab('alerts')">🔔 Smart Alerts Demo</button>
                <button class="tab" onclick="switchTab('costs')">💰 Cost Tracking Demo</button>
                <button class="tab" onclick="switchTab('overtime')">⏰ Overtime Demo</button>
                <button class="tab" onclick="switchTab('future')">🔮 Future Features</button>
            </div>
        </div>

        <!-- Meeting Prep Tab -->
        <div id="meetingprep-tab" class="tab-content active">
            <div class="card">
                <h2>Quick Reference for Thursday Meeting</h2>

                <div class="highlight-box">
                    <h3>The 30-Second Pitch</h3>
                    <p><strong>"We've built a dashboard that pulls employee time data from Rippling's API. It shows who worked on which projects and for how many hours. Now we want to add project budget tracking - comparing hours worked vs hours budgeted - so we can see if projects are on track or over budget. We need help storing budget data in Rippling and accessing it via the API."</strong></p>
                </div>

                <h3>What is an API? (Simple Explanation)</h3>
                <div class="info-box">
                    <h4>The Restaurant Analogy</h4>
                    <p><strong>Think of an API like a waiter in a restaurant:</strong></p>
                    <ul>
                        <li><strong>You (Customer)</strong> = Your computer/dashboard</li>
                        <li><strong>Kitchen</strong> = Rippling's database (where all employee data is stored)</li>
                        <li><strong>Waiter</strong> = The API</li>
                    </ul>
                    <p>You can't go into the kitchen and grab food yourself. Instead, you tell the waiter what you want (API request), the waiter goes to the kitchen (Rippling servers), and brings you what you asked for (API response).</p>
                </div>

                <h3>Our Goal: Project Budget Dashboard</h3>
                <p>We want to track <strong>Hours Worked vs Hours Budgeted</strong> for each project in real-time.</p>

                <div class="mockup-container">
                    <div class="mockup-header">PROPOSED PROJECT DASHBOARD</div>
                    <div class="mockup-project">
                        <strong>Project: M-25-0001 - Lithium Nevada Ducting</strong><br>
                        Today's Hours: 87.5<br>
                        <br>
                        <strong>PROJECT BUDGET STATUS:</strong><br>
                        Budgeted Hours: 500 hrs<br>
                        Hours Worked: 387 hrs (77%)<br>
                        Hours Remaining: 113 hrs (23%)<br>
                        Status: ✓ ON TRACK
                    </div>
                    <div class="mockup-project mockup-over-budget">
                        <strong>Project: M-25-0002 - Phoenix Convention Center</strong><br>
                        Today's Hours: 64.0<br>
                        <br>
                        <strong>PROJECT BUDGET STATUS:</strong><br>
                        Budgeted Hours: 800 hrs<br>
                        Hours Worked: 856 hrs (107%)<br>
                        Hours Over Budget: 56 hrs (7% over)<br>
                        Status: ⚠ OVER BUDGET
                    </div>
                </div>

                <h3>Main Questions to Ask</h3>
                <div class="question-list">
                    <ol>
                        <li><strong>Where can we store project budget data?</strong> (Custom field on job dimensions? Separate table?)</li>
                        <li><strong>What API access do we need?</strong> (Currently have /users and /time-entries, need project fields)</li>
                        <li><strong>Can we add custom fields?</strong> (Budgeted Hours, Project Status, Start/End Dates)</li>
                        <li><strong>What are the API limits?</strong> (We'll make ~288 calls per day)</li>
                        <li><strong>Do you support webhooks?</strong> (For real-time clock in/out notifications)</li>
                    </ol>
                </div>

                <h3>What We've Already Built</h3>
                <ul>
                    <li>✓ Dashboard showing employee hours by project</li>
                    <li>✓ Daily labor reports in Excel</li>
                    <li>✓ Web interface for foremen</li>
                    <li>✓ Automatic data refresh every 5 minutes</li>
                    <li>✓ Working API connection to Rippling</li>
                </ul>
                <p><strong>Demo Links:</strong></p>
                <ul>
                    <li>Local: <a href="http://localhost:5000" target="_blank">http://localhost:5000</a></li>
                    <li>Live: <a href="https://capitol-engineering-demo.onrender.com" target="_blank">https://capitol-engineering-demo.onrender.com</a></li>
                </ul>

                <h3>What We Need from Rippling</h3>
                <div class="warning-box">
                    <ol>
                        <li><strong>API token with project data access</strong></li>
                        <li><strong>Place to store budget numbers</strong> (preferably custom fields on job dimensions)</li>
                        <li><strong>Documentation on project fields</strong></li>
                        <li><strong>Timeline for setup</strong></li>
                    </ol>
                </div>

                <h3>Data We Need to Store</h3>
                <p>For each project, we need:</p>
                <ul>
                    <li><strong>Budgeted Hours</strong> (integer) - Example: 500 hours</li>
                    <li><strong>Project Start Date</strong> (date) - Example: 2025-10-15</li>
                    <li><strong>Project Target End Date</strong> (date) - Example: 2025-12-01</li>
                    <li><strong>Budget Alert Threshold</strong> (percentage, optional) - Example: 90%</li>
                    <li><strong>Project Status</strong> (text, optional) - Active, Completed, On Hold</li>
                </ul>

                <h3>Technical Details (If They Ask)</h3>
                <div class="code-block">
                    Language: Python<br>
                    Authentication: Bearer token<br>
                    Protocol: HTTPS REST API<br>
                    Base URL: https://rest.ripplingapis.com<br>
                    Update frequency: Every 5 minutes<br>
                    Security: Token stored in environment variables
                </div>

                <h3>Value Proposition</h3>
                <ul>
                    <li>💡 See project status in real-time</li>
                    <li>💰 Prevent budget overruns</li>
                    <li>👥 Better resource allocation</li>
                    <li>📊 Improve future bidding</li>
                    <li>⏱️ Save project managers hours per week</li>
                </ul>

                <div class="highlight-box">
                    <h3>If You Get Stuck</h3>
                    <p><strong>Key phrases to fall back on:</strong></p>
                    <ul>
                        <li>"We're already successfully pulling time entries"</li>
                        <li>"We just need to expand to include budget data"</li>
                        <li>"The system is working, we just need guidance on this one piece"</li>
                        <li>"Let me check my documentation and get back to you"</li>
                    </ul>
                </div>

                <h3>After Meeting Action Items</h3>
                <ul>
                    <li>✓ Document all answers and decisions</li>
                    <li>✓ Get API token with new permissions (if needed)</li>
                    <li>✓ Receive documentation on project fields</li>
                    <li>✓ Schedule follow-up if needed</li>
                    <li>✓ Update coworker on progress</li>
                </ul>

                <div class="info-box">
                    <p><strong>📁 Full Documentation Available:</strong></p>
                    <ul>
                        <li>MEETING_PREP_GUIDE.md - Complete detailed guide</li>
                        <li>MEETING_CHEAT_SHEET.md - One-page quick reference</li>
                        <li>DASHBOARD_MOCKUP.md - Visual mockups and examples</li>
                        <li>API_CAPABILITIES.md - What Rippling API provides</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Alerts Tab -->
        <div id="alerts-tab" class="tab-content">
            <div class="card">
                <h2>AI-Powered Alerts & Insights (Demo)</h2>
                <div id="alertsContent">Loading smart alerts...</div>
            </div>
        </div>

        <!-- Cost Tracking Tab -->
        <div id="costs-tab" class="tab-content">
            <div class="card">
                <h2>Real-Time Project Cost Analysis (Demo)</h2>
                <div id="costsContent">Loading cost data...</div>
            </div>
        </div>

        <!-- Overtime Tab -->
        <div id="overtime-tab" class="tab-content">
            <div class="card">
                <h2>Overtime Prediction System (Demo)</h2>
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
                    let html = '<table><thead><tr><th>Employee</th><th>ID</th><th>Hours This Week</th><th>To OT</th><th>Risk</th><th>Recommendation</th></tr></thead><tbody>';

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
    </script>
</body>
</html>"""

    with open(os.path.join(templates_dir, 'demo_meeting_prep.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    create_meeting_prep_html_template()

    port = int(os.environ.get('PORT', 5000))

    print("\n" + "="*80)
    print("CAPITOL ENGINEERING - MEETING PREP DEMO MODE")
    print("="*80)
    print("\nPrepared for Thursday Rippling API Meeting:")
    print("  • Complete meeting preparation guide")
    print("  • API explanation with restaurant analogy")
    print("  • Project budget dashboard mockup")
    print("  • Key questions and talking points")
    print("  • Working demo tabs to show capabilities")
    print(f"\nMeeting Prep Dashboard: http://localhost:{port}")
    print("\nPress Ctrl+C to stop")
    print("="*80 + "\n")

    app.run(debug=False, host='0.0.0.0', port=port)
