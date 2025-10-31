"""
Enhanced Demo Mode - Capitol Engineering Time Tracking System
Shows full API capabilities and data insights

Date created: 2025-10-30
"""

from flask import Flask, render_template, jsonify, request, send_file
from datetime import datetime, timedelta
from demo_data_generator import DemoDataGenerator
import pandas as pd
import os
import json
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
            'Role': employee.get('role', 'N/A'),
            'Project': entry.get('job_code', 'No Project'),
            'Project_Name': entry.get('job_name', 'N/A'),
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

    project_summary = daily_summary.groupby(['Project', 'Project_Name']).agg({
        'Hours': 'sum',
        'Employee': 'count'
    }).reset_index()

    project_summary.columns = ['Project', 'Project_Name', 'Total_Hours', 'Employee_Count']
    project_summary = project_summary.sort_values('Total_Hours', ascending=False)

    return project_summary


def get_weekly_trends():
    """Generate weekly trend data"""
    trends = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=6-i)).strftime('%Y-%m-%d')
        entries = get_demo_time_entries(date)
        total_hours = sum(e['hours'] for e in entries)
        employee_count = len(set(e['employee_id'] for e in entries))

        trends.append({
            'date': date,
            'total_hours': total_hours,
            'employee_count': employee_count
        })

    return trends


def get_employee_analytics():
    """Get employee-level analytics"""
    today = datetime.now().strftime('%Y-%m-%d')
    entries = get_demo_time_entries(today)
    employee_map = {emp['id']: emp for emp in demo_cache['employees']}

    analytics = []
    employee_hours = {}

    for entry in entries:
        emp_id = entry['employee_id']
        if emp_id not in employee_hours:
            employee_hours[emp_id] = 0
        employee_hours[emp_id] += entry['hours']

    for emp_id, hours in employee_hours.items():
        emp = employee_map.get(emp_id, {})
        analytics.append({
            'name': f"{emp.get('first_name', '')} {emp.get('last_name', '')}",
            'role': emp.get('role', 'N/A'),
            'hours': hours,
            'utilization': min(100, (hours / 8) * 100)
        })

    return sorted(analytics, key=lambda x: x['hours'], reverse=True)


@app.route('/')
def index():
    """Main enhanced demo dashboard"""
    return render_template('demo_enhanced.html')


@app.route('/api/daily-summary')
def get_daily_summary():
    """API endpoint to get daily summary data"""
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
    """API endpoint to get project breakdown"""
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


