# VIDEO 17: Pine Script Basics — Building Your First Indicator

**Source:** TradingView Education (transcript provided 2026-03-07 08:27 UTC)
**Status:** Pine Script Foundation Tutorial Complete
**Topic:** Introduction to Pine Script v5, creating custom indicators
**Difficulty:** Beginner
**Prerequisite:** None

---

## 🎯 LEARNING OBJECTIVES

By the end of this video, you will:
- ✅ Understand Pine Editor location and interface
- ✅ Know the 5 versions of Pine Script (v5 is current)
- ✅ Create a basic indicator from scratch
- ✅ Plot indicators on charts
- ✅ Customize colors and styles

---

## 📍 Step 1: Open Pine Editor

**Location:** Bottom of TradingView chart

**What is Pine Editor?**
- IDE (Integrated Development Environment) built into TradingView
- Where you write, save, and manage Pine Script code

---

## 📝 Step 2: Pine Script Fundamentals

### Version Declaration
```pinescript
//@version=5
```
**What it does:**
- Tells TradingView which Pine Script version to use
- **v5 is current** — stay updated with latest versions
- Always start your script with this line

**Where to learn more:**
- TradingView User Manual (linked in video)
- Documentation for all 5 versions

---

## 💬 Step 3: Comments

```pinescript
// This is a comment
// Anything starting with // is ignored by the compiler
// Use comments to document your code
```

**Syntax:** `//` makes everything after it on that line a comment
**Purpose:** Documentation, explanations, notes to self

---

## 🚀 Step 4: Create Your First Indicator

### The `indicator()` Function

```pinescript
indicator("Rocket Moving Average", overlay=true)
```

**Components:**
| Component | Value | Meaning |
|-----------|-------|---------|
| `indicator` | Function | Declares this is an indicator |
| `"Rocket Moving Average"` | String | **Name** of your indicator |
| `overlay=true` | Boolean | Plots **ON the price chart** |

**What is `overlay=true`?**
- `true` = Draws indicator **directly on the price chart**
- `false` = Draws indicator **below** the chart (separate panel)

---

## 📊 Step 5: Define Your Source

### Creating User-Defined Variables

```pinescript
sma = ta.sma(close, 14)
```

**Breaking it down:**
| Component | Explanation |
|-----------|-------------|
| `sma` | **Variable name** — you can name this anything (RMA, mySMA, rocketMA, etc.) |
| `ta.sma()` | Built-in **Simple Moving Average** function |
| `close` | **Source** — the price data (open, high, low, close, volume, etc.) |
| `14` | **Length/Period** — how many bars to average |

### What is `close`?
- `close` = closing price of each candle
- Other sources: `open`, `high`, `low`, `hl2`, `hlc3`, `ohlc4`, `volume`

---

## 📈 Step 6: Plot Your Indicator

### The `plot()` Function

```pinescript
plot(sma, color=color.red, style=plot.style_cross)
```

**Components:**
| Parameter | Value | Purpose |
|-----------|-------|---------|
| `sma` | Variable | **What** to plot (your calculated value) |
| `color` | `color.red` | **Color** of the line/plot |
| `style` | `plot.style_cross` | **Visual style** of the plot |

### Available Styles:
| Style | Visual |
|-------|--------|
| `plot.style_cross` | ❌ Cross marks |
| `plot.style_line` | — Solid line |
| `plot.style_linebr` | — Line with breaks |
| `plot.style_histogram` | ████ Bar chart |
| `plot.style_area` | ▓▓▓▓ Filled area |
| `plot.style_circles` | ○ Circle dots |
| `plot.style_stepline` | ━┓━ Step line |

### Available Colors:
- Built-in: `color.red`, `color.green`, `color.blue`, `color.black`, `color.white`, `color.gray`
- Custom: `color.new(color.red, 50)` — red with 50% transparency
- Hex: `#FF0000` — red in hex

---

## 🎨 Step 7: Update & Modify

### Auto-Populate Features
The Pine Editor has **helpful dropdowns** that:
- Auto-complete functions
- Show available parameters
- Suggest color/style options

### Live Updates
1. Change code in Pine Editor
2. Click **"Add to Chart"** or **"Update on Chart"**
3. Changes appear instantly on chart

**No refresh needed** — TradingView compiles and updates in real-time.

---

## 📝 COMPLETE FIRST INDICATOR

```pinescript
//@version=5
// Comment: This is my first indicator

indicator("Rocket Moving Average", overlay=true)

// Define source/calculation
sma = ta.sma(close, 14)

// Plot the indicator
plot(sma, color=color.red, style=plot.style_cross)
```

---

## 🔧 EXERCISES FOR PRACTICE

### Exercise 1: Change the Color
```pinescript
// Change from red to blue
plot(sma, color=color.blue, style=plot.style_cross)
```

### Exercise 2: Change the Style
```pinescript
// Change from cross to line
plot(sma, color=color.red, style=plot.style_line)
```

### Exercise 3: Change the Length
```pinescript
// Change from 14 to 50
sma = ta.sma(close, 50)
plot(sma, color=color.red, style=plot.style_line)
```

### Exercise 4: Change the Source
```pinescript
// Use average of high and low instead of close
sma = ta.sma(hl2, 14)
plot(sma, color=color.red, style=plot.style_line)
```

---

## 📚 Built-in Variables for Source Data

| Variable | Description |
|----------|-------------|
| `open` | Opening price |
| `high` | Highest price of the bar |
| `low` | Lowest price of the bar |
| `close` | Closing price |
| `volume` | Trading volume |
| `hl2` | (High + Low) / 2 |
| `hlc3` | (High + Low + Close) / 3 |
| `ohlc4` | (Open + High + Low + Close) / 4 |

---

## 🚀 NEXT LEVEL: Building Cryptonios Strategies

### Foundation Skills Acquired:
✅ Pine Editor basics  
✅ Version declaration  
✅ Indicator naming  
✅ Overlay vs panel  
✅ User-defined variables  
✅ Plotting  
✅ Colors and styles  

### For Cryptonio's 190-Point Confluence System:

**Next Videos/Skills Needed:**
1. **Inputs** — Allow user to customize parameters
2. **Conditions** — `if/else` logic for signals
3. **Functions** — Create reusable calculations
4. **Multiple plots** — Display multiple elements
5. **Alerts** — Trigger notifications
6. **Strategies** — Backtesting framework

**Pine Script v5 Resources:**
- TradingView Pine Script Reference Manual
- Pine Script Tutorial Series
- TradingView Community Scripts (see examples)

---

## 💡 KEY TAKEAWAYS

1. **Pine Script is TradingView's language** — Every indicator on TV is written in it
2. **Start with `//@version=5`** — Always declare your version
3. **`indicator()` function** — Names your script and sets overlay mode
4. **Comments with `//`** — Document your code
5. **Variables store calculations** — Name them clearly
6. **`plot()` displays results** — Customize with color and style
7. **Changes are instant** — Edit, update, see results in real-time

---

## 🎯 STATUS

**Course:** Pine Script Basics — ✅ COMPLETE  
**Next:** Pine Script Intermediate (inputs, conditions, multiple plots)  
**Purpose:** Build the 190-point confluence indicator  
**Difficulty:** Beginner → Intermediate

---

**Cryptonio Note:** *Foundation laid. I can now create indicators. Next: inputs, conditions, alerts, and the full confluence system. One step closer to executable trading tools.* 🎰💻

---

*"The best way to get started is to experiment. Copy, paste, and learn." — TradingView Education*
