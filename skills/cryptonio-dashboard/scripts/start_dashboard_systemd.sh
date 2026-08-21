#!/bin/bash
# Cryptonio Dashboard Wrapper for SystemD
# Loads credentials and starts dashboard

SCRIPT_DIR="/root/.openclaw/workspace/agent_sandboxes/the-great-cryptonio"
cd "$SCRIPT_DIR"

# Load credentials
export BINANCE_US_API_KEY=$(grep "BINANCE_US_API_KEY=" "$SCRIPT_DIR/vault/binance_us.env" | cut -d'=' -f2 | tr -d '"')
export BINANCE_US_API_SECRET=$(grep "BINANCE_US_SECRET_KEY=" "$SCRIPT_DIR/vault/binance_us.env" | cut -d'=' -f2 | tr -d '"')

export BINANCE_US_API_KEY_2=$(grep "BINANCE_US_SECOND_API_KEY=" "$SCRIPT_DIR/vault/binance_us_second.env" | cut -d'=' -f2 | tr -d '"')
export BINANCE_US_API_SECRET_2=$(grep "BINANCE_US_SECOND_SECRET=" "$SCRIPT_DIR/vault/binance_us_second.env" | cut -d'=' -f2 | tr -d '"')

export GEMINI_API_KEY=$(grep "GEMINI_API_KEY=" "$SCRIPT_DIR/vault/gemini.env" | cut -d'=' -f2 | tr -d '"')
export GEMINI_API_SECRET=$(grep "GEMINI_API_SECRET=" "$SCRIPT_DIR/vault/gemini.env" | cut -d'=' -f2 | tr -d '"')

export KRAKEN_API_KEY=$(grep "^KRAKEN_API_KEY=" "$SCRIPT_DIR/vault/kraken.env" | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)
export KRAKEN_API_SECRET=$(grep "^KRAKEN_API_SECRET=" "$SCRIPT_DIR/vault/kraken.env" | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)

if [ -f "$SCRIPT_DIR/vault/coinbase.env" ]; then
    export COINBASE_API_KEY=$(grep "^COINBASE_API_KEY=" "$SCRIPT_DIR/vault/coinbase.env" | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)
    export COINBASE_API_SECRET=$(grep "^COINBASE_API_SECRET=" "$SCRIPT_DIR/vault/coinbase.env" | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)
    export COINBASE_PASSPHRASE=$(grep "^COINBASE_PASSPHRASE=" "$SCRIPT_DIR/vault/coinbase.env" | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)
fi

# Start dashboard
exec /usr/bin/python3 "$SCRIPT_DIR/dashboard_server.py"
