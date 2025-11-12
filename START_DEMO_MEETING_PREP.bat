@echo off
echo ========================================
echo CAPITOL ENGINEERING
echo Meeting Prep Demo Launcher
echo ========================================
echo.
echo Starting Meeting Prep Demo...
echo This includes:
echo  - Complete meeting preparation guide
echo  - API explanations
echo  - Project dashboard mockup
echo  - Working demos
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
echo The Meeting Prep tab will be shown first with:
echo  - 30-second elevator pitch
echo  - Restaurant analogy for APIs
echo  - Budget dashboard mockup
echo  - Questions to ask Rippling
echo  - What you've already built
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start Python and open browser after a delay
start /B python demo_mode_with_meeting_prep.py

REM Wait 3 seconds then open browser
timeout /t 3 /nobreak >nul
start http://localhost:5000

REM Keep window open
echo.
echo Browser opened! Server is running...
echo Press Ctrl+C to stop
pause >nul
