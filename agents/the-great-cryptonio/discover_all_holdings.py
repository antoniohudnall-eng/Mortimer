#!/usr/bin/env python3
"""
Discover All Holdings - Standalone script to scan full portfolio
"""

import base64
import hashlib
import hmac
import json
import urllib.parse
import requests
import os
import sys
from datetime import datetime

print("=" * 70)
print("🔍 FULL PORTFOLIO DISCOVERY")
print("=" * 70)
print(f"Time: {datetime.now().isoformat()}")
print()

# Load credentials
def load_credentials():
    creds = {}
    vault_path = '/root/.openclaw/workspace/agent_sandboxes/the-great-cryptonio/vault/'
    
    # Load Kraken
    try:
        with open(vault_path + 'kraken.env') as f:
            for line in f:
                if 'KRAKEN_API_KEY=' in line and not line.startswith('#'):
                    creds['kraken_key'] = line.split('=', 1)[1].strip().strip('"').strip("'")
                elif 'KRAKEN_API_SECRET=' in line and not line.startswith('#'):
                    creds['kraken_secret'] = line.split('=', 1)[1].strip().strip('"').strip("'")
    except:
        pass
    
    # Load Binance Primary
    try:
        with open(vault_path + 'binance_us.env') as f:
            content = f.read()
            for line in content.split('\n'):
                if 'BINANCE_US_API_KEY=' in line:
                    creds['binance_key'] = line.split('=', 1)[1].strip()
                elif 'BINANCE_US_SECRET_KEY=' in line:
                    creds['binance_secret'] = line.split('=', 1)[1].strip()
    except:
        pass
    
    # Load Binance Secondary
    try:
        with open(vault_path + 'binance_us_second.env') as f:
            content = f.read()
            for line in content.split('\n'):
                if 'BINANCE_US_SECOND_API_KEY=' in line:
                    creds['binance_key_2'] = line.split('=', 1)[1]
                elif 'BINANCE_US_SECOND_SECRET=' in line:
                    creds['binance_secret_2'] = line.split('=', 1)[1]
    except:
        pass
    
    return creds

