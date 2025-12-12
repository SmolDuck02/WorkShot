@echo off
REM WorkShot Global Launcher Script
REM Copy this file to C:\Users\YOUR_USERNAME\bin\ and add that directory to PATH

echo [*] Checking for running WorkShot instances...

REM Stop all Python processes that are running WorkShot
powershell -Command "Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -and (Get-WmiObject Win32_Process -Filter \"ProcessId = $($_.Id)\").CommandLine -like '*main.py*' } | ForEach-Object { Write-Host '[*] Stopping previous instance (PID: '$_.Id')...'; Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue }"

REM Wait a moment for processes to fully terminate
timeout /t 2 /nobreak >nul 2>&1

REM Navigate to WorkShot directory (UPDATE THIS PATH TO YOUR INSTALLATION)
cd /d "C:\Users\YOUR_USERNAME\WorkShot\WorkShot"

echo [+] Starting WorkShot...
echo.

REM Run Python directly
python main.py

REM Exit cleanly
exit /b


