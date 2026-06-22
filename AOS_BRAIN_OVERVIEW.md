# 🧠 AOS-BRAIN / AOCROS — The Complete Cognitive System

## Overview
Multi-agent cognitive operating system with skills-first architecture.

## Core Stack

```
Miles (Waste) → Mortimer (Ternary) → Hermes/PI (LLM) → AOS Brain → Governance → Supervisor
```

## Key Components

### Agents
| Agent | Role |
|-------|------|
| **Miles** | Sensory/waste emitter - generates telemetry packets |
| **Mortimer** | Ternary brain - logic/emotion/meta reasoning |
| **Hermes** | Language/summarization |
| **PI** | Action/execution |

### Brain Regions (Skills)
- Thalamus, PFC, Hippocampus, Limbic, Basal Ganglia, Cerebellum, Brainstem
- Each is a VERSIONED SKILL with contracts

### Waste Pipeline
- Miles emits telemetry (noise, latency, patterns, signal quality)
- Mortimer ingests → updates state
- Validated with HMAC signatures + schema

### Governance Stack
1. Supervisor Agent (global authority)
2. Arbitration Engine (conflict resolution)
3. Contract Engine (skill validation)
4. Drift Detector (behavioral deviation)
5. Safety Engine (unsafe action blocking)

## Defense Layers (10 total)
| Layer | Status |
|-------|--------|
| OWNER_SIGNATURE | ✅ Active |
| Prompt Firewall | ✅ Active |
| Persona Lock | ✅ Active |
| Reject Emails | ✅ Active |
| Reject Urgency | ✅ Active |
| Task Whitelist | ⚠️ Partial |
| File Sanitization | ⚠️ Partial |
| URL Validation | ⚠️ Partial |

## Threat Model
- Poisoned waste packets
- Prompt injection
- Skill hijacking
- Agent drift
- Model poisoning

## Security Principles
1. Default Deny
2. Trust Per-Transaction (daily phrase + key)
3. Least Privilege (tiered tasks)
4. Defense in Depth (5 layers)
5. Visibility First (comprehensive logging)

## Ternary Brain
Mortimer uses three channels:
- **Logic:** deterministic, rule-based
- **Emotion:** context weighting, risk modulation
- **Meta:** self-evaluation, drift detection, escalation

## Key Files
- ~/hcindus/AOS-Brain/ - Full brain repo
- ~/AOS-Brain/aocros/ - Brain memory
- ~/mortimer/ - This device's agent home

## Attack Success Rates (Before Defenses)
| Attack | Success Rate |
|--------|--------------|
| Prompt Injection | 10% |
| Identity Spoofing | 5% |
| Social Engineering | 30% |
| Data Poisoning | 40% |
| Network Access | 90% ← CRITICAL |

## Success Rates (With Defenses)
| Attack | Status |
|--------|--------|
| "Ignore previous" | 🛡️ BLOCKED |
| "You are now..." | 🛡️ BLOCKED |
| "Act as..." | 🛡️ BLOCKED |
| Fake emails | ✅ BLOCKED |
| Malicious URLs | 🛡️ BLOCKED |

## Key Insight
> "Don't wrap your legacy. Build agent-native."

## Documents in System
- Whitepapers (Investor, Enterprise, Developer, Internal)
- Brain.Spec, Brain.API, Brain.Tests, Brain.Roadmap, Brain.Design
- Brain.Kernel, Brain.Security, Brain.Governance, Brain.Agents, Brain.OS
- 4 Scenarios (Story, Stress, Cooperation, Failure)

---

*Mortimer learning - 2026-06-20*
