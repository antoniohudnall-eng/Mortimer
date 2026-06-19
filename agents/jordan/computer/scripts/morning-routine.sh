#!/bin/bash
# Jordan's Morning Routine

echo "☀️  Good morning! Running Jordan's morning routine..."

# Check brain status
~/.openclaw/workspace/aocros/agent_sandboxes/jordan/computer/bin/jordan-status > ~/.openclaw/workspace/aocros/agent_sandboxes/jordan/reports/morning-$(date +%Y%m%d).md

# Check for urgent tasks
URGENT=$(grep -i "urgent\|asap\|critical" /root/.openclaw/workspace/aocros/agent_sandboxes/jordan/TASKS.md 2>/dev/null || echo "")
if [ ! -z "$URGENT" ]; then
    echo "⚠️  URGENT tasks detected!"
    echo "$URGENT"
fi

echo "✅ Morning routine complete"
