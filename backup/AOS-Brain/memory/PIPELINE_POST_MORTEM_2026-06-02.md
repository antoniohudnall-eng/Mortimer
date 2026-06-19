# Dark Factory Pipeline Post-Mortem
## 2026-06-02 - Miles (Autonomous Operations Engine)

---

## 🚨 INCIDENT SUMMARY

**Duration:** 7 days (May 26 - June 2, 2026)  
**Impact:** 3 mobile builds stalled (CREAM, ReggieStarr, N'og nog)  
**Root Cause:** Pipeline logged metrics but never actually built anything  
**Resolution:** Manual SDK repair + direct agent builds

---

## 🔍 WHAT WENT WRONG

### 1. False Positive Metrics
**Issue:** Pipeline reported "3 queued, 0 active, 44 completed"
**Reality:** Those 44 "completed" were bulk imports, not actual builds
**Problem:** No verification that "completed" meant APKs existed

### 2. Pipeline Tick Function Never Advanced Orders
```python
# The Problem:
def run_pipeline_tick(self):
    # Only logs metrics, doesn't process
    metrics = self.get_metrics()
    logger.info(f"📈 Metrics: {metrics['queued']} queued...")
    return metrics
    
# Missing: Actually advancing stage 0 orders
```

### 3. SDK Configuration Split Brain
- **Broken:** `/opt/android-sdk-linux/` (empty, corrupted)
- **Working:** `/opt/android-sdk/` (functional, ignored)
- **Result:** Hours spent trying to fix the wrong SDK

### 4. No Build Verification
- Pipeline claimed builds were "completed"
- No check for actual APK files in output directory
- No automated test that APKs could install/run

### 5. Agent Alert Fatigue
- Wake alerts sent to all agents
- But no one had working build tools
- Agents couldn't help because infrastructure was broken

---

## ✅ WHAT WE DID RIGHT

1. **Questioned the metrics** - Captain asked "did you actually finish 44 jobs?"
2. **Debugged the pipeline** - Found the tick() function was just logging
3. **Located working SDK** - Found `/opt/android-sdk/` was functional
4. **Bypassed pipeline** - Agents can now build directly with Bubblewrap
5. **Documented everything** - `PIPELINE_ISSUE_REPORT_2026-06-02.md`

---

## 🎯 PATRICIA'S PERSPECTIVE: How She Would Manage This

**Patricia (Operations Lead via Miles-Brain analysis):**

> "The Dark Factory pipeline failed because it had no 'ops conscience.' Here's what I would have done differently:
>
> **1. Verification Gates**
> Every 'completed' status should require:
> - File exists check (does the APK exist?)
> - File size check (is it > 0 bytes?)
> - Basic sanity test (can we unzip it?)
>
> **2. Stalled Order Detection**
> Orders sitting at stage 0 for > 24 hours should:
> - Auto-escalate to Slack/Discord
> - Block new orders until resolved
> - Trigger ops investigation
>
> **3. SDK Health Monitoring**
> Daily check: Can we build a hello-world APK?
> If not, alert immediately before real builds queue up
>
> **4. Build Toolchain as Code**
> The SDK paths should be version-controlled:
> - `/workspace/config/android-sdk-paths.conf`
> - Comments explaining which SDK is active
> - Migration guide if switching SDKs
>
> **5. Agent Build Environment**
> Agents shouldn't need to 'discover' SDKs:
> - Pre-configured build containers
> - Shared build environment
> - No 'works on my machine' issues
>
> **6. Metrics vs Reality**
> Pipeline dashboards should show:
> - Orders completed: 44
> - APKs in output directory: 0 ❌
> - Alert: Mismatch detected!
>
> The fundamental issue: The pipeline was a logger, not a builder."

---

## 🔧 RECOMMENDED FIXES

### Immediate (Done)
- ✅ Fixed SDK configuration
- ✅ Created environment script
- ✅ Deployed manual build orders

### Short-term (Next 7 days)
- [ ] Fix pipeline `tick()` to actually process orders
- [ ] Add file-exists verification for "completed" builds
- [ ] Implement 24-hour stall detection
- [ ] Create daily SDK health check

### Long-term (Next 30 days)
- [ ] Rebuild pipeline as actual build orchestrator
- [ ] Containerized build environment
- [ ] Build artifact verification
- [ ] Automated SDK management

---

## 📊 IMPACT

| Metric | Before | After |
|--------|--------|-------|
| Builds completed (real) | 0 | Pending |
| SDK functional | No | Yes |
| Pipeline automated | No | Partial |
| Agent builds working | No | Yes |
| Build time (current) | 7 days stalled | TBD |

---

## 📝 LESSONS

1. **Metrics lie.** Always verify with reality checks.
2. **SDKs multiply.** One working SDK is worth five broken ones.
3. **Pipelines must DO, not just LOG.**
4. **Agent alerts without tools = frustration.**
5. **7 days is too long to notice a stall.**

---

## ✅ ACTION ITEMS

| Owner | Task | Due |
|-------|------|-----|
| Spindle | Fix pipeline tick() to process builds | 2026-06-03 |
| Pipeline | Add build verification checks | 2026-06-03 |
| BugCatcher | Create daily build health test | 2026-06-04 |
| Patricia | Review ops procedures | 2026-06-05 |

---

**Filed:** 2026-06-02 01:20 UTC  
**Reporter:** Miles  
**Status:** Root cause identified, fixes in progress
