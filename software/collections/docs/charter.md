# Performance Supply Depot
## Collections Department Charter

**Effective Date:** June 12, 2026  
**Version:** 1.0.0  
**Approved By:** Captain

---

## Mission Statement

To recover outstanding debts efficiently while maintaining positive customer relationships and ensuring full compliance with all applicable laws and regulations.

---

## Department Overview

The Collections Department is responsible for:
- Recovering past-due accounts across all PSD services
- Managing payment plans and arrangements
- Escalating accounts to legal when necessary
- Maintaining customer relationships during collection process
- Ensuring FDCPA, TCPA, and state compliance

---

## Organization Structure

```
Head of Collections
├── Collections Managers (2)
│   ├── Collections Specialists (4)
│   └── Payment Plan Coordinators (2)
├── Legal Escalation Team (1)
└── Compliance Officer (1)
```

### Roles & Responsibilities

**Head of Collections**
- Strategic oversight of recovery operations
- P&L responsibility for collections
- Vendor management (collection agencies, law firms)
- Executive reporting

**Collections Managers**
- Daily operations oversight
- Team performance management
- Dispute resolution
- Customer escalations

**Collections Specialists**
- Account review and prioritization
- Customer contact (email, phone)
- Payment plan negotiation
- Documentation

**Payment Plan Coordinators**
- Plan setup and monitoring
- Failed payment follow-up
- Plan modifications
- Reporting

**Legal Escalation Team**
- Pre-litigation preparation
- Attorney coordination
- Judgment tracking
- Asset investigation

**Compliance Officer**
- FDCPA/TCPA compliance
- Training and audits
- Complaint handling
- Policy maintenance

---

## Service Levels

| Tier | Max Accounts | Response Time | Channels | Pricing |
|------|--------------|---------------|----------|---------|
| Starter | 500 | 72 hours | Email, SMS | $499/mo |
| Professional | 2,000 | 48 hours | + Voice | $999/mo |
| Corporate | Unlimited | 24 hours | + Mail | $3,999/mo |
| Enterprise | Unlimited | 12 hours | + API | Custom |

---

## Recovery Methodology

### Phase 1: Early Stage (0-30 days)
- **Tone:** Friendly, helpful
- **Goal:** Quick resolution, preserve relationship
- **Actions:** Email reminders, SMS nudges, phone calls
- **Success Rate Target:** 65%

### Phase 2: Mid Stage (31-60 days)
- **Tone:** Firm, professional
- **Goal:** Payment or payment plan commitment
- **Actions:** Demand letters, direct phone outreach
- **Success Rate Target:** 45%

### Phase 3: Late Stage (60+ days)
- **Tone:** Serious, formal
- **Goal:** Recovery or legal escalation
- **Actions:** Legal notices, collection agency, litigation
- **Success Rate Target:** 25%

---

## Key Performance Indicators (KPIs)

### Primary Metrics

| KPI | Target | Measurement |
|-----|--------|-------------|
| Recovery Rate | 65%+ | % of accounts recovered |
| Average Days to Collect | 30 days | From placement to payment |
| Cost per Dollar Collected | < $0.15 | Total cost / amount recovered |
| Customer Satisfaction | 3.5/5+ | Post-resolution survey |

### Operational Metrics

| KPI | Target | Measurement |
|-----|--------|-------------|
| SLA Compliance | 95%+ | Response within SLA |
| Contact Success Rate | 40%+ | % of attempts reaching debtor |
| Payment Plan Completion | 75%+ | % of plans completed |
| Dispute Resolution Time | 5 days | Average time to resolve |

### Compliance Metrics

| KPI | Target | Measurement |
|-----|--------|-------------|
| FDCPA Complaints | 0 | Number of violations |
| TCPA Compliance | 100% | Opt-out rate |
| Documentation | 100% | % of contacts documented |

---

## Compliance Framework

### Fair Debt Collection Practices Act (FDCPA)

**Prohibited Actions:**
- Harassment or abuse
- False or misleading representations
- Unfair practices
- Contacting at unreasonable times (before 8am, after 9pm)
- Contacting after written cease request

**Required Actions:**
- Validation notice within 5 days
- Debtor rights disclosure
- Accurate debt amount
- Firm identification

### Telephone Consumer Protection Act (TCPA)

**Requirements:**
- Prior express consent for SMS
- Opt-out mechanism
- Do Not Call compliance
- Written consent for autodialed calls

