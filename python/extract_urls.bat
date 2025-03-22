@echo off
title Flask URL Extractor
cls

set VENV_DIR=venv

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python from https://www.python.org/downloads/
    pause
    exit /b
)

if not exist %VENV_DIR% (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
    echo Installing dependencies in the virtual environment...
    %VENV_DIR%\Scripts\python.exe -m pip install --upgrade pip
    %VENV_DIR%\Scripts\python.exe -m pip install flask requests
)

echo Launching Flask App...
start http://localhost:5000
%VENV_DIR%\Scripts\python.exe app.py

pause