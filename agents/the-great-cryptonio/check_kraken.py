#!/usr/bin/env python3
"""Quick Kraken Balance Check"""
import base64
import hashlib
import hmac
import urllib.parse
import requests
import os
import json

# Load Kraken credentials
with open('/root/.openclaw/workspace/agent_sandboxes/the-great-cryptonio/vault/kraken.env') as f:
    for line in f:
        if 'KRAKEN_API_KEY=' in line and not line.startswith('#'):
            API_KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        elif 'KRAKEN_API_SECRET=' in line and not line.startswith('#'):
            API_SECRET = line.split('=', 1)[1].strip().strip('"').strip("'")

print("=" * 60)
print("🦑 KRAKEN FULL BALANCE CHECK")
print("=" * 60)

# Get balance
nonce = int(__import__('time').time() * 1000)
urlpath = '/0/private/Balance'
postdata = urllib.parse.urlencode({'nonce': nonce})
encoded = (str(nonce) + postdata).encode()
message = urlpath.encode() + hashlib.sha256(encoded).digest()
mac = hmac.new(base64.b64decode(API_SECRET), message, hashlib.sha512)
signature = base64.b64encode(mac.digest()).decode()

headers = {'API-Key': API_KEY, 'API-Sign': signature}
response = requests.post('https://api.kraken.com' + urlpath, headers=headers, data={'nonce': nonce})

result = response.json()

if result.get('error'):
    print(f"Error: {result['error']}")
else:
    balances = result['result']
    
    print("\nAssets with balance:")
    print("-" * 60)
    
    # Asset name mapping
    asset_names = {
        'XXBT': 'BTC', 'XBT': 'BTC', 'BTC': 'BTC',
        'ZUSD': 'USD', 'USD': 'USD',
        'ZEUR': 'EUR', 'EUR': 'EUR',
        'XETH': 'ETH', 'ETH': 'ETH',
        'XLTC': 'LTC', 'LTC': 'LTC',
        'XXRP': 'XRP', 'XRP': 'XRP',
    }
    
    total_assets = 0
    for asset_raw, balance in sorted(balances.items()):
        bal = float(balance)
        if bal > 0:
            total_assets += 1
            # Map asset code
            asset = asset_raw
            for code, name in asset_names.items():
                if asset_raw.startswith(code) or asset_raw == code:
                    asset = name
                    break
            print(f"   {asset:10s}: {bal:15.8f}")
    
    print("-" * 60)
    print(f"Total assets: {total_assets}")
    
    # Get current BTC price for estimate
    print("\nFetching current BTC price...")
    try:
        ticker = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTUSD').json()
        btc_price = float(ticker['result']['XXBTZUSD']['c'][0])
        print(f"Current BTC price: ${btc_price:,.2f}")
        
        # Calculate approximate value
        btc_balance = float(balances.get('XXBT', 0))
        usd_balance = float(balances.get('ZUSD', 0))
        btc_value = btc_balance * btc_price
        total_value = btc_value + usd_balance
        
        print(f"\nEstimated value:")
        print(f"   BTC: {btc_balance:.6f} × ${btc_price:,.2f} = ${btc_value:,.2f}")
        print(f"   USD: ${usd_balance:,.2f}")
        print(f"   TOTAL: ${total_value:,.2f}")
    except Exception as e:
        print(f"Could not fetch price: {e}")

print("=" * 60)
