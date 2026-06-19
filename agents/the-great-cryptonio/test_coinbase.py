#!/usr/bin/env python3
import requests
import base64
import hashlib
import hmac
import json
import time
import os

API_KEY = "85b6b91d-7f35-429f-bae1-f7323ed14f3d"
API_SECRET = "cJnxs3YmFgYGsBN1u4RNqtEyhK9mQFmDc8P4D/YvKg5ZjW5skymvkP6t8NGXxjdXwGn7FVa0MdruBwjYrVHArg=="
PASSPHRASE = ""  # Empty

def get_signature(timestamp, method, path, body=''):
    secret = base64.b64decode(API_SECRET)
    message = f"{timestamp}{method.upper()}{path}{body}"
    signature = hmac.new(secret, message.encode(), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()

print("Testing Coinbase connection...")
print("=" * 60)

# Test 1: Public API (should work)
print("\n[1/3] Testing public API...")
try:
    response = requests.get("https://api.pro.coinbase.com/products")
    if response.status_code == 200:
        products = response.json()
        btc_usd = [p for p in products if p['id'] == 'BTC-USD']
        if btc_usd:
            print(f"   ✅ Public API OK - BTC-USD trading: {btc_usd[0].get('status', 'unknown')}")
        else:
            print(f"   ✅ Public API OK - {len(products)} products available")
except Exception as e:
    print(f"   ❌ Public API error: {e}")

# Test 2: Authenticated endpoint (without passphrase)
print("\n[2/3] Testing authenticated API (without passphrase)...")
try:
    timestamp = str(int(time.time()))
    path = '/accounts'
    signature = get_signature(timestamp, 'GET', path)
    
    headers = {
        'CB-ACCESS-KEY': API_KEY,
        'CB-ACCESS-SIGN': signature,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'CB-ACCESS-PASSPHRASE': PASSPHRASE,  # Empty
        'Content-Type': 'application/json'
    }
    
    response = requests.get("https://api.pro.coinbase.com/accounts", headers=headers)
    print(f"   Response: {response.status_code}")
    print(f"   Body: {response.text[:200]}")
    
    if response.status_code == 200:
        accounts = response.json()
        total = sum(float(a['balance']) for a in accounts if float(a['balance']) > 0)
        print(f"   ✅ AUTHENTICATED - Total balance: ${total:.2f}")
        for a in accounts[:5]:
            if float(a['balance']) > 0:
                print(f"      {a['currency']}: {a['balance']}")
    elif response.status_code == 401:
        print("   ❌ Authentication failed - PASSPHRASE REQUIRED")
        print("   The API key needs the passphrase created during setup")
    else:
        print(f"   ⚠️  Unexpected response: {response.status_code}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Advanced Trade API (newer API, might use different auth)
print("\n[3/3] Testing Advanced Trade API...")
print("   Coinbase Advanced Trade uses OAuth, not API keys")
print("   API key format suggests this is Coinbase Pro (legacy)")

print("\n" + "=" * 60)
print("CONCLUSION:")
print("Coinbase Pro requires 3 credentials:")
print("1. ✅ API Key (UUID)")
print("2. ✅ API Secret (base64)")
print("3. ❌ PASSPHRASE (missing - required for authentication)")
print("\nWithout passphrase, authentication will fail.")
print("\nOptions:")
print("A) Check Coinbase Pro → Profile → API → Edit key → recover passphrase")
print("B) Create new API key (will show new passphrase)")
print("C) Try Advanced Trade OAuth flow (different system)")
