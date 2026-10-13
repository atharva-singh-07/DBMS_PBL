@echo off
title AttendEase Server
echo ===================================================
echo Starting AttendEase Web Server...
echo ===================================================
where python >nul 2>nul
if %errorlevel% equ 0 (
    python app.py
) else (
    py app.py
)
pause
