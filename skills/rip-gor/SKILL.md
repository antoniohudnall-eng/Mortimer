---
name: rip-gor
description: RiP + GoR protocol — Phase 1: Council roast (fatal flaws), Phase 2: Patricia Six Sigma (root cause + fix), Phase 3: GoR (verify fix exists, wire it, test). Use when Captain says "rip this", "rip and gor", "full diagnostic", or when a subsystem shows critical metrics degradation requiring root cause analysis and fix.
---

# RiP + GoR — Full Diagnostic Protocol

Three-phase protocol for finding, diagnosing, and fixing critical subsystem issues.

## Origin

Born 2026-07-28 on Miles Brain v4.4. Discovered Kidney was a black hole — 14,883 excreted, ZERO reabsorbed. GoR (reabsorption code) existed but was never wired into the filter pipeline. RiP found it, Patricia root-caused it, GoR verified the fix.

## When to Trigger

- Brain metrics degradation (cache ratio >100%, reabsorption = 0, Tracray full)
- Any subsystem showing statistically impossible numbers
- Captain says "rip this" or "full diagnostic"
- After major changes — verify nothing broke

## Phase 1: RiP — Roast (Council) + Patricia (Six Sigma)

### Step 1: Gather Waste
```bash
# Pull latest brain waste snapshot
scp root@31.97.6.30:/root/Mortimer/brain-waste-json/waste-*.json ~/downloads/waste_roast/
```

### Step 2: Council Roast
Convene the Council (see `council` skill) on the metrics:
- **Contrarian:** Find fatal bugs. Cache ratio >100%? Reabsorption = 0? Impossible numbers?
- **Expansionist:** What's the upside if fixed?
- **First Principles:** What's actually broken vs. config issue?
- **Researcher:** What do healthy numbers look like?
- **Buyer:** What does this cost us in lost capability?

### Step 3: Patricia — Root Cause Analysis
For each defect found:
| # | Defect | Severity | Root Cause | Fix | Effort |
|---|--------|----------|------------|-----|--------|
| 1 | ... | Critical/Major/Minor | Why it happens | What to change | Time |

### Step 4: Cheapest 48-Hour Test
Minimal change to validate the fix works:
- **H0-1:** Apply fix
- **H1-2:** Verify metric changes
- **H2-48:** Monitor stability

## Phase 2: GoR — Go = Result

### Verify Code Exists
```bash
# Check if the fix code actually exists somewhere
grep -rn "reabsorb\|GoR\|fix" /root/.openclaw/workspace/aoscros_brain/
```

### Check Wiring
Is the fix code CONNECTED to the execution path? Or does it exist but never get called?

### Wire It
If code exists but isn't called, wire it into the pipeline.
If code doesn't exist, implement the minimal version.

### Test
Run a live test with the fix active. Compare metrics before/after.

## Phase 3: Disposition

| Phase | Verdict | Confidence |
|-------|---------|------------|
| Council Roast | GREEN / RESHAPE / KILL | HIGH/MED/LOW |
| Patricia | Root causes + fixes identified | HIGH/MED/LOW |
| GoR | Fix EXISTS / MISSING / WIRED / NOT WIRED | CONFIRMED |
| **Final** | **Proceed / Patch / Escalate** | **Final confidence** |

## Patricia's Final Order

> "Execute 48hr test. If metrics show measurable improvement, promote to BETA. If not, escalate to Captain."

## Shutdown Protocol
```bash
# 1. Save all state
bash myl0n/brain/brain.sh save

# 2. Write RiP+GoR disposition to brain-waste/
# 3. Commit to memory
# 4. Rule 11: Saved to disk
```

## Startup Protocol
```bash
# 1. Read last RiP+GoR disposition
# 2. Check if fixes held
# 3. Re-verify metrics
# 4. If degraded: re-trigger RiP
```

## Notes

- RiP without GoR is just complaining. GoR is what makes it actionable.
- GoR = the code ALREADY EXISTS, it's just not wired. Find it, connect it.
- If GoR code truly doesn't exist, Patricia should design the minimal version.
- Always save the full RiP+GoR cycle to `brain-waste/RIP_GOR_YYYY-MM-DD.md`
