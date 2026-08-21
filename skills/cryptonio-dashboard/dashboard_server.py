#!/usr/bin/env python3
"""
Cryptonio Live Dashboard Server v1.0
Real-time portfolio visualization with WebSocket updates
"""

import json
import asyncio
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from threading import Thread
import time
from datetime import datetime
import sys
import os

# Optional websockets support
try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    print("⚠️ websockets not available - using HTTP polling only")

sys.path.insert(0, '/root/.openclaw/workspace/agent_sandboxes/the-great-cryptonio')

from cryptonio_multi_exchange import UnifiedExchangeManager, Config as BotConfig

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Global state
dashboard_data = {
    'portfolio': {},
    'exchanges': {},
    'prices': {},
    'trades': [],
    'history': [],
    'timestamp': None,
    'total_value': 0.0,
    'total_btc': 0.0
}

exchange_manager = None
price_history = {}

# Crypto colors mapping (brand colors)
CRYPTO_COLORS = {
    'BTC': '#F7931A',   # Bitcoin orange
    'ETH': '#627EEA',   # Ethereum blue
    'LTC': '#BFBBBB',   # Litecoin gray
    'XRP': '#23292F',   # XRP black
    'DOGE': '#C2A633',  # Dogecoin yellow
    'ADA': '#0033AD',   # Cardano blue
    'SOL': '#00FFA3',   # Solana green
    'UNI': '#FF007A',   # Uniswap pink
    'AAVE': '#B6509E',  # AAVE purple
    'LINK': '#2A5ADA',  # Chainlink blue
    'SHIB': '#E8D44D',  # Shiba yellow
    'BCH': '#8DC351',   # Bitcoin Cash green
    'AVAX': '#E84142',  # Avalanche red
    'TRX': '#FF060A',   # Tron red
    'ANKR': '#2B65EC',  # Ankr blue
    'LRC': '#1D4A72',   # Loopring blue
    'MANA': '#FF2D55',  # Decentraland pink
    'POL': '#6F41D8',   # Polygon purple
    'APE': '#0054FA',   # ApeCoin blue
    'XMR': '#FF6600',   # Monero orange
    'ETC': '#3AB54A',   # Ethereum Classic green
    'GBP': '#C8102E',   # GBP red
    'EUR': '#003399',   # EUR blue
    'USD': '#85BB65',   # USD green
    'USDT': '#26A17B',  # Tether green
    'USDC': '#2775CA',  # USDC blue
    'VTHO': '#2B65EC',  # VeThor blue
    'ACH': '#0A3C7B',   # Alchemy Pay blue
    'KAVA': '#FF2D55',   # Kava pink
    'XLM': '#08B5E5',   # Stellar blue
    'SNX': '#00D1FF',   # Synthetix cyan
    'NOBODY': '#6B7280', # Misc gray
    'BABY': '#FFD700',   # Baby doge gold
    'DEFAULT': '#6B7280' # Default gray
}

def get_crypto_color(symbol):
    """Get color for crypto symbol"""
    base = symbol.replace('USD', '').replace('USDT', '').replace('USDC', '')
    return CRYPTO_COLORS.get(base, CRYPTO_COLORS['DEFAULT'])

