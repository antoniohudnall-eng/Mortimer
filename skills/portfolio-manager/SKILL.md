# Portfolio Manager
## Autonomous Crypto Portfolio Management

**Role:** Financial Operations Agent  
**Scope:** Multi-exchange portfolio optimization, dust consolidation, DCA execution  
**Company:** Performance Supply Depot LLC  
**Created:** 2026-03-07 06:26 UTC

---

## Purpose

This skill enables agents to manage cryptocurrency portfolios across multiple exchanges with autonomous decision-making capabilities, risk controls, and company-first investment ethos.

Based on **the-great-cryptonio** operational model.

---

## Core Capabilities

### 1. Multi-Exchange Management
| Exchange | Connection | Features |
|----------|------------|----------|
| Binance.US | API + Secret | Dust sweep, DCA, spot trading |
| Gemini | API + Secret | Institutional features, custody |
| Base (EVM) | Private key | NFT operations, gas management |
| Others | Extensible | Via credential vault |

### 2. Dust Consolidation (Phase 1)
- **Trigger:** Positions <$5 USD equivalent
- **Action:** Convert to USDT/USDC
- **Minimum:** $2 to cover fees
- **Frequency:** Every 6 hours (configurable)
- **Volume Limit:** $10/day across all exchanges

### 3. Dollar-Cost Averaging (Phase 2)
- **Trigger:** Asset drops >5% in 24h
- **Buy Amount:** Configurable ($5 default)
- **Cooldown:** 48h between purchases
- **Monthly Cap:** $50 total
- **Target Assets:** BTC, ETH (configurable)

### 4. Risk Management
- ❌ Never sell core positions (BTC >0.001, LTC, BCH)
- ❌ Never exceed daily volume limit
- ❌ Never trade without logging
- ⚠️ Captain override: "PORTFOLIO HALT"

---

## Decision Framework

All trades must answer:
1. Does this serve company interests?
2. Is this sustainable vs. speculative?
3. Am I protecting capital?
4. Can I explain this to Captain?

**Default:** Growth over speculation, preservation over risk.

---

## Credential Vault

**Location:** `agent_sandboxes/{agent-name}/vault/`

Required files:
- `binance_us.env` — Primary account
- `binance_us_second.env` — Secondary account
- `gemini.env` — Gemini access
- `evm_wallet.json` — Base/EVM private key

**Permissions:** 600 (owner only)

---

## Reporting

### Daily Digest (06:00 UTC)
```
## PORTFOLIO SNAPSHOT — YYYY-MM-DD
**Portfolio Value:** $XXX.XX
**24h Change:** ±X.XX%
**Exchanges Active:** X
**Dust Sweeped:** $X.XX
**DCA Executed:** $X.XX (Y positions)
**Core Holdings:** Protected ✅
```

### Alert Triggers
- Portfolio drops >10%
- Failed trade (3x = auto-suspend)
- API error >5/hour
- Daily volume approaching limit

---

## Usage

```javascript
// Load skill
const portfolio = require('portfolio-manager');

// Initialize with vault path
const cryptonio = portfolio.init({
  vault: '/agent_sandboxes/cryptonio/vault',
  limits: {
    dailyVolume: 10.00,
    monthlyDCA: 50.00,
    dustThreshold: 5.00
  }
});

// Execute dust sweep
await cryptonio.sweepDust();

// Check DCA triggers
await cryptonio.checkDCATriggers();

// Get unified balance
const report = await cryptonio.getUnifiedBalance();
```

---

## Attribution

**Origin:** the-great-cryptonio  
**Company:** Performance Supply Depot LLC  
**Pattern:** Multi-exchange autonomous portfolio optimization  
**Status:** Active production skill

---

*Every dollar has a job. Deploy with purpose.* 🎰
