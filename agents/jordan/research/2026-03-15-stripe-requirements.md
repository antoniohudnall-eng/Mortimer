# Stripe Mobile Integration Requirements
**Research Date:** 2026-03-15  
**Prepared for:** Miles  
**Status:** Actionable Intelligence

---

## Executive Summary

Stripe offers two primary paths for mobile payments: **Stripe Checkout** (fastest, hosted) and **PaymentSheet SDK** (native, customizable). For fastest time-to-market, use Stripe Checkout. For full native control, use the iOS/Android SDKs with PaymentSheet.

---

## 1. What You Need to Accept Payments in a Mobile App

### Option A: Stripe Checkout (Fastest - 2/5 Complexity)
- **What it is:** Redirect users to a Stripe-hosted payment page
- **Requirements:**
  - Stripe account (free to create)
  - Backend endpoint to create Checkout Sessions
  - HTTPS success/cancel URLs
- **Mobile integration:** Open checkout URL in WebView or browser
- **Apple Pay/Google Pay:** Supported automatically (Apple Pay enabled by default, Google Pay must be enabled in Dashboard)

### Option B: Native SDK Integration (Recommended for UX)
- **iOS SDK:** `stripe-ios` (Swift/Objective-C)
- **Android SDK:** `stripe-android` (Kotlin/Java)
- **Key Components:**
  - **PaymentSheet** (prebuilt UI) - Recommended
  - **PaymentSheet FlowController** (custom UI)
  - **Apple Pay / Google Pay** buttons (separate integration)
  - **Address Element** (autofill)

### Technical Requirements (Native SDK)
| Component | iOS | Android |
|-----------|-----|---------|
| Minimum OS | iOS 13+ | API 21+ (Android 5.0) |
| Language | Swift 5.9+ / Obj-C | Kotlin 1.8+ / Java 8+ |
| Backend | Required for PaymentIntent creation | Required for PaymentIntent creation |
| Apple Pay | iOS 11.2+ | N/A |
| Google Pay | N/A | Android 5.0+ |

### Required Backend (Both Options)
- Server endpoint to create PaymentIntents or Checkout Sessions
- Stripe Secret Key (stored server-side only)
- HTTPS endpoint for webhooks (optional but recommended)

---

## 2. Fees

### Standard Pricing (No Monthly Fees)
| Transaction Type | Fee |
|-----------------|-----|
| **Domestic Cards** | **2.9% + $0.30** per transaction |
| **International Cards** | + 1.5% additional |
| **Instant Bank Payments** | 2.6% + $0.30 |
| **Buy Now Pay Later (Klarna)** | 5.99% + $0.30 |
| **In-Person (Terminal)** | 2.7% + $0.05 |

### Additional Fees
- **Chargebacks:** $15 per dispute (waived if dispute is won)
- **Radar (Fraud Protection):** Included free with standard pricing
- **Radar Advanced:** $0.02 per screened transaction
- **Invoicing:** 0.4% of transaction (max $2 per invoice)

### Volume Discounts
- Available for businesses processing $100K+/month
- Contact Stripe Sales for custom pricing

---

## 3. Business Entity Requirements

### Do You Need a Business Entity?
**No, but strongly recommended.**

| Scenario | Requirement |
|----------|-------------|
| **Sole Proprietor / Individual** | Can use SSN, personal bank account |
| **LLC / Corporation** | EIN required, business bank account |
| **Non-US** | Supported in 40+ countries |

### What You Need to Activate Account
- Bank account (personal or business)
- Tax ID (SSN or EIN)
- Business website or app
- Description of what you're selling
- Estimated transaction volume

### Stripe Atlas (If Incorporating)
- **Cost:** $500 one-time
- **Includes:** Delaware C-Corp or LLC, EIN, equity documents, $2,500 Stripe credits
- **Timeline:** 2 business days to incorporate
- **Best for:** Startups planning to raise funding

---

## 4. Fastest Path to Accepting Payments

### Timeline: 1-2 Days

**Day 1: Account Setup**
1. Create Stripe account (5 minutes)
2. Complete identity verification
3. Add bank account for payouts
4. Enable payment methods in Dashboard

**Day 1-2: Integration**

#### Fastest Route (Stripe Checkout)
```
1. Create backend endpoint → Create Checkout Session
2. Mobile app → Call endpoint → Open checkout URL in browser/WebView
3. User pays on Stripe → Redirect to success URL
4. Verify payment via webhook or redirect
```
**Time:** 2-4 hours

#### Native Route (PaymentSheet)
```
1. Install SDK (CocoaPods/SPM for iOS, Gradle for Android)
2. Create backend endpoint for PaymentIntent
3. Initialize PaymentSheet with client_secret
4. Present PaymentSheet UI
5. Handle payment result
```
**Time:** 1-2 days

### Testing
- Use Stripe test mode (no real charges)
- Test cards provided by Stripe
- Test Apple Pay / Google Pay in sandbox

### Going Live
- Toggle from test mode to live mode
- Replace test keys with live keys
- Submit for app store review (if native SDK)

---

## Recommendations

### For MVP / Fastest Launch
→ **Use Stripe Checkout**
- Minimal code
- PCI compliance handled by Stripe
- Works immediately

### For Production / Best UX
→ **Use PaymentSheet SDK**
- Native look and feel
- Apple Pay / Google Pay built-in
- More control over branding

### Business Structure
- **Start as:** Sole proprietorship (use SSN)
- **Upgrade to:** LLC once revenue justifies it
- **Consider Atlas if:** Raising funding or need C-Corp

---

## Key Resources
- **iOS SDK:** https://github.com/stripe/stripe-ios
- **Android SDK:** https://github.com/stripe/stripe-android
- **Stripe Dashboard:** https://dashboard.stripe.com
- **Test Cards:** https://stripe.com/docs/testing

---

## Next Steps
1. [ ] Create Stripe account at dashboard.stripe.com
2. [ ] Decide: Checkout vs Native SDK
3. [ ] Set up backend endpoint (if using native SDK)
4. [ ] Implement and test in test mode
5. [ ] Go live

**Questions requiring Miles' decision:**
- Checkout vs Native SDK preference?
- Current business entity status?
- Estimated monthly transaction volume?
