#!/usr/bin/env python3
"""
AGENT FACTORY v1.0 — Real Spawn Engine
Deployed: 2026-07-25 — Built from RiP verdict (KILL template → REBUILD real)

Endpoints:
  GET  /health          — Service status
  GET  /agents          — Full agent roster
  GET  /agents/{name}   — Single agent info
  POST /spawn           — Create & assign task to agent
  GET  /tasks           — All tasks (filter: ?status=pending|active|completed|failed)
  GET  /tasks/{agent}   — Tasks for specific agent
  POST /tasks/{id}/complete — Mark task complete with result
  POST /tasks/{id}/fail     — Mark task failed with reason
"""

import os
import json
import time
import uuid
import threading
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

HOME = Path.home()
FACTORY_DIR = HOME / "mortimer" / "agent_factory"
AGENTS_DIR = HOME / "agents"
TASKS_DIR = AGENTS_DIR / "tasks"
QUEUE_DIR = TASKS_DIR / "queue"
COMPLETED_DIR = TASKS_DIR / "completed"
FAILED_DIR = TASKS_DIR / "failed"
ROSTER_FILE = HOME / "mortimer" / "crew_roster.md"
PORT = 12852
LOG_FILE = FACTORY_DIR / "factory.log"

# Ensure directories
for d in [FACTORY_DIR, QUEUE_DIR, COMPLETED_DIR, FAILED_DIR]:
    d.mkdir(parents=True, exist_ok=True)


