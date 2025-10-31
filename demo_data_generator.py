"""
Demo Data Generator for Capitol Engineering Time Tracking System
Creates realistic sample data for demonstrations without requiring Rippling API access

Date created: 2025-10-30
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List
import json


class DemoDataGenerator:
    """Generate realistic demo data for time tracking demonstrations"""

    def __init__(self):
        """Initialize demo data generator with Capitol Engineering specific data"""

        # Capitol Engineering employees
        self.employees = [
            {"id": "emp_001", "first_name": "John", "last_name": "Martinez", "employee_id": "CE-101", "role": "Welder"},
            {"id": "emp_002", "first_name": "Sarah", "last_name": "Johnson", "employee_id": "CE-102", "role": "Fabricator"},
            {"id": "emp_003", "first_name": "Mike", "last_name": "Thompson", "employee_id": "CE-103", "role": "Fitter"},
            {"id": "emp_004", "first_name": "Lisa", "last_name": "Anderson", "employee_id": "CE-104", "role": "Welder"},
            {"id": "emp_005", "first_name": "David", "last_name": "Garcia", "employee_id": "CE-105", "role": "Fabricator"},
            {"id": "emp_006", "first_name": "Emily", "last_name": "Rodriguez", "employee_id": "CE-106", "role": "QC Inspector"},
            {"id": "emp_007", "first_name": "James", "last_name": "Williams", "employee_id": "CE-107", "role": "Fitter"},
            {"id": "emp_008", "first_name": "Maria", "last_name": "Lopez", "employee_id": "CE-108", "role": "Welder"},
            {"id": "emp_009", "first_name": "Robert", "last_name": "Davis", "employee_id": "CE-109", "role": "Foreman"},
            {"id": "emp_010", "first_name": "Jennifer", "last_name": "Miller", "employee_id": "CE-110", "role": "Fabricator"},
            {"id": "emp_011", "first_name": "Chris", "last_name": "Wilson", "employee_id": "CE-111", "role": "Painter"},
            {"id": "emp_012", "first_name": "Amanda", "last_name": "Brown", "employee_id": "CE-112", "role": "Fitter"},
            {"id": "emp_013", "first_name": "Daniel", "last_name": "Taylor", "employee_id": "CE-113", "role": "Welder"},
            {"id": "emp_014", "first_name": "Jessica", "last_name": "Moore", "employee_id": "CE-114", "role": "Admin"},
            {"id": "emp_015", "first_name": "Kevin", "last_name": "Jackson", "employee_id": "CE-115", "role": "Detailer"},
        ]

        # Capitol Engineering active projects
        self.projects = [
            {"code": "25-2126", "name": "Lithium Nevada - Thacker Pass Ducting", "type": "Fabrication"},
            {"code": "25-2350", "name": "Forest Energy - Stack Ducting", "type": "Fabrication"},
            {"code": "25-2117", "name": "Industrial Complex - Steel Frame", "type": "Structural"},
            {"code": "25-2574", "name": "Mining Support Structure", "type": "Structural"},
            {"code": "SHOP", "name": "Shop Maintenance & Cleanup", "type": "Internal"},
            {"code": "25-1998", "name": "Refinery Platform Assembly", "type": "Fabrication"},
            {"code": "25-2201", "name": "Water Treatment Piping", "type": "Piping"},
        ]

        # Job dimensions
        self.dimensions = [
            {"id": "dim_001", "name": "Project Code", "type": "project"},
            {"id": "dim_002", "name": "Cost Center", "type": "department"},
        ]

    def generate_time_entry(self, employee: Dict, project: Dict, date: datetime,
                           hours: float = None) -> Dict:
        """
        Generate a single time entry

        Args:
            employee: Employee dictionary
            project: Project dictionary
            date: Date of the time entry
            hours: Optional specific hours (random if not provided)

        Returns:
            Time entry dictionary
        """
        if hours is None:
            # Random hours between 6-10
            hours = round(random.uniform(6.0, 10.0), 2)

        # Generate clock in time (between 6 AM - 8 AM)
        clock_in_hour = random.randint(6, 8)
        clock_in_minute = random.choice([0, 15, 30, 45])
        clock_in = date.replace(hour=clock_in_hour, minute=clock_in_minute, second=0)

        # Calculate clock out time
        clock_out = clock_in + timedelta(hours=hours)

        return {
            "id": f"time_{employee['id']}_{date.strftime('%Y%m%d')}_{project['code']}",
            "employee_id": employee["id"],
            "user_id": employee["id"],
            "date": date.strftime('%Y-%m-%d'),
            "start_time": clock_in.isoformat(),
            "end_time": clock_out.isoformat(),
            "hours": hours,
            "job_code": project["code"],
            "job_name": project["name"],
            "dimension_name": "Project Code",
            "status": "Approved" if random.random() > 0.1 else "Pending",
            "notes": ""
        }

    def generate_daily_time_entries(self, date: datetime = None) -> List[Dict]:
        """
        Generate time entries for a full day

        Args:
            date: Date to generate entries for (defaults to today)

        Returns:
            List of time entry dictionaries
        """
        if not date:
            date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        time_entries = []

        # Assign employees to projects (some employees may work on multiple projects)
        for employee in self.employees:
            # 90% chance employee works today
            if random.random() < 0.9:
                # Most employees work on one project
                num_projects = 1 if random.random() < 0.8 else 2

                # Select random projects
                employee_projects = random.sample(self.projects, num_projects)

                if num_projects == 1:
                    # Full day on one project
                    time_entries.append(
                        self.generate_time_entry(employee, employee_projects[0], date)
                    )
                else:
                    # Split day between two projects
                    hours_1 = round(random.uniform(3.0, 6.0), 2)
                    hours_2 = round(random.uniform(3.0, 6.0), 2)

                    time_entries.append(
                        self.generate_time_entry(employee, employee_projects[0], date, hours_1)
                    )
                    time_entries.append(
                        self.generate_time_entry(employee, employee_projects[1], date, hours_2)
                    )

        return time_entries

    def generate_week_time_entries(self, start_date: datetime = None) -> List[Dict]:
        """
        Generate time entries for a full week (5 work days)

        Args:
            start_date: Start date (Monday) for the week

        Returns:
            List of time entry dictionaries
        """
        if not start_date:
            # Start from last Monday
            today = datetime.now()
            start_date = today - timedelta(days=today.weekday())

        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

        all_entries = []

        # Generate 5 days (Monday-Friday)
        for day_offset in range(5):
            current_date = start_date + timedelta(days=day_offset)
            daily_entries = self.generate_daily_time_entries(current_date)
            all_entries.extend(daily_entries)

        return all_entries

    def generate_sample_employees(self) -> List[Dict]:
        """Get the list of demo employees"""
        return self.employees

    def generate_sample_projects(self) -> List[Dict]:
        """Get the list of demo projects"""
        return self.projects

    def save_demo_data(self, filename: str = "demo_data.json"):
        """
        Save complete demo dataset to JSON file

        Args:
            filename: Output filename
        """
        today = datetime.now()

        # Generate last 7 days of data
        week_start = today - timedelta(days=6)

        demo_data = {
            "generated_at": datetime.now().isoformat(),
            "employees": self.employees,
            "projects": self.projects,
            "dimensions": self.dimensions,
            "time_entries": self.generate_week_time_entries(week_start),
            "demo_info": {
                "company": "Capitol Engineering",
                "website": "www.capitolaz.com",
                "note": "This is demo data for demonstration purposes only"
            }
        }

        with open(filename, 'w') as f:
            json.dump(demo_data, f, indent=2)

        print(f"Demo data saved to {filename}")
        print(f"Employees: {len(demo_data['employees'])}")
        print(f"Projects: {len(demo_data['projects'])}")
        print(f"Time Entries: {len(demo_data['time_entries'])}")

    def print_sample_data(self):
        """Print sample of generated data"""
        print("\n" + "="*70)
        print("CAPITOL ENGINEERING - DEMO DATA SAMPLE")
        print("="*70)

        print("\nSample Employees:")
        print("-"*70)
        for emp in self.employees[:5]:
            print(f"  {emp['first_name']} {emp['last_name']} ({emp['employee_id']}) - {emp['role']}")
        print(f"  ... and {len(self.employees) - 5} more employees")

        print("\nActive Projects:")
        print("-"*70)
        for proj in self.projects:
            print(f"  {proj['code']}: {proj['name']} ({proj['type']})")

        print("\nSample Time Entries (Today):")
        print("-"*70)
        today_entries = self.generate_daily_time_entries()
        for entry in today_entries[:5]:
            emp = next(e for e in self.employees if e['id'] == entry['employee_id'])
            print(f"  {emp['first_name']} {emp['last_name']}: {entry['job_code']} - {entry['hours']} hrs")
        print(f"  ... and {len(today_entries) - 5} more entries")
        print("\n" + "="*70 + "\n")


def main():
    """Generate and save demo data"""
    generator = DemoDataGenerator()

    # Print sample
    generator.print_sample_data()

    # Save complete dataset
    generator.save_demo_data()


if __name__ == "__main__":
    main()
