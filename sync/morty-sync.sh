#!/bin/bash
# morty-sync.sh - Sync Mortimer with VPS fleet
# Usage: ./morty-sync.sh [miles|mortimer|all]
# =============================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

LOG_FILE="$HOME/mortimer/sync/sync.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo -e "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

# VPS definitions
MILES_HOST="root@psdepot.com"
MILES_IP="31.97.6.40"
MORTIMER_HOST="root@31.97.6.30"

# ============================================
# HEALTH CHECKS
# ============================================

check_miles() {
    log "${BLUE}Checking Miles (psdepot.com)...${NC}"
    if ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no "$MILES_HOST" "echo OK" > /dev/null 2>&1; then
        TICK=$(ssh -o ConnectTimeout=5 "$MILES_HOST" "curl -s localhost:8080/api/status 2>/dev/null | grep -o '\"tick\":[^,]*' | cut -d: -f2" || echo "unknown")
        log "${GREEN}✓ Miles ONLINE${NC} - Brain Tick: $TICK"
        return 0
    else
        log "${RED}✗ Miles OFFLINE${NC}"
        return 1
    fi
}

check_mortimer() {
    log "${BLUE}Checking Mortimer Cloud (amhudsupply.com)...${NC}"
    if ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no "$MORTIMER_HOST" "echo OK" > /dev/null 2>&1; then
        TICK=$(ssh -o ConnectTimeout=5 "$MORTIMER_HOST" "curl -s localhost:5001/status 2>/dev/null | grep -o '\"tick_count\":[^}]*' | cut -d: -f2" || echo "unknown")
        log "${GREEN}✓ Mortimer Cloud ONLINE${NC} - Brain Tick: $TICK"
        return 0
    else
        log "${RED}✗ Mortimer Cloud OFFLINE${NC}"
        return 1
    fi
}

# ============================================
# FETCH BRAIN STATUS
# ============================================

fetch_miles_brain() {
    log "${BLUE}Fetching Miles brain status...${NC}"
    ssh -o ConnectTimeout=5 "$MILES_HOST" "curl -s localhost:8080/api/status" 2>/dev/null
}

fetch_mortimer_brain() {
    log "${BLUE}Fetching Mortimer Cloud brain status...${NC}"
    ssh -o ConnectTimeout=5 "$MORTIMER_HOST" "curl -s localhost:5001/status" 2>/dev/null
}

# ============================================
# SYNC BRAIN STATE
# ============================================

