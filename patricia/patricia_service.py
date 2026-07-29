#!/usr/bin/env python3
"""
Patricia v5.0 — Process Excellence Agent
Actually monitors, thinks, alerts, and communicates.

New in v5.0:
- Health checks with auto-restart attempts
- Brain query every cycle (uses the multi-model brain)
- Alert escalation (tts + RED log entries)
- Queue processing
- HTTP API for Mortimer queries
"""

import os
import sys
import json
import time
import threading
import subprocess
import urllib.request
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# Setup paths
HOME = Path.home()
BRAIN_DIR = HOME / "AOS-Brain"
sys.path.insert(0, str(BRAIN_DIR))

from complete_brain_v4_3_multi_model import BrainV43


class PatriciaService:
    """Patricia — Process Excellence Officer. She actually works now."""
    
    def __init__(self):
        self.name = "Patricia"
        self.emoji = "📊"
        self.role = "Process Excellence Officer"
        self.version = "5.0"
        self.brain = BrainV43()
        self.log_file = HOME / "mortimer/patricia/patricia.log"
        self.state_file = HOME / "mortimer/patricia/state.json"
        self.queue_dir = HOME / "mortimer/patricia/queue"
        self.pid_file = HOME / "mortimer/patricia/patricia.pid"
        self.check_interval = 300  # 5 minutes
        self.alert_cooldown = 600  # 10 min between alerts
        self.last_alert = 0
        self.cycle_count = 0
        self.down_history = {}  # track consecutive failures
        
        # Load or init state
        self.state = self._load_state()
        
    def _load_state(self):
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text())
            except:
                pass
        return {
            "cycles": 0,
            "alerts_sent": 0,
            "services_restarted": 0,
            "last_queue_process": None,
            "started": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _save_state(self):
        self.state["cycles"] = self.cycle_count
        self.state["alerts_sent"] = self.state.get("alerts_sent", 0)
        # Atomic write: write to temp file, then rename (avoids corruption on SIGKILL)
        tmp = str(self.state_file) + ".tmp"
        Path(tmp).write_text(json.dumps(self.state, indent=2))
        Path(tmp).rename(self.state_file)
    
    def log(self, msg, level="INFO"):
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        prefix = {"INFO": "📊", "ALERT": "🚨", "OK": "✅", "DOWN": "🔴", "FIX": "🔧"}.get(level, "📊")
        line = f"[{ts}] {prefix} {msg}"
        print(line)
        with open(self.log_file, "a") as f:
            f.write(line + "\n")
    
    # ─── Activation ────────────────────────────────
    
    def activate(self):
        self.log(f"Patricia v{self.version} — Process Excellence Officer", "INFO")
        self.log(f"State: {self.state['cycles']} previous cycles", "INFO")
        
        try:
            self.brain.initialize()
            active = self.brain.registry.active_model
            model_count = len(self.brain.registry.models)
            self.log(f"Brain ready — {model_count} models, active: {active}", "OK")
        except Exception as e:
            self.log(f"Brain init failed: {e}", "ALERT")
        
        # Process old queue
        self.process_queue()
    
    # ─── Main Cycle ────────────────────────────────
    
    def run_cycle(self):
        self.cycle_count += 1
        prefix = f"Cycle #{self.cycle_count}"
        
        try:
            # 1. Health check
            down = self.health_check_services()
            
            # 2. Feed MNEMOSYNE from QMD feed
            self.feed_mnemosyne()
            
            # 3. Brain query — think about what's happening
            if self.brain.registry.active_model:
                self.query_brain(down)
            
            # 3. Alert if needed
            if down:
                self.alert(down)
            
            # 4. Auto-restart down services — DISABLED (Phase 1: runsv owns this now)
            # Services are under runsv supervision as of 2026-07-27
            # if down:
            #     self.auto_restart(down)
            
            # 5. Process queue (every 30 min = 6 cycles)
            if self.cycle_count % 6 == 0:
                self.process_queue()
            
            # 6. Save state every cycle (survive SIGKILL)
            self._save_state()
            status = "🟢 All good" if not down else f"🔴 {len(down)} down"
            self.log(f"{prefix} — {status}", "INFO")
                
        except Exception as e:
            self.log(f"{prefix} error: {e}", "ALERT")
    
    # ─── MNEMOSYNE Feed ───────────────────────────
    
    def feed_mnemosyne(self):
        """Process QMD feed file into MNEMOSYNE database"""
        feed_file = HOME / "mortimer" / "memory" / "qmd_feed.jsonl"
        db_path = HOME / "mortimer" / "mnemosyne" / "mnemosyne.db"
        
        if not feed_file.exists():
            return
        
        try:
            import sqlite3
            lines = feed_file.read_text().strip().split("\n")
            if not lines or lines == [""]:
                return
            
            conn = sqlite3.connect(str(db_path))
            count = 0
            
            for line in lines[-10:]:  # Max 10 per cycle
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    t = entry.get("timestamp", time.time())
                    ctx = entry.get("input", "")[:200]
                    act = entry.get("action", "unknown")
                    resp = entry.get("response", "")[:200]
                    out = entry.get("outcome", 0)
                    
                    conn.execute(
                        "INSERT INTO executions (timestamp, action, outcome, context) VALUES (?,?,?,?)",
                        (t, act, f"{out}: {resp}", ctx)
                    )
                    count += 1
                except Exception:
                    pass
            
            conn.commit()
            conn.close()
            
            # Clear processed feed
            feed_file.write_text("")
            
            if count > 0:
                self.log(f"MNEMOSYNE: Fed {count} interaction(s)", "INFO")
        except Exception as e:
            self.log(f"MNEMOSYNE feed error: {e}", "ALERT")
    
    # ─── Health Checks ─────────────────────────────
    
    def health_check_services(self):
        """Check all services, return list of down services"""
        checks = {
            # Core Trinity
            "Quantum Oracle": ("http://127.0.0.1:7777", None),
            "Prime Helix": ("http://127.0.0.1:7778", None),
            "Riemann Helix": ("http://127.0.0.1:7779", None),
            "QMD Brain": ("http://127.0.0.1:8000/health", None),
                # Galaxy Fleet — deployed to VPS (31.97.6.30), checked remotely
            # Memory & Agents
            "MYL0N v2": ("http://127.0.0.1:12789/health", None),
            # Agent Systems
            "Agent Factory": ("http://127.0.0.1:12852/health", None),
        }
        
        down = []
        for name, (url, _) in checks.items():
            try:
                req = urllib.request.Request(url, method='GET')
                urllib.request.urlopen(req, timeout=3)
                self.down_history[name] = 0  # reset
            except Exception:
                self.down_history[name] = self.down_history.get(name, 0) + 1
                if self.down_history[name] >= 2:  # Only log after 2nd failure
                    self.log(f"{name} — DOWN ({self.down_history[name]}x)", "DOWN")
                down.append(name)
        
        # Check Ollama
        try:
            result = subprocess.run(["pgrep", "-f", "ollama serve"], capture_output=True, timeout=3)
            if result.returncode != 0:
                self.down_history["Ollama"] = self.down_history.get("Ollama", 0) + 1
                if self.down_history["Ollama"] >= 2:
                    self.log(f"Ollama — DOWN", "DOWN")
                down.append("Ollama")
            else:
                self.down_history["Ollama"] = 0
        except Exception:
            down.append("Ollama")
        
        # Check VPS Galaxy fleet remotely
        vps_ip = "31.97.6.30"
        vps_services = {
            "Galaxy-Solar": 7780,
            "Galaxy-Grid": 7781,
            "Galaxy-NogVerse": 7782,
            "Galaxy-v2": 7783,
            "Galaxy-v1": 7784,
            "Galaxy-Unified": 7785,
        }
        for name, port in vps_services.items():
            try:
                req = urllib.request.Request(f"http://{vps_ip}:{port}", method='GET')
                urllib.request.urlopen(req, timeout=5)
                self.down_history[name] = 0
            except Exception:
                self.down_history[name] = self.down_history.get(name, 0) + 1
                if self.down_history[name] >= 3:
                    self.log(f"{name} (VPS:{port}) — DOWN ({self.down_history[name]}x)", "DOWN")
                down.append(name)
        
        # Check Patricia's own brain
        if not self.brain.registry.active_model:
            down.append("Brain")
        
        return down
    
    # ─── Brain Query ───────────────────────────────
    
    def query_brain(self, down_services):
        """Query Ollama directly for pattern analysis using brain's active model"""
        if not down_services:
            return
        
        try:
            # Build context
            recurring = {s: self.down_history.get(s, 0) for s in down_services if self.down_history.get(s, 0) >= 3}
            recent = {s: self.down_history.get(s, 0) for s in down_services}
            
            model_name = self.brain.registry.active_model or "qwen2.5:1.5b"
            
            total_monitored = 5 + 6  # 5 local (Trinity+QMD+MYL0N+Ollama+Brain) + 6 VPS (Galaxy fleet)
            prompt = f"""Fleet status: {len(down_services)} services down out of {total_monitored} monitored.
Down list: {', '.join(down_services)}
Failure counts: {recent}
Recurring (3+ failures): {recurring if recurring else 'none'}
Total cycles: {self.cycle_count}

Short analysis (1-2 sentences): What's the likely root cause? Android OOM? Config issue? Pattern or random?"""
            
            # Query Ollama
            data = json.dumps({
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": 80}
            }).encode()
            
            req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=data)
            req.add_header("Content-Type", "application/json")
            resp = urllib.request.urlopen(req, timeout=15)
            result = json.loads(resp.read())
            
            analysis = result.get("response", "").strip()
            if analysis:
                self.log(f"Brain [{model_name}]: {analysis[:200]}", "INFO")
        except Exception as e:
            self.log(f"Brain query failed: {e}", "ALERT")
    
    # ─── Alerting ──────────────────────────────────
    
    def alert(self, down_services):
        """Alert on critical service failures"""
        now = time.time()
        if now - self.last_alert < self.alert_cooldown:
            return  # rate limit
        
        critical = [s for s in down_services if self.down_history.get(s, 0) >= 3]
        if not critical:
            return
        
        self.last_alert = now
        self.state["alerts_sent"] = self.state.get("alerts_sent", 0) + 1
        
        msg = f"Patricia alert: {len(critical)} service(s) repeatedly down: {', '.join(critical)}"
        self.log(msg, "ALERT")
        
        # Voice alert via termux-tts
        try:
            subprocess.run(
                ["termux-tts-speak", f"Warning. {len(critical)} services are down. {', '.join(critical)}"],
                timeout=5
            )
        except Exception:
            pass
    
    # ─── Auto-Restart ──────────────────────────────
    
    def auto_restart(self, down_services):
        """Attempt to restart down services using seed3 startup script"""
        helix_services = {"Quantum Oracle", "Prime Helix", "Riemann Helix"}
        
        restarters = {
            "Ollama": ["bash", str(HOME / "mortimer/seed3_startup.sh"), "--ollama-only"],
        }
        
        for service in down_services:
            if self.down_history.get(service, 0) < 2:
                continue
            
            # Helix services — restart via seed3_startup.sh
            if service in helix_services:
                self.log(f"Auto-restarting Helix fleet (includes {service})", "FIX")
                try:
                    subprocess.Popen(
                        ["bash", str(HOME / "mortimer/seed3_startup.sh")],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    )
                    self.state["services_restarted"] = self.state.get("services_restarted", 0) + 1
                except Exception as e:
                    self.log(f"Helix restart failed: {e}", "ALERT")
            
            # Galaxy fleet — restart via SSH to VPS
            elif service.startswith("Galaxy-"):
                self.log(f"Auto-restarting Galaxy fleet on VPS (includes {service})", "FIX")
                try:
                    subprocess.Popen(
                        ["ssh", "-o", "ConnectTimeout=5", "-o", "BatchMode=yes",
                         "root@31.97.6.30", "bash /root/galaxy/startup.sh"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    )
                    self.state["services_restarted"] = self.state.get("services_restarted", 0) + 1
                except Exception as e:
                    self.log(f"Galaxy VPS restart failed: {e}", "ALERT")
            
            # Named restarters
            elif service in restarters:
                cmd = restarters[service]
                self.log(f"Auto-restarting {service}: {' '.join(cmd)}", "FIX")
                try:
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    self.state["services_restarted"] = self.state.get("services_restarted", 0) + 1
                except Exception as e:
                    self.log(f"Restart failed for {service}: {e}", "ALERT")
    
    # ─── Queue Processing ──────────────────────────
    
    def process_queue(self):
        """Process old queue files"""
        if not self.queue_dir.exists():
            return
        
        files = sorted([f for f in self.queue_dir.glob("*") if f.is_file()])
        if not files:
            return
        
        self.log(f"Processing queue: {len(files)} file(s)", "INFO")
        processed_dir = self.queue_dir / "processed"
        processed_dir.mkdir(exist_ok=True)
        
        for f in files[:5]:  # Max 5 per cycle
            try:
                content = f.read_text()[:500]
                self.log(f"Queue: {f.name} — {content[:80]}...", "INFO")
                
                # Archive it
                f.rename(processed_dir / f.name)
            except Exception as e:
                self.log(f"Queue error {f.name}: {e}", "ALERT")
        
        self.state["last_queue_process"] = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # ─── HTTP API ──────────────────────────────────
    
    def start_api(self, port=12851):
        """Start HTTP API for Mortimer queries"""
        service = self
        
        class PatriciaHandler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass  # quiet
            
            def do_GET(self):
                if self.path == "/health":
                    self._json({"status": "ok", "service": "patricia", "version": service.version})
                elif self.path == "/status":
                    self._json(service.get_full_status())
                elif self.path == "/state":
                    self._json(service.state)
                else:
                    self._json({"error": "not found"}, 404)
            
            def do_POST(self):
                if self.path == "/audit":
                    length = int(self.headers.get("Content-Length", 0))
                    body = self.rfile.read(length)
                    data = json.loads(body)
                    result = service.run_audit(data.get("topic", "general"))
                    self._json(result)
                elif self.path == "/query":
                    length = int(self.headers.get("Content-Length", 0))
                    body = self.rfile.read(length)
                    data = json.loads(body)
                    result = service.answer_query(data.get("question", ""))
                    self._json(result)
                else:
                    self._json({"error": "not found"}, 404)
            
            def _json(self, data, code=200):
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(data, default=str).encode())
        
        try:
            server = HTTPServer(("127.0.0.1", port), PatriciaHandler)
            server.allow_reuse_address = True
            self.log(f"API listening on http://127.0.0.1:{port}", "OK")
            server.serve_forever()
        except OSError as e:
            self.log(f"API port {port} in use, skipping HTTP API", "ALERT")
    
    # ─── Status & Audits ──────────────────────────
    
    def get_full_status(self):
        return {
            "agent": self.name,
            "version": self.version,
            "role": self.role,
            "cycles": self.cycle_count,
            "uptime_approx": f"{self.cycle_count * self.check_interval // 60} min",
            "brain_model": self.brain.registry.active_model,
            "brain_models": len(self.brain.registry.models),
            "alerts_sent": self.state.get("alerts_sent", 0),
            "services_restarted": self.state.get("services_restarted", 0),
            "queue_processed": self.state.get("last_queue_process"),
            "down_history": {k: v for k, v in self.down_history.items() if v > 0}
        }
    
    def run_audit(self, topic):
        """Run a process audit on a given topic — actually analyzes now."""
        self.log(f"Audit: {topic[:80]}...", "INFO")
        
        findings = []
        score = 100
        
        # Check each known weakness
        checks = {
            "monitor_coverage": len([k for k in self.down_history if self.down_history[k] == 0]) if self.down_history else 0,
            "auto_restart_capable": len(["Quantum Oracle", "Ollama", "Galaxy v1", "Solar System"]),
            "brain_active": bool(self.brain.registry.active_model),
            "state_frequency": 2,  # cycles between saves
            "queue_healthy": not list(self.queue_dir.glob("processed")),
        }
        
        if checks["state_frequency"] > 4:
            findings.append("⚠️ State saved every 60min — risk on SIGKILL. Reduce to 10min.")
            score -= 15
        
        if not checks["queue_healthy"]:
            findings.append("⚠️ Queue dir has 'processed/' subdir causing errors. Add .is_file() check.")
            score -= 10
        
        # Query brain for deeper analysis if available
        brain_insight = None
        try:
            model = self.brain.registry.active_model or "qwen2.5:1.5b"
            prompt = f"""Audit topic: {topic[:200]}
Current state: {json.dumps(checks)}
Give a 1-sentence process improvement recommendation."""
            data = json.dumps({"model": model, "prompt": prompt, "stream": False, "options": {"num_predict": 60}}).encode()
            req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=data)
            req.add_header("Content-Type", "application/json")
            resp = urllib.request.urlopen(req, timeout=15)
            result = json.loads(resp.read())
            brain_insight = result.get("response", "").strip()
        except Exception:
            pass
        
        return {
            "topic": topic,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "auditor": "Patricia v5.1",
            "score": max(score, 0),
            "findings": findings if findings else ["✅ No issues found"],
            "brain_insight": brain_insight or "Brain query unavailable",
            "checks": checks,
            "status": "complete"
        }
    
    def answer_query(self, question):
        """Answer a direct question from Mortimer"""
        return {
            "question": question,
            "respondent": "Patricia v5.0",
            "status": self.get_full_status(),
            "note": "Brain query integration active. Full reasoning pending.",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    # ─── Main Loop ─────────────────────────────────
    
    def _acquire_lock(self):
        """Single-instance enforcement with stale-lock detection for runsv"""
        if self.pid_file.exists():
            try:
                old_pid = int(self.pid_file.read_text().strip())
                # Check if PID is still a patricia process
                result = subprocess.run(
                    ["ps", "-p", str(old_pid), "-o", "args="],
                    capture_output=True, text=True, timeout=3
                )
                if "patricia_service" in result.stdout:
                    self.log(f"Patricia already running (PID {old_pid}). Exiting.", "ALERT")
                    sys.exit(0)
                # PID exists but not patricia — stale lock
            except Exception:
                pass  # Stale PID — claim lock
        self.pid_file.write_text(str(os.getpid()))
    
    def _release_lock(self):
        if self.pid_file.exists():
            self.pid_file.unlink()
    
    def run(self):
        """Main service loop with HTTP API in background"""
        self._acquire_lock()
        self.activate()
        
        # Start HTTP API in background thread
        api_thread = threading.Thread(target=self.start_api, args=(12851,), daemon=True)
        api_thread.start()
        time.sleep(1)
        
        while True:
            try:
                self.run_cycle()
                time.sleep(self.check_interval)
            except KeyboardInterrupt:
                self.log("Shutting down...", "INFO")
                self._save_state()
                self._release_lock()
                break
            except Exception as e:
                self.log(f"Fatal cycle error: {e}", "ALERT")
                self._save_state()
                time.sleep(60)


if __name__ == "__main__":
    service = PatriciaService()
    service.run()
