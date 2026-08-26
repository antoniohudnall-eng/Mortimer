# Jarvis Audit Report — 2026-08-25

Generated: 2026-08-25 22:13
Inputs: master-schedule + startup-cadence (71 tasks)

## Summary
- Total recurring tasks: **71**
- Deterministic (workflow): **42**
- Needs AI (agent): **29**
- Can fire without you: **60**
- Needs you as trigger (session lifecycle): **11**

## Candidate Table

| Task | Trigger | Freq | Owner | Auto? | Needs AI? | Type | Suggested metric | First step |
|------|---------|------|-------|-------|-----------|------|------------------|------------|
| Sync Pull — get latest from GitHub | On wake | daily | Startup Cadence | yes | no | workflow | sync succeeds 100% | cron / temporal-brain script |
| Status Probe — memory, disk, battery, versions | On wake | daily | Startup Cadence | yes | no | workflow | memory file created daily | cron / temporal-brain script |
| API Inventory — OpenRouter, DeepSeek, keys | On wake | daily | Startup Cadence | yes | no | workflow | define one metric before building | cron / temporal-brain script |
| VPS Inventory — what's running on hermes/aosbrain | On wake | daily | Startup Cadence | yes | no | workflow | define one metric before building | cron / temporal-brain script |
| Local Models — disk usage, what's available | On wake | daily | Startup Cadence | yes | no | workflow | define one metric before building | cron / temporal-brain script |
| Memory File — create today's YYYY-MM-DD.md | On wake | daily | Startup Cadence | yes | no | workflow | memory file created daily | cron / temporal-brain script |
| Skill Router — load first, then domain skills | On wake | daily | Skill Router | yes | no | workflow | define one metric before building | cron / temporal-brain script |
| X/Twitter post — industry commentary or quick tip | 08:00 PST | daily | X Content Creator | yes | yes | agent | posts shipped/week | agent + shadow mode (approve first) |
| DepotChaos check — new leads, follow-ups due today | 09:00 PST | daily | DepotChaos | yes | no | workflow | leads processed/week | cron / temporal-brain script |
| Instagram post — product photo or Tip Tuesday (Tue) | 10:00 PST | daily | Instagram Creator | yes | yes | agent | posts shipped/week | agent + shadow mode (approve first) |
| X engagement — reply to CA restaurants, join conversations | 14:00 PST | daily | X Content Creator | yes | yes | agent | define one metric before building | agent + shadow mode (approve first) |
| Shopify check — low stock alerts, abandoned carts | 16:00 PST | daily | Shopify Manager | yes | no | workflow | stock alerts actioned within 24h | cron / temporal-brain script |
| Memory update — append decisions, state changes to today's MD | Before sleep | daily | Startup Cadence | yes | no | workflow | memory file created daily | cron / temporal-brain script |
| Status Snapshot — final system probe | Before sleep | daily | Startup Cadence | yes | no | workflow | define one metric before building | cron / temporal-brain script |
| Sync Push — upload everything to GitHub | Before sleep | daily | Startup Cadence | yes | no | workflow | sync succeeds 100% | cron / temporal-brain script |
| Rule 11 Check — did everything get saved? | Before sleep | daily | Aave/Rule 11 | yes | no | workflow | define one metric before building | cron / temporal-brain script |
| Brain state persistence — save body_state.json (morty_body) | Every 10 cycles | daily | Morty Body | yes | no | workflow | define one metric before building | cron / temporal-brain script |
| Brain Viz state persistence — save viz_state.json | Every 10 polls | daily | Brain Viz | yes | no | workflow | define one metric before building | cron / temporal-brain script |
| Brain health check — tick latency, memory, ollama, skills | On wake | daily | Brain Health Check | yes | no | workflow | memory file created daily | cron / temporal-brain script |
| Brain Viz health — /health + /api/status on :8080 | On wake | daily | Brain Viz | yes | no | workflow | define one metric before building | cron / temporal-brain script |
| Brain priorities load — verify 14 core directives surfaced | On wake | daily | Morty Body | yes | no | workflow | define one metric before building | cron / temporal-brain script |
| PRE-FLIGHT — Are sync token, termux-api, ollama, git online? | session start | session | Startup Cadence | no | no | workflow | sync succeeds 100% | cron / temporal-brain script |
| SYNC PULL — Get latest state from GitHub BEFORE doing work | session start | session | Startup Cadence | no | no | workflow | sync succeeds 100% | cron / temporal-brain script |
| STATUS PROBE — Memory, disk, battery, versions snapshot | session start | session | Startup Cadence | no | no | workflow | memory file created daily | cron / temporal-brain script |
| API INVENTORY — Check OpenRouter, DeepSeek Pro, any new keys | session start | session | Startup Cadence | no | no | workflow | define one metric before building | cron / temporal-brain script |
| VPS INVENTORY — What models/skills/workflows are on the VPS? | session start | session | Startup Cadence | no | no | workflow | define one metric before building | cron / temporal-brain script |
| LOCAL MODELS — What's available locally? Disk usage? | session start | session | Startup Cadence | no | no | workflow | define one metric before building | cron / temporal-brain script |
| MEMORY FILE — Create today's MD if missing (YYYY-MM-DD.md) | session start | session | Startup Cadence | no | no | workflow | memory file created daily | cron / temporal-brain script |
| FINAL INVENTORY — Skills loaded, project files present | session start | session | Startup Cadence | no | no | workflow | define one metric before building | cron / temporal-brain script |
| UPDATE MEMORY — Append end time, decisions, state to today's MD | session end | session | Startup Cadence | no | no | workflow | memory file created daily | cron / temporal-brain script |
| STATUS SNAPSHOT — Final system probe | session end | session | Startup Cadence | no | no | workflow | define one metric before building | cron / temporal-brain script |
| SYNC PUSH — Upload everything to GitHub | session end | session | Startup Cadence | no | no | workflow | sync succeeds 100% | cron / temporal-brain script |
| Weekly Review — metrics, blockers, wins from last week | Monday | weekly | Cadence | yes | yes | agent | define one metric before building | agent + shadow mode (approve first) |
| Competitor Price Check — WebstaurantStore, Amazon thermal paper | Monday | weekly | Browser Automation (Playwright) | yes | yes | agent | competitors checked/week | agent + shadow mode (approve first) |
| Aave Position Check — health factor, yields, rebalance if needed | Monday | weekly | Aave | yes | no | workflow | alerts with 0 false positives | cron / temporal-brain script |
| Content Calendar — plan this week's posts across all channels | Monday | weekly | Buzz → PSD Brand Voice | yes | yes | agent | posts shipped/week | agent + shadow mode (approve first) |
| Tip Tuesday — Instagram carousel (POS/restaurant tip) | Tuesday | weekly | Instagram Creator | yes | yes | agent | define one metric before building | agent + shadow mode (approve first) |
| YouTube script — this week's tutorial or deep-dive | Tuesday | weekly | YouTube Creator | yes | yes | agent | define one metric before building | agent + shadow mode (approve first) |
| Vendor Spotlight — feature 1 of 11 approved vendors | Tuesday | weekly | TikTok + Instagram | yes | yes | agent | define one metric before building | agent + shadow mode (approve first) |
| CRM Deep Dive — tier leads, schedule callbacks, enrichment | Wednesday | weekly | DepotChaos | yes | yes | agent | leads processed/week | agent + shadow mode (approve first) |
| Email Campaign — draft/send weekly newsletter | Wednesday | weekly | Buzz → Email Sender | yes | yes | agent | emails sent/week | agent + shadow mode (approve first) |
| Shopify Audit — product listings, pricing, collections | Wednesday | weekly | Shopify Manager | yes | no | workflow | stock alerts actioned within 24h | cron / temporal-brain script |
| Lead Research — browser automation: research 10 prospects | Thursday | weekly | Browser Automation | yes | yes | agent | leads processed/week | agent + shadow mode (approve first) |
| Social engagement — reply to all pending across X/IG/TT | Thursday | weekly | X + Instagram + TikTok | yes | yes | agent | define one metric before building | agent + shadow mode (approve first) |
| VPS Health Check — hermes, aosbrain: disk, services, ports | Thursday | weekly | Monitor | yes | no | workflow | define one metric before building | cron / temporal-brain script |
| Weekly competitor report — prices, new products, moves | Friday | weekly | Browser Automation | yes | yes | agent | competitors checked/week | agent + shadow mode (approve first) |
| Weekend content queue — schedule Sat/Sun posts | Friday | weekly | All content creators | yes | yes | agent | posts shipped/week | agent + shadow mode (approve first) |
| Aave weekly rebalance — check yields, adjust positions | Friday | weekly | Aave | yes | no | workflow | positions reviewed on schedule | cron / temporal-brain script |
| Sync everything — final push before weekend | Friday | weekly | Startup Cadence | yes | no | workflow | sync succeeds 100% | cron / temporal-brain script |
| Aave quick check — health factor only (5 min) | Saturday | weekly | Aave | yes | no | workflow | alerts with 0 false positives | cron / temporal-brain script |
| X auto-post — pre-scheduled from Friday | Saturday | weekly | X Content Creator | yes | yes | agent | posts shipped/week | agent + shadow mode (approve first) |
| Week ahead plan — review next week's content calendar | Sunday | weekly | Cadence | yes | yes | agent | pieces shipped/week | agent + shadow mode (approve first) |
| Sync pull — get any changes from other devices | Sunday | weekly | Startup Cadence | yes | no | workflow | sync succeeds 100% | cron / temporal-brain script |
| Monthly Retro — what's working, what's not, what changes? | Week 1 | monthly | Cadence | yes | yes | agent | define one metric before building | agent + shadow mode (approve first) |
| Aave deep dive — cross-chain position review, governance proposals | Week 1 | monthly | Aave | yes | yes | agent | positions reviewed on schedule | agent + shadow mode (approve first) |
| DepotChaos cleanup — deduplicate leads, update tiers, archive old | Week 1 | monthly | DepotChaos | yes | yes | agent | leads processed/week | agent + shadow mode (approve first) |
| Content performance review — which posts performed? Adjust strategy | Week 2 | monthly | All creators + Buzz | yes | yes | agent | posts shipped/week | agent + shadow mode (approve first) |
| Vendor check — any new products from 11 approved vendors? | Week 2 | monthly | Shopify Manager | yes | yes | agent | define one metric before building | agent + shadow mode (approve first) |
| Competitor deep dive — full browser scrape of 3 competitors | Week 3 | monthly | Browser Automation | yes | yes | agent | competitors checked/week | agent + shadow mode (approve first) |
| Skill audit — any new skills? Any conflicts? Router still accurate? | Week 3 | monthly | Skill Router | yes | no | workflow | define one metric before building | cron / temporal-brain script |
| Financial review — PSD revenue, Aave yields, gas costs | Week 4 | monthly | Aave | yes | yes | agent | positions reviewed on schedule | agent + shadow mode (approve first) |
| Next month content calendar — plan all 4 weeks | Week 4 | monthly | Buzz + Brand Voice | yes | yes | agent | pieces shipped/week | agent + shadow mode (approve first) |
| Alert immediately, de-risk plan | Aave health factor < 1.5 | event | User (push notification) | yes | yes | agent | define one metric before building | agent + shadow mode (approve first) |
| EMERGENCY — repay or add collateral NOW | Aave health factor < 1.1 | event | User (call + push) | yes | no | workflow | define one metric before building | cron / temporal-brain script |
| Auto-recovery script, restart service | DepotChaos API down | event | User if 3 attempts fail | yes | yes | agent | define one metric before building | agent + shadow mode (approve first) |
| Check from Termux, try SSH, check Hetzner panel | VPS unreachable | event | User | yes | no | workflow | define one metric before building | cron / temporal-brain script |
| Check token, check network, manual git push | Sync push fails 3x | event | User | yes | no | workflow | define one metric before building | cron / temporal-brain script |
| Flag in weekly report, recommend response | Competitor price drop > 15% | event | User (in report) | yes | yes | agent | reports delivered on time | agent + shadow mode (approve first) |
| Alert in daily check, flag for reorder | Shopify low stock < 5 units | event | User (in daily pulse) | yes | no | workflow | define one metric before building | cron / temporal-brain script |
| Ping within 1 hour | Missed daily pulse (any agent) | event | User if 3 hours silent | yes | no | workflow | define one metric before building | cron / temporal-brain script |
| Flag in weekly review | 3 days without progress on any project | event | User | yes | yes | agent | define one metric before building | agent + shadow mode (approve first) |

## Top 3 'Vending Machine' Wins (ship first)

1. **Sync Pull — get latest from GitHub** — On wake, daily → simple script/cron, never fails.
2. **Status Probe — memory, disk, battery, versions** — On wake, daily → simple script/cron, never fails.
3. **API Inventory — OpenRouter, DeepSeek, keys** — On wake, daily → simple script/cron, never fails.

## Guardrails (apply before anything ships)
- [ ] Run in shadow mode first (log what it *would* do)
- [ ] Human approval for anything customer-facing or money-moving
- [ ] Failure alert — never fail silently
- [ ] Dry-run / revert for every automation
- [ ] Meter agent spend in QL via Paymaster

## Notes
- 'Needs AI?' is a keyword heuristic — review the column with human judgment (taste).
- Session-lifecycle tasks (startup/shutdown) are already partly automated by `startup-cadence`.
