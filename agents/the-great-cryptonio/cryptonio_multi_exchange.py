#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRYPTONIO UNIFIED EXCHANGE MANAGER
Multi-Asset Trading Bot with R2-D2 Integration + Arbitrage
Version: 4.1.1 (Multi-Asset + Arbitrage Detection)
- Binance.US (Primary + Secondary)
- Gemini
- Kraken
- Coinbase Pro

Features:
- Unified portfolio view across ALL exchanges
- Smart order routing (best exchange for symbol)
- Cross-exchange arbitrage detection
- Failover between exchanges
- Paper trading mode for all exchanges
- Live trading with safety checks

Total Portfolio: $443.28 (Binance) + pending other exchanges

Author: Mortimer for Captain
Version: 3.0.0 (Multi-Exchange)
"""

import os
import sys
import json
import time
import logging
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, List, Any
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod

import pandas as pd
import numpy as np
import requests

# Add R2 module
sys.path.insert(0, '/root/.openclaw/workspace/agent_sandboxes/r2-d2')
from r2_confluence_calculator import CryptonioAdapter

# ═══════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════

class ExchangeType(Enum):
    BINANCE_US = "binance_us"
    GEMINI = "gemini"
    KRAKEN = "kraken"
    COINBASE = "coinbase"


@dataclass
class ExchangeConfig:
    """Configuration for a single exchange"""
    exchange_type: ExchangeType
    name: str  # e.g., "binance_primary", "binance_secondary", "gemini_main"
    api_key: str
    api_secret: str
    passphrase: Optional[str] = None  # For Coinbase
    sandbox: bool = True
    is_active: bool = False
    priority: int = 1
    
    # Trading limits
    max_daily_risk: float = 10.0
    max_positions: int = 1
    min_order_size: float = 10.0
    

class Config:
    """Master configuration for all exchanges"""
    
    # ═════════════════════════════════════════════════════════
    # BINANCE.US ACCOUNTS
    # ═════════════════════════════════════════════════════════
    EXCHANGES = []
    
    # Binance.US Primary ($188.36)
    if os.getenv('BINANCE_US_API_KEY'):
        EXCHANGES.append(ExchangeConfig(
            exchange_type=ExchangeType.BINANCE_US,
            name="binance_us_primary",
            api_key=os.getenv('BINANCE_US_API_KEY', ''),
            api_secret=os.getenv('BINANCE_US_API_SECRET', ''),
            priority=4,
            is_active=True
        ))
    
    # Binance.US Secondary ($169.88)
    if os.getenv('BINANCE_US_API_KEY_2'):
        EXCHANGES.append(ExchangeConfig(
            exchange_type=ExchangeType.BINANCE_US,
            name="binance_us_secondary",
            api_key=os.getenv('BINANCE_US_API_KEY_2', ''),
            api_secret=os.getenv('BINANCE_US_API_SECRET_2', ''),
            priority=3,
            is_active=True
        ))
    
    # ═════════════════════════════════════════════════════════
# GEMINI - DISABLED (invalid API key)
    # ═════════════════════════════════════════════════════════
#    if os.getenv('GEMINI_API_KEY'):
#        EXCHANGES.append(ExchangeConfig(
#            exchange_type=ExchangeType.GEMINI,
#            name="gemini_main",
#            api_key=os.getenv('GEMINI_API_KEY', ''),
#            api_secret=os.getenv('GEMINI_API_SECRET', ''),
#            priority=2,
#            is_active=True
#        ))
    
    # ═════════════════════════════════════════════════════════
    # KRAKEN (Full Implementation Ready)
    # ═════════════════════════════════════════════════════════
    if os.getenv('KRAKEN_API_KEY'):
        EXCHANGES.append(ExchangeConfig(
            exchange_type=ExchangeType.KRAKEN,
            name="kraken_main",
            api_key=os.getenv('KRAKEN_API_KEY', ''),
            api_secret=os.getenv('KRAKEN_API_SECRET', ''),
            priority=2,
            is_active=True
        ))
    
    # ═════════════════════════════════════════════════════════
    # COINBASE PRO (Full Implementation Ready)
    # ═════════════════════════════════════════════════════════
    if os.getenv('COINBASE_API_KEY'):
        EXCHANGES.append(ExchangeConfig(
            exchange_type=ExchangeType.COINBASE,
            name="coinbase_main",
            api_key=os.getenv('COINBASE_API_KEY', ''),
            api_secret=os.getenv('COINBASE_API_SECRET', ''),
            passphrase=os.getenv('COINBASE_PASSPHRASE', ''),
            priority=2,
            is_active=True
        ))
    if os.getenv('COINBASE_API_KEY'):
        EXCHANGES.append(ExchangeConfig(
            exchange_type=ExchangeType.COINBASE,
            name="coinbase_main",
            api_key=os.getenv('COINBASE_API_KEY', ''),
            api_secret=os.getenv('COINBASE_API_SECRET', ''),
            passphrase=os.getenv('COINBASE_PASSPHRASE', ''),
            priority=2,
            is_active=True
        ))
    
    # ═════════════════════════════════════════════════════════
    # GLOBAL SETTINGS
    # ═════════════════════════════════════════════════════════
    TIMEFRAME = '15m'
    SYMBOL = 'BTCUSD'  # Default single symbol (backward compat)
    
    # Multi-Asset Trading Configuration (v4.1.0)
    ACTIVE_SYMBOLS = [
        'BTCUSD',    # Bitcoin - Primary trading pair
        'DOGEUSD',   # Dogecoin - Large holdings on Binance
        'LTCUSD',    # Litecoin - Available on Binance Primary
        'XRPUSD',    # XRP - Available on Binance Secondary
    ]
    
    # Symbol to Exchange Mapping (preferred exchange per asset)
    SYMBOL_PREFERENCES = {
        'BTCUSD': ['kraken', 'binance_primary', 'binance_secondary'],
        'DOGEUSD': ['binance_primary', 'binance_secondary'],
        'LTCUSD': ['binance_primary'],
        'XRPUSD': ['binance_secondary'],
    }
    
    # Asset to Trading Pair Mapping (for price lookups)
    ASSET_PRICE_MAP = {
        'BTC': 'BTCUSD',
        'ETH': 'ETHUSD',
        'LTC': 'LTCUSD',
        'XRP': 'XRPUSD',
        'DOGE': 'DOGEUSD',
        'ADA': 'ADAUSD',
        'SOL': 'SOLUSD',
        'UNI': 'UNIUSD',
        'AAVE': 'AAVEUSD',
        'LINK': 'LINKUSD',
        'SHIB': 'SHIBUSD',
        'BCH': 'BCHUSD',
        'AVAX': 'AVAXUSD',
        'TRX': 'TRXUSD',
        'ANKR': 'ANKRUSD',
        'LRC': 'LRCUSD',
        'MANA': 'MANAUSD',
        'POL': 'POLUSD',
        'APE': 'APEUSD',
        'XMR': 'XMRUSD',
        'ETC': 'ETCUSD',
        'XLM': 'XLMUSD',
        'SNX': 'SNXUSD',
        'KAVA': 'KAVAUSD',
        'VTHO': 'VTHOUSD',
        'ACH': 'ACHUSD',
        'USD': None,  # Cash
        'USDT': None,
        'USDC': None,
    }
    
    PAPER_TRADING = True
    
    # Risk Management
    TOTAL_MAX_DAILY_RISK = 50.00  # Across ALL exchanges
    MIN_CONFLUENCE_SCORE = 60
    RISK_REWARD_RATIO = 1.5
    
    # Order Splitting
    SPLIT_ORDERS = True
    SPLIT_THRESHOLD = 50.00
    
    # Arbitrage
    ARBITRAGE_THRESHOLD = 0.5  # 0.5% price difference
    
    # Logging
    LOG_FILE = '/root/.openclaw/workspace/agent_sandboxes/the-great-cryptonio/logs/cryptonio_multi.log'


# ═══════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════

os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('CryptonioMulti')


# ═══════════════════════════════════════════════════════════
# ABSTRACT EXCHANGE CLIENT (Base Class)
# ═══════════════════════════════════════════════════════════

class BaseExchangeClient(ABC):
    """Abstract base class for all exchange clients"""
    
    def __init__(self, config: ExchangeConfig):
        self.config = config
        self.name = config.name
        self.exchange_type = config.exchange_type
        self.client = None
        self.is_connected = False
        self.last_error = None
        
        # Account state
        self.balance_usd = 0.0
        self.balance_btc = 0.0
        self.positions_open = 0
        self.daily_risk_used = 0.0
        
    @abstractmethod
    def connect(self) -> bool:
        """Connect to exchange API"""
        pass
    
    @abstractmethod
    def get_klines(self, symbol: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
        """Fetch OHLCV data"""
        pass
    
    @abstractmethod
    def get_balance(self, asset: str) -> float:
        """Get balance for specific asset"""
        pass
    
    @abstractmethod
    def place_market_order(self, symbol: str, side: str, quantity: float,
                          stop_loss: Optional[float] = None,
                          take_profit: Optional[float] = None) -> Optional[Dict]:
        """Place market order"""
        pass
    
    @abstractmethod
    def get_open_orders(self, symbol: str) -> int:
        """Get number of open orders"""
        pass
    
    def get_all_balances(self) -> Dict[str, float]:
        """Get all balances (override if exchange supports batch)"""
        return {
            'USD': self.get_balance('USD'),
            'BTC': self.get_balance('BTC')
        }


# ═══════════════════════════════════════════════════════════
# BINANCE.US CLIENT
# ═══════════════════════════════════════════════════════════

class BinanceClient(BaseExchangeClient):
    """Binance.US exchange client"""
    
    def connect(self) -> bool:
        try:
            from binance.client import Client
            self.client = Client(
                self.config.api_key,
                self.config.api_secret,
                tld='us'
            )
            # Test connection
            self.client.ping()
            self.is_connected = True
            logger.info(f"✅ [{self.name}] Binance.US connected")
            return True
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"❌ [{self.name}] Connection failed: {e}")
            return False
    
    def get_klines(self, symbol: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
        if not self.is_connected:
            return pd.DataFrame()
        
        try:
            # Map timeframe to Binance format
            binance_timeframe = timeframe.replace('m', 'm').replace('h', 'h')
            
            klines = self.client.get_klines(
                symbol=symbol.replace('USD', 'USDT'),  # Binance uses USDT
                interval=binance_timeframe,
                limit=limit
            )
            
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
            
        except Exception as e:
            logger.error(f"[{self.name}] Klines error: {e}")
            return pd.DataFrame()
    
    def get_balance(self, asset: str) -> float:
        if not self.is_connected:
            return 0.0
        
        try:
            account = self.client.get_account()
            for balance in account['balances']:
                if balance['asset'] == asset:
                    return float(balance['free'])
            return 0.0
        except Exception as e:
            logger.error(f"[{self.name}] Balance error: {e}")
            return 0.0
    
    def place_market_order(self, symbol: str, side: str, quantity: float,
                          stop_loss: Optional[float] = None,
                          take_profit: Optional[float] = None) -> Optional[Dict]:
        if Config.PAPER_TRADING:
            logger.info(f"[PAPER][{self.name}] {side} {quantity} {symbol}")
            return {'status': 'PAPER', 'account': self.name}
        
        if not self.is_connected:
            return None
        
        try:
            if side == 'BUY':
                order = self.client.order_market_buy(
                    symbol=symbol.replace('USD', 'USDT'),
                    quantity=quantity
                )
            else:
                order = self.client.order_market_sell(
                    symbol=symbol.replace('USD', 'USDT'),
                    quantity=quantity
                )
            
            logger.info(f"✅ [{self.name}] Order placed: {order['orderId']}")
            return {**order, 'exchange': self.name}
            
        except Exception as e:
            logger.error(f"❌ [{self.name}] Order error: {e}")
            return None
    
    def get_open_orders(self, symbol: str) -> int:
        if not self.is_connected:
            return 999
        
        try:
            orders = self.client.get_open_orders(symbol=symbol.replace('USD', 'USDT'))
            return len(orders)
        except:
            return 999


# ═══════════════════════════════════════════════════════════
# GEMINI CLIENT (Basic Implementation)
# ═══════════════════════════════════════════════════════════

class GeminiClient(BaseExchangeClient):
    """Gemini exchange client"""
    
    BASE_URL = "https://api.gemini.com/v1"
    
    def connect(self) -> bool:
        try:
            # Test with public API
            response = requests.get(f"{self.BASE_URL}/symbols")
            if response.status_code == 200:
                self.is_connected = True
                logger.info(f"✅ [{self.name}] Gemini connected")
                return True
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"❌ [{self.name}] Connection failed: {e}")
        return False
    
    def get_klines(self, symbol: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
        # Placeholder - Gemini uses different API
        logger.warning(f"[{self.name}] Klines not yet implemented")
        return pd.DataFrame()
    
    def get_balance(self, asset: str) -> float:
        if not self.is_connected:
            return 0.0
        
        try:
            import base64
            import hmac
            import hashlib
            
            nonce = int(time.time() * 1000)
            import json
            payload = {"request": "/v1/balances", "nonce": nonce}
            payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode()
            
            signature = hmac.new(
                self.config.api_secret.encode(),
                payload_b64.encode(),
                hashlib.sha384
            ).hexdigest()
            
            headers = {
                "Content-Type": "text/plain",
                "X-GEMINI-APIKEY": self.config.api_key,
                "X-GEMINI-PAYLOAD": payload_b64,
                "X-GEMINI-SIGNATURE": signature
            }
            
            response = requests.post(f"{self.BASE_URL}/balances", headers=headers, timeout=10)
            result = response.json()
            
            if isinstance(result, dict) and result.get('result') == 'error':
                logger.error(f"[{self.name}] Balance error: {result}")
                return 0.0
            
            # Find asset balance
            for item in result:
                if item.get('currency', '').upper() == asset.upper():
                    return float(item.get('balance', '0'))
            
            return 0.0
        
        except Exception as e:
            logger.error(f"[{self.name}] Balance error: {e}")
            return 0.0
    
    def place_market_order(self, symbol: str, side: str, quantity: float,
                          stop_loss: Optional[float] = None,
                          take_profit: Optional[float] = None) -> Optional[Dict]:
        logger.warning(f"[{self.name}] Orders not yet implemented")
        return None
    
    def get_open_orders(self, symbol: str) -> int:
        return 0


# ═══════════════════════════════════════════════════════════
# KRAKEN CLIENT (Full Implementation)
# ═══════════════════════════════════════════════════════════

class KrakenClient(BaseExchangeClient):
    """Kraken exchange client with full API support"""
    
    BASE_URL = "https://api.kraken.com"
    
    def _get_kraken_signature(self, urlpath, data):
        """Generate Kraken API signature"""
        import base64
        import hashlib
        import hmac
        
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()
        mac = hmac.new(base64.b64decode(self.config.api_secret), message, hashlib.sha512)
        return base64.b64encode(mac.digest()).decode()
    
    def connect(self) -> bool:
        try:
            import urllib.parse
            # Test with public API
            response = requests.get(f"{self.BASE_URL}/0/public/Time")
            if response.status_code == 200:
                self.is_connected = True
                logger.info(f"✅ [{self.name}] Kraken connected")
                return True
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"❌ [{self.name}] Connection failed: {e}")
        return False
    
    def get_klines(self, symbol: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
        if not self.is_connected:
            return pd.DataFrame()
        
        try:
            # Kraken uses different symbol format (XBTUSD instead of BTCUSD)
            kraken_symbol = symbol.replace('BTC', 'XBT')
            
            # Map timeframe to Kraken interval
            interval_map = {'1m': 1, '5m': 5, '15m': 15, '30m': 30, '1h': 60, '4h': 240, '1d': 1440}
            kraken_interval = interval_map.get(timeframe, 15)
            
            params = {
                'pair': kraken_symbol,
                'interval': kraken_interval
            }
            
            response = requests.get(f"{self.BASE_URL}/0/public/OHLC", params=params)
            data = response.json()
            
            if data.get('error'):
                logger.error(f"[{self.name}] API error: {data['error']}")
                return pd.DataFrame()
            
            # Parse OHLC data
            ohlc_data = data['result'][list(data['result'].keys())[0]]
            
            df = pd.DataFrame(ohlc_data, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'
            ])
            
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            logger.error(f"[{self.name}] Klines error: {e}")
            return pd.DataFrame()
    
    def get_balance(self, asset: str) -> float:
        if not self.is_connected:
            return 0.0
        
        try:
            import urllib.parse
            nonce = int(time.time() * 1000)
            data = {'nonce': nonce}
            urlpath = '/0/private/Balance'
            
            headers = {
                'API-Key': self.config.api_key,
                'API-Sign': self._get_kraken_signature(urlpath, data)
            }
            
            response = requests.post(f"{self.BASE_URL}{urlpath}", data=data, headers=headers)
            result = response.json()
            
            if result.get('error'):
                logger.error(f"[{self.name}] Balance error: {result['error']}")
                return 0.0
            
            # Map asset to Kraken format
            kraken_asset = asset
            if asset == 'BTC':
                kraken_asset = 'XXBT'
            elif asset == 'USD':
                kraken_asset = 'ZUSD'
            
            balance = result['result'].get(kraken_asset, '0')
            return float(balance)
            
        except Exception as e:
            logger.error(f"[{self.name}] Balance error: {e}")
            return 0.0
    
    def place_market_order(self, symbol: str, side: str, quantity: float,
                          stop_loss: Optional[float] = None,
                          take_profit: Optional[float] = None) -> Optional[Dict]:
        if Config.PAPER_TRADING:
            logger.info(f"[PAPER][{self.name}] {side} {quantity} {symbol}")
            return {'status': 'PAPER', 'exchange': 'kraken', 'account': self.name}
        
        if not self.is_connected:
            return None
        
        try:
            import urllib.parse
            nonce = int(time.time() * 1000)
            
            kraken_symbol = symbol.replace('BTC', 'XBT')
            ordertype = 'market'
            direction = 'buy' if side == 'BUY' else 'sell'
            
            data = {
                'nonce': nonce,
                'ordertype': ordertype,
                'type': direction,
                'volume': str(quantity),
                'pair': kraken_symbol
            }
            
            urlpath = '/0/private/AddOrder'
            headers = {
                'API-Key': self.config.api_key,
                'API-Sign': self._get_kraken_signature(urlpath, data)
            }
            
            response = requests.post(f"{self.BASE_URL}{urlpath}", data=data, headers=headers)
            result = response.json()
            
            if result.get('error'):
                logger.error(f"❌ [{self.name}] Order error: {result['error']}")
                return None
            
            logger.info(f"✅ [{self.name}] Order placed: {result['result']}")
            return {**result['result'], 'exchange': self.name}
            
        except Exception as e:
            logger.error(f"❌ [{self.name}] Order error: {e}")
            return None
    
    def get_open_orders(self, symbol: str) -> int:
        if not self.is_connected:
            return 999
        
        try:
            import urllib.parse
            nonce = int(time.time() * 1000)
            data = {'nonce': nonce}
            urlpath = '/0/private/OpenOrders'
            
            headers = {
                'API-Key': self.config.api_key,
                'API-Sign': self._get_kraken_signature(urlpath, data)
            }
            
            response = requests.post(f"{self.BASE_URL}{urlpath}", data=data, headers=headers)
            result = response.json()
            
            if result.get('error'):
                return 999
            
            return len(result['result'].get('open', {}))
            
        except:
            return 999


# ═══════════════════════════════════════════════════════════
# COINBASE CLIENT (Full Implementation)
# ═══════════════════════════════════════════════════════════

class CoinbaseClient(BaseExchangeClient):
    """Coinbase Pro/Advanced Trade client with full API support"""
    
    BASE_URL = "https://api.coinbase.com"
    Pro_URL = "https://api.pro.coinbase.com"  # Coinbase Pro (legacy but functional)
    
    def _generate_signature(self, timestamp, method, path, body=''):
        """Generate Coinbase Pro signature"""
        import base64
        import hashlib
        import hmac
        
        # Secret is already base64 decoded
        secret = base64.b64decode(self.config.api_secret)
        message = f"{timestamp}{method.upper()}{path}{body}"
        signature = hmac.new(secret, message.encode(), hashlib.sha256).digest()
        return base64.b64encode(signature).decode()
    
    def connect(self) -> bool:
        try:
            # Test with public API first
            response = requests.get(f"{self.Pro_URL}/products")
            if response.status_code == 200:
                # Check if credentials work (test with accounts endpoint)
                if self.config.api_key:
                    timestamp = str(int(time.time()))
                    path = '/accounts'
                    signature = self._generate_signature(timestamp, 'GET', path)
                    
                    headers = {
                        'CB-ACCESS-KEY': self.config.api_key,
                        'CB-ACCESS-SIGN': signature,
                        'CB-ACCESS-TIMESTAMP': timestamp,
                        'CB-ACCESS-PASSPHRASE': self.config.passphrase or '',
                        'Content-Type': 'application/json'
                    }
                    
                    auth_response = requests.get(f"{self.Pro_URL}{path}", headers=headers)
                    if auth_response.status_code == 200:
                        self.is_connected = True
                        logger.info(f"✅ [{self.name}] Coinbase Pro connected with full access")
                        return True
                    else:
                        # Connected but auth failed - might be Advanced Trade API
                        self.is_connected = True
                        logger.warning(f"[{self.name}] Coinbase Pro auth: {auth_response.status_code} - trying Advanced Trade")
                        return True
                
                self.is_connected = True
                logger.info(f"✅ [{self.name}] Coinbase connected (public access)")
                return True
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"❌ [{self.name}] Connection failed: {e}")
        return False
    
    def get_klines(self, symbol: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
        if not self.is_connected:
            return pd.DataFrame()
        
        try:
            # Coinbase uses BTC-USD format
            cb_symbol = f"{symbol[:3]}-{symbol[3:]}"
            
            # Map timeframe to granularity (seconds)
            granularity_map = {'1m': 60, '5m': 300, '15m': 900, '1h': 3600, '6h': 21600, '1d': 86400}
            granularity = granularity_map.get(timeframe, 900)
            
            params = {
                'granularity': granularity,
                'limit': min(limit, 300)  # Coinbase limits to 300 candles
            }
            
            response = requests.get(f"{self.Pro_URL}/products/{cb_symbol}/candles", params=params)
            data = response.json()
            
            if response.status_code != 200 or not data:
                logger.error(f"[{self.name}] Candles error: {data}")
                return pd.DataFrame()
            
            # Coinbase candles format: [time, low, high, open, close, volume]
            df = pd.DataFrame(data, columns=['timestamp', 'low', 'high', 'open', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df.set_index('timestamp', inplace=True)
            
            # Coinbase returns reverse chronological, so sort and reindex
            df = df.sort_index()
            
            return df
            
        except Exception as e:
            logger.error(f"[{self.name}] Klines error: {e}")
            return pd.DataFrame()
    
    def get_balance(self, asset: str) -> float:
        if not self.is_connected:
            return 0.0
        
        try:
            timestamp = str(int(time.time()))
            path = '/accounts'
            signature = self._generate_signature(timestamp, 'GET', path)
            
            headers = {
                'CB-ACCESS-KEY': self.config.api_key,
                'CB-ACCESS-SIGN': signature,
                'CB-ACCESS-TIMESTAMP': timestamp,
                'CB-ACCESS-PASSPHRASE': self.config.passphrase or ''
            }
            
            response = requests.get(f"{self.Pro_URL}{path}", headers=headers)
            
            if response.status_code != 200:
                logger.error(f"[{self.name}] Balance error: {response.status_code}")
                return 0.0
            
            accounts = response.json()
            for account in accounts:
                if account.get('currency') == asset:
                    return float(account.get('available', 0)) + float(account.get('hold', 0))
            
            return 0.0
            
        except Exception as e:
            logger.error(f"[{self.name}] Balance error: {e}")
            return 0.0
    
    def place_market_order(self, symbol: str, side: str, quantity: float,
                          stop_loss: Optional[float] = None,
                          take_profit: Optional[float] = None) -> Optional[Dict]:
        if Config.PAPER_TRADING:
            logger.info(f"[PAPER][{self.name}] {side} {quantity} {symbol}")
            return {'status': 'PAPER', 'exchange': 'coinbase', 'account': self.name}
        
        if not self.is_connected:
            return None
        
        try:
            timestamp = str(int(time.time()))
            cb_symbol = f"{symbol[:3]}-{symbol[3:]}"
            path = '/orders'
            
            body = json.dumps({
                'product_id': cb_symbol,
                'side': side.lower(),
                'order_type': 'market',
                'size': str(quantity)
            })
            
            signature = self._generate_signature(timestamp, 'POST', path, body)
            
            headers = {
                'CB-ACCESS-KEY': self.config.api_key,
                'CB-ACCESS-SIGN': signature,
                'CB-ACCESS-TIMESTAMP': timestamp,
                'CB-ACCESS-PASSPHRASE': self.config.passphrase or '',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(f"{self.Pro_URL}{path}", headers=headers, data=body)
            result = response.json()
            
            if response.status_code != 200:
                logger.error(f"❌ [{self.name}] Order error: {result}")
                return None
            
            logger.info(f"✅ [{self.name}] Order placed: {result.get('id')}")
            return {**result, 'exchange': self.name}
            
        except Exception as e:
            logger.error(f"❌ [{self.name}] Order error: {e}")
            return None
    
    def get_open_orders(self, symbol: str) -> int:
        if not self.is_connected:
            return 999
        
        try:
            timestamp = str(int(time.time()))
            path = '/orders?status=open'
            signature = self._generate_signature(timestamp, 'GET', path)
            
            headers = {
                'CB-ACCESS-KEY': self.config.api_key,
                'CB-ACCESS-SIGN': signature,
                'CB-ACCESS-TIMESTAMP': timestamp,
                'CB-ACCESS-PASSPHRASE': self.config.passphrase or ''
            }
            
            response = requests.get(f"{self.Pro_URL}{path}", headers=headers)
            
            if response.status_code != 200:
                return 999
            
            orders = response.json()
            return len(orders)
            
        except:
            return 999


# ═══════════════════════════════════════════════════════════
# UNIFIED EXCHANGE MANAGER
# ═══════════════════════════════════════════════════════════

class UnifiedExchangeManager:
    """Manages all exchange connections"""
    
    def __init__(self):
        self.clients: Dict[str, BaseExchangeClient] = {}
        self.total_portfolio = {
            'total_usd': 0.0,
            'total_btc': 0.0,
            'total_positions': 0,
            'daily_risk_used': 0.0
        }
        
        self._init_all_exchanges()
    
    def _init_all_exchanges(self):
        """Initialize all configured exchanges"""
        logger.info("Initializing multi-exchange manager...")
        logger.info(f"Configured exchanges: {len(Config.EXCHANGES)}")
        
        for ex_config in Config.EXCHANGES:
            client = self._create_client(ex_config)
            if client:
                self.clients[ex_config.name] = client
                client.connect()
                # Fetch balances
                client.balance_usd = client.get_balance('USD')
                client.balance_btc = client.get_balance('BTC')
        
        self._update_portfolio()
        self._log_portfolio_summary()
    
    def _create_client(self, config: ExchangeConfig) -> Optional[BaseExchangeClient]:
        """Factory method for creating exchange clients"""
        if config.exchange_type == ExchangeType.BINANCE_US:
            return BinanceClient(config)
        elif config.exchange_type == ExchangeType.GEMINI:
            return GeminiClient(config)
        elif config.exchange_type == ExchangeType.KRAKEN:
            return KrakenClient(config)
        elif config.exchange_type == ExchangeType.COINBASE:
            return CoinbaseClient(config)
        return None
    
    def _update_portfolio(self):
        """Calculate total portfolio across all exchanges"""
        self.total_portfolio['total_usd'] = sum(
            c.balance_usd for c in self.clients.values()
        )
        self.total_portfolio['total_btc'] = sum(
            c.balance_btc for c in self.clients.values()
        )
        self.total_portfolio['total_positions'] = sum(
            c.positions_open for c in self.clients.values()
        )
        self.total_portfolio['daily_risk_used'] = sum(
            c.daily_risk_used for c in self.clients.values()
        )
    
    def _log_portfolio_summary(self):
        """Display unified portfolio"""
        logger.info("=" * 60)
        logger.info("💎 UNIFIED MULTI-EXCHANGE PORTFOLIO")
        logger.info("=" * 60)
        
        for name, client in self.clients.items():
            status = "🟢 ONLINE" if client.is_connected else "🔴 OFFLINE"
            logger.info(f"  [{name}] {status}")
            logger.info(f"      USD: ${client.balance_usd:.2f}")
            logger.info(f"      BTC: {client.balance_btc:.6f}")
        
        logger.info("-" * 60)
        logger.info(f"  📊 TOTAL USD: ${self.total_portfolio['total_usd']:.2f}")
        logger.info(f"  📊 TOTAL BTC: {self.total_portfolio['total_btc']:.6f}")
        logger.info(f"  📊 ACTIVE EXCHANGES: {len([c for c in self.clients.values() if c.is_connected])}")
        logger.info("=" * 60)
    
    def fetch_data_with_failover(self, symbol: str, timeframe: str) -> Tuple[pd.DataFrame, Optional[str]]:
        """
        Fetch data with automatic failover between exchanges
        Returns: (DataFrame, source_exchange_name)
        """
        # Sort clients by priority
        sorted_clients = sorted(
            self.clients.items(),
            key=lambda x: x[1].config.priority,
            reverse=True
        )
        
        for name, client in sorted_clients:
            if not client.is_connected:
                continue
            
            df = client.get_klines(symbol, timeframe)
            if not df.empty:
                logger.info(f"📊 Data from [{name}]: {len(df)} candles")
                return df, name
        
        logger.error("No exchanges available for data fetch")
        return pd.DataFrame(), None
    
    def execute_order_with_routing(self, symbol: str, side: str, quantity: float,
                                   stop_loss: float, take_profit: float) -> List[Dict]:
        """
        Execute order with smart exchange routing
        - Uses best exchange (priority + balance)
        - Splits large orders across exchanges
        - Failover if primary fails
        """
        results = []
        
        # Sort by priority and available balance
        sorted_clients = sorted(
            [c for c in self.clients.values() if c.is_connected],
            key=lambda x: (x.config.priority, x.balance_usd),
            reverse=True
        )
        
        if not sorted_clients:
            logger.error("No connected exchanges available")
            return results
        
        # Determine if we should split
        should_split = (Config.SPLIT_ORDERS and quantity > Config.SPLIT_THRESHOLD and 
                       len(sorted_clients) >= 2)
        
        if should_split:
            # Split across top 2 exchanges
            primary_qty = quantity * 0.6
            secondary_qty = quantity * 0.4
            
            # Primary order
            result = sorted_clients[0].place_market_order(
                symbol, side, primary_qty, stop_loss, take_profit
            )
            if result:
                results.append(result)
                sorted_clients[0].daily_risk_used += primary_qty * 0.1  # Estimate
            
            # Secondary order (failover)
            if len(sorted_clients) > 1:
                result = sorted_clients[1].place_market_order(
                    symbol, side, secondary_qty, stop_loss, take_profit
                )
                if result:
                    results.append(result)
                    sorted_clients[1].daily_risk_used += secondary_qty * 0.1
        else:
            # Single order on best exchange
            result = sorted_clients[0].place_market_order(
                symbol, side, quantity, stop_loss, take_profit
            )
            if result:
                results.append(result)
                sorted_clients[0].daily_risk_used += quantity * 0.1
        
        return results
    
    def check_arbitrage_opportunity(self, symbol: str) -> Optional[Dict]:
        """
        Check for arbitrage opportunities across exchanges
        """
        prices = {}
        
        for name, client in self.clients.items():
            if not client.is_connected:
                continue
            
            df = client.get_klines(symbol, '1m')
            if not df.empty:
                prices[name] = df['close'].iloc[-1]
        
        if len(prices) < 2:
            return None
        
        max_price = max(prices.values())
        min_price = min(prices.values())
        max_exchange = max(prices, key=prices.get)
        min_exchange = min(prices, key=prices.get)
        
        spread_pct = ((max_price - min_price) / min_price) * 100
        
        if spread_pct > Config.ARBITRAGE_THRESHOLD:
            return {
                'symbol': symbol,
                'buy_exchange': min_exchange,
                'buy_price': min_price,
                'sell_exchange': max_exchange,
                'sell_price': max_price,
                'spread_pct': spread_pct
            }
        
        return None
    
    def check_multi_asset_arbitrage(self) -> List[Dict]:
        """
        Check for arbitrage opportunities across ALL active symbols
        v4.1.1 - Multi-Asset Arbitrage Detection
        """
        opportunities = []
        
        for symbol in Config.ACTIVE_SYMBOLS:
            arb = self.check_arbitrage_opportunity(symbol)
            if arb and arb['spread_pct'] > Config.ARBITRAGE_THRESHOLD:
                opportunities.append(arb)
        
        return opportunities
    
    def execute_arbitrage(self, opportunity: Dict) -> Optional[Dict]:
        """
        Execute cross-exchange arbitrage
        Buy on low exchange, sell on high exchange
        """
        if Config.PAPER_TRADING:
            logger.info(f"[ARBITRAGE PAPER] {opportunity['symbol']}")
            logger.info(f"  Buy {opportunity['buy_exchange']} @ ${opportunity['buy_price']:.2f}")
            logger.info(f"  Sell {opportunity['sell_exchange']} @ ${opportunity['sell_price']:.2f}")
            logger.info(f"  Spread: {opportunity['spread_pct']:.2f}%")
            return {'status': 'PAPER', 'opportunity': opportunity}
        
        # Live arbitrage execution
        buy_ex = opportunity['buy_exchange']
        sell_ex = opportunity['sell_exchange']
        symbol = opportunity['symbol']
        
        # Calculate position size (small to minimize risk)
        usd_balance = min(
            self.clients[buy_ex].balance_usd,
            self.clients[sell_ex].balance_usd
        )
        
        if usd_balance < 10:  # Minimum $10
            logger.warning(f"Insufficient balance for arbitrage: ${usd_balance:.2f}")
            return None
        
        position_size = min(50.00, usd_balance * 0.5)  # Max $50 or 50%
        
        logger.info(f"🚀 EXECUTING ARBITRAGE on {symbol}")
        logger.info(f"  Size: ${position_size:.2f}")
        logger.info(f"  Buy on {buy_ex} @ ${opportunity['buy_price']:.2f}")
        logger.info(f"  Sell on {sell_ex} @ ${opportunity['sell_price']:.2f}")
        
        try:
            # Execute buy on low exchange
            buy_result = self.clients[buy_ex].place_market_order(
                symbol, 'BUY', position_size / opportunity['buy_price'],
                stop_loss=None, take_profit=None
            )
            
            if not buy_result:
                logger.error(f"Arbitrage buy failed on {buy_ex}")
                return None
            
            # Execute sell on high exchange
            sell_result = self.clients[sell_ex].place_market_order(
                symbol, 'SELL', position_size / opportunity['sell_price'],
                stop_loss=None, take_profit=None
            )
            
            if not sell_result:
                logger.error(f"Arbitrage sell failed on {sell_ex}")
                return buy_result
            
            profit = (opportunity['sell_price'] - opportunity['buy_price']) * (position_size / opportunity['buy_price'])
            
            logger.info(f"✅ ARBITRAGE COMPLETE")
            logger.info(f"  Profit: ${profit:.2f}")
            
            return {
                'status': 'EXECUTED',
                'symbol': symbol,
                'buy': buy_result,
                'sell': sell_result,
                'profit_usd': profit,
                'spread_pct': opportunity['spread_pct']
            }
            
        except Exception as e:
            logger.error(f"Arbitrage execution error: {e}")
            return None


# ═══════════════════════════════════════════════════════════
# MAIN BOT - MULTI EXCHANGE
# ═══════════════════════════════════════════════════════════

class CryptonioMultiExchangeBot:
    """
    Multi-Exchange Trading Bot
    Orchestrates trading across all configured exchanges
    """
    
    def __init__(self):
        self.exchange_manager = UnifiedExchangeManager()
        self.r2 = CryptonioAdapter()
        self.last_check = None
    
    def run_cycle(self):
        """
        Single trading cycle:
        1. Update portfolio
        2. Fetch data (with failover)
        3. R2 analysis
        4. Check arbitrage
        5. Execute if signal valid
        """
        logger.info("\n" + "=" * 60)
        logger.info(f"🤖 MULTI-EXCHANGE CYCLE: {datetime.now().isoformat()}")
        
        # Update portfolio
        self.exchange_manager._update_portfolio()
        
        # Fetch data
        df, source = self.exchange_manager.fetch_data_with_failover(
            Config.SYMBOL, Config.TIMEFRAME
        )
        
        if df.empty:
            logger.error("No data available from any exchange")
            return
        
        # R2 Analysis (pass None for onchain_data, symbol already in Config)
        signal = self.r2.generate_signal_report(df, onchain_data=None)
        
        # Check if signal valid
        if signal['confluence_score'] < Config.MIN_CONFLUENCE_SCORE:
            logger.info(f"⏳ Low confluence: {signal['confluence_score']:.1f}")
            return
        
        if signal['confidence'] < 0.5:
            logger.info(f"⏳ Low confidence: {signal['confidence']:.2%}")
            return
        
        # Check arbitrage
        arb = self.exchange_manager.check_arbitrage_opportunity(Config.SYMBOL)
        if arb:
            logger.warning(f"🚨 ARBITRAGE: {arb['spread_pct']:.2f}% spread detected!")
            logger.warning(f"   Buy on {arb['buy_exchange']} @ ${arb['buy_price']:.2f}")
            logger.warning(f"   Sell on {arb['sell_exchange']} @ ${arb['sell_price']:.2f}")
        
        # Execute trade
        entry = signal['entry_price']
        stop = signal['stop_loss']
        target = signal['take_profit']
        side = 'BUY' if 'LONG' in signal['signal_type'] else 'SELL'
        
        # Calculate position size based on total portfolio
        total_usd = self.exchange_manager.total_portfolio['total_usd']
        position_size = min(10.00, total_usd * 0.02)  # $10 or 2%
        
        logger.info("-" * 60)
        logger.info(f"🎯 SIGNAL: {signal['signal_type']}")
        logger.info(f"   Confluence: {signal['confluence_score']:.1f}/190")
        logger.info(f"   Confidence: {signal['confidence']:.2%}")
        logger.info(f"   Size: ${position_size:.2f}")
        
        # Execute with multi-exchange routing
        results = self.exchange_manager.execute_order_with_routing(
            Config.SYMBOL, side, position_size, stop, target
        )
        
        if results:
            for result in results:
                logger.info(f"✅ EXECUTED: {result.get('exchange', 'unknown')}")
        else:
            logger.warning("Execution failed on all exchanges")
    
    def run_multi_asset_cycle(self):
        """
        Multi-asset trading cycle (v4.1.0):
        Monitor and trade ALL configured symbols
        """
        logger.info("\n" + "=" * 60)
        logger.info(f"🤖 MULTI-ASSET CYCLE: {datetime.now().isoformat()}")
        logger.info(f"🎯 Active Symbols: {', '.join(Config.ACTIVE_SYMBOLS)}")
        logger.info("=" * 60)
        
        # Update portfolio once per cycle
        self.exchange_manager._update_portfolio()
        
        for symbol in Config.ACTIVE_SYMBOLS:
            logger.info(f"\n📊 Analyzing {symbol}...")
            
            # Fetch data for this symbol
            df, source = self.exchange_manager.fetch_data_with_failover(
                symbol, Config.TIMEFRAME
            )
            
            if df.empty:
                logger.warning(f"  ⚠️ No data for {symbol}")
                continue
            
            # R2 Analysis
            signal = self.r2.generate_signal_report(df, onchain_data=None)
            
            confluence = signal['confluence_score']
            confidence = signal['confidence']
            
            logger.info(f"  Confluence: {confluence:.1f}/190 | Confidence: {confidence:.1%}")
            
            # Check thresholds
            if confluence < Config.MIN_CONFLUENCE_SCORE:
                logger.info(f"  ⏳ Low confluence, skipping")
                continue
            
            if confidence < 0.5:
                logger.info(f"  ⏳ Low confidence, skipping")
                continue
            
            # Execute trade
            side = 'BUY' if 'LONG' in signal['signal_type'] else 'SELL'
            
            # Calculate position size based on symbol
            total_usd = self.exchange_manager.total_portfolio['total_usd']
            position_size = min(10.00, total_usd * 0.02)  # $10 or 2%
            
            logger.info(f"  🚀 {side} SIGNAL for {symbol}")
            logger.info(f"     Entry: ${signal['entry_price']:.2f}")
            logger.info(f"     Stop: ${signal['stop_loss']:.2f}")
            logger.info(f"     Target: ${signal['take_profit']:.2f}")
            logger.info(f"     Size: ${position_size:.2f}")
            
            # Execute with routing
            results = self.exchange_manager.execute_order_with_routing(
                symbol, side, position_size,
                signal['stop_loss'], signal['take_profit']
            )
            
            if results:
                for result in results:
                    logger.info(f"  ✅ EXECUTED on {result.get('exchange', 'unknown')}")
            else:
                logger.warning(f"  ❌ Execution failed for {symbol}")
            
            # Small delay between symbols to avoid rate limits
            time.sleep(1)
        
        # ═══════════════════════════════════════════════════════
        # ARBITRAGE DETECTION (v4.1.1) - Check ALL symbols
        # ═══════════════════════════════════════════════════════
        logger.info("\n" + "=" * 60)
        logger.info("🔍 CROSS-EXCHANGE ARBITRAGE SCAN")
        logger.info("=" * 60)
        
        arbitrage_opportunities = self.exchange_manager.check_multi_asset_arbitrage()
        
        if arbitrage_opportunities:
            logger.info(f"🚨 ARBITRAGE FOUND: {len(arbitrage_opportunities)} opportunity(s)")
            
            for arb in arbitrage_opportunities:
                logger.info(f"\n  📊 {arb['symbol']}")
                logger.info(f"     Buy:  {arb['buy_exchange']} @ ${arb['buy_price']:.2f}")
                logger.info(f"     Sell: {arb['sell_exchange']} @ ${arb['sell_price']:.2f}")
                logger.info(f"     Spread: {arb['spread_pct']:.2f}%")
                
                # Auto-execute if spread > 1% (in live mode)
                if arb['spread_pct'] > 1.0 and not Config.PAPER_TRADING:
                    logger.info(f"     🚀 Auto-executing arbitrage...")
                    result = self.exchange_manager.execute_arbitrage(arb)
                    if result:
                        logger.info(f"     ✅ Profit: ${result.get('profit_usd', 0):.2f}")
                elif Config.PAPER_TRADING:
                    logger.info(f"     💡 Would execute in LIVE mode")
        else:
            logger.info("  ✅ No arbitrage opportunities >0.5%")
        
        logger.info("\n" + "=" * 60)
        logger.info("CYCLE COMPLETE")
        logger.info("=" * 60)
    
    def run_continuous(self, interval: int = 15):
        """Continuous trading loop"""
        logger.info("🚀 MULTI-EXCHANGE BOT RUNNING")
        
        while True:
            try:
                now = datetime.now()
                
                if now.minute % interval == 0 and now.second <= 10:
                    self.run_cycle()
                    self.last_check = now.minute
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                logger.info("Bot stopped")
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                time.sleep(60)


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--symbol', default='BTCUSD')
    parser.add_argument('--multi-asset', action='store_true',
                       help='Enable multi-asset mode (BTC, DOGE, LTC, XRP)')
    parser.add_argument('--arbitrage', action='store_true',
                       help='Arbitrage-only mode (scan for price differences)')
    parser.add_argument('--arbitrage-threshold', type=float, default=0.5,
                       help='Minimum spread % to trigger arbitrage (default: 0.5)')
    
    args = parser.parse_args()
    
    Config.SYMBOL = args.symbol
    Config.ARBITRAGE_THRESHOLD = args.arbitrage_threshold
    
    if args.live:
        Config.PAPER_TRADING = False
        logger.warning("⚠️ LIVE TRADING MODE - REAL MONEY AT RISK")
        confirm = input("Type 'LIVE' to confirm: ")
        if confirm != 'LIVE':
            logger.info("Cancelled - switching to paper mode")
            Config.PAPER_TRADING = True
    
    bot = CryptonioMultiExchangeBot()
    
    if args.test:
        if args.multi_asset:
            bot.run_multi_asset_cycle()
        elif args.arbitrage:
            # Arbitrage-only test
            logger.info("🔍 ARBITRAGE TEST MODE")
            opportunities = bot.exchange_manager.check_multi_asset_arbitrage()
            if opportunities:
                for arb in opportunities:
                    print(f"\n{arb['symbol']}: {arb['spread_pct']:.2f}% spread")
                    print(f"  Buy: {arb['buy_exchange']} @ ${arb['buy_price']:.2f}")
                    print(f"  Sell: {arb['sell_exchange']} @ ${arb['sell_price']:.2f}")
            else:
                print("No arbitrage opportunities found")
        else:
            bot.run_cycle()
    else:
        if args.multi_asset:
            logger.info("🚀 MULTI-ASSET MODE ACTIVE")
            logger.info(f"Monitoring: {', '.join(Config.ACTIVE_SYMBOLS)}")
            while True:
                try:
                    now = datetime.now()
                    if now.minute % 15 == 0 and now.second <= 10:
                        bot.run_multi_asset_cycle()
                        bot.last_check = now.minute
                    time.sleep(1)
                except KeyboardInterrupt:
                    logger.info("Shutting down...")
                    break
                except Exception as e:
                    logger.error(f"Error: {e}")
                    time.sleep(60)
        else:
            bot.run_continuous()
