---
name: paydify-payments
version: 1.0.0
description: Integrate Paydify crypto payment gateway into DroidScript games and apps. Create payment sessions, display QR codes, poll for confirmations, and handle webhooks.
author: Performance Supply Depot LLC
---

# Paydify Payments Skill

Complete Paydify payment integration for DroidScript applications.

## Quick Start

```javascript
// Load the library
var PaydifyPayments = require("./lib/PaydifyPayments.js");

// Initialize
var paydify = new PaydifyPayments({
    apiKey: "your-api-key",
    merchantId: "your-merchant-id",
    currency: "BTC",
    environment: "sandbox" // or "production"
});

// Create payment
paydify.createPayment({
    amount: 0.001,
    description: "Chronospace Explorer Full Version",
    orderId: "ORDER-" + Date.now()
}, function(paymentData, error) {
    if (error) {
        app.ShowPopup("Payment failed: " + error.message);
        return;
    }
    
    // Display payment UI
    paydify.displayPaymentUI(paymentData, {
        layout: gameLayout,
        onSuccess: function(data) {
            app.ShowPopup("Payment confirmed!");
            unlockFullGame();
        },
        onFailure: function(data) {
            app.ShowPopup("Payment failed or expired");
        }
    });
});
```

## API Reference

### Constructor

```javascript
new PaydifyPayments(config)
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| apiKey | string | Yes | Your Paydify API key |
| merchantId | string | Yes | Your merchant ID |
| currency | string | No | Default currency (BTC, ETH, etc.) |
| environment | string | No | "sandbox" or "production" |

### Methods

#### createPayment(options, callback)

Create a new payment request.

| Option | Type | Description |
|--------|------|-------------|
| amount | number | Amount to charge |
| currency | string | Crypto currency |
| description | string | Payment description |
| orderId | string | Your internal order ID |
| callbackUrl | string | Webhook URL for notifications |
| metadata | object | Additional data |

#### displayPaymentUI(paymentData, uiConfig)

Display payment QR code and status in your app.

| uiConfig | Type | Description |
|----------|------|-------------|
| layout | Layout | Parent layout (optional) |
| onSuccess | function | Called on payment confirmation |
| onFailure | function | Called on failure/expiry |

#### pollPaymentStatus(paymentId, callback, interval)

Poll for payment status updates.

#### verifyWebhook(payload, signature, secret)

Verify webhook signature for payment notifications.

#### getPaymentHistory(callback, filters)

Retrieve past payments.

## File Location

```
games/ChronospaceExplorer/lib/PaydifyPayments.js
```

## Dependencies

- DroidScript Web API (XMLHttpRequest)
- Internet connection

## Security Notes

- Never expose API keys in client-side code in production
- Use server-side validation for critical operations
- Verify webhook signatures
- Store purchase tokens securely

## Examples

See `examples/paydify-integration.js` for complete implementation.
