"""
Data Merger Module
Combines time tracking data (from Rippling API or demo) with budget data
Calculates metrics: budget %, remaining hours, status, etc.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from budget_manager import BudgetManager


class DataMerger:
    """Merges time tracking data with budget data and calculates metrics"""

    def __init__(self, use_demo_data: bool = True):
        self.use_demo_data = use_demo_data
        self.budget_manager = BudgetManager()

    def get_project_with_actuals(self, project_code: str, date: Optional[str] = None) -> Optional[Dict]:
        """
        Get a single project with budget data merged with actual hours

        Args:
            project_code: The project code (e.g., '25-2126')
            date: Date to get actuals for (YYYY-MM-DD), defaults to today

        Returns:
            Dictionary with complete project data including actuals
        """
        # Get budget data
        budget_data = self.budget_manager.get_project(project_code)
        if not budget_data:
            return None

        # Get actual hours (from Rippling API or demo data)
        if self.use_demo_data:
            actual_data = self._get_demo_time_data(project_code, date)
        else:
            actual_data = self._get_rippling_time_data(project_code, date)

        # Merge budget and actual data
        return self._merge_project_data(budget_data, actual_data)

    def get_all_projects_with_actuals(self, date: Optional[str] = None) -> List[Dict]:
        """
        Get all projects with budget and actual data

        Args:
            date: Date to get actuals for (YYYY-MM-DD), defaults to today

        Returns:
            List of project dictionaries with complete data
        """
        budget_projects = self.budget_manager.get_all_projects()
        merged_projects = []

        for budget_project in budget_projects:
            # Get actual hours
            if self.use_demo_data:
                actual_data = self._get_demo_time_data(budget_project['project_code'], date)
            else:
                actual_data = self._get_rippling_time_data(budget_project['project_code'], date)

            # Merge and add to list
            merged = self._merge_project_data(budget_project, actual_data)
            merged_projects.append(merged)

        return merged_projects

    def _merge_project_data(self, budget_data: Dict, actual_data: Dict) -> Dict:
        """Merge budget and actual data, calculate metrics"""
        project = budget_data.copy()

        # Add actual hours data
        project['total_hours_worked'] = actual_data.get('total_hours', 0)
        project['today_hours'] = actual_data.get('today_hours', 0)
        project['employee_hours'] = actual_data.get('employee_hours', [])
        project['timesheet_entries'] = actual_data.get('timesheet_entries', [])

        # Calculate metrics
        budget_hours = project.get('budget_hours', 0)
        total_hours = project['total_hours_worked']

        project['hours_remaining'] = max(0, budget_hours - total_hours)
        project['budget_usage_percent'] = (total_hours / budget_hours * 100) if budget_hours > 0 else 0
        project['crew_size'] = len(project['employee_hours'])

        # Calculate status
        usage_percent = project['budget_usage_percent']
        if usage_percent >= 100:
            project['status'] = 'over_budget'
        elif usage_percent >= 90:
            project['status'] = 'at_risk'
        elif usage_percent < 20:
            project['status'] = 'early_stage'
        else:
            project['status'] = 'on_track'

        # Merge task-level actuals
        if 'tasks' in project and project['tasks']:
            project['tasks'] = self._merge_task_data(
                project['tasks'],
                actual_data.get('task_hours', {})
            )

        return project

    def _merge_task_data(self, budget_tasks: List[Dict], actual_task_hours: Dict[str, float]) -> List[Dict]:
        """Merge budget tasks with actual hours per task"""
        merged_tasks = []

        for task in budget_tasks:
            task_name = task['task_name']
            estimated = task['estimated_hours']
            actual = actual_task_hours.get(task_name, 0)

            merged_tasks.append({
                'task_name': task_name,
                'estimated_hours': estimated,
                'actual_hours': actual,
                'remaining_hours': max(0, estimated - actual),
                'percent_complete': (actual / estimated * 100) if estimated > 0 else 0,
                'status': self._calculate_task_status(actual, estimated)
            })

        return merged_tasks

    def _calculate_task_status(self, actual: float, estimated: float) -> str:
        """Calculate task status based on actual vs estimated hours"""
        if estimated == 0:
            return 'early_stage'

        percent = (actual / estimated) * 100

        if percent >= 100:
            return 'over_budget'
        elif percent >= 90:
            return 'at_risk'
        elif percent < 20:
            return 'early_stage'
        else:
            return 'on_track'

    def _get_demo_time_data(self, project_code: str, date: Optional[str] = None) -> Dict:
        """Generate demo time tracking data for a project"""
        # Demo employees
        employees = [
            {'name': 'Mike Johnson', 'role': 'Welder'},
            {'name': 'Sarah Chen', 'role': 'Fabricator'},
            {'name': 'Tom Rodriguez', 'role': 'Fitter'},
            {'name': 'Lisa Anderson', 'role': 'Welder'},
            {'name': 'James Wilson', 'role': 'QC Inspector'},
            {'name': 'Maria Garcia', 'role': 'Foreman'},
        ]

        # Get budget data to determine realistic hours
        budget_data = self.budget_manager.get_project(project_code)
        if not budget_data:
            return {
                'total_hours': 0,
                'today_hours': 0,
                'employee_hours': [],
                'timesheet_entries': [],
                'task_hours': {}
            }

        budget_hours = budget_data.get('budget_hours', 100)
        tasks = budget_data.get('tasks', [])

        # Generate somewhat realistic hours (50-80% of budget)
        total_hours = budget_hours * random.uniform(0.5, 0.8)

        # Distribute hours among employees
        num_employees = random.randint(3, 6)
        selected_employees = random.sample(employees, num_employees)

        employee_hours = []
        timesheet_entries = []
        task_hours = {}

        # Distribute total hours among employees
        remaining_hours = total_hours
        for i, employee in enumerate(selected_employees):
            if i == len(selected_employees) - 1:
                # Last employee gets remaining hours
                emp_hours = remaining_hours
            else:
                # Random distribution
                emp_hours = remaining_hours * random.uniform(0.1, 0.3)
                remaining_hours -= emp_hours

            # Today's hours (0-10)
            today_hours = random.uniform(0, 10)

            employee_hours.append({
                'employee_name': employee['name'],
                'role': employee['role'],
                'total_hours': round(emp_hours, 2),
                'today_hours': round(today_hours, 2),
                'percent_of_total': round((emp_hours / total_hours * 100), 1) if total_hours > 0 else 0
            })

            # Generate some timesheet entries for this employee
            for day in range(7):
                entry_date = (datetime.now() - timedelta(days=day)).strftime('%Y-%m-%d')
                day_hours = random.uniform(6, 10) if random.random() > 0.2 else 0

                if day_hours > 0:
                    # Assign to a random task
                    task_name = random.choice(tasks)['task_name'] if tasks else 'General Work'

                    # Add to task hours
                    task_hours[task_name] = task_hours.get(task_name, 0) + day_hours

                    timesheet_entries.append({
                        'date': entry_date,
                        'employee_name': employee['name'],
                        'task': task_name,
                        'hours': round(day_hours, 2),
                        'clock_in': '07:00',
                        'clock_out': f'{7 + int(day_hours)}:{int((day_hours % 1) * 60):02d}'
                    })

        # Calculate today's total hours
        today_hours = sum(emp['today_hours'] for emp in employee_hours)

        # If we have tasks but no task_hours calculated, distribute total_hours
        if tasks and not task_hours:
            remaining = total_hours
            for i, task in enumerate(tasks):
                if i == len(tasks) - 1:
                    task_hours[task['task_name']] = remaining
                else:
                    task_portion = remaining * (task['estimated_hours'] / budget_hours)
                    task_hours[task['task_name']] = task_portion
                    remaining -= task_portion

        return {
            'total_hours': round(total_hours, 2),
            'today_hours': round(today_hours, 2),
            'employee_hours': sorted(employee_hours, key=lambda x: x['total_hours'], reverse=True),
            'timesheet_entries': sorted(timesheet_entries, key=lambda x: x['date'], reverse=True),
            'task_hours': {k: round(v, 2) for k, v in task_hours.items()}
        }

    def _get_rippling_time_data(self, project_code: str, date: Optional[str] = None) -> Dict:
        """
        Get actual time data from Rippling API

        TODO: Implement when Rippling API is connected
        This will:
        1. Call rippling_api_client.get_time_entries()
        2. Filter by project_code (job_code)
        3. Aggregate hours by employee
        4. Format data to match demo data structure
        """
        # Placeholder - will implement with real Rippling API
        return self._get_demo_time_data(project_code, date)


# Convenience functions
def get_project_data(project_code: str, use_demo: bool = True) -> Optional[Dict]:
    """Quick access to get merged project data"""
    merger = DataMerger(use_demo_data=use_demo)
    return merger.get_project_with_actuals(project_code)


def get_all_projects_data(use_demo: bool = True) -> List[Dict]:
    """Quick access to get all merged project data"""
    merger = DataMerger(use_demo_data=use_demo)
    return merger.get_all_projects_with_actuals()


if __name__ == '__main__':
    # Test the data merger
    import json

    # First, ensure we have sample budget data
    from budget_manager import BudgetManager

    manager = BudgetManager()

    # Add sample project if not exists
    manager.add_project(
        project_code='25-2126',
        project_name='Lithium Nevada - Thacker Pass Ducting',
        budget_hours=320,
        hourly_rate=85
    )

    manager.add_task('25-2126', 'Fabrication', 120)
    manager.add_task('25-2126', 'Welding', 140)
    manager.add_task('25-2126', 'QC/Inspection', 60)

    # Test merger
    merger = DataMerger(use_demo_data=True)
    project = merger.get_project_with_actuals('25-2126')

    print('Merged Project Data:')
    print(json.dumps(project, indent=2))

    print('\nData merger test completed successfully')
