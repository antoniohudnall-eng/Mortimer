#!/bin/bash
# Cryptonio Live Dashboard Launcher
# Start the real-time dashboard with all visualizations

echo "=========================================="
echo "🚀 Cryptonio Live Dashboard Starting..."
echo "=========================================="
echo ""

cd /root/.openclaw/workspace/agent_sandboxes/the-great-cryptonio

# Check if already running
if pgrep -f "dashboard_server.py" > /dev/null; then
    echo "⚠️ Dashboard server already running"
    echo "Kill existing process first: pkill -f dashboard_server.py"
    exit 1
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip show flask >/dev/null 2>&1 || pip install flask flask-cors websockets

echo ""
echo "🌐 Dashboard starting at:"
echo "   HTTP: http://localhost:5000"
echo "   WebSocket: ws://localhost:8765"
echo ""
echo "📊 Features:"
echo "   ✓ Real-time pie chart (crypto colors)"
echo "   ✓ Portfolio value line chart"
echo "   ✓ Exchange bars with totals"
echo "   ✓ Open trades list"
echo "   ✓ Holdings by asset grid"
echo ""

# Source credentials and run
source ./run_with_credentials.sh

# Run dashboard
python3 dashboard_server.py
