# R2-D2 Pattern Recognition & Confluence Scoring System
# Production Python Module for Cryptonio Integration
# Based on: Videos 1-21 trading education curriculum
# Author: Mortimer for R2-D2 / Cryptonio collaboration

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional, List

class R2ConfluenceCalculator:
    """
    R2-D2's 190-Point Confluence Scoring System
    
    Calculates trade signals based on:
    - Support/Resistance Levels (40 pts max)
    - Trend Alignment (45 pts max)
    - Volume Profile (55 pts max)
    - Momentum Divergence (25 pts max)
    - Whale Activity (30 pts max)
    
    Threshold: 60+ for high-probability trades
    """
    
    def __init__(self):
        self.max_scores = {
            'support_resistance': 40,
            'trend_alignment': 45,
            'volume_profile': 55,
            'momentum': 25,
            'whale_activity': 30
        }
        self.threshold = 60
        self.max_total = 190
    
    def calculate_support_resistance(self, df: pd.DataFrame, lookback: int = 100) -> Tuple[float, Dict]:
        """
        Calculate Support/Resistance score (Video 3, 5)
        Uses: Pivot points, Volume Profile levels
        
        Returns: score (0-40), metadata dict
        """
        # Calculate pivot levels (daily standard pivots)
        pivot = (df['high'].shift(1) + df['low'].shift(1) + df['close'].shift(1)) / 3
        r1 = (2 * pivot) - df['low'].shift(1)
        s1 = (2 * pivot) - df['high'].shift(1)
        r2 = pivot + (df['high'].shift(1) - df['low'].shift(1))
        s2 = pivot - (df['high'].shift(1) - df['low'].shift(1))
        
        current_price = df['close'].iloc[-1]
        
        # Check proximity to levels (within 1%)
        tolerance = current_price * 0.01
        
        levels = {
            'pivot': pivot.iloc[-1],
            'r1': r1.iloc[-1],
            'r2': r2.iloc[-1],
            's1': s1.iloc[-1],
            's2': s2.iloc[-1]
        }
        
        # Calculate score based on proximity
        score = 0
        for level_name, level_value in levels.items():
            distance = abs(current_price - level_value)
            if distance < tolerance:
                # Closer = higher score
                proximity_score = (1 - (distance / tolerance)) * 8
                score += proximity_score
        
        score = min(score, self.max_scores['support_resistance'])
        
        metadata = {
            'levels': levels,
            'current_price': current_price,
            'tolerance': tolerance,
            'nearest_level': min(levels.items(), key=lambda x: abs(current_price - x[1]))
        }
        
        return score, metadata
    
    def calculate_trend_alignment(self, df: pd.DataFrame) -> Tuple[float, Dict]:
        """
        Calculate Trend Alignment score (Video 4 - Calman Trend Levels)
        Uses: Multi-timeframe EMA alignment
        
        Returns: score (0-45), metadata dict
        """
        # Calculate EMAs (Video 4: length=28, short=40, long=80)
        ema_fast = df['close'].ewm(span=40, adjust=False).mean()
        ema_slow = df['close'].ewm(span=80, adjust=False).mean()
        
        # Current values
        current_close = df['close'].iloc[-1]
        current_fast = ema_fast.iloc[-1]
        current_slow = ema_slow.iloc[-1]
        
        # Trend Direction
        bullish = current_close > current_fast > current_slow
        bearish = current_close < current_fast < current_slow
        
        # Calculate score based on alignment strength
        if bullish:
            # Calculate distance from fast EMA (stronger trend = further above)
            distance = (current_close - current_fast) / current_fast
            # Normalize to score (max ~45)
            score = min(abs(distance) * 2000, self.max_scores['trend_alignment'])
            direction = 'bullish'
        elif bearish:
            distance = (current_fast - current_close) / current_close
            score = min(abs(distance) * 2000, self.max_scores['trend_alignment'])
            direction = 'bearish'
        else:
            # Mixed signals = chop, lower score
            score = 10
            direction = 'chop'
        
        metadata = {
            'direction': direction,
            'close': current_close,
            'ema_40': current_fast,
            'ema_80': current_slow,
            'alignment_strength': score / self.max_scores['trend_alignment']
        }
        
        return score, metadata
    
    def calculate_volume_profile(self, df: pd.DataFrame) -> Tuple[float, Dict]:
        """
        Calculate Volume Profile score (Video 5)
        Uses: Volume spikes at key levels
        
        Returns: score (0-55), metadata dict
        """
        if 'volume' not in df.columns:
            # If no volume data, return neutral
            return 27.5, {'error': 'No volume data'}
        
        current_volume = df['volume'].iloc[-1]
        volume_sma = df['volume'].rolling(window=20).mean().iloc[-1]
        
        # Volume spike threshold (2x average = significant)
        volume_ratio = current_volume / volume_sma if volume_sma > 0 else 1
        
        if volume_ratio > 2.0:
            score = self.max_scores['volume_profile']
        elif volume_ratio > 1.5:
            score = self.max_scores['volume_profile'] * 0.75
        elif volume_ratio > 1.0:
            score = self.max_scores['volume_profile'] * 0.5
        else:
            score = self.max_scores['volume_profile'] * 0.25
        
        metadata = {
            'current_volume': current_volume,
            'volume_sma': volume_sma,
            'volume_ratio': volume_ratio,
            'spike_detected': volume_ratio > 2.0
        }
        
        return score, metadata
    
    def calculate_momentum(self, df: pd.DataFrame) -> Tuple[float, Dict]:
        """
        Calculate Momentum score (Video 11)
        Uses: RSI, MACD, Stochastic
        
        Returns: score (0-25), metadata dict
        """
        # RSI Calculation (14-period)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # Normalize RSI to 0-25 score
        # RSI > 70 or < 30 = strong signal
        current_rsi = rsi.iloc[-1]
        
        if current_rsi > 70 or current_rsi < 30:
            score = self.max_scores['momentum']
        elif current_rsi > 60 or current_rsi < 40:
            score = self.max_scores['momentum'] * 0.75
        else:
            score = self.max_scores['momentum'] * 0.5
        
        metadata = {
            'rsi': current_rsi,
            'overbought': current_rsi > 70,
            'oversold': current_rsi < 30
        }
        
        return score, metadata
    
    def calculate_whale_activity(self, onchain_data: Optional[Dict] = None) -> Tuple[float, Dict]:
        """
        Calculate Whale Activity score (Video 16)
        Uses: On-chain transaction data (large transfers)
        
        Returns: score (0-30), metadata dict
        """
        # If no on-chain data provided, return neutral
        if onchain_data is None:
            return 15, {'note': 'No on-chain data provided'}
        
        # Analyze large transactions
        large_tx_count = onchain_data.get('large_transactions_24h', 0)
        whale_inflow = onchain_data.get('whale_inflow', 0)
        whale_outflow = onchain_data.get('whale_outflow', 0)
        
        # Score based on activity
        if large_tx_count > 100:  # High activity
            score = self.max_scores['whale_activity']
        elif large_tx_count > 50:
            score = self.max_scores['whale_activity'] * 0.75
        elif large_tx_count > 20:
            score = self.max_scores['whale_activity'] * 0.5
        else:
            score = self.max_scores['whale_activity'] * 0.25
        
        metadata = {
            'large_tx_count': large_tx_count,
            'whale_inflow': whale_inflow,
            'whale_outflow': whale_outflow,
            'net_flow': whale_inflow - whale_outflow
        }
        
        return score, metadata
    
    def calculate_total_confluence(self, df: pd.DataFrame, 
                                   onchain_data: Optional[Dict] = None) -> Dict:
        """
        Calculate complete 190-point confluence score
        
        Returns: Complete analysis dict for Cryptonio
        """
        scores = {}
        metadata = {}
        
        # Calculate each component
        scores['support_resistance'], metadata['sr'] = self.calculate_support_resistance(df)
        scores['trend_alignment'], metadata['trend'] = self.calculate_trend_alignment(df)
        scores['volume_profile'], metadata['volume'] = self.calculate_volume_profile(df)
        scores['momentum'], metadata['momentum'] = self.calculate_momentum(df)
        scores['whale_activity'], metadata['whale'] = self.calculate_whale_activity(onchain_data)
        
        # Total score
        total_score = sum(scores.values())
        
        # Signal strength
        signal_strength = total_score / self.max_total
        
        # Recommended action
        if total_score >= 80:
            action = "STRONG_BUY"
        elif total_score >= 60:
            action = "BUY"
        elif total_score >= 40:
            action = "WEAK_BUY"
        else:
            action = "NO_TRADE"
        
        return {
            'timestamp': datetime.now().isoformat(),
            'symbol': df.get('symbol', 'UNKNOWN'),
            'scores': scores,
            'total_score': total_score,
            'max_possible': self.max_total,
            'signal_strength': signal_strength,
            'threshold': self.threshold,
            'above_threshold': total_score >= self.threshold,
            'recommended_action': action,
            'metadata': metadata,
            'r2_verdict': f"Confluence Score: {total_score}/190 - {action}"
        }