# Kraken full balance scan
def get_kraken_balances(key, secret):
    print("\n🦑 Scanning Kraken...")
    try:
        nonce = int(datetime.now().timestamp() * 1000)
        data = {'nonce': nonce}
        urlpath = '/0/private/Balance'
        
        postdata = urllib.parse.urlencode(data)
        encoded = (str(nonce) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()
        mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
        signature = base64.b64encode(mac.digest()).decode()
        
        headers = {'API-Key': key, 'API-Sign': signature}
        response = requests.post('https://api.kraken.com' + urlpath, headers=headers, data=data)
        result = response.json()
        
        if result.get('error'):
            print(f"   Error: {result['error']}")
            return {}
        
        # Asset mapping
        asset_map = {
            'XXBT': 'BTC', 'XBT': 'BTC', 'ZUSD': 'USD', 'ZEUR': 'EUR',
            'XETH': 'ETH', 'XLTC': 'LTC', 'XXRP': 'XRP', 'XADA': 'ADA',
            'XXMR': 'XMR', 'XAVAX': 'AVAX', 'XSOL': 'SOL', 'XLINK': 'LINK',
            'XUNI': 'UNI', 'BCH': 'BCH', 'AAVE': 'AAVE', 'TRX': 'TRX',
            'ANKR': 'ANKR', 'POL': 'POL', 'LRC': 'LRC', 'XETC': 'ETC',
            'ZGBP': 'GBP'
        }
        
        balances = {}
        for k_code, amount in result['result'].items():
            bal = float(amount)
            if bal > 0:
                asset = asset_map.get(k_code, k_code)
                if asset not in balances:
                    balances[asset] = 0.0
                balances[asset] += bal
        
        if balances:
            print(f"   ✅ Found {len(balances)} assets")
        return balances
    except Exception as e:
        print(f"   Error: {e}")
        return {}

# Binance full balance scan
def get_binance_balances(key, secret, label):
    print(f"\n📊 Scanning Binance {label}...")
    try:
        sys.path.insert(0, '/root/.openclaw/workspace/external')
        from binance.client import Client
        client = Client(key, secret, tld='us')
        account = client.get_account()
        
        balances = {}
        for b in account['balances']:
            total = float(b['free']) + float(b['locked'])
            if total > 0:
                balances[b['asset']] = total
        
        if balances:
            print(f"   ✅ Found {len(balances)} assets")
        return balances
    except Exception as e:
        print(f"   Error: {e}")
        return {}

# Get current prices
def get_prices():
    print("\n💰 Fetching current prices...")
    prices = {}
    try:
        response = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTUSD,ETHUSD,LTCUSD,XRPUSD,ADAUSD,SOLUSD,AVAXUSD,LINKUSD,UNIUSD,AAVEUSD,BCHUSD,TRXUSD,ANKRUSD,POLUSD')
        data = response.json()
        if not data.get('error'):
            for pair, info in data['result'].items():
                asset = pair.replace('XXBT', 'BTC').replace('XBT', 'BTC').replace('ZUSD', '').replace('X', '')
                prices[asset] = float(info['c'][0])
    except:
        pass
    return prices

# Main execution
if __name__ == "__main__":
    import sys
    
    creds = load_credentials()
    
    all_balances = {}
    
    # Scan Kraken
    if 'kraken_key' in creds:
        kraken_balances = get_kraken_balances(creds['kraken_key'], creds['kraken_secret'])
        if kraken_balances:
            all_balances['Kraken'] = kraken_balances
    
    # Scan Binance Primary
    if 'binance_key' in creds:
        binance_balances = get_binance_balances(creds['binance_key'], creds['binance_secret'], "Primary")
        if binance_balances:
            all_balances['Binance_Primary'] = binance_balances
    
    # Scan Binance Secondary
    if 'binance_key_2' in creds:
        binance_balances_2 = get_binance_balances(creds['binance_key_2'], creds['binance_secret_2'], "Secondary")
        if binance_balances_2:
            all_balances['Binance_Secondary'] = binance_balances_2
    
    # Get prices
    prices = get_prices()
    
    # Print summary
    print("\n" + "=" * 70)
    print("💎 COMPLETE PORTFOLIO SUMMARY")
    print("=" * 70)
    
    # Consolidate
    consolidated = {}
    for exchange, balances in all_balances.items():
        print(f"\n📊 {exchange.upper()}:")
        for asset, amount in sorted(balances.items(), key=lambda x: x[1], reverse=True)[:15]:
            if amount > 0:
                print(f"   {asset:8s}: {amount:15.8f}")
                if asset not in consolidated:
                    consolidated[asset] = 0.0
                consolidated[asset] += amount
    
    # Calculate values
    print("\n" + "-" * 70)
    print("📈 CONSOLIDATED HOLDINGS:")
    total_value = 0.0
    
    for asset, total in sorted(consolidated.items(), key=lambda x: x[1], reverse=True):
        if total > 0:
            if asset in prices:
                value = total * prices[asset]
                total_value += value
                print(f"   {asset:8s}: {total:15.8f} (${value:,.2f})")
            elif asset in ['USD', 'USDT']:
                total_value += total
                print(f"   {asset:8s}: ${total:,.2f} (cash)")
            else:
                print(f"   {asset:8s}: {total:15.8f} (no price)")
    
    print("-" * 70)
    print(f"💰 TOTAL ESTIMATED VALUE: ${total_value:,.2f}")
    if 'BTC' in prices:
        print(f"   ≈ {total_value / prices['BTC']:.6f} BTC")
    print(f"   {len(consolidated)} unique assets")
    print("=" * 70)
    
    # Save to file
    with open('/tmp/portfolio_discovery.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'exchanges': all_balances,
            'consolidated': consolidated,
            'total_value_usd': total_value,
            'asset_count': len(consolidated)
        }, f, indent=2)
    
    print("\n✅ Results saved to /tmp/portfolio_discovery.json")
