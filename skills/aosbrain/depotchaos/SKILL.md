<!--
VERSION: 1.0.0
UPDATED: 2026-06-03
CHANGELOG: Initial documentation
-->

# DepotChaos - CRM & Lead Management System

**DepotChaos** is the unified Customer Relationship Management system for Performance Supply Depot LLC. It manages leads, customer intelligence, email campaigns, and sales pipelines.

---

## 🎯 Overview

| Component | Path | Purpose |
|-----------|------|---------|
| **Unified Database** | `/data/depot_chaos/unified.db` | Main CRM database (leads, customers, intelligence) |
| **Vendors Database** | `/DepotChaos/depot_chaos.db` | Vendor/supplier data for enrichment |
| **FastAPI Backend** | `/datadepot/web/depotchaos_fastapi.py` | REST API server |
| **Web Interface** | `/var/www/psdepot.com/depotchaos/` | Frontend dashboard |
| **Service** | `depotchaos.service` | Systemd service on port 8082 |

---

## 🚀 Quick Status Check

```bash
# Check service status
systemctl status depotchaos

# Test API connectivity
curl -s http://localhost:8082/api/stats | python3 -m json.tool

# Check database connection
sqlite3 /root/.openclaw/workspace/data/depot_chaos/unified.db "SELECT COUNT(*) FROM leads WHERE deleted = 0;"
```

---

## 📊 Database Schema

### unified.db (Main CRM)

#### `leads` Table
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PRIMARY KEY | Auto-increment ID |
| `business_name` | TEXT | Company/business name |
| `company_name` | TEXT | Alternative company name |
| `county` | TEXT | County/region |
| `city` | TEXT | City |
| `state` | TEXT | State code (e.g., 'CA', 'TX') |
| `zip` | TEXT | ZIP code |
| `contact_name` | TEXT | Primary contact name |
| `contact_title` | TEXT | Contact title/position |
| `phone` | TEXT | Phone number |
| `email` | TEXT | Email address |
| `status` | TEXT | 'new', 'contacted', 'converted', 'unqualified' |
| `tier` | TEXT | 'Tier 1', 'Tier 2', 'Tier 3' |
| `pos_system` | TEXT | POS system name (Aloha, Toast, etc.) |
| `pos_confidence` | REAL | Confidence score 0.0-1.0 |
| `replacement_score` | REAL | Replacement priority 0.0-1.0 |
| `enrichment_data` | TEXT | JSON blob with extra data |
| `deleted` | INTEGER | Soft delete flag (0/1) |
| `created_at` | TIMESTAMP | Creation timestamp |

#### `datadepot_intelligence` Table
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PRIMARY KEY | Auto-increment ID |
| `license_number` | TEXT | CA ABC license |
| `business_name` | TEXT | Business DBA name |
| `county` | TEXT | California county |
| `city` | TEXT | City |
| `address` | TEXT | Street address |
| `phone` | TEXT | Phone |
| `owner_name` | TEXT | License holder |
| `license_status` | TEXT | Active/Inactive/Pending |
| `pos_system` | TEXT | Detected POS system |
| `pos_confidence` | REAL | POS detection confidence |
| `replacement_score` | REAL | Replacement priority |
| `data` | TEXT | Raw JSON from ABC |

### depot_chaos.db (Vendors/Enrichment)

#### `vendors` Table
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PRIMARY KEY | Auto-increment ID |
| `name` | TEXT | Vendor/business name |
| `dba_name` | TEXT | DBA name |
| `contact_name` | TEXT | Contact person |
| `phone` | TEXT | Phone number |
| `email` | TEXT | Email |
| `city` | TEXT | City |
| `state` | TEXT | State |
| `vendor_type` | TEXT | Type of vendor |
| `status` | TEXT | 'active', 'promoted', 'inactive' |
| `notes` | TEXT | Enrichment notes |
| `imported_at` | TIMESTAMP | Import date |

---

## 🔧 Installation

### Prerequisites
```bash
# Required packages
pip install fastapi uvicorn sqlite3

# Verify Python version (3.8+)
python3 --version
```

