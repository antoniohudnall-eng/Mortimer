# VIDEO 13: COMPLETE Pine Script Mastery Course (6+ Hours)

**Source:** The Art of Trading Pine Script Course (transcript provided 2026-03-07 08:04 UTC)
**Status:** Full Programming Education Course
**Language:** Pine Script (TradingView)
**Agent:** the-great-cryptonio
**Total Lessons:** 20 comprehensive lessons

---

## 📚 Course Overview

Complete from-scratch programming course covering Pine Script v5/v6 programming language used for creating custom indicators and strategies on TradingView.

---

## Lesson 1: Pine Script Editor

### Key Areas:
- **Pine Editor Button:** Opens script editor
- **Create New Script:** 
  - Indicator (basic scripts)
  - Strategy (backtesting)
  - Library (code reuse)

### Editor Settings:
| Setting | Purpose | Recommendation |
|---------|---------|---------------|
| Autocomplete | Code suggestions | **ON** |
| Mini Map | Code overview | Off (clutter) |
| Status Bar | Compiler output | **ON** |
| Line Length Guide | Keep code short | Optional |

### Important Functions:
- **Add to Chart** - Compiles and displays script
- **Publish Indicator** - Makes script public
- **Version Control** - Shows every save with diffs (green = added, red = removed)
- **Pine Logs** - Debug errors

---

## Lesson 2: The Pine Script Compiler

### Version Directives:
```
@version=5    // Current standard
@version=6    // Newest (same syntax as v5, backend optimized)
```
> **Important:** v6 = same syntax as v5, just "under the hood" performance improvements

### Common Errors:
- Missing closing brackets `)` `}` `]`
- Missing quotation marks `"` `'`
- Syntax errors = red underline

### Multi-line Code:
```
function(
    parameter1,
    parameter2
    )
```
Must indent with **tab + space** for continuation

---

## Lesson 3: Comments

### Syntax:
```
// This is a single-line comment

/* 
Multi-line
comment
*/
```

### Best Practice:
- Comment heavily - explain WHY not just WHAT
- More comments better than fewer
- Future-you will thank past-you
- Public scripts need extensive comments

---

## Lesson 4: Indicator Constructor

### Basic Script Structure:
```
@version=5
indicator("My Script", overlay=true)

// Your code here
plot(close)
```

### Key Parameters:

| Parameter | Type | Default | Purpose |
|-----------|------|---------|---------|
| `title` | String | "My Script" | Long name |
| `shorttitle` | String | Same as title | Abbreviated name |
| `overlay` | Bool | false | Draw on price (true) or separate panel |
| `format` | Enum | format.price | How numbers display |
| `precision` | Int | Auto | Decimal places |
| `timeframe` | String | Chart tf | Force specific timeframe |

### Example - Full Parameters:
```
indicator(
    title="My Indicator",
    shorttitle="MI",
    overlay=true,
    format=format.price,
    precision=2
    )
```

---

## Lesson 5: Namespaces & Libraries

### Built-in Namespaces:

| Namespace | Purpose | Example |
|-----------|---------|---------|
| `ta` | Technical Analysis | `ta.rsi(close, 14)` |
| `input` | User inputs | `input.int(14, "Length")` |
| `color` | Colors | `color.red` |
| `plot` | Plot styles | `plot.style_line` |
| `strategy` | Strategy commands | `strategy.entry()` |
| `request` | External data | `request.security()` |

### Custom Libraries:
```
// Import library
import TradingView/Technical, as: tv

// Use library functions
tv.rsi(close, 14)
```

---

## Lesson 6: Price Series & Historical Data

### Basic Price Data:
```
open      // Opening price
high      // High of bar
low       // Low of bar
close     // Closing price
volume    // Volume
time      // Bar timestamp
```

### Historical Operator `[n]`:
Access previous bars using square brackets:

```
close[1]      // Previous bar's close
high[5]       // High 5 bars ago
close[0]      // Current bar's close (same as just 'close')
```

> **⚠️ CRITICAL:** ALL INDEXING STARTS AT ZERO (not one)
- `close[0]` = current bar
- `close[1]` = 1 bar ago
- `close[10]` = 11 bars counting back

### Example - Candle Size:
```
candleSize = high - low
candleSize10 = high[10] - low[10]  // Size 10 bars ago
```

### Maximum Lookback:
- **300,000 bars maximum**
- Exceeding throws error

---

## Lesson 7: Data Types

