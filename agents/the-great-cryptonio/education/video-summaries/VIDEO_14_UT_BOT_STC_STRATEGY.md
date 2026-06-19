# VIDEO 14: UT Bot Alert + STC Oscillator Scalping Strategy

**Source:** YouTube Trading Tutorial (transcript provided 2026-03-07 08:05 UTC)
**Status:** Strategy Summary Complete
**Instrument:** Forex/Crypto (5M timeframe minimum)
**Win Rate Claim:** 80% (up to 90-95% with STC confirmation)

---

## ⚠️ DISCLAIMER

> Claims made (80-95% win rate) should be considered marketing hyperbole. Always backtest strategies before live deployment.

---

## Overview

Simple trend-following scalping system using:
1. **Primary:** UT Bot Alert indicator (trend/swing detection)
2. **Confirmation:** STC Oscillator (momentum filter)

---

## Primary Indicator: UT Bot Alert

**Access:** TradingView Indicator Library → Search "UT Bot"

### Setup (Dual Instance Method):

**Instance 1: BUY Signals Only**
- Indicator: UT Bot Alert
- Key Value: `2`
- ATR Period: `1`
- Style: **UNCHECK** Sell option (hide sell signals)

**Instance 2: SELL Signals Only**
- Indicator: UT Bot Alert  
- Key Value: `2`
- ATR Period: `1`
- Style: **UNCHECK** Buy option (hide buy signals)

---

## Confirmation Indicator: STC Oscillator

**Access:** Search "STC oscillator" (momentum oscillator)

### Custom Settings:

| Parameter | Value |
|-----------|-------|
| Length | **80** |
| Fast Length | **27** |

### Visual Settings:
- Plot 1 (main): **Green** (increase opacity)
- Plot 2: **Red** (increase opacity)

---

## Entry Rules

### BUY Trade:
1. ✅ UT Bot shows **buy arrow**
2. ✅ STC line **below green line**
3. ✅ STC line **moving upward**
4. ➡️ Enter long

### SELL Trade:
1. ✅ UT Bot shows **sell arrow**
2. ✅ STC line **above red line**
3. ✅ STC line **moving downward**
4. ➡️ Enter short

---

## Risk Management

| Element | Setting |
|---------|---------|
| **Timeframe** | 5M minimum (no lower) |
| **Stop Loss** | Below/above signal swing low/high |
| **Take Profit** | **2x stop loss** (1:2 R:R) |

### Example Trades:
- Signal quality check: STC must confirm direction
- Trades typically 4:1 R:R mentioned in example
- Exit when target hit or reverse signal appears

---

## Key Points

| Aspect | Detail |
|--------|--------|
| **Simplicity** | No complex analysis - just indicator alignment |
| **Timeframes** | 5M-15M-30M-1H-4H recommended |
| **Market** | Trending forex pairs, crypto assets |
| **Confirmation** | STC prevents false UT Bot signals |

---

## Cryptonio Research Notes

### Strengths:
- Simple mechanical system
- Clear entry/exit rules
- Visual confirmation easy to read
- STC provides additional momentum filter

### Weaknesses:
- 90-95% win rate claim is unrealistic
- Single indicator systems typically fail in ranging markets
- "Set and forget" mentality can lead to large drawdowns
- No volume analysis mentioned
- Works best in TRENDING markets only

### Verification Required:
- [ ] Backtest on 5M over 6 months
- [ ] Test during Asian/London/NY sessions separately
- [ ] Verify across major forex pairs (EUR/USD, GBP/USD, USD/JPY)
- [ ] Test crypto assets (BTC, ETH)
- [ ] Analyze maximum consecutive losses
- [ ] Factor in spread costs for 5M scalping

---

## Integration with Existing Systems

| Video | Strategy | Synergy with This System |
|-------|----------|-------------------------|
| 10 | 4H Range | Different approach - counter-trend vs trend |
| 11 | EMA+RSI+Stoch | Triple confirmation vs dual indicator |
| 12 | VWAP+EMA | Similar simplicity, different toolset |
| 13 | Pine Course | Could code UT Bot logic from scratch |

---

## Status

**Recommended Action:** 
1. Add to backtesting queue (Pine Script implementation)
2. Compare vs existing 4H scalping strategy
3. Determine if worth live testing with small position size

**Priority:** Medium (interesting but unverified claims)

**Research Value:** ★★★☆☆ (simple system worth testing)

---

*"No strategy has a 90% win rate. If it did, everyone would use it. Backtest everything." — Cryptonio's First Law of Trading*
