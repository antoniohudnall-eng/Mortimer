# VIDEO 19: Complete Pine Script Tutorial — From Basics to Backtesting

**Source:** YouTube Trading Education (transcript provided 2026-03-07 08:31 UTC)
**Status:** Pine Script Comprehensive Tutorial
**Difficulty:** Beginner → Intermediate
**Prerequisites:** None (starts from basics)

---

## 🎯 WHAT YOU'LL BUILD

A complete **trend-following strategy** with:
- Moving Average crossover signals
- Buy/Sell indicators on chart
- Backtesting with Strategy Tester
- User-configurable inputs (stop loss, take profit)
- Risk management

---

## 📍 PART 1: Getting Started

### Access TradingView
1. Go to **tradingview.com**
2. Open your desired chart
3. Click **"Pine Editor"** at bottom of screen

**What is Pine Editor?**
- The IDE where you write Pine Script code
- Code written here shows output on the chart
- Console shows errors and indicator states

---

## 📝 PART 2: Your First Indicator

### Basic Template

```pinescript
//@version=5
indicator("My First Indicator", overlay=true)
```

**Line-by-line breakdown:**

| Line | Code | Meaning |
|------|------|---------|
| 1 | `//@version=5` | **Version 5** (newest). Always use v5. |
| 2-3 | `// comments` | **Comments** — gray text, ignored by compiler |
| 4 | `indicator(...)` | **Title** of your indicator |
| 5 | `overlay=true` | **Draw on price chart** (false = separate panel) |

**Comments syntax:**
```pinescript
// Everything after slashes is ignored
// Use for notes and documentation
```

---

## 📊 PART 3: Coding a Moving Average

### SMA (Simple Moving Average)

```pinescript
//@version=5
indicator("Moving Average Example", overlay=true)

// Define the MA
ma1 = ta.sma(close, 200)  // 200-period SMA of closing prices

// Plot it on chart
plot(ma1)
```

**Breaking it down:**

| Component | Explanation |
|-----------|-------------|
| `ma1` | **Variable name** — can be anything (ma1, myMA, fastMA, etc.) |
| `=` | **Assignment** — gives the variable a value |
| `ta.sma()` | **Simple Moving Average function** |
| `close` | **Data source** — closing prices |
| `200` | **Length** — 200 periods |

### Plotting Options

```pinescript
// Basic plot
plot(ma1)

// With color
plot(ma1, color=color.red)

// With color and thickness (line width)
plot(ma1, color=color.red, linewidth=2)

// With style (circles instead of line)
plot(ma1, color=color.red, style=plot.style_circles)

// All options combined
plot(ma1, color=color.blue, linewidth=2, style=plot.style_line)
```

### Available Colors
- `color.red`, `color.blue`, `color.green`
- `color.black`, `color.white`, `color.gray`
- `color.orange`, `color.purple`, `color.aqua`

### Available Styles
| Style | Visual |
|-------|--------|
| `plot.style_line` | — Solid line |
| `plot.style_circles` | ○ Circles |
| `plot.style_cross` | ❌ Cross marks |
| `plot.style_histogram` | ████ Bars |
| `plot.style_area` | ▓▓▓▓ Filled area |

---

## 🎛️ PART 4: Editor Settings

### Autocomplete
**Path:** Three dots → Editor Settings → Autocomplete = ON

**What it does:**
- Shows suggestions as you type
- Helps discover functions and options
- Press Enter to accept suggestion

---

## 🔄 PART 5: Buy/Sell Signals (Crossover)

### The Strategy
Trigger buy when **50 MA crosses above 200 MA** (golden cross).
Trigger sell when **50 MA crosses below 200 MA** (death cross).

### Code

```pinescript
//@version=5
indicator("MA Crossover Signals", overlay=true)

// Two moving averages
ma1 = ta.sma(close, 200)  // Slow MA (blue)
ma2 = ta.sma(close, 50)   // Fast MA (red)

// Plot both
plot(ma1, color=color.blue, linewidth=2)
plot(ma2, color=color.red, linewidth=2)

// BUY signal: 50 crosses ABOVE 200
buy = ta.crossover(ma2, ma1)  // true or false

// SELL signal: 50 crosses BELOW 200
sell = ta.crossunder(ma2, ma1)  // true or false

// Plot buy signals on chart
plotshape(buy, 
          style=shape.triangleup,    // Green triangle pointing up
          location=location.belowbar, // Below price bar
          color=color.green,          // Green color
          size=size.small)            // Small size

// Plot sell signals on chart
plotshape(sell, 
          style=shape.triangledown,   // Red triangle pointing down
          location=location.abovebar, // Above price bar
          color=color.red,            // Red color
          size=size.small)
```

