#!/bin/bash

# Options Scalping Application Launcher
echo "🚀 Launching Options Scalping Dashboard..."

# Activate virtual environment
source bin/activate

# Kill any existing Streamlit processes
pkill -f streamlit 2>/dev/null

# Wait a moment
sleep 2

# Launch the options scalping dashboard
echo "📊 Starting Options Scalping Dashboard at http://localhost:8501"
echo "🌐 Opening browser..."
streamlit run ui/streamlit_app.py --server.headless true --browser.gatherUsageStats false &

# Wait for the server to start
sleep 5

# Open in browser (macOS)
open http://localhost:8501

echo "✅ Options Scalping Dashboard launched successfully!"
echo "📍 URL: http://localhost:8501"
echo "🛑 To stop: pkill -f streamlit"
echo ""
echo "📋 Features Available:"
echo "  • Real-time market data"
echo "  • Advanced signal analysis"
echo "  • Options chain data"
echo "  • Trade history & performance"
echo "  • Automated trading (paper mode)"
echo ""
echo "⚠️  Remember: This is for educational purposes. Use paper trading mode for testing." 