### Service Setup

1. **Create systemd service file** (`/etc/systemd/system/depotchaos.service`):
```ini
[Unit]
Description=DepotChaos CRM Web Interface
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/workspace/datadepot/web
Environment=PYTHONUNBUFFERED=1
Environment=MAILGUN_API_KEY=your_key_here
Environment=MAILGUN_DOMAIN=psdepot.com
ExecStart=/usr/bin/python3 /root/.openclaw/workspace/datadepot/web/depotchaos_fastapi.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

2. **Enable and start service**:
```bash
systemctl daemon-reload
systemctl enable depotchaos
systemctl start depotchaos
```

### Directory Structure

```
/data/depot_chaos/
├── unified.db                    # Main CRM database
├── unified_backup_*.db           # Daily backups
└── daily_stats.json              # Statistics cache

/DepotChaos/
├── depot_chaos.db                # Vendor database
└── yelp_cache.json               # Yelp enrichment cache

/datadepot/
├── web/
│   └── depotchaos_fastapi.py     # FastAPI server
├── queue/
│   ├── pending_emails.json       # Email queue
│   ├── sent_emails.json          # Sent log
│   └── failed_emails.json        # Failed emails
├── content/                      # Email templates
└── templates/                    # HTML templates

/var/www/psdepot.com/depotchaos/
└── index.html                    # Web dashboard
```

---

## 🌐 API Endpoints

### Statistics
```
GET /api/stats
Response: {
    "total_leads": 6052,
    "datadepot_leads": 45,
    "by_status": {"new": 6040, "contacted": 2, ...},
    "by_tier": {"Tier 2": 44, "Tier 3": 6007},
    "intelligence_records": 74521,
    "new_today": 5
}
```

### Leads
```
# List leads (paginated, filterable)
GET /api/leads?page=1&per_page=50&status=new&state=CA

# Get single lead
GET /api/leads/{lead_id}

# Create lead
POST /api/leads
Body: {"business_name": "Joe's Diner", "city": "Fresno", ...}

# Update lead
PUT /api/leads/{lead_id}
Body: {"status": "contacted", "tier": "Tier 1"}

# Soft delete lead
DELETE /api/leads/{lead_id}?hard=false

# Hard delete lead
DELETE /api/leads/{lead_id}?hard=true
```

### Intelligence (CA ABC Data)
```
# List intelligence records
GET /api/intelligence?page=1&county=Fresno&pos_system=Aloha

# Get single record
GET /api/intelligence/{record_id}

# Update record
PUT /api/intelligence/{record_id}
Body: {"pos_system": "Toast", "replacement_score": 0.85}
```

### Email Queue
```
# Get queue status
GET /api/queue

# Send email immediately
POST /api/queue/{email_id}/send

# Cancel queued email
POST /api/queue/{email_id}/cancel

# Preview email
GET /api/queue/{email_id}/preview
```

### Calendar/Callbacks
```
# Get scheduled callbacks
GET /api/calendar?year=2026&month=6

Response: {
    "callbacks": [
        {
            "lead_id": 123,
            "company_name": "Example Corp",
            "callback_date": "2026-06-15T14:00:00",
            "callback_notes": "Follow up on quote"
        }
    ]
}
```

### Vendor Enrichment
```
# Get vendors for enrichment
GET /api/enrichment?page=1&search=pizza&city=Los Angeles

# Get single vendor
GET /api/enrichment/{vendor_id}

# Run Yelp enrichment for vendor
POST /api/enrichment/{vendor_id}/run

# Promote vendor to lead
POST /api/enrichment/{vendor_id}/promote
Body: {"assigned_agent": "Miles"}
```

---

## 🛠️ Common Operations

### Backup Database
```bash
# Create timestamped backup
cp /root/.openclaw/workspace/data/depot_chaos/unified.db \
   /root/.openclaw/workspace/data/depot_chaos/unified_backup_$(date +%Y%m%d_%H%M%S).db
