#!/bin/bash
AGENT="patricia"
AGENT_DIR="$HOME/mortimer/patricia"
SANDBOX="$AGENT_DIR/sandbox"
LOG="$SANDBOX/logs/patricia-$(date +%Y%m%d-%H%M%S).log"
PIDFILE="$SANDBOX/.pid"

mkdir -p "$SANDBOX"/{work,logs,data,tmp}

echo "[$AGENT] Starting service..."
cd "$AGENT_DIR"

# Run the patricia service
nohup /data/data/com.termux/files/usr/bin/python3 -u "$AGENT_DIR/patricia_service.py" >> "$LOG" 2>&1 &
echo $! > "$PIDFILE"

echo "[$AGENT] Started PID $(cat $PIDFILE)"
echo "[$AGENT] Log: $LOG"
