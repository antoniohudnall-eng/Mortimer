---
name: cron-scheduler
description: Create and manage cron jobs for automated task scheduling. Use when setting up recurring tasks, scheduling health checks, automating reports, or managing periodic agent runs. Validates cron expressions, prevents duplicates, and provides job monitoring.
---

# Cron Scheduler Skill

Manage cron jobs for automated task scheduling.

## Quick Start

Add a health check job:
```bash
scripts/add-cron.sh "dusty-health" "*/5 * * * *" "health-check.sh services.txt"
```

List all jobs:
```bash
scripts/list-crons.sh
```

Remove a job:
```bash
scripts/remove-cron.sh "dusty-health"
```

## Cron Expression Format

```
* * * * *
│ │ │ │ │
│ │ │ │ └── Day of week (0-7, 0=Sunday)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```

Common patterns:
- `*/5 * * * *` - Every 5 minutes
- `0 * * * *` - Every hour
- `0 0 * * *` - Daily at midnight
- `0 9 * * 1` - Weekly on Monday 9am

## Validation

All cron expressions are validated before adding. Invalid expressions will be rejected with an error message.

## Job Naming

Use descriptive names:
- `dusty-health-check`
- `daily-report`
- `weekly-backup`

## References

See [references/cron-patterns.md](references/cron-patterns.md) for common scheduling patterns.
