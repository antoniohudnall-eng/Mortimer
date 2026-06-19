#!/usr/bin/env python3
"""
Cryptonio Volatility Monitor v1.0
Tracks market volatility across timeframes and alerts on spikes
"""

import sys
import os
import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

sys.path.insert(0, '/root/.openclaw/workspace/agent_sandboxes/the-great-cryptonio')

try:
    import pandas as pd
    import pandas_ta as ta
except ImportError:
    print("❌ pandas_ta required: pip install pandas_ta")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger('VolatilityMonitor')


class VolatilityLevel(Enum):
    """Market volatility classification"""
    CALM = "calm"
    NORMAL = "normal"
    ELEVATED = "elevated"
    HIGH = "high"
    EXTREME = "extreme"


@dataclass
class VolatilityReading:
    """Single volatility measurement"""
    symbol: str
    timestamp: datetime
    atr_14: float
    atr_percent: float  # ATR as % of price
    bb_width: float  # Bollinger Band width
    volume_zscore: float  # Volume deviation
    price_change_1h: float  # % change 1 hour
    volatility_level: VolatilityLevel
    alert_triggered: bool = False


class VolatilityMonitor:
    """
    Real-time volatility scanner
    Monitors all active symbols for volatility spikes
    """
    
    THRESHOLDS = {
        VolatilityLevel.CALM: 1.0,      # ATR% < 1%
        VolatilityLevel.NORMAL: 2.0,    # ATR% 1-2%
        VolatilityLevel.ELEVATED: 3.5,  # ATR% 2-3.5%
        VolatilityLevel.HIGH: 5.0,      # ATR% 3.5-5%
        VolatilityLevel.EXTREME: 999.0  # ATR% > 5%
    }
    
    def __init__(self, alert_threshold: float = 4.0):
        self.alert_threshold = alert_threshold
        self.readings_history: Dict[str, List[VolatilityReading]] = {}
        self.current_volatility: Dict[str, VolatilityLevel] = {}
        
    def analyze_volatility(self, symbol: str, df: pd.DataFrame) -> VolatilityReading:
        """
        Calculate volatility metrics for a symbol
        """
        if len(df) < 20:
            return VolatilityReading(
                symbol=symbol,
                timestamp=datetime.now(),
                atr_14=0.0,
                atr_percent=0.0,
                bb_width=0.0,
                volume_zscore=0.0,
                price_change_1h=0.0,
                volatility_level=VolatilityLevel.CALM,
                alert_triggered=False
            )
        
        # Calculate ATR (Average True Range)
        atr = ta.atr(df['high'], df['low'], df['close'], length=14)
        current_atr = atr.iloc[-1] if not atr.empty else 0.0
        
        current_price = df['close'].iloc[-1]
        atr_percent = (current_atr / current_price) * 100 if current_price > 0 else 0.0
        
        # Bollinger Band Width
        bb = ta.bbands(df['close'], length=20)
        if bb is not None and not bb.empty:
            upper = bb['BBU_20_2.0'].iloc[-1]
            lower = bb['BBL_20_2.0'].iloc[-1]
            bb_width = ((upper - lower) / current_price) * 100 if current_price > 0 else 0.0
        else:
            bb_width = 0.0
        
        # Volume Z-Score (current vs 20-day average)
        if 'volume' in df.columns and len(df) >= 20:
            vol_20 = df['volume'].tail(20).mean()
            vol_std = df['volume'].tail(20).std()
            current_vol = df['volume'].iloc[-1]
            volume_zscore = (current_vol - vol_20) / vol_std if vol_std > 0 else 0.0
        else:
            volume_zscore = 0.0
        
        # Price change (last 20 candles = ~5 hours on 15m)
        price_change = ((df['close'].iloc[-1] - df['close'].iloc[-20]) / 
                       df['close'].iloc[-20]) * 100 if len(df) >= 20 else 0.0
        
        # Classify volatility level
        volatility_level = self._classify_volatility(atr_percent)
        
        # Trigger alert if elevated+
        alert_triggered = volatility_level.value in ['elevated', 'high', 'extreme']
        
        reading = VolatilityReading(
            symbol=symbol,
            timestamp=datetime.now(),
            atr_14=current_atr,
            atr_percent=atr_percent,
            bb_width=bb_width,
            volume_zscore=volume_zscore,
            price_change_1h=price_change,
            volatility_level=volatility_level,
            alert_triggered=alert_triggered
        )
        
        # Store reading
        if symbol not in self.readings_history:
            self.readings_history[symbol] = []
        self.readings_history[symbol].append(reading)
        
        # Keep only last 100 readings
        self.readings_history[symbol] = self.readings_history[symbol][-100:]
        self.current_volatility[symbol] = volatility_level
        
        return reading
    
    def _classify_volatility(self, atr_percent: float) -> VolatilityLevel:
        """Classify volatility level based on ATR%"""
        for level, threshold in sorted(self.THRESHOLDS.items(), key=lambda x: x[1]):
            if atr_percent <= threshold:
                return level
        return VolatilityLevel.EXTREME
    
    def get_position_size_adjustment(self, symbol: str) -> float:
        """
        Adjust position size based on volatility
        Returns multiplier (0.5 = half size, 2.0 = double)
        """
        level = self.current_volatility.get(symbol, VolatilityLevel.NORMAL)
        
        adjustments = {
            VolatilityLevel.CALM: 1.2,      # Increase size 20%
            VolatilityLevel.NORMAL: 1.0,    # Base size
            VolatilityLevel.ELEVATED: 0.75, # Reduce 25%
            VolatilityLevel.HIGH: 0.5,      # Reduce 50%
            VolatilityLevel.EXTREME: 0.25    # Reduce 75%
        }
        
        return adjustments.get(level, 1.0)
    
    def should_pause_trading(self, symbol: str) -> bool:
        """Check if extreme volatility warrants pausing"""
        level = self.current_volatility.get(symbol, VolatilityLevel.NORMAL)
        return level == VolatilityLevel.EXTREME
    
    def print_volatility_report(self, symbol: str):
        """Display current volatility status"""
        if symbol not in self.readings_history or not self.readings_history[symbol]:
            return
        
        reading = self.readings_history[symbol][-1]
        
        print(f"\n📊 {symbol} Volatility Report")
        print("-" * 50)
        print(f"  ATR(14): ${reading.atr_14:.2f} ({reading.atr_percent:.2f}%)")
        print(f"  Bollinger Width: {reading.bb_width:.2f}%")
        print(f"  Volume Z-Score: {reading.volume_zscore:.2f}")
        print(f"  Price Change(20c): {reading.price_change_1h:.2f}%")
        print(f"  Level: {reading.volatility_level.value.upper()}")
        
        adj = self.get_position_size_adjustment(symbol)
        if adj != 1.0:
            print(f"  Position Size Adjustment: {adj:.0%}")
        
        if reading.alert_triggered:
            print(f"  ⚠️  HIGH VOLATILITY DETECTED")
        
        if self.should_pause_trading(symbol):
            print(f"  🔴 TRADING PAUSED - Extreme volatility")


