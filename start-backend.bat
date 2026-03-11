@echo off
echo Starting VidyaMitra Backend Server...
echo.

cd backend

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo Please edit backend\.env and add your API keys!
    echo.
    pause
)

REM Check if virtual environment exists
if not exist venv311 (
    echo Creating virtual environment...
    python -m venv venv311
)

REM Activate virtual environment
call venv311\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting server on http://localhost:8000
echo API Docs available at http://localhost:8000/docs
echo.

REM Start the server
python main.py