sync_brain_to_mortimer() {
    log "${BLUE}Syncing Miles brain state to Mortimer Cloud...${NC}"
    
    # Get Miles brain state
    MILES_STATE=$(fetch_miles_brain)
    
    if [ -z "$MILES_STATE" ]; then
        log "${RED}✗ Failed to fetch Miles brain state${NC}"
        return 1
    fi
    
    # Save to sync directory
    echo "$MILES_STATE" > "$HOME/mortimer/sync/miles_brain_$(date +%s).json"
    
    # Push to Mortimer Cloud
    ssh -o ConnectTimeout=5 "$MORTIMER_HOST" "
        mkdir -p /root/mortimer/sync/incoming
        echo '$MILES_STATE' | python3 -c '
import json, sys
data = json.load(sys.stdin)
with open(\"/root/mortimer/sync/incoming/miles_state.json\", \"w\") as f:
    json.dump(data, f, indent=2)
print(\"Saved Miles brain state\")
'
    "
    
    log "${GREEN}✓ Brain state synced to Mortimer Cloud${NC}"
}

# ============================================
# SYNC MEMORIES
# ============================================

sync_memories() {
    log "${BLUE}Syncing memories between VPSs...${NC}"
    
    # This would sync memory files
    # For now, just confirm connection
    log "${YELLOW}Memory sync: Not yet implemented${NC}"
}

# ============================================
# SYNC AGENTS
# ============================================

sync_agents() {
    log "${BLUE}Syncing agent roster...${NC}"
    
    # Get agent lists from both VPSs
    MILES_AGENTS=$(ssh -o ConnectTimeout=5 "$MILES_HOST" "ls -la /root/.openclaw/workspace/agent_sandboxes/ 2>/dev/null | grep '^d' | awk '{print \$NF}' | head -20" || echo "unavailable")
    MORTIMER_AGENTS=$(ssh -o ConnectTimeout=5 "$MORTIMER_HOST" "ls -la /root/.openclaw/workspace/agent_sandboxes/ 2>/dev/null | grep '^d' | awk '{print \$NF}' | head -20" || echo "unavailable")
    
    echo "=== Miles Agents ===" > "$HOME/mortimer/sync/agents_report.txt"
    echo "$MILES_AGENTS" >> "$HOME/mortimer/sync/agents_report.txt"
    echo "" >> "$HOME/mortimer/sync/agents_report.txt"
    echo "=== Mortimer Cloud Agents ===" >> "$HOME/mortimer/sync/agents_report.txt"
    echo "$MORTIMER_AGENTS" >> "$HOME/mortimer/sync/agents_report.txt"
    
    log "${GREEN}✓ Agent roster saved${NC}"
    cat "$HOME/mortimer/sync/agents_report.txt"
}

# ============================================
# FULL SYNC REPORT
# ============================================

full_report() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              MORTY SYNC REPORT - $TIMESTAMP            ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Check both VPSs
    check_miles
    check_mortimer
    
    echo ""
    echo "──────────────────────────────────────────────────────────────"
    echo "MILESTM BRAIN (psdepot.com)"
    echo "──────────────────────────────────────────────────────────────"
    MILES_STATUS=$(ssh -o ConnectTimeout=5 "$MILES_HOST" "curl -s localhost:8080/api/status" 2>/dev/null)
    if [ -n "$MILES_STATUS" ]; then
        echo "$MILES_STATUS" | python3 -c "
import json, sys
data = json.load(sys.stdin)
b = data.get('brain', {})
k = b.get('kidneys', {})
c = b.get('consciousness', {})
print(f\"  Version:    {b.get('version', 'N/A')}\")
print(f\"  Tick:       {b.get('tick', 'N/A'):,}\")
print(f\"  Phase:      {b.get('phase', 'N/A')}\")
print(f\"  Signal:     {b.get('signal_quality_20avg', 'N/A'):.3f}\")
print()
print(f\"  Kidneys:    {k.get('total_processed', 'N/A'):,} processed\")
print(f\"  Noise:      {k.get('noise_estimate', 'N/A'):.4f}\")
print(f\"  Unique:     {k.get('unique_patterns_seen', 'N/A'):,}\")
print()
print(f\"  Conscious:  {c.get('conscious', {}).get('active_items', 'N/A')}/{c.get('conscious', {}).get('capacity', 'N/A')}\")
print(f\"  Subcon:     {c.get('subconscious', {}).get('active_items', 'N/A')}/{c.get('subconscious', {}).get('capacity', 'N/A')}\")
print(f\"  Uncon:      {c.get('unconscious', {}).get('active_items', 'N/A')}/{c.get('unconscious', {}).get('capacity', 'N/A')}\")
" 2>/dev/null || echo "  Failed to parse Miles brain data"
    else
        echo "  ✗ Could not fetch Miles brain status"
    fi
    
    echo ""
    echo "──────────────────────────────────────────────────────────────"
    echo "MORTIMER CLOUD (amhudsupply.com)"
    echo "──────────────────────────────────────────────────────────────"
    MORTIMER_STATUS=$(ssh -o ConnectTimeout=5 "$MORTIMER_HOST" "curl -s localhost:5001/status" 2>/dev/null)
    if [ -n "$MORTIMER_STATUS" ]; then
        echo "$MORTIMER_STATUS" | python3 -c "
import json, sys
data = json.load(sys.stdin)
b = data.get('brain', {})
c = b.get('consciousness', {})
print(f\"  Mode:       {b.get('mode', 'N/A')}\")
print(f\"  Tick:       {b.get('tick_count', 'N/A')}\")
print(f\"  Lexicon:    {b.get('lexicon', 'N/A')}\")
print()
m = b.get('memory', {})
lt = m.get('long_term', {})
print(f\"  Long-term:  {lt.get('nodes', 'N/A')} nodes, {lt.get('edges', 'N/A')} edges\")
print(f\"  Mid-term:   {m.get('mid_term', 'N/A')}\")
print(f\"  Short-term: {m.get('short_term', 'N/A')}\")
" 2>/dev/null || echo "  Failed to parse Mortimer brain data"
    else
        echo "  ✗ Could not fetch Mortimer brain status"
    fi
    
    echo ""
    echo "──────────────────────────────────────────────────────────────"
    echo "SERVICES STATUS"
    echo "──────────────────────────────────────────────────────────────"
    
    echo ""
    echo "Miles Services:"
    ssh -o ConnectTimeout=5 "$MILES_HOST" "ss -tlnp | grep -E '8080|3000|8000' | awk '{print \"  \"\$4\" -> \"\$6}'" 2>/dev/null || echo "  Could not fetch"
    
    echo ""
    echo "Mortimer Services:"
    ssh -o ConnectTimeout=5 "$MORTIMER_HOST" "ss -tlnp | grep -E '5001|12789|8000' | awk '{print \"  \"\$4\" -> \"\$6}'" 2>/dev/null || echo "  Could not fetch"
    
    echo ""
    echo "╚══════════════════════════════════════════════════════════════╝"
}

# ============================================
# FIX WASTE REPORTS
# ============================================

fix_waste_reports() {
    log "${BLUE}Fixing waste report mechanism...${NC}"
    
    # Check if Miles API is accessible from Morty's perspective
    echo "Checking Miles API reachability..."
    
    # Try direct localhost first
    LOCAL_CHECK=$(curl -s --max-time 3 localhost:8080/api/status 2>/dev/null)
    if [ -n "$LOCAL_CHECK" ]; then
        log "${GREEN}✓ Miles API accessible via localhost:8080${NC}"
    else
        # Try remote
        REMOTE_CHECK=$(curl -s --max-time 5 http://psdepot.com:8080/api/status 2>/dev/null)
        if [ -n "$REMOTE_CHECK" ]; then
            log "${GREEN}✓ Miles API accessible via psdepot.com:8080${NC}"
        else
            log "${RED}✗ Miles API not accessible externally${NC}"
            log "${YELLOW}  Recommendation: Use internal SSH tunnel or have Miles push reports${NC}"
        fi
    fi
}

# ============================================
# MAIN
# ============================================

case "${1:-all}" in
    miles)
        check_miles
        fetch_miles_brain
        ;;
    mortimer)
        check_mortimer
        fetch_mortimer_brain
        ;;
    all)
        full_report
        ;;
    sync)
        check_miles && check_mortimer
        sync_brain_to_mortimer
        ;;
    agents)
        sync_agents
        ;;
    fix)
        fix_waste_reports
        ;;
    help|--help|-h)
        echo "morty-sync.sh - Sync Mortimer with VPS fleet"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  miles      - Check Miles status"
        echo "  mortimer   - Check Mortimer Cloud status"
        echo "  all        - Full sync report (default)"
        echo "  sync       - Sync brain state to Mortimer Cloud"
        echo "  agents     - Sync agent rosters"
        echo "  fix        - Fix waste report mechanism"
        echo "  help       - Show this help"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Run '$0 help' for usage"
        exit 1
        ;;
esac
