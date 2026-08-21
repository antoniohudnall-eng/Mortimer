---
name: dusty-mvp
description: Manage the Dusty crypto bot MVP sandbox. Use when deploying, testing, or troubleshooting the Dusty crypto dust consolidation bot and its services (core-agent, bridge-mock, openclaw-mock). Handles service startup, health checks, end-to-end testing, and log analysis.
---

# Dusty MVP Skill

Manage the Dusty crypto bot sandbox environment.

## Quick Start

Start all services:
```bash
scripts/start-services.sh
```

Check health:
```bash
curl http://localhost:3000/status
curl http://localhost:3001/health
curl http://localhost:4000/status
```

## Service Architecture

- **core-agent** (port 3000): Task management API
- **bridge-mock** (port 3001): Telegram webhook simulation
- **openclaw-mock** (port 4000): Dusty bot responses

## Common Tasks

### Start Services
Use `scripts/start-services.sh` to start all three services.

### Test End-to-End Flow
```bash
curl -X POST http://localhost:3001/webhook \
  -H "Content-Type: application/json" \
  -d '{"message":{"from":{"username":"test"},"chat":{"id":123},"text":"Find dust"}}'
```

### View Logs
```bash
tail -f /tmp/core-agent.log
tail -f /tmp/bridge.log
```

### Stop Services
```bash
pkill -f "node src/index.js"
pkill -f "node bridge_mock.js"
pkill -f "node openclaw_mock.js"
```

## API Reference

See [references/api.md](references/api.md) for full endpoint documentation.
