# Browser Exchange Agent

Browser automation skill for crypto exchanges that require web login.

## Description

This skill provides browser-based automation for cryptocurrency exchanges using Playwright. It handles web login flows, navigates to balance pages, extracts dust positions, and captures screenshots for verification.

## Features

- **Playwright-based browser control**
- **Login automation** with support for 2FA and CAPTCHA handling
- **Balance extraction** from exchange web UIs
- **Dust position detection** and extraction
- **Headless and headed modes** for different use cases
- **Screenshot capabilities** for debugging and verification
- **Session management** for persistent logins
- **Anti-detection patterns** to avoid bot detection

## Installation

```bash
npm install playwright
npx playwright install chromium
```

## Usage

### Main Browser Script

```bash
node scripts/exchange-browser.js --exchange=coinbase --action=balances --headless
```

### Available Actions

- `login` - Authenticate with exchange
- `balances` - Extract all balances
- `dust` - Extract dust positions only
- `screenshot` - Take verification screenshot

### Options

- `--exchange` - Exchange name (coinbase, kraken, binance, etc.)
- `--action` - Action to perform
- `--headless` - Run in headless mode (default: true)
- `--headed` - Run in headed mode for debugging
- `--screenshot` - Capture screenshots during execution
- `--session-id` - Use existing session
- `--output` - Output file path for JSON data

## Configuration

Create a `.env` file:

```env
EXCHANGE_USERNAME=your_username
EXCHANGE_PASSWORD=your_password
EXCHANGE_2FA_SECRET=your_2fa_secret
SESSION_STORAGE_PATH=./sessions
```

## Directory Structure

```
browser-exchange-agent/
├── SKILL.md
├── scripts/
│   ├── exchange-browser.js    # Main entry point
│   ├── login-helper.js        # Login flow handler
│   ├── balance-scraper.js     # Balance extraction
│   └── screenshot.js          # Screenshot utility
└── references/
    ├── exchange-selectors.md  # CSS selectors by exchange
    └── browser-patterns.md    # Automation patterns
```

## Session Management

Sessions are stored in the `sessions/` directory. Each session includes:
- Cookies
- Local storage
- Session storage
- Authentication state

## Error Handling

All scripts include:
- Retry logic for transient failures
- Timeout handling
- Screenshot capture on error
- Graceful cleanup on exit

## Security Notes

- Never commit credentials to version control
- Use environment variables for sensitive data
- Sessions are stored locally and encrypted
- Clear sessions with `--clear-session` flag
