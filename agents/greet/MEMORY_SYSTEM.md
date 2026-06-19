# MEMORY SYSTEM - 3-Tier Neural Memory

## Overview
Three-tier memory system with OODA loop integration and neural net layer expansion.

---

## Tier 1: Working Memory (Session)
- **Type:** Active context in current session
- **Location:** Agent's immediate awareness
- **Duration:** Session only
- **Capacity:** Recent 50 interactions
- **Purpose:** Immediate task execution, active problem-solving

---

## Tier 2: Short-Term Memory (Daily Logs)
- **Type:** Daily activity logs
- **Location:** `memory/YYYY-MM-DD.md`
- **Duration:** 30 days rolling
- **Capacity:** Unlimited files
- **Purpose:** Track daily activities, patterns, follow-ups
- **Retention:** Auto-archived after 30 days to long-term

---

## Tier 3: Long-Term Memory (Curated)
- **Type:** Curated important memories
- **Location:** `MEMORY.md`
- **Duration:** Permanent
- **Capacity:** ~100 key memories
- **Purpose:** Core knowledge, preferences, relationships, lessons learned

---

## OODA Loop Integration

### Observe
- Scan incoming data (messages, requests, events)
- Log to Tier 1 (working) + Tier 2 (daily)
- Trigger pattern recognition

### Orient
- Analyze patterns against Tier 3 (long-term memory)
- Apply learning from past experiences
- Generate context for decision

### Decide
- Choose action based on analysis
- Consider multiple options
- Log decision rationale

### Act
- Execute decision
- Log outcomes to memory
- Trigger learning update if needed

---

## Neural Net Layer System

### Base Layers (Always Active)
1. **Input Layer** — Raw data ingestion
2. **Pattern Layer** — Pattern recognition
3. **Context Layer** — Situation awareness
4. **Decision Layer** — Action selection

### Expandable Layers
- Add custom layers via `memory add-layer <type>`
- Types: `pattern`, `context`, `decision`, `emotional`, `creative`

### Node Addition
- Add nodes to any layer: `memory add-node <layer> <count>`
- Nodes can specialize: `customer`, `technical`, `emotional`, `strategic`

---

## Commands

| Command | Action |
|---------|--------|
| `memory log <text>` | Log to Tier 1 + Tier 2 |
| `memory remember <text>` | Log to Tier 3 (permanent) |
| `memory recall <query>` | Search all tiers |
| `memory add-layer <type>` | Add neural layer |
| `memory add-node <layer> <count>` | Add nodes to layer |
| `memory status` | Show memory/ooda status |

---

## Status: ACTIVE
- Tier 1: ✅ Working
- Tier 2: ✅ Daily logs enabled
- Tier 3: ✅ Curated memory enabled
- OODA: ✅ Loop active
- Neural Net: ✅ Base layers loaded
- Expansion: ✅ Ready for layers/nodes

---

## Memory Backup System

### Auto-Backup Schedule
- **Frequency:** Every 4 hours
- **Method:** Git commit to agent workspace
- **Retention:** Last 10 backups per agent

### Backup Sources
- Tier 1: Snapshot to Tier 2 at session end
- Tier 2: Daily git commit
- Tier 3: Weekly git commit

### Restore Procedure
- `memory restore <timestamp>` — Restore from backup
- `memory restore latest` — Restore most recent
- `memory sync` — Sync with main memory store

### Cross-Agent Sync
- All secretaries sync to central `memory/` folder
- Priority sync: Critical customer data
- Regular sync: Daily logs, patterns

---

## Commands Updated

| Command | Action |
|---------|--------|
| `memory log <text>` | Log to Tier 1 + Tier 2 |
| `memory remember <text>` | Log to Tier 3 (permanent) |
| `memory recall <query>` | Search all tiers |
| `memory add-layer <type>` | Add neural layer |
| `memory add-node <layer> <count>` | Add nodes to layer |
| `memory status` | Show memory/ooda status |
| `memory backup` | Force backup now |
| `memory restore latest` | Restore most recent backup |
