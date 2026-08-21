#!/bin/bash
# List all cron jobs with names

echo "Cron Jobs:"
echo "=========="
crontab -l 2>/dev/null | grep -v '^#' | while read -r line; do
    [ -z "$line" ] && continue
    JOB_NAME=$(echo "$line" | sed 's/.*# //')
    SCHEDULE=$(echo "$line" | sed 's/ #.*//' | awk '{print $1,$2,$3,$4,$5}')
    COMMAND=$(echo "$line" | sed 's/ #.*//' | cut -d' ' -f6-)
    echo ""
    echo "Name: $JOB_NAME"
    echo "Schedule: $SCHEDULE"
    echo "Command: $COMMAND"
done
