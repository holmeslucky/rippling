@echo off
color 0A
title Capitol Engineering - Deploy to GitHub & Render

echo.
echo ========================================================================
echo   CAPITOL ENGINEERING - QUICK DEPLOY
echo ========================================================================
echo.
echo   Deploying to: https://github.com/holmeslucky/rippling.git
echo.
echo ========================================================================
echo.

echo Checking Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo ✓ Git installed
echo.

echo Initializing Git repository (if needed)...
if not exist .git (
    git init
    echo ✓ Git initialized
) else (
    echo ✓ Already initialized
)
echo.

echo Adding all files...
git add .
echo ✓ Files staged
echo.

echo Creating commit...
git commit -m "Deploy Capitol Engineering Rippling demo"
if %errorlevel% neq 0 (
    echo Note: Files already committed or no changes
)
echo.

echo Setting up remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/holmeslucky/rippling.git
echo ✓ Remote added
echo.

echo Setting main branch...
git branch -M main
echo ✓ Branch set
echo.

echo.
echo ========================================================================
echo   READY TO PUSH
echo ========================================================================
echo.
echo About to push to: https://github.com/holmeslucky/rippling.git
echo.
echo GitHub will ask for credentials:
echo   Username: holmeslucky
echo   Password: Your GitHub Personal Access Token (NOT your password!)
echo.
echo Don't have a token? Get one at:
echo   https://github.com/settings/tokens
echo   - Click "Generate new token (classic)"
echo   - Select "repo" scope
echo   - Copy the token
echo.
pause
echo.

echo Pushing to GitHub...
git push -u origin main
if %errorlevel% neq 0 (
    echo.
    echo ========================================================================
    echo   PUSH FAILED
    echo ========================================================================
    echo.
    echo Common issues:
    echo   1. Need to create Personal Access Token
    echo   2. Repository doesn't exist yet
    echo   3. Incorrect credentials
    echo.
    echo To create the repository:
    echo   1. Go to: https://github.com/holmeslucky
    echo   2. Click "New repository"
    echo   3. Name it: rippling
    echo   4. Click "Create repository"
    echo   5. Run this script again
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo   SUCCESS! CODE PUSHED TO GITHUB
echo ========================================================================
echo.
echo Your code is now at:
echo   https://github.com/holmeslucky/rippling
echo.
echo ========================================================================
echo   NEXT: DEPLOY TO RENDER.COM
echo ========================================================================
echo.
echo 1. Go to: https://render.com
echo 2. Sign up / Log in with GitHub
echo 3. Click "New +" then "Web Service"
echo 4. Connect to: holmeslucky/rippling
echo 5. Configure:
echo      Name: capitol-engineering-demo
echo      Build Command: pip install -r requirements.txt
echo      Start Command: gunicorn demo_mode_enhanced:app
echo 6. Click "Create Web Service"
echo.
echo Your demo will be live at:
echo   https://capitol-engineering-demo.onrender.com
echo.
echo Opening Render.com...
timeout /t 3 /nobreak >nul
start https://render.com
echo.
echo Opening your GitHub repo...
start https://github.com/holmeslucky/rippling
echo.
pause
