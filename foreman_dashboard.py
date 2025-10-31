"""
Simple Web Dashboard for Foremen - Capitol Engineering Time Tracking
Provides an easy-to-use web interface for viewing daily labor reports

Date created: 2025-10-30
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
from project_labor_reports import ProjectLaborReportGenerator
import os

app = Flask(__name__)

# Initialize report generator
try:
    generator = ProjectLaborReportGenerator()
except Exception as e:
    print(f"Warning: Could not initialize report generator: {e}")
    generator = None


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/daily-summary')
def get_daily_summary():
    """API endpoint to get daily summary data"""
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

    try:
        if not generator:
            return jsonify({'error': 'Report generator not initialized. Check API token.'}), 500

        daily_summary = generator.get_daily_project_summary(date)

        if daily_summary.empty:
            return jsonify({
                'date': date,
                'data': [],
                'message': 'No time entries found for this date'
            })

        # Convert DataFrame to list of dictionaries
        data = daily_summary.to_dict(orient='records')

        return jsonify({
            'date': date,
            'data': data,
            'total_records': len(data)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/project-breakdown')
def get_project_breakdown():
    """API endpoint to get project breakdown"""
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

    try:
        if not generator:
            return jsonify({'error': 'Report generator not initialized. Check API token.'}), 500

        project_breakdown = generator.get_project_breakdown(date)

        if project_breakdown.empty:
            return jsonify({
                'date': date,
                'data': [],
                'message': 'No projects found for this date'
            })

        data = project_breakdown.to_dict(orient='records')

        return jsonify({
            'date': date,
            'data': data,
            'total_hours': sum(item['Total_Hours'] for item in data),
            'total_employees': sum(item['Employee_Count'] for item in data)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/weekly-hours')
def get_weekly_hours():
    """API endpoint to get weekly hours"""
    try:
        if not generator:
            return jsonify({'error': 'Report generator not initialized. Check API token.'}), 500

        weekly_hours = generator.get_employee_weekly_hours()

        if weekly_hours.empty:
            return jsonify({
                'data': [],
                'message': 'No weekly data found'
            })

        # Convert to format suitable for JSON
        data = weekly_hours.reset_index().to_dict(orient='records')

        return jsonify({
            'data': data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export-excel')
def export_to_excel():
    """Generate and download Excel report"""
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

    try:
        if not generator:
            return jsonify({'error': 'Report generator not initialized. Check API token.'}), 500

        output_path = f"Capitol_Labor_Report_{date}.xlsx"
        generator.export_foreman_report(output_path, date)

        return jsonify({
            'success': True,
            'file': output_path,
            'message': f'Report generated: {output_path}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def create_html_template():
    """Create the HTML template for the dashboard"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Capitol Engineering - Labor Dashboard</title>
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

        .controls {
            display: flex;
            gap: 15px;
            align-items: center;
            margin-top: 15px;
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
            transition: background 0.3s;
        }

        .controls button:hover {
            background: #5568d3;
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
            background: #f8f9fa;
            border-radius: 5px;
            margin-bottom: 10px;
        }

        .stat-box .label {
            font-weight: 600;
            color: #666;
        }

        .stat-box .value {
            font-weight: bold;
            color: #667eea;
            font-size: 1.2em;
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
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Capitol Engineering - Daily Labor Dashboard</h1>
            <p>Real-time project labor monitoring from Rippling</p>
            <div class="controls">
                <label for="reportDate">Select Date:</label>
                <input type="date" id="reportDate" value="">
                <button onclick="loadData()">Load Report</button>
                <button onclick="exportExcel()">Export to Excel</button>
                <button onclick="loadData()">Refresh</button>
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
    </div>

    <script>
        // Set today's date on load
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

                    // Update project summary
                    let html = '';
                    if (data.data.length === 0) {
                        html = '<p>No projects found for this date.</p>';
                    } else {
                        html = '<table><thead><tr><th>Project</th><th>Hours</th><th>Employees</th></tr></thead><tbody>';
                        data.data.forEach(project => {
                            html += `<tr>
                                <td><span class="project-badge">${project.Project}</span></td>
                                <td>${project.Total_Hours.toFixed(2)} hrs</td>
                                <td>${project.Employee_Count}</td>
                            </tr>`;
                        });
                        html += '</tbody></table>';
                    }
                    document.getElementById('projectSummary').innerHTML = html;

                    // Update quick stats
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
                                    <th>Project</th>
                                    <th>Hours</th>
                                    <th>Clock In</th>
                                    <th>Clock Out</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>`;

                        data.data.forEach(entry => {
                            html += `<tr>
                                <td>${entry.Employee}</td>
                                <td><span class="project-badge">${entry.Project}</span></td>
                                <td>${entry.Hours.toFixed(2)} hrs</td>
                                <td>${entry.Clock_In || 'N/A'}</td>
                                <td>${entry.Clock_Out || 'N/A'}</td>
                                <td>${entry.Status}</td>
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
                        alert(data.message);
                    } else {
                        alert('Error: ' + (data.error || 'Unknown error'));
                    }
                });
        }

        // Load data on page load
        loadData();

        // Auto-refresh every 5 minutes
        setInterval(loadData, 300000);
    </script>
</body>
</html>"""

    with open(os.path.join(templates_dir, 'dashboard.html'), 'w') as f:
        f.write(html_content)


if __name__ == '__main__':
    # Create template if it doesn't exist
    create_html_template()

    print("\n" + "="*60)
    print("Capitol Engineering - Foreman Dashboard")
    print("="*60)
    print("\nStarting web server...")
    print("Dashboard will be available at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    print("="*60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