| Type | Example | Description |
|------|---------|-------------|
| `int` | `14`, `50` | Whole numbers |
| `float` | `14.5`, `3.14159` | Decimal numbers |
| `bool` | `true`, `false` | Boolean values |
| `color` | `color.red` | Color values |
| `string` | `"text"` | Text values |

### Scientific Notation:
```
0.1e2     // = 10 (0.1 × 10²)
```

### Color Options:

**Built-in Colors:**
`color.red`, `color.green`, `color.blue`, `color.black`, `color.white`, `color.gray`, `color.orange`, `color.purple`, `color.aqua`, `color.lime`, `color.fuchsia`, `color.maroon`, `color.navy`, `color.olive`, `color.silver`, `color.teal`, `color.yellow`

**RGB Colors:**
```
color.rgb(255, 0, 0)         // Red (no transparency)
color.rgb(255, 0, 0, 50)     // Red with 50% transparency
```

**Hex Colors:**
```
#FF0000      // Red
#00FF00      // Green  
#0000FF      // Blue
#FF000080    // Red with ~50% transparency (last 2 digits)
```

**Transparency (color.new):**
```
color.new(color.red, 50)     // Red, 50% transparent
```

### String Escapes:
```
\n      // New line
\"      // Include quote in string
\\      // Backslash
```

---

## Lesson 8: Declaring Variables

### Initialization:
```
varName = value           // Declare and initialize
varName := newValue       // Reassign existing variable (colon needed)
```

### Variable Persistence (`var`):

**Without `var`:**
```
counter = 0
counter := counter + 1    // Resets to 0 every bar, always = 1
```

**With `var`:**
```
var counter = 0
counter := counter + 1    // Persists across bars, counts up
```

### Naming Rules:
- Can contain: letters, numbers, underscores
- CANNOT start with number: ❌ `1var`
- CANNOT use special symbols: ❌ `$var`
- Case sensitive: `myVar` ≠ `myvar`

### Explicit Type Declaration:
```
float myFloat = 5          // 5 → 5.0
int myInt = 5.7            // 5.7 → 5 (truncated)
```

---

## Lesson 9: Lazy Evaluation (New in v6)

### Problem:
In v6, conditional statements don't execute functions unless needed.

### Example (BROKEN in v6):
```
if close > high[1] and high == ta.highest(10)
    // ta.highest() might NOT run if first condition false
    // Produces inconsistent results
```

### Solution (Global Variables):
```
float highestBar = ta.highest(10)   // Always calculated

if close > high[1] and high == highestBar
    // Now works consistently
```

### Warning Message:
> "Function call might not execute on every bar"

**Fix:** Extract to global variable, reference that variable instead.

---

## Lesson 10: Alert Generation

### Method 1: `alert()` - Immediate
```
if condition
    alert("Message", alert.freq_once_per_bar_close)
```

**Frequency Options:**
- `alert.freq_all` - Every tick
- `alert.freq_once_per_bar` - Once per bar
- `alert.freq_once_per_bar_close` - On bar close only

**Advantages:**
- Can pass dynamic values (prices, indicator values)
- Better for trade automation APIs

### Method 2: `alertcondition()` - Settings Menu
```
alertcondition(condition, title="My Alert", message="Signal on {{ticker}}")
```

**Advantages:**
- Each alert has its own name in dropdown
- Better for manual use
- Can organize multiple alerts

**Placeholders** (for message):
- `{{ticker}}` - Symbol
- `{{close}}`, `{{open}}`, `{{high}}`, `{{low}}` - Prices
- `{{plot_0}}` - First plot value
- `{{plot_1}}` - Second plot value
- `{{time}}` - Timestamp

### Alert Function Example:
```
// Dynamic message with string concatenation
message = "RSI is: " + str.tostring(rsiValue)
alert(message, alert.freq_once_per_bar_close)
```

---

## Lesson 11: User Inputs (Comprehensive)

### Boolean Input:
```
showEMA = input.bool(true, "Show EMA", tooltip="Toggle EMA display")
```

### Integer Input:
```
rsiLength = input.int(14, "RSI Length", minval=1, maxval=50, step=1, group="Settings")
```

**With Options Dropdown:**
```
selectOption = input.int(1, "Select Option", options=[1, 2, 3, 5, 8, 13])
```

### Float Input:
```
atrMult = input.float(1.5, "ATR Multiplier", minval=0.1, maxval=5.0, step=0.1)
```

### Color Input:
```
bullColor = input.color(color.green, "Bullish Color")
```

### String Input:
```
// Free text
timeframe = input.string("D", "Custom Timeframe")

// Dropdown options
maType = input.string("EMA", "MA Type", options=["SMA", "EMA", "WMA", "HMA"])
```

