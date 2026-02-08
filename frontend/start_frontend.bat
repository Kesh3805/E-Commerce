@echo off
echo ======================================
echo   Starting ShopEase Frontend Server
echo ======================================
echo.
cd /d "%~dp0"

REM Check if node_modules exists
if not exist "node_modules\" (
    echo WARNING: node_modules not found!
    echo Installing dependencies...
    call npm install
)

echo.
echo Starting Vite dev server on http://localhost:3000
echo Press Ctrl+C to stop the server
echo.

npm run dev

pause
