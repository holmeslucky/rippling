# Project Dashboard Mockup - Before and After

This document shows the visual difference between what we have now and what we want to build.

---

## CURRENT DASHBOARD (What We Have Now)

```
╔═══════════════════════════════════════════════════════════════════════╗
║               CAPITOL ENGINEERING - DAILY LABOR REPORT                ║
║                         Date: 2025-11-11                              ║
╚═══════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────┐
│ PROJECT: M-25-0001 - Lithium Nevada - Thacker Pass Ducting         │
├─────────────────────────────────────────────────────────────────────┤
│ Today's Hours: 87.5                                                  │
│ Employees Working: 12                                                │
│                                                                      │
│ Top Workers:                                                         │
│  - Jose Martinez (Welder): 8.5 hrs                                  │
│  - Mike Johnson (Foreman): 8.0 hrs                                  │
│  - Carlos Rodriguez (Fabricator): 8.0 hrs                           │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ PROJECT: M-25-0002 - Phoenix Convention Center HVAC                 │
├─────────────────────────────────────────────────────────────────────┤
│ Today's Hours: 64.0                                                  │
│ Employees Working: 8                                                 │
│                                                                      │
│ Top Workers:                                                         │
│  - David Chen (Installer): 8.0 hrs                                  │
│  - Robert Smith (Supervisor): 8.0 hrs                               │
│  - Maria Garcia (Technician): 8.0 hrs                               │
└─────────────────────────────────────────────────────────────────────┘

Total Hours Today: 243.5
Total Employees: 27
Active Projects: 7
```

### What's Missing?

We can see:
- Who worked today
- What project they worked on
- How many hours they worked

We CANNOT see:
- Is the project on budget?
- How many hours were budgeted?
- How many hours remain?
- Are we going to go over budget?

---

## PROPOSED DASHBOARD (What We Want to Build)

```
╔═══════════════════════════════════════════════════════════════════════╗
║          CAPITOL ENGINEERING - PROJECT DASHBOARD WITH BUDGETS         ║
║                         Date: 2025-11-11                              ║
╚═══════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────┐
│ PROJECT: M-25-0001 - Lithium Nevada - Thacker Pass Ducting         │
├─────────────────────────────────────────────────────────────────────┤
│ Today's Hours: 87.5                                                  │
│ Employees Working: 12                                                │
│                                                                      │
│ PROJECT BUDGET STATUS:                                               │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ Budgeted Hours:    500 hrs                                      │ │
│ │ Hours Worked:      387 hrs  (77%)                               │ │
│ │ Hours Remaining:   113 hrs  (23%)                               │ │
│ │                                                                  │ │
│ │ Progress: [████████████████████████░░░░░░░] 77%                │ │
│ │                                                                  │ │
│ │ Status: ✓ ON TRACK                                              │ │
│ │ Estimated Completion: 5 days at current rate                    │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│ Top Workers Today:                                                   │
│  - Jose Martinez (Welder): 8.5 hrs                                  │
│  - Mike Johnson (Foreman): 8.0 hrs                                  │
│  - Carlos Rodriguez (Fabricator): 8.0 hrs                           │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ PROJECT: M-25-0002 - Phoenix Convention Center HVAC                 │
├─────────────────────────────────────────────────────────────────────┤
│ Today's Hours: 64.0                                                  │
│ Employees Working: 8                                                 │
│                                                                      │
│ PROJECT BUDGET STATUS:                                               │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ Budgeted Hours:    800 hrs                                      │ │
│ │ Hours Worked:      856 hrs  (107%)                              │ │
│ │ Hours Over Budget: 56 hrs   (7% over)                           │ │
│ │                                                                  │ │
│ │ Progress: [█████████████████████████████████] 107%             │ │
│ │                                                                  │ │
│ │ Status: ⚠ OVER BUDGET                                           │ │
│ │ Action Required: Review scope or request budget increase        │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│ Top Workers Today:                                                   │
│  - David Chen (Installer): 8.0 hrs                                  │
│  - Robert Smith (Supervisor): 8.0 hrs                               │
│  - Maria Garcia (Technician): 8.0 hrs                               │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ PROJECT: M-25-0003 - Intel Fab Expansion                            │
├─────────────────────────────────────────────────────────────────────┤
│ Today's Hours: 32.0                                                  │
│ Employees Working: 4                                                 │
│                                                                      │
│ PROJECT BUDGET STATUS:                                               │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ Budgeted Hours:    1200 hrs                                     │ │
│ │ Hours Worked:      245 hrs  (20%)                               │ │
│ │ Hours Remaining:   955 hrs  (80%)                               │ │
│ │                                                                  │ │
│ │ Progress: [██████░░░░░░░░░░░░░░░░░░░░░░░░░░] 20%               │ │
│ │                                                                  │ │
│ │ Status: ✓ EARLY STAGE                                           │ │
│ │ Projected Completion: 30 days at current rate                   │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│ Top Workers Today:                                                   │
│  - Tom Wilson (Lead): 8.0 hrs                                       │
│  - Sarah Brown (Installer): 8.0 hrs                                 │
└─────────────────────────────────────────────────────────────────────┘

╔═══════════════════════════════════════════════════════════════════════╗
║                         SUMMARY - ALL PROJECTS                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║ Total Projects: 7                                                     ║
║ On Track: 5  │  Over Budget: 1  │  Under Budget: 1                  ║
║                                                                       ║
║ Total Hours Today: 243.5                                              ║
║ Total Budgeted Hours: 4,800                                           ║
║ Total Hours Worked: 2,234 (47%)                                       ║
║ Total Hours Remaining: 2,566 (53%)                                    ║
║                                                                       ║
║ ⚠ ALERTS: 1 project over budget, requires attention                  ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## KEY DIFFERENCES

### What Gets Added

1. **Budget Information**
   - Budgeted hours per project
   - Hours worked (with percentage)
   - Hours remaining
   - Progress bar visualization

2. **Status Indicators**
   - On Track: Green checkmark
   - Over Budget: Red warning
   - Early Stage: Blue info
   - At Risk: Yellow caution

3. **Projections**
   - Estimated completion date
   - Current burn rate
   - Action recommendations

4. **Alerts Section**
   - Quick view of projects needing attention
   - Summary of budget status across all projects

---

## DATA REQUIRED FROM RIPPLING

To build the proposed dashboard, we need this additional data:

### For Each Project

1. **Budgeted Hours** (integer)
   - Total hours allocated for the project
   - Example: 500 hours

2. **Project Start Date** (date)
   - When project began
   - Example: 2025-10-15

3. **Project Target End Date** (date)
   - When project should complete
   - Example: 2025-12-01

4. **Budget Alert Threshold** (percentage, optional)
   - When to show warning
   - Example: 90% = show warning at 450 hours

5. **Project Status** (text, optional)
   - Active, Completed, On Hold, Cancelled
   - Example: Active

### Where This Data Could Live

Option 1: Custom fields on Job Dimensions in Rippling
Option 2: External database linked by project code
Option 3: Spreadsheet we maintain and import

We prefer Option 1 (Rippling custom fields) for single source of truth.

---

## TECHNICAL IMPLEMENTATION

### Current API Calls (Already Working)

```
GET /users
GET /time-entries?start_date=2025-11-11&end_date=2025-11-11
GET /job-dimensions
```

### New API Calls Needed

```
GET /job-dimensions/{id}
  Response should include:
  {
    "id": "dim_001",
    "code": "M-25-0001",
    "name": "Lithium Nevada - Thacker Pass Ducting",
    "custom_fields": {
      "budgeted_hours": 500,
      "start_date": "2025-10-15",
      "target_end_date": "2025-12-01",
      "alert_threshold": 90,
      "status": "Active"
    }
  }
