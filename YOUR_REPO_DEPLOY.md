# Deploy to Your GitHub Repository

Date created: 2025-10-30

## Your Repository
https://github.com/holmeslucky/rippling.git

---

## FASTEST METHOD (5 Minutes)

### Double-click: DEPLOY_NOW.bat

This automated script will:
1. Initialize Git
2. Commit your code
3. Push to https://github.com/holmeslucky/rippling.git
4. Open Render.com for deployment

**That's it!**

---

## Manual Method

### Step 1: Push to GitHub

Open Command Prompt in your Rippling folder:

```bash
cd C:\Users\holme\OneDrive\Desktop\Rippling
```

### Initialize and commit:

```bash
git init
git add .
git commit -m "Deploy Capitol Engineering Rippling demo"
```

### Connect to your repository:

```bash
git remote add origin https://github.com/holmeslucky/rippling.git
git branch -M main
```

### Push to GitHub:

```bash
git push -u origin main
```

**Note:** GitHub will ask for credentials:
- Username: `holmeslucky`
- Password: Use a **Personal Access Token** (not your password!)

### Get Personal Access Token:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name: "Rippling Deploy"
4. Select scope: **repo** (check the box)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)
7. Use this token as your password when pushing

---

## Step 2: Deploy to Render.com

### Create Render Account:

1. Go to: https://render.com
2. Click "Get Started"
3. Sign up with GitHub (easiest!)
4. Authorize Render to access GitHub

### Create Web Service:

1. Click "New +" button
2. Select "Web Service"
3. Click "Connect" next to **holmeslucky/rippling**
4. If you don't see it:
   - Click "Configure GitHub App"
   - Give Render access to the repository
   - Refresh and try again

### Configure Service:

**Name:** `capitol-engineering-demo`
- Your URL will be: capitol-engineering-demo.onrender.com

**Environment:** `Python 3`

**Region:** Choose closest to you
- US East (Ohio)
- US West (Oregon)

**Branch:** `main`

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn demo_mode_enhanced:app
```

**Instance Type:** `Free`

### Click "Create Web Service"

---

## Step 3: Wait for Deployment

Render will:
1. Clone your repository
2. Install packages (requirements.txt)
3. Start the app with gunicorn
4. Provide you a URL

**Watch the logs:**
```
Building...
Installing dependencies...
Starting service...
Your service is live! ✓
```

**Takes 2-3 minutes**

---

## Step 4: Access Your Demo!

Your demo will be live at:

```
https://capitol-engineering-demo.onrender.com
```

Click the URL and your enhanced demo loads!

---

## Important Notes

### Free Tier Behavior:

**Automatic Sleep:**
- Free apps sleep after 15 minutes of inactivity
- First visit takes 30-60 seconds to wake up
- After that, it's fast!

**To Keep Awake:**
Use UptimeRobot (free):
1. Go to: https://uptimerobot.com
2. Create free account
3. Add monitor for your Render URL
4. Check every 5 minutes
5. App stays awake!

---

## Updating Your Demo

### When you make changes:

```bash
git add .
git commit -m "Updated features"
git push
```

Render automatically detects the push and redeploys!

**Auto-deploy is enabled by default**

---

## Your URLs

**GitHub Repository:**
https://github.com/holmeslucky/rippling

**Demo URL (after deployment):**
https://capitol-engineering-demo.onrender.com

**Render Dashboard:**
https://dashboard.render.com

---

## Troubleshooting

### "Repository doesn't exist"

Create it on GitHub:
1. Go to: https://github.com/new
2. Repository name: `rippling`
3. Public (check this)
4. Don't initialize with README
5. Click "Create repository"
6. Run DEPLOY_NOW.bat again

### "Authentication failed"

You need a Personal Access Token:
1. Go to: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select "repo" scope
4. Use token as password

### "Build failed on Render"

Check the logs:
- Usually missing package
- Verify requirements.txt pushed to GitHub
- Check Python version in runtime.txt

### "Application error"

Check Start Command:
- Should be: `gunicorn demo_mode_enhanced:app`
- No typos
- Case sensitive

---

## Quick Commands Reference

### Initial Push:
```bash
git init
git add .
git commit -m "Initial deploy"
git remote add origin https://github.com/holmeslucky/rippling.git
git branch -M main
git push -u origin main
```

### Updates:
```bash
git add .
git commit -m "Updated demo"
git push
```

### Check Status:
```bash
git status
```

---

## Sharing Your Demo

### Direct Link:
```
https://capitol-engineering-demo.onrender.com
```

### QR Code:
Generate at: https://www.qr-code-generator.com

### Short URL:
Create at: https://bitly.com
Example: https://bit.ly/capitol-demo

### Email:
```
Check out our new time tracking system:
https://capitol-engineering-demo.onrender.com
```

---

## Next Steps

### After Deployment:

1. ✓ Test all features
2. ✓ Share URL with team
3. ✓ Present from anywhere
4. ✓ Get feedback
5. ✓ Deploy production when ready

---

## Production Version

### When approved:

**Option 1: Separate Production Instance**
- Deploy foreman_dashboard.py
- Add RIPPLING_API_TOKEN environment variable
- Use different URL

**Option 2: Environment-Based**
- Same code
- Add environment variable in Render
- Switches to real data when token present

---

## Support

**GitHub Issues:**
https://github.com/holmeslucky/rippling/issues

**Render Docs:**
https://render.com/docs/deploy-flask

**Capitol Engineering:**
Contact: Blake Holmes
Website: www.capitolaz.com

---

## Success Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web service configured
- [ ] Deployment successful
- [ ] URL tested and working
- [ ] Demo shared with team
- [ ] Stakeholder approval received

---

Capitol Engineering
www.capitolaz.com

Your repository: https://github.com/holmeslucky/rippling
Your demo: https://capitol-engineering-demo.onrender.com

Date: 2025-10-30
Status: Ready to Deploy
