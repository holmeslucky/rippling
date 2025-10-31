# Deploy Quick Reference Card

Your GitHub: https://github.com/holmeslucky/rippling.git

---

## EASIEST DEPLOYMENT (5 Minutes)

### Double-click: DEPLOY_NOW.bat

**This will:**
1. ✓ Commit your code to Git
2. ✓ Push to GitHub (holmeslucky/rippling)
3. ✓ Open Render.com for you
4. ✓ Open your GitHub repo

**Then on Render.com:**
1. Sign up with GitHub
2. New + → Web Service
3. Connect to holmeslucky/rippling
4. Name: capitol-engineering-demo
5. Build: `pip install -r requirements.txt`
6. Start: `gunicorn demo_mode_enhanced:app`
7. Create Web Service

**Result:** https://capitol-engineering-demo.onrender.com

---

## Your Credentials

**GitHub Username:** holmeslucky

**GitHub Password:** Use Personal Access Token
- Get at: https://github.com/settings/tokens
- Generate new token (classic)
- Select "repo" scope
- Copy token, use as password

**Repository:** https://github.com/holmeslucky/rippling.git

---

## Quick Commands

### First Deploy:
```bash
git init
git add .
git commit -m "Deploy demo"
git remote add origin https://github.com/holmeslucky/rippling.git
git branch -M main
git push -u origin main
```

### Updates:
```bash
git add .
git commit -m "Updated"
git push
```

---

## Your URLs

**GitHub:** https://github.com/holmeslucky/rippling
**Demo:** https://capitol-engineering-demo.onrender.com
**Render:** https://dashboard.render.com

---

## Files Created

All ready to deploy:
- ✓ Procfile
- ✓ runtime.txt
- ✓ .gitignore
- ✓ requirements.txt (with gunicorn)

---

## Next Step

**Double-click: DEPLOY_NOW.bat**

Capitol Engineering - www.capitolaz.com
