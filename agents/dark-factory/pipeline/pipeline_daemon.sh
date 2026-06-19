#!/bin/bash
# Dark Factory Pipeline Daemon
# Continuous background processing for the Dark Factory

DAEMON_NAME="dark-factory-pipeline"
PIPELINE_LOG="/var/log/dark_factory/pipeline.log"
PIDFILE="/var/run/${DAEMON_NAME}.pid"
WORKSPACE="/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY"

create_directories() {
    mkdir -p /var/log/dark_factory
    mkdir -p /var/run
    touch "$PIPELINE_LOG"
}

start() {
    create_directories
    
    if [ -f "$PIDFILE" ] && kill -0 $(cat "$PIDFILE") 2>/dev/null; then
        echo "⚠️  Dark Factory Pipeline is already running (PID: $(cat $PIDFILE))"
        exit 1
    fi
    
    echo "🌑 Starting Dark Factory Pipeline..."
    
    nohup python3 "$WORKSPACE/pipeline/dark_factory_pipeline.py" run --interval 300 \
        >> "$PIPELINE_LOG" 2>&1 &
    
    echo $! > "$PIDFILE"
    echo "✅ Dark Factory Pipeline started (PID: $(cat $PIDFILE))"
    echo "   Log: $PIPELINE_LOG"
    echo "   Check: tail -f $PIPELINE_LOG"
}

stop() {
    if [ ! -f "$PIDFILE" ]; then
        echo "⚠️  Dark Factory Pipeline is not running"
        exit 1
    fi
    
    PID=$(cat "$PIDFILE")
    echo "🛑 Stopping Dark Factory Pipeline (PID: $PID)..."
    
    kill "$PID" 2>/dev/null
    rm -f "$PIDFILE"
    
    echo "✅ Dark Factory Pipeline stopped"
}

status() {
    if [ -f "$PIDFILE" ] && kill -0 $(cat "$PIDFILE") 2>/dev/null; then
        PID=$(cat "$PIDFILE")
        UPTIME=$(ps -o etime= -p "$PID" 2>/dev/null | tr -d ' ')
        echo "🌑 Dark Factory Pipeline: RUNNING"
        echo "   PID: $PID"
        echo "   Uptime: ${UPTIME:-unknown}"
        echo "   Log: $PIPELINE_LOG"
        
        # Show last 5 log entries
        echo "   Recent activity:"
        tail -n 5 "$PIPELINE_LOG" 2>/dev/null | sed 's/^/     /'
    else
        echo "🌑 Dark Factory Pipeline: STOPPED"
        if [ -f "$PIDFILE" ]; then
            rm -f "$PIDFILE"
        fi
    fi
}

run_once() {
    create_directories
    echo "🔄 Running single pipeline tick..."
    python3 "$WORKSPACE/pipeline/dark_factory_pipeline.py" tick
}

report() {
    python3 "$WORKSPACE/pipeline/dark_factory_pipeline.py" report
}

queue() {
    python3 "$WORKSPACE/pipeline/dark_factory_pipeline.py" queue
}

add_order() {
    python3 "$WORKSPACE/pipeline/dark_factory_pipeline.py" add "$@"
}

# Ensure log directory exists
create_directories

case "${1:-status}" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart|reload)
        stop
        sleep 1
        start
        ;;
    status)
        status
        ;;
    tick|once)
        run_once
        ;;
    report)
        report
        ;;
    queue)
        queue
        ;;
    add)
        shift
        add_order "$@"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|tick|report|queue|add}"
        echo ""
        echo "Commands:"
        echo "  start    - Start the continuous pipeline daemon"
        echo "  stop     - Stop the pipeline daemon"
        echo "  restart  - Restart the pipeline daemon"
        echo "  status   - Show pipeline status"
        echo "  tick     - Run a single pipeline tick"
        echo "  report   - Generate pipeline report"
        echo "  queue    - Show current queue"
        echo "  add      - Add a new order (requires --product, --type, etc.)"
        echo ""
        echo "Examples:"
        echo "  $0 start"
        echo "  $0 add --product 'POS System' --type pos --client 'ClientName'"
        exit 1
        ;;
esac