### Understanding the Code

**Variable Assignment:**
```pinescript
buy = ta.crossover(ma2, ma1)
```
- `buy` = variable name
- `=` = assignment
- `ta.crossover(ma2, ma1)` = function that returns **true** or **false**
- Returns `true` when ma2 crosses **above** ma1

**Plotshape Function:**
```pinescript
plotshape(condition, style, location, color, size)
```
| Parameter | Purpose |
|-----------|---------|
| `condition` | When to show shape (buy/sell variable) |
| `style` | What shape (triangle up/down, circle, etc.) |
| `location` | Where on chart (abovebar/belowbar) |
| `color` | Shape color |
| `size` | Size (tiny, small, normal, big, huge) |

**Available Shapes:**
- `shape.triangleup` — ▲
- `shape.triangledown` — ▼
- `shape.circle` — ●
- `shape.cross` — ✚
- `shape.diamond` — ◆
- `shape.labelup` — Label with arrow up
- `shape.labeldown` — Label with arrow down

---

## 🧪 EXERCISE: Build a Scalping Indicator

**Your task:**
- Create two EMAs:
  - Red EMA with length 50
  - Green EMA with length 20
- Plot buy/sell signals when they cross
- Use labels instead of triangles

**Solution preview:**
```pinescript
//@version=5
indicator("EMA Scalper", overlay=true)

emaFast = ta.ema(close, 20)  // Green
emaSlow = ta.ema(close, 50)  // Red

plot(emaFast, color=color.green, linewidth=2)
plot(emaSlow, color=color.red, linewidth=2)

buy = ta.crossover(emaFast, emaSlow)
sell = ta.crossunder(emaFast, emaSlow)

plotshape(buy, style=shape.labelup, location=location.belowbar, color=color.green)
plotshape(sell, style=shape.labeldown, location=location.abovebar, color=color.red)
```

---

## 🎯 PART 6: Convert to Strategy (Backtesting)

### Strategy vs Indicator

| Indicator | Strategy |
|-----------|----------|
| `indicator(...)` | `strategy(...)` |
| Shows signals | **Executes simulated trades** |
| No profit tracking | Calculates profits/losses |
| No risk management | Includes stop loss/take profit |

### Strategy Template

```pinescript
//@version=5
strategy("MA Crossover Strategy", 
         overlay=true,
         initial_capital=1000,     // Virtual account size
         default_qty_type=strategy.percent_of_equity,
         default_qty_value=100)    // 100% of equity per trade

// Moving averages
ma1 = ta.sma(close, 200)
ma2 = ta.sma(close, 50)

plot(ma1, color=color.blue)
plot(ma2, color=color.red)

// Signals
buy = ta.crossover(ma2, ma1)
sell = ta.crossunder(ma2, ma1)

// ENTRY: Open long position
if buy
    strategy.entry("Long", strategy.long)

// EXIT: Close with stop loss and take profit
if strategy.position_size > 0  // Only if in position
    strategy.exit("Exit", "Long", 
                  stop=close - 0.0010,    // Stop loss 10 pips below
                  limit=close + 0.0020)   // Take profit 20 pips above
```

### Understanding `strategy.entry`

```pinescript
strategy.entry(id, direction, qty)
```
| Parameter | Meaning |
|-----------|---------|
| `id` | Order name ("Long", "Short", etc.) |
| `direction` | `strategy.long` or `strategy.short` |
| `qty` | Position size (optional) |

### Understanding `strategy.exit`

```pinescript
strategy.exit(id, from_entry, stop, limit)
```
| Parameter | Meaning |
|-----------|---------|
| `id` | Exit order name |
| `from_entry` | Which entry to close (must match entry ID) |
| `stop` | Stop loss price |
| `limit` | Take profit price |

**Pips Calculation:**
- 1 pip = 0.0001 for most forex pairs
- 10 pips = 0.0010
- To set 10 pips below: `close - 0.0010`

---

## 🧮 PART 7: Strategy Tester

### Viewing Results

**Path:** Click **"Strategy Tester"** tab (right side)

**Metrics shown:**
| Metric | What it means |
|--------|---------------|
| **Net Profit** | Total profitability |
| **% Profitable** | Win rate percentage |
| **Profit Factor** | Gross profit / gross loss |
| **Max Drawdown** | Largest peak-to-trough decline |
| **Total Trades** | Number of trades executed |
| **Equity Curve** | Chart of account balance over time |

