# Rippling Time Tracking Integration - Project Overview

Date created: 2025-10-30
Company: Capitol Engineering (capitolaz.com)
Previous System: TSheets (Intuit)
New System: Rippling

## What This System Does

This integration connects to your Rippling account and automatically pulls time tracking data to generate daily labor reports for your foremen. They can easily monitor employees and see what projects everyone is working on.

## Files Created

### Core Integration Files

1. **rippling_api_client.py**
   - Connects to Rippling REST API
   - Handles authentication with API tokens
   - Provides methods to fetch employees, time entries, and job dimensions
   - Base URL: https://rest.ripplingapis.com

2. **project_labor_reports.py**
   - Generates daily project summaries
   - Creates Excel reports with multiple sheets
   - Calculates hours from time entries
   - Groups data by project and employee

3. **foreman_dashboard.py**
   - Web-based dashboard for foremen
   - Real-time viewing of labor data
   - Browser-based interface (no Excel needed)
   - Auto-refreshes every 5 minutes

### Configuration Files

4. **.env.example**
   - Template for API token configuration
   - Copy to .env and add your actual token

5. **requirements.txt**
   - Python package dependencies
   - requests, pandas, openpyxl, flask, python-dotenv

### Documentation

6. **README.md**
   - Complete documentation
   - Setup instructions
   - Usage examples
   - Troubleshooting guide

7. **QUICKSTART.md**
   - 5-minute setup guide
   - Quick reference for daily usage
   - Common tasks and solutions

8. **PROJECT_OVERVIEW.md** (this file)
   - High-level system overview
   - Architecture explanation

### Utilities

9. **setup.bat**
   - Automated setup script for Windows
   - Installs packages and tests connection

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Rippling Cloud                          │
│  (Employee time tracking, projects, hours)                  │
└───────────────────────┬─────────────────────────────────────┘
                        │ REST API
                        │ (API Token Auth)
                        ↓
┌─────────────────────────────────────────────────────────────┐
│              rippling_api_client.py                         │
│  - Authentication                                            │
│  - API calls (GET /users, /time-entries, /job-dimensions)  │
│  - Error handling                                            │
└──────────────────┬──────────────────────────────────────────┘
                   │
         ┌─────────┴─────────┐
         ↓                   ↓
┌──────────────────┐  ┌─────────────────────┐
│  Excel Reports   │  │  Web Dashboard      │
│                  │  │                     │
│  project_labor_  │  │  foreman_          │
│  reports.py      │  │  dashboard.py      │
│                  │  │                     │
│  • Daily Summary │  │  • Browser UI      │
│  • Project Totals│  │  • Real-time       │
│  • Weekly Hours  │  │  • Auto-refresh    │
└──────────────────┘  └─────────────────────┘
         │                     │
         ↓                     ↓
   [.xlsx files]         [http://localhost:5000]
         │                     │
         ↓                     ↓
    Project Managers      Foremen (any device)
```

## Data Flow

1. **Employee clocks in/out in Rippling**
   - Assigns project/job code
   - Time entry is recorded

2. **API Integration pulls data**
   - Authenticates with API token
   - Fetches time entries for date range
   - Retrieves employee information
   - Gets project/job dimensions

3. **Data Processing**
   - Groups by project and employee
   - Calculates total hours
   - Formats for reports

4. **Report Generation**
   - Excel: Multi-sheet workbook with detailed data
   - Web: Interactive dashboard with live updates

5. **Foreman Access**
   - View reports via web browser
   - Export to Excel as needed
   - Monitor daily progress

## Key Features

### For Foremen
- Easy-to-read web dashboard
- See all employees and their projects at a glance
- View daily hours by project
- Access from any computer with a browser
- No Excel or technical knowledge required

### For Project Managers
- Detailed Excel reports with multiple views
- Historical data tracking
- Weekly summaries
- Export capabilities
- Automated report generation

### For Administrators
- Simple API token authentication
- Secure environment variable storage
- Automated setup scripts
- Comprehensive error handling
- Easy to maintain and update

## Report Types

### 1. Daily Summary Report
Shows all employees, their projects, and hours for a specific day.

Columns:
- Employee Name
- Employee ID
- Project/Job Code
- Job Dimension
- Hours Worked
- Clock In Time
- Clock Out Time
- Status

### 2. Project Breakdown Report
Summary view of total hours per project.

Columns:
- Project Name
- Total Hours
- Employee Count

### 3. Weekly Hours Report
7-day view of all employee hours by project.

Format:
- Rows: Employee + Project
- Columns: Each date
- Values: Hours worked

## API Endpoints Used

1. **GET /users**
   - Fetches employee list
   - Returns: employee_id, first_name, last_name, status

2. **GET /time-entries**
   - Fetches time tracking data
   - Parameters: start_date, end_date, limit, cursor
   - Returns: Time entry records with hours and job codes

3. **GET /job-dimensions**
   - Fetches project/cost center configuration
   - Returns: Dimension list for job tracking

## Security Considerations

- API token stored in .env file (not committed to git)
- Token expires after 30 days of inactivity
- Use environment variables, never hardcode tokens
- Treat API tokens like passwords
- Each user should generate their own token

## Deployment Options

### Option 1: Local Computer
- Run on project manager or admin computer
- Foremen access via network
- Simple setup, no server required

### Option 2: Dedicated Server
- Install on office server
- 24/7 availability
- Centralized management
- Better for larger teams

### Option 3: Cloud Deployment
- Deploy to Heroku, AWS, or Azure
- Access from anywhere
- Most reliable uptime
- Requires cloud account

## Automation Possibilities

### Daily Reports
- Windows Task Scheduler
- Generate reports at end of day
- Email distribution (future enhancement)

### Dashboard Monitoring
- Keep web server running 24/7
- Auto-refresh for real-time data
- Mobile-friendly interface

### Alerts and Notifications
- Low hours warnings (future)
- Missing time entry alerts (future)
- Project over-budget notifications (future)

## Migration from TSheets

Key Differences:
- TSheets: Intuit-based system
- Rippling: More comprehensive HR platform

Benefits of Rippling:
- Unified HR/Payroll/Time tracking
- Better API documentation
- More flexible job dimension tracking
- Modern REST API

Migration Steps:
1. Export historical data from TSheets (if needed)
2. Set up Rippling API access
3. Configure job codes to match projects
4. Train employees on new system
5. Run parallel for testing period

## Future Enhancements

Potential additions:
1. Email report distribution
2. Mobile app interface
3. Budget tracking integration
4. Real-time notifications
5. Historical trend analysis
6. Predictive analytics
7. Integration with accounting software
8. Custom report builder
9. Multi-location support
10. Role-based access control

## Support and Maintenance

### Regular Maintenance
- Refresh API token every 30 days
- Update Python packages periodically
- Backup report history
- Monitor for API changes

### Common Issues
- Expired API tokens
- Network connectivity
- Missing job codes
- Time zone differences

### Getting Help
- Rippling API docs: developer.rippling.com
- Capitol Engineering: Contact Blake Holmes
- System documentation: See README.md and QUICKSTART.md

## Success Metrics

Track these to measure system effectiveness:
- Time saved generating reports
- Foreman adoption rate
- Report accuracy
- System uptime
- User satisfaction

## Contact Information

Capitol Engineering
Website: www.capitolaz.com
Contact: Blake Holmes

Rippling Support
Website: developer.rippling.com
Account Manager: [Your account manager]

---

Date: 2025-10-30 20:30
Version: 1.0
Status: Initial Implementation Complete
