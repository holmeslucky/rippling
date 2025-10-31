## Rippling API Capabilities - Technical Documentation

Date created: 2025-10-30

## What the Rippling API Provides

This document explains what data and capabilities are available through the Rippling REST API integration.

---

## API Base Information

**Base URL:** https://rest.ripplingapis.com

**Authentication:** Bearer Token (API Token)

**Format:** JSON REST API

**Rate Limits:** Standard Rippling API limits apply

---

## Available Endpoints

### 1. Employee Data API

**Endpoint:** `GET /users`

**What it does:** Retrieves complete employee information from Rippling

**Available Data Fields:**
- Employee ID (unique identifier)
- First Name / Last Name
- Email Address
- Phone Number
- Job Title / Role
- Department / Division
- Employment Status (Active, Inactive, Terminated)
- Hire Date / Start Date
- Manager Information
- Work Location
- Custom Fields (if configured)
- Compensation Details (with permissions)
- Benefits Enrollment (with permissions)

**Use Cases for Capitol Engineering:**
- Crew roster management
- Role-based reporting
- Organizational charts
- Contact directories
- Foreman assignments
- Skill tracking
- Certification management

**Example Response:**
```json
{
  "id": "emp_001",
  "first_name": "John",
  "last_name": "Martinez",
  "employee_id": "CE-101",
  "role": "Welder",
  "department": "Fabrication",
  "status": "Active",
  "hire_date": "2023-01-15",
  "manager_id": "emp_009"
}
```

---

### 2. Time Tracking API

**Endpoint:** `GET /time-entries`

**What it does:** Retrieves all time clock entries and hours worked

**Parameters:**
- start_date (YYYY-MM-DD)
- end_date (YYYY-MM-DD)
- employee_id (optional filter)
- limit (pagination)
- cursor (for next page)

**Available Data Fields:**
- Employee ID
- Entry Date
- Clock In Time (timestamp)
- Clock Out Time (timestamp)
- Total Hours (calculated)
- Break Time (if tracked)
- Job Code / Project Code
- Department / Cost Center
- Approval Status (Pending, Approved, Rejected)
- Overtime Flag
- Location (if GPS enabled)
- Notes / Comments
- Modified By / Modified Date

**Use Cases for Capitol Engineering:**
- Daily labor reports
- Project cost tracking
- Payroll verification
- Overtime management
- Job costing
- Budget tracking
- Foreman review
- Time card approval workflow

**Example Response:**
```json
{
  "id": "time_12345",
  "employee_id": "emp_001",
  "date": "2025-10-30",
  "start_time": "2025-10-30T07:15:00Z",
  "end_time": "2025-10-30T15:30:00Z",
  "hours": 8.25,
  "job_code": "25-2126",
  "status": "Approved",
  "overtime": false
}
```

---

### 3. Job Dimensions API

**Endpoint:** `GET /job-dimensions`

**What it does:** Retrieves project codes, cost centers, and job tracking configuration

**Available Data Fields:**
- Dimension ID
- Dimension Name
- Dimension Type (Project, Cost Center, Department)
- Job Codes List
- Active Status
- Budget Information
- Custom Attributes

**Endpoint:** `GET /job-dimensions/{id}/jobs`

**What it does:** Gets all jobs within a specific dimension

**Use Cases for Capitol Engineering:**
- Project tracking
- Cost allocation
- Budget management
- Job costing
- Bid vs actual analysis
- Department reporting
- Multi-project tracking

**Example Response:**
```json
{
  "id": "dim_001",
  "name": "Project Code",
  "type": "project",
  "jobs": [
    {
      "code": "25-2126",
      "name": "Lithium Nevada - Thacker Pass Ducting",
      "active": true
    }
  ]
}
```

---

## Advanced API Features

### Webhooks (Real-time Updates)

**What it does:** Rippling sends automatic notifications when events occur

**Available Events:**
- Employee hired/terminated
- Time entry created/modified
- Time entry approved
- Project code created/modified
- Department changes

**Use Case:** Get instant notifications when employees clock in/out without polling the API

---

### Pagination

**How it works:** Large datasets are split into pages

**Parameters:**
- `limit` - Number of records per page (max 100, default 50)
- `cursor` - Token for next page

**Example:**
```
GET /time-entries?limit=100&cursor=abc123
```

Returns up to 100 records plus a `next_cursor` for the next page

---

### Filtering and Search

**Available Filters:**
- Date ranges
- Employee ID
- Department
- Job code
- Status
- Custom fields

**Example:**
```
GET /time-entries?start_date=2025-10-01&end_date=2025-10-31&job_code=25-2126
```

Gets all time entries for project 25-2126 in October

---

### Bulk Operations

**What it does:** Process multiple records in single API call

**Use Cases:**
- Bulk approve time entries
- Update multiple job codes
- Mass employee updates

---

## Data Relationships

### How the Data Connects

```
Employee (GET /users)
    ↓
Time Entry (GET /time-entries)
    ↓ (links via job_code)
Job Dimension (GET /job-dimensions)
    ↓
Project/Cost Center
```

