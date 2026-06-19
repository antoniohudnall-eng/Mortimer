#!/bin/bash
# Jordan's Computer Setup
# Initializes Jordan's workstation with all tools and automation

set -e

JORDAN_DIR="/root/.openclaw/workspace/aocros/agent_sandboxes/jordan"
COMPUTER_DIR="$JORDAN_DIR/computer"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     Setting up Jordan's Computer...                      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Create directory structure
mkdir -p "$COMPUTER_DIR"/{bin,lib,tmp,logs,scripts,downloads}
mkdir -p "$JORDAN_DIR"/{research,drafts,reports,completed}

echo "📁 Directory structure created"

# Create Jordan's command scripts
cat > "$COMPUTER_DIR/bin/jordan-research" << 'EOF'
#!/bin/bash
# jordan-research - Research assistant tool

TOPIC="$1"
if [ -z "$TOPIC" ]; then
    echo "Usage: jordan-research <topic>"
    exit 1
fi

OUTPUT_FILE="/root/.openclaw/workspace/aocros/agent_sandboxes/jordan/research/$(date +%Y-%m-%d)-$(echo $TOPIC | tr ' ' '-').md"

echo "# Research: $TOPIC" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "**Date:** $(date)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "## Summary" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "(Research findings go here)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "## Sources" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "✅ Research file created: $OUTPUT_FILE"
EOF

cat > "$COMPUTER_DIR/bin/jordan-draft-email" << 'EOF'
#!/bin/bash
# jordan-draft-email - Email drafting tool

SUBJECT="$1"
if [ -z "$SUBJECT" ]; then
    echo "Usage: jordan-draft-email <subject>"
    exit 1
fi

OUTPUT_FILE="/root/.openclaw/workspace/aocros/agent_sandboxes/jordan/drafts/email-$(date +%Y%m%d-%H%M).md"

cat > "$OUTPUT_FILE" << EOL
# Email Draft

**To:** 
**Subject:** $SUBJECT
**Date:** $(date)
**Status:** Draft (Pending Miles' Approval)

---

(Draft content here)

---

**Notes for Miles:**
- 

EOL

echo "✅ Email draft created: $OUTPUT_FILE"
EOF

cat > "$COMPUTER_DIR/bin/jordan-status" << 'EOF'
#!/bin/bash
# jordan-status - Check system status

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     Jordan's Computer Status                             ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

echo "📊 Task Queue:"
if [ -f /root/.openclaw/workspace/aocros/agent_sandboxes/jordan/TASKS.md ]; then
    grep "\- \[ \]" /root/.openclaw/workspace/aocros/agent_sandboxes/jordan/TASKS.md | head -5
else
    echo "   No tasks found"
fi

echo ""
echo "🧠 AOS Brain Status:"
if [ -f ~/.aos/brain/state/brain_state.json ]; then
    python3 -c "
import json
with open('/root/.aos/brain/state/brain_state.json') as f:
    d = json.load(f)
    print(f\"   Tick: {d.get('tick', 'N/A')}\")
    print(f\"   Nodes: {d.get('policy_nn', {}).get('total_nodes', 'N/A')}\")
    print(f\"   Memory: {d.get('memory_nn', {}).get('clusters', 'N/A')}\")
" 2>/dev/null || echo "   State file not readable"
else
    echo "   Brain state not found"
fi

echo ""
echo "📁 Recent Activity:"
ls -lt /root/.openclaw/workspace/aocros/agent_sandboxes/jordan/research/ 2>/dev/null | head -3 | awk '{print "   " $9}' || echo "   No recent research"

echo ""
echo "💾 Disk Usage:"
df -h /root | tail -1 | awk '{print "   Used: " $3 " / " $2 " (" $5 ")"}'

echo ""
EOF

cat > "$COMPUTER_DIR/bin/jordan-complete-task" << 'EOF'
#!/bin/bash
# jordan-complete-task - Mark task as complete

TASK="$1"
if [ -z "$TASK" ]; then
    echo "Usage: jordan-complete-task <task-number-or-description>"
    exit 1
fi

TASKS_FILE="/root/.openclaw/workspace/aocros/agent_sandboxes/jordan/TASKS.md"

# Mark task as complete (simple sed replacement)
sed -i "s/- \[ \] $TASK/- [x] $TASK/" "$TASKS_FILE" 2>/dev/null || true

echo "✅ Task marked complete: $TASK"
EOF

# Make all scripts executable
chmod +x "$COMPUTER_DIR/bin/"*

echo "🛠️  Command tools installed:"
ls "$COMPUTER_DIR/bin/" | sed 's/^/   /'

# Create automation scripts
cat > "$COMPUTER_DIR/scripts/morning-routine.sh" << 'EOF'
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
EOF

cat > "$COMPUTER_DIR/scripts/hourly-check.sh" << 'EOF'
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
EOF

chmod +x "$COMPUTER_DIR/scripts/"*.sh

echo "⚙️  Automation scripts installed"

# Create PATH setup
cat > "$COMPUTER_DIR/bin/activate" << EOF
# Add Jordan's tools to PATH
export PATH="$COMPUTER_DIR/bin:\$PATH"
export JORDAN_HOME="/root/.openclaw/workspace/aocros/agent_sandboxes/jordan"
export JORDAN_COMPUTER="$COMPUTER_DIR"

echo "💻 Jordan's Computer activated"
echo "Available commands:"
ls "$COMPUTER_DIR/bin/" | sed 's/^/  /'
EOF

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║     ✅ Jordan's Computer Ready!                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "To activate:"
echo "   source /root/.openclaw/workspace/aocros/agent_sandboxes/jordan/computer/bin/activate"
echo ""
echo "Available commands:"
ls "$COMPUTER_DIR/bin/" | sed 's/^/   /'
echo ""
echo "Automation scripts:"
ls "$COMPUTER_DIR/scripts/" | sed 's/^/   /'
