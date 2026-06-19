#!/bin/bash
# Mortimer Pi Startup Script
# Launches all services when pi agent starts

echo "═══════════════════════════════════════════════════"
echo "  Mortimer Pi Startup"
echo "═══════════════════════════════════════════════════"

# 1. PulseAudio
echo "[1/5] PulseAudio..."
if ! pgrep -x pulseaudio > /dev/null; then
    pulseaudio --start --exit-idle-time=-1
    echo "  ✓ Started"
else
    echo "  ✓ Already running"
fi

# 2. Ollama
echo "[2/5] Ollama..."
if ! pgrep -f "ollama serve" > /dev/null; then
    export OLLAMA_HOST=0.0.0.0:11434
    nohup ollama serve > ~/mortimer/services/ollama.log 2>&1 &
    sleep 2
    echo "  ✓ Started (PID: $!)"
else
    echo "  ✓ Already running"
fi

# 3. QMD Service
echo "[3/5] QMD Service..."
mkdir -p ~/mortimer/services
if ! pgrep -f "qmd_service.py" > /dev/null; then
    cd ~/mortimer/services
    export OLLAMA_MODEL="${OLLAMA_MODEL:-qwen2.5:1.5b}"
    export USE_OLLAMA="${USE_OLLAMA:-true}"
    nohup python3 qmd_service.py > ~/mortimer/services/qmd.log 2>&1 &
    sleep 1
    echo "  ✓ Started (PID: $!)"
else
    echo "  ✓ Already running"
fi

# 4. Termux API
echo "[4/5] Termux API..."
export PATH=$PREFIX/bin:$PATH
if ! command -v termux-battery-status &>/dev/null; then
    pkg install -y termux-api 2>/dev/null
fi
echo "  ✓ Ready"

# 5. Voice (11Labs config)
echo "[5/5] Voice config..."
if [ -f ~/mortimer/voice/config.sh ]; then
    source ~/mortimer/voice/config.sh
    echo "  ✓ Config loaded"
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo "  All services started!"
echo "═══════════════════════════════════════════════════"
echo ""
echo "Services:"
echo "  - PulseAudio: $(pgrep -x pulseaudio > /dev/null && echo '✓' || echo '✗')"
echo "  - Ollama: $(pgrep -f 'ollama serve' > /dev/null && echo '✓' || echo '✗')"
echo "  - QMD: $(pgrep -f 'qmd_service.py' > /dev/null && echo '✓' || echo '✗')"
echo ""
echo "Ollama models:"
ollama list | grep -v "^$" | head -10
