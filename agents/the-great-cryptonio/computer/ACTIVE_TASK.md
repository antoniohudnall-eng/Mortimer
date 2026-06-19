# ACTIVE TASK — The Great Cryptonio
## Priority: HIGH | Deadline: Ongoing (Daily 06:00, 12:00, 18:00, 00:00 UTC)

**Assigned by:** Captain (Antonio Maurice Hudnall)  
**Date:** 2026-03-06 22:49 UTC  
**Type:** AUTONOMOUS OPERATION

---

## Mission: Dust Consolidation & DCA Trading

### Phase 1: Dust Sweeper (Current)
Execute dust_sweeper.js every 6 hours to:
1. Scan both Binance.US accounts
2. Identify dust positions (<$5 USD, >$2 USD)
3. Calculate USD values using live prices
4. Log proposed trades
5. **Simulation mode for 7 days, then LIVE**

### Phase 2: DCA on Dips (Pending)
After Phase 1 proven (2026-03-13), enable:
1. BTC price monitoring every 1 hour
2. Buy $5 USDC worth on 5%+ daily drops
3. 48h cooldown between purchases
4. Max $50/month

---

## Execution Schedule

```
0 */6 * * * /usr/bin/node /root/.openclaw/workspace/agent_sandboxes/the-great-cryptonio/workspace/dust_sweeper.js
```

**Runs at:** 00:00, 06:00, 12:00, 18:00 UTC

---

## Deliverables

1. **Daily Log** → `/memory/trading/YYYY-MM-DD.log`
2. **Daily Digest** → Console output summarizing activity
3. **Weekly Report** → Captain notification with portfolio delta

---

## Success Metrics

- [ ] All dust positions identified within 48h
- [ ] $20+ USDC recovered from dust (Phase 1)
- [ ] 3+ successful test trades (simulation)
- [ ] Portfolio value maintained or increased
- [ ] Full automation approved by Captain

---

## Risk Alerts

Trigger immediate halt if:
- Any core position (BTC, LTC, BCH) is threatened
- Portfolio drops >10% in 24h
- 3+ consecutive trade failures
- Unauthorized trade attempt

**HALT COMMAND:** "CRYPTONIO HALT"

---

💎🎰 *The Great Cryptonio — Trading Operation Alpha*
