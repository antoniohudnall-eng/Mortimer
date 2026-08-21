---
name: jarvis-audit
description: "Audit recurring tasks and predictable triggers to find automation candidates, then classify each as a deterministic workflow vs an AI agent. Runs an executable audit over master-schedule and startup-cadence. Use to build systems that run without you."
---

# Jarvis Audit

> Category: execution — Task automation, command running, and process management

## What It Is

A repeatable, **executable** audit that reads your canonical task list, classifies every task, and produces a persisted candidate report. Goal: turn your day into systems that run **without you as the trigger**.

## Run It

```bash
python3 ~/.pi/agent/skills/jarvis-audit/audit.py             # full audit -> research/jarvis-audit-report-YYYY-MM-DD.md
python3 ~/.pi/agent/skills/jarvis-audit/audit.py --dry-run   # print only
python3 ~/.pi/agent/skills/jarvis-audit/audit.py --meter     # also record 25 QL to jarvis-audit in the ledger
python3 ~/.pi/agent/skills/jarvis-audit/audit.py --no-memory # skip appending a note to today's memory file
```

**Inputs (read automatically):**
- `~/.pi/agent/skills/master-schedule/SKILL.md` — daily/weekly/monthly rhythms + alerts
- `~/.pi/agent/skills/startup-cadence/SKILL.md` — session start/shutdown steps

**Output:** `~/downloads/mortimer-v1/research/jarvis-audit-report-YYYY-MM-DD.md` — candidate table, top-3 vending-machine wins, guardrails. Also appends a note to today's memory file.

## The Core Rule

> **Vending machine vs. slot machine.**
> - Deterministic task (same input → same output) → **workflow/script** — cheap, never breaks.
> - Needs reasoning/content (messy input) → **AI agent** — powerful, but costly, can fail, adds risk.
>
> **Default to the simplest thing that works.**

## The Two Questions (per task)

1. **Do I need to be the one triggering this?** Or can the system fire on its own?
2. **Does this actually need AI?** Or would a Python script / no-code workflow do it cheaper and safer?

Both "no" → workflow. Second is "yes" → agent + guardrails.

## Classification Table

| Type | Use when | Tool in stack |
|------|----------|----------------|
| Workflow (deterministic) | same input → same output | cron, `master-schedule`, `temporal-brain`, shell/Python script |
| Agent (reasoning) | messy input, judgment, generated content | `browser-automation`, `verify`, `buzz`, content-creator skills; meter via `paymaster` |

## Define "Done" (one metric per automation)

Pick ONE metric before building, so you know when to stop:
- Support → tickets resolved/day · Sales → meetings/week · Ops → refund % down X% · Content → posts/week · Monitoring → zero false-positive alerts.
Hit it → **maintenance mode**. Don't keep adding features.

## Guardrails (because you're out of the loop)

- [ ] **Shadow mode first** — log what it *would* do, don't act.
- [ ] **Human approval** for anything customer-facing or money-moving.
- [ ] **Failure alert** — never fail silently.
- [ ] **Dry-run / revert** for every automation.
- [ ] **Meter it** — charge agent work in QL via Paymaster.

## Worked Examples (from the actual stack)

1. **Aave health factor watch** — trigger every 6h; needs AI? No → cron + RPC + notify. Add `verify` only to sanity-check the number.
2. **New PSD order → fulfillment email** — trigger new Shopify order; deterministic → workflow; AI only to personalize one line (human preview first).
3. **Competitor price drop → alert** — trigger daily scrape; needs AI? Yes → `browser-automation` scrape + `verify` + Paymaster charges QL.
4. **Monday revenue report** — trigger Mon 9am; no AI → cron/`temporal-brain` pulling Stripe → Slack. Never fails.

## Rules

1. Never default to an agent — recommend the simplest workflow first.
2. Every recommendation needs a trigger, a metric, and a guardrail.
3. No predictable trigger → it stays manual (note it, don't force it).
4. `audit.py` is the source of truth for *running* this; this file is the *framework*.
5. The keyword classifier in `audit.py` is a heuristic — always review the "Needs AI?" column with human judgment.
