# TASK: R2-D2 Trading Bot - Assigned to Software Team
**Created:** 2026-03-16 16:56 UTC  
**Assigned to:** Software Team (Spindle/CTO, Pipeline, TapTap, BugCatcher)  
**Priority:** HIGH  
**Source:** R2-D2 design specs + Captain's requirements  
**Review by:** R2-D2 upon completion

---

## Overview
Build a standalone multi-exchange cryptocurrency trading bot with R2-D2's 190-point confluence scoring system. This bot will integrate with The Great Cryptonio portfolio manager and support automated trading across multiple exchanges.

---

## Technical Requirements

### Supported Exchanges (5 total)
1. **Kraken** - Primary institutional exchange
2. **Coinbase** - US retail/trading
3. **Gemini** - US regulated exchange
4. **Binance.US Account 1** - Primary Binance account
5. **Binance.US Account 2** - Secondary Binance account (separate credentials)

### Core Technologies
- **Language:** Python 3.10+
- **API Libraries:** 
  - ccxt (unified exchange API)
  - krakenex (Kraken specific)
  - coinbase-advanced-py (Coinbase)
  - python-binance (Binance.US)
- **Data Analysis:** pandas, numpy, TA-Lib
- **Database:** SQLite (local) or PostgreSQL (optional)
- **Config:** YAML for settings

---

## Architecture

```
r2-trading-bot/
├── r2_trading_bot.py          # Main entry point
├── config.yaml                # User configuration
├── exchanges/
│   ├── __init__.py
│   ├── base.py                # Base exchange wrapper
│   ├── kraken_api.py
│   ├── coinbase_api.py
│   ├── gemini_api.py
│   └── binance_us_api.py      # Handles both accounts
├── signal_engine/
│   ├── __init__.py
│   ├── confluence_calculator.py  # R2's 190-point system
│   ├── indicators.py          # Technical indicators
│   └── patterns.py            # Pattern recognition
├── risk_management/
│   ├── __init__.py
│   ├── position_sizing.py
│   ├── stop_loss.py           # ATR-based
│   └── take_profit.py         # ATR-based
├── data/
│   ├── market_data.py         # OHLCV fetching
│   └── storage.py             # SQLite storage
├── trading/
│   ├── __init__.py
│   ├── paper_trading.py       # Simulation mode
│   ├── live_trading.py        # Live execution
│   └── order_manager.py       # Order lifecycle
├── cryptonio/
│   └── integration.py         # Portfolio manager link
├── tests/
│   └── test_*.py
├── requirements.txt
├── setup.py
└── README.md
```

---

## Signal Engine (R2-D2 Specs)

### 190-Point Confluence Scoring
```python
class ConfluenceCalculator:
    MAX_SCORE = 190
    
    CATEGORIES = {
        'trend_alignment': 30,      # EMA alignment, trend strength
        'momentum': 25,             # RSI, MACD, Stochastics
        'volume': 20,               # Volume profile, OBV
        'support_resistance': 25,   # Key levels, pivots
        'pattern_recognition': 25,  # Chart patterns, candlestick patterns
        'divergence': 20,           # Price/indicator divergence
        'market_structure': 20,     # Higher highs/lows, breakouts
        'multi_timeframe': 25       # Alignment across 15m/1h/4h
    }
    
    THRESHOLDS = {
        'weak': 40,
        'moderate': 60,     # Minimum for trades
        'strong': 80,
        'excellent': 100,
        'perfect': 130+
    }
```

### Technical Indicators Required
- **Trend:** EMA(9, 21, 50, 200), SMA, ADX
- **Momentum:** RSI(14), MACD(12,26,9), Stochastic(14,3,3)
- **Volume:** OBV, Volume Profile, VWAP
- **Volatility:** ATR(14), Bollinger Bands
- **Support/Resistance:** Pivot points, Fibonacci retracement

### Timeframes
- Primary: 1-hour (main signal generation)
- Confirmation: 4-hour (trend direction)
- Entry: 15-minute (precise entry/exit)

---

## Risk Management

