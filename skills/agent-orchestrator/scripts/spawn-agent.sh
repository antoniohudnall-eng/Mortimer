#!/bin/bash
# Spawn a sub-agent with given task and label

TASK="$1"
LABEL="$2"
TIMEOUT="${3:-300}"

if [ -z "$TASK" ] || [ -z "$LABEL" ]; then
    echo "Usage: spawn-agent.sh 'task description' 'label' [timeout_seconds]"
    exit 1
fi

echo "Spawning agent: $LABEL"
echo "Task: $TASK"
echo "Timeout: ${TIMEOUT}s"

# Note: This is a template - actual spawning uses OpenClaw's sessions_spawn API
# In practice, call this via the OpenClaw agent API
