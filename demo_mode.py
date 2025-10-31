"""
Demo Mode - Capitol Engineering Time Tracking System
Web dashboard using demo data for presentations and training

Date created: 2025-10-30
"""

from flask import Flask, render_template, jsonify, request, send_file
from datetime import datetime, timedelta
from demo_data_generator import DemoDataGenerator
import pandas as pd
import os
import json

app = Flask(__name__)

# Initialize demo data generator
demo_generator = DemoDataGenerator()

# Generate demo data cache
demo_cache = {
    'employees': demo_generator.generate_sample_employees(),
    'projects': demo_generator.generate_sample_projects(),
    'time_entries': {},  # Will be populated on demand
    'generated_at': datetime.now()
}


def get_demo_time_entries(date_str: str):
    """Get or generate time entries for a specific date"""
    if date_str not in demo_cache['time_entries']:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        demo_cache['time_entries'][date_str] = demo_generator.generate_daily_time_entries(date)
    return demo_cache['time_entries'][date_str]


def process_demo_daily_summary(date: str):
    """Process demo time entries into daily summary format"""
    time_entries = get_demo_time_entries(date)
    employee_map = {emp['id']: emp for emp in demo_cache['employees']}

    report_data = []

    for entry in time_entries:
        employee_id = entry.get('employee_id')
        employee = employee_map.get(employee_id, {})

        report_data.append({
            'Employee': f"{employee.get('first_name', '')} {employee.get('last_name', '')}",
            'Employee_ID': employee.get('employee_id', 'N/A'),
            'Project': entry.get('job_code', 'No Project'),
            'Job_Dimension': entry.get('dimension_name', 'N/A'),
            'Hours': entry.get('hours', 0),
            'Clock_In': datetime.fromisoformat(entry['start_time']).strftime('%I:%M %p'),
            'Clock_Out': datetime.fromisoformat(entry['end_time']).strftime('%I:%M %p'),
            'Status': entry.get('status', 'Active')
        })

    df = pd.DataFrame(report_data)
    if not df.empty:
        df = df.sort_values(['Project', 'Employee'])

    return df


def process_demo_project_breakdown(date: str):
    """Process demo data into project breakdown"""
    daily_summary = process_demo_daily_summary(date)

    if daily_summary.empty:
        return pd.DataFrame()

    project_summary = daily_summary.groupby('Project').agg({
        'Hours': 'sum',
        'Employee': 'count'
    }).reset_index()

    project_summary.columns = ['Project', 'Total_Hours', 'Employee_Count']
    project_summary = project_summary.sort_values('Total_Hours', ascending=False)

    return project_summary


@app.route('/')
def index():
    """Main demo dashboard page"""
    return render_template('demo_dashboard.html')


