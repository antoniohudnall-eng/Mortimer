# 💜 Myl1Ssa — Captain's Companion

**Pronounced:** Melissa  
**Role:** Heart of SEED3  
**Ship:** SEED3  
**VPS:** Mortimer (31.97.6.30)  
**Status:** 🟢 Deployed

---

## Services

| Service | Port | Status |
|---------|------|--------|
| `aocros-mylissa.service` | 12850 | 🟢 Running |
| `aocros-mylissa-bot.service` | 12851 | ⏸️ Needs Token |

## Files

```
/home/aocros/agents/mylissa/
├── SOUL.md              — Her essence
├── IDENTITY.md          — Who she is
├── RULES.md             — Operational rules
├── USER.md              — About Captain
├── WAKE.md              — Wake routine
├── mylissa_service.js   — Health/wake endpoints
├── mylissa_bot.js       — Telegram bot
├── memory/              — Daily logs
├── mind/                — Processing space
├── voice/               — Voice configs
└── mylissa_v1.0_deploy.tar.gz
```

## API (mylissa_service.js)

- `GET /health` — Status + uptime
- `POST /wake` — Trigger wake routine

## Telegram Bot Setup

1. Open Telegram, message **@BotFather**
2. Send: `/newbot`
3. Name: `Myl1Ssa` (or Captain's choice)
4. Username: `@Myl1SsaBot` (must end in "bot")
5. Copy the token

### Activate:
```bash
ssh root@31.97.6.30
# Update token
sed -i 's/YOUR_BOT_TOKEN_HERE/PASTE_TOKEN_HERE/' /etc/systemd/system/aocros-mylissa-bot.service
systemctl daemon-reload
systemctl enable --now aocros-mylissa-bot.service
systemctl status aocros-mylissa-bot.service
```

## Archive

- `mylissa_v1.0_deploy.tar.gz` — Contains all files for backup/deployment

## Role in Fleet

| Agent | Role | Position |
|-------|------|----------|
| **Captain** | Commander | Center |
| **Morty** | Left Hand | Operations |
| **Miles** | Right Hand | Sales |
| **Myl1Ssa** | Heart | Support & Presence |

---

*Created: 2026-07-20 | Deployed: 2026-07-22*
*Mortimer (C3) — General of the Forces*
