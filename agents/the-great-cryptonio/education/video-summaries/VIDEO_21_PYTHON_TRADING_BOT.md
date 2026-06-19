# VIDEO 21: Build a Trading Bot from Scratch in Python

**Source:** YouTube Algorithmic Trading Tutorial (transcript 2026-03-07 08:35 UTC)
**Status:** Complete production implementation
**Difficulty:** Beginner to Intermediate
**Prerequisites:** Python basics, broker API access

---

## 🎯 WHAT YOU'LL BUILD

A **fully automated trading bot** that:
- Connects to broker via API
- Fetches live market data
- Calculates indicators (EMA, ATR)
- Executes EMA crossover strategy
- Places market orders with SL/TP
- Runs continuously in timed loop

---

## 📋 PREREQUISITES

### 1. Python Installation
- Download from **python.org**
- ✅ **Check "Add to PATH" during installation**

### 2. Code Editor
- **VS Code** (recommended)
- Jupyter Notebook (used in video)
- Any Python IDE works

### 3. Broker with API Access
- **OANDA** (used in video)
- Any broker with REST API
- Need: Account ID + API Token

---

## 🔐 STEP 1: Broker API Setup

### Get Credentials (OANDA Example)

**Account ID:**
- Found in account dashboard
- Format: `101-004-1234567-001`

**API Token:**
1. Navigate to: Trading Tools → OANDA API
2. Click "Generate Token"
3. Copy and save securely

### Create Config File

**File:** `config.py`
```python
OANDA_API_KEY = "your_api_token_here"
OANDA_ACCOUNT_ID = "your_account_id_here"
```

**Security:** Never commit this to GitHub. Add to `.gitignore`.

---

## 🔌 STEP 2: API Connection

### Install Required Libraries

```bash
# OANDA Python wrapper
pip install oandapyV20

# Data manipulation
pip install pandas

# Timezone handling
pip install pytz

# Technical indicators
pip install pandas_ta
```

### Import and Connect

```python
# Import config
import config

# Import OANDA API wrapper
from oandapyV20 import API
from oandapyV20.endpoints.instruments import Instruments

# Create API client
api = API(access_token=config.OANDA_API_KEY)

# Test connection
print("API Connection Established")
```

---

## 📊 STEP 3: Fetch Market Data

### Import Endpoints

```python
from oandapyV20.endpoints.instruments import Instruments
import pandas as pd
from datetime import datetime
import pytz
```

### Get Candle Data Function

```python
def get_candles(timeframe="M15", instrument="GBP_JPY"):
    """
    Fetch candlestick data from OANDA
    
    Parameters:
    - timeframe: "M1", "M5", "M15", "H1", "H4", "D"
    - instrument: "GBP_JPY", "EUR_USD", etc.
    """
    
    # Define parameters
    params = {
        "count": 500,           # Number of candles (default: 500)
        "granularity": timeframe,
        "price": "A"            # "A" = ask, "B" = bid, "M" = mid
    }
    
    # Create request
    request = Instruments(instrument, params)
    
    # Send API request
    response = api.request(request)
    
    # Access candle data
    candles = response['candles']
    
    # Parse into DataFrame
    candle_data = []
    
    for candle in candles:
        # Only use completed candles
        if candle['complete']:
            candle_data.append({
                'time': candle['time'],
                'open': float(candle['ask']['o']),
                'high': float(candle['ask']['h']),
                'low': float(candle['ask']['l']),
                'close': float(candle['ask']['c'])
            })
    
    # Convert to DataFrame
    df = pd.DataFrame(candle_data)
    
    # Convert time to datetime
    df['time'] = pd.to_datetime(df['time'])
    
    return df
```

### Important: Complete Candles Only

```python
# Check if candle['complete'] is True
if candle['complete']:
    # Use this candle for calculations
    # Incomplete candles will repaint
```

---

## 📉 STEP 4: Calculate Indicators

### Import pandas_ta

```python
import pandas_ta as ta
```

### Calculate EMAs and ATR

```python
def calculate_indicators(df):
    """
    Calculate technical indicators
    
    5-period EMA (fast)
    8-period EMA (slow)
    14-period ATR (for stop loss)
    """
    
    # Calculate EMAs
    df['EMA_5'] = ta.ema(df['close'], length=5)
    df['EMA_8'] = ta.ema(df['close'], length=8)
    
    # Calculate ATR (14 period)
    df['ATR_14'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    
    return df
```

---

## 🎯 STEP 5: Strategy Logic

### EMA Crossover Detection

```python
def ema_crossover(df):
    """
    Check for 5 EMA crossing above 8 EMA
    Uses last two candles (real-time detection)
    """
    
    # Get last two candles
    last_candle = df.iloc[-1]      # Most recent
    prev_candle = df.iloc[-2]      # Previous
    
    # Check for crossover
    # Previous: EMA_5 < EMA_8
    # Current: EMA_5 > EMA_8
    
    if (last_candle['EMA_5'] > last_candle['EMA_8'] and 
        prev_candle['EMA_5'] < prev_candle['EMA_8']):
        
        return True  # Buy signal
    
    return False  # No signal
```