### Position Sizing
```python
MAX_DAILY_RISK = 50.00          # $50 max per day total
MAX_PAIR_RISK = 10.00           # $10 max per pair
MAX_OPEN_POSITIONS = 5          # Max concurrent trades
POSITION_SIZE_PCT = 0.02        # 2% of account per trade
```

### Stop Loss & Take Profit (ATR-Based)
```python
STOP_LOSS_MULTIPLIER = 1.5      # 1.5x ATR
TAKE_PROFIT_MULTIPLIER = 3.0    # 3:1 RR ratio (3x ATR)

# Example:
# Entry: $100
# ATR(14): $2
# Stop Loss: $100 - (1.5 * $2) = $97
# Take Profit: $100 + (3 * $2) = $106
```

### Trading Pairs (8 assets)
- BTC/USDT
- ETH/USDT
- SOL/USDT
- ADA/USDT
- DOT/USDT
- LINK/USDT
- MATIC/USDT
- AVAX/USDT

---

## Configuration (config.yaml)

```yaml
# R2-D2 Trading Bot Configuration

bot:
  name: "R2-D2 Trading Bot"
  version: "1.0.0"
  mode: "paper"  # paper | live
  log_level: "INFO"

exchanges:
  kraken:
    enabled: true
    api_key: "${KRAKEN_API_KEY}"
    api_secret: "${KRAKEN_API_SECRET}"
    sandbox: false
    
  coinbase:
    enabled: true
    api_key: "${COINBASE_API_KEY}"
    api_secret: "${COINBASE_API_SECRET}"
    passphrase: "${COINBASE_PASSPHRASE}"
    sandbox: false
    
  gemini:
    enabled: true
    api_key: "${GEMINI_API_KEY}"
    api_secret: "${GEMINI_API_SECRET}"
    sandbox: false
    
  binance_us:
    account_1:
      enabled: true
      api_key: "${BINANCE_US_1_API_KEY}"
      api_secret: "${BINANCE_US_1_API_SECRET}"
    account_2:
      enabled: false  # User can enable
      api_key: "${BINANCE_US_2_API_KEY}"
      api_secret: "${BINANCE_US_2_API_SECRET}"

risk:
  max_daily_risk_usd: 50.00
  max_pair_risk_usd: 10.00
  max_open_positions: 5
  position_size_pct: 0.02
  
  stop_loss:
    type: "atr"
    multiplier: 1.5
    
  take_profit:
    type: "atr"
    multiplier: 3.0
    
  trailing_stop:
    enabled: true
    activation_pct: 1.0  # Activate after 1% profit
    distance_pct: 0.5    # Trail at 0.5% below high

signals:
  confluence_threshold: 60  # Minimum score to trade
  
  timeframes:
    primary: "1h"
    confirmation: "4h"
    entry: "15m"
  
  indicators:
    ema_periods: [9, 21, 50, 200]
    rsi_period: 14
    macd_fast: 12
    macd_slow: 26
    macd_signal: 9
    atr_period: 14
    
  pairs:
    - BTC/USDT
    - ETH/USDT
    - SOL/USDT
    - ADA/USDT
    - DOT/USDT
    - LINK/USDT
    - MATIC/USDT
    - AVAX/USDT

cryptonio:
  enabled: true
  webhook_url: "https://myl0nr0s.cloud/api/v1/portfolio/update"
  api_key: "${CRYPTONIO_API_KEY}"

notifications:
  on_trade: true
  on_signal: false
  on_error: true
```

---

## Database Schema (SQLite)

