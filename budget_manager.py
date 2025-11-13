"""
Budget Manager Module
Handles CRUD operations for project budgets and tasks
Data stored in SQLite database (budgets.db)
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

DATABASE_FILE = 'budgets.db'


class BudgetManager:
    """Manages project budget data storage and retrieval"""

    def __init__(self, db_file: str = DATABASE_FILE):
        self.db_file = db_file
        self._init_database()

    def _init_database(self):
        """Initialize database tables if they don't exist"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                project_code TEXT PRIMARY KEY,
                project_name TEXT NOT NULL,
                budget_hours REAL NOT NULL,
                hourly_rate REAL DEFAULT 85.0,
                start_date TEXT,
                target_end_date TEXT,
                status TEXT DEFAULT 'active',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_code TEXT NOT NULL,
                task_name TEXT NOT NULL,
                estimated_hours REAL NOT NULL,
                sort_order INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_code) REFERENCES projects(project_code) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        conn.close()

    def add_project(self, project_code: str, project_name: str, budget_hours: float,
                   hourly_rate: float = 85.0, start_date: Optional[str] = None,
                   target_end_date: Optional[str] = None, status: str = 'active') -> bool:
        """Add a new project to the budget database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO projects (project_code, project_name, budget_hours, hourly_rate,
                                     start_date, target_end_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (project_code, project_name, budget_hours, hourly_rate,
                 start_date, target_end_date, status))

            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False  # Project already exists

    def update_project(self, project_code: str, **kwargs) -> bool:
        """Update project fields"""
        valid_fields = ['project_name', 'budget_hours', 'hourly_rate',
                       'start_date', 'target_end_date', 'status']

        updates = {k: v for k, v in kwargs.items() if k in valid_fields}
        if not updates:
            return False

        updates['updated_at'] = datetime.now().isoformat()

        set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [project_code]

        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(f'''
                UPDATE projects
                SET {set_clause}
                WHERE project_code = ?
            ''', values)

            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    def delete_project(self, project_code: str) -> bool:
        """Delete a project and all its tasks"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('DELETE FROM projects WHERE project_code = ?', (project_code,))

            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    def get_project(self, project_code: str) -> Optional[Dict]:
        """Get a single project with its tasks"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM projects WHERE project_code = ?', (project_code,))
        project_row = cursor.fetchone()

        if not project_row:
            conn.close()
            return None

        project = dict(project_row)

        # Get tasks for this project
        cursor.execute('''
            SELECT task_name, estimated_hours
            FROM tasks
            WHERE project_code = ?
            ORDER BY sort_order, id
        ''', (project_code,))

        project['tasks'] = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return project

    def get_all_projects(self, include_inactive: bool = False) -> List[Dict]:
        """Get all projects with their tasks"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if include_inactive:
            cursor.execute('SELECT * FROM projects ORDER BY project_code')
        else:
            cursor.execute('SELECT * FROM projects WHERE status = "active" ORDER BY project_code')

        projects = [dict(row) for row in cursor.fetchall()]

        # Get tasks for each project
        for project in projects:
            cursor.execute('''
                SELECT task_name, estimated_hours
                FROM tasks
                WHERE project_code = ?
                ORDER BY sort_order, id
            ''', (project['project_code'],))

            project['tasks'] = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return projects

    def add_task(self, project_code: str, task_name: str, estimated_hours: float,
                sort_order: int = 0) -> bool:
        """Add a task to a project"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO tasks (project_code, task_name, estimated_hours, sort_order)
                VALUES (?, ?, ?, ?)
            ''', (project_code, task_name, estimated_hours, sort_order))

            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False

    def update_task(self, task_id: int, task_name: Optional[str] = None,
                   estimated_hours: Optional[float] = None,
                   sort_order: Optional[int] = None) -> bool:
        """Update a task"""
        updates = {}
        if task_name is not None:
            updates['task_name'] = task_name
        if estimated_hours is not None:
            updates['estimated_hours'] = estimated_hours
        if sort_order is not None:
            updates['sort_order'] = sort_order

        if not updates:
            return False

        set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [task_id]

        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(f'''
                UPDATE tasks
                SET {set_clause}
                WHERE id = ?
            ''', values)

            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    def clear_tasks(self, project_code: str) -> bool:
        """Remove all tasks for a project"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('DELETE FROM tasks WHERE project_code = ?', (project_code,))

            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False

    def import_projects_from_json(self, json_data: str) -> Tuple[int, List[str]]:
        """
        Import projects from JSON string
        Returns: (success_count, error_list)
        """
        try:
            data = json.loads(json_data)
            if not isinstance(data, list):
                data = [data]

            success_count = 0
            errors = []

            for item in data:
                try:
                    project_code = item.get('project_code')
                    if not project_code:
                        errors.append('Missing project_code')
                        continue

                    # Add or update project
                    self.add_project(
                        project_code=project_code,
                        project_name=item.get('project_name', ''),
                        budget_hours=float(item.get('budget_hours', 0)),
                        hourly_rate=float(item.get('hourly_rate', 85.0)),
                        start_date=item.get('start_date'),
                        target_end_date=item.get('target_end_date'),
                        status=item.get('status', 'active')
                    )

                    # Clear existing tasks and add new ones
                    self.clear_tasks(project_code)

                    tasks = item.get('tasks', [])
                    for idx, task in enumerate(tasks):
                        self.add_task(
                            project_code=project_code,
                            task_name=task.get('name', task.get('task_name', '')),
                            estimated_hours=float(task.get('estimated_hours', 0)),
                            sort_order=idx
                        )

                    success_count += 1

                except Exception as e:
                    errors.append(f"{item.get('project_code', 'Unknown')}: {str(e)}")

            return success_count, errors

        except json.JSONDecodeError as e:
            return 0, [f"JSON parse error: {str(e)}"]

    def export_to_json(self) -> str:
        """Export all projects to JSON string"""
        projects = self.get_all_projects(include_inactive=True)

        # Format tasks properly
        for project in projects:
            project['tasks'] = [
                {
                    'name': task['task_name'],
                    'estimated_hours': task['estimated_hours']
                }
                for task in project.get('tasks', [])
            ]

        return json.dumps(projects, indent=2)


# Convenience functions for quick access
def get_project_budget(project_code: str) -> Optional[Dict]:
    """Quick access to get a project's budget info"""
    manager = BudgetManager()
    return manager.get_project(project_code)


def get_all_budgets() -> List[Dict]:
    """Quick access to get all project budgets"""
    manager = BudgetManager()
    return manager.get_all_projects()


if __name__ == '__main__':
    # Test the budget manager
    manager = BudgetManager()

    # Add sample project
    manager.add_project(
        project_code='25-2126',
        project_name='Lithium Nevada - Thacker Pass Ducting',
        budget_hours=320,
        hourly_rate=85,
        start_date='2025-01-15',
        target_end_date='2025-03-15'
    )

    # Add tasks
    manager.add_task('25-2126', 'Fabrication', 120, 0)
    manager.add_task('25-2126', 'Welding', 140, 1)
    manager.add_task('25-2126', 'QC/Inspection', 60, 2)

    # Test retrieval
    project = manager.get_project('25-2126')
    print('Project:', json.dumps(project, indent=2))

    print('\nBudget manager test completed successfully')
