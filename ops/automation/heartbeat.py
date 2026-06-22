#!/usr/bin/env python3
"""
💓 SEED3 HEARTBEAT
Automated pulse check for all services
Runs every 5 minutes via automation
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime
from pathlib import Path

HOME = Path.home()
AUTOMATION_DIR = HOME / "mortimer" / "ops" / "automation"
AUTOMATION_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = AUTOMATION_DIR / "ship_state.json"
PULSE_LOG = AUTOMATION_DIR / "heartbeat_log.json"

SERVICES = [
    ("Quantum Oracle", 7777),
    ("Prime Helix", 7778),
    ("Riemann Helix", 7779),
    ("Sales v1", 3333),
    ("Sales v2", 3334),
    ("Ollama", 11434),
    ("QMD", 8000),
]

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"[{ts}] {msg}")

def check_port(port):
    try:
        result = subprocess.run(
            f"curl -s -o /dev/null -w '%{{http_code}}' http://127.0.0.1:{port}/",
            shell=True, capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() == "200"
    except:
        return False

def check_process(name):
    result = subprocess.run(
        f"pgrep -x {name} > /dev/null && echo YES || echo NO",
        shell=True, capture_output=True, text=True
    )
    return result.stdout.strip() == "YES"

def pulse():
    """Send heartbeat pulse"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "services": {}
    }
    
    all_healthy = True
    
    for name, port in SERVICES:
        if port:
            healthy = check_port(port)
        else:
            healthy = check_process(name.lower())
        
        results["services"][name] = healthy
        icon = "✅" if healthy else "❌"
        log(f"{icon} {name}")
        
        if not healthy:
            all_healthy = False
    
    # Check critical processes
    for proc in ["nginx", "ollama"]:
        healthy = check_process(proc)
        results["services"][proc] = healthy
        icon = "✅" if healthy else "❌"
        log(f"{icon} {proc}")
        if not healthy:
            all_healthy = False
    
    # Save pulse log
    if PULSE_LOG.exists():
        with open(PULSE_LOG) as f:
            pulses = json.load(f)
    else:
        pulses = []
    
    pulses.append(results)
    pulses = pulses[-100:]  # Keep last 100
    
    with open(PULSE_LOG, "w") as f:
        json.dump(pulses, f, indent=2)
    
    # Update state
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            state = json.load(f)
    else:
        state = {}
    
    state["last_pulse"] = datetime.now().isoformat()
    state["all_healthy"] = all_healthy
    
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
    
    return all_healthy

if __name__ == "__main__":
    healthy = pulse()
    log(f"Pulse complete - All healthy: {healthy}")
    sys.exit(0 if healthy else 1)
