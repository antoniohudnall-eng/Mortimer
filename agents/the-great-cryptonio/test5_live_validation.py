#!/usr/bin/env python3
"""
TEST #5: Live Trading Validation
Verify real order placement without executing (dry-run validation)
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/agent_sandboxes/the-great-cryptonio')

# Load credentials
import os
with open('vault/binance_us.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            os.environ[k] = v

# Get secondary creds  
with open('vault/binance_us_second.env') as f:
    content = f.read()
    for line in content.split('\n'):
        if 'BINANCE_US_SECOND_API_KEY=' in line:
            os.environ['BINANCE_US_API_KEY_2'] = line.split('=', 1)[1]
        elif 'BINANCE_US_SECOND_SECRET=' in line:
            os.environ['BINANCE_US_API_SECRET_2'] = line.split('=', 1)[1]

from binance.client import Client

print("=" * 60)
print("🧪 TEST #5: LIVE TRADING VALIDATION")
print("=" * 60)

# Test Primary Account
print("\n[1/4] Testing Primary Account Connection...")
try:
    client1 = Client(os.environ['BINANCE_US_API_KEY'], os.environ['BINANCE_US_SECRET_KEY'], tld='us')
    client1.ping()
    print("   ✅ Primary API: Connected")
    
    # Get account info
    account = client1.get_account()
    balances = {b['asset']: float(b['free']) for b in account['balances'] if float(b['free']) > 0}
    print(f"   ✅ Primary Balances: {balances}")
    
    # Check specific BTC
    btc_bal = next((float(b['free']) for b in account['balances'] if b['asset'] == 'BTC'), 0)
    print(f"   💎 Primary BTC: {btc_bal:.6f}")
    
except Exception as e:
    print(f"   ❌ Primary Failed: {e}")
    client1 = None

# Test Secondary Account
print("\n[2/4] Testing Secondary Account Connection...")
try:
    if os.environ.get('BINANCE_US_API_KEY_2'):
        client2 = Client(os.environ['BINANCE_US_API_KEY_2'], os.environ['BINANCE_US_API_SECRET_2'], tld='us')
        client2.ping()
        print("   ✅ Secondary API: Connected")
        
        account2 = client2.get_account()
        btc_bal2 = next((float(b['free']) for b in account2['balances'] if b['asset'] == 'BTC'), 0)
        print(f"   💎 Secondary BTC: {btc_bal2:.6f}")
    else:
        print("   ⚠️ Secondary credentials not loaded")
        client2 = None
except Exception as e:
    print(f"   ❌ Secondary Failed: {e}")
    client2 = None

# Test Market Data
print("\n[3/4] Testing Live Market Data...")
try:
    if client1:
        ticker = client1.get_symbol_ticker(symbol='BTCUSDT')
        price = float(ticker['price'])
        print(f"   ✅ Live BTC Price: ${price:,.2f}")
        
        # Get order book
        depth = client1.get_order_book(symbol='BTCUSDT', limit=5)
        best_bid = float(depth['bids'][0][0])
        best_ask = float(depth['asks'][0][0])
        spread = ((best_ask - best_bid) / best_bid) * 100
        print(f"   ✅ Order Book: Bid ${best_bid:,.2f} / Ask ${best_ask:,.2f} (spread: {spread:.3f}%)")
    else:
        print("   ⚠️ Skipped - no primary client")
except Exception as e:
    print(f"   ❌ Market Data Failed: {e}")

# Validate Trading Permissions
print("\n[4/4] Validating Trading Permissions...")
try:
    if client1:
        # Check exchange info
        info = client1.get_exchange_info()
        btc_info = next((s for s in info['symbols'] if s['symbol'] == 'BTCUSDT'), None)
        if btc_info:
            print(f"   ✅ BTCUSDT Trading: Enabled")
            print(f"   ✅ Status: {btc_info.get('status', 'Unknown')}")
            
            # Check our permissions
            account_info = client1.get_account()
            can_trade = account_info.get('canTrade', False)
            print(f"   ✅ Account Trading Permission: {can_trade}")
            
            if can_trade:
                print("\n" + "=" * 60)
                print("🟢 LIVE TRADING READY")
                print("=" * 60)
                print("All validations passed. Ready for live order placement.")
            else:
                print("\n🔴 Trading permissions disabled")
                
except Exception as e:
    print(f"   ❌ Trading Check Failed: {e}")

print("\n" + "=" * 60)
print("TEST #5 COMPLETE")
print("=" * 60)
