# Quick Start Guide - Rippling Time Tracking Integration

Date created: 2025-10-30

## Getting Started in 5 Minutes

### Step 1: Get Your API Token

1. Log into Rippling: https://rippling.com
2. Go to API Tokens app (or contact your account manager)
3. Generate new token and copy it

### Step 2: Setup Environment

Open Command Prompt or PowerShell in this directory and run:

```bash
pip install -r requirements.txt
```

### Step 3: Configure API Token

Copy the example file:
```bash
copy .env.example .env
```

Edit .env and paste your token:
```
RIPPLING_API_TOKEN=paste_your_token_here
```

### Step 4: Test Connection

```bash
python rippling_api_client.py
```

You should see success messages.

### Step 5: Start the Dashboard

```bash
python foreman_dashboard.py
```

Then open your browser to: http://localhost:5000

## What You Can Do Now

### View Live Dashboard
- Real-time project labor tracking
- Daily summaries by project
- Employee time details
- Auto-refreshes every 5 minutes

### Generate Excel Reports

Run this anytime:
```bash
python project_labor_reports.py
```

Creates: Capitol_Labor_Report_YYYY-MM-DD.xlsx

### Access from Other Computers

If you want foremen to access the dashboard from their computers:

1. Find your computer's IP address:
   ```bash
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. Make sure the dashboard is running

3. From other computers on the same network, go to:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```
   Example: http://192.168.1.100:5000

## Daily Usage

### For Foremen:
1. Open browser to dashboard URL
2. Select date (defaults to today)
3. Click "Load Report" to refresh
4. View project summaries and employee details
5. Click "Export to Excel" if you need a spreadsheet

### For Project Managers:
Run the Python script to generate detailed reports:
```bash
python project_labor_reports.py
```

This creates comprehensive Excel files with:
- Daily Summary sheet
- Project Totals sheet
- Weekly Hours sheet

## Automation Options

### Windows Task Scheduler
Generate reports automatically every day at 5 PM:

1. Open Task Scheduler
2. Create Basic Task
3. Daily trigger at 17:00
4. Action: Start Program
   - Program: python
   - Arguments: "C:\path\to\project_labor_reports.py"
   - Start in: "C:\path\to\Rippling"

### Keep Dashboard Running 24/7

Option 1: Leave Python running
```bash
python foreman_dashboard.py
```

Option 2: Run as Windows Service (advanced)
- Use NSSM (Non-Sucking Service Manager)
- Install as a Windows service

## Troubleshooting

### "API token not found"
- Check your .env file exists
- Make sure RIPPLING_API_TOKEN= has no spaces
- Verify token isn't expired (30 days inactive = expired)

### "No time entries found"
- Verify employees are clocking in/out in Rippling
- Check they're assigning projects when clocking in
- Try a different date that you know has data

### Dashboard won't start
- Check if port 5000 is already in use
- Make sure Flask is installed: pip install flask
- Verify your API token is valid

### Can't access from other computers
- Check firewall allows port 5000
- Verify computers are on same network
- Use correct IP address (not localhost)

## Next Steps

Read the full README.md for:
- Detailed API documentation
- Custom report creation
- Advanced filtering options
- Email automation setup

## Support

Capitol Engineering:
- Contact: Blake Holmes
- Website: capitolaz.com

Rippling API Help:
- Documentation: developer.rippling.com
- Your account manager
