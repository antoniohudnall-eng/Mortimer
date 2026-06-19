#!/bin/bash
# Activate Patricia and Jordan for Factory & Office Operations

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     🌑 PATRICIA & JORDAN ACTIVATION SEQUENCE                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Make scripts executable
chmod +x /root/.openclaw/workspace/agent_sandboxes/patricia/patricia_factory_controller.py
chmod +x /root/.openclaw/workspace/agent_sandboxes/jordan/jordan_office_controller.py
echo "✅ Scripts made executable"

# Reload systemd
systemctl daemon-reload
echo "✅ Systemd reloaded"

# Enable services
systemctl enable patricia-factory.service jordan-office.service
echo "✅ Services enabled"

# Start Patricia first (she monitors the factory)
echo ""
echo "🌑 Starting Patricia (Factory Controller)..."
systemctl start patricia-factory
echo "✅ Patricia activated"

# Start Jordan second (he manages the office)
echo ""
echo "🔧 Starting Jordan (Office Controller)..."
systemctl start jordan-office
echo "✅ Jordan activated"

# Wait a moment
sleep 2

# Check status
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "STATUS CHECK"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "🌑 PATRICIA (Factory Controller):"
systemctl is-active patricia-factory --quiet && echo "   Status: ✅ RUNNING" || echo "   Status: ❌ STOPPED"
echo "   Role: Six Sigma Quality Control, Defect Detection"
echo "   Monitors: Dark Factory Pipeline, Production Orders"
echo ""

echo "🔧 JORDAN (Office Controller):"
systemctl is-active jordan-office --quiet && echo "   Status: ✅ RUNNING" || echo "   Status: ❌ STOPPED"
echo "   Role: Systems Integration, Diagnostics, GitHub Sync"
echo "   Monitors: Brain, Mission Control, All AGI Systems"
echo ""

# Run initial reports
echo "═══════════════════════════════════════════════════════════════"
echo "INITIALIZING CONTROLLERS..."
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "📊 Patricia analyzing factory..."
python3 /root/.openclaw/workspace/agent_sandboxes/patricia/patricia_factory_controller.py tick 2>/dev/null || echo "   (Service will run on schedule)"
echo ""

echo "🔧 Jordan scanning office..."
python3 /root/.openclaw/workspace/agent_sandboxes/jordan/jordan_office_controller.py tick 2>/dev/null || echo "   (Service will run on schedule)"
echo ""

# Create cron jobs for regular operation
echo "═══════════════════════════════════════════════════════════════"
echo "SETTING UP AUTOMATION..."
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Add to crontab if not already there
(crontab -l 2>/dev/null | grep -q "patricia_factory_controller" || echo "*/5 * * * * /usr/bin/python3 /root/.openclaw/workspace/agent_sandboxes/patricia/patricia_factory_controller.py tick >> /var/log/patricia/factory.log 2>&1") | crontab -
(crontab -l 2>/dev/null | grep -q "jordan_office_controller" || echo "*/10 * * * * /usr/bin/python3 /root/.openclaw/workspace/agent_sandboxes/jordan/jordan_office_controller.py tick >> /var/log/jordan/office.log 2>&1") | crontab -

echo "✅ Patricia: Every 5 minutes (factory monitoring)"
echo "✅ Jordan: Every 10 minutes (office diagnostics)"
echo ""

# Ensure log directories
mkdir -p /var/log/patricia /var/log/jordan
echo "✅ Log directories created"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "ACTIVATION COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "🌑 PATRICIA (Factory)"
echo "   └─ Monitors production quality"
echo "   └─ Detects defects and delays"
echo "   └─ Generates Six Sigma reports"
echo ""
echo "🔧 JORDAN (Office)"
echo "   └─ Manages system integrations"
echo "   └─ Runs diagnostics"
echo "   └─ Syncs to GitHub"
echo ""
echo "Both agents are now running the factory & office!"
echo ""
echo "Commands:"
echo "  systemctl status patricia-factory  # Check Patricia"
echo "  systemctl status jordan-office     # Check Jordan"
echo "  systemctl stop patricia-factory    # Stop Patricia"
echo "  systemctl stop jordan-office       # Stop Jordan"
echo ""