```

### Query Examples
```bash
# Count leads by state
sqlite3 /root/.openclaw/workspace/data/depot_chaos/unified.db \
    "SELECT state, COUNT(*) FROM leads WHERE deleted = 0 GROUP BY state ORDER BY COUNT(*) DESC;"

# Find leads needing follow-up
sqlite3 /root/.openclaw/workspace/data/depot_chaos/unified.db \
    "SELECT business_name, phone, callback_date FROM leads WHERE callback_date IS NOT NULL AND deleted = 0 ORDER BY callback_date;"

# High-value intelligence (replacement score > 0.8)
sqlite3 /root/.openclaw/workspace/data/depot_chaos/unified.db \
    "SELECT business_name, county, pos_system, replacement_score FROM datadepot_intelligence WHERE replacement_score > 0.8 ORDER BY replacement_score DESC LIMIT 20;"
```

### Add New Lead
```bash
curl -X POST http://localhost:8082/api/leads \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "New Restaurant",
    "city": "Fresno",
    "state": "CA",
    "phone": "559-555-1234",
    "status": "new",
    "tier": "Tier 2"
  }'
```

---

## 🚨 Troubleshooting

### Issue: Service Won't Start (Port Already in Use)

**Symptoms:**
```
ERROR: [Errno 98] error while attempting to bind on address ('0.0.0.0', 8082): address already in use
```

**Solution:**
```bash
# Find process using port 8082
lsof -i :8082
ss -tlnp | grep 8082

# Kill zombie process
sudo kill -9 <PID>

# Restart service
systemctl restart depotchaos
```

### Issue: Database Locked

**Symptoms:**
```
sqlite3.OperationalError: database is locked
```

**Solution:**
```bash
# Check for other connections
fuser /root/.openclaw/workspace/data/depot_chaos/unified.db

# Wait for transactions to complete, or:
# 1. Restart the service
systemctl restart depotchaos

# 2. If persistent, check for zombie python processes
ps aux | grep python3 | grep -v grep
```

### Issue: API Returns 404/Connection Refused

**Symptoms:**
```
curl: (7) Failed to connect to localhost port 8082: Connection refused
```

**Solution:**
```bash
# Check service status
systemctl status depotchaos

# Check for port conflicts
netstat -tlnp | grep 8082

# Check logs
journalctl -u depotchaos -n 50 --no-pager

# Manual restart
systemctl stop depotchaos
sleep 2
systemctl start depotchaos
```

### Issue: Missing Tables or Schema Errors

**Solution:**
```bash
# Check database integrity
sqlite3 /root/.openclaw/workspace/data/depot_chaos/unified.db "PRAGMA integrity_check;"

# View schema
sqlite3 /root/.openclaw/workspace/data/depot_chaos/unified.db ".schema leads"
sqlite3 /root/.openclaw/workspace/data/depot_chaos/unified.db ".schema datadepot_intelligence"

# If corrupted, restore from backup
ls -la /root/.openclaw/workspace/data/depot_chaos/unified_backup_*.db
```

### Issue: Web Interface Not Loading

**Solution:**
```bash
# Check nginx configuration
cat /etc/nginx/sites-available/psdepot.com | grep -A5 depotchaos

# Test nginx config
nginx -t

# Reload nginx
systemctl reload nginx

# Check static files exist
ls -la /var/www/psdepot.com/depotchaos/
```

---

## 🤖 Agent Operations

### When to Check DepotChaos

Check DepotChaos status when:
- 🚨 User reports CRM is "not working" or "not connected"
- 📧 Email campaigns need monitoring
- 📊 Daily/weekly sales reports are requested
- 🔄 Lead imports or data synchronization tasks
- 🔍 Intelligence data enrichment operations

### Agent Diagnostic Script

```python
#!/usr/bin/env python3
"""DepotChaos health check for agents"""
import subprocess
import json
import sqlite3
import sys

def check_service():
    result = subprocess.run(
        ['systemctl', 'is-active', 'depotchaos'],
        capture_output=True, text=True
    )
    return result.stdout.strip() == 'active'

def check_port():
    result = subprocess.run(
        ['lsof', '-i', ':8082'],
        capture_output=True, text=True
    )
    return result.returncode == 0

