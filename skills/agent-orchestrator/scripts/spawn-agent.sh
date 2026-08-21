#!/data/data/com.termux/files/usr/bin/bash
# ╔═══════════════════════════════════════════╗
# ║  AGENT ORCHESTRATOR v2.0                 ║
# ║  Real sub-agent spawning via task queue  ║
# ╚═══════════════════════════════════════════╝
#
# Usage:
#   spawn-agent.sh "task description" agent-label [priority] [timeout]
#   spawn-agent.sh --status                    # List all sub-agents
#   spawn-agent.sh --collect agent-label       # Collect results
#
# Rewired: 2026-07-24 — Bypassed blocked sessions_spawn API,
# now uses Agent Factory task queue with real execution.

QUEUE_DIR="$HOME/agents/tasks/queue"
COMPLETED_DIR="$HOME/agents/tasks/completed"
FAILED_DIR="$HOME/agents/tasks/failed"
ORCHESTRATOR_LOG="$HOME/agents/orchestrator.log"

log() { echo "[$(date +%H:%M:%S)] $1" | tee -a "$ORCHESTRATOR_LOG"; }

# ─── Status: List all agents ────────────────────
if [ "$1" = "--status" ] || [ "$1" = "list" ]; then
    echo "╔═══════════════════════════════════════════╗"
    echo "║   AGENT ORCHESTRATOR — Fleet Status      ║"
    echo "╚═══════════════════════════════════════════╝"
    echo ""
    
    # Running agents (SOUL files = registered agents)
    echo "📋 REGISTERED AGENTS:"
    for agent_dir in "$HOME"/agents/*/; do
        agent=$(basename "$agent_dir")
        if [ -f "$agent_dir/SOUL.md" ]; then
            # Check if agent has a backend
            backend=""
            [ -f "$agent_dir/start.sh" ] && backend="🟢 start.sh"
            [ -f "$agent_dir/cmd.sh" ] && backend="🟢 cmd.sh"
            [ -f "$HOME/mortimer/agents/browser_agent/browser_agent.py" ] && [ "$agent" = "browser-agent" ] && backend="🟢 browser_agent.py"
            
            # Check for pending/completed tasks
            pending=$(ls "$QUEUE_DIR/${agent}_"*.json 2>/dev/null | wc -l)
            completed=$(ls "$COMPLETED_DIR/${agent}_"*.json 2>/dev/null | wc -l)
            
            [ -z "$backend" ] && backend="⚪ SOUL only"
            echo "  $agent — $backend | Pending: $pending | Done: $completed"
        fi
    done
    
    echo ""
    echo "📊 QUEUE: $(ls "$QUEUE_DIR"/*.json 2>/dev/null | wc -l) pending"
    echo "✅ DONE:  $(ls "$COMPLETED_DIR"/*.json 2>/dev/null | wc -l) completed"
    echo "❌ FAIL:  $(ls "$FAILED_DIR"/*.json 2>/dev/null | wc -l) failed"
    echo ""
    exit 0
fi

# ─── Collect results ────────────────────────────
if [ "$1" = "--collect" ] || [ "$1" = "collect" ]; then
    AGENT_FILTER="${2:-}"
    
    echo "📦 COLLECTING RESULTS"
    echo "===================="
    
    if [ -n "$AGENT_FILTER" ]; then
        files=$(ls "$COMPLETED_DIR/${AGENT_FILTER}_"*.json 2>/dev/null)
    else
        files=$(ls "$COMPLETED_DIR"/*.json 2>/dev/null)
    fi
    
    count=0
    for task_file in $files; do
        [ -e "$task_file" ] || continue
        echo ""
        echo "▶️ $(basename $task_file)"
        python3 -c "
import json
with open('$task_file') as f:
    t = json.load(f)
    print(f\"  Agent: {t.get('agent', '?')}\")
    print(f\"  Task:  {t.get('task', '?')}\")
    print(f\"  Prio:  {t.get('priority', '?')}\")
    result = t.get('result', {})
    if result:
        print(f\"  Result: {json.dumps(result)[:200]}\")
"
        count=$((count + 1))
    done
    
    echo ""
    echo "===================="
    echo "📦 Collected $count results"
    exit 0
fi

# ─── Spawn sub-agent ─────────────────────────────
TASK="$1"
LABEL="$2"
PRIORITY="${3:-normal}"
TIMEOUT="${4:-300}"

if [ -z "$TASK" ] || [ -z "$LABEL" ]; then
    echo "Usage: spawn-agent.sh 'task description' agent-label [priority] [timeout]"
    echo "       spawn-agent.sh --status"
    echo "       spawn-agent.sh --collect [agent-label]"
    echo ""
    echo "Examples:"
    echo "  spawn-agent.sh 'Scrape competitor prices' browser-agent high"
    echo "  spawn-agent.sh 'Run security audit' sentinel normal 600"
    echo "  spawn-agent.sh --status"
    echo "  spawn-agent.sh --collect browser-agent"
    exit 1
fi

# Generate task ID
TASK_ID="${LABEL}_$(date +%Y%m%d_%H%M%S)"

log "🚀 SPAWNING: $LABEL — $TASK"

# Create task JSON
cat > "$QUEUE_DIR/${TASK_ID}.json" << JSONEOF
{
  "id": "$TASK_ID",
  "agent": "$LABEL",
  "task": "$TASK",
  "priority": "$PRIORITY",
  "timeout": $TIMEOUT,
  "created": "$(date -u +'%Y-%m-%d %H:%M:%S UTC')",
  "status": "queued",
  "spawned_by": "orchestrator",
  "spec": {
    "task": "$TASK",
    "label": "$LABEL",
    "timeout_seconds": $TIMEOUT
  }
}
JSONEOF

log "  📋 Task ID: $TASK_ID"
log "  📋 Agent: $LABEL"
log "  📋 Priority: $PRIORITY"
log "  📋 Timeout: ${TIMEOUT}s"

# Now execute the task immediately
log "  ⚡ Dispatching..."
bash "$HOME/agents/execute_task.sh" "$LABEL" 2>&1 | while read line; do
    log "    $line"
done

# Check if task completed
if [ -f "$COMPLETED_DIR/${TASK_ID}.json" ]; then
    log "  ✅ SPAWN COMPLETE — $LABEL finished"
    echo ""
    echo "✅ Agent '$LABEL' completed task: $TASK"
    
    # Show result if available
    python3 -c "
import json
with open('$COMPLETED_DIR/${TASK_ID}.json') as f:
    t = json.load(f)
    result = t.get('result', {})
    if result:
        print(f'Result: {json.dumps(result)[:300]}')
" 2>/dev/null
    
elif [ -f "$FAILED_DIR/${TASK_ID}.json" ]; then
    log "  ❌ SPAWN FAILED — check $FAILED_DIR/${TASK_ID}.json"
    echo ""
    echo "❌ Agent '$LABEL' FAILED: $TASK"
    exit 1
else
    log "  ⚠️ SPAWN QUEUED — $LABEL task queued for next executor run"
    echo ""
    echo "📋 Agent '$LABEL' queued: $TASK"
    echo "   Run 'bash ~/agents/execute_task.sh $LABEL' to process"
fi

echo ""
echo "📊 Fleet status: bash spawn-agent.sh --status"
