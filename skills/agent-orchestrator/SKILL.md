---
name: agent-orchestrator
description: Spawn and manage sub-agents for parallel task execution. Uses Agent Factory task queue with real backends (not blocked sessions_spawn API).
metadata:
  emoji: 🚀
  triggers:
    - spawn agent
    - orchestrate
    - sub-agent
    - parallel
    - /spawn
---

# Agent Orchestrator v2.0

Real sub-agent orchestration via Agent Factory task queue.

**Status: 🟢 VERIFIED WORKING (2026-07-24)**

## Quick Start

```bash
# Spawn a sub-agent
spawn-agent.sh "Scrape https://psdepot.com for meta and prices" browser-agent high

# Check fleet status
spawn-agent.sh --status

# Collect results from an agent
spawn-agent.sh --collect browser-agent
```

## Verified Agents (with working backends)

| Agent | Backend | Capability |
|-------|---------|------------|
| **browser-agent** ✅ | browser_agent.py | Web scraping, price extraction, competitor monitoring |
| **jordan** ✅ | cmd.sh | Office controller, diagnostics |
| **patricia** ⚠️ | patricia_service.py | Process excellence (service mode) |
| **mortimer** ✅ | self | All tasks (orchestrator default) |

## Orchestration Patterns

### Fan-Out: Parallel Scraping

```bash
spawn-agent.sh "Scrape https://competitor1.com" browser-agent high &
spawn-agent.sh "Scrape https://competitor2.com" browser-agent high &
spawn-agent.sh "Scrape https://competitor3.com" browser-agent high &
wait
spawn-agent.sh --collect browser-agent
```

### Pipeline: Scrape → Analyze

```bash
# Step 1: Browser agent scrapes data
spawn-agent.sh "Scrape https://psdepot.com products" browser-agent high

# Step 2: Patricia analyzes results
spawn-agent.sh "Analyze scraped pricing data" patricia normal

# Step 3: Collect all
spawn-agent.sh --collect
```

### Map-Reduce: Distributed Processing

```bash
# Map: Split work across agents
spawn-agent.sh "Process DepotChaos leads batch 1" miles high
spawn-agent.sh "Process DepotChaos leads batch 2" pulp high
spawn-agent.sh "Process DepotChaos leads batch 3" jane high

# Wait for completion, then reduce
spawn-agent.sh --collect
```

## File Locations

- **Orchestrator:** `~/.pi/agent/skills/mortimer/skills/agent-orchestrator/scripts/spawn-agent.sh`
- **Task Queue:** `~/agents/tasks/`
- **Executor:** `~/agents/execute_task.sh` (v2.0 — real dispatch engine)

## History

- **v2.0 (2026-07-24):** Rewired to use Agent Factory task queue, bypassing blocked `sessions_spawn` API. First successful sub-agent spawn (browser-agent → psdepot.com).
- **v1.0 (2026-06-18):** Original template — referenced blocked API, never actually spawned agents.

## Notes

- Add new agent backends to `~/agents/execute_task.sh` AGENT_BACKENDS array
- All spawns recorded in `~/agents/orchestrator.log`
- Tasks auto-dispatch immediately on spawn
- Failed spawns go to `~/agents/tasks/failed/`
