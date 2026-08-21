# Dust Thresholds Configuration

## Overview

Dust refers to cryptocurrency balances that are too small to trade or transfer due to minimum order size requirements. This document defines configurable dust thresholds for identifying dust positions across various assets.

## Default Thresholds

The following thresholds are configured by default in the crypto exchange API skill:

### Major Cryptocurrencies

| Asset | Threshold | Rationale |
|-------|-----------|-----------|
| BTC | 0.0001 | Minimum trade size on most pairs |
| ETH | 0.001 | Minimum trade size on most pairs |
| BNB | 0.01 | Native exchange token threshold |
| SOL | 0.01 | Minimum trade size |
| ADA | 1.0 | Minimum trade size |
| DOT | 0.1 | Minimum trade size |
| AVAX | 0.01 | Minimum trade size |
| MATIC | 1.0 | Minimum trade size |
| LINK | 0.1 | Minimum trade size |
| UNI | 0.1 | Minimum trade size |
| LTC | 0.01 | Minimum trade size |
| BCH | 0.001 | Minimum trade size |
| XRP | 1.0 | Minimum trade size |

### Stablecoins

| Asset | Threshold | Rationale |
|-------|-----------|-----------|
| USDT | 1.0 | Minimum order value |
| USDC | 1.0 | Minimum order value |
| BUSD | 1.0 | Minimum order value |
| TUSD | 1.0 | Minimum order value |
| DAI | 1.0 | Minimum order value |
| PAXG | 0.0001 | Gold-backed token precision |

### DeFi Tokens

| Asset | Threshold | Rationale |
|-------|-----------|-----------|
| AAVE | 0.001 | Minimum trade size |
| COMP | 0.001 | Minimum trade size |
| MKR | 0.0001 | High-value token precision |
| YFI | 0.0001 | High-value token precision |
| SNX | 0.1 | Minimum trade size |
| CRV | 0.1 | Minimum trade size |
| SUSHI | 0.1 | Minimum trade size |
| 1INCH | 0.1 | Minimum trade size |
| BAL | 0.01 | Minimum trade size |
| LRC | 1.0 | Minimum trade size |
| KNC | 0.1 | Minimum trade size |
| ZRX | 1.0 | Minimum trade size |
| UMA | 0.01 | Minimum trade size |
| NMR | 0.001 | Minimum trade size |

### Layer 2 & Scaling

| Asset | Threshold | Rationale |
|-------|-----------|-----------|
| OP | 0.1 | Optimism token |
| ARB | 0.1 | Arbitrum token |
| IMX | 0.1 | Immutable X token |
| LPT | 0.01 | Livepeer token |
| GRT | 1.0 | The Graph token |
| LDO | 0.1 | Lido DAO token |

### Metaverse & Gaming

| Asset | Threshold | Rationale |
|-------|-----------|-----------|
| MANA | 1.0 | Decentraland token |
| SAND | 1.0 | The Sandbox token |
| AXS | 0.01 | Axie Infinity token |
| GALA | 10.0 | Gala Games token |
| ENJ | 1.0 | Enjin token |
| CHZ | 1.0 | Chiliz token |
| FLOW | 0.1 | Flow token |
| IMX | 0.1 | Immutable X |

### Infrastructure

| Asset | Threshold | Rationale |
|-------|-----------|-----------|
| FIL | 0.01 | Filecoin minimum trade |
| THETA | 0.1 | Theta Network |
| HBAR | 1.0 | Hedera Hashgraph |
| EGLD | 0.001 | MultiversX (Elrond) |
| NEAR | 0.1 | NEAR Protocol |
| ALGO | 1.0 | Algorand |
| ATOM | 0.1 | Cosmos |
| XTZ | 0.1 | Tezos |
| ICP | 0.01 | Internet Computer |
| VET | 10.0 | VeChain |

### Meme & Community