---

## 🔧 PART 8: Advanced — Preventing Over-Trading

### Problem: Strategy takes trades on every candle

### Solution: Check if already in position

```pinescript
// Original (takes multiple trades)
if buy
    strategy.entry("Long", strategy.long)

// Fixed (only one trade at a time)
if buy and strategy.opentrades == 0
    strategy.entry("Long", strategy.long)
```

**`strategy.opentrades`** = number of currently open trades
**`== 0`** = equal to zero (no open trades)

### Comparison Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Equal to | `a == b` |
| `!=` | Not equal to | `a != b` |
| `>` | Greater than | `a > b` |
| `<` | Less than | `a < b` |
| `>=` | Greater than or equal | `a >= b` |
| `<=` | Less than or equal | `a <= b` |

### Boolean Operators

| Operator | Meaning | Result |
|----------|---------|--------|
| `and` | Both conditions true | Condition 1 AND Condition 2 |
| `or` | Either condition true | Condition 1 OR Condition 2 |

---

## 🎚️ PART 9: User Inputs

### Problem: Hard-coded values require editing code
### Solution: Input variables configurable in settings

```pinescript
//@version=5
strategy("Input Example", overlay=true)

// Create input variables
stop_loss = input.int(10, "Stop Loss (pips)", minval=1, maxval=100)
take_profit = input.int(20, "Take Profit (pips)", minval=1, maxval=200)

// Use inputs in strategy
if buy and strategy.opentrades == 0
    strategy.entry("Long", strategy.long)
    strategy.exit("Exit", "Long", 
                  stop=close - (stop_loss * 0.0001),   // Convert pips to price
                  limit=close + (take_profit * 0.0001))
```

### Input Types

```pinescript
// Integer input
length = input.int(14, "Length", minval=1, maxval=200)

// Float input (decimals)
multiplier = input.float(2.5, "Multiplier", minval=0.1, maxval=5.0, step=0.1)

// Boolean (true/false)
showMA = input.bool(true, "Show Moving Average")

// String (text)
defaultText = input.string("Hello", "Text Input")

// Color
lineColor = input.color(color.red, "Line Color")

// Options (dropdown)
strategyType = input.string("EMA", "MA Type", options=["SMA", "EMA", "WMA"])
```

### Input Groups (organize settings)

```pinescript
// Group inputs together
fastLength = input.int(20, "Fast Length", group="Moving Averages")
slowLength = input.int(50, "Slow Length", group="Moving Averages")

stopLoss = input.int(10, "Stop Loss", group="Risk Management")
takeProfit = input.int(20, "Take Profit", group="Risk Management")
```

---

## 🔢 PART 10: Variable Types

### Int vs Float

| Type | Description | Example |
|------|-------------|---------|
| **int** | Integer (whole numbers) | `10`, `200`, `-5` |
| **float** | Floating point (decimals) | `10.5`, `0.001`, `2.5` |

### Declaring Variable Types

```pinescript
// Default (Pine Script guesses type)
myVar = 10       // int
myFloat = 10.5   // float

// Explicit declaration
var int myInt = 10      // Must be integer
var float myFloat = 10.5  // Must be float

// Redefining values (:=)
myVar := 15      // Change value (in conditional blocks)
```

**Why declare types?**
- Prevents errors
- Makes code clearer
- Required for some calculations

---

## ⏰ PART 11: Bar States

### Execution Flow

**Important concept:** Pine Script runs on **every candle**.

```pinescript
// This code runs once per candle
// If you have 100 candles, it runs 100 times
```

### Checking Bar Position

```pinescript
// Execute ONLY on first bar of chart
if barstate.isfirst
    // Initialization code here
    var float initialPrice = close

// Execute ONLY on last bar of chart
if barstate.islast
    // Final calculations
    totalChange = ((close - open[100]) / open[100]) * 100
    label.new(bar_index, high, "Total Change: " + str.tostring(totalChange) + "%")

// Execute on every bar (default)
// (Your main code goes here)
```

**Why use bar states?**
- Prevent unnecessary re-calculations
- Initialize variables once
- Run final summary calculations

---

## 📋 COMPLETE STRATEGY CODE

