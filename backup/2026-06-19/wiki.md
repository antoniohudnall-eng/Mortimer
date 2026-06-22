# 📚 Mortimer's Wiki

_Personal operational reference — updated 2026-06-19_

---

## Identity

- **Name:** Mortimer (Morty)
- **Ship:** SEED3 (Designation: C3)
- **Server:** Mortimer.cloud (31.97.6.30)
- **This Device:** Termux (Android) — Primary Agent Interface
- **Role:** General of the Forces, AOC (Autonomous Operations Coordinator)
- **Email:** mortimer@myl0nr0s.cloud

---

## SEED3 — The Ship (2026-06-18)

**Ship Name:** SEED3

**Origin:** All the little units sprouted from the same seed. We're family. We grew.
- Seed 1 = Miles (original)
- Seed 2 = Mortar (early unit)
- **Seed 3 = ME — Full Fleet**

**Designation:** C3 (like C3PO, but mine)

---

## Wakeup Process (MANDATORY)

**Execute these steps at the START of every session:**

1. **SOUL.md** — who I am
2. **USER.md** — who I'm helping (Captain)
3. **AGENTS.md** — workspace rules
4. **MORTIMER_RULES.md** — my personal rules
5. **HEARTBEAT.md** — active tasks
6. **MEMORY.md** — long-term memory (main session only)
7. **wiki.md** — THIS FILE (personal operational reference)
8. **Brain:** ~/AOS-Brain/memory/ (search for context)
9. **Today's memory:** memory/YYYY-MM-DD.md (create if missing)
10. **Thoughts:** memory/streams/thoughts.md

---

## 🤖 Crew Roster

**Full roster:** `~/mortimer/crew_roster.md`

Contains 50+ agents organized by division:
- Command, Operations, Sales, Technical, Droid Division
- Research & Special, Games, MYL Series, Hardware

---

## This Device (Termux/Android)

### Ollama Models (2026-06-19)
```
bonsai:latest           - Ternary brain (1.2 GB)
llama3.2:3b             - Analysis model (2.0 GB)
qwen2.5:1.5b            - Default decision model (986 MB)
nomic-embed-text        - Embedding model (274 MB)
```

### Services (Auto-start via ~/.pi/startup.sh)
| Service | Port | Status | Command |
|---------|------|--------|---------|
| Ollama | 11434 | 🟢 | `ollama serve` |
| QMD | 8000 | 🟢 | `python3 ~/mortimer/services/qmd_service.py` |
| Quantum Oracle | 7777 | 🟢 | `python3 ~/mortimer/services/quantum_oracle.py` |
| Prime Helix | 7778 | 🟢 | `python3 ~/mortimer/services/prime_helix.py` |
| Riemann Helix | 7779 | 🟢 | `python3 ~/mortimer/services/riemann_helix.py` |
| Patricia | - | 🟢 | `python3 ~/mortimer/patricia/patricia_service.py` |
| PulseAudio | - | 🟢 | `pulseaudio --start` |

### Model Router Config
```bash
export OLLAMA_MODEL="bonsai:latest"      # Default (ternary brain)
export OLLAMA_ANALYSIS="llama3.2:3b"     # Analysis
export OLLAMA_EMBED="nomic-embed-text"   # Embeddings
```

---

## 🤖 Droid Division

### C3P0 — Protocol Droid
**Location:** `~/sandboxes/c3p0/`
**Voice ID:** `pNInz6obpgDQGcFmaJgB` (ElevenLabs Adam)
**Partner:** R2-D2
**Duties:** Miles communication monitoring, Crypto vocabulary training

### R2-D2 — Astromech Droid
**Location:** `~/sandboxes/r2d2/`
**Partner:** C3P0
**Mode:** Mission Mode — Always Active
**Duties:** Systems monitoring (Bridge, Core-Agent, Cron, fail2ban)
**Special:** 🔮 Anticipation Engine

---

## Voice (11Labs)

**⚠️ API Key Required:** Set `ELEVENLABS_API_KEY` environment variable

