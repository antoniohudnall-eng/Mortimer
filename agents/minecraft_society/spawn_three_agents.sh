#!/bin/bash
#
# Spawn 3 Mineflayer Agents with Brain OODA
# Usage: ./spawn_three_agents.sh
#

cd /root/.openclaw/workspace/scripts/minecraft_agents

echo "=========================================="
echo "  SPAWNING 3 AUTONOMOUS AGENTS"
echo "=========================================="
echo ""

# Ensure Brain server is running
if ! ss -tlnp | grep -q ":8767"; then
    echo "Starting Brain server..."
    python3 simple_brain_server.py > /tmp/brain.log 2>&1 &
    sleep 2
fi

echo "Spawning mylzeron..."
node simple_agent.js mylzeron localhost 25566 ws://localhost:8767 > /tmp/mylzeron.log 2>&1 &
MYLZERON_PID=$!
echo "  PID: $MYLZERON_PID"
sleep 3

echo "Spawning mylonen..."
node simple_agent.js mylonen localhost 25566 ws://localhost:8767 > /tmp/mylonen.log 2>&1 &
MYLONEN_PID=$!
echo "  PID: $MYLONEN_PID"
sleep 3

echo "Spawning myltwon..."
node simple_agent.js myltwon localhost 25566 ws://localhost:8767 > /tmp/myltwon.log 2>&1 &
MYLTWON_PID=$!
echo "  PID: $MYLTWON_PID"
sleep 3

echo ""
echo "=========================================="
echo "  3 AGENTS SPAWNED"
echo "=========================================="
echo ""
echo "Agents:"
echo "  mylzeron (male)   - PID $MYLZERON_PID"
echo "  mylonen (male)    - PID $MYLONEN_PID"
echo "  myltwon (male)    - PID $MYLTWON_PID"
echo ""
echo "Logs:"
echo "  /tmp/mylzeron.log"
echo "  /tmp/mylonen.log"
echo "  /tmp/myltwon.log"
echo ""
echo "Brain:"
echo "  /tmp/brain.log"
echo ""
echo "To stop: kill $MYLZERON_PID $MYLONEN_PID $MYLTWON_PID"
echo ""

# Monitor
sleep 5
echo "Status check:"
ps aux | grep -E "(mylzeron|mylonen|myltwon)" | grep -v grep | awk '{print $11, $2, $3"%"}'

echo ""
echo "Agents are now autonomously:"
echo "  - Observing world state (blocks, entities, health)"
echo "  - Orienting (identifying threats/opportunities)"
echo "  - Deciding (OODA loop at 2 Hz)"
echo "  - Acting (move, mine, hunt, flee, explore)"
echo "  - Reporting to Brain for coordination"
echo ""
echo "Type 'stop' to terminate all agents"

read -r input
if [ "$input" = "stop" ]; then
    kill $MYLZERON_PID $MYLONEN_PID $MYLTWON_PID 2>/dev/null
    echo "Agents stopped"
fi