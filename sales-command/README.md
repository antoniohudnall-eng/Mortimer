# 🤖 AGI Company Sales Command Center

**Built on SEED3 (Mortimer.cloud)**  
**Captain: Antonio Maurice Hudnall**

---

## 📊 What's Built

### 1. Command Center (`command_center.py`)
Unified sales pipeline tracking:
- 7,820 leads from AOS-Brain
- Agent sales tracking
- Lead attribution by source

### 2. TikTok Sales Tracker (`tiktok_sales.py`)
Video performance & conversion:
- Views, leads, sales per video
- Revenue calculation
- Conversion rates

### 3. Invoice Generator (`~/mortimer/sales-tools/invoice_generator.py`)
- Auto-generate invoices
- HTML format with crypto payment
- Tracks payment status

### 4. Pricing Catalog (`~/mortimer/sales-tools/pricing_catalog.py`)
6 agent tiers with pricing:
- CLERK ($97)
- GREET ($147)
- PERSONAL ($197)
- VELVET ($247)
- CONCIERGE ($297)
- EXECUTIVE ($497)

### 5. Lead Capture Webhook (`webhooks/tiktok_lead.py`)
- POST endpoint for TikTok leads
- Logs to database

---

## 🚀 Quick Start

```bash
# Show dashboard
python3 ~/mortimer/sales-command/command_center.py

# TikTok report
python3 ~/mortimer/sales-command/tiktok_sales.py

# Pricing catalog
python3 ~/mortimer/sales-tools/pricing_catalog.py

# Generate invoice
python3 ~/mortimer/sales-tools/invoice_generator.py
```

---

## 📁 File Structure

```
~/mortimer/
├── sales-command/
│   ├── command_center.py      # Main pipeline
│   ├── tiktok_sales.py        # TikTok tracking
│   ├── data/
│   │   ├── sales.db           # SQLite database
│   │   ├── leads_cache.json   # 7,820 leads
│   │   ├── videos.json        # Video stats
│   │   └── tiktok_leads.json  # TikTok leads
│   └── webhooks/
│       └── tiktok_lead.py     # Lead capture
└── sales-tools/
    ├── invoice_generator.py
    ├── pricing_catalog.py
    ├── sales_funnel.py
    └── invoices/              # Generated invoices
```

---

## 💰 Crypto Payment Address

**ETH/USDC:** `0x7244d8C20394CC11D54b2583Fb813B3EB8B72f36`

---

## 📈 Current Stats

| Metric | Value |
|--------|-------|
| Total Leads | 7,820 |
| TikTok Views | 49,600 |
| TikTok Leads | 84 |
| Agent Sales | 8 |
| Revenue | $1,376 |

---

**Built by Mortimer (C3) — SEED3**  
*Intelligence Engineered.*
