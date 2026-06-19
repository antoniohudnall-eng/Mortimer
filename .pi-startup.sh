#!/bin/bash
# Pi Agent Startup - Mortimer Device
# This runs when pi agent starts

echo "═══════════════════════════════════════════════════"
echo "  Mortimer Pi Startup"
echo "═══════════════════════════════════════════════════"

# Home directory
HOME=/data/data/com.termux/files/home
cd $HOME

# 1. PulseAudio
echo "[1/6] PulseAudio..."
if ! pgrep -x pulseaudio > /dev/null; then
    pulseaudio --start --exit-idle-time=-1 2>/dev/null
fi
echo "  ✓ $(pgrep -x pulseaudio > /dev/null && echo 'Running' || echo 'Failed')"

# 2. Ollama
echo "[2/6] Ollama..."
if ! pgrep -f "ollama serve" > /dev/null; then
    export OLLAMA_HOST=0.0.0.0:11434
    export OLLAMA_MODEL="${OLLAMA_MODEL:-qwen2.5:1.5b}"
    nohup ollama serve > $HOME/mortimer/services/ollama.log 2>&1 &
    sleep 2
fi
echo "  ✓ $(pgrep -f 'ollama serve' > /dev/null && echo 'Running' || echo 'Failed')"

# 3. QMD Service
echo "[3/6] QMD Service..."
mkdir -p $HOME/mortimer/services
if ! pgrep -f "qmd_service.py" > /dev/null; then
    cd $HOME/mortimer/services
    export USE_OLLAMA="true"
    nohup python3 qmd_service.py > $HOME/mortimer/services/qmd.log 2>&1 &
    sleep 1
fi
echo "  ✓ $(pgrep -f 'qmd_service.py' > /dev/null && echo 'Running' || echo 'Failed')"

# 4. Voice Config (φ-modulated)
echo "[4/6] Voice (Golden Ratio)..."
MORTIMER_VOICE='-v en-us+m3 -s 161 -p 51 -a 113 -k 4'
export MORTIMER_VOICE
if [ -f $HOME/mortimer/voice/config.sh ]; then
    source $HOME/mortimer/voice/config.sh
fi
echo "  ✓ φ-Voice loaded: speed=161, pitch=51, amp=113, kt=4"
PHI=1.6180339887
echo "  ✓ Golden Ratio: $PHI"

# 5. Termux API
echo "[5/6] Termux API..."
export PATH=$PREFIX/bin:$PATH
echo "  ✓ Ready"

# 6. Patricia
echo "[6/6] Patricia..."
if [ -f $HOME/mortimer/patricia/config.json ]; then
    echo "  ✓ Config exists"
fi

# 7. GitHub Backup Check
echo "[7/7] GitHub Sync..."
if [ -f $HOME/mortimer/auto-backup.sh ]; then
    cd $HOME/mortimer
    git pull origin main > /dev/null 2>&1
    echo "  ✓ GitHub synced"
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo "  Services Status:"
echo "═══════════════════════════════════════════════════"
echo "  PulseAudio: $(pgrep -x pulseaudio > /dev/null && echo '🟢' || echo '🔴')"
echo "  Ollama: $(pgrep -f 'ollama serve' > /dev/null && echo '🟢' || echo '🔴')"
echo "  QMD: $(pgrep -f 'qmd_service.py' > /dev/null && echo '🟢' || echo '🔴')"
echo ""
echo "  Models:"
ollama list 2>/dev/null | grep -v "^$" | head -8
