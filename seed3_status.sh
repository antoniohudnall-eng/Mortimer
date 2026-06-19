#!/bin/bash
# SEED3 STATUS CHECKER
echo "╔═══════════════════════════════════════╗"
echo "║  SEED3 STATUS - $(date '+%H:%M:%S')"
echo "╚═══════════════════════════════════════╝"
echo ""

echo "🟢 QUANTUM SERVICES:"
for port in 7777 7778 7779; do
    if curl -s --max-time 1 http://127.0.0.1:$port/health > /dev/null 2>&1; then
        echo "   Port $port: 🟢 ONLINE"
    else
        echo "   Port $port: 🔴 OFFLINE"
    fi
done

echo ""
echo "🧠 AI SERVICES:"
pgrep -a ollama > /dev/null && echo "   Ollama: 🟢 RUNNING" || echo "   Ollama: 🔴 STOPPED"
pgrep -f "qmd_service.py" > /dev/null && echo "   QMD: 🟢 RUNNING" || echo "   QMD: 🔴 STOPPED"

echo ""
echo "🤖 AGENTS: $(ls -1 /data/data/com.termux/files/home/mortimer/agents/ | wc -l) loaded"
echo "📦 SOFTWARE: $(find /data/data/com.termux/files/home/mortimer/software -type f | wc -l) files"
