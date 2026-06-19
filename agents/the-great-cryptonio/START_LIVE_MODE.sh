#!/bin/bash
# Live Multi-Asset Arbitrage Launcher
# Version: 4.1.1-LIVE

cd "$(dirname "$0")"

# Load credentials
export $(cat vault/binance_us.env | grep -v '^#' | xargs)
export $(cat vault/binance_us_second.env | grep -v '^#' | xargs)
export $(cat vault/kraken.env | grep -v '^#' | xargs)

echo "=========================================="
echo "  CRYPTONIO v4.1.1 — LIVE MODE"
echo "  Multi-Asset + Arbitrage"
echo "=========================================="
echo ""
echo "Symbols: BTC, DOGE, LTC, XRP"
echo "Exchanges: Binance (2), Kraken, Gemini"
echo "Arbitrage Threshold: 0.5%"
echo "Auto-Execute: >1% spread"
echo "Risk: $10/day per exchange"
echo ""
echo "Type 'LIVE' to confirm:"
read CONFIRM

if [ "$CONFIRM" != "LIVE" ]; then
    echo "Cancelled."
    exit 1
fi

echo ""
echo "🚀 STARTING LIVE TRADING..."
echo ""

# Start with all features
python3 cryptonio_multi_exchange.py --live --multi-asset 2>&1 | tee logs/live_trading_$(date +%Y%m%d_%H%M%S).log
