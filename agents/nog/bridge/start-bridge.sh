#!/bin/bash
# nognog-bridge.sh - Start the N'og nog Brain Bridge

echo "Starting N'og nog Brain Bridge..."
echo "================================"

# Check if brain socket exists
if [ ! -S /tmp/aos_brain.sock ]; then
    echo "⚠️  Brain socket not found at /tmp/aos_brain.sock"
    echo "   Is the AOS Brain running?"
    echo "   Try: systemctl start aos-brain-v4"
    exit 1
fi

# Check if bridge is already running
if pgrep -f "bridge_server.py" > /dev/null; then
    echo "ℹ️  Bridge server is already running"
    echo "   PID: $(pgrep -f 'bridge_server.py')"
else
    echo "🚀 Starting bridge server..."
    cd /root/.openclaw/workspace/nognog/bridge
    nohup python3 bridge_server.py > /var/log/aos/nognog-bridge.log 2>&1 &
    sleep 2
    
    if pgrep -f "bridge_server.py" > /dev/null; then
        echo "✅ Bridge server started successfully"
        echo "   PID: $(pgrep -f 'bridge_server.py')"
        echo "   Log: /var/log/aos/nognog-bridge.log"
    else
        echo "❌ Failed to start bridge server"
        exit 1
    fi
fi

echo ""
echo "Bridge Status:"
echo "=============="
echo "WebSocket: ws://localhost:8765"
echo "Brain Socket: /tmp/aos_brain.sock"
echo ""
echo "To view log: tail -f /var/log/aos/nognog-bridge.log"
