"""
Workforce-Style Project Dashboard
QuickBooks Workforce-inspired interface for Capitol Engineering
"""

from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
from datetime import datetime
import json
import io
from typing import Dict, List

from budget_manager import BudgetManager
from data_merger import DataMerger
import pandas as pd

app = Flask(__name__)
CORS(app)

# Initialize managers
budget_manager = BudgetManager()
data_merger = DataMerger(use_demo_data=True)


def init_sample_data():
    """Initialize sample budget data for demo"""
    sample_projects = [
        {
            'project_code': '25-2126',
            'project_name': 'Lithium Nevada - Thacker Pass Ducting',
            'budget_hours': 320,
            'hourly_rate': 85,
            'start_date': '2025-01-15',
            'target_end_date': '2025-03-15',
            'tasks': [
                {'name': 'Fabrication', 'estimated_hours': 120},
                {'name': 'Welding', 'estimated_hours': 140},
                {'name': 'QC/Inspection', 'estimated_hours': 60}
            ]
        },
        {
            'project_code': '25-2350',
            'project_name': 'Forest Energy - Stack Ducting',
            'budget_hours': 480,
            'hourly_rate': 90,
            'start_date': '2025-02-01',
            'target_end_date': '2025-04-30',
            'tasks': [
                {'name': 'Material Prep', 'estimated_hours': 80},
                {'name': 'Fabrication', 'estimated_hours': 180},
                {'name': 'Welding', 'estimated_hours': 160},
                {'name': 'Finishing', 'estimated_hours': 60}
            ]
        },
        {
            'project_code': '25-2117',
            'project_name': 'Industrial Complex - Steel Frame',
            'budget_hours': 600,
            'hourly_rate': 95,
            'start_date': '2025-01-10',
            'target_end_date': '2025-05-15',
            'tasks': [
                {'name': 'Foundation Work', 'estimated_hours': 100},
                {'name': 'Steel Erection', 'estimated_hours': 250},
                {'name': 'Welding', 'estimated_hours': 180},
                {'name': 'QC/Testing', 'estimated_hours': 70}
            ]
        },
        {
            'project_code': '25-2574',
            'project_name': 'Mining Support Structure',
            'budget_hours': 280,
            'hourly_rate': 88,
            'start_date': '2025-02-15',
            'target_end_date': '2025-03-30',
            'tasks': [
                {'name': 'Design Verification', 'estimated_hours': 40},
                {'name': 'Fabrication', 'estimated_hours': 120},
                {'name': 'Assembly', 'estimated_hours': 80},
                {'name': 'Installation Support', 'estimated_hours': 40}
            ]
        },
        {
            'project_code': 'SHOP',
            'project_name': 'Shop Maintenance & Cleanup',
            'budget_hours': 160,
            'hourly_rate': 65,
            'start_date': '2025-01-01',
            'target_end_date': '2025-12-31',
            'tasks': [
                {'name': 'Equipment Maintenance', 'estimated_hours': 80},
                {'name': 'Shop Cleanup', 'estimated_hours': 40},
                {'name': 'Tool Organization', 'estimated_hours': 40}
            ]
        },
        {
            'project_code': '25-1998',
            'project_name': 'Refinery Platform Assembly',
            'budget_hours': 520,
            'hourly_rate': 92,
            'start_date': '2025-01-20',
            'target_end_date': '2025-04-15',
            'tasks': [
                {'name': 'Platform Fabrication', 'estimated_hours': 200},
                {'name': 'Railing & Stairs', 'estimated_hours': 120},
                {'name': 'Welding & QC', 'estimated_hours': 160},
                {'name': 'Surface Treatment', 'estimated_hours': 40}
            ]
        }
    ]

    # Check if data already exists
    existing_projects = budget_manager.get_all_projects()
    if len(existing_projects) > 0:
        print(f"Sample data already exists ({len(existing_projects)} projects)")
        return

    # Import sample data
    json_data = json.dumps(sample_projects)
    success_count, errors = budget_manager.import_projects_from_json(json_data)

    print(f"Initialized {success_count} sample projects")
    if errors:
        print(f"Errors: {errors}")


# Routes

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('workforce_dashboard.html')


