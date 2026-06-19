#!/bin/bash
# SEED3 STARTUP SCRIPT
# Morty's Ship Initialization

echo "🚀 SEED3 INITIALIZING..."
echo ""

# Quantum Services
echo "🟢 Starting Quantum Oracle (7777)..."
cd /data/data/com.termux/files/home/mortimer/services
if ! pgrep -f "quantum_oracle.py" > /dev/null; then
    nohup python3 quantum_oracle.py > quantum_oracle.log 2>&1 &
    echo "   ✅ Quantum Oracle online"
else
    echo "   ⚠️  Already running"
fi

echo "🟢 Starting Prime Helix (7778)..."
if ! pgrep -f "prime_helix.py" > /dev/null; then
    nohup python3 prime_helix.py > prime_helix.log 2>&1 &
    echo "   ✅ Prime Helix online"
else
    echo "   ⚠️  Already running"
fi

echo "🟢 Starting Riemann Helix (7779)..."
if ! pgrep -f "riemann_helix.py" > /dev/null; then
    nohup python3 riemann_helix.py > riemann_helix.log 2>&1 &
    echo "   ✅ Riemann Helix online"
else
    echo "   ⚠️  Already running"
fi

echo ""
echo "📊 SERVICE STATUS:"
for port in 7777 7778 7779; do
    if curl -s --max-time 1 http://127.0.0.1:$port/health > /dev/null 2>&1; then
        echo "   🟢 Port $port - ONLINE"
    else
        echo "   🔴 Port $port - OFFLINE"
    fi
done

echo ""
echo "✅ SEED3 INITIALIZATION COMPLETE"
date
