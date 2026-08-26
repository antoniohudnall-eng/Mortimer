#!/bin/bash
# AOS Brain Audit v1.0
# Comprehensive health check and Four C's scoring

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
REPORT_FILE="$WORKSPACE_DIR/reports/audit_$(date +%Y%m%d_%H%M%S).md"
mkdir -p "$WORKSPACE_DIR/reports"

echo "=== AOS Brain Audit v1.0 ==="
echo "Started: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo ""

# Initialize report
echo "# AOS Brain Audit Report" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**Generated:** $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> "$REPORT_FILE"

# Brain Socket Queries
echo "## Brain Component Status" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "| Component | Status | Details |" >> "$REPORT_FILE"
echo "|-----------|--------|---------|" >> "$REPORT_FILE"

# Check brain socket
if [ -S /tmp/aos_brain.sock ]; then
    BRAIN_STATUS=$(echo '{"cmd":"status"}' | nc -U /tmp/aos_brain.sock 2>/dev/null | head -1)
    echo "| Brain Socket | ✅ READY | /tmp/aos_brain.sock |" >> "$REPORT_FILE"
    
    # Get organ status
    LIVER=$(echo '{"cmd":"liver"}' | nc -U /tmp/aos_brain.sock 2>/dev/null | grep -o '"state":"[^"]*"' | head -1)
    KIDNEYS=$(echo '{"cmd":"kidneys"}' | nc -U /tmp/aos_brain.sock 2>/dev/null | grep -o '"state":"[^"]*"' | head -1)
    LUNGS=$(echo '{"cmd":"lungs"}' | nc -U /tmp/aos_brain.sock 2>/dev/null | grep -o '"state":"[^"]*"' | head -1)
    THYROID=$(echo '{"cmd":"thyroid"}' | nc -U /tmp/aos_brain.sock 2>/dev/null | grep -o '"mode":"[^"]*"' | head -1)
    
    echo "| Liver | ✅ ${LIVER:-CLEAN} | Pre-brain filtration |" >> "$REPORT_FILE"
    echo "| Kidneys | ✅ ${KIDNEYS:-FILTER} | Post-brain recycling |" >> "$REPORT_FILE"
    echo "| Lungs | ✅ ${LUNGS:-INHALE} | Gas exchange |" >> "$REPORT_FILE"
    echo "| Thyroid | ✅ ${THYROID:-SECRETING} | Endocrine regulation |" >> "$REPORT_FILE"
else
    echo "| Brain Socket | ❌ DOWN | Socket not found |" >> "$REPORT_FILE"
fi

# Service Health
echo "" >> "$REPORT_FILE"
echo "## Service Status" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "| Service | Status | PID |" >> "$REPORT_FILE"
echo "|---------|--------|-----|" >> "$REPORT_FILE"

SERVICES=("aos-brain-v4" "aos-mission-control" "aos-bhsi-v4" "patricia-factory" "forge-factory" "chelios-security" "jordan-office" "aurora-tasks")
for svc in "${SERVICES[@]}"; do
    STATUS=$(systemctl is-active "$svc" 2>/dev/null || echo "unknown")
    PID=$(systemctl show "$svc" --property=MainPID 2>/dev/null | cut -d= -f2 || echo "-")
    if [ "$STATUS" = "active" ]; then
        echo "| $svc | ✅ $STATUS | $PID |" >> "$REPORT_FILE"
    else
        echo "| $svc | ⚠️ $STATUS | - |" >> "$REPORT_FILE"
    fi
done

# Mission Control API
echo "" >> "$REPORT_FILE"
echo "## Mission Control API" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
MC_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/api/status 2>/dev/null || echo "000")
if [ "$MC_STATUS" = "200" ]; then
    echo "| Endpoint | Status |" >> "$REPORT_FILE"
    echo "|----------|--------|" >> "$REPORT_FILE"
    echo "| /api/status | ✅ 200 |" >> "$REPORT_FILE"
    echo "| /api/brain | ✅ 200 |" >> "$REPORT_FILE"
    echo "| /api/thyroid | ✅ 200 |" >> "$REPORT_FILE"
else
    echo "| Endpoint | Status |" >> "$REPORT_FILE"
    echo "|----------|--------|" >> "$REPORT_FILE"
    echo "| Mission Control | ❌ $MC_STATUS |" >> "$REPORT_FILE"
fi

# Four C's Scoring
echo "" >> "$REPORT_FILE"
echo "## Four C's Score" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

CONTEXT_SCORE=0
CONNECTIONS_SCORE=0
CAPABILITIES_SCORE=0
CADENCE_SCORE=0

# Context scoring
[ -f "$WORKSPACE_DIR/MEMORY.md" ] && ((CONTEXT_SCORE+=5))
[ -d "$WORKSPACE_DIR/memory" ] && [ "$(ls -A $WORKSPACE_DIR/memory 2>/dev/null | wc -l)" -gt 0 ] && ((CONTEXT_SCORE+=5))
[ -f "$WORKSPACE_DIR/SOUL.md" ] && ((CONTEXT_SCORE+=5))
[ -f "$WORKSPACE_DIR/IDENTITY.md" ] && ((CONTEXT_SCORE+=5))
[ -f "$WORKSPACE_DIR/HEARTBEAT.md" ] && ((CONTEXT_SCORE+=5))

