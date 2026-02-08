#!/bin/bash
echo "======================================"
echo "  Starting ShopEase Backend Server"
echo "======================================"
echo ""

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    echo "Then install dependencies: pip install -r requirements.txt"
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Starting Flask server on http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python run.py
