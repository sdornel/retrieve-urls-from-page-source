#!/bin/bash
VENV_DIR="venv"

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Please install Python from https://www.python.org/downloads/"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
    echo "Installing dependencies in the virtual environment..."
    $VENV_DIR/bin/python3 -m pip install --upgrade pip
    $VENV_DIR/bin/python3 -m pip install streamlit requests
fi

echo "Launching Streamlit App..."
$VENV_DIR/bin/python3 -m streamlit run extract_urls.py