class AgentFactory:
    """Real Agent Factory — spawns, tracks, manages agent tasks."""
    
    def __init__(self):
        self.version = "1.0"
        self.started = time.time()
        self.tasks_spawned = 0
        self.tasks_completed = 0
        self.tasks_failed = 0
        self._load_state()
        self._parse_roster()
        
    def log(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] 🏭 {msg}"
        print(line)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    
    def _load_state(self):
        sf = FACTORY_DIR / "state.json"
        if sf.exists():
            try:
                d = json.loads(sf.read_text())
                self.tasks_spawned = d.get("tasks_spawned", 0)
                self.tasks_completed = d.get("tasks_completed", 0)
                self.tasks_failed = d.get("tasks_failed", 0)
            except:
                pass
    
    def _save_state(self):
        (FACTORY_DIR / "state.json").write_text(json.dumps({
            "tasks_spawned": self.tasks_spawned,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "last_updated": datetime.now().isoformat()
        }, indent=2))
    
    def _parse_roster(self):
        """Parse crew_roster.md into agent list — TRUTH-PASSED v2.0
        Only registers agents with backend scripts. Skips services, games, hardware."""
        self.agents = {}
        if not ROSTER_FILE.exists():
            self.log("WARNING: crew_roster.md not found")
            return
        
        content = ROSTER_FILE.read_text()
        current_division = "Uncategorized"
        skip_section = False
        
        # Sections to skip (reclassified as NOT agents)
        SKIP_SECTIONS = [
            "games", "hardware", "seed3 services", "fleet totals",
            "not agents", "projects, not agents", "concepts, not agents"
        ]
        # Known non-agent names to never register
        SKIP_NAMES = {
            "total fleet", "quantum oracle", "prime helix", "riemann helix",
            "qmd brain", "ollama", "name", "---", "category", "service"
        }
        
        for line in content.split("\n"):
            line = line.strip()
            
            # Track division headers — check if we should skip this section
            if line.startswith("## "):
                division = line.replace("## ", "").strip().lower()
                skip_section = any(s in division for s in SKIP_SECTIONS)
                current_division = division
                continue
            
            if skip_section:
                continue
            
            # Parse table rows: supports old and new (truth-passed) formats
            if line.startswith("| **") and "|" in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) < 3:
                    continue
                    
                name = parts[1].replace("**", "").strip().lower()
                
                # Skip non-agent names
                if name in SKIP_NAMES:
                    continue
                    
                role = parts[2].strip() if len(parts) > 2 else ""
                status = parts[3].strip() if len(parts) > 3 else "🟢"
                
                # Normalize name for sandbox lookup (handle hyphens, special cases)
                sandbox_name = name.replace("-", "").replace(" ", "")  # LEDGER-9 → ledger9
                sandbox_candidates = [sandbox_name]
                
                # Multi-word names: try last word ("the great cryptonio" → "cryptonio")
                if " " in name:
                    sandbox_candidates.append(name.split()[-1])
                
                # Special case: Patricia lives in ~/mortimer/patricia/ not ~/agents/
                if name == "patricia":
                    patricia_scripts = list((HOME / "mortimer/patricia").glob("*.py"))
                    has_backend = len(patricia_scripts) > 0
                    has_sandbox = True
                else:
                    has_sandbox = False
                    actual_dir = None
                    for candidate in sandbox_candidates:
                        if (AGENTS_DIR / candidate).exists():
                            has_sandbox = True
                            actual_dir = AGENTS_DIR / candidate
                            break
                    
                    has_backend = False
                    if has_sandbox and actual_dir:
                        scripts = list(actual_dir.glob("*.sh")) + \
                                   list(actual_dir.glob("*.py")) + \
                                   list(actual_dir.glob("*.js"))
                        has_backend = len(scripts) > 0
                        sandbox_name = actual_dir.name  # Use actual dir name for path
                
                # Only register if agent has backend OR is in an active division
                # (truth column check in new roster format: ✅ = operational)
                backend_col = parts[2].strip() if len(parts) > 2 else ""
                deployable_col = parts[4].strip() if len(parts) > 4 else ""
                
                # New format: Backend column = parts[2], Deployable = parts[4]
                # Old format: Role = parts[2], Status = parts[3]
                is_operational = "✅" in backend_col or has_backend
                is_deployable = "🟢" in deployable_col or is_operational
                
                if name:
                    self.agents[name] = {
                        "name": name,
                        "display_name": name.upper(),
                        "role": role,
                        "division": current_division,
                        "status": "active" if is_deployable else "inactive",
                        "has_backend": is_operational,
                        "sandbox": str(actual_dir) if has_sandbox and actual_dir else None
                    }
        
        operational = sum(1 for a in self.agents.values() if a.get("has_backend"))
        self.log(f"Roster parsed: {len(self.agents)} agents ({operational} operational)")
    
    # ─── Task Management ──────────────────────────
    
    def spawn_task(self, agent_name: str, task: str, priority: str = "medium") -> dict:
        """Create a new task for an agent"""
        agent_name = agent_name.lower().strip()
        
        if agent_name not in self.agents:
            return {"ok": False, "error": f"Unknown agent: {agent_name}"}
        
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        task_obj = {
            "id": task_id,
            "agent": agent_name,
            "task": task,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "created_by": "agent-factory",
            "assigned_to": self.agents[agent_name]["display_name"]
        }
        
        # Write to queue
        task_file = QUEUE_DIR / f"{task_id}.json"
        task_file.write_text(json.dumps(task_obj, indent=2))
        
        self.tasks_spawned += 1
        self._save_state()
        
        self.log(f"SPAWNED: {task_id} → {agent_name.upper()} [{priority}] — {task[:80]}")
        
        return {"ok": True, "task": task_obj}
    
    def complete_task(self, task_id: str, result: dict = None) -> dict:
        """Mark a task as completed"""
        task_file = QUEUE_DIR / f"{task_id}.json"
        if not task_file.exists():
            return {"ok": False, "error": f"Task not found: {task_id}"}
        
        task = json.loads(task_file.read_text())
        task["status"] = "completed"
        task["completed_at"] = datetime.now().isoformat()
        task["result"] = result or {}
        
        # Move to completed
        dest = COMPLETED_DIR / f"{task_id}.json"
        dest.write_text(json.dumps(task, indent=2))
        task_file.unlink()
        
        self.tasks_completed += 1
        self._save_state()
        
        self.log(f"COMPLETED: {task_id} → {task['agent'].upper()}")
        return {"ok": True, "task": task}
    
    def fail_task(self, task_id: str, reason: str = "Unknown error") -> dict:
        """Mark a task as failed"""
        task_file = QUEUE_DIR / f"{task_id}.json"
        if not task_file.exists():
            # Check if it was already completed
            completed_file = COMPLETED_DIR / f"{task_id}.json"
            if completed_file.exists():
                return {"ok": False, "error": "Task already completed"}
            return {"ok": False, "error": f"Task not found: {task_id}"}
        
        task = json.loads(task_file.read_text())
        task["status"] = "failed"
        task["failed_at"] = datetime.now().isoformat()
        task["failure_reason"] = reason
        
        dest = FAILED_DIR / f"{task_id}.json"
        dest.write_text(json.dumps(task, indent=2))
        task_file.unlink()
        
        self.tasks_failed += 1
        self._save_state()
        
        self.log(f"FAILED: {task_id} → {task['agent'].upper()} — {reason[:80]}")
        return {"ok": True, "task": task}
    
    def get_tasks(self, agent: str = None, status: str = None) -> list:
        """Get tasks, optionally filtered"""
        tasks = []
        
        # Pending tasks
        for f in sorted(QUEUE_DIR.glob("*.json")):
            try:
                t = json.loads(f.read_text())
                if agent and t.get("agent") != agent: continue
                if status and t.get("status") != status: continue
                tasks.append(t)
            except:
                pass
        
        # Completed tasks
        if not status or status == "completed":
            for f in sorted(COMPLETED_DIR.glob("*.json")):
                try:
                    t = json.loads(f.read_text())
                    if agent and t.get("agent") != agent: continue
                    tasks.append(t)
                except:
                    pass
        
        # Failed tasks
        if not status or status == "failed":
            for f in sorted(FAILED_DIR.glob("*.json")):
                try:
                    t = json.loads(f.read_text())
                    if agent and t.get("agent") != agent: continue
                    tasks.append(t)
                except:
                    pass
        
        return sorted(tasks, key=lambda t: t.get("created_at", ""), reverse=True)
    
    def get_status(self) -> dict:
        """Full factory status"""
        pending = len(list(QUEUE_DIR.glob("*.json")))
        completed = len(list(COMPLETED_DIR.glob("*.json")))
        failed = len(list(FAILED_DIR.glob("*.json")))
        
        divisions = {}
        for agent in self.agents.values():
            div = agent["division"]
            if div not in divisions:
                divisions[div] = 0
            divisions[div] += 1
        
        return {
            "service": "agent-factory",
            "version": self.version,
            "uptime_seconds": int(time.time() - self.started),
            "agents": {
                "total": len(self.agents),
                "by_division": divisions
            },
            "tasks": {
                "pending": pending,
                "completed": completed,
                "failed": failed,
                "total_spawned": self.tasks_spawned,
                "total_completed": self.tasks_completed,
                "total_failed": self.tasks_failed
            }
        }


