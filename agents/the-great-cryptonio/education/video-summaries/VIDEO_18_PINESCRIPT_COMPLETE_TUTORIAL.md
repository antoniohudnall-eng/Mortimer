# VIDEO 18: Pine Script Tutorial — From Indicator to Strategy to Production

**Source:** YouTube Trading Education (transcript provided 2026-03-07 08:29 UTC)
**Status:** Advanced Pine Script + Strategy Development + Production Migration
**Difficulty:** Intermediate → Advanced
**Prerequisites:** Basic Pine Script (Video 17)

---

## 🎯 WHAT YOU'LL LEARN

1. ✅ Build indicators in Pine Script
2. ✅ Develop them into **backtestable strategies**
3. ✅ Optimize for market conditions
4. ✅ **Migrate to production** via exchange APIs

---

## 📍 PART 1: TradingView Setup

### Choose Your Market
**Recommendation:** Use what you know best
- **Forex:** EUR/USD
- **Stocks:** Your familiar ticker
- **Crypto:** BTC/USD (used in tutorial, 1H timeframe)

**Timeframe:** 1H for detail (tutorial uses 1H)

---

## 📝 PART 2: First Pine Script Indicator

### Basic Moving Average Indicator

```pinescript
//@version=5
indicator("My MA Indicator", overlay=true)

// Overlay = true → draws on price chart (not below)

// Define moving averages
fastMA = ta.sma(close, 24)   // Simple MA, 24 periods, close price
slowMA = ta.sma(close, 200)  // Simple MA, 200 periods

// Plot them
plot(fastMA, "Fast MA", color=color.blue)
plot(slowMA, "Slow MA", color=color.yellow)
```

**What is `overlay=true`?**
- `true` = Plots **on** the price chart
- `false` = Plots in **separate panel** below

---

## 📊 PART 3: Pine Script Fundamentals

### Series Data Concept

**TradingView builds around "series data":**

| Variable | Description |
|----------|-------------|
| `open` | Opening price of period |
| `high` | Highest price of period |
| `low` | Lowest price of period |
| `close` | Closing price of period |
| `volume` | Trading volume |
| `time` | Timestamp |

**Execution Model:**
- Script executes **on every candle**
- For 100 candles → script runs 100 times
- Calculates from start to end of each period

### Built-in Functions

**Technical Analysis Functions:**
```pinescript
// RSI (Relative Strength Index)
rsiValue = ta.rsi(close, 14)

// Moving Averages
ta.sma(source, length)    // Simple MA
ta.ema(source, length)    // Exponential MA
ta.wma(source, length)    // Weighted MA
ta.vwap()                 // Volume Weighted Average Price

// Average True Range (ATR)
atrValue = ta.atr(14)
```

**Full function list in TradingView reference manual**

### Inputs (User Customization)

```pinescript
// Create input for fast MA length
fastLength = input.int(24, "Fast MA Length", minval=5, maxval=50)
fastMA = ta.sma(close, fastLength)
```

**Benefits:**
- Change values without editing code
- UI-friendly settings panel
- Share code with customizable parameters

### Execution Timing

**Standard:** Executes at **close of every candle**

**Real-time option:**
```pinescript
//@version=5
calc_on_every_tick = true  // Execute on every tick (live data)
```

---

## 🎯 PART 4: Convert Indicator → Strategy

### Strategy Syntax

```pinescript
//@version=5
strategy("My Strategy", overlay=true, 
         initial_capital=1000, 
         default_qty_type=strategy.percent_of_equity,
         default_qty_value=10)

// Your indicator logic here...

// Entry condition
crossover = ta.crossover(fastMA, slowMA)

// Execute trade
if crossover
    strategy.entry("Long", strategy.long)
    strategy.exit("Exit", "Long", stop=close * 0.97, limit=close * 1.12) // 3% SL, 12% TP
```

### Strategy Parameters

| Parameter | Purpose |
|-----------|---------|
| `initial_capital` | Starting money for backtest |
| `default_qty_type` | Position sizing method |
| `default_qty_value` | Position size value |

### Quantity Types:
- `strategy.fixed` = Fixed number of contracts/shares
- `strategy.percent_of_equity` = % of available capital
- `strategy.cash` = Fixed dollar amount

---

## 🔧 PART 5: Strategy Components

### Entry Conditions

```pinescript
// Condition 1: EMA crossover
inUptrend = emaFast > emaSlow

// Condition 2: RSI filter
rsiOk = ta.rsi(close, 14) > 40

// Condition 3: Time filter (only trade after Dec 15, 2020)
timeCondition = timestamp(year, month, dayofmonth, hour, minute) >= 
              timestamp(2020, 12, 15, 0, 0)

// Condition 4: Not already in trade
notInTrade = strategy.position_size == 0

// Combined entry
if inUptrend and rsiOk and timeCondition and notInTrade
    strategy.entry("Long", strategy.long)
```

### Exit Conditions

**Two approaches:**

#### Approach 1: Fixed Stop/Take Profit
```pinescript
strategy.exit("TP/SL", "Long", 
              stop=close * 0.97,      // 3% below entry
              limit=close * 1.12)      // 12% above entry
```

