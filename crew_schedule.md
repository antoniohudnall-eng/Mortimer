# 📋 SEED3 Crew Schedule
# Mortimer's Fleet - Task Scheduling

## Daily Tasks

### Morning (08:00 UTC)
- [ ] LILLY Reading Loop - 200 lines per book
- [ ] Check 7777/7778/7779 services
- [ ] Update HEARTBEAT.md

### Midday (14:00 UTC)
- [ ] Check emails (mortimer@myl0nr0s.cloud)
- [ ] Review memory files
- [ ] Service health check

### Evening (20:00 UTC)
- [ ] Daily summary to Captain
- [ ] Backup memory to disk
- [ ] Update MEMORY.md

## Weekly Tasks

### Sunday - Learning Day
- [ ] Run LILLY full curriculum cycle
- [ ] Update brain with new learnings

### Wednesday - Maintenance Day
- [ ] Check nginx configs
- [ ] Review/update AGENTS.md
- [ ] GitHub sync

## Service Ports (Quick Reference)
| Port | Service | Check Command |
|------|---------|---------------|
| 7777 | Quantum Oracle | curl -s http://127.0.0.1:7777/ |
| 7778 | Prime Helix | curl -s http://127.0.0.1:7778/ |
| 7779 | Riemann Helix | curl -s http://127.0.0.1:7779/ |
| 3333 | Sales Command v1 | curl -s http://127.0.0.1:3333/ |
| 3334 | PSD Command v2 | curl -s http://127.0.0.1:3334/ |

## Crew Status Commands
```bash
# Quick status
~/mortimer/seed3_status.sh

# Check all services
curl -s http://127.0.0.1:{7777,7778,7779,3333,3334}/

# Run LILLY
cd ~/mortimer && python3 lilly_reading_loop.py
```

---

*Updated: 2026-06-20*