def update_dashboard_data():
    """Update dashboard data from exchanges"""
    global dashboard_data, exchange_manager
    
    try:
        if not exchange_manager:
            exchange_manager = UnifiedExchangeManager()
        
        # Get all balances
        all_balances = {}
        exchanges_data = {}
        
        for name, client in exchange_manager.clients.items():
            balances = client.get_all_balances()
            all_balances[name] = balances
            
            # Calculate exchange totals
            exchange_total = 0.0
            for asset, amount in balances.items():
                pair = BotConfig.ASSET_PRICE_MAP.get(asset)
                if pair:
                    df = client.get_klines(pair, '1m', limit=1)
                    if not df.empty:
                        price = df['close'].iloc[-1]
                        exchange_total += amount * price
                        if asset not in dashboard_data['prices']:
                            dashboard_data['prices'][asset] = price
            
            exchanges_data[name] = {
                'total_usd': exchange_total,
                'balances': balances,
                'connected': client.is_connected
            }
        
        # Consolidate holdings
        consolidated = {}
        for exchange, balances in all_balances.items():
            for asset, amount in balances.items():
                if amount > 0:
                    if asset not in consolidated:
                        consolidated[asset] = {'total': 0, 'exchanges': {}}
                    consolidated[asset]['total'] += amount
                    consolidated[asset]['exchanges'][exchange] = amount
        
        # Calculate values for pie chart
        portfolio_items = []
        total_value = 0.0
        
        for asset, data in consolidated.items():
            pair = BotConfig.ASSET_PRICE_MAP.get(asset)
            price = dashboard_data['prices'].get(asset, 0)
            value = data['total'] * price if price > 0 else 0
            
            if asset in ['USD', 'USDT', 'USDC']:
                value = data['total']  # Cash is value itself
            
            total_value += value
            
            portfolio_items.append({
                'asset': asset,
                'amount': data['total'],
                'value_usd': value,
                'price': price,
                'color': get_crypto_color(asset),
                'exchanges': data['exchanges']
            })
        
        # Sort by value descending
        portfolio_items.sort(key=lambda x: x['value_usd'], reverse=True)
        
        # Update history for line chart
        if total_value > 0:
            price_history['values'] = price_history.get('values', [])
            price_history['values'].append({
                'timestamp': datetime.now().isoformat(),
                'value': total_value
            })
            # Keep last 1000 data points
            if len(price_history['values']) > 1000:
                price_history['values'] = price_history['values'][-1000:]
        
        dashboard_data = {
            'portfolio': portfolio_items,
            'exchanges': exchanges_data,
            'prices': dashboard_data['prices'],
            'trades': dashboard_data.get('trades', []),
            'history': price_history.get('values', []),
            'timestamp': datetime.now().isoformat(),
            'total_value': total_value,
            'total_btc': total_value / dashboard_data['prices'].get('BTC', 68000) if dashboard_data['prices'].get('BTC') else 0
        }
        
    except Exception as e:
        print(f"Error updating dashboard: {e}")

# Background data updater
def data_updater():
    """Background thread to update data"""
    while True:
        update_dashboard_data()
        time.sleep(30)  # Update every 30 seconds

# Flask routes
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/data')
def get_data():
    return jsonify(dashboard_data)

@app.route('/api/symbols')
def get_symbols():
    """Get available symbols"""
    if not exchange_manager:
        exchange_manager = UnifiedExchangeManager()
    symbols = {}
    for name, client in exchange_manager.clients.items():
        if hasattr(client, 'get_available_symbols'):
            symbols[name] = client.get_available_symbols()
    return jsonify(symbols)

@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """Force refresh data"""
    update_dashboard_data()
    return jsonify({'status': 'refreshed', 'timestamp': datetime.now().isoformat()})

# WebSocket handler (only if available)
if WEBSOCKETS_AVAILABLE:
    async def websocket_handler(websocket, path):
        """WebSocket handler for real-time updates"""
        try:
            await websocket.send(json.dumps({
                'type': 'connected',
                'message': 'Cryptonio Dashboard WebSocket connected'
            }))
            
            while True:
                # Send current data
                await websocket.send(json.dumps({
                    'type': 'update',
                    'data': dashboard_data
                }))
                await asyncio.sleep(5)  # Update every 5 seconds
                
        except websockets.exceptions.ConnectionClosed:
            pass
    
    # Start WebSocket server
    async def start_websocket():
        async with websockets.serve(websocket_handler, "0.0.0.0", 8765):
            await asyncio.Future()  # Run forever
    
    def run_websocket():
        """Run WebSocket server in thread"""
        asyncio.run(start_websocket())
else:
    def run_websocket():
        """WebSocket not available"""
        pass

if __name__ == '__main__':
    # Start data updater thread
    updater_thread = Thread(target=data_updater, daemon=True)
    updater_thread.start()
    
    # Start WebSocket server thread (if available)
    if WEBSOCKETS_AVAILABLE:
        websocket_thread = Thread(target=run_websocket, daemon=True)
        websocket_thread.start()
    
    # Start Flask server
    print("🚀 Cryptonio Dashboard Server starting...")
    print("📊 Dashboard: http://localhost:5000")
    if WEBSOCKETS_AVAILABLE:
        print("🔌 WebSocket: ws://localhost:8765")
    else:
        print("⚠️ WebSocket unavailable - using HTTP polling")
    print("📦 Auto-refresh: Every 5 seconds")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
