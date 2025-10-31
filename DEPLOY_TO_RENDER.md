# Deploy to Render.com - Step by Step

Date created: 2025-10-30

## The Easiest Way to Host Your Demo Online (FREE!)

This guide will get your Capitol Engineering demo live on the web in about 10 minutes.

---

## What You'll Get

**Live URL:** https://capitol-engineering-demo.onrender.com

**Features:**
- Accessible from anywhere
- HTTPS (secure) automatically
- Share with anyone via URL
- Professional hosting
- FREE (with limitations)

---

## Before You Start

**What you need:**
1. GitHub account (free)
2. Render account (free)
3. Your Rippling folder (you have this!)
4. 10 minutes

---

## Step 1: Create GitHub Account (if you don't have one)

### Go to github.com

1. Click "Sign up"
2. Enter email, create password
3. Choose username (e.g., "capitolengineering")
4. Verify email
5. Done!

**Time:** 2 minutes

---

## Step 2: Create GitHub Repository

### On GitHub:

1. Click the "+" in top right
2. Select "New repository"
3. Fill in details:
   - **Name:** capitol-rippling-demo
   - **Description:** Capitol Engineering Time Tracking Demo
   - **Public** (check this)
   - **Don't** check "Initialize with README"
4. Click "Create repository"

**Time:** 1 minute

---

## Step 3: Push Your Code to GitHub

### Open Command Prompt in your Rippling folder:

```bash
cd C:\Users\holme\OneDrive\Desktop\Rippling
```

### Initialize Git:

```bash
git init
```

### Add all files:

```bash
git add .
```

### Create first commit:

```bash
git commit -m "Initial commit - Capitol Engineering demo"
```

### Connect to GitHub:

Replace YOUR_USERNAME with your actual GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/capitol-rippling-demo.git
```

### Push to GitHub:

```bash
git branch -M main
git push -u origin main
```

**Note:** GitHub may ask for credentials. Use your GitHub username and a Personal Access Token (not your password).

**To create token:**
1. GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Select "repo" scope
4. Copy token and use it as password

**Time:** 3 minutes

---

## Step 4: Create Render Account

### Go to render.com

1. Click "Get Started"
2. Sign up with GitHub (easiest)
3. Authorize Render to access GitHub
4. You're in!

**Time:** 1 minute

---

## Step 5: Create Web Service on Render

### In Render Dashboard:

1. Click "New +" button (top right)
2. Select "Web Service"
3. Click "Connect" next to your repository
   - If you don't see it, click "Configure GitHub"
   - Give Render access to your repo
4. Repository should now appear - click "Connect"

**Time:** 1 minute

---

## Step 6: Configure Your Service

### Fill in these settings:

**Name:** capitol-engineering-demo
- This becomes your URL: capitol-engineering-demo.onrender.com

**Environment:** Python 3

**Region:** Choose closest to your location
- US East (Ohio) for East Coast
- US West (Oregon) for West Coast

**Branch:** main

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn demo_mode_enhanced:app
```

**Instance Type:** Free

### Click "Create Web Service"

**Time:** 2 minutes

---

## Step 7: Wait for Deployment

Render will:
1. Download your code
2. Install packages
3. Start your app

**Watch the logs** - you'll see:
```
Building...
Installing packages...
Starting service...
Live! ✓
```

**Time:** 2-3 minutes

---

## Step 8: Access Your Demo!

Once you see "Live" with a green checkmark:

**Your demo is online!**

URL format:
```
https://YOUR-SERVICE-NAME.onrender.com
```

Example:
```
https://capitol-engineering-demo.onrender.com
```

Click the URL and your enhanced demo opens!

---

## Important: Free Tier Behavior

### Sleep After Inactivity

**What happens:**
- Free apps sleep after 15 minutes of no traffic
- First visit after sleep takes 30-60 seconds to wake up
- After that, it's fast!

**Solutions:**

1. **Accept it** - Just warn people "first load takes a minute"

2. **Keep it awake** - Use UptimeRobot (free):
   - Go to uptimerobot.com
   - Create free account
   - Add new monitor
   - URL: your Render URL
   - Check every 5 minutes
   - Prevents sleep!

---

## Updating Your Demo

### When you make changes:

1. Save changes locally
2. Commit changes:
   ```bash
   git add .
   git commit -m "Updated demo features"
   git push
   ```
3. Render automatically detects and redeploys!
4. Wait 2-3 minutes
5. Refresh your browser

