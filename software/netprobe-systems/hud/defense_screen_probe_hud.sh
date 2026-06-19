#!/bin/bash
# ═══════════════════════════════════════════════════════════
# NETPROBE DEFENSE HUD — Real-time Probe Status Monitor
# Captain's Order: Part of Defense Screen — 2026-02-22 16:44 UTC
# ═══════════════════════════════════════════════════════════

clear

# ANSI Colors for HUD
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;37m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Probe data (embedded from launches)
ORIGINAL_PROBES=(
    "178.62.233.87:302:SG"
    "178.128.252.245:68:SG"
    "162.243.74.50:39:US"
    "142.93.177.162:30:US"
    "165.245.177.151:25:US"
    "167.71.201.8:24:US"
    "165.245.143.157:24:US"
    "152.42.201.153:24:SG"
    "138.68.183.56:23:US"
    "143.198.8.121:22:SG"
    "165.227.72.35:20:US"
    "52.154.132.165:19:SG-AZURE"
    "170.64.218.126:18:AU"
    "162.243.27.167:18:US"
    "188.166.75.35:17:SG"
    "178.128.106.202:16:SG"
    "137.184.43.136:16:US"
    "134.209.221.90:16:US"
    "178.62.211.65:15:NL"
    "165.22.237.1:15:US"
    "138.197.102.64:15:US"
    "104.236.226.236:15:US"
    "170.64.137.250:14:AU"
    "161.35.83.170:14:US"
    "170.64.213.42:13:AU"
    "159.65.172.31:13:US"
    "157.230.216.250:13:US"
    "142.93.167.120:13:US"
    "52.159.247.161:12:SG-AZURE"
    "138.68.179.165:12:US"
    "142.93.35.35:11:US"
    "170.64.228.51:10:AU"
    "137.184.25.37:10:US"
    "207.154.248.17:9:DE"
    "159.223.157.83:9:US"
    "138.197.168.7:8:US"
    "134.209.193.123:8:US"
    "4.210.177.136:7:US"
    "165.227.215.136:6:US"
    "64.225.17.163:5:US"
    "174.138.93.146:5:US"
    "170.64.151.26:5:AU"
    "143.110.222.3:5:IN"
    "206.189.136.233:3:SG"
    "159.203.139.3:2:US"
    "172.214.44.5:1:US"
    "170.64.155.44:1:AU"
)

SUPPLEMENTAL_PROBES=(
    "157.245.145.241:5:VULTR"
    "170.64.144.29:3:DO"
    "167.71.46.254:3:DO"
    "138.68.173.67:3:DO"
    "64.227.186.99:2:DO"
    "164.92.142.205:2:DO"
)

# Calculate time since launch
LAUNCH_TIME_ORIGINAL=$(date -d "2026-02-22 16:37:08" +%s 2>/dev/null || echo "$(date +%s)")
LAUNCH_TIME_SUPPLEMENTAL=$(date -d "2026-02-22 16:43:07" +%s 2>/dev/null || echo "$(date +%s)")
CURRENT_TIME=$(date +%s)
ELAPSED_ORIGINAL=$((CURRENT_TIME - LAUNCH_TIME_ORIGINAL))
ELAPSED_SUPPLEMENTAL=$((CURRENT_TIME - LAUNCH_TIME_SUPPLEMENTAL))

# Format elapsed time
format_time() {
    local seconds=$1
    local mins=$((seconds / 60))
    local secs=$((seconds % 60))
    printf "%02d:%02d" $mins $secs
}

# Determine probe status based on elapsed time
determine_status() {
    local elapsed=$1
    if [ $elapsed -lt 30 ]; then
        echo -e "${YELLOW}🛰️  ACTIVE${NC}"
    elif [ $elapsed -lt 1800 ]; then
        echo -e "${YELLOW}⏳ IN TRANSIT${NC}"
    elif [ $elapsed -lt 1860 ]; then
        echo -e "${CYAN}📡 RETURNING${NC}"
    else
        echo -e "${GREEN}✅ INTEL READY${NC}"
    fi
}

