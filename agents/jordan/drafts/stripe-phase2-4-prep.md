# Stripe Phase 2-4 Preparation

**Date:** 2026-03-15  
**Status:** Ready for Miles' Stripe account setup  
**Next:** Phase 2 (Backend) → Phase 3 (Webhook) → Phase 4 (Testing)

---

## Phase 2: Backend PaymentIntent Endpoint

### Node.js Implementation (Express)

```javascript
// server.js - PaymentIntent endpoint
const express = require('express');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const app = express();

app.use(express.json());

// Create PaymentIntent
app.post('/api/create-payment-intent', async (req, res) => {
  try {
    const { amount, currency = 'usd', metadata = {} } = req.body;
    
    // Validate amount
    if (!amount || amount < 50) { // Minimum 50 cents
      return res.status(400).json({ error: 'Invalid amount' });
    }
    
    const paymentIntent = await stripe.paymentIntents.create({
      amount: amount, // Amount in cents
      currency: currency,
      automatic_payment_methods: { enabled: true },
      metadata: {
        ...metadata,
        created_at: new Date().toISOString(),
      },
    });
    
    res.json({
      clientSecret: paymentIntent.client_secret,
      paymentIntentId: paymentIntent.id,
    });
  } catch (error) {
    console.error('PaymentIntent error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Retrieve PaymentIntent status
app.get('/api/payment-intent/:id', async (req, res) => {
  try {
    const paymentIntent = await stripe.paymentIntents.retrieve(req.params.id);
    res.json({
      status: paymentIntent.status,
      amount: paymentIntent.amount,
      currency: paymentIntent.currency,
      metadata: paymentIntent.metadata,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 4242;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
```

### Python Implementation (Flask)

```python
# app.py - PaymentIntent endpoint
from flask import Flask, request, jsonify
import stripe
import os
from datetime import datetime

app = Flask(__name__)
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

@app.route('/api/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = request.json
        amount = data.get('amount')
        currency = data.get('currency', 'usd')
        metadata = data.get('metadata', {})
        
        # Validate amount
        if not amount or amount < 50:
            return jsonify({'error': 'Invalid amount'}), 400
        
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            automatic_payment_methods={'enabled': True},
            metadata={
                **metadata,
                'created_at': datetime.utcnow().isoformat(),
            }
        )
        
        return jsonify({
            'clientSecret': payment_intent.client_secret,
            'paymentIntentId': payment_intent.id,
        })
    except Exception as e:
        print(f"PaymentIntent error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/payment-intent/<id>', methods=['GET'])
def get_payment_intent(id):
    try:
        payment_intent = stripe.PaymentIntent.retrieve(id)
        return jsonify({
            'status': payment_intent.status,
            'amount': payment_intent.amount,
            'currency': payment_intent.currency,
            'metadata': payment_intent.metadata,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=4242)
```

### Environment Variables

```bash
# .env - NEVER commit this file
STRIPE_SECRET_KEY=sk_test_...        # Test key for development
STRIPE_PUBLISHABLE_KEY=pk_test_...   # Frontend key
STRIPE_WEBHOOK_SECRET=whsec_...        # Webhook endpoint secret
PORT=4242
NODE_ENV=development
```

---

## Phase 3: Webhook Handler Template

### Node.js Webhook Handler

```javascript
// webhook.js - Stripe webhook handler
const express = require('express');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const app = express();

// Use raw body for webhook signature verification
app.post('/webhook', 
  express.raw({ type: 'application/json' }),
  async (req, res) => {
    const sig = req.headers['stripe-signature'];
    const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;
    
    let event;
    
    try {
      event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
    } catch (err) {
      console.error(`Webhook signature verification failed: ${err.message}`);
      return res.status(400).send(`Webhook Error: ${err.message}`);
    }
    
    // Handle events
    switch (event.type) {
      case 'payment_intent.succeeded':
        const paymentIntent = event.data.object;
        console.log('PaymentIntent succeeded:', paymentIntent.id);
        
        // TODO: Fulfill order, send confirmation email, update database
        await fulfillOrder(paymentIntent);
        break;
        
      case 'payment_intent.payment_failed':
        const failedPayment = event.data.object;
        console.log('Payment failed:', failedPayment.id);
        
        // TODO: Notify customer, log failure
        await handleFailedPayment(failedPayment);
        break;
        
      case 'charge.refunded':
        const refund = event.data.object;
        console.log('Refund processed:', refund.id);
        
        // TODO: Update order status, notify customer
        await handleRefund(refund);
        break;
        
      case 'customer.subscription.created':
        const subscription = event.data.object;
        console.log('Subscription created:', subscription.id);
        break;
        
      case 'invoice.payment_succeeded':
        const invoice = event.data.object;
        console.log('Invoice paid:', invoice.id);
        break;
        
      default:
        console.log(`Unhandled event type: ${event.type}`);
    }
    
    res.json({ received: true });
  }
);

// Fulfillment functions
async function fulfillOrder(paymentIntent) {
  // Update database
  // Send confirmation email
  // Grant access to product
  // Log transaction
}

async function handleFailedPayment(paymentIntent) {
  // Log failure
  // Send retry email to customer
  // Alert admin if repeated failures
}

async function handleRefund(charge) {
  // Update order status to refunded
  // Revoke product access if needed
  // Send refund confirmation
}
```

