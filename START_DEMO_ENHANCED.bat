@echo off
color 0B
title Capitol Engineering - Enhanced API Demo

echo.
echo ========================================================================
echo   CAPITOL ENGINEERING - ENHANCED API DEMO
echo ========================================================================
echo.
echo   Full Rippling API Capabilities Showcase
echo.
echo   NEW FEATURES IN THIS DEMO:
echo   • Interactive charts and analytics
echo   • API endpoint documentation
echo   • Employee utilization tracking
echo   • Advanced filtering and search
echo   • Weekly trend analysis
echo   • Multi-tab interface
echo.
echo ========================================================================
echo.

echo Installing required packages (including Chart.js support)...
pip install flask pandas openpyxl --quiet
if %errorlevel% neq 0 (
    echo WARNING: Some packages may not have installed correctly
)
echo ✓ Packages ready
echo.

echo.
echo ========================================================================
echo   STARTING ENHANCED DEMO SERVER...
echo ========================================================================
echo.
echo   Dashboard URL: http://localhost:5000
echo.
echo   DEMO TABS:
echo   1. Dashboard     - Real-time labor tracking
echo   2. Analytics     - Charts and trends
echo   3. API Info      - What Rippling API can do
echo   4. Employees     - Detailed analytics
echo.
echo   Press Ctrl+C to stop the demo
echo.
echo ========================================================================
echo.

timeout /t 2 /nobreak >nul

start http://localhost:5000

python demo_mode_enhanced.py

pause
