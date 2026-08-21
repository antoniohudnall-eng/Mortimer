#!/bin/bash
# Remove a cron job by name

JOB_NAME="$1"

if [ -z "$JOB_NAME" ]; then
    echo "Usage: remove-cron.sh <job_name>"
    exit 1
fi

if ! crontab -l 2>/dev/null | grep -q "# $JOB_NAME$"; then
    echo "❌ Job '$JOB_NAME' not found"
    exit 1
fi

crontab -l 2>/dev/null | grep -v "# $JOB_NAME$" | crontab -
echo "✅ Removed cron job: $JOB_NAME"
