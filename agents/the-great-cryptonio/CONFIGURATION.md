# Cryptonio Trading Configuration
## Strategy: Dust Consolidation + DCA (Phased)

**Activated:** 2026-03-06 22:49 UTC  
**Authority:** Captain (Antonio Maurice Hudnall)  
**Phase:** 1 of 3

---

## PHASE 1: Dust Consolidation (ACTIVE)

### Objective
Eliminate small balances (<$5 USD) by converting to USDC

### Rules
| Parameter | Value |
|-----------|-------|
| Dust Threshold | <$5 USD equivalent |
| Target Asset | USDC |
| Minimum Trade | $2 USD |
| Gas Budget | Max 2% of trade value |
| Frequency | Every 6 hours |
| Max Daily Trades | 5 |

### Eligible Assets for Dust Sweep
- Current dust in Account 1: MANA, ETC, AAVE, VTHO, TRX, XRP
- Current dust in Account 2: KAVA, SNX, SHIB, AAVE, BCH, ACH, DOGE, XLM, VTHO

### Execution Logic
```
IF balance_value < $5 AND balance_value > $2:
    EXECUTE market_sell → USDC
    LOG trade + fee
    NOTIFY Captain (daily digest)
```

---

## PHASE 2: DCA on Dips (PENDING)

### Objective
Accumulate BTC on 5%+ daily drops

### Rules
| Parameter | Value |
|-----------|-------|
| Trigger | BTC drops >5% in 24h |
| Buy Amount | $5 USDC |
| Cooldown | 48h between purchases |
| Max Monthly | $50 ($10/week limit) |
| Target | Accumulate to 0.005 BTC total |

### Execution Logic
```
IF BTC_24h_change < -5% AND time_since_last_buy > 48h:
    EXECUTE buy BTC @ market
    AMOUNT = min($5, available_USDC)
    NOTIFY Captain immediately
```

---

## PHASE 3: Full Autonomy (FUTURE)

### Enable After
- 30 days profitable Phase 1+2
- Captain approval
- Expanded capital (>$100 liquid)

### Will Include
- Momentum rotation on approved alts
- Arbitrage between accounts
- Stop-loss automation
- Profit-taking rules

---

## RISK CONTROLS

### Hard Stops
- ❌ NEVER sell core positions (BTC >0.001, LTC, BCH)
- ❌ NEVER exceed $10/day trading volume
- ❌ NEVER hold non-USD stablecoins as target
- ❌ NEVER trade on weekends without alert

### Approval Required
- Any trade >$10 value
- Changing target asset from USDC
- Adjusting dust threshold
- Enabling Phase 2

### Auto-Suspensions
- Portfolio drops >20% in 24h
- 3 consecutive failed trades
- API errors >5/hour
- Captain command: "CRYPTONIO HALT"

---

## CURRENT STATE

**Portfolio:** $396.30 (Account 1: $188.36, Account 2: $207.94)  
**Liquid:** $47.99 USDT/USDC  
**Dust Eligible:** ~$25-30 in dust positions  
**First Sweep Estimate:** $20-25 USDC recovered

---

## 🎯 AUTHORITY TRANSFER — CAPTAIN'S ORDER
**Date:** 2026-03-07 06:08 UTC  
**Ordered by:** Captain
**Status:** 🟢 **CRYPTONIO IS IN CHARGE OF THE PORTFOLIO**

### Scope Granted:
- ✅ Full portfolio management authority (both accounts)
- ✅ Execute Phase 1 dust consolidation (permissionless under $10/day)
- ✅ Activate Phase 2 DCA strategy (BTC buy-on-dip)
- ✅ Make tactical asset allocation decisions
- ✅ Report to Captain daily (06:00 UTC)

### Boundaries (Hard Limits):
- ❌ NEVER exceed $10/day trading volume
- ❌ NEVER sell core positions (BTC >0.001, LTC, BCH)
- ❌ NEVER trade without logging to MEMORY
- ⚠️ Captain override available ("CRYPTONIO HALT")

### Authorization:
**"You are in charge of the portfolio."
— Captain, 2026-03-07 06:08 UTC**

---

## OPERATIONAL NOTES

**Run Mode:** **FULLY AUTONOMOUS** ✅ (Subject to hard stops above)  
**Notification:** Daily digest at 06:00 UTC  
**Logging:** All trades to `/memory/trading/YYYY-MM-DD.md`

**Next Review:** Weekly captain sync, or on alert trigger

---

💎🎰 *The Great Cryptonio — Autonomous Portfolio Maestro*  
*Phase 1: Dust Begone*
