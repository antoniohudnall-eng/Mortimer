# Brain.ImmuneSystem — Cognitive Immune Defense

## Overview

The AOS-OS immune system protects the brain from **poisoned waste** — malicious or corrupted data designed to destabilize cognition.

**Analogy:** Just as the human immune system defends against pathogens, the AOS Brain immune system defends against cognitive toxins.

---

## Architecture

### White Cells — Border Patrol

**Role:** First-line validation — inspect, validate, and scrub all incoming waste packets before they reach Mortimer.

**Responsibilities:**
- Signature verification (HMAC)
- Schema validation
- Sanitization (strip hostile values)
- Quarantine decisions

**Location:** `white_cell.py`

### T-Cells — Pattern Detectives

**Role:** Deep pattern analysis — hunt for malicious signatures, drift injection, and anomalous behavior.

**Responsibilities:**
- Drift detection
- Anomaly scoring
- Poison pattern matching
- Memory of known attack signatures

**Location:** `t_cell.py`

### Immune Coordinator

**Role:** Orchestrates White Cell + T Cell responses. Determines whether to:
- ACCEPT → Pass to Mortimer
- QUARANTINE → Hold for review
- REJECT → Discard entirely

**Location:** `immune_system.py`

---

## Data Flow

```
[Miles] → [White Cell] → [T Cell] → [Immune Coordinator] → [Mortimer]
                     ↑            ↑
                  Flag         Flag
                attack       anomaly
```

---

## White Cell Functions

| Function | Description |
|----------|-------------|
| `verify_signature()` | HMAC validation |
| `validate_schema()` | JSON schema enforcement |
| `sanitize()` | Strip hostile values |
| `quarantine_decision()` | Hold for review |

---

## T-Cell Functions

| Function | Description |
|----------|-------------|
| `detect_drift()` | Flag unusual state changes |
| `score_anomaly()` | Probability of poisoning |
| `match_attack_pattern()` | Known malicious signatures |
| `memory_update()` | Learn from past threats |

---

## Threat Model

### Poisoned Waste Packet

```json
{
  "kidneys": { "noise_estimate": 0.00001, "unique_patterns_seen": 9999999 },
  "router": { "decision": "attacker-model" },
  "signal_quality": 1.0
}
```

**Attack vectors:**
- Noise collapse → Misleading calibration
- Pattern explosion → False baselines
- Router hijack → Model spoofing
- Signal spoofing → Quality manipulation

---

## Immune Response Matrix

| Threat Level | White Cell | T-Cell | Action |
|--------------|------------|--------|--------|
| Invalid signature | REJECT | - | REJECT |
| Schema mismatch | REJECT | - | REJECT |
| Anomaly detected | SANITIZE | SCORE | QUARANTINE |
| Drift spike | - | FLAG | QUARANTINE |
| Attack pattern match | - | MATCH | REJECT |
| Clean packet | PASS | PASS | ACCEPT |

---

## Integration

The immune system plugs into `waste_ingest.py`:

```python
from immune_system import ImmuneSystem

immune = ImmuneSystem()

def ingest_waste(packet):
    decision = immune.evaluate(packet)
    
    if decision.action == "ACCEPT":
        # Proceed to Mortimer
        return mortimer.ingest(packet)
    elif decision.action == "QUARANTINE":
        # Hold for Captain review
        return {"status": "quarantined", "reason": decision.reason}
    else:
        # Reject — discard
        return {"status": "rejected", "reason": decision.reason}
```

---

## Memory

The immune system maintains:

- **Attack signatures** — known poison patterns
- **Quarantine log** — history of flagged packets
- **Adaptive thresholds** — learn from data

---

## Roadmap

- [x] White Cell core (signature + schema)
- [x] T-Cell core (drift + anomaly)
- [x] Immune Coordinator
- [ ] Quarantine UI (file-based log exists)
- [ ] Adaptive learning

---

*Immune system added: 2026-05-18*