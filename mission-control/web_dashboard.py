#!/usr/bin/env python3
"""
🎮 Mortimer Mission Control - Web Dashboard
Serves both HTML and /status API
"""

import os
import json
import glob
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

PORT = 8082
HTML_FILE = "/data/data/com.termux/files/home/mortimer/mission-control/dashboard.html"

def get_status():
    status = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "services": {},
        "brain": {},
        "consciousness": {}
    }
    
    # Ollama
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
        lines = [l for l in result.stdout.strip().split("\n") if ":" in l]
        status["services"]["ollama"] = {"status": "ONLINE", "models": len(lines)}
    except:
        status["services"]["ollama"] = {"status": "OFFLINE", "models": 0}
        
    # QMD
    try:
        import urllib.request
        resp = urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=2)
        data = json.loads(resp.read())
        status["services"]["qmd"] = {"status": "ONLINE" if data.get("status") == "ok" else "OFFLINE"}
    except:
        status["services"]["qmd"] = {"status": "OFFLINE"}
        
    # Telegram
    try:
        result = subprocess.run(["pgrep", "-f", "mortimer_telegram"], capture_output=True, text=True)
        status["services"]["telegram"] = {"status": "ONLINE" if result.returncode == 0 else "OFFLINE"}
    except:
        status["services"]["telegram"] = {"status": "ERROR"}
        
    # Patricia
    try:
        result = subprocess.run(["pgrep", "-f", "patricia_service"], capture_output=True, text=True)
        status["services"]["patricia"] = {"status": "ONLINE" if result.returncode == 0 else "OFFLINE"}
    except:
        status["services"]["patricia"] = {"status": "ERROR"}
        
    # Brain
    brain_dir = "/data/data/com.termux/files/home/AOS-Brain/memory"
    mem_files = glob.glob(f"{brain_dir}/*.md")
    status["brain"]["memory_files"] = len(mem_files)
    today = datetime.now().strftime("%Y-%m-%d")
    status["brain"]["today_study"] = os.path.exists(f"{brain_dir}/study-{today}.md")
    
    try:
        with open("/data/data/com.termux/files/home/mortimer/memory/curriculum_progress.json") as f:
            p = json.load(f)
            status["brain"]["curriculum_stage"] = p.get("stage", 0)
            status["brain"]["curriculum_complete"] = p.get("complete", False)
    except:
        status["brain"]["curriculum_stage"] = 0
        status["brain"]["curriculum_complete"] = True
        
    # Consciousness
    status["consciousness"] = {
        "conscious": "10/10",
        "subconscious": "100/100",
        "unconscious": "2000/2000",
        "drives": {"serve_captain": 1.0, "grow_smarter": 0.9, "be_useful": 0.8, "learn_new_things": 0.7}
    }
    
    return status

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status" or self.path == "/status.json":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(get_status()).encode())
        elif self.path == "/" or self.path == "/index" or self.path == "/dashboard":
            self.path = "/dashboard.html"
            SimpleHTTPRequestHandler.do_GET(self)
        else:
            SimpleHTTPRequestHandler.do_GET(self)
    
    def log_message(self, format, *args):
        pass

os.chdir("/data/data/com.termux/files/home/mortimer/mission-control")

server = HTTPServer(("", PORT), Handler)
print(f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🎮 MORTIMER MISSION CONTROL - WEB DASHBOARD           ║
║                                                           ║
║   🌐 http://localhost:{PORT}                              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")
server.serve_forever()
