@echo off
echo Starting VidyaMitra - Full Stack Application
echo.
echo This will start both Backend and Frontend servers
echo.

REM Start backend in a new window
start "VidyaMitra Backend" cmd /k start-backend.bat

REM Wait a few seconds for backend to start
echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

REM Start frontend in a new window
start "VidyaMitra Frontend" cmd /k start-frontend.bat

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8080
echo.
echo Check the new windows for server logs
echo.
pause
