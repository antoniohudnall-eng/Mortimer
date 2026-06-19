# VIDEO 4: TradingView Trend Filter + Calman Trend Levels Strategy

**Source:** YouTube (transcript provided by Captain 2026-03-07 07:22 UTC)  
**Agent:** the-great-cryptonio  
**Topic:** Trend-following indicator strategy  
**Timeframe:** 15-minute (as demonstrated)  
**Assets:** Gold, BTC/ETH crypto  

---

## 📺 Video Intro

> "I've tested over 50 TradingView indicators and honestly most of them were complete garbage. But in the process, I discovered five absolute gamechangers that almost nobody is talking about."

**Focus:** Trend-based confluence strategy (2 of 5 indicators shown)

---

## 🔧 Indicator #1: Trend Filter

### How to Add:
1. Click **Indicators** tab in TradingView
2. Search: **"trend filter"**
3. Add to chart

### Settings:
| Parameter | Default | Modified | Purpose |
|-----------|---------|----------|---------|
| Length | 20 | **28** | Smoother trend detection |
| Style | Default | Hide some | Cleaner visuals |

### Signal Interpretation:
- **RED** two-pole filter line = **SELL** territory (downtrend)
- **GREEN** two-pole filter line = **BUY** territory (uptrend)

### Rule:
- Price **below** red line = Only take SELL trades
- Price **above** green line = Only take BUY trades

---

## 🔧 Indicator #2: Calman Trend Levels

### How to Add:
1. Click **Indicators** tab
2. Search: **"calman trend levels"**
3. Select by creator
4. Add to chart

### Settings:
| Parameter | Default | Modified | Purpose |
|-----------|---------|----------|---------|
| Short Length | 50 | **40** | Faster signal |
| Long Length | 150 | **80** | Responsive trend |

### Signal Output:
- **BUY signal box:** Price moves up
- **SELL signal box:** Price moves down

---

## 📊 Complete Trading Rules

### LONG Setup (BUY):
**ALL conditions must be met:**

1. ✅ Trend Filter shows **GREEN** two-pole filter line
2. ✅ Price moves **ABOVE** the green two-pole filter line
3. ✅ Calman Trend Levels gives **BUY** signal
4. ✅ **Confirmation:** **Bullish candle** present

**Entry:** Market order  
**Stop Loss:** Below Calman's dot line  
**Target:** **1:1.5 risk-reward ratio**

---

### SHORT Setup (SELL):
**ALL conditions must be met:**

1. ✅ Trend Filter shows **RED** two-pole filter line
2. ✅ Price moves **BELOW** the red two-pole filter line
3. ✅ Calman Trend Levels gives **SELL** signal
4. ✅ **Confirmation:** **Bearish candle** present

**Entry:** Market order  
**Stop Loss:** Above Calman's dot line  
**Target:** **1:1.5 risk-reward ratio**

---

## 📈 Example Trades (From Video):

### Example 1: Gold Sell Trade (15M)
- Trend Filter: RED line
- Price: Below red line
- Calman: SELL signal
- Candle: Bearish confirmation
- **Result:** Hit 1:1.5 target ✅

### Example 2: BTC Buy Trade
- Trend Filter: GREEN line
- Price: Above green line
- Calman: BUY signal
- Candle: Bullish confirmation
- **Result:** Hit 1:1.5 target ✅

### Example 3: BTC Buy Trade
- Same conditions as Example 2
- **Result:** Hit target ✅

### Example 4: BTC Sell Trade
- Trend Filter: RED line
- Price: Below red line
- Calman: SELL signal
- Candle: Bearish
- **Result:** Hit target ✅

### Example 5: BTC Buy Trade
- Trend Filter: GREEN line
- Price: Above green line
- Calman: BUY signal
- Candle: Bullish
- **Result:** Hit target ✅

---

## 🧠 Key Principles:

1. **Trade WITH the trend** — "Don't fight against the trend. Trade with the trend."
2. **Wait for ALL conditions** — Don't enter until all 4 criteria met
3. **1:1.5 minimum R:R** — Target at least 1.5x the risk
4. **Use Calman's dots for stops** — Automated S/R levels
5. **Best in trending markets** — Choppy/sideways markets = stay out

---

## 🎯 Integration with Cryptonio's System:

### Pine Script Enhancement:
Add to `CRYPTONIO_CONFLUENCE_STRATEGY.pine`:

```pinescript
// Trend Filter Detection
isTrendFilterGreen = trendFilterLine > 0 and close > trendFilterLine
isTrendFilterRed = trendFilterLine < 0 and close < trendFilterLine

// Calman Signal Detection
isCalmanBuy = calmanSignal == 1
isCalmanSell = calmanSignal == -1

// Confluence Scoring
var int trendScore = 0
if isTrendFilterGreen and isCalmanBuy
    trendScore := 45  // Trend alignment + signal
else if isTrendFilterRed and isCalmanSell
    trendScore := -45  // Short signal

// Add to total confluence score += trendScore
```

### Confluence Points:
| Component | Points |
|-----------|--------|
| Trend Filter alignment | +15 |
| Price above/below filter | +10 |
| Calman signal | +20 |
| **Total possible** | **+45** |

**Combined with Video 3 system:** Max 135 points, threshold 60+ for trade.

---

## 📝 Disclaimers:

> "This is purely for informational purposes. Nothing in this video should be taken as financial advice."

**Test first:** Backtest before deploying live capital.

---

## 🎬 Next:

**Status:** 4/11 videos processed

- ✅ Video 1: Risk management + confluence
- ✅ Video 2: 8 candlestick patterns
- ✅ Video 3: S/R, Elliott Wave, FVG, Fibonacci
- ✅ Video 4: Trend Filter + Calman Trend Levels
- 📚 Videos 5-11: Research assignment

---

**The trend is your friend until it ends.** 📈📉