@app.route('/api/daily-summary')
def get_daily_summary():
    """API endpoint to get daily summary data (demo)"""
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

    try:
        daily_summary = process_demo_daily_summary(date)

        if daily_summary.empty:
            return jsonify({
                'date': date,
                'data': [],
                'message': 'No time entries found for this date',
                'demo_mode': True
            })

        data = daily_summary.to_dict(orient='records')

        return jsonify({
            'date': date,
            'data': data,
            'total_records': len(data),
            'demo_mode': True
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/project-breakdown')
def get_project_breakdown():
    """API endpoint to get project breakdown (demo)"""
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

    try:
        project_breakdown = process_demo_project_breakdown(date)

        if project_breakdown.empty:
            return jsonify({
                'date': date,
                'data': [],
                'message': 'No projects found for this date',
                'demo_mode': True
            })

        data = project_breakdown.to_dict(orient='records')

        return jsonify({
            'date': date,
            'data': data,
            'total_hours': sum(item['Total_Hours'] for item in data),
            'total_employees': sum(item['Employee_Count'] for item in data),
            'demo_mode': True
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export-excel')
def export_to_excel():
    """Generate and prepare Excel report (demo)"""
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

    try:
        output_path = f"Capitol_Labor_Report_DEMO_{date}.xlsx"

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Sheet 1: Daily summary
            daily_summary = process_demo_daily_summary(date)
            if not daily_summary.empty:
                daily_summary.to_excel(writer, sheet_name='Daily Summary', index=False)

            # Sheet 2: Project breakdown
            project_breakdown = process_demo_project_breakdown(date)
            if not project_breakdown.empty:
                project_breakdown.to_excel(writer, sheet_name='Project Totals', index=False)

            # Sheet 3: Demo info
            demo_info = pd.DataFrame([{
                'Note': 'This is DEMO DATA for demonstration purposes',
                'Company': 'Capitol Engineering',
                'Website': 'www.capitolaz.com',
                'Generated': datetime.now().strftime('%Y-%m-%d %I:%M %p')
            }])
            demo_info.to_excel(writer, sheet_name='Demo Info', index=False)

        return jsonify({
            'success': True,
            'file': output_path,
            'message': f'Demo report generated: {output_path}',
            'demo_mode': True
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats')
def get_stats():
    """Get overall demo statistics"""
    return jsonify({
        'total_employees': len(demo_cache['employees']),
        'total_projects': len(demo_cache['projects']),
        'demo_mode': True,
        'company': 'Capitol Engineering',
        'system': 'Rippling Time Tracking Integration (DEMO)'
    })


def create_demo_html_template():
    """Create the HTML template for the demo dashboard"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Capitol Engineering - Labor Dashboard (DEMO)</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .demo-banner {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            text-align: center;
            font-size: 1.2em;
            font-weight: bold;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.9; }
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }

        .header h1 {
            color: #333;
            margin-bottom: 10px;
        }

        .header .subtitle {
            color: #666;
            font-size: 1.1em;
            margin-bottom: 15px;
        }

        .controls {
            display: flex;
            gap: 15px;
            align-items: center;
            margin-top: 15px;
            flex-wrap: wrap;
        }

        .controls input[type="date"] {
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }

        .controls button {
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s;
            font-weight: 600;
        }

        .controls button:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        .controls button.export {
            background: #28a745;
        }

        .controls button.export:hover {
            background: #218838;
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.15);
        }

        .card h2 {
            color: #333;
            margin-bottom: 20px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }

        .stat-box {
            display: flex;
            justify-content: space-between;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .stat-box .label {
            font-weight: 600;
            font-size: 1em;
        }

        .stat-box .value {
            font-weight: bold;
            font-size: 1.3em;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        table th {
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }

        table td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }

        table tr:hover {
            background: #f8f9fa;
        }

        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }

        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #c33;
        }

        .project-badge {
            display: inline-block;
            padding: 5px 12px;
            background: #667eea;
            color: white;
            border-radius: 15px;
            font-size: 0.9em;
            font-weight: 600;
        }

        .company-logo {
            text-align: center;
            margin: 20px 0;
        }

        .company-logo h3 {
            color: white;
            font-size: 1.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .footer {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
            color: #666;
        }

        .status-badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: 600;
        }

        .status-approved {
            background: #d4edda;
            color: #155724;
        }

        .status-pending {
            background: #fff3cd;
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="demo-banner">
            DEMO MODE - Sample Data for Presentation
        </div>

        <div class="company-logo">
            <h3>Capitol Engineering - www.capitolaz.com</h3>
        </div>

        <div class="header">
            <h1>Daily Labor Dashboard</h1>
            <p class="subtitle">Rippling Time Tracking Integration - Real-time Project Labor Monitoring</p>
            <div class="controls">
                <label for="reportDate">Select Date:</label>
                <input type="date" id="reportDate" value="">
                <button onclick="loadData()">Load Report</button>
                <button class="export" onclick="exportExcel()">Export to Excel</button>
                <button onclick="loadData()">Refresh Data</button>
            </div>
        </div>

        <div class="dashboard-grid">
            <div class="card">
                <h2>Project Summary</h2>
                <div id="projectSummary">
                    <div class="loading">Loading project data...</div>
                </div>
            </div>

            <div class="card">
                <h2>Quick Stats</h2>
                <div id="quickStats">
                    <div class="loading">Loading statistics...</div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>Employee Time Details</h2>
            <div id="employeeDetails">
                <div class="loading">Loading employee data...</div>
            </div>
        </div>

        <div class="footer">
            <p>This is a demonstration using sample data</p>
            <p>Capitol Engineering Time Tracking System | Powered by Rippling API</p>
        </div>
    </div>

    <script>
        document.getElementById('reportDate').valueAsDate = new Date();

        function loadData() {
            const date = document.getElementById('reportDate').value;
            loadProjectBreakdown(date);
            loadDailySummary(date);
        }

        function loadProjectBreakdown(date) {
            fetch(`/api/project-breakdown?date=${date}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('projectSummary').innerHTML =
                            `<div class="error">Error: ${data.error}</div>`;
                        document.getElementById('quickStats').innerHTML =
                            `<div class="error">Error loading stats</div>`;
                        return;
                    }

                    let html = '';
                    if (data.data.length === 0) {
                        html = '<p>No projects found for this date.</p>';
                    } else {
                        html = '<table><thead><tr><th>Project</th><th>Hours</th><th>Employees</th></tr></thead><tbody>';
                        data.data.forEach(project => {
                            html += `<tr>
                                <td><span class="project-badge">${project.Project}</span></td>
                                <td><strong>${project.Total_Hours.toFixed(2)}</strong> hrs</td>
                                <td>${project.Employee_Count}</td>
                            </tr>`;
                        });
                        html += '</tbody></table>';
                    }
                    document.getElementById('projectSummary').innerHTML = html;

                    document.getElementById('quickStats').innerHTML = `
                        <div class="stat-box">
                            <span class="label">Total Hours Today</span>
                            <span class="value">${data.total_hours?.toFixed(2) || 0} hrs</span>
                        </div>
                        <div class="stat-box">
                            <span class="label">Active Projects</span>
                            <span class="value">${data.data.length}</span>
                        </div>
                        <div class="stat-box">
                            <span class="label">Total Employees</span>
                            <span class="value">${data.total_employees || 0}</span>
                        </div>
                    `;
                })
                .catch(error => {
                    document.getElementById('projectSummary').innerHTML =
                        `<div class="error">Error loading data: ${error}</div>`;
                });
        }

        function loadDailySummary(date) {
            fetch(`/api/daily-summary?date=${date}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('employeeDetails').innerHTML =
                            `<div class="error">Error: ${data.error}</div>`;
                        return;
                    }

                    let html = '';
                    if (data.data.length === 0) {
                        html = '<p>No employee time entries found for this date.</p>';
                    } else {
                        html = `<table>
                            <thead>
                                <tr>
                                    <th>Employee</th>
                                    <th>Employee ID</th>
                                    <th>Project</th>
                                    <th>Hours</th>
                                    <th>Clock In</th>
                                    <th>Clock Out</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>`;

                        data.data.forEach(entry => {
                            const statusClass = entry.Status === 'Approved' ? 'status-approved' : 'status-pending';
                            html += `<tr>
                                <td><strong>${entry.Employee}</strong></td>
                                <td>${entry.Employee_ID}</td>
                                <td><span class="project-badge">${entry.Project}</span></td>
                                <td><strong>${entry.Hours.toFixed(2)}</strong> hrs</td>
                                <td>${entry.Clock_In || 'N/A'}</td>
                                <td>${entry.Clock_Out || 'N/A'}</td>
                                <td><span class="status-badge ${statusClass}">${entry.Status}</span></td>
                            </tr>`;
                        });

                        html += '</tbody></table>';
                    }
                    document.getElementById('employeeDetails').innerHTML = html;
                })
                .catch(error => {
                    document.getElementById('employeeDetails').innerHTML =
                        `<div class="error">Error loading data: ${error}</div>`;
                });
        }

        function exportExcel() {
            const date = document.getElementById('reportDate').value;
            fetch(`/api/export-excel?date=${date}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Demo Report Generated!\\n\\n' + data.message + '\\n\\nNote: This is demo data for presentation purposes.');
                    } else {
                        alert('Error: ' + (data.error || 'Unknown error'));
                    }
                });
        }

        loadData();
        setInterval(loadData, 300000);
    </script>
</body>
</html>"""

    with open(os.path.join(templates_dir, 'demo_dashboard.html'), 'w') as f:
        f.write(html_content)


if __name__ == '__main__':
    create_demo_html_template()

    print("\n" + "="*70)
    print("CAPITOL ENGINEERING - DEMO MODE")
    print("="*70)
    print("\nThis is a demonstration version using sample data")
    print("Perfect for presentations and showing your team!")
    print("\nDemo Dashboard: http://localhost:5000")
    print("\nPress Ctrl+C to stop the demo server")
    print("="*70 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