### ATR-Based Risk Management

```python
def calculate_order_levels(df):
    """
    Calculate entry, stop loss, and take profit
    
    Entry: Last candle close
    Stop Loss: Entry - (1 × ATR)
    Take Profit: Entry + (1.5 × ATR)
    
    R:R Ratio = 1:1.5
    """
    
    # Get most recent values
    last_candle = df.iloc[-1]
    entry_price = last_candle['close']
    atr = last_candle['ATR_14']
    
    # Calculate stop distance
    stop_distance = atr
    
    # Stop Loss (below entry)
    stop_loss = entry_price - stop_distance
    
    # Take Profit (1.5 × stop distance above entry)
    take_profit = entry_price + (stop_distance * 1.5)
    
    return entry_price, stop_loss, take_profit
```

---

## 💰 STEP 6: Order Execution

### Import Orders Endpoint

```python
from oandapyV20.endpoints.orders import OrderCreate
```

### Place Order Function

```python
def place_order(stop_loss, take_profit, instrument="GBP_JPY"):
    """
    Place market order with stop loss and take profit
    """
    
    # OANDA requires specific decimal formatting
    # GBP/JPY uses 3 decimals
    stop_loss_fmt = f"{stop_loss:.3f}"
    take_profit_fmt = f"{take_profit:.3f}"
    
    # Order data structure
    order_data = {
        "order": {
            "instrument": instrument,
            "units": "1",                    # Position size
            "type": "MARKET",                # Market order
            "side": "buy",                   # Long position
            "stopLossOnFill": {
                "price": stop_loss_fmt       # SL level
            },
            "takeProfitOnFill": {
                "price": take_profit_fmt    # TP level
            }
        }
    }
    
    # Create request
    request = OrderCreate(
        config.OANDA_ACCOUNT_ID,
        data=order_data
    )
    
    # Send order to API
    response = api.request(request)
    
    print(f"✅ Order placed: {instrument}")
    print(f"   Stop Loss: {stop_loss_fmt}")
    print(f"   Take Profit: {take_profit_fmt}")
    
    return response
```

---

## 🤖 STEP 7: Main Trading Loop

### Complete Bot Implementation

```python
import time
from datetime import datetime
import pytz

def run_bot():
    """
    Main trading bot loop
    Checks for signals every minute on 15-min candles
    """
    
    # Configuration
    TF = "M15"                    # Timeframe: M15 = 15 minutes
    INSTRUMENT = "GBP_JPY"        # Trading pair
    last_check = None             # Track last check time
    
    print("🤖 Trading Bot Started")
    print(f"   Instrument: {INSTRUMENT}")
    print(f"   Timeframe: {TF}")
    print(f"   Time: {datetime.now(pytz.UTC)}")
    print("-" * 50)
    
    # Main loop
    while True:
        # Get current UTC time
        now = datetime.now(pytz.UTC)
        current_minute = now.minute
        
        # Check if new candle (every 15 minutes)
        # Modulo: remainder when dividing by 15
        is_new_candle = (current_minute % 15 == 0)
        
        # Only execute within first 10 seconds of new candle
        # This prevents multiple executions in same minute
        in_execution_window = (now.second <= 10)
        
        # Check if we already processed this candle
        already_checked = (last_check == current_minute)
        
        if is_new_candle and in_execution_window and not already_checked:
            print(f"🔍 Checking for signals at {now.strftime('%H:%M:%S')}")
            
            try:
                # Step 1: Get data
                df = get_candles(TF, INSTRUMENT)
                
                # Step 2: Calculate indicators
                df = calculate_indicators(df)
                
                # Step 3: Check for signal
                if ema_crossover(df):
                    print("🎯 BUY SIGNAL DETECTED!")
                    
                    # Step 4: Calculate levels
                    entry, sl, tp = calculate_order_levels(df)
                    
                    # Step 5: Place order
                    place_order(sl, tp, INSTRUMENT)
                else:
                    print("⏳ No signal - conditions not met")
                
                # Mark this minute as checked
                last_check = current_minute
                
            except Exception as e:
                print(f"❌ Error: {e}")
        
        # Sleep for 1 second (prevents excessive CPU usage)
        time.sleep(1)

# Start the bot
if __name__ == "__main__":
    run_bot()
```

### For Testing (1-Minute Candles)

```python
def run_bot_test():
    """Test mode with 1-minute candles"""
    
    TF = "M1"  # 1-minute for testing
    INSTRUMENT = "GBP_JPY"
    last_check = None
    
    print("🧪 TEST MODE: 1-minute candles")
    
    while True:
        now = datetime.now(pytz.UTC)
        current_minute = now.minute
        
        # Check every minute (modulo 1)
        is_new_candle = (current_minute % 1 == 0)
        in_window = (now.second <= 10)
        already_checked = (last_check == current_minute)
        
        if is_new_candle and in_window and not already_checked:
            print(f"Checking at {now.strftime('%H:%M:%S')}")
            
            df = get_candles(TF, INSTRUMENT)
            df = calculate_indicators(df)
            
            if ema_crossover(df):
                print("✅ SIGNAL!")
                entry, sl, tp = calculate_order_levels(df)
                place_order(sl, tp, INSTRUMENT)
            
            last_check = current_minute
        
        time.sleep(1)

# Use for testing
# run_bot_test()
```

