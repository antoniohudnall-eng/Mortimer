#!/bin/bash
# Load credentials from vault and run bot

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load Binance Primary
export BINANCE_US_API_KEY=$(grep "BINANCE_US_API_KEY=" "$SCRIPT_DIR/vault/binance_us.env" | cut -d'=' -f2 | tr -d '"')
export BINANCE_US_API_SECRET=$(grep "BINANCE_US_SECRET_KEY=" "$SCRIPT_DIR/vault/binance_us.env" | cut -d'=' -f2 | tr -d '"')

# Load Binance Secondary
export BINANCE_US_API_KEY_2=$(grep "BINANCE_US_SECOND_API_KEY=" "$SCRIPT_DIR/vault/binance_us_second.env" | cut -d'=' -f2 | tr -d '"')
export BINANCE_US_API_SECRET_2=$(grep "BINANCE_US_SECOND_SECRET=" "$SCRIPT_DIR/vault/binance_us_second.env" | cut -d'=' -f2 | tr -d '"')

# Load Gemini
export GEMINI_API_KEY=$(grep "GEMINI_API_KEY=" "$SCRIPT_DIR/vault/gemini.env" | cut -d'=' -f2 | tr -d '"')
export GEMINI_API_SECRET=$(grep "GEMINI_API_SECRET=" "$SCRIPT_DIR/vault/gemini.env" | cut -d'=' -f2 | tr -d '"')

# Load Kraken
export KRAKEN_API_KEY=$(grep "^KRAKEN_API_KEY=" "$SCRIPT_DIR/vault/kraken.env" | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)
export KRAKEN_API_SECRET=$(grep "^KRAKEN_API_SECRET=" "$SCRIPT_DIR/vault/kraken.env" | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)

# Load Coinbase (optional)
if [ -f "$SCRIPT_DIR/vault/coinbase.env" ]; then
    export COINBASE_API_KEY=$(grep "^COINBASE_API_KEY=" "$SCRIPT_DIR/vault/coinbase.env" | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)
    export COINBASE_API_SECRET=$(grep "^COINBASE_API_SECRET=" "$SCRIPT_DIR/vault/coinbase.env" | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)
    export COINBASE_PASSPHRASE=$(grep "^COINBASE_PASSPHRASE=" "$SCRIPT_DIR/vault/coinbase.env" | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)
fi

echo "✅ Credentials loaded from vault"
echo "   - Binance Primary: ${BINANCE_US_API_KEY:0:10}..."
echo "   - Binance Secondary: ${BINANCE_US_API_KEY_2:0:10}..."
echo "   - Gemini: ${GEMINI_API_KEY:0:10}..."
echo "   - Kraken: ${KRAKEN_API_KEY:0:15}..."
if [ -n "$COINBASE_API_KEY" ] && [ "$COINBASE_API_KEY" != "PASTE_KEY_HERE" ]; then
    echo "   - Coinbase: ${COINBASE_API_KEY:0:10}..."
fi
echo ""
if [ -n "$KRAKEN_API_KEY" ]; then
    echo "🔑 Kraken activated!"
fi
if [ -n "$COINBASE_API_KEY" ] && [ "$COINBASE_API_KEY" != "PASTE_KEY_HERE" ]; then
    echo "🔑 Coinbase activated!"
fi
echo ""

# Run bot with arguments
python3 "$SCRIPT_DIR/cryptonio_multi_exchange.py" "$@"
