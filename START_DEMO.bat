@echo off
color 0A
title Capitol Engineering - Demo Mode

echo.
echo ========================================================================
echo   CAPITOL ENGINEERING - TIME TRACKING DEMO
echo ========================================================================
echo.
echo   This demonstration shows the Rippling integration system
echo   using realistic sample data from Capitol Engineering
echo.
echo   Perfect for presentations and team previews!
echo.
echo ========================================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)
echo ✓ Python is installed
echo.

echo Installing required packages...
pip install flask pandas openpyxl --quiet
if %errorlevel% neq 0 (
    echo WARNING: Some packages may not have installed correctly
    echo Trying to continue anyway...
)
echo ✓ Packages ready
echo.

echo.
echo ========================================================================
echo   STARTING DEMO SERVER...
echo ========================================================================
echo.
echo   The demo will open in your browser automatically
echo   If it doesn't, manually go to: http://localhost:5000
echo.
echo   Features you can demonstrate:
echo   • Real-time project labor tracking
echo   • Daily employee time summaries
echo   • Project breakdown by hours
echo   • Excel report export
echo   • Easy-to-use foreman interface
echo.
echo   Press Ctrl+C to stop the demo server
echo.
echo ========================================================================
echo.

timeout /t 3 /nobreak >nul

start http://localhost:5000

python demo_mode.py

pause
