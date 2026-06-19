# CRYPTONIO Pine Script Strategy
## Confluence Scoring System with R2-D2 Integration

**Agent:** the-great-cryptonio  
**Strategy:** Confluence-based crypto trading  
**Platform:** TradingView  
**Version:** Pine Script v5  
**Created:** 2026-03-07 06:58 UTC  

---

## Overview

This Pine Script implements **Cryptonio's 60-point confluence scoring system** from the technical analysis masterclass (Videos 1-3). It detects candlestick patterns, support/resistance levels, Fair Value Gaps (FVG), Fibonacci alignments, and trend direction to generate high-probability trade signals.

---

## How to Use

### Step 1: Add to TradingView

1. Open TradingView (tradingview.com)
2. Select any crypto chart (BTC/ETH recommended)
3. Open **Pine Editor** (bottom of screen)
4. Copy/paste `CRYPTONIO_CONFLUENCE_STRATEGY.pine`
5. Click **Add to Chart**

### Step 2: Configure Inputs

Click the gear icon ⚙️ next to the strategy name:

| Setting | Default | Description |
|---------|---------|-------------|
| Risk Per Trade | 2% | Position size |
| Confluence Threshold | 60 | Minimum score to trade |
| Min Risk:Reward | 1.5 | Filter low R:R setups |
| Show Patterns | true | Display pattern labels |
| Show FVG | true | Show Fair Value Gaps |
| Show SMA | true | Display EMAs (20/50/200) |

### Step 3: Set Alerts

1. Click **Alerts** (top right clock icon)
2. Click **Create Alert**
3. Select condition: **CRYPTONIO Confluence System**
4. Choose either:
   - 📊 **CRYPTONIO - BUY Signal**
   - 📊 **CRYPTONIO - SELL Signal**
5. **Webhook URL:** Enter your endpoint (e.g., `https://myl0nr0s.cloud:9001/tradingview-webhook`)
6. Click **Create**

---

## Pattern Detection

### 8 Candlestick Patterns (Video 2)

| Pattern | Code | Signal |
|---------|------|--------|
| **Bullish Engulfing** | BE | Reversal at support |
| **Bearish Engulfing** | SE | Reversal at resistance |
| **Hammer** | H | Bullish reversal |
| **Shooting Star** | SS | Bearish reversal |
| **Bullish Marubozu** | MZ | Trend continuation (green) |
| **Bearish Marubozu** | MZ | Trend continuation (red) |
| **Doji** | D | Indecision/reversal |
| **Momentum** | — | Breakout/breakdown candle |

### Smart Money Concepts (Video 3)

- **Fair Value Gaps (FVG):** Orange boxes showing imbalance zones
- **Support/Resistance:** Green (support) / Red (resistance) lines
- **Fibonacci Levels:** 0.618 retracement (golden ratio)

---

## Confluence Scoring System

Score components when pattern appears at key levels:

| Component | Points | Requirement |
|-----------|--------|-------------|
| Pattern at S/R | 20 | Pattern + support/resistance confluence |
| Pattern detected | 15 | Any valid pattern |
| Momentum candle | 15 | 2-3x previous candle size |
| Fibonacci alignment | 10 | Price near 0.618 level |
| Fair Value Gap | 10 | FVG in trend direction |
| Trend direction | 10 | EMA 20/50 alignment |
| Volume spike | 10 | (Requires volume indicator) |
| **TOTAL POSSIBLE** | **90** | **60+ = Trade Signal** |

---

## Visual Cues

### Background Colors
- **Green tint:** BUY signal active
- **Red tint:** SELL signal active

### Pattern Labels
- Appear directly on candles
- Color-coded (green = bullish, red = bearish)

### Info Panel (Top Right)
Displays in real-time:
- ⭐ **Confluence Score** (current)
- 📊 **Pattern detected**
- 📈 **Trend direction** (BULLISH/BEARISH/NEUTRAL)
- 🎯 **S/R proximity**
- 🚨 **Trade signal** (LONG/SHORT/—)

