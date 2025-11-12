# Rippling API Meeting Preparation Guide

Date: 2025-11-11
Meeting: Thursday with Rippling and IT
Attendee: Blake Holmes, Capitol Engineering

---

## Table of Contents

1. [What is an API? (Simple Explanation)](#what-is-an-api-simple-explanation)
2. [What is an API Connection?](#what-is-an-api-connection)
3. [Our Specific Goal](#our-specific-goal)
4. [What We Want to Do with Rippling API](#what-we-want-to-do-with-rippling-api)
5. [How We Will Use It](#how-we-will-use-it)
6. [What We Need from Rippling/IT](#what-we-need-from-ripplingit)
7. [Questions to Ask](#questions-to-ask)
8. [Demo to Show](#demo-to-show)

---

## What is an API? (Simple Explanation)

### The Restaurant Analogy

Think of an API like a waiter in a restaurant:

- **You (Customer)** = Your computer/dashboard
- **Kitchen** = Rippling's database (where all employee data is stored)
- **Waiter** = The API

You can't go into the kitchen and grab food yourself. Instead:
1. You tell the waiter what you want (API request)
2. The waiter goes to the kitchen (Rippling servers)
3. The waiter brings you what you asked for (API response)

### In Technical Terms

**API = Application Programming Interface**

It's a way for two computer programs to talk to each other. Specifically:
- Rippling has all your employee and time tracking data
- Your computer wants to get that data
- The API is the "bridge" that lets your computer ask for and receive that data

### Real-World Example

When you check the weather on your phone:
- Your weather app uses an API
- It asks the weather service "What's the temperature in Phoenix?"
- The weather service sends back "95 degrees"
- Your app displays it

**Our use case:** We ask Rippling "Who worked on Project M-25-0001 today?" and it sends back the employee names and hours.

---

## What is an API Connection?

### Simple Explanation

An API connection is like having a phone line between two offices:
- One end is at Capitol Engineering (your computer)
- The other end is at Rippling (their servers)
- The connection lets you call them anytime to ask for information
- They answer automatically (no human needed)

### How It Works

1. **Authentication (Security Key)**
   - You get an API token (like a password)
   - Every time you ask for data, you show this token
   - Rippling verifies it's really you
   - Only then do they send the data

2. **The Connection Process**
   ```
   Your Computer → Internet → Rippling API → Rippling Database
                             ↓
   Your Computer ← Internet ← Rippling API ← Data returned
   ```

3. **What Gets Transmitted**
   - Your request: "Give me time entries for 2025-11-11"
   - Rippling's response: JSON data with all the time entries
   - All encrypted and secure (HTTPS)

### What Makes It "Connected"

- The connection is always available (24/7)
- No manual work required
- Automatic updates (real-time data)
- Secure authentication
- Two-way communication

---

## Our Specific Goal

### PRIMARY OBJECTIVE

**Create a Project Dashboard to track hours worked vs hours budgeted**

### What This Means

Right now:
- Employees clock in/out in Rippling
- Time is tracked by project
- But we can't easily see project hours vs budget

What we want:
- A dashboard showing all active projects
- Total hours worked on each project
- Budgeted hours for each project
- Percentage complete (hours worked / hours budgeted)
- Visual indicators (red if over budget, green if under)

### Example Dashboard View

```
Project Dashboard - Capitol Engineering

Project: M-25-0001 - Lithium Nevada Ducting
Budgeted Hours: 500 hours
Hours Worked: 387 hours
Remaining: 113 hours (23%)
Status: ON TRACK

Project: M-25-0002 - Phoenix Convention Center
Budgeted Hours: 800 hours
Hours Worked: 856 hours
Remaining: -56 hours (107%)
Status: OVER BUDGET - ALERT

Project: M-25-0003 - Intel Fab Expansion
Budgeted Hours: 1200 hours
Hours Worked: 245 hours
Remaining: 955 hours (20%)
Status: EARLY STAGE
```

---

## What We Want to Do with Rippling API

### The Complete Picture

#### Phase 1: Current System (Already Built)
What we have working now:
- Pull employee time entries from Rippling
- Generate daily labor reports
- Show who worked on what project
- Display hours per employee per project
- Web dashboard for foremen

#### Phase 2: Project Budget Tracking (What We Need Help With)
What we want to add:
- Pull project data from Rippling
- Link time entries to project budgets
- Calculate hours worked vs hours budgeted
- Show project status (on track, over budget, etc.)
- Alert when projects exceed budget

#### Phase 3: Future Enhancements
Later additions:
- Cost tracking (hours × hourly rate)
- Predictive analytics (estimated completion date)
- Resource allocation (which crew to assign)
- Integration with accounting system

### Specific Data We Need from Rippling

1. **Employee Data** (Already have this)
   - Employee names and IDs
   - Job titles
   - Hourly rates (if available)

2. **Time Tracking Data** (Already have this)
   - Clock in/out times
   - Total hours per day
   - Project/job code assignments

3. **Project Data** (This is what we need)
   - Project names and codes
   - Project budgets (total budgeted hours)
   - Project start/end dates
   - Project status (active, completed, etc.)
   - Custom fields (if we add budget information)

4. **Job Dimensions** (Need to understand this better)
   - How projects are organized in Rippling
   - Where budget information might be stored
   - Custom fields we can use

---

## How We Will Use It

### Daily Workflow

#### Morning (6:00 AM)
1. System automatically pulls overnight time entries
2. Updates project totals
3. Checks for budget warnings
4. Generates alert report

#### During Day (Real-time)
1. Dashboard shows live project status
2. Foremen check crew assignments
3. Project managers monitor budgets
4. Automatic refresh every 5 minutes

#### End of Day (5:00 PM)
1. System generates daily labor report
2. Exports to Excel for distribution
3. Sends budget alerts if needed
4. Archives data for historical tracking

### Who Uses What

#### Foremen
- View daily crew assignments
- See who's working on which project
- Check total hours for the day
- Access via web browser (phone, tablet, computer)

#### Project Managers
- Monitor project budgets
- Track hours vs budget
- Review weekly summaries
- Export detailed Excel reports

#### Accounting
- Verify payroll hours
- Allocate costs to projects
- Generate billing reports
- Track labor costs

#### Executives
- High-level project status
- Budget utilization across all projects
- Identify problem projects
- Resource planning

### Technical Architecture

```
┌─────────────────────────────────────────┐
│         RIPPLING CLOUD                  │
│  - Employee Data                        │
│  - Time Entries                         │
│  - Project/Job Data                     │
└─────────────┬───────────────────────────┘
              │ API Connection
              │ (HTTPS, Token Auth)
              ↓
┌─────────────────────────────────────────┐
│    CAPITOL ENGINEERING SERVER           │
│  - Python Integration Script            │
│  - Data Processing                      │
│  - Budget Calculations                  │
└─────────────┬───────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────┐
│      PROJECT DASHBOARD                  │
│  - Web Interface                        │
│  - Real-time Updates                    │
│  - Budget vs Actual Display             │
│  - Alert Notifications                  │
└─────────────────────────────────────────┘
              │
              ↓
    ┌─────────┴──────────┐
    ↓                    ↓
[Foremen Tablets]  [Manager Computers]
```

### Frequency of Data Updates

- **Time Entries:** Every 5 minutes
- **Employee Data:** Daily (changes rarely)
- **Project Data:** Daily or on-demand
- **Budget Calculations:** Real-time (when time entries update)

### Storage and Retention

- Keep 90 days of detailed data
- Archive older data for historical reports
- Backup database daily
- Export monthly reports for permanent records

---

## What We Need from Rippling/IT

### Questions for Rippling

#### 1. Project Budget Data
- **Question:** Where can we store project budgeted hours in Rippling?
- **Options:**
  - Job dimension custom fields?
  - Separate project table?
  - Integration with external system?
- **Need:** A field we can populate with budgeted hours per project

#### 2. API Permissions
- **Question:** What API endpoints do we need access to?
- **Current Access:** /users, /time-entries
- **Need Access To:** /job-dimensions, project details, budget fields
- **Who:** Need API token with appropriate permissions

#### 3. Custom Fields
- **Question:** Can we add custom fields to projects/job dimensions?
- **Fields Needed:**
  - Budgeted Hours (integer)
  - Project Status (active, completed, on hold)
  - Budget Alert Threshold (percentage, e.g., 90%)
  - Project Start Date
  - Project End Date
- **Access:** Need permission to read/write these fields via API

#### 4. Rate Limits
- **Question:** What are the API rate limits?
- **Our Usage:** Approximately 1 call every 5 minutes (288 calls/day)
- **Concern:** Will we hit any limits with real-time updates?

#### 5. Webhooks
- **Question:** Does Rippling support webhooks for real-time notifications?
- **Use Case:** Get notified immediately when someone clocks in/out
- **Benefit:** Reduce API polling, get instant updates

#### 6. Historical Data
- **Question:** How far back can we retrieve time entry data?
- **Need:** Ability to backfill project hours from start of year

### Questions for IT

#### 1. Server/Hosting
- **Question:** Where should we host this dashboard?
- **Options:**
  - Office server
  - Cloud hosting (Render, AWS, Azure)
  - Dedicated computer
- **Requirements:** Always-on, network accessible

#### 2. Network Access
- **Question:** Who needs access to the dashboard?
- **Requirement:** Internal network access for all foremen and managers
- **Security:** Should it be accessible from outside office?

#### 3. Firewall/Security
- **Question:** Any firewall rules needed for API calls?
- **Requirement:** Allow HTTPS connections to rest.ripplingapis.com
- **Port:** 443 (standard HTTPS)

#### 4. Authentication
- **Question:** How do we secure the dashboard login?
- **Options:**
  - Simple password
  - Active Directory integration
  - No login (internal network only)

#### 5. Backup and Disaster Recovery
- **Question:** What's the backup plan?
- **Need:** Regular backups of historical data
- **Recovery:** Plan if server goes down

#### 6. Monitoring
- **Question:** How do we monitor if the system goes down?
- **Need:** Alerts if API connection fails
- **Tool:** Email alerts, SMS, monitoring dashboard

### What We'll Provide

#### From Capitol Engineering
1. Technical requirements document
2. API token management
3. User training for foremen
4. Budget data entry
5. Ongoing maintenance

#### From Rippling
1. API token with appropriate permissions
2. Documentation on project/budget fields
3. Technical support for API questions
4. Guidance on custom field setup

#### From IT
1. Server/hosting infrastructure
2. Network configuration
3. Security setup
4. Backup system
5. User access management

---

## Questions to Ask

### Technical Questions

1. **Project Structure**
   - How are projects organized in Rippling?
   - What's the relationship between job codes and projects?
   - Can we add budget information to job dimensions?

2. **API Capabilities**
   - Can we read and write project budget data via API?
   - What's the format of project/job dimension data?
   - Are there example API calls for project data?

3. **Data Refresh**
   - How often does time entry data update in Rippling?
   - Is there lag between clock-in and API availability?
   - Can we get real-time notifications?

4. **Scaling**
   - What if we add more employees/projects?
   - Are there API call limits we should know about?
   - What's the largest dataset we can retrieve?

### Business Questions

1. **Cost**
   - Is there additional cost for API access?
   - Are there usage fees based on API calls?
   - Any fees for additional data fields?

2. **Support**
   - Who do we contact for API issues?
   - Is there developer support available?
   - What's the SLA for API uptime?

3. **Training**
   - Can Rippling provide training on their API?
   - Documentation available?
   - Example code or integrations?

4. **Compliance**
   - Any security requirements for API access?
   - Data privacy considerations?
   - Audit logging requirements?

### Process Questions

1. **Setup Timeline**
   - How long to get API access?
   - How long to set up custom fields?
   - When can we start testing?

2. **Implementation**
   - Do we need Rippling's help to set up?
   - Can we do this ourselves?
   - Any required consulting/professional services?

3. **Testing**
   - Can we test in a sandbox environment?
   - How to test without affecting production?
   - What's the approval process?

---

## Demo to Show

### What We've Already Built

During the meeting, demonstrate:

#### 1. Current Dashboard
- Show the live dashboard at http://localhost:5000
- Explain what data it's pulling
- Demonstrate the three demo versions

#### 2. Daily Reports
- Show an example Excel report
- Explain the three sheets (Daily Summary, Project Totals, Weekly Hours)
- Show how foremen use these reports

#### 3. Technical Architecture
- Show the code structure (briefly)
- Explain the API integration
- Demonstrate a live API call

### Demo Script

**Start with the problem:**
"Right now, we can see who worked and how many hours, but we can't track those hours against our project budgets. We need to know if we're on track or over budget."

**Show what we have:**
"Here's the dashboard we built. It shows all our employees and projects in real-time. The data comes directly from Rippling every 5 minutes."

**Show what we need:**
"What we want to add is this section here [point to mockup] that shows budgeted hours vs actual hours. To do that, we need to store budget information in Rippling and pull it via the API."

**Explain the value:**
"This will let project managers see at a glance if projects are on track. If a project is over budget, we can reassign resources or adjust the timeline before it becomes a bigger problem."

### Mockup to Show

Create a simple visual showing:
```
CURRENT VIEW:
┌─────────────────────────────────────┐
│ Project 25-2126                     │
│ Employees: 12                       │
│ Hours Today: 87.5                   │
└─────────────────────────────────────┘

PROPOSED VIEW:
┌─────────────────────────────────────┐
│ Project 25-2126                     │
│ Employees: 12                       │
│ Hours Today: 87.5                   │
│                                     │
│ Budget: 500 hrs                     │
│ Worked: 387 hrs (77%)               │
│ Remaining: 113 hrs                  │
│ Status: ✓ ON TRACK                  │
└─────────────────────────────────────┘
```

---

## Key Talking Points

### Why We Need This

1. **Visibility**
   - Currently tracking time but not budget
   - Need to see project status at a glance
   - Prevent budget overruns

2. **Efficiency**
   - Automate manual budget tracking
   - Save project managers hours per week
   - Real-time alerts, not end-of-month surprises

3. **Better Decision Making**
   - Know which projects are profitable
   - Adjust resources proactively
   - Improve future bidding accuracy

4. **Already Invested**
   - We've already built the foundation
   - System is working for time tracking
   - Just need to add budget component

### What Makes This Easy

1. **Small Scope**
   - We're not asking for a major system change
   - Just need to store budget numbers
   - Simple calculation (actual vs budget)

2. **We'll Do the Work**
   - We've built the dashboard
   - We'll maintain the system
   - Just need access to the data

3. **Low Risk**
   - Read-only API access (mostly)
   - Won't affect Rippling's core functionality
   - Can test in isolation

4. **High Value**
   - Immediate benefit to project management
   - Scalable to all projects
   - Foundation for future analytics

---

## Follow-Up Actions

### After the Meeting

#### Immediate (Day 1)
- [ ] Document all answers and decisions
- [ ] Get API token with new permissions (if needed)
- [ ] Receive documentation on project fields
- [ ] Schedule follow-up if needed

#### Week 1
- [ ] Test new API endpoints
- [ ] Set up custom fields for project budgets
- [ ] Enter budget data for active projects
- [ ] Develop budget tracking calculations

#### Week 2
- [ ] Build budget dashboard view
- [ ] Test with sample data
- [ ] Get feedback from project managers
- [ ] Refine alert thresholds

#### Week 3
- [ ] Deploy to production
- [ ] Train users
- [ ] Monitor for issues
- [ ] Iterate based on feedback

---

## Sharing This Information

### For Your Coworker

This document contains everything they need to understand:
- What an API is (restaurant analogy)
- How our system works
- What we're trying to accomplish
- Technical details

**Recommended reading order:**
1. "What is an API?" section
2. "Our Specific Goal" section
3. "How We Will Use It" section
4. Rest as reference material

### Additional Resources

Point them to these files in the project:
- [README.md](README.md) - Complete system documentation
- [API_CAPABILITIES.md](API_CAPABILITIES.md) - What Rippling API can do
- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - System architecture
- [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) - How to use the system

### Quick Demo for Coworker

1. **Show the restaurant analogy** - Easiest way to explain APIs
2. **Run the demo** - Double-click START_DEMO_ULTRA.bat
3. **Show a report** - Open an example Excel report
4. **Explain the goal** - Show the mockup of budget tracking
5. **Answer questions** - Use this document as reference

---

## Confidence Builders

### What You Can Say with Confidence

1. "We've already built a working system that pulls time tracking data from Rippling."
2. "Our foremen are using the dashboard daily to monitor crew hours."
3. "This project has already saved us significant time on manual reporting."
4. "We just need to expand it to include project budget tracking."

### If They Ask Technical Questions

1. "We're using Python with the Rippling REST API."
2. "The system makes authenticated HTTPS calls to your API endpoints."
3. "We're already successfully pulling employee and time entry data."
4. "We need access to project/job dimension data and the ability to store budget information."

### If They Ask About Your Skill Level

1. "We have a working integration and understand API basics."
2. "We've read the Rippling API documentation."
3. "We're comfortable with REST APIs, JSON, and authentication."
4. "We just need guidance on where project budget data should live in Rippling."

---

## Summary

### The One-Minute Pitch

"We've built a dashboard that pulls employee time tracking data from Rippling via their API. It's working great for daily labor reports. Now we want to add project budget tracking so we can see hours worked versus hours budgeted. To do this, we need to store project budget information in Rippling and access it via the API. This will give our project managers real-time visibility into project status and help prevent budget overruns."

### The Core Request

"We need help understanding where to store project budget information in Rippling and how to access that data via the API."

### The Expected Outcome

By the end of the meeting, we should know:
1. Where to store project budgets in Rippling
2. How to access that data via API
3. What permissions/tokens we need
4. Timeline for implementation
5. Next steps

---

Good luck with your meeting! You've got this.

Capitol Engineering
www.capitolaz.com
Date: 2025-11-11
