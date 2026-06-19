#!/bin/bash
# Jordan's Hourly System Check

LOG_FILE="/root/.openclaw/workspace/aocros/agent_sandboxes/jordan/computer/logs/hourly-$(date +%Y%m%d).log"

echo "[$(date)] Hourly check starting..." >> "$LOG_FILE"

# Check if brain is running
if pgrep -f "brain.py" > /dev/null; then
    echo "[$(date)] ✓ Brain running" >> "$LOG_FILE"
else
    echo "[$(date)] ✗ Brain NOT running" >> "$LOG_FILE"
fi

# Check disk space
DISK_USAGE=$(df /root | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    echo "[$(date)] ⚠️  Disk usage high: ${DISK_USAGE}%" >> "$LOG_FILE"
fi

echo "[$(date)] Hourly check complete" >> "$LOG_FILE"
