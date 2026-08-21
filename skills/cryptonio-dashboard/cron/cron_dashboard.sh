#!/bin/bash
# Cryptonio Dashboard Cron Launcher
# Run this every 5 minutes to ensure dashboard is running

DASHBOARD_PID=$(pgrep -f "dashboard_server.py" | head -1)

if [ -z "$DASHBOARD_PID" ]; then
    echo "$(date): Dashboard not running, starting..."
    cd /root/.openclaw/workspace/agent_sandboxes/the-great-cryptonio
    source ./run_with_credentials.sh 2>/dev/null
    nohup python3 dashboard_server.py > logs/dashboard_cron.log 2>&1 &
    echo "$(date): Dashboard started with PID $!"
else
    echo "$(date): Dashboard already running (PID: $DASHBOARD_PID)"
fi