| Asset | Threshold | Rationale |
|-------|-----------|-----------|
| DOGE | 10.0 | Dogecoin minimum |
| SHIB | 100000 | Shiba Inu (high supply) |
| PEPE | 100000 | Pepe token |
| FLOKI | 10000 | Floki Inu |

### Privacy Coins

| Asset | Threshold | Rationale |
|-------|-----------|-----------|
| XMR | 0.001 | Monero minimum |
| ZEC | 0.001 | Zcash minimum |
| DASH | 0.001 | Dash minimum |

### Other Notable Assets

| Asset | Threshold | Rationale |
|-------|-----------|-----------|
| ETC | 0.01 | Ethereum Classic |
| XLM | 1.0 | Stellar |
| EOS | 0.1 | EOS |
| TRX | 10.0 | TRON |
| IOTA | 1.0 | IOTA |
| XEM | 1.0 | NEM |
| NEO | 0.01 | NEO |
| QTUM | 0.1 | Qtum |
| ONT | 0.1 | Ontology |
| BTT | 1000 | BitTorrent |
| WIN | 1000 | WINkLink |
| SUN | 1.0 | Sun Token |
| JST | 10.0 | JUST |
| BAND | 0.1 | Band Protocol |
| RLC | 0.1 | iExec |
| STORJ | 0.1 | Storj |
| KAVA | 0.1 | Kava |
| WAVES | 0.01 | Waves |
| DCR | 0.001 | Decred |
| LSK | 0.1 | Lisk |
| STEEM | 1.0 | Steem |
| HIVE | 0.1 | Hive |
| SC | 10.0 | Siacoin |
| DGB | 10.0 | DigiByte |
| NANO | 0.01 | Nano |
| RVN | 1.0 | Ravencoin |
| CVC | 1.0 | Civic |
| OXT | 1.0 | Orchid |
| REP | 0.01 | Augur |
| ANT | 0.1 | Aragon |
| BNT | 0.1 | Bancor |
| REN | 1.0 | Ren |
| KEEP | 1.0 | Keep Network |
| NU | 1.0 | NuCypher |
| TBTC | 0.0001 | tBTC |
| MLN | 0.001 | Enzyme |

## Custom Threshold Configuration

### JSON Format

Create a custom thresholds file:

```json
{
  "BTC": 0.0005,
  "ETH": 0.005,
  "USDT": 5.0,
  "CUSTOM_TOKEN": 100.0
}
```

### Usage

#### In Node.js

```javascript
const binanceApi = require('./binance-api');

const customThresholds = {
  'BTC': 0.0005,
  'ETH': 0.005
};

const dust = await binanceApi.identifyDust(customThresholds);
```

#### Via CLI

```bash
node dust-analyzer.js --thresholds ./my-thresholds.json
```

#### Via binance-api.js

```bash
node binance-api.js dust '{"BTC":0.0005,"ETH":0.005}'
```

## Threshold Guidelines

### Setting Your Own Thresholds

When defining custom thresholds, consider:

1. **Minimum Trade Size**: Check the exchange's minimum order size for each pair
2. **Transaction Fees**: Ensure the value exceeds withdrawal/trading fees
3. **Personal Preference**: Some users consider anything under $1-5 as dust
4. **Asset Volatility**: High-volatility assets may need higher thresholds

### Example: USD-Based Thresholds

```json
{
  "_comment": "Minimum $5 USD equivalent per asset",
  "BTC": 0.0001,
  "ETH": 0.002,
  "BNB": 0.02,
  "SOL": 0.05,
  "USDT": 5.0,
  "USDC": 5.0
}
```

## Updating Thresholds

Thresholds should be reviewed periodically as:
- Exchange minimums may change
- New assets are listed
- Asset values fluctuate significantly

## References

- [Binance Trading Rules](https://www.binance.com/en/trade-rule)
- [Binance API Filters](binance-api-docs.md#trading-filters)
- [MIN_NOTIONAL Filter](binance-api-docs.md#min_notional)