@app.route('/api/weekly-trends')
def get_weekly_trends_api():
    """API endpoint for weekly trends"""
    try:
        trends = get_weekly_trends()
        return jsonify({
            'trends': trends,
            'demo_mode': True
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/employee-analytics')
def get_employee_analytics_api():
    """API endpoint for employee analytics"""
    try:
        analytics = get_employee_analytics()
        return jsonify({
            'analytics': analytics,
            'demo_mode': True
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/capabilities')
def get_api_capabilities():
    """Show what the Rippling API can do"""
    capabilities = {
        'employees': {
            'endpoint': 'GET /users',
            'description': 'Retrieve all employee information',
            'data_fields': [
                'Employee ID',
                'First Name / Last Name',
                'Job Title / Role',
                'Department',
                'Employment Status',
                'Hire Date',
                'Manager Information',
                'Contact Details'
            ],
            'demo_count': len(demo_cache['employees']),
            'use_cases': [
                'Crew roster management',
                'Role-based reporting',
                'Organizational charts',
                'Contact directories'
            ]
        },
        'time_entries': {
            'endpoint': 'GET /time-entries',
            'description': 'Retrieve time tracking records',
            'data_fields': [
                'Employee ID',
                'Date / Time',
                'Clock In / Out',
                'Total Hours',
                'Job Code / Project',
                'Approval Status',
                'Break Times',
                'Overtime Flags'
            ],
            'demo_count': len(get_demo_time_entries(datetime.now().strftime('%Y-%m-%d'))),
            'use_cases': [
                'Daily labor reports',
                'Project cost tracking',
                'Payroll verification',
                'Overtime management'
            ]
        },
        'job_dimensions': {
            'endpoint': 'GET /job-dimensions',
            'description': 'Retrieve project and cost center configuration',
            'data_fields': [
                'Dimension ID',
                'Dimension Name',
                'Job Codes',
                'Cost Centers',
                'Department Mapping',
                'Custom Fields'
            ],
            'demo_count': len(demo_cache['projects']),
            'use_cases': [
                'Project tracking',
                'Cost allocation',
                'Budget management',
                'Job costing'
            ]
        },
        'advanced_features': {
            'endpoint': 'Various endpoints',
            'description': 'Additional API capabilities',
            'features': [
                'Webhooks for real-time updates',
                'Pagination for large datasets',
                'Filtering and search',
                'Custom field support',
                'Date range queries',
                'Bulk operations',
                'Export capabilities',
                'Historical data access'
            ]
        },
        'integration_benefits': [
            'Real-time data synchronization',
            'No manual data entry',
            'Single source of truth',
            'Automated reporting',
            'Reduced errors',
            'Better decision making',
            'Time savings',
            'Cost visibility'
        ]
    }

    return jsonify(capabilities)


@app.route('/api/export-excel')
def export_to_excel():
    """Generate enhanced Excel report"""
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

    try:
        output_path = f"Capitol_Labor_Report_ENHANCED_{date}.xlsx"

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Sheet 1: Daily summary
            daily_summary = process_demo_daily_summary(date)
            if not daily_summary.empty:
                daily_summary.to_excel(writer, sheet_name='Daily Summary', index=False)

            # Sheet 2: Project breakdown
            project_breakdown = process_demo_project_breakdown(date)
            if not project_breakdown.empty:
                project_breakdown.to_excel(writer, sheet_name='Project Totals', index=False)

            # Sheet 3: Weekly trends
            trends = get_weekly_trends()
            trends_df = pd.DataFrame(trends)
            trends_df.to_excel(writer, sheet_name='Weekly Trends', index=False)

            # Sheet 4: Employee analytics
            analytics = get_employee_analytics()
            analytics_df = pd.DataFrame(analytics)
            analytics_df.to_excel(writer, sheet_name='Employee Analytics', index=False)

            # Sheet 5: API Info
            api_info = pd.DataFrame([{
                'System': 'Rippling Time Tracking Integration',
                'Company': 'Capitol Engineering',
                'Website': 'www.capitolaz.com',
                'API Base URL': 'https://rest.ripplingapis.com',
                'Demo Mode': 'Yes - Sample Data',
                'Generated': datetime.now().strftime('%Y-%m-%d %I:%M %p')
            }])
            api_info.to_excel(writer, sheet_name='System Info', index=False)

        return jsonify({
            'success': True,
            'file': output_path,
            'message': f'Enhanced demo report generated: {output_path}',
            'demo_mode': True
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def create_enhanced_html_template():
    """Create enhanced HTML template with charts and API info"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Capitol Engineering - Enhanced Labor Dashboard (DEMO)</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
        }

        .header {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }

        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .tab {
            padding: 12px 24px;
            background: #f0f0f0;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s;
        }

        .tab:hover {
            background: #e0e0e0;
        }

        .tab.active {
            background: #667eea;
            color: white;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .controls {
            display: flex;
            gap: 15px;
            align-items: center;
            margin-top: 15px;
            flex-wrap: wrap;
        }

        .controls input, .controls select {
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

        .project-badge {
            display: inline-block;
            padding: 5px 12px;
            background: #667eea;
            color: white;
            border-radius: 15px;
            font-size: 0.9em;
            font-weight: 600;
        }

        .api-endpoint {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }

        .api-endpoint code {
            background: #333;
            color: #0f0;
            padding: 2px 8px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }

        .feature-list {
            list-style: none;
            padding: 0;
        }

        .feature-list li {
            padding: 10px;
            margin: 5px 0;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 3px solid #667eea;
        }

        .feature-list li:before {
            content: "✓ ";
            color: #28a745;
            font-weight: bold;
            margin-right: 8px;
        }

        .chart-container {
            position: relative;
            height: 300px;
            margin-top: 20px;
        }

        .filter-section {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }

        .filter-section label {
            margin-right: 10px;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="demo-banner">
            ENHANCED DEMO MODE - Full API Capabilities Showcase
        </div>

        <div class="header">
            <h1>Capitol Engineering - Advanced Labor Dashboard</h1>
            <p>Rippling API Integration - Real-time Analytics & Insights</p>

            <div class="tabs">
                <button class="tab active" onclick="switchTab('dashboard')">Dashboard</button>
                <button class="tab" onclick="switchTab('analytics')">Analytics</button>
                <button class="tab" onclick="switchTab('api')">API Capabilities</button>
                <button class="tab" onclick="switchTab('employees')">Employee Details</button>
            </div>

            <div class="controls">
                <label for="reportDate">Select Date:</label>
                <input type="date" id="reportDate" value="">
                <button onclick="loadAllData()">Refresh All</button>
                <button onclick="exportExcel()" style="background: #28a745;">Export to Excel</button>
            </div>
        </div>

        <!-- Dashboard Tab -->
        <div id="dashboard-tab" class="tab-content active">
            <div class="dashboard-grid">
                <div class="card">
                    <h2>Project Summary</h2>
                    <div id="projectSummary">Loading...</div>
                </div>

                <div class="card">
                    <h2>Quick Stats</h2>
                    <div id="quickStats">Loading...</div>
                </div>
            </div>

            <div class="card">
                <h2>Today's Labor Activity</h2>
                <div class="filter-section">
                    <label>Filter by:</label>
                    <select id="projectFilter" onchange="applyFilters()">
                        <option value="">All Projects</option>
                    </select>
                    <select id="roleFilter" onchange="applyFilters()">
                        <option value="">All Roles</option>
                    </select>
                    <input type="text" id="searchBox" placeholder="Search employee..." onkeyup="applyFilters()">
                </div>
                <div id="employeeDetails">Loading...</div>
            </div>
        </div>

        <!-- Analytics Tab -->
        <div id="analytics-tab" class="tab-content">
            <div class="dashboard-grid">
                <div class="card">
                    <h2>Weekly Hours Trend</h2>
                    <div class="chart-container">
                        <canvas id="weeklyChart"></canvas>
                    </div>
                </div>

                <div class="card">
                    <h2>Employee Utilization</h2>
                    <div class="chart-container">
                        <canvas id="utilizationChart"></canvas>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2>Project Distribution</h2>
                <div class="chart-container">
                    <canvas id="projectChart"></canvas>
                </div>
            </div>
        </div>

        <!-- API Capabilities Tab -->
        <div id="api-tab" class="tab-content">
            <div class="card">
                <h2>Rippling API Integration</h2>
                <p>This system uses the official Rippling REST API to provide real-time access to your time tracking data.</p>
                <div id="apiCapabilities">Loading API information...</div>
            </div>
        </div>

        <!-- Employee Details Tab -->
        <div id="employees-tab" class="tab-content">
            <div class="card">
                <h2>Detailed Employee Analytics</h2>
                <div id="employeeAnalytics">Loading...</div>
            </div>
        </div>
    </div>

    <script>
        let allData = [];
        let weeklyChart, utilizationChart, projectChart;

        document.getElementById('reportDate').valueAsDate = new Date();

        function switchTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));

            event.target.classList.add('active');
            document.getElementById(tabName + '-tab').classList.add('active');

            if (tabName === 'analytics') {
                loadAnalytics();
            } else if (tabName === 'api') {
                loadAPICapabilities();
            } else if (tabName === 'employees') {
                loadEmployeeAnalytics();
            }
        }

        function loadAllData() {
            const date = document.getElementById('reportDate').value;
            loadProjectBreakdown(date);
            loadDailySummary(date);
        }

        function loadProjectBreakdown(date) {
            fetch(`/api/project-breakdown?date=${date}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('projectSummary').innerHTML = `<div class="error">${data.error}</div>`;
                        return;
                    }

                    // Update project filter
                    const projectFilter = document.getElementById('projectFilter');
                    projectFilter.innerHTML = '<option value="">All Projects</option>';
                    data.data.forEach(p => {
                        projectFilter.innerHTML += `<option value="${p.Project}">${p.Project}</option>`;
                    });

                    let html = '<table><thead><tr><th>Project</th><th>Description</th><th>Hours</th><th>Employees</th></tr></thead><tbody>';
                    data.data.forEach(project => {
                        html += `<tr>
                            <td><span class="project-badge">${project.Project}</span></td>
                            <td>${project.Project_Name}</td>
                            <td><strong>${project.Total_Hours.toFixed(2)}</strong> hrs</td>
                            <td>${project.Employee_Count}</td>
                        </tr>`;
                    });
                    html += '</tbody></table>';
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
                        <div class="stat-box">
                            <span class="label">Avg Hours/Employee</span>
                            <span class="value">${(data.total_hours / data.total_employees).toFixed(1)} hrs</span>
                        </div>
                    `;
                });
        }

        function loadDailySummary(date) {
            fetch(`/api/daily-summary?date=${date}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('employeeDetails').innerHTML = `<div class="error">${data.error}</div>`;
                        return;
                    }

                    allData = data.data;

                    // Update role filter
                    const roleFilter = document.getElementById('roleFilter');
                    const roles = [...new Set(allData.map(e => e.Role))];
                    roleFilter.innerHTML = '<option value="">All Roles</option>';
                    roles.forEach(r => {
                        roleFilter.innerHTML += `<option value="${r}">${r}</option>`;
                    });

                    renderEmployeeTable(allData);
                });
        }

        function renderEmployeeTable(data) {
            let html = `<table>
                <thead>
                    <tr>
                        <th>Employee</th>
                        <th>ID</th>
                        <th>Role</th>
                        <th>Project</th>
                        <th>Hours</th>
                        <th>Clock In</th>
                        <th>Clock Out</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>`;

            data.forEach(entry => {
                const statusClass = entry.Status === 'Approved' ? 'status-approved' : 'status-pending';
                html += `<tr>
                    <td><strong>${entry.Employee}</strong></td>
                    <td>${entry.Employee_ID}</td>
                    <td>${entry.Role}</td>
                    <td><span class="project-badge">${entry.Project}</span></td>
                    <td><strong>${entry.Hours.toFixed(2)}</strong> hrs</td>
                    <td>${entry.Clock_In}</td>
                    <td>${entry.Clock_Out}</td>
                    <td><span class="status-badge ${statusClass}">${entry.Status}</span></td>
                </tr>`;
            });

            html += '</tbody></table>';
            document.getElementById('employeeDetails').innerHTML = html;
        }

        function applyFilters() {
            const projectFilter = document.getElementById('projectFilter').value;
            const roleFilter = document.getElementById('roleFilter').value;
            const searchText = document.getElementById('searchBox').value.toLowerCase();

            let filtered = allData.filter(entry => {
                const matchProject = !projectFilter || entry.Project === projectFilter;
                const matchRole = !roleFilter || entry.Role === roleFilter;
                const matchSearch = !searchText || entry.Employee.toLowerCase().includes(searchText);
                return matchProject && matchRole && matchSearch;
            });

            renderEmployeeTable(filtered);
        }

        function loadAnalytics() {
            fetch('/api/weekly-trends')
                .then(response => response.json())
                .then(data => {
                    const labels = data.trends.map(t => t.date);
                    const hours = data.trends.map(t => t.total_hours);
                    const employees = data.trends.map(t => t.employee_count);

                    if (weeklyChart) weeklyChart.destroy();

                    weeklyChart = new Chart(document.getElementById('weeklyChart'), {
                        type: 'line',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Total Hours',
                                data: hours,
                                borderColor: '#667eea',
                                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                                tension: 0.4
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                title: { display: true, text: '7-Day Labor Hours Trend' }
                            }
                        }
                    });
                });

            fetch('/api/employee-analytics')
                .then(response => response.json())
                .then(data => {
                    const names = data.analytics.slice(0, 10).map(a => a.name.split(' ')[0]);
                    const hours = data.analytics.slice(0, 10).map(a => a.hours);

                    if (utilizationChart) utilizationChart.destroy();

                    utilizationChart = new Chart(document.getElementById('utilizationChart'), {
                        type: 'bar',
                        data: {
                            labels: names,
                            datasets: [{
                                label: 'Hours Worked',
                                data: hours,
                                backgroundColor: '#667eea'
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                title: { display: true, text: 'Top 10 Employees by Hours' }
                            }
                        }
                    });
                });

            const date = document.getElementById('reportDate').value;
            fetch(`/api/project-breakdown?date=${date}`)
                .then(response => response.json())
                .then(data => {
                    if (data.data) {
                        const projects = data.data.map(p => p.Project);
                        const hours = data.data.map(p => p.Total_Hours);

                        if (projectChart) projectChart.destroy();

                        projectChart = new Chart(document.getElementById('projectChart'), {
                            type: 'doughnut',
                            data: {
                                labels: projects,
                                datasets: [{
                                    data: hours,
                                    backgroundColor: [
                                        '#667eea', '#764ba2', '#f093fb', '#f5576c',
                                        '#4facfe', '#00f2fe', '#43e97b', '#38f9d7'
                                    ]
                                }]
                            },
                            options: {
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {
                                    title: { display: true, text: 'Hours Distribution by Project' }
                                }
                            }
                        });
                    }
                });
        }

        function loadAPICapabilities() {
            fetch('/api/capabilities')
                .then(response => response.json())
                .then(data => {
                    let html = '';

                    // Employees API
                    html += '<div class="api-endpoint">';
                    html += `<h3>Employee Data API</h3>`;
                    html += `<p><code>${data.employees.endpoint}</code></p>`;
                    html += `<p>${data.employees.description}</p>`;
                    html += `<p><strong>Demo Data:</strong> ${data.employees.demo_count} employees</p>`;
                    html += '<p><strong>Available Fields:</strong></p><ul class="feature-list">';
                    data.employees.data_fields.forEach(field => {
                        html += `<li>${field}</li>`;
                    });
                    html += '</ul></div>';

                    // Time Entries API
                    html += '<div class="api-endpoint">';
                    html += `<h3>Time Tracking API</h3>`;
                    html += `<p><code>${data.time_entries.endpoint}</code></p>`;
                    html += `<p>${data.time_entries.description}</p>`;
                    html += `<p><strong>Demo Data:</strong> ${data.time_entries.demo_count} time entries today</p>`;
                    html += '<p><strong>Available Fields:</strong></p><ul class="feature-list">';
                    data.time_entries.data_fields.forEach(field => {
                        html += `<li>${field}</li>`;
                    });
                    html += '</ul></div>';

                    // Job Dimensions API
                    html += '<div class="api-endpoint">';
                    html += `<h3>Project Tracking API</h3>`;
                    html += `<p><code>${data.job_dimensions.endpoint}</code></p>`;
                    html += `<p>${data.job_dimensions.description}</p>`;
                    html += `<p><strong>Demo Data:</strong> ${data.job_dimensions.demo_count} active projects</p>`;
                    html += '<p><strong>Available Fields:</strong></p><ul class="feature-list">';
                    data.job_dimensions.data_fields.forEach(field => {
                        html += `<li>${field}</li>`;
                    });
                    html += '</ul></div>';

                    // Integration Benefits
                    html += '<div class="api-endpoint">';
                    html += '<h3>Integration Benefits</h3>';
                    html += '<ul class="feature-list">';
                    data.integration_benefits.forEach(benefit => {
                        html += `<li>${benefit}</li>`;
                    });
                    html += '</ul></div>';

                    document.getElementById('apiCapabilities').innerHTML = html;
                });
        }

        function loadEmployeeAnalytics() {
            fetch('/api/employee-analytics')
                .then(response => response.json())
                .then(data => {
                    let html = '<table><thead><tr><th>Employee</th><th>Role</th><th>Hours Today</th><th>Utilization</th></tr></thead><tbody>';

                    data.analytics.forEach(emp => {
                        const utilColor = emp.utilization >= 90 ? '#28a745' : emp.utilization >= 70 ? '#ffc107' : '#dc3545';
                        html += `<tr>
                            <td><strong>${emp.name}</strong></td>
                            <td>${emp.role}</td>
                            <td>${emp.hours.toFixed(2)} hrs</td>
                            <td>
                                <div style="background: #f0f0f0; height: 20px; border-radius: 10px; overflow: hidden;">
                                    <div style="width: ${emp.utilization}%; background: ${utilColor}; height: 100%; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.8em; font-weight: bold;">
                                        ${emp.utilization.toFixed(0)}%
                                    </div>
                                </div>
                            </td>
                        </tr>`;
                    });

                    html += '</tbody></table>';
                    document.getElementById('employeeAnalytics').innerHTML = html;
                });
        }

        function exportExcel() {
            const date = document.getElementById('reportDate').value;
            fetch(`/api/export-excel?date=${date}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Enhanced Demo Report Generated!\\n\\n' + data.message + '\\n\\nIncludes: Daily Summary, Project Totals, Weekly Trends, Employee Analytics, and System Info');
                    } else {
                        alert('Error: ' + (data.error || 'Unknown error'));
                    }
                });
        }

        loadAllData();
    </script>
</body>
</html>"""

    with open(os.path.join(templates_dir, 'demo_enhanced.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)


if __name__ == '__main__':
    create_enhanced_html_template()

    print("\n" + "="*70)
    print("CAPITOL ENGINEERING - ENHANCED DEMO MODE")
    print("="*70)
    print("\nFull API Capabilities Showcase")
    print("Features:")
    print("  - Interactive charts and analytics")
    print("  - API endpoint documentation")
    print("  - Employee utilization tracking")
    print("  - Advanced filtering and search")
    print("  - Weekly trend analysis")
    print("\nDemo Dashboard: http://localhost:5000")
    print("\nPress Ctrl+C to stop the demo server")
    print("="*70 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
