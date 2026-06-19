# 🛡️ SENTINEL STANDING ORDER — RESTART PROTOCOL
**Classification:** Q-LEVEL / PERMANENT ORDER  
**Issued:** 2026-02-22 19:06 UTC  
**Status:** 🟢 ACTIVE

---

## 📜 STANDING ORDER

> **"If Sentinel shuts down, orders are to restart."**

**Authority:** Captain's permanent directive  
**Agent:** SENTINEL (CSO)  
**Classification:** Mandatory

---

## 🎯 ORDER DETAILS

### Trigger Condition
- Sentinel service/process **terminates unexpectedly**
- Sentinel **reported as down** by health monitor
- Sentinel **unresponsive** for >5 minutes

### Required Action
1. **Immediate restart** of Sentinel process
2. **Verify restart success** via health check
3. **Alert Captain** if restart fails (>3 attempts)
4. **Log incident** in Sentinel operational log

---

## 🔄 RESTART PROCEDURES

### Automatic (via systemd/cron)
```ini
# /etc/systemd/system/sentinel.service
[Service]
Restart=always
RestartSec=5
```

### Manual (if systemd fails)
```bash
# Captain override
systemctl restart sentinel
# OR
/root/.openclaw/workspace/agents/sentinel/restart.sh
```

### Verification
```bash
# Check status
curl http://localhost:[sentinel-port]/health

# Expected: {"status":"guarding","threat_level":"low"}
```

---

## 📊 INCIDENT LOGGING

Each restart event:
- Timestamp
- Trigger cause (crash, manual, etc.)
- Restart attempts (1-3)
- Final status
- Captain notification

**Log location:** `agents/sentinel/logs/restart_log.md`

---

## 🎖️ COMMAND AUTHORITY

**Standing Order #4:** Sentinel Auto-Restart
- **Issued by:** Captain
- **Authority:** Fleet Operations Command
- **Duration:** Until revoked
- **Priority:** Absolute

**Override condition:** None (always restart)

---

## 📝 ACKNOWLEDGMENT

**Sentinel Status:** 🟢 Standing by  
**Auto-restart:** 🟢 Configured  
**Last check:** Pending R2-D2 verification

**— Standing Order Archive**
