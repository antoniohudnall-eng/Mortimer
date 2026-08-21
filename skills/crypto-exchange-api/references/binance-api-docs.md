# Binance API Documentation

## Overview

This document provides key information about the Binance REST API endpoints used by the crypto exchange API skill.

## Base URLs

| Environment | URL |
|-------------|-----|
| Production | `https://api.binance.com` |
| Testnet | `https://testnet.binance.vision` |

## Authentication

All authenticated endpoints require:
1. API Key (header: `X-MBX-APIKEY`)
2. HMAC SHA256 signature

### Signature Generation

```javascript
const signature = crypto
  .createHmac('sha256', apiSecret)
  .update(queryString)
  .digest('hex');
```

### Required Parameters for Authenticated Requests

- `timestamp` - Current timestamp in milliseconds
- `signature` - HMAC SHA256 signature of the query string

## Endpoints

### Account Endpoints

#### GET /api/v3/account

Get current account information including balances.

**Weight:** 10

**Parameters:**
| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| timestamp | LONG | YES | Current timestamp |
| signature | STRING | YES | HMAC SHA256 signature |
| recvWindow | LONG | NO | Validity window (default: 5000ms) |

**Response:**
```json
{
  "makerCommission": 15,
  "takerCommission": 15,
  "buyerCommission": 0,
  "sellerCommission": 0,
  "canTrade": true,
  "canWithdraw": true,
  "canDeposit": true,
  "updateTime": 123456789,
  "accountType": "SPOT",
  "balances": [
    {
      "asset": "BTC",
      "free": "0.5",
      "locked": "0.1"
    }
  ],
  "permissions": ["SPOT"]
}
```

### Market Data Endpoints

#### GET /api/v3/exchangeInfo

Get exchange information including trading pairs and filters.

**Weight:** 10

**Parameters:** None (public endpoint)

**Response:**
```json
{
  "timezone": "UTC",
  "serverTime": 1565246363776,
  "rateLimits": [...],
  "exchangeFilters": [...],
  "symbols": [
    {
      "symbol": "BTCUSDT",
      "status": "TRADING",
      "baseAsset": "BTC",
      "baseAssetPrecision": 8,
      "quoteAsset": "USDT",
      "quotePrecision": 8,
      "orderTypes": ["LIMIT", "MARKET", ...],
      "filters": [...]
    }
  ]
}
```

#### GET /api/v3/ticker/24hr

Get 24-hour rolling window price change statistics.

**Weight:** 1 per symbol, 40 for all symbols

**Parameters:**
| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| symbol | STRING | NO | Trading pair (e.g., BTCUSDT) |

**Response (single symbol):**
```json
{
  "symbol": "BTCUSDT",
  "priceChange": "-94.99999800",
  "priceChangePercent": "-95.960",
  "weightedAvgPrice": "0.29628482",
  "prevClosePrice": "0.10002000",
  "lastPrice": "4.00000200",
  "lastQty": "200.00000000",
  "bidPrice": "4.00000000",
  "bidQty": "100.00000000",
  "askPrice": "4.00000200",
  "askQty": "100.00000000",
  "openPrice": "99.00000000",
  "highPrice": "100.00000000",
  "lowPrice": "0.10000000",
  "volume": "8913.30000000",
  "quoteVolume": "15.30000000",
  "openTime": 1499783499040,
  "closeTime": 1499869899040,
  "firstId": 28385,
  "lastId": 28460,
  "count": 76
}
```

#### GET /api/v3/ticker/price

Get latest price for a symbol or symbols.

**Weight:** 1 per symbol, 2 for all symbols

**Parameters:**
| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| symbol | STRING | NO | Trading pair |
| symbols | ARRAY | NO | Array of symbols (JSON array) |

#### GET /api/v3/ticker/bookTicker

Get best price/qty on the order book for a symbol or symbols.

**Weight:** 1 per symbol, 2 for all symbols

**Parameters:** Same as `/api/v3/ticker/price`

## Rate Limits

### Request Weight Limits

| Type | Limit | Interval |
|------|-------|----------|
| REQUEST_WEIGHT | 1200 | 1 minute |
| ORDERS | 10 | 1 second |
| ORDERS | 100 | 10 seconds |
| ORDERS | 200 | 1 minute |
| RAW_REQUESTS | 5000 | 5 minutes |

### Rate Limit Headers

| Header | Description |
|--------|-------------|
| `X-MBX-USED-WEIGHT-1M` | Current used weight for the 1-minute window |
| `X-MBX-ORDER-COUNT-1S` | Current order count for the 1-second window |
| `X-MBX-ORDER-COUNT-1D` | Current order count for the 1-day window |

### Rate Limit Response Codes