**Example Query Flow:**
1. Get all employees → List of employee IDs
2. Get time entries for date range → Hours per employee
3. Get job dimensions → Project names for job codes
4. Combine data → Complete labor report

---

## What You Can Build

### Reports You Can Generate

1. **Daily Labor Report**
   - Who worked today
   - What project they were on
   - How many hours
   - Approval status

2. **Project Cost Report**
   - Total hours per project
   - Labor cost (hours × rate)
   - Budget vs actual
   - Cost overruns

3. **Employee Utilization**
   - Hours worked per employee
   - Utilization percentage
   - Overtime tracking
   - Productivity metrics

4. **Weekly Summary**
   - Hours by day
   - Project distribution
   - Overtime trends
   - Approval rate

5. **Foreman Dashboard**
   - Current crew location
   - Active projects
   - Hours today
   - Who's missing

6. **Payroll Verification**
   - Total hours by employee
   - Regular vs overtime
   - Project allocation
   - Ready for payroll export

---

## Security and Permissions

### API Token Security

**What to know:**
- Tokens have same permissions as the user who created them
- Treat tokens like passwords - never share
- Tokens expire after 30 days of inactivity
- Use environment variables, never hardcode
- Regenerate if compromised

### Data Access

**What you can access depends on your Rippling permissions:**
- Admin users → Full access
- Manager users → Their team only
- Custom roles → As configured

**Best Practice:** Create dedicated API user with minimum required permissions

---

## Performance Considerations

### Response Times

**Typical Response Times:**
- Employee list (100 records): ~500ms
- Time entries (day): ~300ms
- Job dimensions: ~200ms

**Optimization Tips:**
- Use pagination for large datasets
- Cache employee data (changes infrequently)
- Use date filters to limit results
- Make parallel requests when possible

### Rate Limits

**Rippling API Limits:**
- Consult Rippling documentation for current limits
- Implement exponential backoff for retries
- Cache data when appropriate

---

## Integration Benefits

### What This Means for Capitol Engineering

**Time Savings:**
- No manual timesheet entry
- Automated report generation
- Instant data access
- Reduced payroll processing time

**Cost Visibility:**
- Real-time project costs
- Labor allocation tracking
- Budget monitoring
- Better bidding data

**Accuracy:**
- Single source of truth
- No transcription errors
- Automatic calculations
- Audit trail

**Flexibility:**
- Custom reports
- Any date range
- Multiple filter options
- Export to Excel/CSV

---

## API Comparison: TSheets vs Rippling

| Feature | TSheets (Old) | Rippling (New) |
|---------|---------------|----------------|
| API Type | REST | REST |
| Real-time | Limited | Webhooks available |
| Employee Data | Basic | Comprehensive |
| Custom Fields | Limited | Extensive |
| Job Tracking | Yes | Enhanced |
| Integrations | ~100 | 600+ |
| Modern Features | Aging | Current |

---

## Demo vs Production

### What's Different

**Demo System:**
- Uses sample data
- No API token required
- Simulates API responses
- 15 sample employees
- 7 sample projects

**Production System:**
- Uses real Rippling data
- Requires API token
- Live API connections
- Your actual employees
- Your actual projects

**Same Features:**
- Identical interface
- Same reports
- Same functionality
- Same performance

---

## Getting Started with Production

### Setup Steps

1. **Get API Token**
   - Log into Rippling
   - Navigate to API Tokens app
   - Generate new token
   - Copy and secure it

2. **Configure System**
   - Add token to .env file
   - Test connection
   - Verify data access

3. **Deploy**
   - Run on office computer or server
   - Set up for network access
   - Train foremen

### First API Calls

**Test Connection:**
```python
from rippling_api_client import RipplingAPIClient

client = RipplingAPIClient()
employees = client.get_employees(limit=5)
print(f"Connected! Found {len(employees)} employees")
```

**Get Today's Hours:**
```python
import datetime

today = datetime.now().strftime('%Y-%m-%d')
entries = client.get_time_entries(start_date=today, end_date=today)
print(f"Today's time entries: {len(entries)}")
```

---

## Support Resources

### Rippling Documentation

**Official API Docs:** developer.rippling.com

**Key Sections:**
- REST API Reference
- Authentication Guide
- Time Tracking endpoints
- Job Dimensions guide

### Capitol Engineering Support

**Internal Contact:** Blake Holmes

**What we provide:**
- Setup assistance
- Custom report development
- Troubleshooting
- Feature requests

---

## Future Enhancements

### Possible Additions

**Phase 2:**
- Mobile app
- Email reports
- Alerts/notifications
- Budget tracking

**Phase 3:**
- Accounting integration
- Predictive analytics
- Resource planning
- Automated scheduling

---

## Conclusion

The Rippling API provides comprehensive access to your time tracking and employee data, enabling powerful automation and reporting capabilities with zero additional software costs.

**Key Takeaways:**
- Full access to employee, time, and project data
- Real-time updates available via webhooks
- Flexible filtering and search
- Secure token-based authentication
- Same data that powers Rippling itself

**Ready to deploy?** See QUICKSTART.md for production setup instructions.

---

Capitol Engineering
www.capitolaz.com

Date: 2025-10-30
System: Rippling Time Tracking Integration