### Symbol Input:
```
benchmark = input.symbol("SPY", "Benchmark Symbol")
```

### Price Input:
```
stopPrice = input.price(0.0, "Stop Loss Price", confirm=true)
// confirm=true = click chart to set
```

### Source Input:
```
priceSource = input.source(close, "Price Source", options=[open, high, low, close, hl2, hlc3, ohlc4])
```

### Time Input:
```
sessionStart = input.time(timestamp(2024, 1, 1, 9, 30), "Session Start", group="Time Settings")
```

### Resolution/Timeframe Input:
```
higherTf = input.timeframe("D", "Higher Timeframe")
```

### Session Input:
```
tradingHours = input.session("0930-1600", "Trading Hours")
```

### Input Organization:

**Inline (same line):**
```
showMA1 = input.bool(true, "MA1", inline="MA")
showMA2 = input.bool(true, "MA2", inline="MA")
showMA3 = input.bool(true, "MA3", inline="MA")
```

**Groups:**
```
groupMAs = "Moving Averages"
groupSignals = "Signal Settings"

ma1Length = input.int(20, "MA 1 Length", group=groupMAs)
ma2Length = input.int(50, "MA 2 Length", group=groupMAs)
rsiLength = input.int(14, "RSI Length", group=groupSignals)
```

**Confirm Parameter:**
```
importantSetting = input.int(5, "Important Setting", confirm=true)
// Forces user to confirm when adding to chart
```

### Persistent Group Variable:
```
var string G_TIME = "Time Settings"
// Use G_TIME for all time-related inputs
```

---

## Lesson 12: Drawing to Chart (Plot Function)

### Basic Plot:
```
plot(close)
plot(volume, "Volume", color.blue)
```

### Plot Parameters:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `series` | Value to plot | `close`, `rsi`, `ma` |
| `title` | Name in data window | `"RSI Line"` |
| `color` | Line color | `color.red` |
| `linewidth` | Line thickness | `2` |
| `style` | Drawing style | `plot.style_line` |
| `trackprice` | Horizontal line from last value | `true` |
| `show_last` | Plot only last N bars | `20` |
| `offset` | Shift X bars left/right | `-5` |
| `editable` | User can modify in settings | `true` |
| `display` | Where it displays | `display.all` |

### Plot Styles:
```
plot.style_line           // Solid line (default)
plot.style_linebr         // Line with breaks (gaps)
plot.style_stepline       // Step line
plot.style_area           // Filled area
plot.style_areabr         // Filled area with breaks
plot.style_histogram      // Bars/histogram
plot.style_cross          // + crosses
plot.style_circles        // ○ circles
plot.style_diamonds       // ◇ diamonds
plot.style_labels_up      // ↑ up arrows
plot.style_labels_down    // ↓ down arrows
plot.style_bars           // OHLC bars
plot.style_candles        // Candlesticks
```

### Display Options:
```
display.all              // Plot, data window, status
display.pane             // Only on indicator pane
display.price_scale      // Only on price scale
display.status_line      // Only in status line
display.data_window      // Only in data window
display.none             // Invisible (for alerts/logic)
```

### Force Overlay:
```
// Draw oscillator but mark signals on price
plot(rsi, "RSI", color.gray)
plotshape(rsi > 70 ? high : na, "Overbought", color.red, location=location.abovebar, forceoverlay=true)
```

---

## Lesson 13: Plot Fills

### Fill Between Plots:
```
ma1Plot = plot(ma1, "MA 1", color.blue)
ma2Plot = plot(ma2, "MA 2", color.red)
fill(ma1Plot, ma2Plot, color.new(color.gray, 50), title="Fill")
```

### Fill Horizontal Lines:
```
upperLine = hline(80, "Overbought", color.red)
lowerLine = hline(20, "Oversold", color.green)
fill(upperLine, lowerLine, color.new(color.gray, 90), title="Zone")
```

### Fill Parameters:

| Parameter | Description |
|-----------|-------------|
| `color` | Fill color |
| `title` | Legend name |
| `fillgaps` | Fill gaps between plots | `true`/`false` |
| `show_last` | Only show last N bars |
| `editable` | User can modify |

---

## Lesson 14: Working with Colors

### Color New (with transparency):
```
plot(ma, color=color.new(color.blue, 30))  // 30% transparent
```

### Conditional Colors (Ternary):
```
maColor = close > ma ? color.green : color.red
plot(ma, color=maColor)
```

