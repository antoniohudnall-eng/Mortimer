#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRYPTONIO PRODUCTION TRADING BOT - DUAL BINANCE EDITION
Based on: Video 21 Python Trading Bot + R2-D2 Integration
Enhanced: Multi-account Binance.US support with unified portfolio

Features:
- DUAL Binance.US accounts (Primary + Secondary)
- Unified portfolio tracking ($188.36 + $169.88 = $358.24 total)
- Smart order routing (highest balance, split orders, failover)
- R2-D2 confluence validation
- ATR-based risk management
- Automated order execution with fallback logic

Accounts:
- PRIMARY: $188.36 USD (high-risk trades)
- SECONDARY: $169.88 USD (low-risk/backup)
- TOTAL: $358.24 USD under management

Author: Mortimer for Captain
Version: 2.0.0 (Dual Account)
"""

import os
import sys
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass, field
from enum import Enum

import pandas as pd
import numpy as np

# Add R2 module to path
sys.path.insert(0, '/root/.openclaw/workspace/agent_sandboxes/r2-d2')
from r2_confluence_calculator import CryptonioAdapter, R2ConfluenceCalculator

# ═══════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════

class Config:
    """Production configuration for dual Binance setup"""
    
    # ═════════════════════════════════════════════════════════
    # BINANCE.US ACCOUNT 1 (PRIMARY - $188.36)
    # ═════════════════════════════════════════════════════════
    BINANCE_US_API_KEY = os.getenv('BINANCE_US_API_KEY', '')
    BINANCE_US_API_SECRET = os.getenv('BINANCE_US_API_SECRET', '')
    BINANCE_US_ACCOUNT_NAME = 'primary'
    BINANCE_US_ACCOUNT_BALANCE = 188.36  # Initial USD
    
    # ═════════════════════════════════════════════════════════
    # BINANCE.US ACCOUNT 2 (SECONDARY - $169.88)
    # ═════════════════════════════════════════════════════════
    BINANCE_US_API_KEY_2 = os.getenv('BINANCE_US_API_KEY_2', '')
    BINANCE_US_API_SECRET_2 = os.getenv('BINANCE_US_API_SECRET_2', '')
    BINANCE_US_ACCOUNT_NAME_2 = 'secondary'
    BINANCE_US_ACCOUNT_BALANCE_2 = 169.88  # Initial USD
    
    # ═════════════════════════════════════════════════════════
    # TRADING PARAMETERS
    # ═════════════════════════════════════════════════════════
    BASE_URL = 'https://api.binance.us'
    
    TIMEFRAME = '15m'  # 15-minute candles
    SYMBOL = 'BTCUSD'  # Primary trading pair
    
    # Risk Management
    MAX_DAILY_RISK_PER_ACCOUNT = 10.00  # $10/day per account
    TOTAL_MAX_DAILY_RISK = 20.00  # $20/day combined
    MIN_CONFLUENCE_SCORE = 60  # R2 threshold
    RISK_REWARD_RATIO = 1.5  # 1:1.5 minimum
    
    # Position Limits
    MAX_POSITIONS_PER_ACCOUNT = 1
    MAX_TOTAL_POSITIONS = 2  # Can have 1 per account
    
    # Order Splitting
    SPLIT_ORDERS = True  # Distribute large orders across accounts
    SPLIT_THRESHOLD = 50.00  # Split if position > $50
    
    # Execution
    PAPER_TRADING = True
    ATR_PERIOD = 14
    ATR_MULTIPLIER = 1.0
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = '/root/.openclaw/workspace/agent_sandboxes/the-great-cryptonio/logs/cryptonio_bot.log'


# ═══════════════════════════════════════════════════════════
# DUAL ACCOUNT DATA STRUCTURES
# ═══════════════════════════════════════════════════════════

@dataclass
class AccountInfo:
    """Binance account state"""
    name: str
    api_key: str
    api_secret: str
    client: Optional[object] = None
    balance_usd: float = 0.0
    balance_btc: float = 0.0
    positions_open: int = 0
    daily_risk_used: float = 0.0
    is_active: bool = False
    last_error: Optional[str] = None
    priority: int = 1  # Higher = preferred for orders


@dataclass
class UnifiedPortfolio:
    """Combined view of all accounts"""
    total_usd: float = 0.0
    total_btc: float = 0.0
    total_positions: int = 0
    total_daily_risk_used: float = 0.0
    accounts: Dict[str, AccountInfo] = field(default_factory=dict)
    active_accounts: List[str] = field(default_factory=list)
    
    def update_totals(self):
        """Recalculate combined totals"""
        self.total_usd = sum(acc.balance_usd for acc in self.accounts.values())
        self.total_btc = sum(acc.balance_btc for acc in self.accounts.values())
        self.total_daily_risk_used = sum(acc.daily_risk_used for acc in self.accounts.values())
        self.total_positions = sum(acc.positions_open for acc in self.accounts.values())
        self.active_accounts = [name for name, acc in self.accounts.items() if acc.is_active]


# ═══════════════════════════════════════════════════════════
# LOGGING SETUP
# ═══════════════════════════════════════════════════════════

os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('CryptonioBot')


# ═══════════════════════════════════════════════════════════
# DUAL BINANCE CLIENT
# ═══════════════════════════════════════════════════════════

class BinanceUSMultiClient:
    """
    Dual Binance.US account manager
    Handles Primary ($188.36) and Secondary ($169.88) accounts
    """
    
    def __init__(self):
        self.portfolio = UnifiedPortfolio()
        self._init_accounts()
    
    def _init_accounts(self):
        """Initialize both Binance accounts"""
        logger.info("Initializing dual Binance.US accounts...")
        
        # Account 1: Primary
        self.primary = AccountInfo(
            name=Config.BINANCE_US_ACCOUNT_NAME,
            api_key=Config.BINANCE_US_API_KEY,
            api_secret=Config.BINANCE_US_API_SECRET,
            balance_usd=Config.BINANCE_US_ACCOUNT_BALANCE,
            priority=2  # Higher priority
        )
        self.portfolio.accounts['primary'] = self.primary
        
        # Account 2: Secondary
        self.secondary = AccountInfo(
            name=Config.BINANCE_US_ACCOUNT_NAME_2,
            api_key=Config.BINANCE_US_API_KEY_2,
            api_secret=Config.BINANCE_US_API_SECRET_2,
            balance_usd=Config.BINANCE_US_ACCOUNT_BALANCE_2,
            priority=1
        )
        self.portfolio.accounts['secondary'] = self.secondary
        
        # Initialize clients
        for account_name, account in self.portfolio.accounts.items():
            self._connect_account(account)
        
        self.portfolio.update_totals()
        self._log_portfolio_summary()
    
    def _connect_account(self, account: AccountInfo):
        """Connect single Binance account"""
        try:
            from binance.client import Client
            
            if not account.api_key or not account.api_secret:
                logger.warning(f"[{account.name}] No API credentials")
                account.last_error = "Missing credentials"
                return
            
            account.client = Client(account.api_key, account.api_secret, tld='us')
            account.is_active = True
            logger.info(f"✅ [{account.name}] Binance client connected")
            
            # Fetch actual balances
            self._update_account_balance(account)
            
        except Exception as e:
            account.is_active = False
            account.last_error = str(e)
            logger.error(f"❌ [{account.name}] Connection failed: {e}")
    
    def _update_account_balance(self, account: AccountInfo):
        """Fetch real balances from Binance"""
        if not account.client or not account.is_active:
            return
        
        try:
            # Get USD balance
            account_info = account.client.get_account()
            for balance in account_info['balances']:
                if balance['asset'] == 'USD':
                    account.balance_usd = float(balance['free'])
                if balance['asset'] == 'BTC':
                    account.balance_btc = float(balance['free'])
            
            # Sync positions
            open_orders = account.client.get_open_orders(symbol=Config.SYMBOL)
            account.positions_open = len(open_orders)
            
        except Exception as e:
            logger.error(f"[{account.name}] Balance update failed: {e}")
    
    def _log_portfolio_summary(self):
        """Display unified portfolio"""
        logger.info("=" * 60)
        logger.info("💎 CRYPTONIO UNIFIED PORTFOLIO")
        logger.info("=" * 60)
        
        for name, account in self.portfolio.accounts.items():
            status = "🟢 ACTIVE" if account.is_active else "🔴 FAILED"
            logger.info(f"  [{name.upper()}] {status}")
            logger.info(f"      USD: ${account.balance_usd:.2f}")
            logger.info(f"      BTC: {account.balance_btc:.6f}")
            logger.info(f"      Positions: {account.positions_open}")
            logger.info(f"      Risk Used: ${account.daily_risk_used:.2f}")
            if account.last_error:
                logger.info(f"      Error: {account.last_error}")
        
        logger.info("-" * 60)
        logger.info(f"  📊 TOTAL USD: ${self.portfolio.total_usd:.2f}")
        logger.info(f"  📊 TOTAL BTC: {self.portfolio.total_btc:.6f}")
        logger.info(f"  📊 TOTAL POSITIONS: {self.portfolio.total_positions}")
        logger.info(f"  📊 TOTAL RISK: ${self.portfolio.total_daily_risk_used:.2f}")
        logger.info(f"  📊 ACTIVE ACCOUNTS: {len(self.portfolio.active_accounts)}")
        logger.info("=" * 60)
    
    def get_klines(self, symbol: str, interval: str, limit: int = 500) -> pd.DataFrame:
        """
        Fetch candlestick data
        Uses Primary account, falls back to Secondary
        """
        for account_name in ['primary', 'secondary']:
            account = self.portfolio.accounts.get(account_name)
            if not account or not account.is_active:
                continue
            
            try:
                klines = account.client.get_klines(
                    symbol=symbol,
                    interval=interval,
                    limit=limit
                )
                
                df = pd.DataFrame(klines, columns=[
                    'timestamp', 'open', 'high', 'low', 'close', 'volume',
                    'close_time', 'quote_asset_volume', 'number_of_trades',
                    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
                ])
                
                numeric_cols = ['open', 'high', 'low', 'close', 'volume']
                for col in numeric_cols:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df.set_index('timestamp', inplace=True)
                
                return df
                
            except Exception as e:
                logger.error(f"[{account.name}] Klines failed: {e}")
                continue
        
        logger.error("Both accounts failed to fetch klines")
        return pd.DataFrame()
    
    def select_account_for_order(self, quantity: float, risk_amount: float) -> Optional[AccountInfo]:
        """
        Smart account selection:
        - Primary preferred for most orders
        - Secondary fallback if primary full/failed
        - Based on available balance and daily risk
        """
        candidates = []
        
        for account in self.portfolio.accounts.values():
            if not account.is_active:
                continue
            
            # Check if account has capacity
            if account.daily_risk_used + risk_amount > Config.MAX_DAILY_RISK_PER_ACCOUNT:
                continue
            
            if account.balance_usd < risk_amount * 2:  # 2x buffer
                continue
            
            if account.positions_open >= Config.MAX_POSITIONS_PER_ACCOUNT:
                continue
            
            candidates.append(account)
        
        if not candidates:
            logger.warning("No accounts available for order")
            return None
        
        # Sort by priority (higher first)
        candidates.sort(key=lambda x: x.priority, reverse=True)
        
        return candidates[0]
    
    def place_market_order_split(self, symbol: str, side: str, total_quantity: float,
                                  stop_loss: float, take_profit: float) -> List[Dict]:
        """
        Place orders with smart splitting:
        - Single account if order small (< $50)
        - Split 50/50 if order large (>= $50)
        - Failover to secondary if primary fails
        """
        results = []
        
        should_split = Config.SPLIT_ORDERS and total_quantity > Config.SPLIT_THRESHOLD
        
        if should_split:
            # Split across accounts
            qty_primary = total_quantity * 0.6  # 60% to primary
            qty_secondary = total_quantity * 0.4  # 40% to secondary
            
            # Primary order
            result = self._place_single_order('primary', symbol, side, qty_primary, 
                                              stop_loss, take_profit)
            if result:
                results.append(result)
            
            # Secondary order
            result = self._place_single_order('secondary', symbol, side, qty_secondary,
                                              stop_loss, take_profit)
            if result:
                results.append(result)
        else:
            # Single order on best account
            account = self.select_account_for_order(total_quantity, stop_loss)
            if account:
                result = self._place_single_order(account.name, symbol, side, total_quantity,
                                                  stop_loss, take_profit)
                if result:
                    results.append(result)
        
        return results
    
    def _place_single_order(self, account_name: str, symbol: str, side: str, 
                           quantity: float, stop_loss: float, take_profit: float) -> Optional[Dict]:
        """Place order on specific account"""
        account = self.portfolio.accounts.get(account_name)
        if not account or not account.client:
            return None
        
        try:
            if Config.PAPER_TRADING:
                logger.info(f"[PAPER][{account.name}] {side} {quantity} {symbol}")
                logger.info(f"[PAPER][{account.name}] SL: {stop_loss}, TP: {take_profit}")
                
                # Track risk
                risk = abs(account.balance_usd - stop_loss) if stop_loss else quantity * 0.02
                account.daily_risk_used += risk
                account.positions_open += 1
                
                return {
                    'status': 'PAPER_TEST',
                    'account': account.name,
                    'symbol': symbol,
                    'side': side,
                    'quantity': quantity
                }
            
            # Real order
            order = account.client.order_market_buy(
                symbol=symbol, quantity=quantity
            ) if side == 'BUY' else account.client.order_market_sell(
                symbol=symbol, quantity=quantity
            )
            
            logger.info(f"✅ [{account.name}] Order placed: {order['orderId']}")
            
            # Update tracking
            account.positions_open += 1
            
            return {**order, 'account': account.name}
            
        except Exception as e:
            logger.error(f"❌ [{account.name}] Order failed: {e}")
            account.last_error = str(e)
            return None


# ═══════════════════════════════════════════════════════════
# R2 INTEGRATION (unchanged)
# ═══════════════════════════════════════════════════════════

class R2Integration:
    """Bridge between R2 analysis and Cryptonio execution"""
    
    def __init__(self):
        self.adapter = CryptonioAdapter()
        self.logger = logging.getLogger('R2')
    
    def analyze_market(self, df: pd.DataFrame, symbol: str = "BTCUSD") -> Dict:
        """Generate complete signal analysis"""
        self.logger.info(f"Requesting R2 analysis for {symbol}...")
        signal = self.adapter.generate_signal_report(df, symbol=symbol)
        self.logger.info(f"R2 Verdict: {signal['r2_verdict']}")
        return signal
    
    def validate_signal_quality(self, signal: Dict) -> Tuple[bool, str]:
        """Validate signal meets minimum standards"""
        if signal['confluence_score'] < Config.MIN_CONFLUENCE_SCORE:
            return False, f"Confluence {signal['confluence_score']} < {Config.MIN_CONFLUENCE_SCORE}"
        if signal['confidence'] < 0.5:
            return False, f"Confidence {signal['confidence']:.2} < 0.5"
        if signal['risk_reward'] < Config.RISK_REWARD_RATIO:
            return False, f"R:R {signal['risk_reward']} < {Config.RISK_REWARD_RATIO}"
        return True, "Signal validated by R2"


# ═══════════════════════════════════════════════════════════
# MAIN TRADING BOT - DUAL ACCOUNT
# ═══════════════════════════════════════════════════════════

class CryptonioBot:
    """
    Dual Account Trading Bot
    Manages $358.24 across Primary + Secondary Binance accounts
    """
    
    def __init__(self):
        self.config = Config()
        self.r2 = R2Integration()
        self.multi_client = BinanceUSMultiClient()
        self.last_check = None
        
        # Stats
        self.trades_today = 0
        self.total_trades = { 'primary': 0, 'secondary': 0 }
    
    def run_cycle(self):
        """
        Single bot cycle:
        1. Get unified portfolio view
        2. Fetch market data (failover between accounts)
        3. R2 analysis
        4. Smart order routing
        5. Execute with splitting/failover
        """
        logger.info("\n" + "=" * 60)
        logger.info(f"🤖 DUAL ACCOUNT CYCLE: {datetime.now().isoformat()}")
        
        # Step 1: Refresh portfolio
        self.multi_client.portfolio.update_totals()
        
        # Step 2: Fetch data (with failover)
        df = self.multi_client.get_klines(Config.SYMBOL, Config.TIMEFRAME, limit=500)
        if df.empty:
            logger.error("No data from any account")
            return
        
        logger.info(f"📊 Data: {len(df)} candles (failover working)")
        
        # Step 3: R2 analysis
        signal = self.r2.analyze_market(df, Config.SYMBOL)
        
        # Step 4: Validate
        is_valid, reason = self.r2.validate_signal_quality(signal)
        if not is_valid:
            logger.info(f"⏳ Signal rejected: {reason}")
            return
        
        # Step 5: Calculate order
        entry = signal['entry_price']
        stop = signal['stop_loss']
        target = signal['take_profit']
        
        # Determine position size across accounts
        available_usd = self.multi_client.portfolio.total_usd
        risk_per_trade = min(10.00, available_usd * 0.02)  # 2% or $10
        
        # Step 6: Place order with smart routing
        side = 'BUY' if 'LONG' in signal['signal_type'] else 'SELL'
        
        logger.info("-" * 60)
        logger.info(f"🎯 SIGNAL: {signal['signal_type']}")
        logger.info(f"   Confluence: {signal['confluence_score']:.1f}/190")
        logger.info(f"   Entry: ${entry:.2f}")
        logger.info(f"   Stop: ${stop:.2f}")
        logger.info(f"   Target: ${target:.2f}")
        
        # Place order (split if needed)
        results = self.multi_client.place_market_order_split(
            Config.SYMBOL, side, risk_per_trade, stop, target
        )
        
        if results:
            self.trades_today += len(results)
            for result in results:
                acc_name = result.get('account', 'unknown')
                self.total_trades[acc_name] = self.total_trades.get(acc_name, 0) + 1
                logger.info(f"✅ EXECUTED on [{acc_name}]")
        else:
            logger.warning("No orders executed")
    
    def run_continuous(self, interval_minutes: int = 15):
        """Continuous trading loop"""
        logger.info(f"🚀 DUAL ACCOUNT BOT RUNNING")
        logger.info(f"   Checking every {interval_minutes} minutes")
        logger.info(f"   Total AUM: ${Config.BINANCE_US_ACCOUNT_BALANCE + Config.BINANCE_US_ACCOUNT_BALANCE_2:.2f}")
        
        while True:
            try:
                now = datetime.now()
                current_minute = now.minute
                
                is_new_interval = (current_minute % interval_minutes == 0)
                in_window = (now.second <= 10)
                already_checked = (self.last_check == current_minute)
                
                if is_new_interval and in_window and not already_checked:
                    self.run_cycle()
                    self.last_check = current_minute
                
                # Daily reset at midnight
                if now.hour == 0 and now.minute == 0:
                    for account in self.multi_client.portfolio.accounts.values():
                        account.daily_risk_used = 0.0
                    logger.info("Daily risk reset")
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                logger.info("Bot stopped")
                break
            except Exception as e:
                logger.error(f"Bot error: {e}")
                time.sleep(60)


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Cryptonio Dual Account Bot')
    parser.add_argument('--test', action='store_true', help='Single test cycle')
    parser.add_argument('--paper', action='store_true', help='Paper trading')
    parser.add_argument('--symbol', default='BTCUSD', help='Trading pair')
    
    args = parser.parse_args()
    
    if args.paper:
        Config.PAPER_TRADING = True
    
    if args.symbol:
        Config.SYMBOL = args.symbol
    
    bot = CryptonioBot()
    
    if args.test:
        logger.info("RUNNING SINGLE TEST CYCLE (DUAL ACCOUNT)")
        bot.run_cycle()
    else:
        logger.info("RUNNING CONTINUOUS DUAL ACCOUNT MODE")
        bot.run_continuous(interval_minutes=15)


if __name__ == "__main__":
    sys.exit(main())