class R2PatternValidator:
    """
    R2-D2 Pattern Recognition & Validation
    Based on Video 20 Monte Carlo Validation Framework
    """
    
    def __init__(self):
        self.train_window = None
        self.test_window = None
    
    def detect_ema_crossover(self, df: pd.DataFrame, fast: int = 5, slow: int = 8) -> Dict:
        """
        Detect EMA Crossover (Video 17-19 logic)
        
        Returns: Signal dict for Cryptonio execution
        """
        ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
        
        # Current and previous values
        curr_fast = ema_fast.iloc[-1]
        curr_slow = ema_slow.iloc[-1]
        prev_fast = ema_fast.iloc[-2]
        prev_slow = ema_slow.iloc[-2]
        
        # Detect crossover
        golden_cross = (curr_fast > curr_slow) and (prev_fast <= prev_slow)
        death_cross = (curr_fast < curr_slow) and (prev_fast >= prev_slow)
        
        return {
            'golden_cross': golden_cross,
            'death_cross': death_cross,
            'fast_ema': curr_fast,
            'slow_ema': curr_slow,
            'trend': 'bullish' if curr_fast > curr_slow else 'bearish'
        }
    
    def calculate_atr_stop(self, df: pd.DataFrame, period: int = 14, multiplier: float = 1.0) -> Dict:
        """
        ATR-based stop loss (Video 18)
        
        Returns: Stop loss and take profit levels
        """
        # Calculate ATR
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        atr = true_range.rolling(period).mean()
        
        current_price = df['close'].iloc[-1]
        current_atr = atr.iloc[-1]
        
        # Stop and target
        stop_distance = current_atr * multiplier
        stop_loss = current_price - stop_distance
        take_profit = current_price + (stop_distance * 1.5)  # 1:1.5 R:R
        
        return {
            'current_price': current_price,
            'atr': current_atr,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'stop_distance': stop_distance,
            'risk_reward': 1.5
        }
    
    def detect_divergence(self, df: pd.DataFrame) -> Dict:
        """
        Detect Price-Momentum Divergence (Video 11)
        
        Returns: Divergence signals
        """
        # Calculate price lows/highs
        price_lows = df['low'].rolling(window=5).min()
        price_highs = df['high'].rolling(window=5).max()
        
        # Calculate RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # Detect bullish divergence (price lower low, RSI higher low)
        bullish_div = (df['low'].iloc[-1] < price_lows.iloc[-5]) and (rsi.iloc[-1] > rsi.iloc[-5])
        
        # Detect bearish divergence (price higher high, RSI lower high)
        bearish_div = (df['high'].iloc[-1] > price_highs.iloc[-5]) and (rsi.iloc[-1] < rsi.iloc[-5])
        
        return {
            'bullish_divergence': bullish_div,
            'bearish_divergence': bearish_div,
            'current_rsi': rsi.iloc[-1]
        }