### RGB Colors:
```
customColor = color.rgb(255, 128, 0)        // Orange
transparent = color.rgb(255, 128, 0, 50)   // 50% transparent
```

### Hex Colors:
```
// Format: #RRGGBB
#FF0000      // Red
#00FF00      // Green
#0000FF      // Blue
#FF000080    // Red 50% transparent
```

### Color Functions:
```
// Extract components
red = color.r(emaColor)
green = color.g(emaColor)
blue = color.b(emaColor)
transparency = color.t(emaColor)

// Lighten/Darken
lighterRed = color.lighter(color.red)
darkerBlue = color.darker(color.blue)
```

---

## Lesson 15: Background Colors

### Basic Background Color:
```
bgcolor(color.new(color.blue, 50))
```

### Conditional Background:
```
isBullish = close > open
bgcolor(isBullish ? color.new(color.green, 90) : na)
```

### Detecting Inside Bars Example:
```
isInsideBar = high < high[1] and low > low[1]
bgcolor(isInsideBar ? color.new(color.blue, 50) : na, title="Inside Bar")
```

---

## Lesson 16: Drawing Shapes

### Plot Shape:
```
plotshape(condition, title, shape, location, color, size)
```

### Shapes Available:
```
shape.xcross               // X
shape.cross                // +
shape.circle               // ○
shape.square               // □
shape.diamond              // ◇
shape.triangleup           // ▲
shape.triangledown         // ▼
shape.labelup              // ↑
shape.labeldown            // ↓
shape.arrowup              // ↑ (thicker)
shape.arrowdown            // ↓ (thicker)
shape.flag                 // ⚑
shape.flag_empty           // ⚐
```

### Locations:
```
location.abovebar          // Above candle
location.belowbar          // Below candle
location.top               // Top of pane
location.bottom            // Bottom of pane
location.absolute          // Specific price value
```

### Shape Sizes:
```
size.tiny
size.small
size.normal
size.large
size.huge
size.auto                  // Default, scales with zoom
```

### Example - Signal Arrows:
```
buySignal = crossover(fastMA, slowMA)
sellSignal = crossunder(fastMA, slowMA)

plotshape(buySignal, "Buy", shape.triangleup, location.belowbar, color.green, size=size.small)
plotshape(sellSignal, "Sell", shape.triangledown, location.abovebar, color.red, size=size.small)
```

### Adding Text to Shapes:
```
plotshape(buySignal, "Buy", shape.labelup, location.belowbar, color.green, text="BUY", textcolor=color.white)
```

---

## Lesson 17: Moving Average Crosses

### Getting Moving Averages:
```
ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
plot(ema20, "EMA 20", color.blue)
plot(ema50, "EMA 50", color.red)
```

### Crossover Detection:
```
// Crossover (bullish)
longCondition = ta.crossover(ema20, ema50)

// Crossunder (bearish)
shortCondition = ta.crossunder(ema20, ema50)

// Either cross (either direction)
anyCross = ta.cross(ema20, ema50)
```

### Background Color on Cross:
```
bgcolor(longCondition ? color.new(color.green, 50) : shortCondition ? color.new(color.red, 50) : na)
```

---

## Lesson 18: RSI Overbought/Oversold Signal Indicator

### Complete Indicator Code:
```
@version=5
indicator("RSI Exhaustion Signals", overlay=false)

// Inputs
lookback = input.int(7, "Lookback (for patterns)")
rsiLength = input.int(7, "RSI Length")
rsiOB = input.float(80.0, "Overbought Level")
rsiOS = input.float(20.0, "Oversold Level")

// RSI
rsi = ta.rsi(close, rsiLength)

// Overbought/Oversold Conditions
toosold = rsi < rsiOS
toobought = rsi > rsiOB

// Candlestick Pattern Detection (Engulfing)
isBullishEngulfing = close > open and close[1] < open[1] and close > open[1] and open < close[1]
isBearishEngulging = close < open and close[1] > open[1] and close < open[1] and open > close[1]

// Combined Signals
// RSI oversold NOW or on previous bar AND bullish engulfing
buySignal = (toosold or toosold[1]) and isBullishEngulfing
sellSignal = (toobought or toobought[1]) and isBearishEngulfing

// Plot RSI
rsiColor = (toosold or toosold[1]) ? color.lime : (toobought or toobought[1]) ? color.red : color.gray
plot(rsi, "RSI", color=rsiColor, linewidth=2)

// Plot levels
hline(rsiOB, "Overbought", color.red)
hline(rsiOS, "Oversold", color.green)

// Background color on signal
bgcolor(buySignal ? color.new(color.green, 90) : sellSignal ? color.new(color.red, 90) : na, title="Signal")

// Alert
alertcondition(buySignal or sellSignal, title="RSI Signal", message="RSI Exhaustion on {{ticker}}")
```

