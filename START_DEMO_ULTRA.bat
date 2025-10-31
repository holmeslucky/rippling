@echo off
color 0C
title Capitol Engineering - ULTRA Demo (All Features)

echo.
echo ========================================================================
echo   CAPITOL ENGINEERING - ULTRA DEMO
echo ========================================================================
echo.
echo   THIS DEMO SHOWS EVERYTHING INCLUDING FUTURE FEATURES:
echo.
echo   🔔 Smart Alerts System
echo      - AI-powered insights
echo      - Budget warnings
echo      - Proactive recommendations
echo.
echo   💰 Cost Tracking
echo      - Real-time project costs
echo      - Budget vs actual
echo      - Profit margin analysis
echo      - Labor cost tracking
echo.
echo   ⏰ Overtime Prediction
echo      - Who's approaching OT
echo      - Risk levels
echo      - Reallocation suggestions
echo.
echo   🔮 Future Features Roadmap
echo      - See what's coming
echo      - Implementation timelines
echo      - Feature status
echo.
echo ========================================================================
echo.

echo Installing packages...
pip install flask pandas --quiet
echo.

echo Starting ULTRA demo server...
echo.
echo Dashboard will open at: http://localhost:5000
echo.
timeout /t 2 /nobreak >nul

start http://localhost:5000

python demo_mode_ultra.py

pause