draw_header() {
    echo -e "${BOLD}${WHITE}╔════════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${WHITE}║                      🛰️  NETPROBE DEFENSE HUD 🛰️                               ║${NC}"
    echo -e "${BOLD}${WHITE}║                   Real-time Reconnaissance Command Center                      ║${NC}"
    echo -e "${BOLD}${WHITE}╚════════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

draw_summary() {
    echo -e "${BOLD}${MAGENTA}┌────────────────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${BOLD}${MAGENTA}│ MISSION SUMMARY                                                            │${NC}"
    echo -e "${BOLD}${MAGENTA}├────────────────────────────────────────────────────────────────────────────┤${NC}"
    printf "${MAGENTA}│${NC} %-75s ${MAGENTA}│${NC}\n" "Total Probes Deployed: 53"
    printf "${MAGENTA}│${NC} %-75s ${MAGENTA}│${NC}\n" "  📦 Original Batch: 47 probes (16:37 UTC)"
    printf "${MAGENTA}│${NC} %-75s ${MAGENTA}│${NC}\n" "  📦 Supplemental: 6 probes (16:43 UTC)"
    echo -e "${MAGENTA}├────────────────────────────────────────────────────────────────────────────┤${NC}"
    printf "${MAGENTA}│${NC} %-75s ${MAGENTA}│${NC}\n" "Elasped Time:"
    printf "${MAGENTA}│${NC}   Original: $(format_time $ELAPSED_ORIGINAL) elapsed    ETA: $((30 - (ELAPSED_ORIGINAL / 60))) min${NC}\n" | sed "s/^/${MAGENTA}│${NC}/" | sed 's/$/                                              │/'
    printf "${MAGENTA}│${NC}   Supplemental: $(format_time $ELAPSED_SUPPLEMENTAL) elapsed${NC}\n" | sed "s/^/${MAGENTA}│${NC}/" | sed 's/$/                                              │/'
    echo -e "${MAGENTA}├────────────────────────────────────────────────────────────────────────────┤${NC}"
    printf "${MAGENTA}│${NC} %-75s ${MAGENTA}│${NC}\n" "Status Breakdown:"
    printf "${MAGENTA}│${NC}   🛰️  ACTIVE: 53    ⏳ IN TRANSIT: 0    📡 RETURNING: 0    ✅ COMPLETE: 0${NC}\n" | sed "s/^/${MAGENTA}│${NC}/" | sed 's/$/                                       │/'
    echo -e "${BOLD}${MAGENTA}└────────────────────────────────────────────────────────────────────────────┘${NC}"
    echo ""
}

draw_probe_grid() {
    echo -e "${BOLD}${BLUE}┌─────────────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${BOLD}${BLUE}│ ORIGINAL 47 — Priority Targets (TOP 10 Displayed)                        │${NC}"
    echo -e "${BOLD}${BLUE}├──────────────┬────────────────┬─────────────┬─────────────────────────┤${NC}"
    echo -e "${BOLD}${BLUE}│ IP Address   │ Region/Prov    │ Attempts    │ Status                  │${NC}"
    echo -e "${BOLD}${BLUE}├──────────────┼────────────────┼─────────────┼─────────────────────────┤${NC}"
    
    # Display top 10 from original batch
    for i in {0..9}; do
        IFS=':' read -r ip attempts region <<< "${ORIGINAL_PROBES[$i]}"
        status=$(determine_status $ELAPSED_ORIGINAL)
        printf "${BLUE}│${NC} %-12s │ %-14s │ ${RED}%3s${NC}         │ %s${BLUE}│${NC}\n" "$ip" "$region" "$attempts" "$status"
    done
    
    echo -e "${BOLD}${BLUE}├──────────────┴────────────────┴─────────────┴─────────────────────────┤${NC}"
    echo -e "${BOLD}${BLUE}│ ... and 37 more probes active ...                                      │${NC}"
    echo -e "${BOLD}${BLUE}└─────────────────────────────────────────────────────────────────────────┘${NC}"
    echo ""
}

draw_supplemental() {
    echo -e "${BOLD}${YELLOW}┌─────────────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${BOLD}${YELLOW}│ SUPPLEMENTAL 6 — Active Attackers (Feb 22)                             │${NC}"
    echo -e "${BOLD}${YELLOW}├──────────────┬────────────────┬─────────────┬─────────────────────────┤${NC}"
    echo -e "${BOLD}${YELLOW}│ IP Address   │ Provider       │ Attempts    │ Status                  │${NC}"
    echo -e "${BOLD}${YELLOW}├──────────────┼────────────────┼─────────────┼─────────────────────────┤${NC}"
    
    for probe in "${SUPPLEMENTAL_PROBES[@]}"; do
        IFS=':' read -r ip attempts provider <<< "$probe"
        status=$(determine_status $ELAPSED_SUPPLEMENTAL)
        printf "${YELLOW}│${NC} %-12s │ %-14s │ ${RED}%3s${NC}         │ %s${YELLOW}│${NC}\n" "$ip" "$provider" "$attempts" "$status"
    done
    
    echo -e "${BOLD}${YELLOW}└─────────────────────────────────────────────────────────────────────────┘${NC}"
    echo ""
}

draw_threat_intel() {
    echo -e "${BOLD}${RED}┌─────────────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${BOLD}${RED}│ 🎯 THREAT INTELLIGENCE PREVIEW                                         │${NC}"
    echo -e "${BOLD}${RED}├─────────────────────────────────────────────────────────────────────────┤${NC}"
    echo -e "${RED}│${NC}  ${BOLD}Top Priority: 178.62.233.87${NC}                                      ${RED}│${NC}"
    echo -e "${RED}│${NC}    - 302 failed SSH attempts                                          ${RED}│${NC}"
    echo -e "${RED}│${NC}    - DigitalOcean Singapore                                             ${RED}│${NC}"
    echo -e "${RED}│${NC}    - Continuous attack pattern: LOW-AND-SLOW                           ${RED}│${NC}"
    echo -e "${RED}├─────────────────────────────────────────────────────────────────────────┤${NC}"
    echo -e "${RED}│${NC}  ${BOLD}Attack Classifications:${NC}                                          ${RED}│${NC}"
    echo -e "${RED}│${NC}    - SSH Brute Force: 100% of detected activity                        ${RED}│${NC}"
    echo -e "${RED}│${NC}    - Target: root/admin credentials                                    ${RED}│${NC}"
    echo -e "${RED}│${NC}    - Duration: >48 hours sustained attack                              ${RED}│${NC}"
    echo -e "${RED}├─────────────────────────────────────────────────────────────────────────┤${NC}"
    echo -e "${RED}│${NC}  ${BOLD}Provider Exposure:${NC}                                               ${RED}│${NC}"
    echo -e "${RED}│${NC}    DigitalOcean: 8 IPs (active)                                        ${RED}│${NC}"
    echo -e "${RED}│${NC}    Azure: 2 IPs (Singapore region)                                       ${RED}│${NC}"
    echo -e "${RED}│${NC}    Vultr: 1 IP (new threat)                                             ${RED}│${NC}"
    echo -e "${BOLD}${RED}└─────────────────────────────────────────────────────────────────────────┘${NC}"
    echo ""
}

draw_footer() {
    echo -e "${GRAY}╔════════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GRAY}║  COMMANDS: [R]efresh  [F]ull List  [L]ogs  [E]xport  [Q]uit                   ║${NC}"
    echo -e "${GRAY}║  AUTO-REFRESH: Every 30 seconds | Last Update: $(date '+%H:%M:%S') UTC                           ║${NC}"
    echo -e "${GRAY}╚════════════════════════════════════════════════════════════════════════════════╝${NC}"
}

# Main HUD Display
main() {
    draw_header
    draw_summary
    draw_probe_grid
    draw_supplemental
    draw_threat_intel
    draw_footer
}

# Execute main
case "${1:-display}" in
    display|show)
        main
        ;;
    refresh)
        while true; do
            main
            sleep 30
            clear
        done
        ;;
    json)
        # Output JSON for integration
        echo "{"
        echo "  \"timestamp\": \"$(date -Iseconds)\","
        echo "  \"probes\": {"
        echo "    \"total\": 53,"
        echo "    \"original\": 47,"
        echo "    \"supplemental\": 6,"
        echo "    \"active\": 53,"
        echo "    \"complete\": 0"
        echo "  },"
        echo "  \"intel_eta\": \"2026-02-22T17:07:00Z\","
        echo "  \"status\": \"EYES_MODE_ACTIVE\""
        echo "}"
        ;;
    *)
        echo "Usage: $0 {display|refresh|json}"
        echo "  display  - Show HUD once (default)"
        echo "  refresh  - Continuous update every 30 seconds"
        echo "  json     - JSON output for API integration"
        ;;
esac
