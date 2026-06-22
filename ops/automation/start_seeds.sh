#!/bin/bash
# 🚀 SEED3 AUTO-START
# Run on device boot to initialize all services

echo "=================================================="
echo "🚀 SEED3 STARTUP - $(date)"
echo "=================================================="

cd ~/mortimer

# Start PulseAudio
echo "[1/6] Starting PulseAudio..."
pulseaudio --start 2>/dev/null || true

# Start nginx
echo "[2/6] Starting nginx..."
nginx -t 2>/dev/null && nginx -s reload 2>/dev/null || nginx

# Start Ollama
echo "[3/6] Starting Ollama..."
if ! pgrep -x ollama > /dev/null; then
    nohup ollama serve > /dev/null 2>&1 &
    sleep 3
fi

# Start QMD
echo "[4/6] Starting QMD service..."
if ! pgrep -f qmd_service > /dev/null; then
    cd ~/mortimer/services
    nohup python3 -u qmd_service.py > qmd.log 2>&1 &
    sleep 2
fi

# Start Patricia
echo "[5/6] Starting Patricia..."
if ! pgrep -f patricia_service > /dev/null; then
    cd ~/mortimer/patricia
    nohup python3 -u patricia_service.py > patricia.log 2>&1 &
    sleep 2
fi

# Verify
echo "[6/6] Verifying services..."
sleep 2

echo ""
echo "=================================================="
echo "📊 SERVICE STATUS"
echo "=================================================="

echo "nginx: $(pgrep -a nginx | head -1 | cut -d' ' -f1) ✅" 2>/dev/null || echo "nginx: ❌"
echo "ollama: $(pgrep -a ollama | head -1 | cut -d' ' -f1) ✅" 2>/dev/null || echo "ollama: ❌"
echo "qmd: $(pgrep -f qmd_service | cut -d' ' -f1) ✅" 2>/dev/null || echo "qmd: ❌"
echo "patricia: $(pgrep -f patricia_service | cut -d' ' -f1) ✅" 2>/dev/null || echo "patricia: ❌"

echo ""
echo "🚀 SEED3 READY"
echo "=================================================="

# Run health check
python3 ~/mortimer/ops/automation/ship_automation.py health