```

### Calculation Logic (We'll Build This)

```python
def calculate_project_status(project):
    budget_hours = project['budgeted_hours']
    hours_worked = project['total_hours_worked']

    percent_complete = (hours_worked / budget_hours) * 100
    hours_remaining = budget_hours - hours_worked

    if percent_complete > 100:
        status = "OVER BUDGET"
        color = "red"
    elif percent_complete > 90:
        status = "AT RISK"
        color = "yellow"
    elif percent_complete < 50:
        status = "EARLY STAGE"
        color = "blue"
    else:
        status = "ON TRACK"
        color = "green"

    return {
        'percent': percent_complete,
        'remaining': hours_remaining,
        'status': status,
        'color': color
    }
```

---

## COLOR CODING SCHEME

### Status Colors

- **Green** (On Track): 50% - 89% complete
- **Blue** (Early Stage): 0% - 49% complete
- **Yellow** (At Risk): 90% - 99% complete
- **Red** (Over Budget): 100%+ complete

### Progress Bar Colors

Same color scheme applies to progress bars:
- Green: Project progressing normally
- Blue: Project just started
- Yellow: Nearing budget limit
- Red: Over budget

---

## BUSINESS VALUE

### For Project Managers

**Before:**
- Manually track hours in spreadsheet
- Find out project is over budget at month end
- No early warning system
- Time-consuming to calculate

**After:**
- Real-time budget tracking
- Instant alerts when approaching limit
- Proactive management
- Data updated automatically

### Time Savings

- Current process: 2-3 hours per week per manager
- New process: 5 minutes per week (just review dashboard)
- Savings: 2-3 hours per week × 3 managers = 6-9 hours per week
- Annual savings: 312-468 hours

### Cost Savings

- Catch budget overruns early
- Reassign resources before it's too late
- Better project estimates for future bids
- Improved profitability per project

---

## PRINT THIS PAGE FOR THE MEETING

Take this mockup to show Rippling exactly what you're trying to build.

Point to the "PROJECT BUDGET STATUS" box and say:
"This is what we want to add. We need to store these budget numbers somewhere in Rippling and pull them via the API."

---

Capitol Engineering
www.capitolaz.com
Date: 2025-11-11 20:12
