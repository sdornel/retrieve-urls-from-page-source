@echo off
title Streamlit URL Extractor
cls

:: Define the virtual environment folder
set VENV_DIR=venv

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python from https://www.python.org/downloads/
    pause
    exit /b
)

:: Check if the virtual environment exists
if not exist %VENV_DIR% (
    echo Creating a virtual environment...
    python -m venv %VENV_DIR%
    echo Installing dependencies in the virtual environment...
    %VENV_DIR%\Scripts\python.exe -m pip install --upgrade pip
    %VENV_DIR%\Scripts\python.exe -m pip install streamlit requests
)

echo Launching Streamlit App...
%VENV_DIR%\Scripts\python.exe -m streamlit run extract_urls_streamlit.py
pause