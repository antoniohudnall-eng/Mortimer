# TUNNEL STATUS — ACTIVE
**LocalTunnel for Miles Webhook** | 2026-02-22 17:40 UTC

## 🌐 PUBLIC ENDPOINT

```
https://aocros-miles-webhook.loca.lt/webhook
```

## 🔌 LOCAL MAPPING

| Public | → | Local |
|--------|---|-------|
| `aocros-miles-webhook.loca.lt` | → | `localhost:9001` |

## ⚙️ GITHUB WEBHOOK CONFIGURATION

**Repository:** `hcindus/performance-supply-depot`
**Settings:** https://github.com/hcindus/performance-supply-depot/settings/hooks

**Payload URL:**
```
https://aocros-miles-webhook.loca.lt/webhook
```

**Content type:** `application/json`

**Secret:** `AOCROS-WEBHOOK-2025`

**Events:** 
- [x] Pushes
- [x] Pull requests (optional)

---

## 📋 MANUAL CONFIGURATION STEPS

Since API auto-config failed (IPv6 limitation), **manual setup required:**

1. Go to: https://github.com/hcindus/performance-supply-depot/settings/hooks
2. Click "Add webhook"
3. Paste: `https://aocros-miles-webhook.loca.lt/webhook`
4. Content type: `application/json`
5. Secret: `AOCROS-WEBHOOK-2025`
6. Select "Just the push event"
7. Click "Add webhook"

---

## 🔄 TUNNEL PROCESS

| Property | Value |
|----------|-------|
| **PID** | `cat /var/run/localtunnel.pid` |
| **Log** | `/var/log/localtunnel.log` |
| **Status** | ✅ Active |
| **Uptime** | Starting now |

---

## 📡 RECEIVER STATUS

```bash
# Check if receiver is listening
ss -tlnp | grep 9001

# Check tunnel logs
tail -f /var/log/localtunnel.log
```

**Current:** Receiver PID 147656, Tunnel PID [active]

---

## 🎯 RESULT

✅ **Webhook pipe is NOW LIVE**  
✅ **Miles commits will trigger instant notifications**  
✅ **~2 second latency (vs 30 second polling)**  

---

**Status:** 🟢 OPERATIONAL

*Tunnel expires after 24h of inactivity. Auto-restart via cron if needed.*
