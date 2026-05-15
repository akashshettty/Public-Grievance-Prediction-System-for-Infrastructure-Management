@echo off
REM UrbanPulse AI Dashboard - Setup Script for Windows

echo.
echo 🚀 UrbanPulse AI Dashboard - Setup Script
echo ==========================================
echo.

echo Installing Python dependencies...
pip install -r requirements-api.txt

echo.
echo Setting up frontend...
cd frontend
call npm install

echo.
echo Building frontend...
call npm run build

cd ..

echo.
echo ✅ Setup complete!
echo.
echo To start the dashboard:
echo 1. Start Flask API: python src/dashboard/api.py
echo 2. Start React dev server: cd frontend ^&^& npm run dev
echo 3. Open http://localhost:3000 in your browser
echo.
echo For production:
echo npm run build in frontend folder creates optimized build
pause