def monitor_all_symbols():
    """Monitor volatility across all configured symbols"""
    from cryptonio_multi_exchange import Config, UnifiedExchangeManager
    
    print("=" * 70)
    print("🌊 CRYPTONIO VOLATILITY MONITOR v1.0")
    print("=" * 70)
    print(f"Time: {datetime.now().isoformat()}")
    print(f"Symbols: {', '.join(Config.ACTIVE_SYMBOLS)}")
    print(f"Alert Threshold: {VolatilityMonitor.THRESHOLDS[VolatilityLevel.HIGH]}% ATR")
    print("=" * 70)
    print()
    
    # Initialize
    manager = UnifiedExchangeManager()
    monitor = VolatilityMonitor(alert_threshold=4.0)
    
    print(f"Exchanges connected: {len(manager.clients)}")
    for name, client in manager.clients.items():
        status = "🟢" if client.is_connected else "🔴"
        print(f"  {status} {name}")
    print()
    
    # Analyze each symbol
    alerts_triggered = []
    
    for symbol in Config.ACTIVE_SYMBOLS:
        print(f"\nAnalyzing {symbol}...")
        
        # Fetch data from primary exchange for this symbol
        df, source = manager.fetch_data_with_failover(symbol, Config.TIMEFRAME)
        
        if df.empty:
            print(f"  ⚠️ No data available")
            continue
        
        # Calculate volatility
        reading = monitor.analyze_volatility(symbol, df)
        
        # Print report
        monitor.print_volatility_report(symbol)
        
        # Track alerts
        if reading.alert_triggered:
            alerts_triggered.append({
                'symbol': symbol,
                'level': reading.volatility_level.value,
                'atr_pct': reading.atr_percent,
                'price_change': reading.price_change_1h
            })
    
    # Summary
    print("\n" + "=" * 70)
    print("VOLATILITY SUMMARY")
    print("=" * 70)
    
    if alerts_triggered:
        print(f"\n⚠️  {len(alerts_triggered)} HIGH VOLATILITY ALERT(S):")
        for alert in alerts_triggered:
            print(f"   {alert['symbol']}: {alert['level'].upper()} "
                  f"(ATR: {alert['atr_pct']:.2f}%, Change: {alert['price_change']:.2f}%)")   
    else:
        print("\n✅ All markets within normal volatility ranges")
    
    print("\nPosition Size Recommendations:")
    for symbol in Config.ACTIVE_SYMBOLS:
        adj = monitor.get_position_size_adjustment(symbol)
        level = monitor.current_volatility.get(symbol, VolatilityLevel.NORMAL)
        if adj != 1.0:
            print(f"   {symbol}: {adj:.0%} ({level.value})")
        else:
            print(f"   {symbol}: 100% (normal)")
    
    print("\n" + "=" * 70)
    
    return monitor


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Cryptonio Volatility Monitor")
    parser.add_argument('--continuous', action='store_true', 
                       help='Run continuous monitoring')
    parser.add_argument('--interval', type=int, default=15,
                       help='Check interval in minutes (default: 15)')
    
    args = parser.parse_args()
    
    if args.continuous:
        print("Starting continuous volatility monitoring...")
        print("Press Ctrl+C to stop")
        try:
            while True:
                monitor_all_symbols()
                print(f"\n⏳ Next check in {args.interval} minutes...")
                import time
                time.sleep(args.interval * 60)
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped.")
    else:
        monitor_all_symbols()
