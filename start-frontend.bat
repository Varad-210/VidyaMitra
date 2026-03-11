@echo off
echo Starting VidyaMitra Frontend Server...
echo.

REM Check if node_modules exists
if not exist node_modules (
    echo Installing dependencies...
    call npm install
)

echo.
echo Starting frontend on http://localhost:8080
echo.

REM Start the development server
call npm run dev
