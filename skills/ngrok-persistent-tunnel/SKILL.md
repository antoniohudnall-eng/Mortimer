---
skill_id: ngrok-tunnel
name: Ngrok Persistent Tunnel
version: 1.0.0
author: Captain
description: Create stable, persistent tunnels using ngrok with authtoken authentication. Solves LocalTunnel collapse on restart issue.
tags:
  - tunnel
  - networking
  - infrastructure
  - communication
requires:
  host_binaries:
    - ngrok
  env_vars:
    - NGROK_TOKEN
---

# Ngrok Persistent Tunnel Skill

Create stable, persistent tunnels using ngrok.

## Overview

This skill creates reliable tunnels that persist across system restarts, unlike LocalTunnel which collapses on restart. Essential for fleet communications.

## Quick Start

### Start a tunnel:
```bash
export NGROK_TOKEN=$(cat /root/.openclaw/workspace/vault/NGROK_TOKEN.txt | grep -v '^#' | grep -v '^$' | cut -d= -f2)
ngrok http 8080 --authtoken=$NGROK_TOKEN
```

### Subdomain persistence:
```bash
ngrok http 8080 --authtoken=$NGROK_TOKEN --subdomain=miles-stable
```

## Common Patterns

### Fleet Communication Tunnel:
```bash
# Start persistent webhook receiver tunnel
ngrok http 8080 --authtoken=$NGROK_TOKEN \
  --subdomain=miles-webhook \
  --bind-tls=true
```

### TCP Forwarding:
```bash
# Forward SSH or other TCP services
ngrok tcp 22 --authtoken=$NGROK_TOKEN
```

## Configuration Files

Create `ngrok.yml`:
```yaml
authtoken: YOUR_TOKEN
region: us
console_ui: false
tunnels:
  webhook:
    addr: 8080
    proto: http
    subdomain: miles-webhook
    bind_tls: true
```

Then run:
```bash
ngrok start webhook --config=ngrok.yml
```

## Reference

- Ngrok Docs: https://ngrok.com/docs
- Web Dashboard: http://localhost:4040
