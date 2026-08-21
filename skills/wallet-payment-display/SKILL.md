---
name: wallet-payment-display
version: 2.0.0
description: Multi-currency wallet payment display for DroidScript apps. Supports BTC, ETH, USDC, USDT with fiat conversion (USD, EUR, GBP). Multi-language ready (8 languages).
author: Performance Supply Depot LLC
---

# Wallet Payment Display Skill v2.0

Multi-currency, multi-language crypto payment solution for DroidScript games and POS systems.

## Supported Currencies (ReggieStarr Compatible)

### Crypto
- **BTC** (Bitcoin) - ₿
- **ETH** (Ethereum) - Ξ
- **USDC** (USD Coin) - $ (stable)
- **USDT** (Tether) - $ (stable)

### Fiat Display
- **USD** - US Dollar - $
- **EUR** - Euro - €
- **GBP** - British Pound - £

## Supported Languages (8 Languages)

1. **English** (en) - Primary
2. **Spanish** (es) - Español
3. **French** (fr) - Français
4. **German** (de) - Deutsch
5. **Arabic** (ar) - العربية
6. **Chinese** (zh) - 中文
7. **Korean** (ko) - 한국어
8. **Japanese** (ja) - 日本語

## Quick Start

```javascript
// Load library
var WalletPaymentDisplay = require("./lib/WalletPaymentDisplay.js");

// Initialize with multi-currency support
var wallet = new WalletPaymentDisplay({
    walletAddress: "bc1q...",  // or ETH address, USDC contract
    currency: "BTC",           // "BTC" | "ETH" | "USDC" | "USDT"
    fiatCurrency: "USD",       // "USD" | "EUR" | "GBP"
    suggestedAmount: 10.00,    // Amount in fiat
    language: "en"             // "en" | "es" | "fr" | "de" | "ar" | "zh" | "ko" | "ja"
});

// Show payment screen
wallet.showMultiCurrencyPaymentScreen({
    amounts: {
        "USD": 10.00,
        "EUR": 9.20,
        "GBP": 8.00,
        "BTC": 0.00025,
        "ETH": 0.0032,
        "USDC": 10.00,
        "USDT": 10.00
    },
    label: "Game Purchase",
    message: "Enjoyed the game? Support development!",
    onDismiss: function() { app.Exit(); }
});
```

## Multi-Currency Features

- **Currency Selector:** Let users choose payment currency
- **Fiat Conversion:** Display prices in USD/EUR/GBP
- **ReggieStarr Compatible:** Supports all POS currencies (USD, EUR, GBP, BTC, USDC, USDT)
- **Multi-Language UI:** All text localized to 8 languages
- **QR Code Generation:** Multi-format QR support
- **Exchange Rate API:** Real-time conversion rates

## API Reference

### Constructor

```javascript
new WalletPaymentDisplay(config)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| walletAddress | string | required | Receiving address |
| currency | string | "BTC" | "BTC" | "ETH" | "USDC" | "USDT" |
| fiatCurrency | string | "USD" | Display currency: "USD" | "EUR" | "GBP" |
| suggestedAmount | number | 0.001 | Amount in specified currency |
| language | string | "en" | UI language: "en" | "es" | "fr" | "de" | "ar" | "zh" | "ko" | "ja" |

### Methods

#### showMultiCurrencyPaymentScreen(options)

Display payment screen with all currency options.

| Option | Type | Description |
|--------|------|-------------|
| amounts | object | {USD, EUR, GBP, BTC, ETH, USDC, USDT} amounts |
| label | string | Payment description |
| message | string | Custom message (localized) |
| onDismiss | function | Callback on close |

#### generatePaymentURI(currency, amount, label)

Generate BIP21/BIP72 payment URI.

```javascript
var uri = wallet.generatePaymentURI("BTC", 0.001, "Game Purchase");
// bitcoin:bc1q...?amount=0.001&label=Game%20Purchase

var ethUri = wallet.generatePaymentURI("ETH", 0.01, "Item");
// ethereum:0x...?value=0.01

var usdcUri = wallet.generatePaymentURI("USDC", 10, "Store");
// ethereum:0x.../transfer?address=...&amount=10&token=USDC
```

#### getExchangeRates()

Get current exchange rates for all currencies.

```javascript
wallet.getExchangeRates(function(rates) {
    console.log(rates.BTC.USD);  // BTC to USD rate
    console.log(rates.ETH.EUR);  // ETH to EUR rate
    console.log(rates.USDC.USD); // 1.00
});
```

#### verifyPayment(currency, txid, callback)

Verify transaction on blockchain.

```javascript
wallet.verifyPayment("BTC", "txid-here", function(verified, confirmations, amount) {
    if (verified) {
        app.ShowPopup("Confirmed! " + confirmations + " confirmations, Amount: " + amount);
    }
});
```

#### checkBalance(currency, callback)

Check wallet balance.

```javascript
wallet.checkBalance("BTC", function(balance, error) {
    if (!error) {
        app.ShowPopup("Balance: " + balance + " BTC");
    }
});