**Auto-deploy is enabled by default!**

---

## Custom Domain (Optional)

### Want your own domain like demo.capitolaz.com?

**Render supports custom domains:**

1. Buy domain (GoDaddy, Namecheap, etc.)
2. In Render dashboard, click your service
3. Go to "Settings"
4. Click "Add Custom Domain"
5. Enter your domain
6. Update DNS records (Render shows you how)
7. Done!

**Note:** Custom domains work on free tier!

---

## Sharing Your Demo

### Easy sharing options:

**1. Direct URL**
Send the Render URL to anyone:
```
https://capitol-engineering-demo.onrender.com
```

**2. QR Code**
Generate QR code at qr-code-generator.com
- Enter your URL
- Download QR code
- Put on presentations/handouts

**3. Short URL**
Use bit.ly or tinyurl.com:
```
https://bit.ly/capitol-demo
```

**4. Embed in Email**
```html
Check out our new time tracking system:
<a href="https://capitol-engineering-demo.onrender.com">
  View Demo
</a>
```

---

## Troubleshooting

### "Build Failed"

**Check logs in Render:**
- Usually a missing package
- Make sure requirements.txt is pushed
- Verify Python version in runtime.txt

### "Application Error"

**Check Start Command:**
- Should be: gunicorn demo_mode_enhanced:app
- Check for typos

### "Repo Not Found"

**GitHub connection issue:**
- Reconnect Render to GitHub
- Make repo Public
- Refresh Render page

### "Slow First Load"

**Normal for free tier:**
- App is sleeping
- Takes 30-60 seconds to wake
- Fast after that
- Use UptimeRobot to prevent sleep

---

## Monitoring Your Demo

### Render Dashboard shows:

- **Deploy logs** - See build process
- **Service logs** - See visitor activity
- **Metrics** - CPU, memory usage
- **Activity** - Deploy history

### Check visitor activity:
Look for lines like:
```
GET / 200
GET /api/daily-summary 200
```

---

## Cost Breakdown

### Free Tier Includes:
- 750 hours/month (enough for 24/7 with one app)
- HTTPS/SSL included
- Automatic deploys
- Basic metrics
- Email support

### If you need more:
- **Starter:** $7/month
  - No sleep
  - Faster performance
  - More resources

**For a demo, free tier is perfect!**

---

## Security Notes

### Your demo is public!

**What's safe:**
- Demo data (it's fake)
- Code (it's a demo)
- URL (meant to be shared)

**What's NOT safe:**
- Real API tokens (use .env, which is in .gitignore)
- Production data
- Real employee info

**Your .env file is NOT uploaded to GitHub** (thanks to .gitignore)

---

## Next Steps

### After successful deployment:

1. ✓ Test all features online
2. ✓ Share URL with team
3. ✓ Present from anywhere
4. ✓ Get feedback
5. ✓ Deploy production version when ready

---

## Production Version

### When you're ready for real data:

**Option 1: Separate instance**
- Deploy foreman_dashboard.py (production version)
- Add real API token as environment variable in Render
- Use different URL: capitol-engineering-prod.onrender.com

**Option 2: Upgrade demo**
- Add environment variable for RIPPLING_API_TOKEN
- Modify code to use real API when token is present
- Same URL switches to production data

---

## Quick Reference Commands

### Initial Deploy:
```bash
cd C:\Users\holme\OneDrive\Desktop\Rippling
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/capitol-rippling-demo.git
git push -u origin main
```

### Updates:
```bash
git add .
git commit -m "Description of changes"
git push
```

### View Status:
```bash
git status
```

---

## Success Checklist

- [ ] GitHub account created
- [ ] Repository created
- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web service created
- [ ] Configuration complete
- [ ] Deployment successful
- [ ] URL tested and working
- [ ] Demo shared with team

---

## Support

### Render Documentation:
https://render.com/docs/deploy-flask

### GitHub Help:
https://docs.github.com

### Your setup:
- Repository: github.com/YOUR_USERNAME/capitol-rippling-demo
- Demo URL: YOUR-SERVICE-NAME.onrender.com
- Dashboard: dashboard.render.com

---

## Congratulations!

Your Capitol Engineering demo is now live on the web!

Share the URL with your team and present from anywhere.

**Demo URL:** https://capitol-engineering-demo.onrender.com

Capitol Engineering - www.capitolaz.com

Date: 2025-10-30