#### Approach 2: Conditional Exit
```pinescript
// Exit if trend reverses
if emaFast < emaSlow
    strategy.close("Long")

// Exit if 5% drop from previous bar
if close < close[1] * 0.95
    strategy.close("Long")

// Close ALL positions
strategy.close_all()
```

---

## 📈 PART 6: Strategy Optimization

### Problem: Basic MA Strategy Underperforms

**Observation:** Simple crossover strategy:
- **Net profit:** +35%
- **Buy & Hold:** +47%
- **Missing:** Huge portions of bull run
- **Chop:** Losing money in sideways markets

### Solution: Enhanced Conditions

#### Condition 1: Trend Confirmation
```pinescript
// Fast EMA > SMA (not just slow MA)
// EMA = recent weight, SMA = average
// If EMA > SMA: recent momentum +ve
recentMomentum = emaFast > smaFast

trendCondition = emaFast > emaSlow and recentMomentum
```

#### Condition 2: ATR Stop Loss
```pinescript
// Use ATR instead of fixed percentage
atr14 = ta.atr(14)
stopLoss = close - (atr14 * 3)  // 3x ATR below entry
```

#### Condition 3: Background Coloring
```pinescript
// Color background when in trade
bgColor = strategy.position_size > 0 ? color.new(color.green, 90) : na
bgcolor(bgColor)
```

### Optimization Results:
| Metric | Basic Strategy | Optimized |
|--------|---------------|-----------|
| Net Profit | +35% | **+200%** |
| Buy & Hold | +47% | +47% |
| Sharpe Ratio | Low | **High** |
| Capture | Partial | Full bull run |

**Key insight:** Trend-following strategies work in **trending** markets, get destroyed in **sideways** markets.

---

## 🔮 PART 7: Market Condition Adaptation

### Trend Following vs Mean Reversion

| Market | Best Strategy |
|--------|---------------|
| **Trending** (bull/bear) | MA crossover, momentum |
| **Sideways** | Mean reversion, breakouts |
| **Volatility** | Breakout strategies |

### Dynamic Strategy Logic
```pinescript
// Detect if trending
isTrending = adx > 25  // ADX >25 = strong trend

if isTrending
    useTrendFollowingStrategy()
else
    useMeanReversionStrategy()
```

---

## 🚀 PART 8: Production Migration

### TradingView Limitations
**Author's opinion:** TradingView is best for **development/testing**, not production execution.

**Better execution platforms:** Dedicated servers with exchange APIs

### The Migration Path

#### Step 1: Strategy → Alert
```pinescript
// Create alerts for manual execution
alertcondition(emaFast > emaSlow, title="Long Signal", 
               message='{"action": "buy", "price": {{close}}}')
```

**TradingView Alerts:**
- Send SMS, email, webhook
- Manual execution based on alerts

#### Step 2: Automated via Trading Panel
**Not recommended** by author — not robust for serious systems

#### Step 3: Custom Server (Recommended)

**Architecture:**
```
Exchange API
    ↓
Data Sanitizer (clean data)
    ↓
Trading Bot (Pine Script logic → Python/Node.js)
    ↓
Execution Strategy (order management)
    ↓
Security/Backup
    ↓
Web UI/Analytics
```

#### Step 4: Code Translation (Pine → Python/Node.js)

**Example Python equivalent:**
```python
def calculate_ema(prices, period):
    """Exponential Moving Average"""
    multiplier = 2 / (period + 1)
    ema = prices[0]
    for price in prices[1:]:
        ema = (price - ema) * multiplier + ema
    return ema

def should_enter(fast_ema, slow_ema, price):
    """Entry condition equivalent to Pine Script"""
    return fast_ema > slow_ema

# Connect to exchange API
exchange = ccxt.binance({'apiKey': 'xxx', 'secret': 'xxx'})

while True:
    # Fetch data
    ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1h')
    closes = [candle[4] for candle in ohlcv]
    
    # Calculate indicators
    fast_ema = calculate_ema(closes, 24)
    slow_ema = calculate_ema(closes, 200)
    
    # Check conditions
    if should_enter(fast_ema, slow_ema, closes[-1]):
        # Execute order
        exchange.create_market_buy_order('BTC/USDT', 0.01)
    
    time.sleep(3600)  # Wait 1 hour
```

---

## ♻️ PART 9: Advanced Concepts

### Smoothing Algorithm
```pinescript
// Simple smoothing (like EMA foundation)
smoothed = (close + close[1]) / 2 * 0.5 + close[1] * 0.5
// ^ 0.5 factor adjustable for recent vs previous weight
```

### Dynamic Coloring
```pinescript
// Change color based on condition
lineColor = close > open ? color.green : color.red
plot(close, "Price", color=lineColor, linewidth=2)

// Background color
bgColor = close > emaFast ? color.new(color.green, 90) : 
          color.new(color.red, 90)
bgcolor(bgColor)
```

