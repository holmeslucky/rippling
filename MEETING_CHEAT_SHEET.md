# Meeting Cheat Sheet - Rippling API Discussion

Date: Thursday, 2025-11-14
Quick Reference for Blake Holmes

---

## The 30-Second Explanation

"We built a dashboard that pulls employee time data from Rippling's API. It shows who worked on which projects and for how many hours. Now we want to add project budget tracking - comparing hours worked vs hours budgeted - so we can see if projects are on track or over budget. We need help storing budget data in Rippling and accessing it via the API."

---

## What is an API? (Simple Answer)

"An API is like a waiter in a restaurant. We can't go into the kitchen (Rippling's database) ourselves, so we tell the waiter (API) what we want, and it brings us the data. It's an automatic way for our computer to ask Rippling for employee and time tracking information."

---

## What We've Already Built

- Dashboard showing employee hours by project
- Daily labor reports in Excel
- Web interface for foremen
- Automatic data refresh every 5 minutes
- Working API connection to Rippling

Demo: http://localhost:5000 or https://capitol-engineering-demo.onrender.com

---

## What We Want to Add

PROJECT BUDGET TRACKING

Show this for each project:
- Job Number: M-25-0001
- Budgeted hours: 500 hrs
- Hours worked: 387 hrs
- Remaining: 113 hrs (23%)
- Status: ON TRACK / OVER BUDGET

---

## Main Questions to Ask

### 1. Where can we store project budget data?
- Custom field on job dimensions?
- Separate project table?
- External integration?

### 2. What API access do we need?
- Current: /users, /time-entries
- Need: /job-dimensions, project budget fields

### 3. Can we add custom fields?
- Budgeted Hours
- Project Status
- Start/End Dates

### 4. What are the API limits?
- We'll make ~288 calls per day
- Any restrictions?

### 5. Do you support webhooks?
- For real-time clock in/out notifications

---

## What We Need

1. API token with project data access
2. Place to store budget numbers
3. Documentation on project fields
4. Timeline for setup

---

## Value Proposition

- See project status in real-time
- Prevent budget overruns
- Better resource allocation
- Improve future bidding
- Save project managers hours per week

---

## Technical Details (If Asked)

- Language: Python
- Authentication: Bearer token
- Protocol: HTTPS REST API
- Base URL: https://rest.ripplingapis.com
- Update frequency: Every 5 minutes
- Security: Token stored in environment variables

---

## Files to Reference

- MEETING_PREP_GUIDE.md - Complete detailed guide
- API_CAPABILITIES.md - What Rippling API provides
- README.md - Full system documentation

---

## If You Get Stuck

**Fall back to:** "Let me check my documentation" and refer to MEETING_PREP_GUIDE.md

**Key phrases:**
- "We're already successfully pulling time entries"
- "We just need to expand to include budget data"
- "The system is working, we just need guidance on this one piece"

---

## After Meeting - Action Items

- [ ] Get new API token (if needed)
- [ ] Receive field documentation
- [ ] Set up custom fields
- [ ] Schedule follow-up
- [ ] Update coworker

---

## Contact Info

Capitol Engineering: www.capitolaz.com
Blake Holmes
Live Demo: https://capitol-engineering-demo.onrender.com

---

YOU'VE GOT THIS! Keep it simple, show what you've built, explain what you need.