@app.route('/api/projects')
def get_projects():
    """Get all projects with budget and actual data"""
    try:
        projects = data_merger.get_all_projects_with_actuals()

        # Calculate summary stats
        total_projects = len(projects)
        on_track = len([p for p in projects if p.get('status') == 'on_track'])
        at_risk = len([p for p in projects if p.get('status') == 'at_risk'])
        over_budget = len([p for p in projects if p.get('status') == 'over_budget'])

        return jsonify({
            'success': True,
            'projects': projects,
            'summary': {
                'total': total_projects,
                'on_track': on_track,
                'at_risk': at_risk,
                'over_budget': over_budget
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/project/<project_code>')
def get_project(project_code):
    """Get detailed data for a single project"""
    try:
        project = data_merger.get_project_with_actuals(project_code)

        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404

        return jsonify({
            'success': True,
            'project': project
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/project/<project_code>/tasks')
def get_project_tasks(project_code):
    """Get task breakdown for a project"""
    try:
        project = data_merger.get_project_with_actuals(project_code)

        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404

        return jsonify({
            'success': True,
            'tasks': project.get('tasks', [])
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/project/<project_code>/users')
def get_project_users(project_code):
    """Get employee hours for a project"""
    try:
        project = data_merger.get_project_with_actuals(project_code)

        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404

        return jsonify({
            'success': True,
            'employees': project.get('employee_hours', [])
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/project/<project_code>/timesheets')
def get_project_timesheets(project_code):
    """Get detailed timesheet entries for a project"""
    try:
        project = data_merger.get_project_with_actuals(project_code)

        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404

        # Get filters from query params
        employee_filter = request.args.get('employee')
        task_filter = request.args.get('task')

        timesheets = project.get('timesheet_entries', [])

        # Apply filters
        if employee_filter:
            timesheets = [t for t in timesheets if t.get('employee_name') == employee_filter]

        if task_filter:
            timesheets = [t for t in timesheets if t.get('task') == task_filter]

        return jsonify({
            'success': True,
            'timesheets': timesheets
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/budget/<project_code>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_budget(project_code):
    """Manage project budget (CRUD operations)"""
    try:
        if request.method == 'GET':
            project = budget_manager.get_project(project_code)
            if not project:
                return jsonify({'success': False, 'error': 'Project not found'}), 404
            return jsonify({'success': True, 'project': project})

        elif request.method in ['POST', 'PUT']:
            data = request.json

            # Add or update project
            budget_manager.add_project(
                project_code=project_code,
                project_name=data.get('project_name', ''),
                budget_hours=float(data.get('budget_hours', 0)),
                hourly_rate=float(data.get('hourly_rate', 85)),
                start_date=data.get('start_date'),
                target_end_date=data.get('target_end_date'),
                status=data.get('status', 'active')
            )

            # Clear and re-add tasks
            budget_manager.clear_tasks(project_code)
            tasks = data.get('tasks', [])
            for idx, task in enumerate(tasks):
                budget_manager.add_task(
                    project_code=project_code,
                    task_name=task.get('name', task.get('task_name', '')),
                    estimated_hours=float(task.get('estimated_hours', 0)),
                    sort_order=idx
                )

            return jsonify({'success': True, 'message': 'Budget updated'})

        elif request.method == 'DELETE':
            success = budget_manager.delete_project(project_code)
            if success:
                return jsonify({'success': True, 'message': 'Project deleted'})
            else:
                return jsonify({'success': False, 'error': 'Project not found'}), 404

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/export/excel/<project_code>')
def export_project_excel(project_code):
    """Export project data to Excel"""
    try:
        project = data_merger.get_project_with_actuals(project_code)

        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404

        # Create Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Summary sheet
            summary_data = {
                'Metric': [
                    'Project Code',
                    'Project Name',
                    'Budget Hours',
                    'Hours Worked',
                    'Hours Remaining',
                    'Budget Usage %',
                    'Status',
                    'Crew Size',
                    'Hourly Rate',
                    'Start Date',
                    'Target End Date'
                ],
                'Value': [
                    project.get('project_code', ''),
                    project.get('project_name', ''),
                    project.get('budget_hours', 0),
                    project.get('total_hours_worked', 0),
                    project.get('hours_remaining', 0),
                    f"{project.get('budget_usage_percent', 0):.1f}%",
                    project.get('status', '').replace('_', ' ').title(),
                    project.get('crew_size', 0),
                    f"${project.get('hourly_rate', 0):.2f}",
                    project.get('start_date', ''),
                    project.get('target_end_date', '')
                ]
            }
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='Summary', index=False)

            # Tasks sheet
            if project.get('tasks'):
                df_tasks = pd.DataFrame(project['tasks'])
                df_tasks.to_excel(writer, sheet_name='Tasks', index=False)

            # Employee hours sheet
            if project.get('employee_hours'):
                df_employees = pd.DataFrame(project['employee_hours'])
                df_employees.to_excel(writer, sheet_name='Labor', index=False)

            # Timesheets sheet
            if project.get('timesheet_entries'):
                df_timesheets = pd.DataFrame(project['timesheet_entries'])
                df_timesheets.to_excel(writer, sheet_name='Timesheets', index=False)

        output.seek(0)

        filename = f"{project_code}_report_{datetime.now().strftime('%Y%m%d')}.xlsx"

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/summary')
def get_summary():
    """Get dashboard summary statistics"""
    try:
        projects = data_merger.get_all_projects_with_actuals()

        total_budget_hours = sum(p.get('budget_hours', 0) for p in projects)
        total_hours_worked = sum(p.get('total_hours_worked', 0) for p in projects)
        total_today_hours = sum(p.get('today_hours', 0) for p in projects)

        summary = {
            'total_projects': len(projects),
            'active_projects': len([p for p in projects if p.get('status') != 'inactive']),
            'on_track': len([p for p in projects if p.get('status') == 'on_track']),
            'at_risk': len([p for p in projects if p.get('status') == 'at_risk']),
            'over_budget': len([p for p in projects if p.get('status') == 'over_budget']),
            'total_budget_hours': round(total_budget_hours, 2),
            'total_hours_worked': round(total_hours_worked, 2),
            'total_today_hours': round(total_today_hours, 2),
            'overall_budget_usage': round((total_hours_worked / total_budget_hours * 100), 1) if total_budget_hours > 0 else 0
        }

        return jsonify({
            'success': True,
            'summary': summary
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    import os

    print("Initializing Capitol Engineering Workforce Dashboard...")

    # Initialize sample data
    init_sample_data()

    print("\nStarting server...")
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'

    print(f"Dashboard URL: http://localhost:{port}")
    print("\nAPI Endpoints:")
    print("  GET  /api/projects - All projects overview")
    print("  GET  /api/project/<code> - Project details")
    print("  GET  /api/project/<code>/tasks - Task breakdown")
    print("  GET  /api/project/<code>/users - Employee hours")
    print("  GET  /api/project/<code>/timesheets - Timesheet entries")
    print("  GET  /api/export/excel/<code> - Export to Excel")
    print("  POST /api/budget/<code> - Add/update budget")
    print("\nPress Ctrl+C to stop")

    app.run(host='0.0.0.0', port=port, debug=debug)
