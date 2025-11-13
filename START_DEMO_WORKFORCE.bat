@echo off
echo ========================================
echo Capitol Engineering
echo Workforce-Style Project Dashboard
echo ========================================
echo.
echo Starting server...
echo.
echo Dashboard will open at: http://localhost:5000
echo.
echo Features:
echo  - Project overview with drill-down
echo  - Budget vs Actual tracking
echo  - Task-level breakdown
echo  - Employee labor allocation
echo  - Detailed timesheet entries
echo  - Excel export per project
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

start http://localhost:5000
python demo_mode_workforce.py

pause
