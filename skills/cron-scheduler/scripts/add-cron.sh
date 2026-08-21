#!/bin/bash
# Add a cron job with validation

JOB_NAME="$1"
CRON_EXPR="$2"
COMMAND="$3"

if [ -z "$JOB_NAME" ] || [ -z "$CRON_EXPR" ] || [ -z "$COMMAND" ]; then
    echo "Usage: add-cron.sh <job_name> <'cron_expression'> <command>"
    echo "Example: add-cron.sh 'health-check' '*/5 * * * *' 'check-health.sh'"
    exit 1
fi

# Validate cron expression (basic check)
if ! echo "$CRON_EXPR" | grep -qE '^([0-9*,/-]+ +){4}[0-9*,/-]+$'; then
    echo "❌ Invalid cron expression: $CRON_EXPR"
    exit 1
fi

# Create cron entry
CRON_ENTRY="$CRON_EXPR $COMMAND # $JOB_NAME"

# Check if job already exists
if crontab -l 2>/dev/null | grep -q "# $JOB_NAME$"; then
    echo "⚠️  Job '$JOB_NAME' already exists. Remove it first or use update-cron.sh"
    exit 1
fi

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo "✅ Added cron job: $JOB_NAME"
echo "   Schedule: $CRON_EXPR"
echo "   Command: $COMMAND"
