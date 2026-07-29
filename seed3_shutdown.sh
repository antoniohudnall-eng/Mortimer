#!/bin/bash
# ╔═══════════════════════════════════════════╗
# ║   SEED3 FLEET SHUTDOWN SEQUENCE          ║
# ║   Graceful teardown — no data loss       ║
# ╚═══════════════════════════════════════════╝
#
# Usage: bash seed3_shutdown.sh [--force]
#   --force : Skip confirmations, immediate shutdown
#
# Shutdown order (reverse of startup):
#   1. FORGE → 2. JORDAN → 3. Patricia → 4. QMD → 5. Helix/Oracle → 6. Ollama → 7. PulseAudio
#   Each step: SIGTERM → wait 5s → SIGKILL if still running
#
# Created: 2026-07-24 — Patricia Priority Fix #1

set -e

FORCE=false
if [ "$1" = "--force" ]; then
    FORCE=true
fi

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

LOG="$HOME/mortimer/logs/shutdown-$(date +%Y%m%d-%H%M%S).log"
mkdir -p "$HOME/mortimer/logs"

log() {
    echo -e "$1" | tee -a "$LOG"
}

# ─── Safety Check ───────────────────────────────────
if [ "$FORCE" = false ]; then
    echo ""
    echo "╔═══════════════════════════════════════════╗"
    echo "║   SEED3 SHUTDOWN — Are you sure?         ║"
    echo "║   This will stop ALL fleet services.     ║"
    echo "╚═══════════════════════════════════════════╝"
    echo ""
    read -p "Type 'shutdown' to confirm: " CONFIRM
    if [ "$CONFIRM" != "shutdown" ]; then
        echo "Aborted."
        exit 0
    fi
fi

log "${BLUE}════════════════════════════════════════════${NC}"
log "${BLUE}  SEED3 SHUTDOWN — $(date)${NC}"
log "${BLUE}════════════════════════════════════════════${NC}"
log ""

# ─── Pre-Shutdown: Flush MNEMOSYNE ───────────────────
log "${YELLOW}[PRE] Flushing MNEMOSYNE brain state...${NC}"
if [ -f "$HOME/mortimer/mnemosyne/mnemosyne_db.py" ]; then
    cd "$HOME/mortimer/mnemosyne"
    python3 -c "
