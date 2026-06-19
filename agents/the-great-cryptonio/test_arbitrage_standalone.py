#!/usr/bin/env python3
"""
Standalone Arbitrage Test
Tests price differences across exchanges without full bot initialization
"""

import os
import sys
import requests
import pandas as pd
from datetime import datetime

sys.path.insert(0, '/root/.openclaw/workspace/agent_sandboxes/r2-d2')

print("=" * 70)
print("🔍 CROSS-EXCHANGE ARBITRAGE SCANNER v4.1.1")
print("=" * 70)
print(f"Time: {datetime.now().isoformat()}")
print()

# Load credentials
def load_env_file(filepath):
    """Load environment variables from file"""
    env_vars = {}
    try:
        with open(filepath) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, val = line.strip().split('=', 1)
                    env_vars[key] = val.strip().strip('"').strip("'")
    except Exception as e:
        print(f"⚠️  Could not load {filepath}: {e}")
    return env_vars

# Load all credentials
print("Loading credentials...")
binance_1 = load_env_file('vault/binance_us.env')
binance_2 = load_env_file('vault/binance_us_second.env')
kraken = load_env_file('vault/kraken.env')

print(f"✅ Credentials loaded: {len(binance_1) + len(binance_2) + len(kraken)} keys")
print()

# Set environment
os.environ.update(binance_1)
os.environ.update(binance_2)
os.environ.update(kraken)

# Now import and test
from cryptonio_multi_exchange import UnifiedExchangeManager, Config

print("=" * 70)
print("Connecting to exchanges...")
print("=" * 70)

manager = UnifiedExchangeManager()

connected = [name for name, client in manager.clients.items() if client.is_connected]
print(f"\n🟢 Connected: {len(connected)} exchanges")
for name in connected:
    print(f"   ✓ {name}")

if not connected:
    print("\n❌ No exchanges connected - cannot scan arbitrage")
    print("\nPossible issues:")
    print("  - API keys not found in vault/")
    print("  - Network connectivity")
    print("  - Rate limiting")
    sys.exit(1)

print()
print("=" * 70)
print("Scanning for arbitrage opportunities...")
print(f"Symbols: {', '.join(Config.ACTIVE_SYMBOLS)}")
print(f"Threshold: {Config.ARBITRAGE_THRESHOLD}%")
print("=" * 70)

opportunities_found = []

for symbol in Config.ACTIVE_SYMBOLS:
    print(f"\n📊 {symbol}")
    print("-" * 50)
    
    prices = {}
    errors = []
    
    for name, client in manager.clients.items():
        if not client.is_connected:
            continue
        
        try:
            # Get latest price
            df = client.get_klines(symbol, '1m', limit=1)
            if not df.empty and len(df) > 0:
                price = float(df['close'].iloc[-1])
                prices[name] = price
                print(f"   {name:20s}: ${price:>12,.2f}")
            else:
                errors.append(f"{name}: No data")
        except Exception as e:
            errors.append(f"{name}: {str(e)[:30]}")
    
    if errors:
        for err in errors:
            print(f"   ⚠️  {err}")
    
    if len(prices) >= 2:
        max_price = max(prices.values())
        min_price = min(prices.values())
        max_ex = max(prices, key=prices.get)
        min_ex = min(prices, key=prices.get)
        spread_pct = ((max_price - min_price) / min_price) * 100
        
        profit_per_unit = max_price - min_price
        
        print(f"\n   Spread: {spread_pct:.2f}%")
        
        if spread_pct > Config.ARBITRAGE_THRESHOLD:
            print(f"   🚨 ARBITRAGE OPPORTUNITY DETECTED!")
            print(f"   💡 BUY on {min_ex}  @ ${min_price:,.2f}")
            print(f"   💡 SELL on {max_ex} @ ${max_price:,.2f}")
            print(f"   💰 Profit per unit: ${profit_per_unit:,.2f}")
            
            # Calculate potential profit with $50 position
            if 'BTC' in symbol:
                units = 50 / min_price
                potential_profit = units * profit_per_unit
                print(f"   💰 With $50: Buy {units:.6f} BTC → Profit ${potential_profit:.2f}")
            elif 'DOGE' in symbol:
                units = 50 / min_price
                potential_profit = units * profit_per_unit
                print(f"   💰 With $50: Buy {units:.2f} DOGE → Profit ${potential_profit:.2f}")
            else:
                print(f"   💰 Example: $50 position → ${50 * spread_pct / 100:.2f} profit")
            
            opportunities_found.append({
                'symbol': symbol,
                'buy_exchange': min_ex,
                'buy_price': min_price,
                'sell_exchange': max_ex,
                'sell_price': max_price,
                'spread_pct': spread_pct,
                'profit_per_unit': profit_per_unit
            })
        else:
            print(f"   ✅ No significant spread detected")
    else:
        print(f"   ⚠️  Insufficient data ({len(prices)} exchange(s))")

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)

if opportunities_found:
    print(f"\n🎉 {len(opportunities_found)} arbitrage opportunity(s) found!")
    print()
    for i, opp in enumerate(opportunities_found, 1):
        print(f"{i}. {opp['symbol']}: {opp['spread_pct']:.2f}% spread")
        print(f"   Buy {opp['buy_exchange']} @ ${opp['buy_price']:,.2f}")
        print(f"   Sell {opp['sell_exchange']} @ ${opp['sell_price']:,.2f}")
    print()
    print("To execute these arbitrages:")
    print("  python3 cryptonio_multi_exchange.py --live --multi-asset")
else:
    print("\n📊 No arbitrage opportunities above threshold")
    print("   Prices are closely aligned across exchanges")
    print("\nThis is normal - arbitrage opportunities are:")
    print("  - Time-sensitive (last seconds to minutes)")
    print("  - More common during high volatility")
    print("  - Require fast execution to capture")
    print("\nContinuous monitoring will catch them when they appear!")

print()
print("=" * 70)
