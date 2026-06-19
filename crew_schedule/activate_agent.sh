#!/bin/bash
# ACTIVATE AGENT - Send work assignment to agent
AGENT=$1
MODE=$2
MESSAGE=$3

LOG_DIR=~/mortimer/crew_schedule/logs
mkdir -p $LOG_DIR

TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
LOG_FILE="$LOG_DIR/${AGENT}_activity.log"

# Log the activation
echo "[$TIMESTAMP] $MODE: $MESSAGE" >> $LOG_FILE

# Send message to agent (via Telegram or direct)
case $AGENT in
    miles)
        # Send to Miles
        echo "[$TIMESTAMP] Activating Miles: $MESSAGE" | tee -a ~/memory/2026-06-19.md
        ;;
    dusty)
        # Trigger Dusty crypto check
        ~/mortimer/agents/dusty/check_markets.sh
        ;;
    sentinel)
        # Trigger security report
        ~/mortimer/agents/sentinel/security_report.sh
        ;;
    pulp|jane)
        # Sales team notification
        echo "[$TIMESTAMP] Sales alert to $AGENT" >> ~/mortimer/sales/reminder.log
        ;;
    *)
        echo "[$TIMESTAMP] $AGENT ($MODE): $MESSAGE" 
        ;;
esac

echo "✅ $AGENT activated: $MESSAGE"