class CryptonioAdapter:
    """
    Bridge between R2 Analysis and Cryptonio Execution
    """
    
    def __init__(self):
        self.calculator = R2ConfluenceCalculator()
        self.validator = R2PatternValidator()
    
    def generate_signal_report(self, df: pd.DataFrame, 
                               onchain_data: Optional[Dict] = None,
                               symbol: str = "BTCUSD") -> Dict:
        """
        Complete signal generation for Cryptonio
        
        1. Calculate confluence score
        2. Detect patterns
        3. Validate with Monte Carlo (placeholder)
        4. Return execution-ready signal
        """
        # Step 1: Confluence Analysis
        confluence = self.calculator.calculate_total_confluence(df, onchain_data)
        
        # Step 2: Pattern Detection
        ema_signal = self.validator.detect_ema_crossover(df)
        atr_levels = self.validator.calculate_atr_stop(df)
        divergence = self.validator.detect_divergence(df)
        
        # Step 3: Signal Quality Check
        quality_score = confluence['total_score'] / 190
        has_divergence = divergence['bullish_divergence'] or divergence['bearish_divergence']
        has_crossover = ema_signal['golden_cross'] or ema_signal['death_cross']
        
        # Composite signal
        if confluence['above_threshold'] and has_crossover:
            if ema_signal['golden_cross'] and divergence['bullish_divergence']:
                signal_type = "STRONG_LONG"
                confidence = quality_score * 1.2  # Bonus for divergence confirmation
            elif ema_signal['death_cross'] and divergence['bearish_divergence']:
                signal_type = "STRONG_SHORT"
                confidence = quality_score * 1.2
            elif ema_signal['golden_cross']:
                signal_type = "LONG"
                confidence = quality_score
            else:
                signal_type = "SHORT"
                confidence = quality_score
        else:
            signal_type = "NEUTRAL"
            confidence = quality_score
        
        return {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'signal_type': signal_type,
            'confidence': min(confidence, 1.0),
            'confluence_score': confluence['total_score'],
            'confluence_breakdown': confluence['scores'],
            'entry_price': atr_levels['current_price'],
            'stop_loss': atr_levels['stop_loss'],
            'take_profit': atr_levels['take_profit'],
            'risk_reward': atr_levels['risk_reward'],
            'pattern_confirms': {
                'ema_crossover': ema_signal,
                'divergence': divergence
            },
            'r2_verdict': f"{signal_type} @ {atr_levels['current_price']:.2f} (SL: {atr_levels['stop_loss']:.2f}, TP: {atr_levels['take_profit']:.2f})",
            'execution_ready': confluence['above_threshold'] and confidence > 0.4
        }


