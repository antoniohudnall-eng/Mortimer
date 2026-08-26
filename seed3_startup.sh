#!/bin/bash
# ╔═══════════════════════════════════════════╗
# ║   SEED3 FLEET STARTUP — Unified v2.0     ║
# ║   Single source of truth for all boots   ║
# ╚═══════════════════════════════════════════╝
#
# Usage:
#   bash seed3_startup.sh             # Normal boot
#   bash seed3_startup.sh --dry-run    # Preview only, don't start anything
#   bash seed3_startup.sh --status     # Check what's running
#
# Changelog:
#   v2.1 (2026-08-25): Added Brain Viz (morty_body.py, :8080) to boot + status + health report.
#   v2.0 (2026-07-24): Merged pi_startup.sh + seed3_startup.sh. Added health checks, idempotency, dry-run.
#   v1.0 (2026-06-18): Original seed3 startup with service launches

set -e

MODE="run"
if [ "$1" = "--dry-run" ]; then MODE="dry"; fi
if [ "$1" = "--status" ]; then MODE="status"; fi

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

HOME_DIR=/data/data/com.termux/files/home
LOG_DIR="$HOME_DIR/mortimer/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/boot-$(date +%Y%m%d-%H%M%S).log"

log() { echo -e "$1" | tee -a "$LOG"; }
dry() { if [ "$MODE" = "dry" ]; then echo -e "  ${CYAN}[DRY]${NC} $1"; return 0; else return 1; fi; }

# ─── Health Check Functions ──────────────────────────
check_http() {
    # check_http <port> <name> [path]
    local port="$1" name="$2" path="${3:-/}"
    if dry "Would check $name on :$port"; then return 0; fi
    local code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "http://127.0.0.1:${port}${path}" 2>/dev/null || echo "000")
    if [ "$code" = "000" ] || [ "$code" = "502" ]; then
        log "  ${RED}✗${NC} $name (:${port}) — no response"
        return 1
    else
        log "  ${GREEN}✓${NC} $name (:${port}) — HTTP $code"
        return 0
    fi
}

check_process() {
    # check_process <pattern> <name>
    local pattern="$1" name="$2"
    if dry "Would check process: $name"; then return 0; fi
    if pgrep -f "$pattern" > /dev/null 2>&1; then
        local pid=$(pgrep -f "$pattern" | head -1)
        log "  ${GREEN}✓${NC} $name (PID $pid)"
        return 0
    else
        log "  ${YELLOW}−${NC} $name — not running"
        return 1
    fi
}

start_if_dead() {
    # start_if_dead <pattern> <name> <start_cmd>
    local pattern="$1" name="$2" cmd="$3"
    
    if pgrep -f "$pattern" > /dev/null 2>&1; then
        if [ "$MODE" != "status" ]; then
            log "  ${GREEN}✓${NC} $name — already running (skipping)"
        fi
        return 0
    fi
    
    if dry "Would start $name: $cmd"; then return 0; fi
    if [ "$MODE" = "status" ]; then
        log "  ${YELLOW}⚠${NC} $name — DOWN"
        return 1
    fi
    
    log "  ${YELLOW}→${NC} $name — starting..."
    eval "$cmd" &
    sleep 1
}

# ─── Status Mode ─────────────────────────────────────
if [ "$MODE" = "status" ]; then
    echo ""
    echo "╔═══════════════════════════════════════════╗"
    echo "║   SEED3 STATUS — $(date '+%H:%M:%S')            ║"
    echo "╚═══════════════════════════════════════════╝"
    echo ""
    
    check_process "pulseaudio" "PulseAudio"
    check_process "ollama serve" "Ollama"
    check_http 8000 "QMD Brain" "/query"
    check_http 8080 "Brain Viz" "/health"
    check_http 7777 "Quantum Oracle"
    check_http 7778 "Prime Helix" 
    check_http 7779 "Riemann Helix"
    check_process "patricia" "Patricia"
    check_process "jordan" "JORDAN"
    check_process "dark-factory\|start-forge" "FORGE"
    
    echo ""
    echo "  Running processes: $(ps aux | grep -E 'python3|ollama|node' | grep -v grep | wc -l)"
    echo ""
    exit 0
