#!/bin/bash
# SEED3 Fleet Startup Script
# Auto-run on device boot

echo "╔═══════════════════════════════════════════╗"
echo "║   SEED3 FLEET BOOT SEQUENCE              ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

LOG="$HOME/mortimer/logs/boot-$(date +%Y%m%d-%H%M%S).log"
echo "Logging to: $LOG"

# 1. Core Services
echo "[1/5] Starting core services..."
cd ~/mortimer/services
for svc in quantum_oracle prime_helix riemann_helix; do
  nohup python3 -u "$svc.py" >> ~/mortimer/logs/"$svc".log 2>&1 &
  echo "  ✅ $svc (PID $!)"
done

# 2. QMD Brain
echo "[2/5] Starting QMD brain..."
cd ~/mortimer/services
# Kill anything on 8000 first
fuser -k 8000/tcp 2>/dev/null
sleep 1
nohup python3 -u qmd_service.py >> ~/mortimer/logs/qmd.log 2>&1 &
echo "  ✅ QMD (PID $!)"

# 3. Patricia
echo "[3/5] Starting Patricia..."
cd ~/mortimer/patricia
bash start.sh 2>/dev/null || nohup python3 -u patricia_service.py >> sandbox/logs/patricia.log 2>&1 &
echo "  ✅ Patricia"

# 4. JORDAN
echo "[4/5] Starting JORDAN..."
cd ~/agents/jordan
bash start.sh
echo "  ✅ JORDAN"

# 5. FORGE
echo "[5/5] Starting FORGE..."
cd ~/projects/standalone-dark-factory
bash start-forge.sh
echo "  ✅ FORGE"

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║   SEED3 FLEET ONLINE                     ║"
echo "╚═══════════════════════════════════════════╝"
ps aux | grep -E "node|python" | grep -v grep | wc -l
echo " processes running"

# Voice Settings (for future reference)
# DroidScript sweet voice: app.TextToSpeech("text", 1.618, 1.94)
# espeak: en-us -s 162 -p 52 -a 110 -k 0
# Sweet voice file: ~/downloads/voice_preview_claire.mp3

# Golden Mean Voice
# espeak -v en-us -s 161 -p 52 -a 100 -k 0

# VOICE SETTINGS (2026-07-14)
# Female: espeak -v en-us+f5 -s 155 -p 50 -a 65 -k 0
