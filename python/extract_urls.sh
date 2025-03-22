#!/bin/bash
VENV_DIR="venv"
APP_FILE="extract_urls.py"

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed."
    exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
    $VENV_DIR/bin/python -m pip install --upgrade pip
    $VENV_DIR/bin/python -m pip install flask requests
fi

rm -rf $VENV_DIR/lib/python3.10/site-packages/__pycache__

echo "Starting Flask app..."
$VENV_DIR/bin/python $APP_FILE &
FLASK_PID=$!

echo "Waiting for app to fully respond..."
until $VENV_DIR/bin/python -c "
import time
import http.client
while True:
    try:
        conn = http.client.HTTPConnection('localhost', 5000)
        conn.request('GET', '/')
        resp = conn.getresponse()
        if resp.status == 200 and resp.read():
            break
    except:
        pass
    time.sleep(0.2)
"; do :; done

echo "Opening browser..."
xdg-open http://localhost:5000 > /dev/null 2>&1

wait $FLASK_PID