fi

# ─── Boot Banner ─────────────────────────────────────
echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║   SEED3 FLEET BOOT v2.0                  ║"
echo "╚═══════════════════════════════════════════╝"
echo ""
log "Boot started: $(date)"
log "Mode: $MODE"
log "Log: $LOG"
log ""

if [ "$MODE" = "dry" ]; then
    log "${CYAN}═══ DRY RUN — No services will be started ═══${NC}"
    log ""
fi

# ─── Step 1: PulseAudio ──────────────────────────────
log "${BLUE}[1/7] PulseAudio${NC}"
start_if_dead "pulseaudio" "PulseAudio" \
    "pulseaudio --start --exit-idle-time=-1 2>/dev/null"
sleep 1
check_process "pulseaudio" "PulseAudio"

# ─── Step 2: Ollama ──────────────────────────────────
log ""
log "${BLUE}[2/7] Ollama${NC}"
if [ "$MODE" != "dry" ]; then
    export OLLAMA_HOST=0.0.0.0:11434
    export OLLAMA_MODEL="${OLLAMA_MODEL:-qwen2.5:1.5b}"
fi
start_if_dead "ollama serve" "Ollama" \
    "nohup ollama serve > $LOG_DIR/ollama.log 2>&1"
sleep 2
check_process "ollama serve" "Ollama"

# ─── Step 3: QMD Brain ───────────────────────────────
log ""
log "${BLUE}[3/7] QMD Brain Service${NC}"
if ! dry; then
    export USE_OLLAMA="true"
fi
start_if_dead "qmd_service" "QMD" \
    "cd $HOME_DIR/mortimer/services && nohup python3 -u qmd_service.py > $LOG_DIR/qmd.log 2>&1"
sleep 2
check_http 8000 "QMD Brain" "/query"

# ─── Step 4: Visualization Services ──────────────────
log ""
log "${BLUE}[4/7] Helix & Oracle Services${NC}"
for svc in quantum_oracle prime_helix riemann_helix; do
    start_if_dead "$svc" "$svc" \
        "cd $HOME_DIR/mortimer/services && nohup python3 -u ${svc}.py > $LOG_DIR/${svc}.log 2>&1"
done
sleep 2
check_http 7777 "Quantum Oracle"
check_http 7778 "Prime Helix"
check_http 7779 "Riemann Helix"

# Brain Viz (morty_body.py) — 3D constellation on :8080
if [ -f "$HOME_DIR/mortimer/brain-viz/start.sh" ]; then
    start_if_dead "brain-viz/server.py" "Brain Viz" \
        "cd $HOME_DIR/mortimer/brain-viz && bash start.sh 2>/dev/null"
    sleep 2
    check_http 8080 "Brain Viz" "/health"
else
    log "  ${YELLOW}⚠${NC} Brain Viz not found — skipping"
fi

# ─── Step 5: Patricia ────────────────────────────────
log ""
log "${BLUE}[5/7] Patricia (Process Excellence)${NC}"
start_if_dead "patricia_service\|patricia_v4" "Patricia" \
    "cd $HOME_DIR/mortimer/patricia && bash start.sh 2>/dev/null || (cd $HOME_DIR/mortimer/patricia && nohup python3 -u patricia_service.py > patricia.log 2>&1)"
sleep 2
check_process "patricia" "Patricia"

# ─── Step 6: JORDAN ──────────────────────────────────
log ""
log "${BLUE}[6/7] JORDAN (Office Controller)${NC}"
if [ -f "$HOME_DIR/agents/jordan/start.sh" ]; then
    start_if_dead "agents/jordan" "JORDAN" \
        "cd $HOME_DIR/agents/jordan && bash start.sh 2>/dev/null"
    sleep 1
    check_process "jordan" "JORDAN"
