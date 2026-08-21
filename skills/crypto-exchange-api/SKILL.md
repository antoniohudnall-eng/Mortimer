# Crypto Exchange API Skill

## Description

Query crypto exchange APIs for balances, trades, and dust identification. This skill provides a Node.js-based interface to interact with cryptocurrency exchange APIs, with initial support for Binance REST API.

## Features

- **Balance Queries**: Retrieve account balances across all assets
- **Dust Identification**: Automatically identify dust positions (small balances below configurable thresholds)
- **Exchange Information**: Get trading pairs, filters, and exchange metadata
- **Rate Limiting**: Built-in rate limit handling with automatic retries
- **Error Handling**: Comprehensive error handling for authentication failures, rate limits, and API errors

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BINANCE_API_KEY` | Your Binance API key | Yes |
| `BINANCE_API_SECRET` | Your Binance API secret | Yes |
| `BINANCE_BASE_URL` | Binance API base URL (default: https://api.binance.com) | No |

### Setting Up

```bash
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_API_SECRET="your_api_secret_here"
```

## Methods

### `getBalances()`

Retrieve all account balances with non-zero amounts.

**Returns:** `Promise<Array<{asset: string, free: string, locked: string}>>`

**Example:**
```javascript
const balances = await binanceApi.getBalances();
console.log(balances);
// [{ asset: 'BTC', free: '0.5', locked: '0.1' }, ...]
```

### `identifyDust(thresholds?)`

Identify dust positions - small balances that are below trading minimums or configurable thresholds.

**Parameters:**
- `thresholds` (optional): Object mapping asset symbols to threshold values

**Returns:** `Promise<Array<{asset: string, free: string, locked: string, total: number, threshold: number, isDust: boolean}>>`

**Example:**
```javascript
const dust = await binanceApi.identifyDust({
  'BTC': 0.0001,
  'ETH': 0.001,
  'USDT': 1.0
});
```

### `getExchangeInfo()`

Retrieve exchange information including trading pairs, filters, and limits.

**Returns:** `Promise<Object>` - Full exchange info from Binance API

**Example:**
```javascript
const info = await binanceApi.getExchangeInfo();
console.log(info.symbols); // Array of trading pairs
```

## Scripts

### binance-api.js

Main API client for Binance. Provides the core methods for interacting with the exchange.

**Usage:**
```bash
node scripts/binance-api.js [command] [options]

Commands:
  balances              Get account balances
  dust [thresholds]     Identify dust positions
  exchange-info         Get exchange information
  ticker <symbol>       Get ticker for a symbol
```

### test-connection.sh

Test API connectivity and authentication.

**Usage:**
```bash
./scripts/test-connection.sh
```

### dust-analyzer.js

Analyze balances and identify dust positions with detailed reporting.

**Usage:**
```bash
node scripts/dust-analyzer.js [options]

Options:
  --thresholds <file>   Load thresholds from JSON file
  --min-value <usd>     Minimum USD value to consider (default: 1.0)
  --output <format>     Output format: json, table (default: table)
```

## Error Handling

The skill handles the following error types:

| Error Type | HTTP Status | Behavior |
|------------|-------------|----------|
| Authentication Error | 401 | Throws with clear message about invalid credentials |
| Rate Limit Exceeded | 429 | Retries with exponential backoff |
| IP Ban | 418 | Throws with ban duration info |
| Invalid Symbol | 400 | Throws with symbol validation error |
| Network Error | - | Retries up to 3 times |

## Rate Limiting

Built-in rate limiting features:
- Request weight tracking
- Automatic retry on 429 errors
- Exponential backoff (1s, 2s, 4s, 8s)
- IP ban protection

## References

- `references/binance-api-docs.md` - Key Binance API endpoints and parameters
- `references/dust-thresholds.md` - Configurable dust thresholds per asset

## Dependencies

- `axios` - HTTP client for API requests
- `crypto` - Node.js built-in for HMAC-SHA256 signatures

## Security Notes

- Never commit API keys to version control
- Use environment variables or secure secret management
- API keys should have appropriate permissions (read-only for balance queries)
- Consider using IP whitelisting on your Binance API keys
