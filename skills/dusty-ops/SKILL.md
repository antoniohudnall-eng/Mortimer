---
name: dusty-ops
description: Production operations for Dusty crypto wallet. Covers deployment, monitoring, the 10% revenue model, employee/agent management, and integration with Performance Supply Depot LLC business operations.
---

# Dusty Operations Skill

Manage Dusty in production — from deployment to revenue tracking to team coordination.

## Business Model Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Performance Supply Depot LLC              │
│                         (Parent/Cash Cow)                    │
└──────────────────┬──────────────────────────────────────────┘
                   │ Funds VPS & Operations
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                         Dusty                                │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐  │
│  │   Employees  │────▶│ Free Wallets │────▶│   10% Fee   │  │
│  │  (Internal)  │     │   + Tools    │     │   (If dust  │  │
│  └──────────────┘     └──────────────┘     │  collected) │  │
│                                              └──────┬──────┘  │
│                                                     │         │
└─────────────────────────────────────────────────────┼─────────┘
                                                    ▼
                                            ┌──────────────┐
                                            │   Revenue    │
                                            │   Bucket     │
                                            └──────────────┘
```

## Revenue Model: The 10% Rule

**Structure:**
- Employees/Agents get free Dusty wallets
- If Dusty helps them consolidate dust → they pay 10% to cover costs
- If they earn nothing → they pay nothing
- No recruiting fees, no multi-level nonsense

**Implementation:**
```javascript
// Example revenue sharing calculation
function calculateRevenueShare(dustValueUSD) {
  const platformFee = dustValueUSD * 0.10;  // 10% to Dusty
  const agentKeeps = dustValueUSD * 0.90;   // 90% to user
  
  return {
    grossDust: dustValueUSD,
    platformFee: platformFee,
    netToAgent: agentKeeps,
    timestamp: new Date().toISOString()
  };
}
```

**Tracking:**
- Log all dust consolidations
- Calculate 10% fee in USD at time of conversion
- Auto-deduct or invoice monthly
- Transparent dashboard showing: dust collected, fees due, total earned

## Employee Management

### Onboarding Checklist

```bash
# For each new employee/agent
1. Create Dusty wallet
2. Add to internal tracking sheet
3. Grant access to exchanges (if needed)
4. Set up API keys (securely)
5. Document in employee agreements:
   - Free wallet benefit
   - 10% fee on dust consolidated
   - Confidentiality around user data
