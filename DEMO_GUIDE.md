# Demo Guide - Capitol Engineering Time Tracking System

Date created: 2025-10-30

## Overview

This demo system shows exactly how the Rippling time tracking integration will work for Capitol Engineering, using realistic sample data. Perfect for presentations to management, foremen, and stakeholders.

## What's Included in the Demo

### Sample Data
- 15 realistic Capitol Engineering employees (welders, fabricators, fitters, etc.)
- 7 active projects based on your actual project naming (25-2126, 25-2350, etc.)
- Realistic time entries with proper clock in/out times
- Multiple days of historical data

### Full Dashboard
- Live project summaries
- Employee time details
- Quick statistics
- Excel export capability
- Professional Capitol Engineering branding

## Running the Demo

### Quick Start (1 minute)

1. Double-click: **START_DEMO.bat**
2. Wait for browser to open automatically
3. Start presenting!

That's it - no API token or configuration needed!

### Manual Start

If you prefer command line:

```bash
cd C:\Users\holme\OneDrive\Desktop\Rippling
python demo_mode.py
```

Then open: http://localhost:5000

## Demo Features to Showcase

### 1. Daily Project Summary

Show how foremen can see:
- All active projects for the day
- Total hours per project
- Number of employees per project
- Which projects are busy vs. slow

**Demo Script:**
"Here you can see all 7 active projects. The Lithium Nevada project has 5 employees working today with 42 hours logged. This gives foremen instant visibility into labor allocation."

### 2. Employee Time Details

Demonstrate:
- Complete employee list with times
- Which project each employee is on
- Clock in/out times
- Approval status

**Demo Script:**
"Foremen can see exactly when John Martinez clocked in at 7:00 AM and that he's working on the Forest Energy project. All time entries show approved or pending status."

### 3. Quick Stats Dashboard

Highlight:
- Total hours for the day
- Number of active projects
- Total employees working

**Demo Script:**
"At a glance, we can see 95 total hours across all projects today with 13 employees actively working. This instant overview helps with resource planning."

### 4. Date Selection

Show:
- Ability to view any date
- Historical data access
- Future planning capability

**Demo Script:**
"Foremen aren't limited to today - they can pull up any date to review past work or plan ahead. Let me show you yesterday's data..."

### 5. Excel Export

Demonstrate:
- One-click Excel generation
- Multiple sheets (Daily Summary, Project Totals, Demo Info)
- Professional formatting

**Demo Script:**
"If they need to share with management or do deeper analysis, one click generates a professional Excel report with multiple detailed sheets."

### 6. Mobile/Tablet Access

Show:
- Responsive design
- Works on phones and tablets
- Same features everywhere

**Demo Script:**
"Foremen can access this from their phone, tablet, or office computer - it works the same everywhere. No special apps to install."

## Presentation Tips

### For Management

Focus on:
- Cost savings from automation
- Real-time visibility into labor costs
- Better project management
- Reduced administrative time

**Key Points:**
- "No more manual timesheet entry"
- "Instant project cost tracking"
- "Foremen spend less time on paperwork"
- "Better resource allocation decisions"

### For Foremen

Focus on:
- How easy it is to use
- Time savings
- Better crew management
- No technical skills needed

**Key Points:**
- "Just open your browser - that's it"
- "See your entire crew at a glance"
- "Know who's on which job instantly"
- "Auto-refreshes every 5 minutes"

### For IT/Technical Staff

Focus on:
- Rippling API integration
- Security (API tokens)
- Reliability
- Easy deployment

**Key Points:**
- "Official Rippling REST API"
- "Secure token authentication"
- "Can run on any Windows computer"
- "Simple Python installation"

## Common Demo Questions & Answers

### Q: "Is this real data?"
**A:** "This is demo data for presentation, but it's based on our actual projects and employee structure. The real system will pull live data directly from Rippling."

### Q: "How often does it update?"
**A:** "The real system auto-refreshes every 5 minutes, but you can also manually refresh anytime. The demo works the same way."

### Q: "Can we customize the projects shown?"
**A:** "Absolutely. The system pulls whatever job codes you've set up in Rippling. As you add or remove projects in Rippling, they automatically appear here."

### Q: "What if someone forgets to clock in?"
**A:** "The system shows exactly what's in Rippling. If there's no time entry, it won't show - which actually helps foremen catch missing timesheets quickly."

### Q: "Can we access this from the shop floor?"
**A:** "Yes, any device on your network can access it. We can set it up so foremen access it from tablets in the shop or their phones."

### Q: "How much does this cost?"
**A:** "The integration itself has no additional cost beyond your existing Rippling subscription. It's a free Python-based system we can host on any Windows computer."

### Q: "What about historical data?"
**A:** "You can view any date going back as far as your Rippling data goes. Great for reviewing past projects or comparing week-over-week."

### Q: "Can we export to our accounting system?"
**A:** "The Excel export can be imported into most accounting systems. We can also add direct integrations if needed."

## Advanced Demo Features

### Generate Custom Demo Data

If you want different demo scenarios:

```bash
python demo_data_generator.py
```

This creates a demo_data.json file with a week of sample data.

### Modify Sample Projects

Edit demo_data_generator.py and change the projects list:

```python
self.projects = [
    {"code": "YOUR-PROJECT", "name": "Your Project Name", "type": "Fabrication"},
    # Add your projects here
]
```

### Modify Sample Employees

Edit the employees list in demo_data_generator.py to match your crew.

## Sharing the Demo

### Option 1: Local Network
1. Start the demo
2. Find your computer's IP (run: ipconfig)
3. Others access: http://YOUR_IP:5000

### Option 2: Screen Share
- Use Teams/Zoom screen sharing
- Run demo on your computer
- Share your screen

### Option 3: Portable Demo
- Copy entire Rippling folder to USB drive
- Run START_DEMO.bat from USB on any Windows PC
- Great for on-site presentations

## Troubleshooting Demo Issues

### Demo won't start
- Make sure Python is installed
- Run: pip install flask pandas openpyxl
- Check port 5000 isn't already in use

### Browser doesn't open
- Manually go to http://localhost:5000
- Try different browser (Chrome, Edge, Firefox)

### No data showing
- The demo generates data on-demand
- Try refreshing the page
- Check console for errors

### Want to reset demo
- Stop the server (Ctrl+C)
- Restart START_DEMO.bat
- Fresh demo data will be generated

## After the Demo

Once stakeholders approve, transition to live system:

1. Get Rippling API token
2. Run setup.bat instead of START_DEMO.bat
3. Configure .env with real token
4. Same dashboard, now with real data!

## Demo Checklist

Before your presentation:

- [ ] Python installed and working
- [ ] START_DEMO.bat launches successfully
- [ ] Browser opens to dashboard
- [ ] Data loads properly
- [ ] Excel export works
- [ ] Practiced your talking points
- [ ] Tested on presentation computer/projector
- [ ] Have backup (screenshot slides) ready

## Support During Demo

If something goes wrong during presentation:

1. Have screenshots ready as backup
2. Can show this README as documentation
3. Explain it's a demo - real system is even better
4. Schedule follow-up demo

## Next Steps After Successful Demo

1. Get approval from stakeholders
2. Obtain Rippling API token
3. Install production version
4. Train foremen on usage
5. Set up automated daily reports
6. Deploy to network/server for 24/7 access

---

**Remember:** This demo is designed to impress and show value. The actual system will be even better because it's using real-time data from your actual Rippling account!

Good luck with your presentation!

Capitol Engineering - www.capitolaz.com
