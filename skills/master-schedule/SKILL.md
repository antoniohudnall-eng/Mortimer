---
name: master-schedule
description: "Master operational schedule for the AIOS ecosystem — Mortimer Mobile, PSD marketing, Aave positions, CRM, competitor monitoring, and VPS health checks. Use for scheduling and rhythm questions."
---

# Master Schedule

> Category: execution — Task automation, command running, and process management

## Description

The master operational schedule for the entire AIOS ecosystem — Mortimer Mobile, PSD marketing, Aave positions, DepotChaos CRM, competitor monitoring, and VPS health checks. Every agent, every rhythm, one calendar.

## Instructions

# Master Schedule — AIOS Operational Calendar

This is the SINGLE source of truth for every recurring task across the AIOS ecosystem. Every agent, every skill, every check-in maps to a slot on this calendar.

**Principle**: If it's not on the schedule, it doesn't happen. If it's on the schedule, it happens or escalates.

---

## ⏰ DAILY RHYTHM

### Morning Startup (Session Start)
| Time | Task | Owner | Duration |
|------|------|-------|----------|
| **On wake** | Sync Pull — get latest from GitHub | Startup Cadence | 30s |
| **On wake** | Status Probe — memory, disk, battery, versions | Startup Cadence | 30s |
| **On wake** | API Inventory — OpenRouter, DeepSeek, keys | Startup Cadence | 30s |
| **On wake** | VPS Inventory — what's running on hermes/aosbrain | Startup Cadence | 1m |
| **On wake** | Local Models — disk usage, what's available | Startup Cadence | 30s |
| **On wake** | Memory File — create today's YYYY-MM-DD.md | Startup Cadence | 1m |
| **On wake** | Skill Router — load first, then domain skills | Skill Router | 10s |

### Marketing Pulse (Daily)
| Time | Task | Owner | Duration |
|------|------|------|----------|
| **08:00 PST** | X/Twitter post — industry commentary or quick tip | X Content Creator | 5m |
| **09:00 PST** | DepotChaos check — new leads, follow-ups due today | DepotChaos | 10m |
| **10:00 PST** | Instagram post — product photo or Tip Tuesday (Tue) | Instagram Creator | 10m |
| **12:00 PST** | TikTok — product demo or repair timelapse | TikTok Creator | 15m |
| **14:00 PST** | X engagement — reply to CA restaurants, join conversations | X Content Creator | 15m |
| **16:00 PST** | Shopify check — low stock alerts, abandoned carts | Shopify Manager | 10m |

### Evening Shutdown (Session End)
| Time | Task | Owner | Duration |
|------|------|------|----------|
| **Before sleep** | Memory update — append decisions, state changes to today's MD | Startup Cadence | 2m |
| **Before sleep** | Status Snapshot — final system probe | Startup Cadence | 30s |
| **Before sleep** | Sync Push — upload everything to GitHub | Startup Cadence | 30s |
| **Before sleep** | Rule 11 Check — did everything get saved? | Aave/Rule 11 | 10s |

---

## 📅 WEEKLY RHYTHM

### Monday — Planning & Setup
| Task | Owner | Duration |
|------|-------|----------|
| **Weekly Review** — metrics, blockers, wins from last week | Cadence | 20m |
| **Competitor Price Check** — WebstaurantStore, Amazon thermal paper | Browser Automation (Playwright) | 15m |
| **Aave Position Check** — health factor, yields, rebalance if needed | Aave | 15m |
| **Content Calendar** — plan this week's posts across all channels | Buzz → PSD Brand Voice | 20m |

### Tuesday — Content Day
| Task | Owner | Duration |
|------|-------|----------|
| **Tip Tuesday** — Instagram carousel (POS/restaurant tip) | Instagram Creator | 20m |
| **YouTube script** — this week's tutorial or deep-dive | YouTube Creator | 30m |
| **Vendor Spotlight** — feature 1 of 11 approved vendors | TikTok + Instagram | 20m |

### Wednesday — Operations
| Task | Owner | Duration |
|------|-------|----------|
| **CRM Deep Dive** — tier leads, schedule callbacks, enrichment | DepotChaos | 30m |
| **Email Campaign** — draft/send weekly newsletter | Buzz → Email Sender | 30m |
| **Shopify Audit** — product listings, pricing, collections | Shopify Manager | 20m |

### Thursday — Growth
| Task | Owner | Duration |
|------|-------|----------|
| **Lead Research** — browser automation: research 10 prospects | Browser Automation | 30m |
| **Social engagement** — reply to all pending across X/IG/TT | X + Instagram + TikTok | 30m |
| **VPS Health Check** — hermes, aosbrain: disk, services, ports | Monitor | 15m |

