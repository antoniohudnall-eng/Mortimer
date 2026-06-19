#!/bin/bash
# Mortimer Device Setup Script
# Sets up: Brain/QMD, Patricia, Temporal, Voice (11Labs)

set -e

echo "═══════════════════════════════════════════════════"
echo "  Mortimer Device Setup"
echo "═══════════════════════════════════════════════════"

# 1. PULSEAUDIO (already installed & running)
echo -e "\n[1/6] PulseAudio..."
if ! pgrep -x pulseaudio > /dev/null; then
    pulseaudio --start --exit-idle-time=-1
fi
echo "✓ PulseAudio running"

# 2. OLLAMA MODELS
echo -e "\n[2/6] Ollama Models..."
echo "Current models:"
ollama list

# Download needed models
MODELS=("llama3.2:3b" "nomic-embed-text:latest")
for model in "${MODELS[@]}"; do
    if ! ollama list | grep -q "^$model "; then
        echo "Pulling $model..."
        ollama pull "$model"
    else
        echo "✓ $model already installed"
    fi
done

# 3. QMD SERVICE
echo -e "\n[3/6] QMD Service..."
mkdir -p ~/mortimer/services
mkdir -p ~/mortimer/voice/output

# Create systemd/tmux service for QMD
cat > ~/mortimer/services/start_qmd.sh << 'EOF'
#!/bin/bash
cd ~/mortimer/services
source ~/.bashrc 2>/dev/null
export OLLAMA_MODEL="${OLLAMA_MODEL:-qwen2.5:1.5b}"
export USE_OLLAMA="${USE_OLLAMA:-false}"
python3 qmd_service.py
EOF
chmod +x ~/mortimer/services/start_qmd.sh

# Start QMD in background if not running
if ! pgrep -f "qmd_service.py" > /dev/null; then
    nohup ~/mortimer/services/start_qmd.sh > ~/mortimer/services/qmd.log 2>&1 &
    echo "✓ QMD service started (PID: $!)"
else
    echo "✓ QMD service already running"
fi

# 4. PATRICIA AGENT
echo -e "\n[4/6] Patricia Agent..."
mkdir -p ~/mortimer/patricia

# Create Patricia config
cat > ~/mortimer/patricia/config.json << 'EOF'
{
    "name": "Patricia",
    "role": "Process Excellence Officer",
    "emoji": "📊🧠🔄",
    "models": {
        "decision": "qwen2.5:1.5b",
        "analysis": "llama3.2:3b",
        "embedding": "nomic-embed-text:latest"
    },
    "brain": {
        "memory_dir": "/data/data/com.termux/files/home/AOS-Brain/memory",
        "qmd_endpoint": "http://127.0.0.1:8000"
    },
    "skills": ["process_analysis", "optimization", "reporting"]
}
EOF
echo "✓ Patricia configured"

# 5. TEMPORAL
echo -e "\n[5/6] Temporal Server..."
TEMPORAL_DIR=~/mortimer/temporal
mkdir -p $TEMPORAL_DIR

if [ ! -f "$TEMPORAL_DIR/temporal" ]; then
    echo "Downloading Temporal..."
    cd $TEMPORAL_DIR
    
    # Detect architecture
    ARCH=$(uname -m)
    case $ARCH in
        aarch64|arm64) TEMPORAL_ARCH="arm64" ;;
        x86_64) TEMPORAL_ARCH="amd64" ;;
        *) echo "Unknown architecture: $ARCH"; exit 1 ;;
    esac
    
    VERSION="1.25.0"
    URL="https://temporal.download/cli/artifacts/${VERSION}/temporal_${VERSION}_linux_${TEMPORAL_ARCH}.zip"
    
    curl -sL "$URL" -o temporal.zip
    unzip -q temporal.zip
    rm temporal.zip
    chmod +x temporal
    
    echo "✓ Temporal downloaded"
else
    echo "✓ Temporal already installed"
fi

# Create Temporal config
cat > $TEMPORAL_DIR/config.yaml << 'EOF'
persistence:
  default:
    driver: "sqlite"
    config:
      filename: "./data/default.db"

services:
  history:
    rpc:
      port: 7233
  matching:
    rpc:
      port: 7235
  worker:
    rpc:
      port: 7239
  frontend:
    rpc:
      port: 7233
    grpcPort: 7233

ui:
  enabled: true
  port: 8233

log:
  level: info
EOF

mkdir -p $TEMPORAL_DIR/data

# 6. VOICE (11Labs)
echo -e "\n[6/6] Voice Configuration..."
source ~/mortimer/voice/config.sh

# Create Python TTS wrapper
cat > ~/mortimer/voice/speak.py << 'EOF'
#!/usr/bin/env python3
"""ElevenLabs TTS wrapper for Mortimer"""

import sys
import os
import requests
import tempfile
from pathlib import Path

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
VOICE_ID = os.environ.get("VOICE_ADAM", "pNInz6obpgDQGcFmaJgB")

def speak(text, voice_id=None, play=True):
    if not ELEVENLABS_API_KEY:
        print("[TTS] No API key configured")
        return None
    
    voice = voice_id or VOICE_ID
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
    
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    try:
        resp = requests.post(url, json=data, headers=headers, timeout=30)
        if resp.status_code == 200:
            # Save to temp file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                f.write(resp.content)
                path = f.name
            
            if play:
                os.system(f"play '{path}' 2>/dev/null || aplay '{path}' 2>/dev/null")
            
            return path
        else:
            print(f"[TTS] Error: {resp.status_code}")
            return None
    except Exception as e:
        print(f"[TTS] Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        speak(text)
    else:
        print("Usage: speak.py <text>")
EOF
chmod +x ~/mortimer/voice/speak.py

echo ""
echo "═══════════════════════════════════════════════════"
echo "  Setup Complete!"
echo "═══════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "  1. Set ELEVENLABS_API_KEY environment variable"
echo "  2. Start Temporal: ~/mortimer/temporal/temporal server start"
echo "  3. Check services: ~/mortimer/services/start_qmd.sh"
echo ""
echo "To use voice:"
echo "  source ~/mortimer/voice/config.sh"
echo "  export ELEVENLABS_API_KEY=your_key_here"
echo "  python3 ~/mortimer/voice/speak.py 'Hello Captain'"
echo ""