---

## Webhook Integration (R2-D2)

### Alert Format Sent to Webhook:

```json
{
  "symbol": "BTCUSDT",
  "side": "buy",
  "price": 67234.50,
  "score": 75,
  "pattern": "Bullish Engulfing at Support",
  "timeframe": "15",
  "timestamp": "2026-03-07T06:58:00Z"
}
```

### Webhook Flow:

```
TradingView Chart
      ↓ (Alert fires)
   Webhook POST
      ↓
Your Endpoint (dusty-bridge)
      ↓
   R2-D2 Validation
      ↓
   Binance.US API
      ↓
   Trade Executed ✅
```

---

## Recommended Timeframes

| Timeframe | Use Case | Risk Level |
|-----------|----------|------------|
| **5m** | Scalping | High |
| **15m** | Intraday | Medium |
| **1H** | Swing trading | Low-Medium |
| **4H** | Position trading | Low |
| **1D** | Investing | Very Low |

**Cryptonio's recommendation:** Start with **15m or 1H** for balanced accuracy.

---

## Backtesting

TradingView automatically backtests the strategy:

1. Click **Strategy Tester** tab
2. View performance metrics:
   - Win rate %
   - Profit factor
   - Max drawdown
   - Net profit

**Adjust confluence threshold** based on backtest results.

---

## Integration with Existing System

### For Cryptonio's Portfolio Management:

1. **Daily Scanner (06:00 UTC):** Run strategy on BTC, ETH, and portfolio coins
2. **Alert Handler:** Webhook → `dusty-core` → Binance.US execution
3. **Risk Management:** Strategy uses 2% risk per trade (matches Cryptonio limits)
4. **Confluence Filter:** Only trades 60+ score signals
5. **R2 Integration:** Pattern detection + probability analysis

### Files:
- Strategy: `CRYPTONIO_CONFLUENCE_STRATEGY.pine`
- This README: `README_PINE_SCRIPT.md`
- Location: `agent_sandboxes/the-great-cryptonio/pinescript/`

---

## Video References

| Video | Content | Applied In Strategy |
|-------|---------|---------------------|
| **1** | Risk management, confluence | Risk per trade, confluence scoring |
| **2** | 8 candlestick patterns | Pattern detection logic |
| **3** | Elliott Wave, FVG, S/R | Multi-timeframe, FVG boxes, S/R levels |

---

## Troubleshooting

### No signals showing?
- ✅ Check confluence threshold (try lowering to 40-50 for testing)
- ✅ Verify EMA 20/50/200 are displayed (trend filter)
- ✅ Ensure timeframe has enough historical data

### Too many signals?
- ⬆️ Increase confluence threshold to 70-80
- ⬆️ Increase minimum risk:reward to 2.0+
- ⬇️ Add volume filter (if volume data available)

### Patterns not detecting?
- ✅ Check "Show Patterns" input is enabled
- ✅ Some patterns require specific candle sizes (zoom in on chart)

---

## R2-D2 Protocol Integration

R2's enhanced analysis format:

```
R2: "╔════════════════════════════════════╗
     ║ BTC/USDT Multi-Timeframe Scan     ║
     ╠════════════════════════════════════╣
     ║ Pine Script: Score 75/100 🟢         ║
     ║ Pattern: Bullish Engulfing at S/R   ║
     ║ 4H: FVG at $66,800 (support)       ║
     ║ 1H: Cup formation (U-shape)        ║
     ║ 15M: Confirmation candle           ║
     ║                                    ║
     ║ RECOMMENDATION: Long setup ✅       ║
     ║ Entry: $66,850 | SL: $66,500       ║
     ╚════════════════════════════════════╝"
```

---

**The portfolio is yours, Captain. Let Cryptonio make it sing.** 🎰📈

---

*"Every dollar has a job. Deploy with purpose."*
