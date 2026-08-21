---
name: health-monitor
description: Monitor system and service health with automated checks and alerting. Use when setting up health checks for services, detecting failures, sending alerts, and generating health reports. Supports HTTP endpoints, process monitoring, and log analysis.
---

# Health Monitor Skill

Automated health monitoring for services and systems.

## Quick Start

Check a service:
```bash
scripts/check-http.sh http://localhost:3000/status
```

Monitor multiple services:
```bash
scripts/health-check.sh services.txt
```

## Features

- HTTP endpoint health checks
- Process status monitoring
- Log file analysis
- Alert on failure
- Generate health reports

## Common Tasks

### Check Single Endpoint
```bash
scripts/check-http.sh http://localhost:3000/status
```

### Monitor Service List
Create `services.txt`:
```
http://localhost:3000/status
core-agent
http://localhost:3001/health
bridge-mock
```

Then run:
```bash
scripts/health-check.sh services.txt
```

### Setup Automated Monitoring
Use with cron to run checks every 5 minutes:
```bash
*/5 * * * * /path/to/scripts/health-check.sh /path/to/services.txt
```

## Alerting

Configure alerts in `references/alert-config.md`.
