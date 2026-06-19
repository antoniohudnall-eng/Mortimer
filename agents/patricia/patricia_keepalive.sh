#!/bin/bash
# PATRICIA KEEPALIVE SYSTEM
# Keeps Patricia running until all jobs in her queue are complete

SCRIPT_DIR="/root/.openclaw/workspace/agent_sandboxes/patricia"
LOG_FILE="/var/log/patricia/keepalive.log"
PIDFILE="/var/run/patricia-keepalive.pid"

# Ensure log directory exists
mkdir -p /var/log/patricia

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_queue_complete() {
    # Query Patricia's database for incomplete items
    python3 -c "
import sqlite3
conn = sqlite3.connect('/root/.openclaw/workspace/data/factory/dark_factory.db')
c = conn.cursor()
c.execute(\"SELECT COUNT(*) FROM production_orders WHERE status NOT IN ('completed', 'delivered')\")
count = c.fetchone()[0]
conn.close()
print(count)
" 2>/dev/null
}

run_patricia_tick() {
    log "🌑 Running Patricia factory tick..."
    python3 "$SCRIPT_DIR/patricia_factory_controller.py" tick >> "$LOG_FILE" 2>&1
}

run_patricia_analysis() {
    log "📊 Running Patricia analysis..."
    python3 "$SCRIPT_DIR/patricia_factory_controller.py" report >> "$LOG_FILE" 2>&1
}

advance_orders() {
    # Auto-advance orders that have been stuck
    python3 -c "
import sqlite3
import json
from datetime import datetime, timedelta

conn = sqlite3.connect('/root/.openclaw/workspace/data/factory/dark_factory.db')
c = conn.cursor()

# Find stalled orders (over 2 hours in same stage)
c.execute(\"\"
    SELECT id, status, stage FROM production_orders
    WHERE status NOT IN ('completed', 'delivered', 'queued')
    AND datetime(last_updated) < datetime('now', '-2 hours')
    ORDER BY priority DESC, created_at ASC
    LIMIT 1
\"\")

stalled = c.fetchone()
if stalled:
    order_id, status, stage = stalled
    new_stage = stage + 1
    stages = ['queued', 'design', 'vendor_sourcing', 'procurement', 'production', 
              'assembly', 'qc', 'packaging', 'shipping_prep', 'distribution', 'delivered']
    new_status = stages[min(new_stage, len(stages)-1)]
    
    completed_at = None
    if new_stage >= len(stages) - 1:
        new_status = 'completed'
        completed_at = datetime.now().isoformat()
        print(f'✅ Order {order_id} COMPLETED')
    
    c.execute(\"\"\"
        UPDATE production_orders 
        SET stage = ?, status = ?, completed_at = COALESCE(?, completed_at), 
            last_updated = ?
        WHERE id = ?
    \"\"\", (new_stage, new_status, completed_at, datetime.now().isoformat(), order_id))
    
    conn.commit()
    print(f'⏩ Advanced {order_id} to {new_status}')
else:
    # Check for queued orders to start
    c.execute(\"\"\"
        SELECT id FROM production_orders
        WHERE status = 'queued'
        ORDER BY priority DESC, created_at ASC
        LIMIT 1
    \"\"\")
    
    queued = c.fetchone()
    if queued:
        order_id = queued[0]
        c.execute(\"\"\"
            UPDATE production_orders 
            SET status = 'in_progress', stage = 1, started_at = ?, last_updated = ?
            WHERE id = ?
        \"\"\", (datetime.now().isoformat(), datetime.now().isoformat(), order_id))
        conn.commit()
        print(f'🚀 Started {order_id}')

conn.close()
" 2>/dev/null
}

sync_to_github() {
    log "☁️ Syncing Patricia updates to GitHub..."
    cd /root/.openclaw/workspace
    git add -A >> "$LOG_FILE" 2>&1
    git commit -m "Patricia keepalive: Queue updates $(date +%Y-%m-%d_%H:%M)" >> "$LOG_FILE" 2>&1 || true
    git push origin master >> "$LOG_FILE" 2>&1 || true
}

main_loop() {
    log "🌑 PATRICIA KEEPALIVE STARTED"
    log "   Monitoring queue until all jobs complete..."
    
    # Save PID
    echo $$ > "$PIDFILE"
    
    while true; do
        # Check queue status
        incomplete=$(check_queue_complete)
        
        if [ "$incomplete" -eq 0 ]; then
            log "✅ ALL QUEUE ITEMS COMPLETE! Patricia signing off."
            rm -f "$PIDFILE"
            exit 0
        fi
        
        log "📋 Queue status: $incomplete items remaining"
        
        # Run Patricia operations
        run_patricia_tick
        advance_orders
        
        # Every 6th tick (30 min), run full analysis and sync
        TICK_COUNT=$(cat /tmp/patricia_tick_count 2>/dev/null || echo "0")
        TICK_COUNT=$((TICK_COUNT + 1))
        echo "$TICK_COUNT" > /tmp/patricia_tick_count
        
        if [ $((TICK_COUNT % 6)) -eq 0 ]; then
            run_patricia_analysis
            sync_to_github
        fi
        
        log "⏱️  Sleeping 5 minutes..."
        sleep 300
    done
}

# Handle command
case "${1:-run}" in
    start)
        if [ -f "$PIDFILE" ] && kill -0 $(cat "$PIDFILE") 2>/dev/null; then
            echo "Patricia keepalive already running (PID: $(cat $PIDFILE))"
            exit 1
        fi
        main_loop &
        echo "✅ Patricia keepalive started"
        ;;
    stop)
        if [ -f "$PIDFILE" ]; then
            kill $(cat "$PIDFILE") 2>/dev/null
            rm -f "$PIDFILE"
            echo "🛑 Patricia keepalive stopped"
        else
            echo "Patricia keepalive not running"
        fi
        ;;
    status)
        if [ -f "$PIDFILE" ] && kill -0 $(cat "$PIDFILE") 2>/dev/null; then
            incomplete=$(check_queue_complete)
            echo "🌑 Patricia keepalive: RUNNING (PID: $(cat $PIDFILE))"
            echo "   Queue: $incomplete items remaining"
            echo "   Log: $LOG_FILE"
        else
            echo "🌑 Patricia keepalive: STOPPED"
        fi
        ;;
    once)
        run_patricia_tick
        advance_orders
        incomplete=$(check_queue_complete)
        echo "Queue: $incomplete items remaining"
        ;;
    *)
        main_loop
        ;;
esac
