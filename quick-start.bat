@echo off
REM Quick Start Script for UrbanPulse AI Dashboard

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║   UrbanPulse AI - Premium Smart City Dashboard          ║
echo ║   Quick Start Setup                                      ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Check Python
echo ✓ Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Check Node
echo ✓ Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Node.js not found. Please install Node.js 16+
    pause
    exit /b 1
)

echo.
echo 📦 Installing dependencies...
echo.

REM Install Python dependencies
echo Installing Python packages...
pip install -r requirements-api.txt

REM Install frontend
echo.
echo Installing Node packages...
cd frontend
call npm install
cd ..

echo.
echo ✅ Setup complete!
echo.
echo 🚀 To start the dashboard:
echo.
echo    Terminal 1 (Flask API):
echo    $ python src/dashboard/api.py
echo.
echo    Terminal 2 (React Frontend):
echo    $ cd frontend ^&^& npm run dev
echo.
echo    Then open: http://localhost:3000
echo.
echo 📚 Documentation: see DASHBOARD_REDESIGN_GUIDE.md
echo 📖 Frontend README: frontend\README.md
echo.
pause
