---
name: cryptonio-dashboard
description: Real-time cryptocurrency portfolio dashboard with live data visualization. Provides web-based UI showing portfolio distribution, exchange holdings, asset values, and trade history across multiple exchanges. Auto-refreshes every 30 seconds with live market data.
metadata:
  clawdbot:
    emoji: 📊
    homepage: https://github.com/hcindus/aocros
    requires:
      bins:
        - python3
        - pip
      packages:
        - flask
        - flask-cors
      ports:
        - 5000
      files:
        - credential vault
---

# Cryptonio Dashboard Skill

Real-time cryptocurrency portfolio visualization dashboard.

## Overview

This skill provides a live web dashboard displaying:
- Portfolio distribution (pie chart with crypto brand colors)
- Portfolio value over time (line chart)
- Exchange holdings (bar charts per exchange)
- Asset holdings grid (all 29+ assets)
- Recent trades table
- Auto-refresh every 30 seconds

## Prerequisites

- Python 3.11+
- Exchange API credentials configured in vault
- Flask and dependencies installed

## Installation

### 1. Detect Skill Directory

```bash
SKILL_DIR=$(ls -d \
  ~/openclaw/skills/cryptonio-dashboard \
  ~/.openclaw/skills/cryptonio-dashboard \
  /root/.openclaw/workspace/skills/cryptonio-dashboard \
  2>/dev/null | head -1)

cd "$SKILL_DIR"
```

### 2. Install Dependencies

```bash
pip install flask flask-cors --break-system-packages 2>/dev/null || pip install flask flask-cors
```

### 3. Configure Credentials

Create vault files for each exchange:

```bash
mkdir -p vault/

# Binance.US Primary
echo 'BINANCE_US_API_KEY="your_key"'
echo 'BINANCE_US_SECRET_KEY="your_secret"' > vault/binance_us.env

# Binance.US Secondary  
echo 'BINANCE_US_SECOND_API_KEY="your_key"'
echo 'BINANCE_US_SECOND_SECRET="your_secret"' > vault/binance_us_second.env

# Kraken
echo 'KRAKEN_API_KEY="your_key"'
echo 'KRAKEN_API_SECRET="your_secret"' > vault/kraken.env

# Gemini (optional)
echo 'GEMINI_API_KEY="your_key"'
echo 'GEMINI_API_SECRET="your_secret"' > vault/gemini.env

# Coinbase (optional)
echo 'COINBASE_API_KEY="your_key"'
echo 'COINBASE_API_SECRET="your_secret"'
echo 'COINBASE_PASSPHRASE="your_passphrase"' > vault/coinbase.env
```

## Usage

### Start Dashboard

```bash
cd "$SKILL_DIR"
source ./start_dashboard.sh
```

Or with SystemD:
```bash
systemctl start cryptonio-dashboard
```

### Access Dashboard

- **Local:** http://localhost:5000
- **Network:** http://YOUR_IP:5000
- **API:** http://localhost:5000/api/data

### Auto-Start Configuration

Enable SystemD service:
```bash
sudo systemctl enable cryptonio-dashboard
sudo systemctl start cryptonio-dashboard
```

Add cron job for auto-restart:
```bash
openclaw cron add --name "dashboard-autostart" \
  --schedule "every 5m" \
  --command "$SKILL_DIR/check_and_restart.sh"
```

## Dashboard Components

### 1. Portfolio Overview
- Total portfolio value in USD
- BTC equivalent
- Last update timestamp
- Connection status indicator

### 2. Charts
- **Pie Chart:** Asset distribution (crypto brand colors)
- **Line Chart:** Portfolio value over time (last 7 days)

### 3. Exchange Holdings
- Cards for each connected exchange
- Total USD value per exchange
- Online/offline status

### 4. Asset Grid
- All held assets with amounts
- Current USD value
- Exchange breakdown

### 5. Recent Trades
- Trade history table
- Buy/sell indicators
- Status (filled/pending)

## API Endpoints

### GET /api/data
Returns current dashboard data:

```json
{
  "total_value": 1247.89,
  "total_btc": 0.018342,
  "timestamp": "2026-03-07T11:40:32",
  "exchanges": {
    "kraken": {
      "total_usd": 450.00,
      "connected": true,
      "balances": {...}
    }
  },
  "portfolio": [...],
  "prices": {...},
  "trades": [...],
  "history": [...]
}
```

### GET /api/refresh
Force refresh of exchange data.

## Configuration

### Environment Variables

Edit `dashboard_server.py` to customize:

```python
# Update interval (seconds)
UPDATE_INTERVAL = 30

# Number of history data points to keep
MAX_HISTORY_POINTS = 1000

# Default port
PORT = 5000
```

### Custom Colors

Edit crypto brand colors in `dashboard_server.py`:

```python
CRYPTO_COLORS = {
    'BTC': '#F7931A',  # Bitcoin orange
    'ETH': '#627EEA',  # Ethereum blue
    # ... add your colors
}
```

## Monitoring

Check dashboard status:
```bash
curl http://localhost:5000/api/data | jq '.total_value'
```

View logs:
```bash
tail -f logs/cryptonio_multi.log
```

Check screen session:
```bash
screen -ls | grep cryptonio
```

## Troubleshooting

### "ASSET_PRICE_MAP" Error
Update `cryptonio_multi_exchange.py` Config class to include ASSET_PRICE_MAP.

### Connection Refused
- Verify dashboard is running: `ps aux | grep dashboard`
- Check port 5000 is available: `lsof -i :5000`

### No Exchange Data
- Verify credentials are loaded: `echo $KRAKEN_API_KEY`
- Check exchange APIs are accessible
- Review logs in `logs/` directory

## Security Notes

- Credentials stored in `vault/` directory (chmod 600)
- Private keys never transmitted
- Dashboard only accessible locally by default
- Use nginx/reverse proxy for external access

## Files

| File | Purpose |
|------|---------|
| `dashboard_server.py` | Flask backend server |
| `templates/dashboard.html` | Web UI template |
| `start_dashboard.sh` | Launcher script |
| `start_dashboard_systemd.sh` | SystemD wrapper |
| `cron_dashboard.sh` | Cron check script |
| `vault/*.env` | Exchange credentials |

## Version

- **Version:** 1.0.0
- **Requires:** Python 3.11+, Flask
- **Compatible:** Linux, macOS

## License

Performance Supply Depot LLC - Private Use