# ─── HTTP Server ──────────────────────────────────

factory = AgentFactory()

class FactoryHandler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass
    
    def _json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())
    
    def do_GET(self):
        # Split path from query string
        full_path = self.path
        path = full_path.split("?")[0].rstrip("/")
        qs = full_path.split("?")[1] if "?" in full_path else ""
        
        # Parse query params
        params = {}
        for pair in qs.split("&"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                params[k] = v
        
        # Health
        if path == "/health":
            return self._json({"ok": True, "service": "agent-factory", "version": factory.version})
        
        # Full status
        if path == "/status":
            return self._json(factory.get_status())
        
        # Agent roster
        if path == "/agents":
            return self._json({
                "total": len(factory.agents),
                "agents": list(factory.agents.values())
            })
        
        # Single agent
        if path.startswith("/agents/"):
            name = path.split("/agents/")[1].lower()
            agent = factory.agents.get(name)
            if agent:
                return self._json(agent)
            return self._json({"error": "Agent not found"}, 404)
        
        # Tasks for agent
        if path.startswith("/tasks/"):
            agent_or_status = path.split("/tasks/")[1]
            
            # Check if it's an agent name
            if agent_or_status in factory.agents:
                agent_tasks = factory.get_tasks(agent=agent_or_status)
                return self._json({"agent": agent_or_status, "count": len(agent_tasks), "tasks": agent_tasks})
            
            return self._json({"error": f"Unknown agent: {agent_or_status}"}, 404)
        
        # All tasks (with optional ?status= filter)
        if path == "/tasks":
            status = params.get("status")
            
            tasks = factory.get_tasks(status=status)
            return self._json({"count": len(tasks), "tasks": tasks})
        
        return self._json({"error": "not found"}, 404)
    
    def do_POST(self):
        path = self.path.rstrip("/")
        
        # Read body
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(body)
        except:
            return self._json({"ok": False, "error": "Invalid JSON"}, 400)
        
        # Spawn task
        if path == "/spawn":
            agent = data.get("agent")
            task = data.get("task")
            priority = data.get("priority", "medium")
            
            if not agent or not task:
                return self._json({"ok": False, "error": "Missing 'agent' or 'task'"}, 400)
            
            result = factory.spawn_task(agent, task, priority)
            code = 200 if result.get("ok") else 400
            return self._json(result, code)
        
        # Complete task
        if path.startswith("/tasks/") and path.endswith("/complete"):
            task_id = path.split("/tasks/")[1].split("/complete")[0]
            result = factory.complete_task(task_id, data.get("result"))
            return self._json(result)
        
        # Fail task
        if path.startswith("/tasks/") and path.endswith("/fail"):
            task_id = path.split("/tasks/")[1].split("/fail")[0]
            reason = data.get("reason", "Unknown error")
            result = factory.fail_task(task_id, reason)
            return self._json(result)
        
        return self._json({"error": "not found"}, 404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def run():
    factory.log(f"AGENT FACTORY v{factory.version} — Real Spawn Engine")
    factory.log(f"Roster: {len(factory.agents)} agents | Listening on :{PORT}")
    
    server = HTTPServer(("127.0.0.1", PORT), FactoryHandler)
    server.allow_reuse_address = True
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        factory.log("Shutting down...")
        factory._save_state()
        server.shutdown()


if __name__ == "__main__":
    run()