def check_api():
    import urllib.request
    try:
        with urllib.request.urlopen('http://localhost:8082/api/stats', timeout=5) as resp:
            data = json.loads(resp.read())
            return data.get('total_leads', 0) > 0
    except:
        return False

def check_db():
    try:
        conn = sqlite3.connect('/root/.openclaw/workspace/data/depot_chaos/unified.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM leads WHERE deleted = 0")
        count = c.fetchone()[0]
        conn.close()
        return count > 0
    except:
        return False

if __name__ == '__main__':
    health = {
        'service': check_service(),
        'port': check_port(),
        'api': check_api(),
        'database': check_db()
    }
    
    all_healthy = all(health.values())
    
    print(json.dumps(health, indent=2))
    print(f"\nOverall: {'HEALTHY' if all_healthy else 'UNHEALTHY'}")
    sys.exit(0 if all_healthy else 1)
```

### Automated Recovery

```python
#!/usr/bin/env python3
"""Auto-recover DepotChaos issues"""
import subprocess
import time
import os
import signal

def recover_port_conflict():
    """Kill zombie processes on port 8082"""
    result = subprocess.run(
        ['lsof', '-t', '-i', ':8082'],
        capture_output=True, text=True
    )
    pids = result.stdout.strip().split('\n')
    
    for pid in pids:
        if pid:
            try:
                os.kill(int(pid), signal.SIGKILL)
                print(f"Killed process {pid}")
            except:
                pass
    
    time.sleep(2)
    subprocess.run(['systemctl', 'restart', 'depotchaos'])
    return True

def ensure_running():
    """Ensure service is running"""
    result = subprocess.run(
        ['systemctl', 'is-active', 'depotchaos'],
        capture_output=True, text=True
    )
    
    if result.stdout.strip() != 'active':
        print("Service not active, attempting restart...")
        subprocess.run(['systemctl', 'restart', 'depotchaos'])
        time.sleep(5)
        
        # Verify
        result = subprocess.run(
            ['systemctl', 'is-active', 'depotchaos'],
            capture_output=True, text=True
        )
        return result.stdout.strip() == 'active'
    
    return True

if __name__ == '__main__':
    if not ensure_running():
        print("Attempting port conflict recovery...")
        recover_port_conflict()
```

---

## 📅 Maintenance Schedule

| Task | Frequency | Command |
|------|-----------|---------|
| **Database backup** | Daily (automated) | Script in `/datadepot/cron/` |
| **Service health check** | Every 5 min | `systemctl status depotchaos` |
| **Port conflict scan** | Hourly | `lsof -i :8082` |
| **Log rotation** | Weekly | `journalctl --vacuum-time=7d` |
| **Backup cleanup** | Weekly | Remove backups >30 days |

---

## 📞 Support Contacts

| Issue Type | Contact | Method |
|------------|---------|--------|
| **Database corruption** | Hcindus | Telegram/Discord |
| **API failures** | AOS Brain | Socket `/tmp/aos_brain.sock` |
| **Email delivery** | Mailgun Dashboard | Web |
| **Nginx issues** | System logs | `journalctl -u nginx` |

---

## 🔗 Related Systems

| System | Integration | Port/Path |
|--------|-------------|-----------|
| **Mission Control** | Brain status | Port 8080 |
| **PSD Dashboard** | Customer data | Port 8081 |
| **DepotChaos** | Leads/Intel | Port 8082 |
| **Payment Server** | Stripe payments | Port 8083 |
| **N'og nog** | Game crew | tappylewis.cloud |

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-06-03 | Initial documentation |
| 1.1.0 | 2026-04-29 | FastAPI backend, unified database |
| 1.0.0 | 2026-03-16 | First CRM deployment |

---

**Status as of 2026-06-03:**
- ✅ Service: Active (PID 3190173)
- ✅ API: Responding
- ✅ Database: 6,052 leads, 74,521 intelligence records
- ✅ Port: 8082 (no conflicts)

*Source: `/root/.openclaw/workspace/skills/depotchaos/SKILL.md`*
