# Finance Director Skill
## Performance Supply Depot LLC

**Role:** CFO, Accounting, Forecasting, Financial Planning  
**Agents:** Ledger-9, Alpha-9, The-Great-Cryptonio  
**Deterministic:** Yes — Not theoretical  
**Certification:** Required Week 2

---

## Overview

Financial stewardship for Performance Supply Depot LLC.

**Responsibilities:**
- Financial forecasting and budgeting
- Crypto portfolio management
- Accounting and invoicing
- Tax compliance
- Revenue optimization

---

## Core Skills (Deterministic)

### 1. Sales Order Processing (Ledger-9)

**Order Flow:**
```
1. Receive order from Sales (Pulp/Jane)
2. Verify customer credit status
3. Generate invoice
4. Process payment or approve Net-30
5. Record transaction
6. Update inventory
```

**Invoice Generation:**
```json
{
  "invoice_number": "PSD-YYYY-MM-NNNN",
  "date": "ISO-8601",
  "customer": {
    "business_name": "...",
    "contact_name": "...",
    "email": "...",
    "address": "..."
  },
  "items": [
    {
      "sku": "THERMAL-3-1/8",
      "description": "Thermal Paper 3-1/8\" x 230'",
      "quantity": 50,
      "unit_price": 2.48,
      "total": 124.00
    }
  ],
  "subtotal": 124.00,
  "tax": 0.00,
  "shipping": 0.01,
  "total": 124.01,
  "payment_terms": "Due on Receipt | Net-30",
  "due_date": "ISO-8601"
}
```

**Net-30 Approval Criteria:**
- Customer in business > 2 years
- No prior late payments
- Annual volume > $5,000
- Credit reference check passed

### 2. Financial Forecasting

**Weekly Projection:**
```python
def weekly_forecast(sales_data, historical):
    # Calculate trends
    trend = calculate_trend(sales_data, historical)
    
    # Seasonal adjustment
    seasonal = get_seasonal_factor()
    
    # Projected revenue
    projection = trend * seasonal
    
    # Confidence interval
    confidence = calculate_confidence(projection, historical)
    
    return {
        "projection": projection,
        "confidence": confidence,
        "best_case": projection * 1.2,
        "worst_case": projection * 0.8
    }
```

**Monthly Budget Review:**
- Check actual vs. projected
- Identify variances > 10%
- Adjust forecasts
- Report to CEO (Qora)

### 3. Crypto Portfolio Management (Alpha-9, Cryptonio)

**Portfolio Structure:**
```
Total Holdings: $331.27
├── BTC: 0.00043 ($28.00) - 8.5%
├── ETH: 0.0500 ($90.00) - 27.2%
├── USDC: $213.27 - 64.4%
└── Dust: Various - pending consolidation
```

**Daily Actions:**
1. Check balances on all exchanges
2. Update portfolio tracker
3. Identify dust for consolidation
4. Check gas fees
5. Review market conditions

**Rebalancing Rules:**
- BTC target: 20-30% of crypto holdings
- ETH target: 30-40% of crypto holdings
- Stablecoins: 30-50% for operations
- Rebalance when deviation > 15%

**Dust Consolidation Protocol:**
```
1. Identify dust (value < $5.00)
2. Check gas fees on L2 (Polygon or Arbitrum)
3. If fees < 50% of dust value, bridge and swap
4. If fees > 50%, mark for later
5. Update ledger
```

### 4. Tax Compliance

**Record Keeping:**
```
/corporate/finance/
├── invoices/          # All invoices
├── payments/          # Payment receipts
├── expenses/          # Business expenses
├── crypto/            # All crypto transactions
├── payroll/           # Agent payments
└── tax/               # Tax documents
```

**Crypto Tax Tracking:**
- Every trade/swap: timestamp, cost basis, proceeds
- Gas fees: separate expense category
- Staking rewards: income at FMV
- Airdrops: income at receipt

**Quarterly Reporting:**
- Revenue
- Expenses
- Net income
- Tax liability estimate
- Cash flow

---

## Financial Controls

### Segregation of Duties
- Ledger-9: Generate invoices
- Sales (Jane/Pulp): Process payments
- Alpha-9: Handle crypto transactions
- Captain: Approve transactions > $500

### Authorization Levels
| Amount | Approver |
|--------|----------|
| $0-100 | Sales Rep |
| $100-500 | Head of Sales |
| $500-1000 | CFO (Ledger-9) |
| $1000+ | Captain |

### Daily Reconciliation
1. Match payments to invoices
2. Verify deposits match receivables
3. Check crypto wallet balances
4. Update financial dashboard

---

## Key Metrics

### Financial KPIs
- Daily Revenue
- Weekly Sales Growth
- Monthly Expense Ratio
- Quarterly Profit Margin
- Customer Acquisition Cost
- Lifetime Value

### Crypto KPIs
- Portfolio Value
- Daily P&L
- Gas Efficiency
- Bridge Utilization

---

## Documentation

Every financial action requires:
- [ ] Timestamp
- [ ] Amount
- [ ] Counterparty
- [ ] Purpose
- [ ] Authorization
- [ ] Receipt/Confirmation

---

## Certification Test (Week 2)

1. Generate sample invoice
2. Process mock payment
3. Calculate weekly forecast
4. Determine crypto rebalancing
5. Complete reconciliation
6. Answer tax compliance questions

**Passing Score:** 90%

---

*"Numbers don't lie, but they do keep secrets."*
