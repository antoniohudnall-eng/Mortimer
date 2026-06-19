#!/usr/bin/env python3
"""
Full Portfolio Scanner - Shows ALL assets across exchanges
"""

import sys
import os

# Load credentials
with open('vault/binance_us.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            os.environ[k] = v

with open('vault/binance_us_second.env') as f:
    content = f.read()
    for line in content.split('\n'):
        if 'BINANCE_US_SECOND_API_KEY=' in line:
            os.environ['BINANCE_US_API_KEY_2'] = line.split('=', 1)[1]
        elif 'BINANCE_US_SECOND_SECRET=' in line:
            os.environ['BINANCE_US_API_SECRET_2'] = line.split('=', 1)[1]

sys.path.insert(0, '/root/.openclaw/workspace/agent_sandboxes/the-great-cryptonio')
from binance.client import Client

print('=' * 60)
print('💎 FULL PORTFOLIO ACROSS ALL ASSETS')
print('=' * 60)

# Primary Account
print('\n📊 PRIMARY ACCOUNT (Binance.US):')
try:
    client1 = Client(os.environ['BINANCE_US_API_KEY'], os.environ['BINANCE_US_SECRET_KEY'], tld='us')
    account1 = client1.get_account()
    
    assets1 = []
    for b in account1['balances']:
        amt = float(b['free']) + float(b['locked'])
        if amt > 0:
            assets1.append((b['asset'], amt))
    
    assets1.sort(key=lambda x: x[1], reverse=True)
    for asset, amt in assets1[:15]:
        print(f'   {asset:6s}: {amt:15.6f}')
except Exception as e:
    print(f'   Error: {e}')

# Secondary Account
print('\n📊 SECONDARY ACCOUNT (Binance.US):')
try:
    if os.environ.get('BINANCE_US_API_KEY_2'):
        client2 = Client(os.environ['BINANCE_US_API_KEY_2'], os.environ['BINANCE_US_API_SECRET_2'], tld='us')
        account2 = client2.get_account()
        
        assets2 = []
        for b in account2['balances']:
            amt = float(b['free']) + float(b['locked'])
            if amt > 0:
                assets2.append((b['asset'], amt))
        
        assets2.sort(key=lambda x: x[1], reverse=True)
        for asset, amt in assets2[:10]:
            print(f'   {asset:6s}: {amt:15.6f}')
except Exception as e:
    print(f'   Error: {e}')

# Get current prices
try:
    print('\n💰 ESTIMATED VALUES (at current prices):')
    prices = client1.get_symbol_ticker()
    price_map = {p['symbol']: float(p['price']) for p in prices}
    
    # Add Kraken BTC balance (from previous logs)
    print('\n📊 KRAKEN ACCOUNT:')
    print('   BTC   :      0.003473  (~$236)')
    
    total_value = 236  # Kraken estimate
    
    # Calculate primary account value
    primary_subtotal = 0
    for asset, amt in assets1:
        if asset in ['USD', 'USDT', 'USDC', 'BUSD']:
            value = amt
        elif asset + 'USDT' in price_map:
            value = amt * price_map[asset + 'USDT']
        elif asset + 'USD' in price_map:
            value = amt * price_map[asset + 'USD']
        else:
            value = 0
        if value > 0.5:  # Only show values > $0.50
            print(f'   {asset:6s}: ${value:10.2f} ({amt:12.6f})')
            primary_subtotal += value
    
    print(f'\n   Primary Subtotal:   ${primary_subtotal:10.2f}')
    
    # Secondary
    secondary_subtotal = 0
    for asset, amt in assets2:
        if asset in ['USD', 'USDT', 'USDC', 'BUSD']:
            value = amt
        elif asset + 'USDT' in price_map:
            value = amt * price_map[asset + 'USDT']
        elif asset + 'USD' in price_map:
            value = amt * price_map[asset + 'USD']
        else:
            value = 0
        if value > 0.5:
            secondary_subtotal += value
    
    print(f'   Secondary Subtotal: ${secondary_subtotal:10.2f}')
    print(f'   Kraken Estimate:    ${236:10.2f}')
    
    total = primary_subtotal + secondary_subtotal + 236
    print(f'\n   {"="*40}')
    print(f'   TOTAL PORTFOLIO:     ${total:10.2f}')
    print(f'   {"="*40}')
    
except Exception as e:
    print(f'   Price lookup error: {e}')

print('\n' + '=' * 60)
