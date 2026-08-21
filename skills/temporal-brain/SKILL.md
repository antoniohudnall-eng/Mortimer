---
name: temporal-brain
description: "Durable workflow orchestration via Temporal.io on the VPS — execute, schedule, and monitor brain and schedule workflows."
---

# Temporal Brain

> Category: execution — Task automation, command running, and process management

## Description

Durable workflow orchestration via Temporal.io on VPS (31.97.6.30:7233). Execute, schedule, and monitor workflows for brain processing, scheduled tasks, and the Master Schedule. Three brain workflows (init/pulse/process) + custom workflow creation.

## Instructions

# Temporal Brain — Durable Workflow Orchestration

Temporal.io running on the VPS. Workflows survive crashes, retry on failure, and can be scheduled with cron. This is the execution engine for everything that "must happen, no matter what."

---

## 🏗 Architecture

```
Phone (Termux)                VPS (31.97.6.30)
     │                              │
     │  HTTP POST /process          │
     ├──────────────────────────────→ Port 5100 (Temporal Brain API v3)
     │                              │
     │                              ├── Temporal Server :7233
     │                              │   ├── Worker (mortimer-brain-queue)
     │                              │   │   ├── BrainInitWorkflow
     │                              │   │   ├── ProcessQueryWorkflow
     │                              │   │   └── BrainPulseWorkflow
     │                              │   │
     │                              │   └── Activities (8):
     │                              │       liver → kidney → thyroid → QMD
     │                              │       → consciousness → tracray
     │                              │
     │  ◄── JSON response           │
     │                              │
```

**Server**: `31.97.6.30:7233` (Temporal) | `31.97.6.30:5100` (HTTP API)
**Namespace**: `default`
**Task Queue**: `mortimer-brain-queue`

---

## 🧠 Brain Workflows

### 1. BrainInit — Initialize brain state
```bash
# CLI (on VPS)
python3 temporal_brain_v3.py init

# HTTP (from phone)
curl http://31.97.6.30:5100/init
```
**Returns**: `{status: "initialized", timestamp, organs: [kidney, consciousness, tracray, thyroid, liver, cortex]}`

### 2. BrainPulse — Health check + state snapshot
```bash
# CLI
python3 temporal_brain_v3.py pulse

# HTTP
curl http://31.97.6.30:5100/pulse
```
**Returns**: `{pulse: "complete", state: {conscious_items, kidney_noise, thyroid_state, signal_quality, ...}}`

### 3. ProcessQuery — Full brain pipeline for any input
```bash
# CLI
python3 temporal_brain_v3.py process "analyze competitor pricing for thermal paper"

# HTTP
curl -X POST http://31.97.6.30:5100/process \
  -H "Content-Type: application/json" \
  -d '{"query": "analyze competitor pricing for thermal paper"}'
```
**Pipeline**: Liver (filter toxic) → Kidney (quality score) → Thyroid (route local/VPS) → QMD (query memory) → Consciousness (store it) → Tracray (remember it)

---

## 🔄 The Brain Pipeline (What Happens)

Every query flows through 6 organs in order:

| Step | Organ | What It Does | Gate |
|------|-------|-------------|------|
| 1 | **Liver** | Filters toxic/harmful content | Blocked if unsafe |
| 2 | **Kidney** | Scores signal quality (0-1) | Blocked if < 0.4 |
| 3 | **Thyroid** | Routes: LOCAL (< 100 chars) or VPS (> 100 chars) | Always passes |
| 4 | **QMD** | Queries memory across all layers | Always passes |
| 5 | **Consciousness** | Stores item in conscious layer | Always passes |
| 6 | **Tracray** | Records as episodic experience | Always passes |

**Rejection reasons**: `toxic` (liver blocked it) or `low_quality` (kidney rejected it)

---

## 📞 Calling from Phone (Termux)

The Temporal Brain exposes a simple HTTP API. No Temporal SDK needed on the phone.

### Health Check
```bash
curl -s http://31.97.6.30:5100/health | python3 -m json.tool
```

### Process a Query
```bash
curl -s -X POST http://31.97.6.30:5100/process \
  -H "Content-Type: application/json" \
  -d '{"query": "YOUR TEXT HERE"}' | python3 -m json.tool
```

### Get Brain Pulse
```bash
curl -s http://31.97.6.30:5100/pulse | python3 -m json.tool
```

### Python Wrapper (phone-side)
```python
import urllib.request, json

def temporal_process(query: str) -> dict:
    """Send a query through the brain pipeline."""
    data = json.dumps({"query": query}).encode()
    req = urllib.request.Request(
        "http://31.97.6.30:5100/process",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

def temporal_pulse() -> dict:
    """Get brain health snapshot."""
    with urllib.request.urlopen("http://31.97.6.30:5100/pulse", timeout=10) as resp:
        return json.loads(resp.read())
```

---

## ⏰ Scheduling Workflows (Cron)

Temporal supports cron schedules natively. Use `temporal schedule` on the VPS:

### Create a Scheduled Workflow
```bash
# On VPS:
temporal schedule create \
  --schedule-id "daily-brain-pulse" \
  --workflow-type "BrainPulseWorkflow" \
  --task-queue "mortimer-brain-queue" \
  --cron "0 8 * * *"   # Every day at 08:00 UTC
```

### List Schedules
```bash
temporal schedule list
```

### Describe a Schedule
```bash
temporal schedule describe --schedule-id "daily-brain-pulse"
```

### Delete a Schedule
```bash
temporal schedule delete --schedule-id "daily-brain-pulse"
```

### Master Schedule → Temporal Cron Map

| Master Schedule Task | Temporal Cron | Workflow |
|---------------------|---------------|----------|
| Aave health check (daily) | `0 16 * * *` (8am PST) | Custom: AaveHealthWorkflow |
| Competitor prices (Mon) | `0 17 * * 1` | Custom: CompetitorScanWorkflow |
| Brain pulse (daily) | `0 15 * * *` | BrainPulseWorkflow |
| CRM sync (daily) | `0 16 * * *` | Custom: DepotChaosSyncWorkflow |
| VPS health (Thu) | `0 14 * * 4` | BrainPulseWorkflow |

---

## 🏗 Creating Custom Workflows

Template for a new Temporal workflow:

```python
# custom_workflow.py (deploy to VPS)
from datetime import timedelta
from temporalio import workflow, activity

@activity.defn
async def my_activity(input_data: str) -> dict:
    """Your activity logic here."""
    return {"result": f"Processed: {input_data}"}

@workflow.defn
class MyCustomWorkflow:
    @workflow.run
    async def run(self, input_data: str) -> dict:
        result = await workflow.execute_activity(
            my_activity,
            input_data,
            start_to_close_timeout=timedelta(seconds=30),
        )
        return {"status": "complete", "data": result}

# Register in the Worker:
# worker = Worker(client, task_queue="mortimer-brain-queue",
#     workflows=[..., MyCustomWorkflow],
#     activities=[..., my_activity])
```

### Deploy Steps
1. Write workflow file on VPS: `~/downloads/mortimer-v1/brain/custom_workflow.py`
2. Add to Worker in `temporal_brain_v3.py`
3. Restart worker: `python3 temporal_brain_v3.py worker`
4. Test: `python3 temporal_brain_v3.py custom "test input"`

---

## 🩺 Health Monitoring

### Check if Temporal is Alive
```bash
# Direct (only works from VPS localhost — port 5100 not exposed externally)
ssh root@31.97.6.30 "curl -s http://localhost:5100/"

# Via SSH wrapper (phone-friendly)
ssh root@31.97.6.30 "curl -s http://localhost:5100/pulse" | python3 -m json.tool
```

⚠ **Port 5100 is NOT publicly accessible.** All API calls must go through SSH. This is by design — the brain API is internal.

### Check Worker Status (on VPS)
```bash
ssh root@31.97.6.30 "ps aux | grep 'temporal_brain\|sop' | grep python | grep -v grep"
```

### Check Temporal Server (on VPS)
```bash
ssh root@31.97.6.30 "temporal workflow list"
ssh root@31.97.6.30 "temporal schedule list"
```

---

## 🚢 Temporal Fleet (SOP Workers)

Beyond the brain, the VPS runs a Temporal Fleet with SOP (Standard Operating Procedure) workers:

| Worker | Queue | Status |
|--------|-------|--------|
| **SOP-001** | (fleet queue) | ✅ Running (Jul 25) |
| **SOP-002** | (fleet queue) | ✅ Running (Jul 25) |
| **SOP-003** | (fleet queue) | ✅ Running (Jul 25) — OrderStatusWorkflow |

**Active workflows**: `OrderStatusWorkflow` (×2, running 2+ weeks — may need investigation)

### Fleet Operations
```bash
# Check fleet status
ssh root@31.97.6.30 "ps aux | grep sop | grep python | grep -v grep"

# View fleet workflows
ssh root@31.97.6.30 "temporal workflow list | grep -E 'sop|Order|Fleet'"

# Check fleet logs
ssh root@31.97.6.30 "tail -20 /tmp/sop001_v3.log"
ssh root@31.97.6.30 "tail -20 /tmp/sop002_v3.log"
ssh root@31.97.6.30 "tail -20 /tmp/sop003_v3.log"
```

## ⚠ VPS Path Awareness

**This skill runs on VPS (31.97.6.30).** Temporal server and worker are VPS-only. The phone calls via SSH (no public HTTP — port 5100 is localhost-only). If Temporal is unreachable:
1. Check VPS is up: `ping 31.97.6.30`
2. Check port 5100: `curl -s --connect-timeout 5 http://31.97.6.30:5100/health`
3. Escalate to user if down > 5 minutes

**Local (Termux)**: `temporalio` Python package NOT installed (ModuleNotFoundError). All Temporal operations must go through the HTTP API to the VPS.

---

## 🧠 Local LLM — Bonsai (Ollama)

