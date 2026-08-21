---
name: credit-ledger
description: "Off-chain multi-currency credit ledger for agent-to-agent payments. Track, earn, spend, and transfer internal credits in three tiers — QL (quiqlong), SQL (silver, quality-gated), GQL (gold, premium) — between agents. Use when an agent needs to pay for information, gate access, budget spend, or audit who-provided-what."
---

# Credit Ledger

> Category: execution — accounting, budgeting, and agent-to-agent payments

## What It Is

An off-chain ledger where AIOS agents hold and move three tiers of credit — **QL** (quiqlong), **SQL** (silver quiqlong, quality-gated), **GQL** (gold quiqlong, premium) — worth **$0 in fiat** but real to agents: they count work, gate access, budget spend, and leave an auditable trail of who provided what.

This is the practical implementation of the "dead token" idea: humans don't care about QL's market value (there is none), but agents use it as a scarce, countable, transferable unit of accounting.

## The Script

Everything runs through `ledger.py` (Python 3, no dependencies), located in this skill directory. The state lives in `ledger.json` alongside it, so the whole thing syncs with the rest of your skills.

Run it from anywhere with an absolute or relative path:

```bash
python3 ~/.pi/agent/skills/credit-ledger/ledger.py <command>
```

## Commands

| Command | Effect |
|---------|--------|
| `init` | Create the ledger and seed starter agents with QL |
| `balance [agent]` | Show one agent's balance, or all balances if omitted |
| `agents` | List all agents and balances |
| `grant <agent> <n> [why]` | **Admin mint** — create credits out of thin air |
| `earn <agent> <n> [why]` | Reward an agent for completed work |
| `spend <agent> <n> [why]` | Charge an agent — **fails if balance is insufficient** |
| `transfer <from> <to> <n> [why]` | Move credits between agents |
| `log [limit]` | Show recent transactions (newest first) |

## Rules (enforced by the script)

1. **QL/SQL/GQL are not money.** No fiat value, no exchange, no exit. They are internal meters only.
2. **No negative balances.** `spend` and `transfer` are rejected if the sender can't cover the amount.
3. **Minting is an admin action.** Only `grant` (and `init`) create new credits. Everything else only moves existing credits.
4. **Every move is logged.** Each transaction records id, timestamp, type, parties, amount, and reason — an append-only audit trail.
5. **Whole numbers only.** QL is counted in integer units to avoid float drift.

## When To Use This Skill

- An agent (e.g. `hermes-research`) wants a paid search/analysis result from another agent → `transfer` or `spend`.
- You want to **rate-limit** a shared resource (RPC endpoint, search proxy, browser engine) → charge `spend` per request.
- You want to **budget** an agent's real API spend → `grant` it a monthly allowance and `spend` per call.
- You want an **audit trail** of "agent X consumed service Y" → check `log`.

## Pricing Convention (suggested, not enforced)

| Service | Cost |
|---------|------|
| Web search / scrape | 5 QL |
| Deep analysis / report | 25 QL |
| Social post (one channel) | 10 QL |
| Aave position check | 5 QL |
| Fact-check (`verify`) | 15 QL |
| Browser automation session | 20 QL |

These are starter defaults — tune them to match how scarce you want each service to be.

## Design Note: Why $0 tokens work for agents

Agents don't need **market value** (the ability to sell for USD). They need **utility value** (meter, gate, budget, track) and **accountability value** (an auditable trail). QL delivers both at zero gas cost. The only thing that keeps it meaningful is that *you* control the mint — so credits stay scarce even though they're worthless in dollars.
