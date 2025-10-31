@echo off
echo ========================================
echo Capitol Engineering - Rippling Setup
echo ========================================
echo.

echo Step 1: Installing Python packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing packages!
    pause
    exit /b 1
)
echo ✓ Packages installed successfully
echo.

echo Step 2: Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo ✓ Created .env file
    echo.
    echo IMPORTANT: Edit the .env file and add your Rippling API token!
    echo Open .env in Notepad and paste your token.
    echo.
) else (
    echo .env file already exists
    echo.
)

echo Step 3: Testing connection...
echo.
python rippling_api_client.py
if %errorlevel% neq 0 (
    echo.
    echo ⚠ Connection test failed!
    echo Make sure you've added your API token to the .env file.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run: python foreman_dashboard.py
echo    Then open: http://localhost:5000
echo.
echo 2. Or run: python project_labor_reports.py
echo    To generate Excel reports
echo.
echo See QUICKSTART.md for more details
echo.
pause
