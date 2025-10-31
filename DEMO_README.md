# Capitol Engineering - Time Tracking Demo

Date created: 2025-10-30

## What This Is

A **fully functional demonstration** of the Rippling time tracking integration for Capitol Engineering. Uses realistic sample data to show exactly how the system will work - perfect for presentations!

## Quick Start - 30 Seconds

1. **Double-click:** START_DEMO.bat
2. **Wait:** Browser opens automatically
3. **Present:** Show your team the system!

No configuration needed. No API token required. Just works!

## What You'll See

### Live Dashboard Features
- Real-time project summaries
- Employee time tracking by project
- Daily hours breakdown
- Professional reporting interface
- Excel export capability

### Sample Data Included
- 15 Capitol Engineering employees
- 7 active projects (based on your actual naming)
- Realistic time entries and schedules
- Multiple days of historical data

## Perfect For

- Management presentations
- Foreman training
- Stakeholder approval meetings
- IT evaluation
- System demonstrations

## Demo vs. Production

| Feature | Demo | Production |
|---------|------|------------|
| Data Source | Sample data | Live Rippling API |
| Setup Time | 30 seconds | 5 minutes |
| API Token | Not needed | Required |
| Projects | 7 sample | Your actual projects |
| Employees | 15 sample | Your actual employees |
| Functionality | 100% same | 100% same |

## System Requirements

- Windows 7 or higher
- Python 3.8+ (will help install if missing)
- Any modern web browser
- Internet connection (for package install only)

## What to Demonstrate

### 1. Project Overview
Show the project summary section:
- Total hours per project
- Employee count per project
- Quick project comparison

**Say this:** "Foremen can instantly see labor allocation across all active projects."

### 2. Employee Details
Show the detailed employee table:
- Who's working today
- Which project they're on
- Clock in/out times
- Hours worked

**Say this:** "Every employee's time is visible at a glance - no more calling around to find out who's where."

### 3. Date Selection
Change the date to show historical data:
- Click different dates
- Show how data updates
- Demonstrate historical tracking

**Say this:** "Foremen can review any day's data for reporting or comparison."

### 4. Export Function
Click "Export to Excel":
- Generates professional report
- Multiple sheets
- Ready for management

**Say this:** "One click creates a detailed Excel report for management review or payroll verification."

### 5. Statistics Panel
Point out the quick stats:
- Total hours today
- Active projects count
- Total employees working

**Say this:** "These key metrics give instant insight into daily operations."

## Sharing the Demo

### On Same Network
1. Start demo on your computer
2. Run: ipconfig (to get your IP)
3. Others visit: http://YOUR_IP:5000

### Remote Presentation
- Use Teams/Zoom screen share
- Share your browser window
- Walk through features live

### Portable Demo
- Copy entire Rippling folder to USB
- Run on any Windows computer
- Perfect for job site demos

## Files You Need

All files are already included:

```
Rippling/
├── START_DEMO.bat          ← Double-click this!
├── demo_mode.py            ← Demo server
├── demo_data_generator.py  ← Sample data
├── DEMO_GUIDE.md          ← Detailed presentation guide
└── DEMO_README.md         ← This file
```

## Troubleshooting

### "Python is not recognized"
Install Python from python.org, then run demo again.

### Browser doesn't open
Manually go to: http://localhost:5000

### Port already in use
Another program is using port 5000. Close it or restart computer.

### No data showing
Refresh the page. Data generates on first load.

## After Approval

Ready to go live? Easy transition:

1. Get Rippling API token from your account
2. Run setup.bat (instead of START_DEMO.bat)
3. Add your API token to .env file
4. Same dashboard, now with real data!

See README.md for production setup.

## Common Questions

**Q: Is this the actual system?**
A: Yes! Same code, same interface. Demo uses sample data, production uses your Rippling data.

**Q: Can we customize it?**
A: Absolutely. Colors, layout, columns - everything can be customized.

**Q: How much does it cost?**
A: Zero additional cost beyond your Rippling subscription. This is a free integration.

**Q: What about security?**
A: Production uses secure API tokens. Demo requires no credentials.

**Q: Can it run 24/7?**
A: Yes. Can be installed on any Windows PC or server for constant availability.

## Need Help?

During demo if something goes wrong:
1. Stop and restart START_DEMO.bat
2. Have screenshots as backup
3. Show this documentation
4. Schedule follow-up demo

## Next Steps

1. Run the demo
2. Present to stakeholders
3. Get approval
4. Set up production version
5. Train foremen
6. Go live!

---

## Ready to Demo?

**Just double-click START_DEMO.bat and you're ready to present!**

Capitol Engineering
www.capitolaz.com

Date: 2025-10-30
System: Rippling Time Tracking Integration
