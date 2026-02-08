#!/bin/bash
echo "======================================"
echo "  Starting ShopEase Frontend Server"
echo "======================================"
echo ""

cd "$(dirname "$0")"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "WARNING: node_modules not found!"
    echo "Installing dependencies..."
    npm install
fi

echo ""
echo "Starting Vite dev server on http://localhost:3000"
echo "Press Ctrl+C to stop the server"
echo ""

npm run dev