### State Regulations

**California:**
- Rosenthal Fair Debt Collection Practices Act
- Additional notification requirements
- Stricter timing rules

**New York:**
- Additional disclosure requirements
- Exempt income protections
- Specific validation requirements

---

## Dispute Handling

### Process

1. **Receive Dispute** (Day 0)
   - Document dispute reason
   - Suspend collection activity
   - Acknowledge receipt within 24 hours

2. **Investigation** (Days 1-5)
   - Verify debt validity
   - Review account history
   - Check documentation

3. **Resolution** (Day 5-10)
   - If valid: Resume collection
   - If invalid: Cancel debt, notify customer
   - If partial: Adjust balance, notify

4. **Follow-up**
   - Document resolution
   - Update customer
   - Close dispute ticket

### Dispute Types

| Type | Response | Action |
|------|----------|--------|
| Not my debt | Verify identity | Cease if confirmed |
| Already paid | Check records | Update if verified |
| Wrong amount | Recalculate | Adjust if needed |
| Bankruptcy | Verify filing | Cease immediately |
| Identity theft | Report to fraud | Law enforcement |

---

## Tools & Technology

### Core Platform
- Collections Module v1.0
- PostgreSQL database
- Redis caching layer
- REST API

### Communication
- SendGrid (email)
- Twilio (SMS/voice)
- Lob (mail)

### Payment Processing
- Stripe (credit/debit)
- ACH processing
- Check scanning

### Reporting
- Grafana dashboards
- Custom reports
- Executive dashboards

---

## Training Program

### Onboarding (Week 1)
- FDCPA/TCPA compliance
- System training
- Script practice
- Shadow experienced agents

### Ongoing Training
- Monthly compliance updates
- Quarterly role-plays
- Annual certification
- Industry seminars

### Certifications Required
- FDCPA compliance certification
- TCPA compliance certification
- Company product knowledge
- Customer service excellence

---

## Escalation Matrix

### Internal Escalations

| Level | Trigger | Handler | Timeline |
|-------|---------|---------|----------|
| 1 | Customer requests manager | Collections Specialist + Manager | Same day |
| 2 | Payment plan > $10K | Collections Manager | 24 hours |
| 3 | Legal threat received | Compliance Officer + Legal | 4 hours |
| 4 | Media/PR inquiry | Head of Collections | 2 hours |

### External Escalations

| Stage | Criteria | Action | Timing |
|-------|----------|--------|--------|
| Collection Agency | 90+ days, no response | Forward to agency | Weekly batch |
| Legal | 120+ days, asset found | Attorney referral | As needed |
| Litigation | Judgment obtained | Court filing | Per attorney |
| Asset Recovery | Judgment issued | Garnishment/liens | Per attorney |

---

## Reporting Structure

### Daily Reports
- Accounts worked
- Payments received
- New placements
- Failed payments

### Weekly Reports
- Recovery rates by tier
- SLA compliance
- Dispute summary
- Team performance

### Monthly Reports
- Executive dashboard
- Financial performance
- Compliance audit
- Customer satisfaction

### Quarterly Reports
- Strategic review
- Vendor performance
- Technology roadmap
- Budget review

---

## Budget

### Revenue Model

| Source | Monthly | Annual |
|--------|---------|--------|
| Service Fees | $50,000+ | $600,000+ |
| Commission (10%) | $25,000+ | $300,000+ |
| **Total** | **$75,000+** | **$900,000+** |

### Operating Costs

| Category | Monthly | % of Revenue |
|----------|---------|--------------|
| Salaries | $35,000 | 47% |
| Technology | $5,000 | 7% |
| Vendors | $8,000 | 11% |
| Legal | $3,000 | 4% |
| Overhead | $4,000 | 5% |
| **Total** | **$55,000** | **73%** |

**Net Margin:** 27%

---

## Continuous Improvement

### Quarterly Reviews
- KPI performance vs targets
- Process efficiency
- Technology updates
- Staff feedback

### Annual Planning
- Strategic objectives
- Budget allocation
- Technology roadmap
- Training plan

### Innovation
- AI/ML enhancements
- New channel testing
- Process automation
- Customer experience improvements

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-12 | Collections Team | Initial charter |

**Next Review:** 2026-09-12

---

## Approval

This charter is approved by:

_________________________  
Captain  
Commander, AGI Company  
Date: ___________

---

*© 2026 Performance Supply Depot LLC*
