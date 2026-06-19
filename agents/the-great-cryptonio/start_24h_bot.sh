#!/usr/bin/env bash
# CRYPTONIO 24/7 TRADING BOT RUNNER
# Runs the crypto trading bot continuously with auto-restart

set -e

BOT_DIR="/root/.openclaw/workspace/aocros/agent_sandboxes/the-great-cryptonio"
LOG_DIR="$BOT_DIR/logs"
VAULT_DIR="/root/.aos/vault"

# Ensure directories exist
mkdir -p "$LOG_DIR"
mkdir -p "$VAULT_DIR"

echo "═══════════════════════════════════════════════════════════"
echo "  CRYPTONIO PRODUCTION BOT - 24/7 RUNNER"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check if API keys exist in vault
if [ ! -f "$VAULT_DIR/binance_api.json" ]; then
    echo "⚠️  API keys not found in vault!"
    echo "Expected: $VAULT_DIR/binance_api.json"
    echo ""
    echo "Please create the file with:"
    echo '{"api_key": "YOUR_KEY", "api_secret": "YOUR_SECRET"}'
    exit 1
fi

# Load API keys
export BINANCE_US_API_KEY=$(cat "$VAULT_DIR/binance_api.json" | python3 -c "import sys,json; print(json.load(sys.stdin)['api_key'])")
export BINANCE_US_API_SECRET=$(cat "$VAULT_DIR/binance_api.json" | python3 -c "import sys,json; print(json.load(sys.stdin)['api_secret'])")

if [ -z "$BINANCE_US_API_KEY" ] || [ -z "$BINANCE_US_API_SECRET" ]; then
    echo "❌ Failed to load API keys from vault"
    exit 1
fi

echo "✅ API keys loaded from vault"
echo "✅ Bot directory: $BOT_DIR"
echo "✅ Log directory: $LOG_DIR"
echo ""

# Kill existing session if running
if tmux has-session -t cryptonio 2>/dev/null; then
    echo "🛑 Stopping existing Cryptonio session..."
    tmux kill-session -t cryptonio
    sleep 2
fi

# Install dependencies if needed
if ! python3 -c "import pandas, numpy, requests" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install pandas numpy requests --break-system-packages 2>/dev/null || pip3 install pandas numpy requests
fi

echo "🚀 Starting Cryptonio Bot in PAPER TRADING MODE..."
echo ""

# Start bot in tmux with auto-restart
tmux new-session -d -s cryptonio "
    cd '$BOT_DIR'
    export PAPER_TRADING=true
    export MAX_DAILY_RISK_PER_PAIR=10.00
    export GLOBAL_MAX_DAILY_RISK=50.00
    while true; do
        echo 'Starting Cryptonio Bot v3.0 (Multi-Currency) at \$(date)'
        python3 cryptonio_bot_v3.py 2>&1 | tee -a '$LOG_DIR/cryptonio_24h.log'
        echo 'Bot crashed or stopped at \$(date). Restarting in 10 seconds...'
        sleep 10
    done
"

echo "═══════════════════════════════════════════════════════════"
echo "  ✅ CRYPTONIO IS NOW RUNNING 24/7 (PAPER TRADING)"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Session: tmux attach -t cryptonio"
echo "Logs: tail -f $LOG_DIR/cryptonio_24h.log"
echo "Stop: tmux kill-session -t cryptonio"
echo ""
echo "Wallet for profits: 0x2ce0c5D9aaD321d1Ea0ad02F02bde75A5fB0E3BE"
echo ""
echo "⚠️  PAPER TRADING MODE - No real money at risk"
echo ""