wallet.checkBalance("USDC", function(balance, error) {
    if (!error) {
        app.ShowPopup("Balance: $" + balance + " USDC");
    }
});
```

### Language Support

```javascript
// Set language
wallet.setLanguage("es");  // Switch to Spanish

// Get localized string
var msg = wallet.getLocalizedString("payment_title");
// "Realizar Pago" (Spanish)
// "Make Payment" (English)
// "支払いをする" (Japanese)
```

**Supported String Keys:**
- `payment_title` - "Make Payment"
- `select_currency` - "Select Currency"
- `amount` - "Amount"
- `qr_code` - "Scan QR Code"
- `copy_address` - "Copy Address"
- `verifying` - "Verifying..."
- `thank_you` - "Thank You!"
- `payment_received` - "Payment Received"

## Currency Symbols

| Currency | Symbol | Code |
|----------|--------|------|
| USD | $ | USD |
| EUR | € | EUR |
| GBP | £ | GBP |
| BTC | ₿ | BTC |
| ETH | Ξ | ETH |
| USDC | $ | USDC |
| USDT | $ | USDT |

## ReggieStarr Integration

Compatible with ReggieStarr RS-79 POS:

```javascript
// ReggieStarr payment
var payment = new WalletPaymentDisplay({
    walletAddress: storeWallet,
    currency: currentCurrency,  // "USD", "EUR", "GBP", "BTC", "USDC", "USDT"
    fiatCurrency: displayCurrency,  // For display purposes
    suggestedAmount: transactionTotal,
    language: currentLanguage
});

// Show in POS UI
payment.showMultiCurrencyPaymentScreen({
    amounts: convertAllCurrencies(transactionTotal, displayCurrency),
    label: "POS Transaction " + transactionId,
    message: getLocalizedMessage("pos_payment", currentLanguage)
});
```

## Security Considerations

- **Public addresses only** — Never expose private keys
- **Address validation** — Verify address format per currency
- **Manual verification** — Check payments manually or via API
- **Exchange rate sources** — Use reliable APIs (CoinGecko, etc.)
- **Gas fees** — Display estimated ETH gas for USDC/USDT

## Workflow

```
User clicks "Pay"
    ↓
Show currency selection (USD, EUR, GBP, BTC, ETH, USDC, USDT)
    ↓
User selects currency → Show amount in selected currency
    ↓
Display QR code with payment URI
    ↓
User scans QR or copies address
    ↓
User sends payment from wallet
    ↓
Poll blockchain or user provides TXID
    ↓
Verify on blockchain
    ↓
Confirm payment, unlock content
```

## File Location

```
skills/wallet-payment-display/
├── SKILL.md                          ← This file
├── lib/
│   ├── WalletPaymentDisplay.js       ← Main library
│   ├── currencies/                   ← Currency configs
│   │   ├── BTC.js
│   │   ├── ETH.js
│   │   ├── USDC.js
│   │   └── USDT.js
│   └── languages/                    ← 8 language packs
│       ├── en.json
│       ├── es.json
│       ├── fr.json
│       ├── de.json
│       ├── ar.json
│       ├── zh.json
│       ├── ko.json
│       └── ja.json
└── examples/
    ├── multi-currency-payment.js
    ├── reggiestarr-integration.js
    └── language-switcher.js
```

## Dependencies

- `axios` - For exchange rate API calls
- `qrcode` - For QR generation
- `crypto` - For address validation

## Changelog

### v2.0.0 (2026-02-18)
- ✅ Added multi-currency support (BTC, ETH, USDC, USDT)
- ✅ Added fiat display (USD, EUR, GBP)
- ✅ Added 8-language support (en, es, fr, de, ar, zh, ko, ja)
- ✅ ReggieStarr POS compatibility
- ✅ Multi-currency QR generation
- ✅ Real-time exchange rates

### v1.0.0
- BTC-only support
- Basic QR generation

---

**ReggieStarr Compatible:** ✅ All 6 currencies supported  
**Multi-Language:** ✅ 8 languages ready  
**Version:** 2.0.0  
**Updated:** 2026-02-18