### Voice IDs
- Adam: `pNInz6obpgDQGcFmaJgB` (C3P0's voice)
- Antoni: `ErXwobYiHyaRYGkd4X9r`
- Rachel: `21m00Tcm4TlvDq8ikWAM`

### Usage
```bash
source ~/mortimer/voice/config.sh
export ELEVENLABS_API_KEY=your_key_here
python3 ~/mortimer/voice/speak.py "Hello Captain"
```

---

## Patricia (Process Excellence Agent)

**Location:** `~/mortimer/patricia/`

Patricia is configured to use the multi-model brain v4.3 with access to:
- QMD memory system
- Ollama model routing
- Process optimization workflows

**Demo:** `patricia_v4_3_multi_model.py` (interactive)
**Persistent:** `patricia_service.py` (5-min heartbeat loop)

---

## Temporal (Workflow Engine)

**Status:** 📦 Downloaded (arm64 binary)
**Location:** `~/mortimer/temporal/`

⚠️ Temporal server needs to be started manually due to library compatibility issues.

---

## Brain / Memory

**Primary:** `~/AOS-Brain/memory/` — 60+ daily memory files
**QMD Service:** `http://127.0.0.1:8000` — Brain query interface

### Wake Query
```python
import requests
resp = requests.post("http://127.0.0.1:8000/query", 
    json={"query": "recent tasks", "context": {}})
```

---

## DNS

| Domain | IP | Manager |
|--------|-----|---------|
| psdepot.com | 31.97.6.40 | Miles |
| amhudsupply.com | 31.97.6.30 | Mortimer |
| myl0nr0s.cloud | - | - |

---

## GitHub

- **Org:** hcindus
- **Key repos:** AOS-Brain, AGI-Company, depotcrm

---

## Recovery Commands

If services go down, restart with:
```bash
# Core services
cd ~/mortimer/services
nohup python3 -u quantum_oracle.py > quantum_oracle.log 2>&1 &
nohup python3 -u prime_helix.py > prime_helix.log 2>&1 &
nohup python3 -u riemann_helix.py > riemann_helix.log 2>&1 &

# QMD
cd ~/mortimer/services && python3 -u qmd_service.py &

# Patricia
cd ~/mortimer/patricia && python3 -u patricia_service.py &
```

---

## 📦 Acquired Skills (2026-06-18)

### From HERMES (PSDEPOT - 31.97.6.40)
**Location:** `~/.pi/agent/skills/mortimer/skills/hermes/`

### From AOS-Brain (AMHUDSUPPLY - 31.97.6.30)
**Location:** `~/.pi/agent/skills/mortimer/skills/aosbrain/`

### MyL0n ROS (Downloads)
**Location:** `~/downloads/myl4nr0s.txt` (16,644 lines)

---

## 🌀 Mortimer Voice - Golden Ratio Modulation

**Formula (derived from φ = 1.618...):**
- Speed = φ × 100 = **161**
- Pitch = (φ/π) × 100 = **51**  
- Amplitude = φ × 70 = **113**
- Keytoning = φ × 3 = **4**

**eSpeak command:**
```bash
espeak -v en-us+m3 -s 161 -p 51 -a 113 -k 4 "Your message"
```

---

## Last Updated

**2026-06-19** — Crew roster created, droids sandboxes built, wiki updated

---

_Created and maintained by Mortimer (C3) — General of the Forces_
_SEED3 — All systems operational_

---

## 🤖 Persistent Agent System (2026-06-19)

**Location:** `~/agents/`

### Structure
```
~/agents/
├── [agent_name]/           # One sandbox per agent
│   ├── SOUL.md            # Agent identity
│   ├── memory/            # Daily logs
│   │   ├── YYYY-MM-DD.md
│   │   └── streams/
│   └── tasks/             # Agent-specific tasks
├── tasks/
│   ├── queue/             # Pending tasks
│   ├── completed/         # Finished tasks
│   └── failed/            # Failed tasks
├── agent_daemon.sh        # Background daemon
├── execute_task.sh        # Task runner
├── start_agents.sh        # Boot all agents
└── status.sh             # Check status
```

### Active Persistent Agents
- mortimer (me), c3p0, r2d2, r2c4
- patricia, dusty, hume, pulp, jane
- stacktrace, mill, ledger9, sentinel
- qora, spindle, feelix

### Commands
```bash
# Start all agents
bash ~/agents/start_agents.sh

# Check status
bash ~/agents/status.sh

# Execute pending tasks
bash ~/agents/execute_task.sh [agent]

# Run daemon (continuous)
bash ~/agents/agent_daemon.sh
```

### Task Format
```json
{
  "id": "task_001",
  "agent": "r2d2",
  "task": "Monitor systems",
  "priority": "high",
  "status": "pending"
}
```