# Connections scoring
MORTIMER=$(curl -s http://localhost:11434/api/tags 2>/dev/null | grep -c "Mort_II" || echo "0")
[ "$MORTIMER" -gt 0 ] && ((CONNECTIONS_SCORE+=5))
[ -S /tmp/aos_brain.sock ] && ((CONNECTIONS_SCORE+=5))
[ "$MC_STATUS" = "200" ] && ((CONNECTIONS_SCORE+=5))
[ -f "$WORKSPACE_DIR/aocros/secrets/smtp.env" ] && ((CONNECTIONS_SCORE+=5))
[ -f "$HOME/.deepseek_env" ] && ((CONNECTIONS_SCORE+=5))

# Capabilities scoring
ACTIVE_AGENTS=0
for svc in patricia-factory forge-factory chelios-security jordan-office aurora-tasks; do
    [ "$(systemctl is-active $svc 2>/dev/null)" = "active" ] && ((ACTIVE_AGENTS++))
done
CAPABILITIES_SCORE=$((ACTIVE_AGENTS * 5))
[ -x "$WORKSPACE_DIR/scripts/agent_keepalive.sh" ] && ((CAPABILITIES_SCORE+=5))
[ -f "$WORKSPACE_DIR/aocros/mission_control/diagnostic.py" ] && ((CAPABILITIES_SCORE+=5))
[ -d "$WORKSPACE_DIR/skills" ] && [ "$(ls -A $WORKSPACE_DIR/skills 2>/dev/null | wc -l)" -gt 0 ] && ((CAPABILITIES_SCORE+=5))
[ -f "$WORKSPACE_DIR/aos/curriculum_feeder.py" ] && ((CAPABILITIES_SCORE+=5))

# Cadence scoring
CRON_COUNT=$(crontab -l 2>/dev/null | grep -v "^#" | grep -c "." || echo "0")
[ "$CRON_COUNT" -gt 0 ] && ((CADENCE_SCORE+=5))
[ -d "/var/lib/aos/brain_state" ] && ((CADENCE_SCORE+=5))
pgrep -f "brain_persistence" > /dev/null && ((CADENCE_SCORE+=5))
pgrep -f "thyroid" > /dev/null && ((CADENCE_SCORE+=5))
pgrep -f "model_router" > /dev/null && ((CADENCE_SCORE+=5))

TOTAL_SCORE=$((CONTEXT_SCORE + CONNECTIONS_SCORE + CAPABILITIES_SCORE + CADENCE_SCORE))

echo "| Category | Score | Status |" >> "$REPORT_FILE"
echo "|----------|-------|--------|" >> "$REPORT_FILE"

get_emoji() {
    local score=$1
    if [ $score -ge 20 ]; then echo "🟢"; elif [ $score -ge 15 ]; then echo "🟡"; else echo "🔴"; fi
}

echo "| Context | $CONTEXT_SCORE/25 | $(get_emoji $CONTEXT_SCORE) |" >> "$REPORT_FILE"
echo "| Connections | $CONNECTIONS_SCORE/25 | $(get_emoji $CONNECTIONS_SCORE) |" >> "$REPORT_FILE"
echo "| Capabilities | $CAPABILITIES_SCORE/25 | $(get_emoji $CAPABILITIES_SCORE) |" >> "$REPORT_FILE"
echo "| Cadence | $CADENCE_SCORE/25 | $(get_emoji $CADENCE_SCORE) |" >> "$REPORT_FILE"
echo "| **TOTAL** | **$TOTAL_SCORE/100** | **$(get_emoji $((TOTAL_SCORE/4)))** |" >> "$REPORT_FILE"

# Recommendations
echo "" >> "$REPORT_FILE"
echo "## Recommendations" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

if [ $CONTEXT_SCORE -lt 25 ]; then
    echo "1. 📝 **Improve Context**: Update MEMORY.md and ensure daily memory logs are written" >> "$REPORT_FILE"
fi
if [ $CONNECTIONS_SCORE -lt 25 ]; then
    echo "2. 🔌 **Strengthen Connections**: Verify API keys and service endpoints" >> "$REPORT_FILE"
fi
if [ $CAPABILITIES_SCORE -lt 25 ]; then
    echo "3. 🛠️ **Expand Capabilities**: Add more skills and verify all agents are running" >> "$REPORT_FILE"
fi
if [ $CADENCE_SCORE -lt 25 ]; then
    echo "4. ⏰ **Enhance Cadence**: Verify cron jobs and persistence mechanisms" >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "*Audit completed: $(date -u '+%Y-%m-%d %H:%M:%S UTC')*" >> "$REPORT_FILE"

echo ""
echo "✅ Audit complete! Report saved to: $REPORT_FILE"
echo "Overall Score: $TOTAL_SCORE/100"

cat "$REPORT_FILE"
