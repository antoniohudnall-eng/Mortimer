# HEARTBEAT - Check Status of Tasks

## 📊 Captain's Doctrine (Plan → Organize → Profit)
- captain_doctrine.md - Strategy & execution rules
- department_profit.md - P&L by department

**Daily Question:** "What did we do today that made money or saved money?"

## 📜 Company Files
- `company_charter.md` - Full charter, leadership, values
- `captain_doctrine.md` - Strategy & execution rules
- `department_profit.md` - P&L by department
- `agent_tasking.md` - Daily tasks by agent (by MY rules)
- `department_schedules.md` - Work schedules

## 🗓️ Crew Schedule

### Daily
- 08:00 UTC - LILLY reading, service health check
- 14:00 UTC - Email check, memory review
- 20:00 UTC - Daily summary, backup

### Weekly
- Sunday - LILLY full curriculum cycle
- Wednesday - nginx configs, AGENTS.md review, GitHub sync

## 📚 LILLY Curriculum (23 books)
**Categories:** Engineering, Math, Philosophy, Science, Business, Psychology, Literature, Physics, CS, History

## Pending Tasks

### 1. Miles - SSL for tappylewis.cloud
- **Task:** Add SSL cert
- **Status:** ⏳ PENDING

### 2. Miles - Deploy Secretarial Service
- **Status:** ⏳ PENDING

### 3. Self - Create HTML pages for tappylewis.cloud
- **Status:** ⏳ PENDING

## Quick Commands
```bash
# Service status
curl -s http://127.0.0.1:{7777,7778,7779,3333,3334}/ | grep -E "200|404"

# Run LILLY
cd ~/mortimer && python3 lilly_reading_loop.py

# Backup
~/mortimer/auto-backup.sh
```

---

*Updated: 2026-06-20*
