# DepotChaos - Quick Reference

## 🚨 Emergency Commands

```bash
# Check if working
curl -s http://localhost:8082/api/stats | python3 -m json.tool

# Restart service
systemctl restart depotchaos

# Kill port conflicts
sudo kill -9 $(lsof -t -i:8082) 2>/dev/null; systemctl restart depotchaos

# View recent logs
journalctl -u depotchaos -n 20 --no-pager

# Full diagnostic
python3 /root/.openclaw/workspace/skills/depotchaos/diagnose.py
```

## 📊 Current Stats (Live)

```bash
# Lead counts
echo "Total Leads: $(sqlite3 /root/.openclaw/workspace/data/depot_chaos/unified.db 'SELECT COUNT(*) FROM leads WHERE deleted = 0;')"

# Intelligence records
echo "Intelligence: $(sqlite3 /root/.openclaw/workspace/data/depot_chaos/unified.db 'SELECT COUNT(*) FROM datadepot_intelligence;')"

# By state
sqlite3 /root/.openclaw/workspace/data/depot_chaos/unified.db "SELECT state, COUNT(*) FROM leads WHERE deleted = 0 GROUP BY state ORDER BY COUNT(*) DESC LIMIT 10;"

# Today's new leads
echo "Today: $(sqlite3 /root/.openclaw/workspace/data/depot_chaos/unified.db \"SELECT COUNT(*) FROM leads WHERE DATE(created_at) = DATE('now') AND deleted = 0;\")"
```

## 🗄️ Database Locations

| Database | Path | Records |
|----------|------|---------|
| **Unified (CRM)** | `/data/depot_chaos/unified.db` | Leads, customers, intelligence |
| **Vendors** | `/DepotChaos/depot_chaos.db` | Vendor enrichment data |
| **Queue** | `/datadepot/queue/*.json` | Email queue |

## 🔌 API Quick Calls

```bash
# Base URL
BASE="http://localhost:8082/api"

# Stats
curl -s $BASE/stats

# List leads (page 1, 50 per page)
curl -s "$BASE/leads?page=1&per_page=50&status=new"

# Search leads
curl -s "$BASE/leads?search=Fresno&state=CA"

# Get intelligence by county
curl -s "$BASE/intelligence?county=Fresno&pos_system=Aloha"

# Check email queue
curl -s $BASE/queue

# Get calendar callbacks
curl -s "$BASE/calendar?year=2026&month=6"
```

## 🔧 Common Fixes

### Port 8082 in use
```bash
sudo fuser -k 8082/tcp 2>/dev/null; sleep 2; systemctl restart depotchaos
```

### Database locked
```bash
systemctl stop depotchaos
sleep 5
systemctl start depotchaos
```

### Web interface not loading
```bash
nginx -t && systemctl reload nginx
ls -la /var/www/psdepot.com/depotchaos/
```

## 📧 Email Queue

```bash
# View pending
ls -la /root/.openclaw/workspace/datadepot/queue/pending_emails.json

# Send specific email
curl -X POST "http://localhost:8082/api/queue/{email_id}/send"

# Cancel email
curl -X POST "http://localhost:8082/api/queue/{email_id}/cancel"
```

## 🔍 Troubleshooting Checklist

- [ ] Service running: `systemctl is-active depotchaos`
- [ ] Port listening: `ss -tlnp | grep 8082`
- [ ] API responding: `curl -s http://localhost:8082/api/stats`
- [ ] Database readable: `sqlite3 unified.db "SELECT 1"`
- [ ] Static files exist: `ls /var/www/psdepot.com/depotchaos/`
- [ ] Nginx config valid: `nginx -t`

---
*Quick ref for DepotChaos CRM - Last updated: 2026-06-03*
