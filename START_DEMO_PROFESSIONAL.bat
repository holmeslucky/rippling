@echo off
echo ========================================
echo CAPITOL ENGINEERING
echo Professional Dashboard Launcher
echo ========================================
echo.
echo Starting Professional Project Dashboard...
echo.
echo Features:
echo  - Clean corporate design
echo  - Project budget tracking
echo  - Status indicators and progress bars
echo  - Real-time hours vs budget
echo  - Professional blue/slate colors
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Check if demo_data_generator.py exists
if not exist "demo_data_generator.py" (
    echo ERROR: demo_data_generator.py not found
    echo Please run from the project directory
    pause
    exit /b 1
)

REM Start the Flask server
echo.
echo Starting Flask server...
echo Dashboard will open automatically at http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start Python and open browser after a delay
start /B python demo_mode_professional.py

REM Wait 3 seconds then open browser
timeout /t 3 /nobreak >nul
start http://localhost:5000

REM Keep window open
echo.
echo Browser opened! Dashboard is running...
echo Press Ctrl+C to stop
pause >nul
