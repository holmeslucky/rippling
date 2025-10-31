"""
Project Labor Report Generator for Capitol Engineering
Generates daily reports for foremen to monitor employee time tracking by project

Date created: 2025-10-30 20:15
"""

from datetime import datetime, timedelta
from typing import Dict, List
import pandas as pd
from rippling_api_client import RipplingAPIClient


class ProjectLaborReportGenerator:
    """Generate daily project labor reports from Rippling time tracking data"""

    def __init__(self, api_token: str = None):
        """Initialize the report generator with Rippling API client"""
        self.client = RipplingAPIClient(api_token)

    def get_daily_project_summary(self, date: str = None) -> pd.DataFrame:
        """
        Generate daily project summary showing all employees and their project assignments

        Args:
            date: Date in YYYY-MM-DD format (defaults to today)

        Returns:
            DataFrame with columns: Employee, Project, Hours, Status
        """
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        # Get time entries for the specified date
        time_entries = self.client.get_time_entries(start_date=date, end_date=date)

        # Get employee data
        employees = self.client.get_employees()
        employee_map = {emp['id']: emp for emp in employees}

        # Process time entries into report format
        report_data = []

        for entry in time_entries:
            employee_id = entry.get('employee_id') or entry.get('user_id')
            employee = employee_map.get(employee_id, {})

            report_data.append({
                'Employee': f"{employee.get('first_name', '')} {employee.get('last_name', '')}",
                'Employee_ID': employee.get('employee_id', 'N/A'),
                'Project': entry.get('job_code', 'No Project'),
                'Job_Dimension': entry.get('dimension_name', 'N/A'),
                'Hours': self._calculate_hours(entry),
                'Clock_In': entry.get('start_time', ''),
                'Clock_Out': entry.get('end_time', ''),
                'Status': entry.get('status', 'Active')
            })

        df = pd.DataFrame(report_data)

        if df.empty:
            print(f"No time entries found for {date}")
            return pd.DataFrame()

        # Sort by project, then employee name
        df = df.sort_values(['Project', 'Employee'])

        return df

    def get_project_breakdown(self, date: str = None) -> pd.DataFrame:
        """
        Generate project-level summary showing total hours per project

        Args:
            date: Date in YYYY-MM-DD format (defaults to today)

        Returns:
            DataFrame with columns: Project, Total_Hours, Employee_Count
        """
        daily_summary = self.get_daily_project_summary(date)

        if daily_summary.empty:
            return pd.DataFrame()

        project_summary = daily_summary.groupby('Project').agg({
            'Hours': 'sum',
            'Employee': 'count'
        }).reset_index()

        project_summary.columns = ['Project', 'Total_Hours', 'Employee_Count']
        project_summary = project_summary.sort_values('Total_Hours', ascending=False)

        return project_summary

    def get_employee_weekly_hours(self, employee_id: str = None) -> pd.DataFrame:
        """
        Get weekly hours breakdown for specific employee or all employees

        Args:
            employee_id: Optional specific employee ID

        Returns:
            DataFrame with employee hours by day
        """
        # Get last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=6)

        time_entries = self.client.get_time_entries(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )

        employees = self.client.get_employees()
        employee_map = {emp['id']: emp for emp in employees}

        weekly_data = []

        for entry in time_entries:
            emp_id = entry.get('employee_id') or entry.get('user_id')

            # Filter by specific employee if requested
            if employee_id and emp_id != employee_id:
                continue

            employee = employee_map.get(emp_id, {})
            entry_date = entry.get('date', entry.get('start_time', ''))[:10]

            weekly_data.append({
                'Employee': f"{employee.get('first_name', '')} {employee.get('last_name', '')}",
                'Date': entry_date,
                'Project': entry.get('job_code', 'No Project'),
                'Hours': self._calculate_hours(entry)
            })

        df = pd.DataFrame(weekly_data)

        if df.empty:
            return pd.DataFrame()

        # Pivot to show days as columns
        pivot = df.pivot_table(
            index=['Employee', 'Project'],
            columns='Date',
            values='Hours',
            aggfunc='sum',
            fill_value=0
        )

        return pivot

    def export_foreman_report(self, output_path: str, date: str = None):
        """
        Export comprehensive foreman report to Excel with multiple sheets

        Args:
            output_path: Path to save Excel file
            date: Date for the report (defaults to today)
        """
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Sheet 1: Daily project summary
            daily_summary = self.get_daily_project_summary(date)
            if not daily_summary.empty:
                daily_summary.to_excel(writer, sheet_name='Daily Summary', index=False)

            # Sheet 2: Project breakdown
            project_breakdown = self.get_project_breakdown(date)
            if not project_breakdown.empty:
                project_breakdown.to_excel(writer, sheet_name='Project Totals', index=False)

            # Sheet 3: Weekly hours
            weekly_hours = self.get_employee_weekly_hours()
            if not weekly_hours.empty:
                weekly_hours.to_excel(writer, sheet_name='Weekly Hours')

        print(f"Report generated successfully: {output_path}")

    def _calculate_hours(self, time_entry: Dict) -> float:
        """
        Calculate hours from a time entry

        Args:
            time_entry: Time entry dictionary from API

        Returns:
            Hours as float
        """
        # Check if hours are directly provided
        if 'hours' in time_entry:
            return float(time_entry['hours'])

        # Calculate from start and end times
        if 'start_time' in time_entry and 'end_time' in time_entry:
            try:
                start = datetime.fromisoformat(time_entry['start_time'].replace('Z', '+00:00'))
                end = datetime.fromisoformat(time_entry['end_time'].replace('Z', '+00:00'))
                duration = (end - start).total_seconds() / 3600
                return round(duration, 2)
            except Exception as e:
                print(f"Error calculating hours: {e}")
                return 0.0

        # If duration is provided in minutes
        if 'duration_minutes' in time_entry:
            return round(time_entry['duration_minutes'] / 60, 2)

        return 0.0

    def print_daily_summary(self, date: str = None):
        """
        Print a formatted daily summary to console

        Args:
            date: Date in YYYY-MM-DD format (defaults to today)
        """
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        print(f"\n{'='*80}")
        print(f"Capitol Engineering - Daily Labor Report")
        print(f"Date: {date}")
        print(f"{'='*80}\n")

        daily_summary = self.get_daily_project_summary(date)

        if daily_summary.empty:
            print("No time entries found for this date.")
            return

        # Print project breakdown
        project_breakdown = self.get_project_breakdown(date)
        print("PROJECT SUMMARY:")
        print("-" * 80)
        for _, row in project_breakdown.iterrows():
            print(f"  {row['Project']:<40} {row['Total_Hours']:>6.2f} hrs  ({int(row['Employee_Count'])} employees)")

        print(f"\n{'='*80}")
        print("DETAILED EMPLOYEE BREAKDOWN:")
        print("-" * 80)

        # Group by project
        for project in daily_summary['Project'].unique():
            project_data = daily_summary[daily_summary['Project'] == project]
            print(f"\n{project}:")
            for _, row in project_data.iterrows():
                print(f"  {row['Employee']:<30} {row['Hours']:>6.2f} hrs  ({row['Clock_In']} - {row['Clock_Out']})")

        print(f"\n{'='*80}\n")


def main():
    """Main function to generate daily reports"""
    generator = ProjectLaborReportGenerator()

    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')

    # Print console summary
    generator.print_daily_summary(today)

    # Export to Excel
    output_file = f"Capitol_Labor_Report_{today}.xlsx"
    generator.export_foreman_report(output_file, today)


if __name__ == "__main__":
    main()