```

### Offboarding

```bash
# When employee leaves
1. Revoke exchange API keys
2. Archive wallet (don't delete - they own keys)
3. Export transaction history
4. Calculate any remaining fees owed
5. Remove from active monitoring
```

## Production Deployment

### Environment Setup

```bash
# Production prerequisites
export NODE_ENV=production
export DUSTY_DB_PATH=/var/lib/dusty/db.sqlite
export DUSTY_LOG_LEVEL=info
export DUSTY_FEE_PERCENT=10

# VPS requirements
RAM: 2GB minimum, 4GB recommended
Disk: 20GB+ (for logs and DB)
Network: Stable, low-latency to exchange APIs
```

### Deployment Checklist

```bash
# Pre-deploy
[ ] All tests passing
[ ] Security audit complete
[ ] Backup strategy tested
[ ] Monitoring configured
[ ] Rollback plan ready

# Deploy
[ ] Stop services gracefully
[ ] Backup database
[ ] Deploy new code
[ ] Run migrations
[ ] Start services
[ ] Health checks pass
[ ] Monitor for 30 minutes
```

### Monitoring & Alerting

**Key Metrics:**
- Exchange API up/down status
- Dust consolidations per hour/day
- Revenue generated (10% fees)
- Error rates
- VPS resource usage

**Alerts:**
```yaml
Critical:
  - Exchange API down > 5 minutes
  - VPS CPU > 90% for 10 minutes
  - Database errors
  - Failed dust consolidations

Warning:
  - API latency > 5 seconds
  - Disk usage > 80%
  - Unusual transaction patterns
```

## Integration with Performance Supply Depot

### Financial Flow

```
Performance Supply Depot (Square) Revenue
                    │
                    ▼
            Business Account
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
   Operating Costs           VPS Payment (Dusty)
   (Inventory, etc)              │
                        ┌───────┴───────┐
                        ▼               ▼
                   Infrastructure    Emergency Fund
                   (2 years paid)    (6 months runway)
```

### Cross-Promotion

**Opportunities:**
- Depot customers get Dusty wallet discount (if public)
- Dusty users get Depot coupon
- Shared branding/loyalty program

## Operational Commands

```bash
# Check Dusty status
dusty status

# View revenue dashboard
dusty revenue --period=month

# List all employee wallets
dusty agents --list

# Check exchange health
dusty exchanges health

# Backup database
dusty backup --destination=s3://dusty-backups

# Rotate API keys (security)
dusty rotate-keys --agent=<employee_id>

# View logs
dusty logs --tail --service=core-agent

# Emergency stop
dusty emergency-stop
```

## Security Operations

**Daily:**
- Review failed authentications
- Check for unusual API activity

**Weekly:**
- Rotate API keys (if high-value targets)
- Review access logs
- Verify backup integrity

**Monthly:**
- Security scan of VPS
- Employee access audit
- Update dependencies

**Incident Response:**
```
1. Identify breach scope
2. Revoke compromised credentials
3. Isolate affected systems
4. Notify affected agents/employees
5. Document everything
6. Post-mortem and fixes
7. Legal review (if user funds involved)
```

## Scaling Considerations

**When to Scale:**
- > 1000 daily active agents
- > $10K monthly dust volume
- API rate limits hit consistently

**Scaling Options:**
1. Vertical: Upgrade VPS
2. Horizontal: Multiple VPS behind load balancer
3. Exchange API: Enterprise tier for higher limits

## Success Metrics

**Track These:**
```json
{
  "agents": {
    "total": 0,
    "active_30d": 0,
    "new_this_month": 0
  },
  "dust_consolidated": {
    "monthly_usd": 0,
    "all_time_usd": 0,
    "top_exchanges": {}
  },
  "revenue": {
    "10_percent_fees_usd": 0,
    "projected_annual": 0,
    "collection_rate": 0
  },
  "system": {
    "uptime_percent": 99.9,
    "api_latency_ms": 0,
    "error_rate": 0
  }
}
```

## Troubleshooting

**Exchange API Failures:**
```bash
# Test each exchange
curl -X GET "https://api.binance.com/api/v3/ping"
curl -X GET "https://api.kucoin.com/api/v1/timestamp"

# Check Dusty's exchange health
dusty exchanges health --verbose
```

**Database Issues:**
```bash
# Check integrity
sqlite3 $DUSTY_DB_PATH "PRAGMA integrity_check;"

# Vacuum for performance
sqlite3 $DUSTY_DB_PATH "VACUUM;"

# Backup before repair
cp $DUSTY_DB_PATH $DUSTY_DB_PATH.bak.$(date +%Y%m%d)
```

**VPS Full Disk:**
```bash
# Clean logs
find /var/log -name "*.log.*" -mtime +7 -delete

# Clean old backups
find /backup -name "*.tar.gz" -mtime +30 -delete

# Check Dusty logs
journalctl --vacuum-time=7d
```

## Emergency Contacts

**Escalation Path:**
1. Check dusty-status dashboard
2. Review #ops Slack/Discord channel
3. Contact VPS provider support
4. Contact exchange API support
5. Legal counsel (if user funds at risk)
6. Business owner (you)

## Quarterly Reviews

**Every 3 months:**
- [ ] Review 10% fee structure (still fair?)
- [ ] Audit agent access levels
- [ ] Review exchange integrations
- [ ] Update runbooks based on incidents
- [ ] Plan for next quarter scaling needs
- [ ] Review compliance status for expansion
