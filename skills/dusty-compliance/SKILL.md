---
name: dusty-compliance
description: Regulatory compliance and legal requirements for Dusty crypto wallet operations. Covers KYC/AML, money transmission licensing, custody regulations, and tax reporting obligations for multi-exchange crypto consolidation services.
---

# Dusty Compliance Skill

Navigate regulatory requirements for operating a crypto dust consolidation wallet service.

## Overview

Dusty handles crypto assets across multiple exchanges and blockchains. This creates regulatory obligations in most jurisdictions.

## Key Compliance Areas

### 1. Money Transmission / MSB Registration

**When Required:**
- Transmitting crypto on behalf of others
- Holding customer funds (even temporarily)
- Facilitating transfers between parties

**US Requirements:**
- Register as MSB (Money Services Business) with FinCEN
- State-by-state money transmitter licenses may be required
- Exception: If Dusty only provides software and never touches funds

**International:**
- EU: MiCA regulations (effective 2024-2025)
- UK: FCA registration for cryptoasset businesses
- Most jurisdictions have similar requirements

### 2. KYC / AML Compliance

**Required for:**
- Public users (not internal employees)
- Any transaction > $1,000 equivalent
- Suspicious activity detection

**Implementation:**
```
Identity Verification:
  - Government-issued ID
  - Proof of address
  - Liveness check (selfie)

Ongoing Monitoring:
  - Transaction screening
  - PEP (Politically Exposed Persons) checks
  - Sanctions screening (OFAC, UN, EU)
  - Suspicious Activity Reports (SARs)
```

### 3. Custody & Wallet Structure

**Critical Decision:**
| Model | Regulatory Burden | User Experience |
|-------|------------------|-----------------|
| Non-custodial (user controls keys) | Low - you're just software | User manages keys |
| Custodial (you hold keys) | High - you're a bank/payment institution | Seamless but regulated |

**Recommendation for Dusty MVP:**
Start non-custodial. Users hold their own keys. Dusty only orchestrates API calls on their behalf. This dramatically reduces regulatory burden.

### 4. Tax Reporting

**Employee Payments in Crypto:**
- W-2 must reflect USD equivalent at time of payment
- Employee responsible for capital gains on appreciation
- Employer must withhold/pay FICA taxes in USD

**User Dust Consolidation:**
- Each consolidation = taxable event (potentially)
- Users need 1099-B or transaction history
- Consider partnering with crypto tax software (CoinTracker, Koinly)

### 5. Bitgert & Exchange Compliance

**API Usage:**
- Each exchange has ToS restrictions
- Bitgert may have geographic restrictions
- Monitor for regulatory changes

**Geographic Blocking:**
- New York (BitLicense required)
- Certain sanctioned countries
- China (crypto trading banned)

## Compliance Roadmap

### Phase 1: Internal Only (Current)
- ✅ No public users
- ✅ Minimal regulatory exposure
- ⚠️ Still document employee crypto payments for tax

### Phase 2: Beta / Limited Public
- [ ] Terms of Service drafted
- [ ] Privacy Policy compliant (GDPR/CCPA)
- [ ] Geographic restrictions implemented
- [ ] US: FinCEN MSB registration (if custodial)
- [ ] KYC provider selected (for public users)

### Phase 3: Full Public Launch
- [ ] State-by-state MSB licenses (if custodial)
- [ ] Annual compliance audits
- [ ] AML program documented
- [ ] Compliance officer appointed
- [ ] Incident response plan

## Quick Compliance Check

Run this checklist before each phase:

```bash
# Are we touching customer funds?
USER_HOLDS_KEYS=true  # Set false if you custody

# Are we transmitting between parties?
PEER_TO_PEER_ENABLED=false

# What's our transaction volume/month?
VOLUME_USD=0  # Update monthly

# Do we have US users?
US_USERS=true

# Do we have EU users?
EU_USERS=false
```

## Resources

**US:**
- FinCEN: https://www.fincen.gov/msb-state-selector
- IRS Crypto Guidance: https://www.irs.gov/individuals/international-taxpayers/frequently-asked-questions-on-virtual-currency-transactions

**International:**
- FATF Virtual Asset Guidance: https://www.fatf-gafi.org/publications/fatfrecommendations/documents/guidance-rba-virtual-assets-2021.html
- EU MiCA: https://www.esma.europa.eu/esmas-activities/digital-finance-and-innovation/markets-crypto-assets-mica

**KYC Providers:**
- Persona (https://withpersona.com) - Good for startups
- Onfido - Enterprise-grade
- Jumio - Established provider

## Cost Estimates

**Minimal Compliance (Non-custodial):**
- Legal review: $5K-15K
- Terms/Privacy Policy: $2K-5K
- KYC integration: $1K-3K setup + $1-3 per check

**Full Compliance (Custodial):**
- MSB registration: $0 (FinCEN) but $50K-500K+ state licenses
- Compliance program: $50K-200K setup
- Annual audits: $20K-100K

## Recommendation

**For Dusty 2026:**

1. **Stay non-custodial** - Users hold keys, Dusty just orchestrates
2. **Internal-only for Phase 1** - Limit exposure while building
3. **Simple terms for public beta** - Disclose risks, limit liability
4. **Block NY and sanctioned countries** - Easy compliance win
5. **Partner with tax provider** - Don't build reporting yourself

This keeps 2-year runway focused on product, not legal.

## Emergency Contacts

**When to call a lawyer:**
- Before public launch
- If user funds are lost/compromised
- If subpoenaed for user data
- Before adding custodial features
- State AG inquiry received
