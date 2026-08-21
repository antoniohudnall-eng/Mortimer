# GoR Protocol v1.0 — Governance-Optimized Resolution

## Name
gor-protocol

## Description
Two-stage decision pipeline: Roast Council (adversarial analysis) → Patricia (strategic context) → Go/No-Go verdict. Prevents sycophancy, catches blind spots, and ensures every significant decision gets both adversarial scrutiny and organizational alignment before execution.

## When to Use
- Before Patricia delegates any complex or high-stakes task
- When evaluating new initiatives, features, or products
- Before resource allocation decisions ($1000+ or 40+ hours)
- Security-sensitive or customer-facing changes
- Any decision where Captain needs confidence it's been properly stress-tested

## The Formula
```
GoR(task) = Roast(task) + Patricia(roast_result) → Go(verdict)
```

### Stage 1: Roast (Internal Adversarial Analysis)
The 6-persona Roast Council evaluates the task independently:

| Persona | Role | Weight | Focus |
|---------|------|--------|-------|
| Contrarian | Fatal Flaw Finder | 25% | Why this WILL fail |
| Expansionist | Upside Maximizer | 15% | Biggest possible win |
| FirstPrinciples | Logic Purist | 20% | Strip assumptions, find truth |
| Researcher | Market Intelligence | 20% | Real data, competitors, TAM |
| Buyer | Customer Proxy | 20% | Would I pay? Objections? |
| Judge | Final Arbiter | — | Synthesize → Verdict |

**Output:** Weighted score (0-10) + Verdict (GREEN_LIGHT / RESHAPE / KILL)

### Stage 2: Patricia (Strategic Context)
Patricia reviews the Roast output and adds:
- **Organizational alignment** — Does this fit current priorities?
- **Resource availability** — Who's free? What's the budget?
- **Delegation target** — Which department/agent should execute?
- **Risk calibration** — Org-level risk appetite adjustment
- **Timeline impact** — How does this affect other commitments?

### Stage 3: GoR Verdict
Combined output:
- **Go** — GREEN_LIGHT from Roast + Patricia alignment = Execute
- **Reshape** — Mixed signals = Modify and re-submit
- **Kill** — KILL from Roast OR Patricia veto = Abandon

## Protocol Flow
```
Task Submitted
    │
    ▼
┌─────────────────────┐
│  STAGE 1: ROAST     │
│  6 Personas Evaluate │
│  Weighted Score     │
│  Verdict Generated   │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  STAGE 2: PATRICIA  │
│  Strategic Review    │
│  Org Context Added   │
│  Delegation Plan     │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  STAGE 3: GoR       │
│  Combined Decision   │
│  GO / RESHAPE / KILL │
│  Delegation Output   │
└─────────────────────┘
```

## Usage

### From AOS Socket
```bash
# Submit a task through GoR protocol
echo '{"cmd":"gor","task":{"title":"Launch new product","objective":"Create $9/mo SaaS tool","budget":5000,"time_estimate":80}}' | nc -U /tmp/aos_brain.sock

# Check GoR queue
echo '{"cmd":"gor","action":"queue"}' | nc -U /tmp/aos_brain.sock

# Get last GoR result
echo '{"cmd":"gor","action":"last"}' | nc -U /tmp/aos_brain.sock
```

### From Python
```python
from gor_protocol import GoRProtocol

gor = GoRProtocol()
result = gor.evaluate({
    "title": "Launch new product",
    "objective": "Create $9/mo SaaS tool for content creators",
    "budget": 5000,
    "time_estimate": 80
})

print(f"Verdict: {result['gor_verdict']}")
print(f"Roast Score: {result['roast_score']}/10")
print(f"Patricia Says: {result['patricia_context']}")
print(f"Delegated To: {result['delegation']['agent']}")
```

## Integration Points
- **Roast Skill:** `/root/.aos/aos/roast_skill.py`
- **Patricia:** Chief of Staff / Protocol Architect (qwen2.5:14b)
- **AOS Brain:** Socket at `/tmp/aos_brain.sock`
- **Org Structure:** `/root/.aos/aos/patricia_org_v2.json`

## Guardrails
- Always roast before Patricia reviews (never skip Stage 1)
- Patricia cannot override a KILL verdict (only escalate to Captain)
- RESHAPE verdicts must include specific modification requirements
- All GoR decisions logged to `/var/lib/aos/brain_state/gor_history.json`
- Captain has final override on any verdict

## Reference Files
- `gor_protocol.py` — Main protocol engine (`/root/.aos/aos/gor_protocol.py`)
- `/root/.aos/aos/roast_skill.py` — Stage 1: Roast Council
- `/root/.aos/aos/patricia_org_v2.json` — Org structure for delegation
- `/var/lib/aos/brain_state/gor_history.json` — Decision audit trail
