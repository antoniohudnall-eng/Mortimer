---
name: store-integration
version: 1.0.0
description: Unified store integration for DroidScript games supporting Payhip, Paydify, Google Play, and direct wallet payments. Display store selectors, handle checkouts, and verify purchases.
author: Performance Supply Depot LLC
---

# Store Integration Skill

Multi-platform store integration for selling DroidScript games.

## Supported Platforms

| Platform | Payment Type | Integration |
|----------|--------------|-------------|
| Payhip | Fiat (Card/PayPal) | API + WebView |
| Paydify | Crypto (BTC, ETH) | API |
| Google Play | Mixed | Native billing |
| Direct Wallet | Crypto (BTC) | QR Code display |

## Quick Start

```javascript
// Load library
var StoreIntegration = require("./lib/StoreIntegration.js");

// Initialize
var store = new StoreIntegration({
    payhipApiKey: "your-payhip-key",
    payhipStoreUrl: "https://payhip.com/your-store",
    paydifyApiKey: "your-paydify-key",
    paydifyStoreUrl: "https://paydify.com/your-store",
    productId: "your-product-id"
});

// Show store selector
store.showStoreSelector({
    productName: "Chronospace Explorer",
    priceUsd: 4.99,
    priceBtc: 0.00012,
    onDirectWallet: function() {
        // Show wallet payment screen
        walletDisplay.showExitPaymentScreen();
    }
});
```

## Platform-Specific Setup

### Payhip

1. Create Payhip account at https://payhip.com
2. Upload your APK as a digital product
3. Get API key from dashboard
4. Configure product ID

### Paydify

1. Create merchant account at https://paydify.com
2. Set up crypto wallet
3. Get API credentials
4. Configure webhook URL

### Google Play

1. Create Google Play Developer account ($25)
2. Sign APK with release key
3. Upload to Play Console
4. Set up in-app products

### Direct Wallet

1. Create BTC wallet (Electrum, Wasabi, etc.)
2. Copy receiving address
3. Configure in WalletPaymentDisplay

## API Reference

### Constructor

```javascript
new StoreIntegration(config)
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| payhipApiKey | string | No | Payhip API key |
| payhipStoreUrl | string | No | Your Payhip store URL |
| paydifyApiKey | string | No | Paydify API key |
| paydifyStoreUrl | string | No | Your Paydify store URL |
| productId | string | No | Default product ID |

### Methods

#### showStoreSelector(options)

Display unified store selection dialog.

| Option | Type | Description |
|--------|------|-------------|
| productName | string | Product display name |
| priceUsd | number | Price in USD |
| priceBtc | number | Price in BTC |
| onDirectWallet | function | Callback for wallet option |

#### openPayhipCheckout(options)

Open Payhip checkout (WebView or browser).

#### openPaydifyCheckout(options)

Open Paydify crypto checkout.

#### verifyPayhipPurchase(orderId, callback)

Verify Payhip purchase via API.

#### validateLicense(licenseKey, callback)

Validate purchase license (requires backend).

### License Management

```javascript
// Store purchase token
store.storePurchaseToken("token-from-purchase");

// Check if purchased
if (store.hasPurchased()) {
    unlockFullGame();
}

// Get stored token
var token = store.getPurchaseToken();
```

## File Location

```
games/ChronospaceExplorer/lib/StoreIntegration.js
```

## Security

- Store API keys securely
- Use server-side validation for licenses
- Implement receipt verification
- Protect against tampering

## Examples

See `examples/store-integration-demo.js` for complete workflow.
