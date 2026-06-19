#!/bin/bash
# Society Agent Keepalive - Simple stable version
# Spawns 5 agents with delays, restarts them if they die

AGENT_DIR="/root/.openclaw/workspace/scripts/minecraft_agents"
LOG_DIR="/var/log/aos"
AGENTS="marcus julius titus julia livia"

cd "$AGENT_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to check if agent is running
check_agent() {
    local agent=$1
    pgrep -f "simple_society_agent.js $agent" > /dev/null
}

# Function to spawn agent
spawn_agent() {
    local agent=$1
    log "Spawning $agent..."
    nohup node simple_society_agent.js "$agent" localhost 25565 > "$LOG_DIR/society_${agent}.log" 2>&1 &
    sleep 8  # Delay to avoid connection throttling
}

# Main loop
while true; do
    for agent in $AGENTS; do
        if ! check_agent "$agent"; then
            log "$agent is down, respawning..."
            spawn_agent "$agent"
        fi
    done
    
    # Show status every minute
    if (( $(date +%s) % 60 == 0 )); then
        running=$(pgrep -f "simple_society_agent.js" | wc -l)
        log "Status: $running/5 society agents running"
    fi
    
    sleep 15
done
