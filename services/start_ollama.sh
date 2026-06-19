#!/bin/bash
# Start Ollama server with proper environment

# Kill any existing instance
pkill -f "ollama serve" 2>/dev/null

# Start pulseaudio
pulseaudio --start --exit-idle-time=-1 2>/dev/null

# Start Ollama
export OLLAMA_HOST=0.0.0.0:11434
nohup ollama serve > ~/mortimer/services/ollama.log 2>&1 &
echo "Ollama started with PID: $!"
