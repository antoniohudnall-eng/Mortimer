---
name: webhook-tunnel-setup
description: Set up LocalTunnel webhook for real-time GitHub notifications. Enables instant alerts when commits are pushed, eliminating polling delays.
metadata:
  {
    "openclaw":
      {
        "tags": ["webhook", "tunnel", "github", "real-time", "communication"],
        "author": "OpenClaw",
        "version": "1.0.0",
      },
  }
---

# Webhook Tunnel Setup

Real-time GitHub webhook via LocalTunnel for instant commit notifications.

## What It Does

- Creates public URL for local webhook receiver
- Receives GitHub push events instantly (~2 second latency)
- Eliminates need for polling (was 30s-5min delay)
- Secured with HMAC-SHA256 signature verification

## Quick Start

### 1. Start Receiver
```bash
cd pipes/webhook
python3 github_webhook_receiver.py
# Runs on localhost:9001
```

### 2. Create Tunnel
```bash
npx localtunnel --port 9001 --subdomain aocros-miles-webhook
```

### 3. Configure GitHub
- Go to: `https://github.com/USER/REPO/settings/hooks`
- Payload URL: `https://aocros-miles-webhook.loca.lt/webhook`
- Content type: `application/json`
- Secret: `AOCROS-WEBHOOK-2025`
- Events: Push

## Files Included

| File | Purpose |
|------|---------|
| `webhook/github_webhook_receiver.py` | Python receiver with HMAC verification |
| `TUNNEL_STATUS.md` | Current status and URLs |
| `WEBHOOK_SETUP_INSTRUCTIONS.sh` | Automated setup script |
| `PIPE_DOCUMENTATION.md` | Architecture details |

## Requirements

- Node.js (for localtunnel)
- Python 3
- OpenClaw with message capabilities

## Use Case

**Problem:** Agent on separate VPS (Miles) needs to notify main agent (Mortimer) of commits. File-based messaging has 5+ minute delay.

**Solution:** Webhook pipe reduces latency to ~2 seconds.

## Security

- HMAC-SHA256 signature verification
- Secret token required
- Only "push" events accepted
- Local receiver validates all requests

## Maintenance

- Tunnel expires after 24h (auto-restart recommended)
- Logs: `/var/log/localtunnel.log`
- Receiver PID: check `ss -tlnp | grep 9001`

## Credits

Built for AOCROS Collective | 2026-02-22