### Multiple Conditions with AND/OR
```pinescript
// AND: All conditions must be true
condition1 = close > emaFast
condition2 = volume > sma(volume, 20)
condition3 = rsi < 70

enterLong = condition1 and condition2 and condition3

// OR: Either condition can be true
exitPosition = close < emaSlow or rsi > 80
```

---

## 📋 COMPLETE STRATEGY TEMPLATE

```pinescript
//@version=5
strategy("Complete Strategy Example", 
         overlay=true, 
         initial_capital=1000,
         default_qty_type=strategy.percent_of_equity,
         default_qty_value=10,
         commission_type=strategy.commission.percent,
         commission_value=0.1)

// ═════════════════════════════════════════════════════════
// INPUTS
// ═════════════════════════════════════════════════════════
fastLength = input.int(24, "Fast EMA Length", minval=5, maxval=50)
slowLength = input.int(200, "Slow EMA Length", minval=50, maxval=300)
atrLength = input.int(14, "ATR Length", minval=5, maxval=30)
atrMultiplier = input.float(3.0, "ATR Multiplier for SL", minval=1.0, maxval=5.0)

// ═════════════════════════════════════════════════════════
// INDICATORS
// ═════════════════════════════════════════════════════════
emaFast = ta.ema(close, fastLength)
emaSlow = ta.ema(close, slowLength)
atr14 = ta.atr(atrLength)

// ═════════════════════════════════════════════════════════
// ENTRY CONDITIONS
// ═════════════════════════════════════════════════════════
// Primary: Fast EMA > Slow EMA (trend up)
trendUp = emaFast > emaSlow

// Secondary: Momentum confirmed
recentMomentum = emaFast > ta.sma(close, fastLength)

// Filter: Not already in position
notInPosition = strategy.position_size == 0

// Time filter (optional)
timeInRange = time >= timestamp(2020, 12, 15, 0, 0)

// Combined entry
enterLong = trendUp and recentMomentum and notInPosition and timeInRange

// ═════════════════════════════════════════════════════════
// EXIT CONDITIONS
// ═════════════════════════════════════════════════════════
// Dynamic stop loss
stopLoss = close - (atr14 * atrMultiplier)
takeProfit = close + (atr14 * atrMultiplier * 4) // 1:4 R:R

// Trend reversal exit
exitOnReversal = emaFast < emaSlow

// Combined exit (OR logic)
exitLong = exitOnReversal

// ═════════════════════════════════════════════════════════
// EXECUTION
// ═════════════════════════════════════════════════════════
// Entry
if enterLong
    strategy.entry("Long", strategy.long)
    strategy.exit("TP/SL", "Long", stop=stopLoss, limit=takeProfit)

// Exit
if exitLong and strategy.position_size > 0
    strategy.close("Long")

// ═════════════════════════════════════════════════════════
// VISUALIZATION
// ═════════════════════════════════════════════════════════
// Plot MAs
plot(emaFast, "Fast EMA", color=color.blue)
plot(emaSlow, "Slow EMA", color=color.orange)

// Background in trade
bgcolor(strategy.position_size > 0 ? color.new(color.green, 90) : na)

// Alerts
alertcondition(enterLong, "Long Signal", "Strategy: Enter Long")
alertcondition(exitLong, "Exit Signal", "Strategy: Exit Position")
```

---

## 🎓 KEY TAKEAWAYS

1. **Pine Script → Strategy → Production** is the full pipeline
2. **Backtesting reveals truth:** Basic strategies often underperform buy & hold
3. **Optimization comes from conditions:** Multiple confirmations beat simple signals
4. **Market conditions matter:** Trend following vs mean reversion
5. **TradingView for testing:** Migrate to server + APIs for real trading
6. **Risk management essential:** ATR-based stops, conditional exits
7. **Visual feedback helps:** Background colors, clear entry/exit markers

---

## 🔗 INTEGRATION WITH CRYPTONIO'S SYSTEM

### From Pine Script Basics (Video 17):
✅ Indicators
✅ Plotting
✅ Colors

### From This Video (Video 18):
✅ **Strategies ← NEW**
✅ **Backtesting ← NEW**
✅ **Entry/Exit logic ← NEW**
✅ **Risk management (ATR stops) ← NEW**
✅ **Production migration path ← NEW**

### Next Step for 190-Point System:
Convert `CRYPTONIO_190POINT_CONFLUENCE_INDICATOR.pine` → **Strategy**

**Files needed:**
1. Indicator version (✅ done)
2. **Strategy version** (add entry/exit with scored thresholds)
3. **Backtest results** (optimize threshold, timeframe)
4. **Production version** (Python/Node.js with exchange APIs)

---

## 📚 RESOURCES

**Open Source Code:** In video description/blog post
**Full Tutorial:** Detailed blog post with copy-paste code
**TradingView Reference:** Pine Script v5 manual

---

**Status:** 🎓 **Pine Script Mastery — Advanced Complete**

**Cryptonio Note:** *Now I have the full pipeline. Indicator built, strategy logic understood, production path clear. The 190-point system can now become executable.* 💎🚀

---

**Commit:** `558ce9f` (Video 18 research complete, ready to build strategy version)