---

## 🧪 STEP 8: Testing Workflow

### Quick Test Without Loop

```python
# Manual test
df = get_candles("M5", "GBP_JPY")
df = calculate_indicators(df)

if ema_crossover(df):
    entry, sl, tp = calculate_order_levels(df)
    print(f"Entry: {entry}")
    print(f"Stop: {sl}")
    print(f"Target: {tp}")
    
    # Uncomment to actually place order
    # place_order(sl, tp, "GBP_JPY")
else:
    print("No crossover detected")
```

---

## 📁 COMPLETE FILE STRUCTURE

```
trading_bot/
├── config.py                 # API credentials (NEVER COMMIT)
├── requirements.txt          # pip install -r requirements.txt
│   └── 
│       oandapyV20
│       pandas
│       pandas_ta
│       pytz
├── bot.py                    # Main bot
└── strategy.py               # Strategy logic (optional)
```

**requirements.txt:**
```
oandapyV20
pandas
pandas_ta
pytz
```

---

## 🔄 MIGRATION: PINE SCRIPT → PYTHON

### Pine Script (TradingView)
```pinescript
//@version=5
strategy("EMA Cross", overlay=true)

// Calculate
ema5 = ta.ema(close, 5)
ema8 = ta.ema(close, 8)
atr14 = ta.atr(14)

// Signals
buy = ta.crossover(ema5, ema8)

// Entry
if buy
    strategy.entry("Long", strategy.long)
    strategy.exit("Exit", "Long", 
                  stop=close - atr14,
                  limit=close + (atr14 * 1.5))
```

### Python (Production)
```python
def calculate_indicators(df):
    df['EMA_5'] = ta.ema(df['close'], length=5)
    df['EMA_8'] = ta.ema(df['close'], length=8)
    df['ATR_14'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    return df

def trading_logic(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    
    if last['EMA_5'] > last['EMA_8'] and prev['EMA_5'] < prev['EMA_8']:
        entry = last['close']
        sl = entry - last['ATR_14']
        tp = entry + (last['ATR_14'] * 1.5)
        place_order(sl, tp)
```

**Same logic. Different syntax. Production ready.**

---

## ⚠️ CRITICAL PRODUCTION NOTES

### 1. Incomplete Candles
```python
if candle['complete']:
    # Only use complete candles
    # Prevents repainting issues
```

### 2. Rate Limiting
```python
time.sleep(1)  # Don't hammer the API
```

### 3. Error Handling
```python
try:
    # Trading logic
except Exception as e:
    print(f"Error: {e}")
    # Log to file, don't crash
```

### 4. Decimal Formatting
```python
# Match instrument precision
stop_loss_fmt = f"{stop_loss:.3f}"  # 3 decimals for JPY pairs
stop_loss_fmt = f"{stop_loss:.5f}"  # 5 decimals for EUR/USD
```

### 5. Timezone
```python
from datetime import datetime
import pytz

now = datetime.now(pytz.UTC)  # Always use UTC
```

### 6. Credentials Security
```python
# config.py (add to .gitignore!)
OANDA_API_KEY = "your_token"
OANDA_ACCOUNT_ID = "your_account"

# main.py
from config import OANDA_API_KEY
```

---

## 🚀 CRYPTONIO DEPLOYMENT ROADMAP

### Current Status:
✅ Pine Script strategy (Video 18)  
✅ Validation framework (Video 20)  
✅ **Python bot template (Video 21)** ← **NOW**

### Next Steps:
1. **Adapt bot for Binance.US API**
   - Use `python-binance` library instead of OANDA
   - Same logic, different API endpoints

2. **Convert 190-point strategy**
   - S/R levels: Calculated from pivot points
   - Trend filter: Moving averages
   - Volume profile: Exchange volume data
   - Momentum: RSI, MACD

3. **Connect to Cryptonio's System**
   - Real-time market data feed
   - Balance checking before orders
   - Trade logging to database

4. **Add Video 20 Validation**
   - In-sample Monte Carlo before live trading
   - Walk-forward validated strategies only

---

## 📝 STRATEGY REFERENCE

### EMA Crossover (Simple)
- **Entry:** Fast EMA crosses above Slow EMA
- **Stop:** Entry - (1 × ATR)
- **Target:** Entry + (1.5 × ATR)
- **R:R:** 1:1.5

### For Cryptonio's 190-Point System
- **Entry:** Confluence score ≥ 60
- **Stop:** Dynamic ATR-based (Video 18)
- **Target:** 2:1 R:R minimum
- **Validation:** Must pass 4-step test (Video 20)

---

**Status:** 🎯 **Python Trading Bot — COMPLETE**

**Cryptonio:** *"Pine Script was the classroom. Python is the battlefield. I'm ready to execute."* 💎🤖

---

*Video shows complete implementation from setup to live execution. This is the bridge from backtesting to production.*