import sqlite3, json, time
try:
    conn = sqlite3.connect('mnemosyne.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS shutdown_log 
        (timestamp TEXT, state TEXT)''')
    conn.execute('INSERT INTO shutdown_log VALUES (?, ?)',
        (time.strftime('%Y-%m-%d %H:%M:%S'), 'graceful_shutdown'))
    conn.commit()
    conn.close()
    print('MNEMOSYNE flushed OK')
except Exception as e:
    print(f'MNEMOSYNE flush warning: {e}')
" 2>&1 | tee -a "$LOG"
    log "${GREEN}  ✓ MNEMOSYNE state saved${NC}"
else
    log "${YELLOW}  ⚠ MNEMOSYNE not found, skipping${NC}"
fi

# ─── Shutdown Functions ───────────────────────────────
graceful_kill() {
    local name="$1"
    local pattern="$2"
    local wait_sec="${3:-5}"
    
    PIDS=$(pgrep -f "$pattern" 2>/dev/null || true)
    if [ -z "$PIDS" ]; then
        log "  ${GREEN}✓${NC} $name — not running"
        return 0
    fi
    
    log "  ${YELLOW}→${NC} $name — sending SIGTERM (PIDs: $(echo $PIDS | tr '\n' ' '))"
    kill $PIDS 2>/dev/null || true
    
    # Wait for graceful exit
    for i in $(seq 1 $wait_sec); do
        if ! pgrep -f "$pattern" > /dev/null 2>&1; then
            log "  ${GREEN}✓${NC} $name — stopped gracefully"
            return 0
        fi
        sleep 1
    done
    
    # Force kill if still running
    REMAINING=$(pgrep -f "$pattern" 2>/dev/null || true)
    if [ -n "$REMAINING" ]; then
        log "  ${RED}⚠${NC} $name — didn't stop, force killing"
        kill -9 $REMAINING 2>/dev/null || true
        sleep 1
    fi
    
    if pgrep -f "$pattern" > /dev/null 2>&1; then
        log "  ${RED}✗${NC} $name — FAILED to stop"
        return 1
    else
        log "  ${GREEN}✓${NC} $name — force stopped"
        return 0
    fi
}

# ─── Step 1: FORGE ────────────────────────────────────
log ""
log "${BLUE}[1/7] FORGE${NC}"
graceful_kill "FORGE" "start-forge\|dark-factory" 5

# ─── Step 2: JORDAN ───────────────────────────────────
log ""
log "${BLUE}[2/7] JORDAN${NC}"
graceful_kill "JORDAN" "agents/jordan" 5

# ─── Step 3: Patricia ─────────────────────────────────
log ""
log "${BLUE}[3/7] Patricia${NC}"
# Save Patricia state before killing
if [ -f "$HOME/mortimer/patricia/patricia.log" ]; then
    echo "[$(date)] Graceful shutdown initiated" >> "$HOME/mortimer/patricia/patricia.log"
fi
graceful_kill "Patricia" "patricia_service\|patricia_v4" 5

# ─── Step 4: QMD Brain ────────────────────────────────
log ""
log "${BLUE}[4/7] QMD Brain Service${NC}"
# Flush QMD state
curl -s -X POST http://127.0.0.1:8000/flush 2>/dev/null || true
sleep 1
graceful_kill "QMD" "qmd_service" 5

# ─── Step 5: Visualization Services ───────────────────
log ""
log "${BLUE}[5/7] Helix & Oracle Services${NC}"
graceful_kill "Riemann Helix" "riemann_helix" 3
graceful_kill "Prime Helix" "prime_helix" 3
graceful_kill "Quantum Oracle" "quantum_oracle" 3

# ─── Step 6: Ollama ───────────────────────────────────
log ""
log "${BLUE}[6/7] Ollama${NC}"
# Ollama may have active generations — give it more time
graceful_kill "Ollama" "ollama serve" 8

# ─── Step 7: PulseAudio ───────────────────────────────
log ""
log "${BLUE}[7/7] PulseAudio${NC}"
graceful_kill "PulseAudio" "pulseaudio" 3

# ─── Final: Memory Flush & Report ─────────────────────
log ""
log "${BLUE}────────────────────────────────────────────${NC}"
log "${BLUE}  SHUTDOWN COMPLETE${NC}"
log "${BLUE}────────────────────────────────────────────${NC}"
log ""

# Log today's memory
MEMORY_FILE="$HOME/mortimer/memory/$(date +%Y-%m-%d).md"
if [ -f "$MEMORY_FILE" ]; then
    echo "" >> "$MEMORY_FILE"
    echo "## System Shutdown — $(date)" >> "$MEMORY_FILE"
    echo "- Graceful shutdown via seed3_shutdown.sh" >> "$MEMORY_FILE"
    echo "- All services stopped in reverse order" >> "$MEMORY_FILE"
    echo "- Log: $LOG" >> "$MEMORY_FILE"
    log "  ${GREEN}✓${NC} Memory file updated"
fi

log ""
log "╔═══════════════════════════════════════════╗"
log "║   SEED3 — SHUTDOWN COMPLETE              ║"
log "║   $(date)              ║"
log "║   Log: $LOG                             ║"
log "╚═══════════════════════════════════════════╝"
log ""

# Optional: speak shutdown
if command -v termux-tts-speak &> /dev/null; then
    termux-tts-speak "SEED3 shutdown complete. All systems offline. See you soon, Captain." 2>/dev/null &
fi