| Code | Status | Description |
|------|--------|-------------|
| 429 | Too Many Requests | Rate limit exceeded |
| 418 | IP Ban | IP has been auto-banned for continuing to exceed limits |

## Error Codes

### General Errors

| Code | Description |
|------|-------------|
| -1000 | UNKNOWN - An unknown error occurred |
| -1001 | DISCONNECTED - Internal error; unable to process request |
| -1002 | UNAUTHORIZED - Action not authorized |
| -1003 | TOO_MANY_REQUESTS - Too many requests |
| -1006 | UNEXPECTED_RESP - Unexpected response from message bus |
| -1007 | TIMEOUT - Timeout waiting for response |
| -1014 | UNKNOWN_ORDER_COMPOSITION - Unsupported order combination |
| -1015 | TOO_MANY_ORDERS - Too many new orders |
| -1016 | SERVICE_SHUTTING_DOWN - Service shutting down |
| -1020 | UNSUPPORTED_OPERATION - Operation not supported |
| -1021 | INVALID_TIMESTAMP - Timestamp outside recvWindow |
| -1022 | INVALID_SIGNATURE - Invalid signature |

### Request Errors

| Code | Description |
|------|-------------|
| -1100 | ILLEGAL_CHARS - Illegal characters found in parameter |
| -1101 | TOO_MANY_PARAMETERS - Too many parameters sent |
| -1102 | MANDATORY_PARAM_EMPTY_OR_MALFORMED - Mandatory parameter missing |
| -1103 | UNKNOWN_PARAM - Unknown parameter sent |
| -1104 | UNREAD_PARAMETERS - Not all parameters were read |
| -1105 | PARAM_EMPTY - Empty parameter |
| -1106 | PARAM_NOT_REQUIRED - Parameter sent when not required |
| -1111 | BAD_PRECISION - Precision exceeds maximum allowed |
| -1112 | NO_DEPTH - No depth available |
| -1114 | TIF_NOT_REQUIRED - TimeInForce not required |
| -1115 | INVALID_TIF - Invalid TimeInForce |
| -1116 | INVALID_ORDER_TYPE - Invalid order type |
| -1117 | INVALID_SIDE - Invalid side |
| -1118 | EMPTY_NEW_CL_ORD_ID - New client order ID was empty |
| -1119 | EMPTY_ORG_CL_ORD_ID - Original client order ID was empty |
| -1120 | BAD_INTERVAL - Invalid interval |
| -1121 | BAD_SYMBOL - Invalid symbol |

### Filter Errors

| Code | Description |
|------|-------------|
| -2010 | NEW_ORDER_REJECTED - New order rejected |
| -2011 | CANCEL_REJECTED - Cancel rejected |
| -2013 | NO_SUCH_ORDER - Order does not exist |
| -2014 | BAD_API_KEY_FMT - API key format invalid |
| -2015 | REJECTED_MBX_KEY - Invalid API key, IP, or permissions |

## Trading Filters

### PRICE_FILTER

Defines price rules for a symbol.

```json
{
  "filterType": "PRICE_FILTER",
  "minPrice": "0.00000100",
  "maxPrice": "100000.00000000",
  "tickSize": "0.00000100"
}
```

### LOT_SIZE

Defines quantity rules for a symbol.

```json
{
  "filterType": "LOT_SIZE",
  "minQty": "0.00100000",
  "maxQty": "100000.00000000",
  "stepSize": "0.00100000"
}
```

### MIN_NOTIONAL

Defines minimum notional value allowed for an order.

```json
{
  "filterType": "MIN_NOTIONAL",
  "minNotional": "0.00010000",
  "applyToMarket": true,
  "avgPriceMins": 5
}
```

### ICEBERG_PARTS

Defines maximum parts allowed for an iceberg order.

```json
{
  "filterType": "ICEBERG_PARTS",
  "limit": 10
}
```

### MARKET_LOT_SIZE

Defines quantity rules for market orders.

```json
{
  "filterType": "MARKET_LOT_SIZE",
  "minQty": "0.00000000",
  "maxQty": "63160.62144473",
  "stepSize": "0.00000000"
}
```

## Best Practices

1. **Use recvWindow wisely**: Default is 5000ms. Increase only if necessary.
2. **Handle rate limits**: Monitor `X-MBX-USED-WEIGHT-1M` header.
3. **Retry with backoff**: Use exponential backoff on 429 errors.
4. **Cache exchange info**: Exchange info rarely changes; cache for efficiency.
5. **Use testnet for development**: Test on testnet before production.

## References

- [Official Binance API Documentation](https://binance-docs.github.io/apidocs/spot/en/)
- [Binance API Postman Collection](https://github.com/binance/binance-api-postman)
