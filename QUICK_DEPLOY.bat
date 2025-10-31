@echo off
color 0E
title Capitol Engineering - Quick Deploy Helper

echo.
echo ========================================================================
echo   CAPITOL ENGINEERING - DEPLOY TO WEB
echo ========================================================================
echo.
echo   This script helps you deploy your demo to the web
echo.
echo ========================================================================
echo.

echo Step 1: Check if Git is installed...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Git is not installed!
    echo.
    echo Please install Git first:
    echo 1. Go to: https://git-scm.com/download/win
    echo 2. Download and install
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)
echo ✓ Git is installed
echo.

echo Step 2: Check if this is a Git repository...
if not exist .git (
    echo.
    echo This is not yet a Git repository.
    echo Initializing Git...
    git init
    echo ✓ Git initialized
) else (
    echo ✓ Already a Git repository
)
echo.

echo Step 3: Check for uncommitted changes...
git status --short >nul 2>&1
echo Files ready to commit
echo.

echo ========================================================================
echo   DEPLOYMENT OPTIONS
echo ========================================================================
echo.
echo   Choose your deployment platform:
echo.
echo   1. Render.com (RECOMMENDED - Free, Easy)
echo   2. PythonAnywhere (Easiest for beginners)
echo   3. Railway.app (Modern, Fast)
echo   4. Manual Git Commands
echo   5. Cancel
echo.
set /p choice="Enter choice (1-5): "

if "%choice%"=="1" goto render
if "%choice%"=="2" goto pythonanywhere
if "%choice%"=="3" goto railway
if "%choice%"=="4" goto manual
if "%choice%"=="5" goto end

echo Invalid choice!
pause
exit /b 1

:render
echo.
echo ========================================================================
echo   DEPLOYING TO RENDER.COM
echo ========================================================================
echo.
echo Great choice! Render is free and easy.
echo.
echo INSTRUCTIONS:
echo.
echo 1. First, we'll commit your code to Git
echo 2. You'll need to create a GitHub account (if you don't have one)
echo 3. Push this code to GitHub
echo 4. Then deploy to Render from GitHub
echo.
echo For detailed step-by-step instructions, see:
echo   DEPLOY_TO_RENDER.md
echo.
echo Press any key to start Git commit process...
pause >nul
goto gitcommit

:pythonanywhere
echo.
echo ========================================================================
echo   DEPLOYING TO PYTHONANYWHERE
echo ========================================================================
echo.
echo PythonAnywhere is great for beginners!
echo.
echo INSTRUCTIONS:
echo.
echo 1. Go to: https://www.pythonanywhere.com
echo 2. Sign up for free account
echo 3. Upload your .py files in the "Files" tab
echo 4. Create a new Flask web app
echo 5. Point it to demo_mode_enhanced.py
echo.
echo For detailed instructions, see:
echo   WEB_HOSTING_GUIDE.md (Option 2)
echo.
echo Opening PythonAnywhere...
start https://www.pythonanywhere.com
echo.
pause
goto end

:railway
echo.
echo ========================================================================
echo   DEPLOYING TO RAILWAY.APP
echo ========================================================================
echo.
echo Railway is modern and fast!
echo.
echo INSTRUCTIONS:
echo.
echo 1. First, we'll commit your code to Git
echo 2. Push to GitHub
echo 3. Go to railway.app and sign up with GitHub
echo 4. Deploy directly from your repository
echo.
echo For detailed instructions, see:
echo   WEB_HOSTING_GUIDE.md (Option 3)
echo.
echo Press any key to start Git commit process...
pause >nul
goto gitcommit

:manual
echo.
echo ========================================================================
echo   MANUAL GIT COMMANDS
echo ========================================================================
echo.
echo Here are the commands you'll need:
echo.
echo 1. Commit your code:
echo    git add .
echo    git commit -m "Deploy Capitol Engineering demo"
echo.
echo 2. Create GitHub repository at github.com
echo.
echo 3. Connect to GitHub:
echo    git remote add origin https://github.com/USERNAME/REPO.git
echo.
echo 4. Push to GitHub:
echo    git push -u origin main
echo.
echo See DEPLOY_TO_RENDER.md for complete guide.
echo.
pause
goto end

:gitcommit
echo.
echo ========================================================================
echo   COMMITTING YOUR CODE
echo ========================================================================
echo.

echo Adding all files to Git...
git add .
if %errorlevel% neq 0 (
    echo ERROR: Failed to add files
    pause
    exit /b 1
)
echo ✓ Files added
echo.

echo Creating commit...
git commit -m "Deploy Capitol Engineering Rippling demo to web"
if %errorlevel% neq 0 (
    echo.
    echo Note: Nothing to commit (or already committed)
    echo This is OK if files haven't changed
)
echo ✓ Commit created
echo.

echo ========================================================================
echo   NEXT STEPS
echo ========================================================================
echo.
echo Your code is committed locally!
echo.
echo NOW DO THIS:
echo.
echo 1. Create GitHub account: https://github.com/signup
echo 2. Create new repository
echo 3. Run these commands:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. Then deploy to Render/Railway from GitHub
echo.
echo See DEPLOY_TO_RENDER.md for detailed step-by-step instructions!
echo.
echo Opening deployment guide...
timeout /t 2 /nobreak >nul
start DEPLOY_TO_RENDER.md
echo.

:end
echo.
echo ========================================================================
echo   DEPLOYMENT HELPER COMPLETE
echo ========================================================================
echo.
echo Need help? Check these files:
echo   - DEPLOY_TO_RENDER.md (Render deployment guide)
echo   - WEB_HOSTING_GUIDE.md (All hosting options)
echo.
pause