```sql
-- trades table
CREATE TABLE trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_id TEXT UNIQUE NOT NULL,
    exchange TEXT NOT NULL,
    account TEXT,
    symbol TEXT NOT NULL,
    side TEXT NOT NULL,  -- buy | sell
    entry_price REAL NOT NULL,
    exit_price REAL,
    quantity REAL NOT NULL,
    stop_loss REAL,
    take_profit REAL,
    confluence_score INTEGER,
    status TEXT NOT NULL,  -- open | closed | cancelled
    pnl REAL,
    pnl_pct REAL,
    opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- signals table
CREATE TABLE signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    signal_id TEXT UNIQUE NOT NULL,
    symbol TEXT NOT NULL,
    exchange TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    confluence_score INTEGER NOT NULL,
    signal_type TEXT NOT NULL,  -- buy | sell | neutral
    indicators TEXT,  -- JSON of indicator values
    executed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- balance_history table
CREATE TABLE balance_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exchange TEXT NOT NULL,
    account TEXT,
    asset TEXT NOT NULL,
    free REAL NOT NULL,
    locked REAL NOT NULL,
    total REAL NOT NULL,
    usd_value REAL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## CLI Interface

```bash
# Run bot
python r2_trading_bot.py --config config.yaml

# Paper trading mode
python r2_trading_bot.py --mode paper

# Live trading (requires confirmation)
python r2_trading_bot.py --mode live --confirm

# Backtest strategy
python r2_trading_bot.py --backtest --start 2024-01-01 --end 2024-12-31

# Generate report
python r2_trading_bot.py --report --period 30d

# Update confluence scores (dry run)
python r2_trading_bot.py --scan --dry-run
```

---

## Testing Requirements

1. **Unit Tests**
   - Confluence calculator accuracy
   - Risk management calculations
   - Exchange API wrappers
   - Order lifecycle

2. **Integration Tests**
   - Exchange connectivity (paper/sandbox)
   - Signal generation pipeline
   - Order execution flow
   - Cryptonio webhook

3. **Paper Trading**
   - Run for 7 days minimum
   - Log all signals and would-be trades
   - Validate confluence scoring

---

## Security Requirements

- ✅ API keys stored in environment variables only
- ✅ No hardcoded credentials
- ✅ Encrypted config file option
- ✅ IP whitelist for exchange APIs
- ✅ 2FA required for live trading mode
- ✅ Withdrawal permissions disabled on API keys

---

## Deliverables Checklist

- [ ] `r2_trading_bot.py` - Main entry point
- [ ] `config.yaml` - Configuration template
- [ ] `exchanges/` - Exchange API modules (5 exchanges)
- [ ] `signal_engine/` - Confluence calculator + indicators
- [ ] `risk_management/` - Position sizing, stops, targets
- [ ] `trading/` - Paper & live trading engines
- [ ] `cryptonio/` - Portfolio manager integration
- [ ] `requirements.txt` - Dependencies
- [ ] `setup.py` - Installation script
- [ ] `README.md` - Documentation
- [ ] Unit tests (80%+ coverage)
- [ ] Integration tests (paper trading)
- [ ] Docker container (optional)

---

## Acceptance Criteria

1. **Functional**
   - [ ] Connects to all 5 exchanges
   - [ ] Generates 190-point confluence scores
   - [ ] Executes trades when score >= 60
   - [ ] ATR-based stops and targets working
   - [ ] Paper trading mode functional
   - [ ] Live trading mode functional
   - [ ] Position sizing respects limits ($10/pair, $50/day)

2. **Performance**
   - [ ] Signal generation < 5 seconds
   - [ ] Order execution < 3 seconds
   - [ ] No missed signals during market hours

3. **Integration**
   - [ ] Webhooks to Cryptonio successful
   - [ ] Balance tracking accurate
   - [ ] Trade history complete

4. **Security**
   - [ ] No credentials in logs
   - [ ] API keys from environment only
   - [ ] Rate limiting respected

---

## Notes for Software Team

- Start with **Kraken + Paper Trading** as MVP
- Use **ccxt** library for unified exchange interface where possible
- R2-D2 has Videos 1-21 on confluence scoring—reference those
- Test on 1h timeframe first, then add 15m/4h
- Coordinate with Cryptonio team for webhook format

**Questions?** Ask R2-D2 or the Captain.

---

**Status:** 🟡 Awaiting Software Team assignment  
**Estimated Effort:** 2-3 weeks (2-3 developers)  
**Review:** R2-D2 will review upon completion