# File Guide - Capitol Engineering Time Tracking System

Date created: 2025-10-30

## Complete File Listing

Here's what each file does and when to use it.

---

## DEMO FILES (Start Here!)

### START_DEMO.bat
**What it is:** One-click demo launcher
**Use when:** Presenting to management/foremen
**How to use:** Double-click it
**Output:** Opens demo dashboard in browser

### demo_mode.py
**What it is:** Demo web server with sample data
**Use when:** Running demo manually
**How to use:** `python demo_mode.py`
**Output:** Web dashboard at http://localhost:5000

### demo_data_generator.py
**What it is:** Creates realistic sample data
**Use when:** Want custom demo scenarios
**How to use:** `python demo_data_generator.py`
**Output:** demo_data.json file

### DEMO_README.md
**What it is:** Quick demo overview
**Use when:** Need 30-second demo instructions
**Read first:** Yes - shortest guide

### DEMO_GUIDE.md
**What it is:** Complete demo presentation guide
**Use when:** Preparing for formal presentation
**Read first:** Before presenting to stakeholders

### PRESENTATION_SCRIPT.md
**What it is:** Word-for-word demo script
**Use when:** First time presenting system
**Read first:** Before first presentation

---

## PRODUCTION FILES (After Approval)

### setup.bat
**What it is:** Automated production setup
**Use when:** Installing for real use
**How to use:** Double-click after getting API token
**Output:** Configured production system

### rippling_api_client.py
**What it is:** Rippling API integration code
**Use when:** System automatically uses it
**How to use:** Don't run directly - imported by other scripts
**Output:** API connection and data retrieval

### project_labor_reports.py
**What it is:** Report generation engine
**Use when:** Want Excel reports
**How to use:** `python project_labor_reports.py`
**Output:** Excel file with daily/weekly reports

### foreman_dashboard.py
**What it is:** Production web dashboard
**Use when:** Daily use by foremen
**How to use:** `python foreman_dashboard.py`
**Output:** Live web dashboard at http://localhost:5000

---

## CONFIGURATION FILES

### .env.example
**What it is:** Template for API token
**Use when:** First time setup
**How to use:** Copy to .env and add token
**Output:** .env file with your credentials

### .env
**What it is:** Your actual API token (created by you)
**Use when:** Production use
**How to use:** Edit with Notepad, add token
**Output:** System can connect to Rippling
**Important:** NEVER share this file!

### requirements.txt
**What it is:** Python package list
**Use when:** Installing packages
**How to use:** `pip install -r requirements.txt`
**Output:** All required packages installed

---

## DOCUMENTATION FILES

### README.md
**What it is:** Complete system documentation
**Use when:** Full setup and reference
**Read first:** For production deployment
**Contains:**
- Complete setup instructions
- Usage examples
- Troubleshooting
- Automation setup

### QUICKSTART.md
**What it is:** 5-minute production setup guide
**Use when:** Need fast setup instructions
**Read first:** If experienced with Python
**Contains:**
- Quick setup steps
- Common tasks
- Troubleshooting

### PROJECT_OVERVIEW.md
**What it is:** System architecture guide
**Use when:** Understanding how it works
**Read first:** For IT/technical staff
**Contains:**
- Architecture diagrams
- Data flow
- API endpoints
- Security info

### FILE_GUIDE.md
**What it is:** This file
**Use when:** Finding the right file
**Read first:** If you're lost

---

## GENERATED FILES (System Creates These)

### templates/
**What it is:** HTML templates for web dashboard
**Created by:** System automatically
**Don't touch:** Auto-generated when needed

### demo_data.json
**What it is:** Sample data for demos
**Created by:** demo_data_generator.py
**Can delete:** Yes, regenerates automatically

### Capitol_Labor_Report_*.xlsx
**What it is:** Generated Excel reports
**Created by:** Report generator scripts
**Can delete:** Yes, these are output files

---

## Quick Reference by Task

### "I want to show my boss the system"
1. START_DEMO.bat
2. Read DEMO_README.md
3. Use PRESENTATION_SCRIPT.md

### "I want to set up for real use"
1. Read QUICKSTART.md
2. Get Rippling API token
3. Run setup.bat
4. Edit .env file

### "I want to understand how it works"
1. Read PROJECT_OVERVIEW.md
2. Look at rippling_api_client.py
3. Look at project_labor_reports.py

### "I want to generate a report"
```bash
python project_labor_reports.py
```

### "I want to start the dashboard"
Production:
```bash
python foreman_dashboard.py
```

Demo:
```bash
python demo_mode.py
```
or just double-click START_DEMO.bat

### "I want to customize the demo"
1. Edit demo_data_generator.py
2. Change projects or employees lists
3. Run it to regenerate data

---

## File Dependencies

```
START_DEMO.bat
    └── demo_mode.py
        └── demo_data_generator.py

setup.bat
    └── rippling_api_client.py
        └── .env (you create this)

foreman_dashboard.py
    └── project_labor_reports.py
        └── rippling_api_client.py
            └── .env

project_labor_reports.py
    └── rippling_api_client.py
        └── .env
```

---

## Files You Need to Edit

Only edit these:

1. **.env** - Add your API token
2. **demo_data_generator.py** - Only if customizing demo

Don't edit anything else unless you know Python!

---

## Files You Can Delete

Safe to delete:
- demo_data.json (regenerates)
- Capitol_Labor_Report_*.xlsx (output files)
- templates/ folder (auto-recreates)
- __pycache__/ folder (Python cache)

Never delete:
- All .py files
- All .md files
- All .bat files
- requirements.txt
- .env.example

---

## Backup Recommendation

Files to backup regularly:
- .env (your API token)
- Any customized .py files
- Generated reports you want to keep

Everything else can be re-downloaded from source.

---

## Getting Help

- **Demo issues:** See DEMO_GUIDE.md
- **Setup issues:** See QUICKSTART.md
- **How it works:** See PROJECT_OVERVIEW.md
- **Everything else:** See README.md

---

Capitol Engineering
www.capitolaz.com
Date: 2025-10-30
