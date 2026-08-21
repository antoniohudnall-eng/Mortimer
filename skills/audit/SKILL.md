# Audit Skill v1.0 - AOS Brain Health & Four C's Scorer

## Name
audit

## Description
Run comprehensive health check on AOS Brain v4.5 and score against the Four C's framework (Context, Connections, Capabilities, Cadence)

## When to Use
- Daily health checks
- After system restarts
- When diagnosing issues
- Weekly performance reviews

## What This Skill Does
1. Queries brain socket for all component status
2. Checks Society Agent services
3. Validates Mission Control endpoints
4. Scores Four C's against Nate's AIOS framework
5. Generates actionable recommendations

## What This Skill Does NOT Do
- Restart services (read-only audit)
- Modify configuration
- Access external APIs beyond localhost

## Workflow

### Phase 1: Brain Socket Query
```bash
# Core brain status
echo '{"cmd":"status"}' | nc -U /tmp/aos_brain.sock

# Organ status
echo '{"cmd":"liver"}' | nc -U /tmp/aos_brain.sock
echo '{"cmd":"kidneys"}' | nc -U /tmp/aos_brain.sock
echo '{"cmd":"lungs"}' | nc -U /tmp/aos_brain.sock
echo '{"cmd":"thyroid"}' | nc -U /tmp/aos_brain.sock
echo '{"cmd":"router"}' | nc -U /tmp/aos_brain.sock
```

### Phase 2: Service Health Check
```bash
systemctl is-active aos-brain-v4 aos-mission-control aos-bhsi-v4
systemctl is-active patricia-factory forge-factory chelios-security jordan-office aurora-tasks
```

### Phase 3: Mission Control API
```bash
curl -s http://localhost:8080/api/status
curl -s http://localhost:8080/api/brain
curl -s http://localhost:8080/api/thyroid
curl -s http://localhost:8080/api/router
```

### Phase 4: Four C's Scoring

#### Context (0-25 points)
- MEMORY.md exists and recent: 5 pts
- memory/ folder with daily logs: 5 pts
- SOUL.md + IDENTITY.md + USER.md: 5 pts
- HEARTBEAT.md current: 5 pts
- TOOLS.md configured: 5 pts

#### Connections (0-25 points)
- Mortimer model responsive: 5 pts
- Brain socket accessible: 5 pts
- Mission Control HTTP ready: 5 pts
- SMTP/env files configured: 5 pts
- External APIs reachable: 5 pts

#### Capabilities (0-25 points)
- Society Agents (5 services): 5 pts
- Keepalive scripts functional: 5 pts
- Diagnostic tools available: 5 pts
- Skills folder populated: 5 pts
- Curriculum feeder active: 5 pts

#### Cadence (0-25 points)
- Cron jobs scheduled: 5 pts
- Auto-checkpoint enabled: 5 pts
- Persistence v1.0 active: 5 pts
- Thyroid auto-regulation: 5 pts
- Router auto-switching: 5 pts

## Output Format

```markdown
# AOS Brain Audit Report - {timestamp}

## Overall Health: {score}/100

### Brain Status
| Component | State | Uptime |
|-----------|-------|--------|
| Brain v4.5 | {status} | {uptime} |
| BHSI v4 | {status} | {uptime} |
| Mission Control | {status} | {pid} |

### Four C's Score
| Category | Score | Status |
|----------|-------|--------|
| Context | {n}/25 | {emoji} |
| Connections | {n}/25 | {emoji} |
| Capabilities | {n}/25 | {emoji} |
| Cadence | {n}/25 | {emoji} |

### Top Recommendations
1. {recommendation}
2. {recommendation}
3. {recommendation}
```

## Reference Files
- ../../MEMORY.md
- ../../HEARTBEAT.md
- ../../SOUL.md
- ../../IDENTITY.md

## Scripts
- scripts/audit.sh - Main audit runner
- scripts/score_four_cs.py - Four C's scoring logic
