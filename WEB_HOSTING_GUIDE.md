# Web Hosting Guide - Deploy Your Demo Online

Date created: 2025-10-30

## Why Host Online?

**Benefits:**
- Access from anywhere
- Share with remote team
- No local computer needed
- Professional URL
- Always available
- Mobile access

**Perfect for:**
- Remote presentations
- Multi-location teams
- Client demonstrations
- Testing from anywhere

---

## Hosting Options (Easiest to Advanced)

---

## OPTION 1: Render.com (RECOMMENDED - FREE!)

**Best for:** Production demo hosting
**Cost:** FREE (with limitations)
**Setup Time:** 10 minutes
**Difficulty:** Easy
**URL:** yourdemo.onrender.com

### Why Render?
- Free tier available
- Automatic deployments from GitHub
- Professional hosting
- SSL certificate included
- Custom domains supported
- Good performance

### Setup Steps:

#### 1. Prepare Your Code
Already done! Your code is ready.

#### 2. Create GitHub Account (if needed)
Go to github.com and sign up for free

#### 3. Create New Repository
```
1. Click "New Repository"
2. Name it: "capitol-rippling-demo"
3. Make it Public
4. Don't initialize with README
5. Click "Create"
```

#### 4. Push Code to GitHub
Open terminal in your Rippling folder:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - Capitol Engineering Rippling Demo"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/capitol-rippling-demo.git

# Push to GitHub
git push -u origin main
```

#### 5. Sign Up for Render
Go to render.com and sign up with GitHub

#### 6. Create New Web Service
```
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select "capitol-rippling-demo"
4. Click "Connect"
```

#### 7. Configure Settings
```
Name: capitol-engineering-demo
Environment: Python 3
Region: Choose closest to you
Branch: main
Build Command: pip install -r requirements.txt
Start Command: gunicorn demo_mode_enhanced:app
```

#### 8. Deploy!
Click "Create Web Service" and wait 2-3 minutes

Your demo will be live at:
```
https://capitol-engineering-demo.onrender.com
```

### Important Notes:

**Free Tier Limitations:**
- Sleeps after 15 minutes of inactivity
- Takes 30 seconds to wake up on first visit
- 750 hours/month free (plenty for demos)

**To Keep It Awake:**
Use a service like UptimeRobot (free) to ping it every 14 minutes

---

## OPTION 2: PythonAnywhere (EASIEST!)

**Best for:** Beginners
**Cost:** FREE
**Setup Time:** 5 minutes
**Difficulty:** Very Easy
**URL:** yourusername.pythonanywhere.com

### Why PythonAnywhere?
- Easiest setup
- Web-based IDE
- No git required
- Good documentation
- Very beginner friendly

### Setup Steps:

#### 1. Sign Up
Go to pythonanywhere.com and create free account

#### 2. Upload Files
```
1. Go to "Files" tab
2. Click "Upload a file"
3. Upload all your .py files
4. Upload requirements.txt
```

#### 3. Create Web App
```
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Flask"
4. Python version: 3.10
5. Path: /home/yourusername/demo_mode_enhanced.py
```

#### 4. Configure
```
1. Source code: /home/yourusername
2. WSGI file: Edit and point to demo_mode_enhanced:app
3. Click "Reload"
```

#### 5. Access
Your demo is live at:
```
https://yourusername.pythonanywhere.com
```

**Free Tier Limitations:**
- Custom domains require paid plan
- Limited CPU time
- Must reload every 3 months

---

## OPTION 3: Railway.app (FAST!)

**Best for:** Modern deployment
**Cost:** FREE with $5 monthly credit
**Setup Time:** 5 minutes
**Difficulty:** Easy
**URL:** your-demo.up.railway.app

### Why Railway?
- Very fast deployment
- Modern interface
- Good free tier
- Easy GitHub integration

### Setup Steps:

#### 1. Push to GitHub (see Render steps above)

#### 2. Sign Up
Go to railway.app and sign up with GitHub

#### 3. Deploy
```
1. Click "New Project"
2. Choose "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Flask
5. Click "Deploy"
```

#### 4. Configure
```
Add Start Command:
gunicorn demo_mode_enhanced:app
```

#### 5. Access
Your demo is live at the Railway URL provided

**Free Tier:**
- $5/month credit
- ~500 hours free
- Great for demos

---

## OPTION 4: Vercel (MODERN!)

**Best for:** Modern serverless
**Cost:** FREE
**Setup Time:** 10 minutes
**Difficulty:** Medium
**URL:** your-demo.vercel.app

### Why Vercel?
- Excellent free tier
- Fast global CDN
- Custom domains easy
- Professional hosting

### Setup Steps:

#### 1. Install Vercel CLI
```bash
npm install -g vercel
```

#### 2. Create vercel.json (we'll create this file)

#### 3. Deploy
```bash
vercel
```

Follow prompts and your demo is live!

---

## Required File for Production

All platforms need this added to requirements.txt:

<function_calls>
<invoke name="Read">
<parameter name="file_path">C:\Users\holme\OneDrive\Desktop\Rippling\requirements.txt