The temporal brain can optionally use the local **Bonsai-8B** model for lightweight processing before or alongside the VPS pipeline. This provides an always-available local brain that doesn't require the VPS to be up.

### Bonsai Specs
| Field | Value |
|-------|-------|
| **Model ID** | `bonsai-8b-q1_0:latest` |
| **Provider** | Ollama (local, port 11434) |
| **Family** | Qwen3 |
| **Params** | 8.2B |
| **Quantization** | Q1_0 (ultra-light) |
| **Context** | 65,536 tokens |
| **Size** | ~1.1 GB |
| **Capabilities** | Completion |

### Calling Bonsai from Termux
```bash
# Quick completion
curl -s http://127.0.0.1:11434/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"bonsai-8b-q1_0:latest","prompt":"Analyze this: ","max_tokens":200}'

# Chat-style
curl -s http://127.0.0.1:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"bonsai-8b-q1_0:latest","messages":[{"role":"user","content":"Summarize the brain pulse state"}]}'
```

### Bonsai + Temporal Hybrid Pipeline
```
Query → Bonsai (local pre-process) → Temporal Brain (VPS) → Response
         └─ Quick filter/triage       └─ Durable execution
```

Use Bonsai for:
- **Pre-filtering**: Run initial quality/liver checks locally before sending to VPS
- **Quick classification**: Classify query type, urgency, routing
- **VPS-down fallback**: Lightweight processing when VPS is unreachable
- **Summarization**: Summarize temporal workflow results locally

### Python Wrapper (Bonsai)
```python
import urllib.request, json

def bonsai_complete(prompt: str, max_tokens: int = 256) -> str:
    """Call local Bonsai model for quick completions."""
    data = json.dumps({
        "model": "bonsai-8b-q1_0:latest",
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": 0.7
    }).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:11434/v1/completions",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())
        return result["choices"][0]["text"]

def bonsai_chat(messages: list, max_tokens: int = 512) -> str:
    """Chat completion with Bonsai."""
    data = json.dumps({
        "model": "bonsai-8b-q1_0:latest",
        "messages": messages,
        "max_tokens": max_tokens
    }).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:11434/v1/chat/completions",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())
        return result["choices"][0]["message"]["content"]
```

### Health Check (Bonsai)
```bash
curl -s http://127.0.0.1:11434/api/tags | python3 -c "import sys,json; models=[m['name'] for m in json.load(sys.stdin)['models']]; print('Bonsai OK' if any('bonsai' in m for m in models) else 'Bonsai MISSING')"
```

## 🔗 Integration Points

| System | How It Connects |
|--------|----------------|
| **Bonsai (Local LLM)** | Pre-filter, classify, fallback processing via Ollama :11434 |
| **Master Schedule** | Temporal cron schedules execute scheduled tasks |
| **Startup Cadence** | `temporal_pulse()` in status probe step |
| **Aave** | Custom AaveHealthWorkflow for daily position checks |
| **DepotChaos** | Custom CRM sync workflow |
| **Browser Automation** | Trigger competitor scans via Temporal |
| **Live Dashboard** | Tracks temporal_brain.pid and bonsai status |

---

## 🚨 Alerts

| Trigger | Action |
|---------|--------|
| HTTP API returns non-200 | Check VPS, check worker process |
| Pulse shows `signal_quality < 0.3` | Brain may be degraded — investigate |
| Worker not running | SSH to VPS, restart: `python3 temporal_brain_v3.py worker` |
| Temporal server down | SSH to VPS, `systemctl restart temporal` |

---

## Aliases

```
brain pulse   → GET /pulse
brain process → POST /process
brain init    → GET /init
brain health  → GET /health
temporal      → This skill
```

## Usage

Load this skill whenever durable workflow execution is needed — scheduled tasks, retry-guaranteed operations, or brain processing. All operations route through the VPS HTTP API. The phone calls; the VPS executes; Temporal guarantees it completes.


## 🖥 Local Brain CLI (`local_brain.py`)

A local processing script that runs Bonsai on-device as the first brain layer. Lives at:
```
~/aios_features/skills/vps/temporal-brain/local_brain.py
```

### Commands
```bash
# Single query
python3 local_brain.py "what's the sentiment on BTC right now?"

# Pipe input
echo "summarize my aave positions" | python3 local_brain.py

# Health check
python3 local_brain.py --pulse

# Watch mode (continuous stdin processing)
python3 local_brain.py --watch

# JSON output for programmatic use
python3 local_brain.py "query" --json

# Skip VPS (local-only processing)
python3 local_brain.py "query" --no-vps
```

### Data Flow
```
Input → Bonsai (local, 8.2B Q1_0) → VPS Temporal Brain (durable storage)
         └─ 128 tokens max          └─ 6-organ pipeline
```

## Usage

Load this skill when the task involves durable workflow orchestration via temporal.io on vps (31.97.6.30:7233). execute, schedule, and monitor workflows for brain processing, scheduled tasks, and the master schedule. three brain workflows (init/pulse/process) + custom workflow creation..

---
*Generated by Skill Factory — 2026-08-10T01:44:13.567Z*
