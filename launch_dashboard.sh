#!/bin/bash

# Stock Analysis Dashboard Launcher
echo "🚀 Launching Stock Analysis Dashboard..."

# Activate virtual environment
source bin/activate

# Kill any existing Streamlit processes
pkill -f streamlit 2>/dev/null

# Wait a moment
sleep 2

# Launch the dashboard with Schwab API
echo "📊 Starting Schwab API Dashboard at http://localhost:8501"
echo "🌐 Opening browser..."
streamlit run enhanced_dashboard.py --server.headless true --browser.gatherUsageStats false &

# Wait for the server to start
sleep 5

# Open in browser (macOS)
open http://localhost:8501

echo "✅ Dashboard launched successfully!"
echo "📍 URL: http://localhost:8501"
echo "🛑 To stop: pkill -f streamlit" 