else
    log "  ${YELLOW}⚠${NC} JORDAN not found — skipping"
fi

# ─── Step 7: FORGE ───────────────────────────────────
log ""
log "${BLUE}[7/7] FORGE (Dark Factory)${NC}"
if [ -f "$HOME_DIR/projects/standalone-dark-factory/start-forge.sh" ]; then
    start_if_dead "dark-factory\|start-forge" "FORGE" \
        "cd $HOME_DIR/projects/standalone-dark-factory && bash start-forge.sh 2>/dev/null"
    sleep 1
    check_process "dark-factory" "FORGE"
else
    log "  ${YELLOW}⚠${NC} FORGE not found — skipping"
fi

# ─── Step 8: Voice Config ────────────────────────────
log ""
log "${BLUE}[8/8] Voice System${NC}"
if dry; then
    log "  ${CYAN}[DRY]${NC} Would configure voice"
else
    export MORTIMER_TTS="termux-tts-speak"
    if [ -f "$HOME_DIR/mortimer/voice/config.sh" ]; then
        source "$HOME_DIR/mortimer/voice/config.sh"
    fi
    MORTIMER_VOICE='-v en-us+m3 -s 161 -p 51 -a 113 -k 4'
    export MORTIMER_VOICE
    log "  ${GREEN}✓${NC} φ-Voice loaded: speed=161, pitch=51"
fi

# ─── Final: Health Check Report ──────────────────────
log ""
log "${BLUE}════════════════════════════════════════════${NC}"
log "${BLUE}  HEALTH CHECK REPORT${NC}"
log "${BLUE}════════════════════════════════════════════${NC}"

HEALTH_OK=0
HEALTH_FAIL=0

check_final() {
    if check_process "$1" "$2" 2>/dev/null; then
        HEALTH_OK=$((HEALTH_OK + 1))
    else
        HEALTH_FAIL=$((HEALTH_FAIL + 1))
    fi
}

check_final "pulseaudio" "PulseAudio"
check_final "ollama serve" "Ollama"
check_final "qmd_service" "QMD"
check_final "quantum_oracle" "Quantum Oracle"
check_final "prime_helix" "Prime Helix"
check_final "riemann_helix" "Riemann Helix"
check_final "brain-viz/server.py" "Brain Viz"
check_final "patricia" "Patricia"

log ""
log "  ${GREEN}Healthy: $HEALTH_OK${NC}  ${RED}Failed: $HEALTH_FAIL${NC}"

# ─── Voice Announcement (only if healthy) ────────────
if [ "$MODE" != "dry" ]; then
    if [ $HEALTH_FAIL -eq 0 ]; then
        log "  ${GREEN}✅ ALL SYSTEMS NOMINAL${NC}"
        if command -v termux-tts-speak &> /dev/null; then
            termux-tts-speak "SEED3 online. All systems nominal. $HEALTH_OK services healthy." 2>/dev/null &
        fi
    elif [ $HEALTH_FAIL -le 2 ]; then
        log "  ${YELLOW}⚠ DEGRADED — $HEALTH_FAIL service(s) down${NC}"
        if command -v termux-tts-speak &> /dev/null; then
            termux-tts-speak "SEED3 online. Warning: $HEALTH_FAIL services not responding." 2>/dev/null &
        fi
    else
        log "  ${RED}🚨 CRITICAL — $HEALTH_FAIL services DOWN${NC}"
        if command -v termux-tts-speak &> /dev/null; then
            termux-tts-speak "SEED3 online but critical: $HEALTH_FAIL services are down." 2>/dev/null &
        fi
    fi
fi

log ""
log "╔═══════════════════════════════════════════╗"
if [ "$MODE" = "dry" ]; then
    log "║   DRY RUN COMPLETE — No changes made     ║"
else
    log "║   SEED3 FLEET ONLINE                     ║"
fi
log "║   $(date)              ║"
log "╚═══════════════════════════════════════════╝"
log ""