---

## Lesson 19: Drawing Stops & Targets (Strategy Visualization)

### Full Strategy Visualization:
```
@version=5
indicator("Signal Stops & Targets", overlay=true)

// Inputs
lookback = input.int(7, "Swing Lookback")
atrMult = input.float(1.0, "ATR Multiplier")
riskReward = input.float(1.0, "Risk:Reward")

// Moving Averages
fastMA = ta.ema(close, 20)
slowMA = ta.ema(close, 50)

// Signals
longSignal = ta.crossover(fastMA, slowMA)
shortSignal = ta.crossunder(fastMA, slowMA)

// ATR for stops
atr = ta.atr(14)

// Calculate Stops using swing points + ATR
longStop = ta.lowest(low, lookback) - (atr * atrMult)
shortStop = ta.highest(high, lookback) + (atr * atrMult)

// Calculate Stop Distance
tradeStopDist = longSignal ? close - longStop : shortSignal ? shortStop - close : na

// Calculate Targets
target = longSignal ? close + (tradeStopDist * riskReward) : shortSignal ? close - (tradeStopDist * riskReward) : na

// Plot Stop & Target only on signal bars
plot(longSignal ? longStop : shortSignal ? shortStop : na, "Stop", color.red, style=plot.style_linebr)
plot(longSignal ? target : shortSignal ? target : na, "Target", color.green, style=plot.style_linebr)

// Plot entry arrows
plotshape(longSignal, "Buy", shape.triangleup, location.belowbar, color.green)
plotshape(shortSignal, "Sell", shape.triangledown, location.abovebar, color.red)

// Alert
alertcondition(longSignal or shortSignal, "Signal", "New signal on {{ticker}}")
```

### Key Concepts:
1. **Swing Points:** `ta.lowest(low, 7)` finds lowest low over 7 bars
2. **ATR Buffer:** Adds volatility buffer to stops (avoid noise)
3. **Line Break Style:** `plot.style_linebr` prevents connecting lines between separate trades
4. **Conditional Plotting:** Only plot stops/targets when condition is true (otherwise `na`)

---

## 🎓 Course Summary

### What Was Covered:

**Fundamentals:**
- ✅ Editor setup and settings
- ✅ Compiler and error handling
- ✅ Comments and documentation
- ✅ Data types (int, float, bool, color, string)
- ✅ Variables (declaration, reassignment, persistence)

**Core Features:**
- ✅ Price series (OHLC, historical access)
- ✅ Technical indicators (`ta` namespace)
- ✅ All user input types (bool, int, float, color, string, symbol, price, session, time, resolution)
- ✅ Input organization (groups, inline, tooltips)

**Drawing & Visualization:**
- ✅ Plot function (all parameters, all styles)
- ✅ Fill between plots/lines
- ✅ Colors (built-in, RGB, hex, transparency)
- ✅ Background colors
- ✅ Shapes (arrows, triangles, all styles)

**Advanced:**
- ✅ Lazy evaluation (v6 fix)
- ✅ Alert generation (immediate + manual)
- ✅ Complete strategy signal indicator
- ✅ Stop/target visualization on chart

### Next Steps:

1. **Practice:** Create 3-5 indicators from scratch
2. **Backtesting:** Learn `strategy()` for automated backtests
3. **Libraries:** Create reusable code modules
4. **Optimization:** Study pine script performance

### Resources:
- TradingView Pine Script documentation
- Pine Script reference manual (`Ctrl + Click` on functions)
- Pine Script version release notes
- Community scripts for learning

---

**Course Completion Time:** 6+ hours  
**Prerequisite:** None (beginner-friendly)  
**Outcome:** Can build custom indicators and signal detectors

---

## 🚀 Cryptonio Integration

This course enables Cryptonio to:
1. Modify existing Pine strategies
2. Create new confluence indicators
3. Build automated signal alerts
4. Develop custom visualizations
5. Backtest strategies before live deployment

**Recommended Next Steps for Cryptonio:**
1. Build 190-point confluence indicator in Pine
2. Create VWAP + EMA strategy visualizer
3. Develop RSI exhaustion signal with auto-alerts
4. Code volume profile confluence overlay

**Status:** Course materials archived and ready for implementation 🎓