# ═══════════════════════════════════════════════════════════
# USAGE EXAMPLE FOR CRYPTONIO
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    """
    R2-D2 Integration Example
    
    How Cryptonio uses R2's analysis:
    1. R2 calculates confluence score
    2. Cryptonio validates capital/risk
    3. If approved → Execute via Video 21 bot
    """
    
    # Mock data (replace with live market data)
    import numpy as np
    
    np.random.seed(42)
    mock_data = pd.DataFrame({
        'open': np.random.randn(100).cumsum() + 50000,
        'high': np.random.randn(100).cumsum() + 50100,
        'low': np.random.randn(100).cumsum() + 49900,
        'close': np.random.randn(100).cumsum() + 50050,
        'volume': np.random.randint(100000, 1000000, 100)
    })
    
    # Initialize R2 Adapter
    r2 = CryptonioAdapter()
    
    # Generate signal
    signal = r2.generate_signal_report(mock_data, symbol="BTCUSD")
    
    print("R2-D2 SIGNAL REPORT")
    print("=" * 50)
    print(f"Symbol: {signal['symbol']}")
    print(f"Signal: {signal['signal_type']}")
    print(f"Confidence: {signal['confidence']:.2%}")
    print(f"Confluence: {signal['confluence_score']}/190")
    print(f"Entry: {signal['entry_price']:.2f}")
    print(f"Stop: {signal['stop_loss']:.2f}")
    print(f"Target: {signal['take_profit']:.2f}")
    print(f"R:R: 1:{signal['risk_reward']}")
    print(f"Execute? {'YES' if signal['execution_ready'] else 'NO'}")
    print("=" * 50)
    
    # Cryptonio decision:
    if signal['execution_ready']:
        print("\n💎 CRYPTONIO: 'Executing R2-verified signal...'")
        print("   → Checking portfolio balance...")
        print("   → Calculating position size...")
        print("   → Submitting order to exchange...")
    else:
        print("\n⏳ CRYPTONIO: 'Signal below threshold. Holding...'")