### Friday — Wrap & Prep
| Task | Owner | Duration |
|------|-------|----------|
| **Weekly competitor report** — prices, new products, moves | Browser Automation | 20m |
| **Weekend content queue** — schedule Sat/Sun posts | All content creators | 20m |
| **Aave weekly rebalance** — check yields, adjust positions | Aave | 15m |
| **Sync everything** — final push before weekend | Startup Cadence | 2m |

### Saturday — Light
| Task | Owner | Duration |
|------|-------|----------|
| **Aave quick check** — health factor only (5 min) | Aave | 5m |
| **X auto-post** — pre-scheduled from Friday | X Content Creator | 1m |

### Sunday — Prep
| Task | Owner | Duration |
|------|-------|----------|
| **Week ahead plan** — review next week's content calendar | Cadence | 15m |
| **Sync pull** — get any changes from other devices | Startup Cadence | 30s |

---

## 📆 MONTHLY RHYTHM

### Week 1
| Task | Owner | Duration |
|------|-------|----------|
| **Monthly Retro** — what's working, what's not, what changes? | Cadence | 30m |
| **Aave deep dive** — cross-chain position review, governance proposals | Aave | 30m |
| **DepotChaos cleanup** — deduplicate leads, update tiers, archive old | DepotChaos | 30m |

### Week 2
| Task | Owner | Duration |
|------|-------|----------|
| **Content performance review** — which posts performed? Adjust strategy | All creators + Buzz | 30m |
| **Vendor check** — any new products from 11 approved vendors? | Shopify Manager | 20m |

### Week 3
| Task | Owner | Duration |
|------|-------|----------|
| **Competitor deep dive** — full browser scrape of 3 competitors | Browser Automation | 45m |
| **Skill audit** — any new skills? Any conflicts? Router still accurate? | Skill Router | 15m |

### Week 4
| Task | Owner | Duration |
|------|-------|----------|
| **Financial review** — PSD revenue, Aave yields, gas costs | Aave | 20m |
| **Next month content calendar** — plan all 4 weeks | Buzz + Brand Voice | 30m |

---

## 🔴 ALERTS & ESCALATIONS

| Trigger | Action | Escalate To | Max Delay |
|---------|--------|-------------|-----------|
| **Aave health factor < 1.5** | Alert immediately, de-risk plan | User (push notification) | 5 minutes |
| **Aave health factor < 1.1** | EMERGENCY — repay or add collateral NOW | User (call + push) | 1 minute |
| **DepotChaos API down** | Auto-recovery script, restart service | User if 3 attempts fail | 15 minutes |
| **VPS unreachable** | Check from Termux, try SSH, check Hetzner panel | User | 30 minutes |
| **Sync push fails 3x** | Check token, check network, manual git push | User | 1 hour |
| **Competitor price drop > 15%** | Flag in weekly report, recommend response | User (in report) | 24 hours |
| **Shopify low stock < 5 units** | Alert in daily check, flag for reorder | User (in daily pulse) | 24 hours |
| **Missed daily pulse (any agent)** | Ping within 1 hour | User if 3 hours silent | 3 hours |
| **3 days without progress on any project** | Flag in weekly review | User | 7 days |
| **Blocker > 48 hours unresolved** | Escalate with context | User | 48 hours |

---

## 🛡️ RULE 11: SAVE OR DIE

Every task above that changes state MUST be followed by a sync. Specifically:

- **After every Aave check** → sync push
- **After every content post** → sync push
- **After every CRM update** → sync push
- **After every session** → sync push (startup cadence handles this)
- **Minimum**: 2 sync pushes per day (morning + evening)

If a sync fails, the task is NOT complete. Retry or escalate.

---

## 📋 QUICK REFERENCE (Today's View)

Ask "what's on the schedule today?" to get:

```
## Today: [Day], [Date]

### ☀️ Morning
- [ ] Sync Pull + Status Probe
- [ ] Memory file: YYYY-MM-DD.md
- [ ] X post (08:00 PST)

### 🌤 Midday
- [ ] DepotChaos check (09:00)
- [ ] Instagram post (10:00)
- [ ] TikTok (12:00)

### 🌙 Evening
- [ ] X engagement (14:00)
- [ ] Shopify check (16:00)
- [ ] Memory update + Sync Push

### ⚠ Alerts
- [any triggered alerts]
```

---

## USAGE

Load this skill after Startup Cadence and Skill Router. It defines WHEN everything else runs. Every agent and skill references this schedule.

To check: "what's on the schedule?" / "what's due today?" / "show me the calendar"
To update: "reschedule [task] to [time/day]" — updates this file


## Usage

Load this skill when the task involves the master operational schedule for the entire aios ecosystem — mortimer mobile, psd marketing, aave positions, depotchaos crm, competitor monitoring, and vps health checks. every agent, every rhythm, one calendar..

---
*Generated by Skill Factory — 2026-08-09T18:47:13.198Z*
