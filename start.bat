@echo off
TITLE BankSecure API Guard Launcher
echo ======================================================================
echo           🏦 BANKSECURE API GUARD - ALL-IN-ONE PLATFORM LAUNCHER
echo ======================================================================
echo.

set PATH=C:\Program Files\nodejs;%PATH%
set PYTHON_EXE=C:\Users\MUKILAN M\AppData\Local\Microsoft\WindowsApps\python3.exe

echo [1/3] Initializing SQLite Database & Baseline Security Test Suite...
cd backend
"%PYTHON_EXE%" -m app.seed
cd ..
echo [OK] Database & Seed Setup Complete.
echo.

echo [2/3] Starting FastAPI Backend Server on http://localhost:8000 ...
cd backend
start "BankSecure Backend Server (Port 8000)" "%PYTHON_EXE%" -m uvicorn app.main:app --host 0.0.0.0 --port 8000
cd ..
echo [OK] Backend Service Running.
echo.

echo [3/3] Starting Vite React Frontend Dashboard on http://localhost:3000 ...
cd frontend
start "BankSecure Web Dashboard (Port 3000)" cmd /k "set PATH=C:\Program Files\nodejs;%%PATH%% && npm run dev"
cd ..
echo [OK] Frontend Service Running.
echo.

echo ======================================================================
echo  🚀 Platform Launching Successfully!
echo  🌐 Dashboard UI: http://localhost:3000
echo  ⚙️ API Gateway:  http://localhost:8000/docs
echo ======================================================================
echo.
timeout /t 3 >nul
start http://localhost:3000
