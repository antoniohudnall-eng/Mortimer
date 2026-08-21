---
skill_id: hostinger-vps
name: Hostinger VPS Fleet Management
version: 1.0.0
author: Captain
description: Manage Hostinger VPS instances via API. List, monitor, and control fleet infrastructure.
tags:
  - vps
  - hosting
  - infrastructure
  - management
requires:
  env_vars:
    - HOSTINGER_API_KEY
---

# Hostinger VPS Fleet Management Skill

Manage Hostinger VPS infrastructure via API.

## Quick Start

### List VPS instances:
```bash
curl -s -X GET "https://developers.hostinger.com/api/vps/v1/virtual-machines" \
  -H "Authorization: Bearer $HOSTINGER_API_KEY" \
  -H "Content-Type: application/json" | jq .
```

## Common Tasks

### Get VPS Details:
```bash
# Requires VPS ID
curl -s -X GET "https://developers.hostinger.com/api/vps/v1/virtual-machines/{id}" \
  -H "Authorization: Bearer $HOSTINGER_API_KEY"
```

### Check VPS Status:
```bash
# Returns state: running, stopped, etc.
```

## Fleet Infrastructure

### Known Fleet VPS:
| Hostname | IP | Status | ID |
|----------|-----|--------|-----|
| Miles.cloud | 31.97.6.40 | running | 1334753 |
| Mortimer.cloud | 31.97.6.30 | running | 1334755 |

Both:
- Plan: KVM 2 (2 vCPU, 8GB RAM, 100GB disk)
- OS: Ubuntu 24.04 LTS
- Data Center: ID 17
- Uptime: Stable

## Reference

- API Docs: https://developers.hostinger.com
- Dashboard: https://www.hostinger.com
