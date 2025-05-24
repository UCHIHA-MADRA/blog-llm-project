@echo off
echo 🚀 Starting Blog LLM Project...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)

REM Install dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

REM Start API server
echo 🌐 Starting API server...
start "API Server" cmd /k "cd api && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a bit for API to start
timeout /t 5 /nobreak >nul

REM Start frontend server
echo 🎨 Starting frontend server...
start "Frontend Server" cmd /k "cd frontend && python -m http.server 8080"

echo ✅ All services started!
echo.
echo 🌐 Frontend: http://localhost:8080
echo 🔧 API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Press any key to continue...
pause >nul