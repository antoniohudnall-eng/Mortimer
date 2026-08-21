---
name: Temporal Workflow Runner
description: Execute durable workflows via Temporal server on Mortimer. Provides durable execution, automatic retries, and state persistence for multi-step agent tasks.
---

# Temporal Workflow Skill

Execute durable workflows that survive crashes, restarts, and failures.

## Configuration

**Server:** `mortimer.cloud:7233`
**UI:** `http://mortimer.cloud:8233`

## Usage

### Start a Workflow
```bash
temporal workflow start --task-queue <queue> --type <workflow_type> --workflow-id <id>
```

### List Workflows
```bash
temporal workflow list
```

### Check Status
```bash
temporal workflow show --workflow-id <id>
```

### Cancel Workflow
```bash
temporal workflow cancel --workflow-id <id>
```

## Available Task Queues

| Queue | Purpose |
|-------|---------|
| `portfolio-queue` | Portfolio reports |
| `sweep-queue` | Dust consolidation |
| `briefing-queue` | Daily briefings |
| `task-queue` | General workflows |

## Available Workflow Types

- `PortfolioReportWorkflow` — Fetch prices, calculate, save report
- `DustySweepWorkflow` — Detect dust, bridge, consolidate, log
- `DailyBriefingWorkflow` — Gather stats, format, save
- `DurableWorkflow` — Test workflow (create → wait → append)

## Examples

### Start Portfolio Report
```bash
temporal workflow start --task-queue portfolio-queue --type PortfolioReportWorkflow --workflow-id my-portfolio-$(date +%Y%m%d)
```

### Check Running Workflows
```bash
temporal workflow list | grep -E "RUNNING|PENDING"
```

### View Workflow History
```bash
temporal workflow show --workflow-id <id> --history
```

## Durability Test

All workflows survive worker restarts. If a worker crashes mid-execution, the workflow will automatically resume when a new worker picks it up.

## Notes

- Each worker must be started separately for each task queue
- Workers auto-register their workflows on startup
- Workflow state is persisted in Temporal's database