### Python Webhook Handler

```python
# webhook.py - Stripe webhook handler
from flask import Flask, request, jsonify
import stripe
import os

app = Flask(__name__)
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
endpoint_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify({'error': 'Invalid signature'}), 400
    
    # Handle events
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        print(f"PaymentIntent succeeded: {payment_intent['id']}")
        fulfill_order(payment_intent)
        
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        print(f"Payment failed: {payment_intent['id']}")
        handle_failed_payment(payment_intent)
        
    elif event['type'] == 'charge.refunded':
        charge = event['data']['object']
        print(f"Refund processed: {charge['id']}")
        handle_refund(charge)
    
    return jsonify({'status': 'success'}), 200

def fulfill_order(payment_intent):
    """Fulfill the order after successful payment"""
    pass

def handle_failed_payment(payment_intent):
    """Handle failed payment"""
    pass

def handle_refund(charge):
    """Handle refund"""
    pass
```

---

## Phase 4: API Key Security Best Practices

### 1. Environment Variables

```bash
# .env.example (safe to commit)
STRIPE_SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=
STRIPE_WEBHOOK_SECRET=

# .env (NEVER commit - add to .gitignore)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### 2. Key Rotation Strategy

```javascript
// key-rotation.js
class StripeKeyManager {
  constructor() {
    this.primaryKey = process.env.STRIPE_SECRET_KEY;
    this.fallbackKey = process.env.STRIPE_SECRET_KEY_FALLBACK;
  }
  
  async rotateKeys() {
    // 1. Create new restricted key in Stripe Dashboard
    // 2. Update environment variable
    // 3. Test with new key
    // 4. Revoke old key after 24h grace period
  }
}
```

### 3. Restricted API Keys

Create restricted keys in Stripe Dashboard with only necessary permissions:
- `write` for PaymentIntents
- `read` for Customers (if needed)
- No access to Payouts, Refunds unless required

### 4. Webhook Security Checklist

- [ ] Verify webhook signature on every request
- [ ] Use HTTPS only (never HTTP in production)
- [ ] Implement idempotency (don't process same event twice)
- [ ] Log all webhook events for debugging
- [ ] Return 200 quickly (process async if needed)
- [ ] Implement exponential backoff for retries

### 5. Frontend Security

```javascript
// Never expose secret keys in frontend
const stripe = Stripe(process.env.STRIPE_PUBLISHABLE_KEY); // OK - public
// const stripe = Stripe('sk_test_...'); // NEVER - secret key
```

---

## Testing Checklist

### Unit Tests

```javascript
// __tests__/payment.test.js
const request = require('supertest');
const app = require('../server');

describe('Payment Endpoints', () => {
  test('POST /api/create-payment-intent - success', async () => {
    const res = await request(app)
      .post('/api/create-payment-intent')
      .send({ amount: 2000, currency: 'usd' });
    
    expect(res.status).toBe(200);
    expect(res.body.clientSecret).toBeDefined();
  });
  
  test('POST /api/create-payment-intent - invalid amount', async () => {
    const res = await request(app)
      .post('/api/create-payment-intent')
      .send({ amount: 10 }); // Too low
    
    expect(res.status).toBe(400);
  });
});
```

### Integration Tests

- [ ] Test card: `4242 4242 4242 4242` (Visa success)
- [ ] Test card: `4000 0000 0000 0002` (Declined)
- [ ] Test card: `4000 0000 0000 9995` (Insufficient funds)
- [ ] Test 3D Secure: `4000 0025 0000 3155`
- [ ] Test webhook signature verification
- [ ] Test idempotency with duplicate events

### End-to-End Test Flow

1. **Create PaymentIntent** → Verify client_secret returned
2. **Confirm payment** (use Stripe test cards) → Verify success
3. **Webhook received** → Verify event processed
4. **Database updated** → Verify order created
5. **Confirmation sent** → Verify email delivered

### Load Testing

```bash
# Using Artillery or k6
npm install -g artillery
artillery quick --count 100 --num 10 http://localhost:4242/api/create-payment-intent
```

---

## Deployment Checklist

### Pre-Launch

- [ ] Switch to Stripe live keys
- [ ] Update webhook endpoint to production URL
- [ ] Configure webhook secret for live mode
- [ ] Test with small live transaction ($1)
- [ ] Set up monitoring (Stripe Dashboard + logs)
- [ ] Configure error alerting (Sentry, PagerDuty)

### Post-Launch Monitoring

- [ ] Payment success rate > 95%
- [ ] Webhook delivery success rate > 99%
- [ ] Average response time < 500ms
- [ ] Error rate < 1%

---

## Required Packages

```json
// package.json
{
  "dependencies": {
    "express": "^4.18.0",
    "stripe": "^14.0.0",
    "dotenv": "^16.0.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "supertest": "^6.0.0"
  }
}
```

```txt
# requirements.txt (Python)
flask==3.0.0
stripe==7.0.0
python-dotenv==1.0.0
gunicorn==21.0.0
```

---

## Next Steps for Miles

1. **Complete Stripe account setup** (business verification)
2. **Generate API keys** (test mode first)
3. **Configure webhook endpoint** in Stripe Dashboard
4. **Deploy backend** to staging environment
5. **Run test suite** (use provided checklist)
6. **Switch to live mode** after successful tests

**Questions?** Flag any blockers for immediate escalation.