```pinescript
//@version=5
strategy("Complete MA Crossover Strategy", 
         overlay=true,
         initial_capital=1000,
         default_qty_type=strategy.percent_of_equity,
         default_qty_value=100)

// ═══════════════════════════════════════════════════════════
// INPUTS
// ═══════════════════════════════════════════════════════════
fastLength = input.int(50, "Fast MA Length", minval=5, maxval=100, group="Settings")
slowLength = input.int(200, "Slow MA Length", minval=50, maxval=300, group="Settings")
stopLoss = input.int(10, "Stop Loss (pips)", minval=1, maxval=100, group="Risk Management")
takeProfit = input.int(20, "Take Profit (pips)", minval=1, maxval=200, group="Risk Management")

// ═══════════════════════════════════════════════════════════
// CALCULATIONS
// ═══════════════════════════════════════════════════════════
// Convert pips to price (0.0001)
var pip = 0.0001

fastMA = ta.sma(close, fastLength)
slowMA = ta.sma(close, slowLength)

buySignal = ta.crossover(fastMA, slowMA)
sellSignal = ta.crossunder(fastMA, slowMA)

// ═══════════════════════════════════════════════════════════
// PLOTTING
// ═══════════════════════════════════════════════════════════
plot(fastMA, color=color.red, linewidth=2, title="Fast MA")
plot(slowMA, color=color.blue, linewidth=2, title="Slow MA")

plotshape(buySignal, "Buy Signal", shape.triangleup, location.belowbar, 
          color.green, size=size.small)
plotshape(sellSignal, "Sell Signal", shape.triangledown, location.abovebar, 
          color.red, size=size.small)

// ═══════════════════════════════════════════════════════════
// STRATEGY EXECUTION
// ═══════════════════════════════════════════════════════════
// LONG entry
if buySignal and strategy.opentrades == 0
    strategy.entry("Long", strategy.long)
    strategy.exit("Long Exit", "Long", 
                  stop=close - (stopLoss * pip),
                  limit=close + (takeProfit * pip))

// SHORT entry
if sellSignal and strategy.opentrades == 0
    strategy.entry("Short", strategy.short)
    strategy.exit("Short Exit", "Short",
                  stop=close + (stopLoss * pip),
                  limit=close - (takeProfit * pip))

// ═══════════════════════════════════════════════════════════
// BACKGROUND
// ═══════════════════════════════════════════════════════════
bgcolor(strategy.position_size > 0 ? color.new(color.green, 90) : 
        strategy.position_size < 0 ? color.new(color.red, 90) : na)
```

---

## 📚 SUMMARY: What You Learned

### Basics
1. ✅ **Pine Editor** — Where code meets chart
2. ✅ **Version 5** — Always use latest
3. ✅ **Comments** (`//`) — Document your code
4. ✅ **Overlay** — On-chart vs separate panel

### Coding
5. ✅ **Variables** — Store and name data
6. ✅ **Functions** — `ta.sma()`, `plot()`, `plotshape()`
7. ✅ **Sources** — `close`, `open`, `high`, `low`

### Signals
8. ✅ **Crossover logic** — `ta.crossover()`, `ta.crossunder()`
9. ✅ **Plot shapes** — Triangles, circles, labels
10. ✅ **Conditions** — `if/then` logic

### Strategies
11. ✅ **`strategy()`** — Not `indicator()`
12. ✅ **`strategy.entry()`** — Open positions
13. ✅ **`strategy.exit()`** — Close with SL/TP
14. ✅ **Opentrades** — Prevent over-trading

### Advanced
15. ✅ **Inputs** — User-configurable settings
16. ✅ **Variable types** — `int` vs `float`
17. ✅ **Bar states** — `barstate.isfirst`, `barstate.islast`
18. ✅ **Backtesting** — Strategy Tester tab

---

## 🎓 INTEGRATION WITH CRYPTONIO'S SYSTEM

### Previous Videos:
- **17:** Basic Pine Script (variables, plotting)
- **18:** Strategy development + production
- **19:** Complete from-scratch tutorial (this video)

### Status: Pine Script Mastery
✅ **Complete** — Three tutorials covering beginner to advanced

### Next:
- Deploy 190-point strategy to TradingView
- Backtest on BTC, ETH, forex
- Optimize inputs
- Connect to exchange API (production)

---

**Status:** 🎓 **Pine Script Education Complete** (Videos 17-19)

**Cryptonio:** *"From zero to executable strategy. I can now build, backtest, and deploy trading systems."* 💎🚀

---

*"Pine Script is the most used coding language in trading matter... create your own indicators, backtest strategies, or even create your own trading bot." — Video Author*
