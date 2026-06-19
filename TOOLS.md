# 🔐 CONFIRMED CREDENTIALS LOCATION
## Performance Supply Depot LLC — Secure Vault Reference

**CRITICAL: These keys EXIST and are ACTIVE. Stop asking for them.**

**Rule:** ALWAYS check these locations BEFORE asking Captain for credentials.

---

## 📋 ACTIVE CREDENTIALS

| Credential | Location | Status | Purpose |
|------------|----------|--------|---------|
| **Telegram Bot** | `config/.private/telegram_credentials.env` | 🟢 ACTIVE | Telegram Bot API |
| **Hostinger API Key 1** | `armory/vault/HOSTINGER_API_KEY.txt` | 🟢 ACTIVE | VPS/DNS Management |
| **Hostinger API Key 2** | `armory/vault/HOSTINGER_API_KEY_SECOND.txt` | 🟢 ACTIVE | Backup/Secondary |
| **Binance.US (1)** | `secrets/binance_us.env` | 🟢 EXISTS | Exchange API |
| **Binance.US (2)** | `secrets/binance_us_second.env` | 🟢 EXISTS | Exchange API (dual) |

---

## 🖥️ HOSTS KNOWN

| Host | IP | VPS ID | Status |
|------|-----|--------|--------|
| **Miles.cloud** | 31.97.6.40 | 1334753 | 🟢 RUNNING |
| **Mortimer.cloud** | 31.97.6.30 | 1334755 | 🟢 RUNNING |

**Specs:** KVM 2 (2 vCPU, 8GB RAM, 100GB), Ubuntu 24.04, Data Center 17

---

## 🌐 DNS STATUS

| Domain | Current IP | Managed By | Status |
|--------|-----------|------------|--------|
| **tappylewis.cloud** | 2.57.91.91 | External | ✅ CORRECT |
| **psdepot.com** | 31.97.6.40 | Miles | ✅ CORRECT (Miles managing) |
| **amhudsupply.com** | 31.97.6.30 | Mortimer | ✅ CORRECT |

---

## 📧 CONTACT

**My Email:** mortimer@myl0nr0s.cloud  
**Domain:** myl0nr0s.cloud  
**Server:** Mortimer.cloud (31.97.6.30)

## 💬 CAPTAIN'S CHAT ID
**Telegram:** 1611228942

## ⏱️ TEMPORAL (Durable Workflows)
**Server:** mortimer.cloud:7233  
**UI:** http://mortimer.cloud:8233

| Queue | Purpose |
|-------|---------|
| portfolio-queue | Portfolio reports |
| sweep-queue | Dust consolidation |
| briefing-queue | Daily briefings |
| task-queue | General/test workflows |

**Available Workflows:**
- `PortfolioReportWorkflow`
- `DustySweepWorkflow`
- `DailyBriefingWorkflow`

**Usage:**
```bash
temporal workflow start --task-queue portfolio-queue --type PortfolioReportWorkflow --workflow-id my-report
```

**CLI wrapper:** `temporal-run <queue> <workflow_type> [id]`

## 💾 DISK STATUS
| Location | Size | Notes |
|----------|------|-------|
| Root | 93G/96G (97%) | 3.4G free — needs monitoring |
| aoscros_brain/ | 321M | Brain data |
| node_modules/ | 151M | npm packages |
| projects/ | 139M | Project files |
| skills/ | 90M | Skills repo |
| dusty/ | 86M | Dusty wallet |

**Cleanup done:** Purged /var/crash (397M freed)

---

**Last Updated:** 2026-02-28 18:03 UTC  
**Location:** `/root/.openclaw/workspace/TOOLS.md`
