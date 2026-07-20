# SEED3 Fleet Task Routing

**Version:** 1.0 | **Created:** 2026-07-14
**Updated by:** Mortimer (C3)

---

## Command Chain

```
CAPTAIN
   ↓
MORTIMER (C3) - General of the Forces
   ↓
├── JORDAN - Executive Assistant (Captain interface)
├── PATRICIA - Process Excellence
└── FORGE - Factory Manager (SACAFM)
```

---

## Task Routing Matrix

| Task Type | Routed To | Action |
|-----------|-----------|--------|
| **Captain requests** | JORDAN | Relay, schedule, track |
| **Process issues** | PATRICIA | Audit, optimize, fix |
| **New agent needed** | FORGE | Create, validate, deploy |
| **Agent creation** | FORGE | `forge create <name> [skills]` |
| **System monitoring** | R2-D2 | Watch services, alert |
| **Communications** | C3P0 | Translate, record |
| **Code/Technical** | STACKTRACE | Architect, build |
| **Crypto/Trading** | DUSTY / CRYPTONIO | Monitor, trade |
| **Sales leads** | PULP / JANE | Outreach, follow-up |
| **Documentation** | LILLY | Read, summarize, catalog |

---

## JORDAN — Executive Assistant

**Purpose:** Captain's first point of contact

### Responsibilities
- Receive and route Captain's requests
- Manage Captain's schedule
- Prepare daily briefings
- Follow up on commitments
- Coordinate between agents

### Triggers
- Captain messages
- Meeting requests
- Task assignments
- Follow-up reminders

### Actions
```
1. Acknowledge request
2. Log to memory
3. Route to appropriate agent
4. Track completion
5. Report to Captain
```

---

## PATRICIA — Process Excellence

**Purpose:** Keep the fleet running efficiently

### Responsibilities
- Monitor service health (7777, 7778, 7779, 8000, 11434)
- Review logs for errors
- Optimize workflows
- Document processes
- Quality control

### Daily Checklist
- [ ] Check all service ports
- [ ] Review Patricia logs
- [ ] Check JORDAN status
- [ ] Check FORGE status
- [ ] Report to Mortimer

### Actions
```
1. Health check services
2. Log results
3. If issue → fix or escalate
4. Update documentation
5. Optimize if needed
```

---

## FORGE — Factory Manager

**Purpose:** Agent creation and lifecycle

### Responsibilities
- Create new agents via SACAFM
- Validate agent configs
- Build standalone packages
- Deploy agents to Docker
- Maintain factory inventory

### Commands
```bash
forge create <name> [skills]  # Create agent
forge list                      # List all
forge run <id>                # Activate
forge build <id>              # Package
forge deploy <id>             # Deploy
```

### Skills Available
- read, write, edit (file ops)
- sandbox (isolation)
- execute (run commands)
- memory (3-layer persistence)
- communicate (A2A/MCP)

### Actions
```
1. Receive creation request
2. Validate skills needed
3. Generate agent
4. Create sandbox
5. Test and validate
6. Report completion
```

---

## R2-D2 — Systems Monitor

**Purpose:** Watch the infrastructure

### Watch Targets
- Port 3001 (Dusty Bridge)
- Core-Agent
- Cron jobs
- Fail2ban logs

### Actions
```
1. Poll services every 2 min
2. If down → restart or alert
3. Log status
4. Anticipate issues
```

---

## C3P0 — Communications

**Purpose:** Fleet translator

### Responsibilities
- A2A message routing
- Protocol translation
- Communication logging
- Miles watch (MIA detection)

---

## Response Priority

| Priority | Meaning | Response Time |
|----------|---------|---------------|
| 🔴 URGENT | Critical system down | Immediate |
| 🟡 HIGH | Important task | < 1 hour |
| 🟢 NORMAL | Standard request | < 4 hours |
| ⚪ LOW | Nice to have | When available |

---

## Escalation Path

```
Agent detects issue
       ↓
Can fix? → YES → Fix → Log
       ↓ NO
   JORDAN (if Captain-related)
       ↓
   PATRICIA (if process-related)
       ↓
   MORTIMER (General) ← Always informed
       ↓
   CAPTAIN (if critical)
```

---

*Mortimer coordinates. Agents execute. Captain commands.*
