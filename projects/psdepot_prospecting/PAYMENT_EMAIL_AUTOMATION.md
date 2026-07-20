# Payment Email Automation Blueprint

**Created:** 2026-07-20
**Status:** ARCHITECTURE READY

---

## Vision

When a payment is received → Client receives personalized thank-you email with the flyer.

---

## Components Needed

### 1. Email Template Engine
- Uses `payment_thankyou_flyer.html` as base
- Replaces placeholders: `{DATE}`, `{REF}`, `{AMOUNT}`, `{METHOD}`, `{NAME}`, `{EMAIL}`
- Sends via SMTP (Gmail, SendGrid, or PSD email server)

### 2. Payment Trigger Points
```python
# When payment recorded in invoices table:
- Update status to 'paid'
- Trigger email send
- Log to payment_history
```

### 3. Database Enhancement
```sql
-- Add to invoices table:
payment_received_date TEXT,
payment_method TEXT,
payment_reference TEXT,
thankyou_email_sent BOOLEAN DEFAULT 0,
thankyou_email_sent_at TIMESTAMP
```

### 4. Email Service Options

| Service | Pros | Cons |
|---------|------|------|
| **Gmail SMTP** | Free, easy | 500/day limit |
| **SendGrid** | Professional, high volume | API key needed |
| **Mailgun** | Good deliverability | API key needed |
| **PSD Mail Server** | Full control | Requires server setup |

---

## Implementation Plan

### Phase 1: Manual Trigger (Now)
```bash
python3 send_payment_thankyou.py --invoice=PSD-20260720-0001
```

### Phase 2: Webhook Trigger (Future)
- Invoice marked "paid" in CRM → triggers email
- Webhook endpoint: `/api/payment-confirmed/<invoice_id>`

### Phase 3: Full Automation (Future)
- Stripe/PayPal webhook on payment
- Auto-generate + send email
- Log everything to DB

---

## Files to Create

| File | Purpose |
|------|---------|
| `email_thankyou_sender.py` | Core email engine |
| `email_config.py` | SMTP settings |
| `payment_thankyou_email.html` | Already exists ✓ |

---

## Environment Variables Needed

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=info@psdepot.com
SMTP_PASS=your_app_password
FROM_NAME="Performance Supply Depot"
```

---

## Captain's Note

> "Email it to our clients when payment received, in the future an automated process."

**This blueprint is the foundation. Ready to build when you are.**
