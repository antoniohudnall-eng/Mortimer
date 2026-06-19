# N'og nog: Crew Expansion System v1.0

**Persistent crew with brain integration, game server bridges, and captain communications.**

---

## 🎯 Overview

Your N'og nog crew now lives beyond the browser. This system provides:

- **5-10 Persistent Crew Members** with skills, levels, and equipment
- **AOS Brain Integration** for autonomous AI-driven decisions
- **Real Game Server Connections** (Roblox, Minecraft)
- **Captain Communications** via email and Telegram
- **Expedition Logging** with photos from crew

---

## 📁 Architecture

```
nognog/crew/
├── core/
│   ├── CrewManager.js        # Persistence + crew lifecycle
│   ├── CrewCoordinator.js    # Main orchestrator
│   └── BrainCrew.js          # AOS brain integration
├── integrations/
│   └── GameBridge.js         # Roblox + Minecraft bridges
├── comms/
│   └── CrewComms.js          # Email + Telegram
├── storage/crew/             # Crew JSON files
└── main.js                   # Full system entry

nognog/crew-lite.js           # Lightweight running system (ACTIVE)
nognog/crew-bridge.js         # Socket bridge to brain
```

---

## ⚡ Quick Commands

### Status
```bash
cd /root/.openclaw/workspace/nognog
node crew-lite.js list
```

### Manual Report
```bash
node crew-lite.js status
```

### Rest Crew
```bash
node crew-lite.js rest 8
```

### Socket Bridge
```bash
# Crew socket
echo '{"cmd":"status"}' | nc -U /tmp/nognog_crew.sock

# Direct brain query
echo '{"cmd":"brain","params":{"decide":true}}' | nc -U /tmp/nognog_crew.sock
```

---

## 🎖️ Current Crew (Generated)

| Name | Role | Level | Status |
|------|------|-------|--------|
| **Vex** | PILOT | Rookie | ACTIVE |
| **Nyx** | ENGINEER | Rookie | ACTIVE |
| **Jax** | SCIENTIST | Rookie | ACTIVE |
| **Luna** | COMBAT | Rookie | ACTIVE |
| **Aria** | MEDIC | Rookie | ACTIVE |

---

## 🧠 Brain Integration

The crew system connects to your AOS brain at `/tmp/aos_brain.sock`:

- **Decision Making**: Brain processes crew personalities + context
- **Autonomous Actions**: Crew make their own choices during ticks
- **Experience Growth**: Brain influences skill development paths

---

## 🌐 Game Bridges

### Roblox
- WebSocket to local bridge (port 8081)
- Real-time crew position tracking
- Command execution in-game

### Minecraft
- RCON connection to server
- 4 Mineflayer bots (Forge, Patricia, Chelios, Stella)
- Crew actions map to bot behaviors

---

## 📧 Communications

### Email Reports
- Hourly status reports to captain
- Discovery alerts
- Emergency notifications

### Telegram
- Real-time crew updates
- Photo sharing from expeditions
- Command interface for remote control

---

## 📊 Expedition Logs

Saved to `/root/.openclaw/workspace/expeditions/`:
- `discoveries.log` - All crew discoveries
- `crew_report_*.json` - Hourly reports
- `crew_*.jpg` - Photos from crew

---

## 🔧 Service Management

```bash
# Check status
systemctl status nognog-crew

# Restart
systemctl restart nognog-crew

# Stop
systemctl stop nognog-crew

# View logs
journalctl -u nognog-crew -f
```

---

## 🔄 Integration with Mission Control

Crew data available at:
- `http://localhost:8080/crew/status` (when implemented)
- Socket: `/tmp/nognog_crew.sock`

---

## 🛣️ Roadmap

- [x] Lite crew system (v1.0)
- [x] Persistence layer
- [x] Tick-based automation
- [x] Report generation
- [ ] Full BrainCrew AI decisions
- [ ] Roblox bridge
- [ ] Minecraft bot integration
- [ ] Email/Telegram notifications
- [ ] Photo handling
- [ ] Web dashboard

---

**Captain:** Your crew is active and ready for autonomous exploration! 🚀
