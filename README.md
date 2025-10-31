# Rippling Time Tracking Integration for Capitol Engineering

This system connects to your Rippling account to pull time tracking data and generate daily labor reports for project monitoring by foremen.

Date created: 2025-10-30

## DEMO MODE AVAILABLE

Want to see it in action before setting up? **Double-click START_DEMO.bat** for a fully functional demo with sample data - perfect for presentations!

See DEMO_README.md and DEMO_GUIDE.md for demo instructions.

## Features

- Pull employee time entries from Rippling API
- Generate daily project labor reports
- Track hours by project and employee
- Export reports to Excel for distribution
- Web dashboard for easy viewing

## Setup Instructions

### 1. Get Your Rippling API Token

1. Log into your Rippling account at rippling.com
2. Navigate to the API Tokens app (you may need to contact your account manager if you don't see it)
3. Generate a new API token
4. Copy the token (you'll need it in the next step)

Important: API tokens expire after 30 days of inactivity, so you'll need to regenerate them periodically.

### 2. Install Required Python Packages

```bash
pip install -r requirements.txt
```

This installs:
- requests (for API calls)
- pandas (for data processing)
- openpyxl (for Excel export)
- python-dotenv (for environment variables)

### 3. Configure Your API Token

Copy the example environment file:
```bash
copy .env.example .env
```

Edit the .env file and add your actual API token:
```
RIPPLING_API_TOKEN=your_actual_token_here
```

### 4. Test the Connection

Run the test script to verify your API connection:
```bash
python rippling_api_client.py
```

You should see:
```
✓ API client initialized successfully
✓ Successfully retrieved X employees (sample)
✓ Successfully retrieved X time entries for today
Connection test successful!
```

### 5. Generate Your First Report

Run the report generator:
```bash
python project_labor_reports.py
```

This will:
- Print a console summary of today's labor
- Generate an Excel file: Capitol_Labor_Report_YYYY-MM-DD.xlsx

## Usage

### Generate Daily Reports

```python
from project_labor_reports import ProjectLaborReportGenerator

generator = ProjectLaborReportGenerator()

# Print today's summary to console
generator.print_daily_summary()

# Generate Excel report for today
generator.export_foreman_report("labor_report.xlsx")

# Generate report for specific date
generator.export_foreman_report("labor_report_2025-10-15.xlsx", date="2025-10-15")
```

### Query Specific Data

```python
# Get daily project summary as DataFrame
daily_summary = generator.get_daily_project_summary("2025-10-30")

# Get project-level totals
project_totals = generator.get_project_breakdown("2025-10-30")

# Get weekly hours for all employees
weekly_hours = generator.get_employee_weekly_hours()
```

## Report Structure

The Excel reports contain three sheets:

1. **Daily Summary**: Detailed breakdown of all employees, projects, and hours for the day
   - Employee name and ID
   - Project/job code
   - Hours worked
   - Clock in/out times
   - Status

2. **Project Totals**: Summary view by project
   - Project name
   - Total hours
   - Number of employees

3. **Weekly Hours**: 7-day view of employee hours
   - Shows last 7 days
   - Broken down by employee and project

## Automating Daily Reports

### Option 1: Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 5:00 PM (or whenever you want the report)
4. Action: Start a program
   - Program: python
   - Arguments: "C:\path\to\project_labor_reports.py"
5. Save the task

### Option 2: Python Script with Schedule

```python
import schedule
import time
from project_labor_reports import ProjectLaborReportGenerator

def generate_daily_report():
    generator = ProjectLaborReportGenerator()
    today = datetime.now().strftime('%Y-%m-%d')
    generator.export_foreman_report(f"reports/labor_report_{today}.xlsx")

# Run every day at 5:00 PM
schedule.every().day.at("17:00").do(generate_daily_report)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Troubleshooting

### API Token Issues

If you get authentication errors:
- Check that your .env file has the correct token
- Verify the token hasn't expired (30 days of inactivity)
- Make sure there are no extra spaces in the .env file

### No Time Entries Found

If reports show no data:
- Verify employees are clocking in/out in Rippling
- Check that job codes/projects are assigned to time entries
- Confirm the date range is correct

### Missing Project Names

If projects show as "No Project":
- Ensure job dimensions are configured in Rippling
- Verify employees are selecting projects when clocking in
- Contact Rippling support to enable job tracking features

## Next Steps

1. Set up the web dashboard (foreman_dashboard.py) for easy browser access
2. Configure automated daily email delivery of reports
3. Customize report columns to match your specific needs
4. Add additional filtering (by foreman, by job site, etc.)

## Support

For Rippling API issues:
- Visit: developer.rippling.com
- Contact your Rippling account manager

For Capitol Engineering specific questions:
- Contact: Blake Holmes
- Company: capitolaz.com
