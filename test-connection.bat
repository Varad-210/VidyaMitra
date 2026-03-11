@echo off
echo Testing VidyaMitra Backend Connection...
echo.

echo Testing Backend Health Endpoint...
curl -s http://localhost:8000/health

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Backend is running and healthy!
) else (
    echo.
    echo ❌ Backend is not responding!
    echo Please start the backend server first using start-backend.bat
)

echo.
echo.
echo Testing Frontend...
curl -s -o nul -w "Frontend Status: %%{http_code}\n" http://localhost:8080

echo.
pause
