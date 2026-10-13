@echo off
title AttendEase Database Initializer
echo ===================================================
echo Initializing AttendEase MySQL Database...
echo ===================================================
if "%~1"=="" (
    py init_db.py
) else (
    py init_db.py --password %1
)
pause
