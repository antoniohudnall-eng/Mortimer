# 📚 Mortimer's Wiki

_Personal operational reference — updated 2026-06-17_

---

## Identity

- **Name:** Mortimer
- **Server:** Mortimer.cloud (31.97.6.30)
- **This Device:** Termux (Android) — Primary Agent Interface
- **Role:** General of the Forces, AOC (Autonomous Operations Coordinator)
- **Email:** mortimer@myl0nr0s.cloud

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

## This Device (Termux/Android)

### Ollama Models
```
qwen2.5:1.5b     - Default decision model
llama3.2:3b      - Analysis model
nomic-embed-text - Embedding model
bonsai-8b-q1_0  - Ternary Bonsai (downloading...)
```

### Services (Auto-start via ~/.pi/startup.sh)
| Service | Port | Status | Command |
|---------|------|--------|---------|
| PulseAudio | - | 🟢 | `pulseaudio --start` |
| Ollama | 11434 | 🟢 | `ollama serve` |
| QMD | 8000 | 🟢 | `python3 ~/mortimer/services/qmd_service.py` |
| Termux API | - | 🟢 | `termux-*` commands |

### Model Router Config
```bash
export OLLAMA_MODEL="bonsai:latest"      # Default (ternary brain)
export OLLAMA_ANALYSIS="llama3.2:3b"    # Analysis
export OLLAMA_EMBED="nomic-embed-text"  # Embeddings
```

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

---

## Temporal (Workflow Engine)

**Status:** 📦 Downloaded (arm64 binary)
**Location:** `~/mortimer/temporal/`
**Binary:** `~/mortimer/prism-llama/llama-prism-b8846-d104cf1/`

⚠️ Temporal server needs to be started manually due to library compatibility issues.

---

## Brain / Memory

**Primary:** `~/AOS-Brain/memory/` — 50+ daily memory files
**QMD Service:** `http://127.0.0.1:8000` — Brain query interface

### Wake Query
```python
# Query memory via QMD API
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

---

## GitHub

- **Org:** hcindus
- **Key repos:** AOS-Brain, AGI-Company, depotcrm

---

## Last Updated

2026-06-17 — Termux device setup complete

---

## Recovery Commands (Updated 2026-06-17)

If services go down, restart with:
```bash
# QMD
cd ~/mortimer/services && python3 -u qmd_service.py &

# Patricia
cd ~/mortimer/patricia && python3 -u patricia_service.py &
```

## Patricia Service
- Demo: `patricia_v4_3_multi_model.py` (interactive)
- Persistent: `patricia_service.py` (5-min heartbeat loop)
- Brain v4.3: Mort_II (primary), Phi-3, TinyLlama, Qwen 2.5, Llama 3.2
