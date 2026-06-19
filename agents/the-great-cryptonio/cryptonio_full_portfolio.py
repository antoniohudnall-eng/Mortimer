#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRYPTONIO UNIFIED EXCHANGE MANAGER
Multi-Asset Trading Bot with ALL Holdings Tracking
Version: 4.2.0 (FULL PORTFOLIO TRACKING)

Features:
- Automatic discovery of ALL holdings across exchanges
- Dynamic symbol monitoring based on actual balances
- Unified portfolio view of all cryptocurrencies
- Cross-exchange arbitrage detection for all supported pairs
- Full asset tracking (22+ assets on Kraken alone)

Total Portfolio: ~$1,000+ across all exchanges

Author: Mortimer for Captain
Version: 4.2.0 (Full Portfolio)
"""

import os
import sys
import json
import time
import logging
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, List, Any, Set
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
    name: str
    api_key: str
    api_secret: str
    passphrase: Optional[str] = None
    sandbox: bool = True
    is_active: bool = False
    priority: int = 1
    max_daily_risk: float = 10.0
    max_positions: int = 1
    min_order_size: float = 10.0


class Config:
    """Master configuration for all exchanges"""
    
    # Populate EXCHANGES from environment
    EXCHANGES = []
    
    if os.getenv('BINANCE_US_API_KEY'):
        EXCHANGES.append(ExchangeConfig(
            exchange_type=ExchangeType.BINANCE_US,
            name="binance_us_primary",
            api_key=os.getenv('BINANCE_US_API_KEY', ''),
            api_secret=os.getenv('BINANCE_US_API_SECRET', ''),
            priority=4, is_active=True
        ))
    
    if os.getenv('BINANCE_US_API_KEY_2'):
        EXCHANGES.append(ExchangeConfig(
            exchange_type=ExchangeType.BINANCE_US,
            name="binance_us_secondary",
            api_key=os.getenv('BINANCE_US_API_KEY_2', ''),
            api_secret=os.getenv('BINANCE_US_API_SECRET_2', ''),
            priority=3, is_active=True
        ))
    
    if os.getenv('GEMINI_API_KEY'):
        EXCHANGES.append(ExchangeConfig(
            exchange_type=ExchangeType.GEMINI,
            name="gemini_main",
            api_key=os.getenv('GEMINI_API_KEY', ''),
            api_secret=os.getenv('GEMINI_API_SECRET', ''),
            priority=2, is_active=True
        ))
    
    if os.getenv('KRAKEN_API_KEY'):
        EXCHANGES.append(ExchangeConfig(
            exchange_type=ExchangeType.KRAKEN,
            name="kraken_main",
            api_key=os.getenv('KRAKEN_API_KEY', ''),
            api_secret=os.getenv('KRAKEN_API_SECRET', ''),
            priority=2, is_active=True
        ))
    
    if os.getenv('COINBASE_API_KEY'):
        EXCHANGES.append(ExchangeConfig(
            exchange_type=ExchangeType.COINBASE,
            name="coinbase_main",
            api_key=os.getenv('COINBASE_API_KEY', ''),
            api_secret=os.getenv('COINBASE_API_SECRET', ''),
            passphrase=os.getenv('COINBASE_PASSPHRASE', ''),
            priority=2, is_active=True
        ))
    
    # GLOBAL SETTINGS
    TIMEFRAME = '15m'
    
    # ═══════════════════════════════════════════════════════
    # DYNAMIC SYMBOLS (replaced at runtime with actual holdings)
    # ═══════════════════════════════════════════════════════
    ACTIVE_SYMBOLS: List[str] = ['BTCUSD']  # Will be populated dynamically
    
    # BASE symbols to always monitor (high priority)
    BASE_SYMBOLS = ['BTCUSD', 'ETHUSD', 'LTCUSD', 'XRPUSD']
    
    PAPER_TRADING = True  # Set to False for live trading
    
    # Risk Management
    TOTAL_MAX_DAILY_RISK = 50.00
    MIN_CONFLUENCE_SCORE = 60
    RISK_REWARD_RATIO = 1.5
    
    # Arbitrage
    ARBITRAGE_THRESHOLD = 0.5
    
    # Asset price sources (for USD conversion in portfolio)
    ASSET_PRICE_MAP = {
        'BTC': 'BTCUSD', 'ETH': 'ETHUSD', 'LTC': 'LTCUSD', 'XRP': 'XRPUSD',
        'DOGE': 'DOGEUSD', 'ADA': 'ADAUSD', 'SOL': 'SOLUSD', 'AVAX': 'AVAXUSD',
        'LINK': 'LINKUSD', 'UNI': 'UNIUSD', 'AAVE': 'AAVEUSD', 'BCH': 'BCHUSD',
        'POL': 'POLUSD', 'ANKR': 'ANKRUSD', 'TRX': 'TRXUSD', 'XMR': 'XMRUSD',
        'LRC': 'LRCUSD', 'BABY': None, 'NVDA': None  # Some assets have no USD pair
    }
    
    # Kraken asset mapping (internal code -> standard code)
    KRAKEN_ASSET_MAP = {
        'XXBT': 'BTC', 'XBT': 'BTC', 'ZUSD': 'USD', 'ZEUR': 'EUR',
        'XETH': 'ETH', 'XLTC': 'LTC', 'XXRP': 'XRP', 'XADA': 'ADA',
        'XXMR': 'XMR', 'XAVAX': 'AVAX', 'XSOL': 'SOL', 'XLINK': 'LINK',
        'XUNI': 'UNI', 'BCH': 'BCH', 'AAVE': 'AAVE', 'TRX': 'TRX',
        'ANKR': 'ANKR', 'POL': 'POL', 'LRC': 'LRC'
    }
    
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
# ABSTRACT EXCHANGE CLIENT
# ═══════════════════════════════════════════════════════════

class BaseExchangeClient(ABC):
    """Abstract base class for all exchange clients with full balance support"""
    
    def __init__(self, config: ExchangeConfig):
        self.config = config
        self.name = config.name
        self.exchange_type = config.exchange_type
        self.client = None
        self.is_connected = False
        self.last_error = None
        
        # Enhanced balance tracking
        self.balance_usd = 0.0
        self.balance_btc = 0.0
        self.balances = {}  # All assets: {asset: amount}
        self.positions_open = 0
        self.daily_risk_used = 0.0
        
    @abstractmethod
    def connect(self) -> bool:
        pass
    
    @abstractmethod
    def get_klines(self, symbol: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def get_balance(self, asset: str) -> float:
        pass
    
    @abstractmethod
    def get_all_balances(self) -> Dict[str, float]:
        """Get ALL balances, not just USD/BTC"""
        pass
    
    @abstractmethod
    def place_market_order(self, symbol: str, side: str, quantity: float,
                          stop_loss: Optional[float] = None,
                          take_profit: Optional[float] = None) -> Optional[Dict]:
        pass
    
    @abstractmethod
    def get_open_orders(self, symbol: str) -> int:
        pass
    
    @abstractmethod
    def get_available_symbols(self) -> List[str]:
        """Get list of available trading pairs"""
        pass


# ═══════════════════════════════════════════════════════════
# BINANCE.US CLIENT (Full Balance Support)
# ═══════════════════════════════════════════════════════════

class BinanceClient(BaseExchangeClient):
    """Binance.US exchange client with full asset tracking"""
    
    def connect(self) -> bool:
        try:
            from binance.client import Client
            self.client = Client(
                self.config.api_key,
                self.config.api_secret,
                tld='us'
            )
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
            binance_timeframe = timeframe.replace('m', 'm').replace('h', 'h')
            klines = self.client.get_klines(
                symbol=symbol.replace('USD', 'USDT'),
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
                    return float(balance['free']) + float(balance['locked'])
            return 0.0
        except Exception as e:
            logger.error(f"[{self.name}] Balance error: {e}")
            return 0.0
    
    def get_all_balances(self) -> Dict[str, float]:
        """Get all balances from Binance"""
        if not self.is_connected:
            return {}
        try:
            account = self.client.get_account()
            balances = {}
            for balance in account['balances']:
                total = float(balance['free']) + float(balance['locked'])
                if total > 0:
                    balances[balance['asset']] = total
            return balances
        except Exception as e:
            logger.error(f"[{self.name}] All balances error: {e}")
            return {}
    
    def get_available_symbols(self) -> List[str]:
        """Get available trading pairs"""
        if not self.is_connected:
            return []
        try:
            exchange_info = self.client.get_exchange_info()
            symbols = []
            for s in exchange_info['symbols']:
                if s['status'] == 'TRADING' and s['quoteAsset'] == 'USD':
                    symbols.append(s['symbol'])
            return symbols
        except:
            return []
    
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
# GEMINI CLIENT
# ═══════════════════════════════════════════════════════════

class GeminiClient(BaseExchangeClient):
    """Gemini exchange client"""
    
    BASE_URL = "https://api.gemini.com/v1"
    
    def connect(self) -> bool:
        try:
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
        logger.warning(f"[{self.name}] Klines not yet implemented")
        return pd.DataFrame()
    
    def get_balance(self, asset: str) -> float:
        logger.warning(f"[{self.name}] Balance fetch not yet implemented")
        return 0.0
    
    def get_all_balances(self) -> Dict[str, float]:
        logger.warning(f"[{self.name}] All balances not yet implemented")
        return {}
    
    def get_available_symbols(self) -> List[str]:
        return []
    
    def place_market_order(self, symbol: str, side: str, quantity: float,
                          stop_loss: Optional[float] = None,
                          take_profit: Optional[float] = None) -> Optional[Dict]:
        logger.warning(f"[{self.name}] Orders not yet implemented")
        return None
    
    def get_open_orders(self, symbol: str) -> int:
        return 0


# ═══════════════════════════════════════════════════════════
# KRAKEN CLIENT (Full Balance Support)
# ═══════════════════════════════════════════════════════════

class KrakenClient(BaseExchangeClient):
    """Kraken exchange client with full asset discovery"""
    
    BASE_URL = "https://api.kraken.com"
    
    def _get_kraken_signature(self, urlpath, data):
        import base64, hashlib, hmac
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()
        mac = hmac.new(base64.b64decode(self.config.api_secret), message, hashlib.sha512)
        return base64.b64encode(mac.digest()).decode()
    
    def connect(self) -> bool:
        try:
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
            kraken_symbol = symbol.replace('BTC', 'XBT')
            interval_map = {'1m': 1, '5m': 5, '15m': 15, '30m': 30, '1h': 60, '4h': 240, '1d': 1440}
            kraken_interval = interval_map.get(timeframe, 15)
            
            params = {'pair': kraken_symbol, 'interval': kraken_interval}
            response = requests.get(f"{self.BASE_URL}/0/public/OHLC", params=params)
            data = response.json()
            
            if data.get('error'):
                logger.error(f"[{self.name}] API error: {data['error']}")
                return pd.DataFrame()
            
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
    
    def get_all_balances(self) -> Dict[str, float]:
        """Get all Kraken balances (includes 22+ assets discovered today)"""
        if not self.is_connected:
            return {}
        try:
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
                logger.error(f"[{self.name}] All balances error: {result['error']}")
                return {}
            
            # Map Kraken asset codes to standard codes
            balances = {}
            for kraken_code, amount in result['result'].items():
                bal = float(amount)
                if bal > 0:
                    # Map to standard asset code
                    asset = Config.KRAKEN_ASSET_MAP.get(kraken_code, kraken_code)
                    if asset not in balances:
                        balances[asset] = 0.0
                    balances[asset] += bal
            
            return balances
        except Exception as e:
            logger.error(f"[{self.name}] All balances error: {e}")
            return {}
    
    def get_available_symbols(self) -> List[str]:
        """Get available Kraken trading pairs"""
        try:
            response = requests.get(f"{self.BASE_URL}/0/public/AssetPairs")
            data = response.json()
            if data.get('error'):
                return []
            symbols = []
            for pair, info in data['result'].items():
                if pair.endswith('USD'):
                    symbols.append(pair)
            return symbols
        except:
            return []
    
    def place_market_order(self, symbol: str, side: str, quantity: float,
                          stop_loss: Optional[float] = None,
                          take_profit: Optional[float] = None) -> Optional[Dict]:
        if Config.PAPER_TRADING:
            logger.info(f"[PAPER][{self.name}] {side} {quantity} {symbol}")
            return {'status': 'PAPER', 'exchange': 'kraken', 'account': self.name}
        
        if not self.is_connected:
            return None
        
        try:
            nonce = int(time.time() * 1000)
            kraken_symbol = symbol.replace('BTC', 'XBT')
            direction = 'buy' if side == 'BUY' else 'sell'
            
            data = {
                'nonce': nonce,
                'ordertype': 'market',
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
            
            logger.info(f"✅ [{self.name}] Order placed")
            return {**result['result'], 'exchange': self.name}
        except Exception as e:
            logger.error(f"❌ [{self.name}] Order error: {e}")
            return None
    
    def get_open_orders(self, symbol: str) -> int:
        if not self.is_connected:
            return 999
        try:
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
# COINBASE CLIENT
# ═══════════════════════════════════════════════════════════

class CoinbaseClient(BaseExchangeClient):
    """Coinbase Pro client"""
    
    BASE_URL = "https://api.coinbase.com"
    Pro_URL = "https://api.pro.coinbase.com"
    
    def _generate_signature(self, timestamp, method, path, body=''):
        import base64, hashlib, hmac
        secret = base64.b64decode(self.config.api_secret)
        message = f"{timestamp}{method.upper()}{path}{body}"
        signature = hmac.new(secret, message.encode(), hashlib.sha256).digest()
        return base64.b64encode(signature).decode()
    
    def connect(self) -> bool:
        try:
            response = requests.get(f"{self.Pro_URL}/products")
            if response.status_code == 200:
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
                        logger.info(f"✅ [{self.name}] Coinbase connected")
                        return True
                self.is_connected = True
                logger.info(f"✅ [{self.name}] Coinbase connected (public)")
                return True
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"❌ [{self.name}] Connection failed: {e}")
        return False
    
    def get_klines(self, symbol: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
        if not self.is_connected:
            return pd.DataFrame()
        try:
            cb_symbol = f"{symbol[:3]}-{symbol[3:]}"
            granularity_map = {'1m': 60, '5m': 300, '15m': 900, '1h': 3600, '6h': 21600, '1d': 86400}
            granularity = granularity_map.get(timeframe, 900)
            
            params = {'granularity': granularity, 'limit': min(limit, 300)}
            response = requests.get(f"{self.Pro_URL}/products/{cb_symbol}/candles", params=params)
            data = response.json()
            
            if response.status_code != 200 or not data:
                return pd.DataFrame()
            
            df = pd.DataFrame(data, columns=['timestamp', 'low', 'high', 'open', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
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
                return 0.0
            
            accounts = response.json()
            for account in accounts:
                if account.get('currency') == asset:
                    return float(account.get('available', 0)) + float(account.get('hold', 0))
            return 0.0
        except Exception as e:
            logger.error(f"[{self.name}] Balance error: {e}")
            return 0.0
    
    def get_all_balances(self) -> Dict[str, float]:
        """Get all Coinbase balances"""
        if not self.is_connected:
            return {}
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
                return {}
            
            balances = {}
            accounts = response.json()
            for account in accounts:
                asset = account.get('currency')
                total = float(account.get('available', 0)) + float(account.get('hold', 0))
                if total > 0:
                    balances[asset] = total
            return balances
        except Exception as e:
            logger.error(f"[{self.name}] All balances error: {e}")
            return {}
    
    def get_available_symbols(self) -> List[str]:
        """Get available Coinbase pairs"""
        try:
            response = requests.get(f"{self.Pro_URL}/products")
            products = response.json()
            symbols = []
            for p in products:
                if p['quote_currency'] == 'USD' and p['status'] == 'online':
                    symbols.append(f"{p['base_currency']}{p['quote_currency']}")
            return symbols
        except:
            return []
    
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
            
            if 'message' in result:
                logger.error(f"❌ [{self.name}] Order error: {result['message']}")
                return None
            
            logger.info(f"✅ [{self.name}] Order placed")
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
            return len(response.json())
        except:
            return 999


# ═══════════════════════════════════════════════════════════
# UNIFIED EXCHANGE MANAGER (Full Portfolio Tracking)
# ═══════════════════════════════════════════════════════════

class UnifiedExchangeManager:
    """
    Manages all exchanges with COMPLETE portfolio tracking
    Discovers and monitors ALL holdings across ALL exchanges
    """
    
    def __init__(self):
        self.clients: Dict[str, BaseExchangeClient] = {}
        self.total_portfolio = {
            'total_usd': 0.0,
            'total_btc': 0.0,
            'all_balances': {},  # {exchange: {asset: amount}}
            'consolidated': {},  # {asset: total_amount}
            'estimated_values': {}  # {asset: usd_value}
        }
        self.discovered_symbols: Set[str] = set()
        self._initialize_exchanges()
    
    def _initialize_exchanges(self):
        """Initialize all configured exchanges"""
        logger.info("Initializing multi-exchange manager...")
        logger.info(f"Configured exchanges: {len(Config.EXCHANGES)}")
        
        for config in Config.EXCHANGES:
            if config.exchange_type == ExchangeType.BINANCE_US:
                client = BinanceClient(config)
            elif config.exchange_type == ExchangeType.GEMINI:
                client = GeminiClient(config)
            elif config.exchange_type == ExchangeType.KRAKEN:
                client = KrakenClient(config)
            elif config.exchange_type == ExchangeType.COINBASE:
                client = CoinbaseClient(config)
            else:
                continue
            
            if client.connect():
                self.clients[config.name] = client
    
    def discover_all_holdings(self) -> Dict[str, float]:
        """
        DISCOVER ALL ASSETS across ALL exchanges
        Returns consolidated view of all holdings
        """
        logger.info("\n" + "=" * 60)
        logger.info("🔍 DISCOVERING ALL HOLDINGS ACROSS EXCHANGES")
        logger.info("=" * 60)
        
        all_balances = {}
        consolidated = {}
        total_usd_estimate = 0.0
        
        for name, client in self.clients.items():
            logger.info(f"\n📊 Scanning {name}...")
            
            balances = client.get_all_balances()
            all_balances[name] = balances
            
            if balances:
                logger.info(f"  Found {len(balances)} assets:")
                for asset, amount in sorted(balances.items(), key=lambda x: x[1], reverse=True)[:15]:
                    logger.info(f"    {asset:6s}: {amount:15.8f}")
                    
                    # Add to consolidated
                    if asset not in consolidated:
                        consolidated[asset] = 0.0
                    consolidated[asset] += amount
            else:
                logger.info("  No balances found")
        
        # Calculate USD values where possible
        logger.info("\n💰 CALCULATING PORTFOLIO VALUE...")
        estimated_values = {}
        
        # Try to get prices from first available exchange
        price_data = {}
        for symbol in Config.ASSET_PRICE_MAP.values():
            if symbol and symbol not in price_data:
                for name, client in self.clients.items():
                    df = client.get_klines(symbol, '1m', limit=1)
                    if not df.empty:
                        price_data[symbol] = df['close'].iloc[-1]
                        break
        
        for asset, total in consolidated.items():
            pair = Config.ASSET_PRICE_MAP.get(asset)
            if pair and pair in price_data:
                value = total * price_data[pair]
                estimated_values[asset] = value
                total_usd_estimate += value
                logger.info(f"  {asset:6s}: {total:12.6f} × ${price_data[pair]:,.2f} = ${value:,.2f}")
            elif asset in ['USD', 'USDT', 'USDC']:
                estimated_values[asset] = total
                total_usd_estimate += total
                logger.info(f"  {asset:6s}: ${total:,.2f} (cash)")
            else:
                logger.info(f"  {asset:6s}: {total:12.6f} (no USD price available)")
        
        # Update portfolio
        self.total_portfolio['all_balances'] = all_balances
        self.total_portfolio['consolidated'] = consolidated
        self.total_portfolio['estimated_values'] = estimated_values
        self.total_portfolio['total_usd'] = total_usd_estimate
        
        # Calculate BTC equivalent
        if 'BTCUSD' in price_data:
            self.total_portfolio['total_btc'] = total_usd_estimate / price_data['BTCUSD']
        
        logger.info("\n" + "=" * 60)
        logger.info(f"💎 TOTAL ESTIMATED VALUE: ${total_usd_estimate:,.2f}")
        logger.info(f"   ≈ {self.total_portfolio['total_btc']:.6f} BTC")
        logger.info(f"   {len(consolidated)} unique assets across {len(self.clients)} exchanges")
        logger.info("=" * 60)
        
        return consolidated
    
    def update_active_symbols(self):
        """Update ACTIVE_SYMBOLS based on actual holdings"""
        logger.info("\n🔄 UPDATING ACTIVE SYMBOLS FROM HOLDINGS...")
        
        # Always include base symbols
        active = set(Config.BASE_SYMBOLS)
        
        # Add symbols for assets we actually hold
        for asset in self.total_portfolio['consolidated'].keys():
            if asset in ['USD', 'EUR', 'GBP']:  # Skip fiat
                continue
            symbol = f"{asset}USD"
            # Check if any exchange supports this pair
            for name, client in self.clients.items():
                df = client.get_klines(symbol, '1m', limit=1)
                if not df.empty:
                    active.add(symbol)
                    self.discovered_symbols.add(symbol)
                    break
        
        Config.ACTIVE_SYMBOLS = sorted(list(active))
        logger.info(f"✅ Now monitoring {len(Config.ACTIVE_SYMBOLS)} symbols:")
        logger.info(f"   {', '.join(Config.ACTIVE_SYMBOLS)}")
        
        return Config.ACTIVE_SYMBOLS
    
    def _update_portfolio(self):
        """Update standard portfolio (USD + BTC only)"""
        total_usd = 0.0
        total_btc = 0.0
        
        for name, client in self.clients.items():
            client.balance_usd = client.get_balance('USD')
            client.balance_btc = client.get_balance('BTC')
            total_usd += client.balance_usd
            total_btc += client.balance_btc
        
        self.total_portfolio['total_usd'] = total_usd
        self.total_portfolio['total_btc'] = total_btc
    
    def print_full_portfolio(self):
        """Print complete portfolio breakdown"""
        print("\n" + "=" * 70)
        print("💎 COMPLETE PORTFOLIO ACROSS ALL EXCHANGES")
        print("=" * 70)
        
        for exchange, balances in self.total_portfolio['all_balances'].items():
            if balances:
                print(f"\n📊 {exchange.upper()}:")
                for asset, amount in sorted(balances.items(), key=lambda x: x[1], reverse=True):
                    if amount > 0:
                        print(f"   {asset:8s}: {amount:15.8f}")
        
        print("\n" + "-" * 70)
        print("📈 CONSOLIDATED HOLDINGS:")
        for asset, total in sorted(self.total_portfolio['consolidated'].items(), 
                                    key=lambda x: x[1], reverse=True):
            if total > 0:
                value = self.total_portfolio['estimated_values'].get(asset, 0)
                if value > 0:
                    print(f"   {asset:8s}: {total:15.8f} (${value:,.2f})")
                else:
                    print(f"   {asset:8s}: {total:15.8f}")
        
        print("-" * 70)
        print(f"💰 TOTAL VALUE: ${self.total_portfolio['total_usd']:,.2f}")
        print("=" * 70)
    
    def fetch_data_with_failover(self, symbol: str, timeframe: str) -> Tuple[pd.DataFrame, str]:
        """Fetch data with exchange failover"""
        sorted_clients = sorted(
            self.clients.items(),
            key=lambda x: Config.EXCHANGES[[e.name for e in Config.EXCHANGES].index(x[0])].priority if x[0] in [e.name for e in Config.EXCHANGES] else 99
        )
        
        for name, client in sorted_clients:
            df = client.get_klines(symbol, timeframe)
            if not df.empty:
                return df, name
        
        return pd.DataFrame(), "none"
    
    def check_arbitrage_opportunity(self, symbol: str) -> Optional[Dict]:
        """Check for arbitrage across exchanges"""
        prices = {}
        
        for name, client in self.clients.items():
            if not client.is_connected:
                continue
            df = client.get_klines(symbol, '1m', limit=1)
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
    
    def check_all_arbitrage(self) -> List[Dict]:
        """Check arbitrage for ALL active symbols"""
        opportunities = []
        for symbol in Config.ACTIVE_SYMBOLS:
            arb = self.check_arbitrage_opportunity(symbol)
            if arb and arb['spread_pct'] > Config.ARBITRAGE_THRESHOLD:
                opportunities.append(arb)
        return opportunities


# ═══════════════════════════════════════════════════════════
# MAIN BOT - FULL PORTFOLIO MODE
# ═══════════════════════════════════════════════════════════

class CryptonioFullPortfolioBot:
    """
    Bot that tracks ALL holdings across ALL exchanges
    Monitors all held assets for trading opportunities
    """
    
    def __init__(self):
        self.exchange_manager = UnifiedExchangeManager()
        self.r2 = CryptonioAdapter()
        self.last_check = None
    
    def initialize(self):
        """Discover all holdings and setup monitoring"""
        logger.info("\n" + "=" * 70)
        logger.info("🚀 CRYPTONIO FULL PORTFOLIO BOT v4.2.0")
        logger.info("=" * 70)
        
        # Step 1: Discover all holdings
        self.exchange_manager.discover_all_holdings()
        
        # Step 2: Update symbols based on holdings
        self.exchange_manager.update_active_symbols()
        
        # Step 3: Print full portfolio
        self.exchange_manager.print_full_portfolio()
        
        logger.info("\n✅ Bot initialized and monitoring ALL holdings")
        logger.info(f"   Active symbols: {len(Config.ACTIVE_SYMBOLS)}")
        logger.info(f"   Exchanges: {len(self.exchange_manager.clients)}")
        logger.info("=" * 70)
    
    def run_full_cycle(self):
        """Run trading cycle across ALL monitored symbols"""
        logger.info("\n" + "=" * 70)
        logger.info(f"🤖 FULL PORTFOLIO CYCLE: {datetime.now().isoformat()}")
        logger.info("=" * 70)
        
        # Refresh holdings
        self.exchange_manager.discover_all_holdings()
        
        for symbol in Config.ACTIVE_SYMBOLS:
            logger.info(f"\n📊 Analyzing {symbol}...")
            
            try:
                df, source = self.exchange_manager.fetch_data_with_failover(symbol, Config.TIMEFRAME)
                
                if df.empty:
                    logger.warning(f"  ⚠️ No data for {symbol}")
                    continue
                
                # R2 Analysis
                signal = self.r2.generate_signal_report(df, onchain_data=None)
                
                confluence = signal['confluence_score']
                confidence = signal['confidence']
                
                logger.info(f"  Confluence: {confluence:.1f}/190 | Confidence: {confidence:.1%}")
                
                if confluence >= Config.MIN_CONFLUENCE_SCORE and confidence >= 0.5:
                    logger.info(f"  🚀 SIGNAL: {signal['signal_type']} for {symbol}")
                    
                    # Check arbitrage as well
                    arb = self.exchange_manager.check_arbitrage_opportunity(symbol)
                    if arb:
                        logger.info(f"  💰 Arbitrage: {arb['spread_pct']:.2f}% spread")
                
                # Arbitrage check independent of signal
                arb = self.exchange_manager.check_arbitrage_opportunity(symbol)
                if arb and arb['spread_pct'] > 1.0:  # Alert on >1% spreads
                    logger.warning(f"  🚨 ARBITRAGE: {arb['spread_pct']:.2f}% spread!")
                    logger.warning(f"     Buy: {arb['buy_exchange']} @ ${arb['buy_price']:.2f}")
                    logger.warning(f"     Sell: {arb['sell_exchange']} @ ${arb['sell_price']:.2f}")
                
            except Exception as e:
                logger.error(f"  ❌ Error analyzing {symbol}: {e}")
        
        logger.info("\n" + "=" * 70)
        logger.info("✅ Cycle complete")
        logger.info("=" * 70)


# ═══════════════════════════════════════════════════════════
# RUNNER
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Cryptonio Full Portfolio Bot")
    parser.add_argument('--discover', action='store_true',
                       help='Discover all holdings and exit')
    parser.add_argument('--live', action='store_true',
                       help='Enable live trading (not paper)')
    parser.add_argument('--cycle', action='store_true',
                       help='Run one trading cycle')
    
    args = parser.parse_args()
    
    if args.live:
        Config.PAPER_TRADING = False
        logger.warning("🔴 LIVE TRADING ENABLED - Real orders will be placed!")
    
    bot = CryptonioFullPortfolioBot()
    
    if args.discover:
        bot.initialize()
    elif args.cycle:
        bot.initialize()
        bot.run_full_cycle()
    else:
        bot.initialize()
        logger.info("\nBot initialized. Use --cycle to run a trading cycle.")
