#!/usr/bin/env python3
"""
🚀 SEED3 AUTOMATION ENGINE
Mortimer's Autonomous Operations Center

This system automates all of SEED3:
- Startup sequence
- Health monitoring
- Auto-recovery
- Daily reporting
- Git sync
- Backup management
"""

import os
import sys
import time
import json
import subprocess
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Callable

# ═══════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════

HOME = Path.home()
OPS_DIR = HOME / "mortimer" / "ops"
AUTOMATION_DIR = OPS_DIR / "automation"
AUTOMATION_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = AUTOMATION_DIR / "ship_state.json"
HEALTH_LOG = AUTOMATION_DIR / "health_log.json"
ALERT_LOG = AUTOMATION_DIR / "alerts.json"

# Service definitions
SERVICES = {
    "qmd": {
        "port": 8000,
        "command": "python3 -u ~/mortimer/services/qmd_service.py",
        "health_check": lambda: check_port(8000),
        "critical": True
    },
    "patricia": {
        "command": "python3 -u ~/mortimer/patricia/patricia_service.py",
        "health_check": lambda: check_process("patricia_service"),
        "critical": False
    },
    "nginx": {
        "command": "nginx",
        "health_check": lambda: check_process("nginx"),
        "critical": True
    },
    "ollama": {
        "port": 11434,
        "command": "ollama serve",
        "health_check": lambda: check_port(11434),
        "critical": True
    },
    "quantum_oracle": {
        "port": 7777,
        "health_check": lambda: check_port(7777),
        "critical": True
    },
    "prime_helix": {
        "port": 7778,
        "health_check": lambda: check_port(7778),
        "critical": True
    },
    "riemann_helix": {
        "port": 7779,
        "health_check": lambda: check_port(7779),
        "critical": True
    },
    "sales_v1": {
        "port": 3333,
        "health_check": lambda: check_port(3333),
        "critical": False
    },
    "sales_v2": {
        "port": 3334,
        "health_check": lambda: check_port(3334),
        "critical": False
    }
}

# ═══════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════

def log(msg: str, level: str = "INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    
    # Append to today's log
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = AUTOMATION_DIR / f"log_{today}.txt"
    with open(log_file, "a") as f:
        f.write(line + "\n")

def cmd(command: str, timeout: int = 30) -> tuple:
    """Run shell command safely"""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True,
            text=True, timeout=timeout, env={**os.environ, "HOME": str(HOME)}
        )
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", 1
    except Exception as e:
        return str(e), 1

def check_port(port: int) -> bool:
    """Check if port is responding"""
    stdout, code = cmd(f"curl -s -o /dev/null -w '%{{http_code}}' http://127.0.0.1:{port}/ 2>/dev/null || echo 'DOWN'")
    return stdout == "200"

def check_process(name: str) -> bool:
    """Check if process is running"""
    stdout, code = cmd(f"pgrep -a {name} 2>/dev/null | grep -q . && echo 'RUNNING' || echo 'STOPPED'")
    return stdout == "RUNNING"

def save_state(state: Dict):
    """Save ship state"""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def load_state() -> Dict:
    """Load ship state"""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "started": None,
        "services": {},
        "last_health_check": None,
        "last_backup": None,
        "last_git_sync": None,
        "uptime_hours": 0
    }

def save_health(health: Dict):
    """Save health log"""
    if HEALTH_LOG.exists():
        with open(HEALTH_LOG) as f:
            data = json.load(f)
    else:
        data = []
    
    data.append(health)
    # Keep last 100 entries
    data = data[-100:]
    
    with open(HEALTH_LOG, "w") as f:
        json.dump(data, f, indent=2)

def send_alert(message: str, severity: str = "WARNING"):
    """Send alert"""
    log(message, severity)
    
    alert = {
        "timestamp": datetime.now().isoformat(),
        "severity": severity,
        "message": message
    }
    
    if ALERT_LOG.exists():
        with open(ALERT_LOG) as f:
            alerts = json.load(f)
    else:
        alerts = []
    
    alerts.append(alert)
    # Keep last 50 alerts
    alerts = alerts[-50:]
    
    with open(ALERT_LOG, "w") as f:
        json.dump(alerts, f, indent=2)

# ═══════════════════════════════════════════════════════════
# STARTUP SEQUENCE
# ═══════════════════════════════════════════════════════════

def startup_sequence():
    """Boot SEED3 - run once on startup"""
    log("🚀 SEED3 STARTUP SEQUENCE INITIATED")
    
    state = load_state()
    state["started"] = datetime.now().isoformat()
    
    # Step 1: Start PulseAudio
    log("Starting PulseAudio...")
    cmd("pulseaudio --start 2>/dev/null || true")
    
    # Step 2: Start nginx
    log("Starting nginx...")
    cmd("nginx -t 2>/dev/null && nginx -s reload 2>/dev/null || nginx")
    
    # Step 3: Start Ollama
    log("Starting Ollama...")
    if not check_process("ollama"):
        cmd("nohup ollama serve > /dev/null 2>&1 &")
        time.sleep(3)
    
    # Step 4: Start QMD
    log("Starting QMD service...")
    if not check_process("qmd"):
        cmd("cd ~/mortimer/services && nohup python3 -u qmd_service.py > qmd.log 2>&1 &")
        time.sleep(2)
    
    # Step 5: Start Patricia
    log("Starting Patricia...")
    if not check_process("patricia"):
        cmd("cd ~/mortimer/patricia && nohup python3 -u patricia_service.py > patricia.log 2>&1 &")
        time.sleep(2)
    
    # Step 6: Verify services
    log("Verifying core services...")
    health = check_all_services()
    
    if health["healthy_count"] >= 3:
        log(f"✅ STARTUP COMPLETE - {health['healthy_count']}/{health['total']} services healthy")
        state["services"] = health["services"]
        save_state(state)
        return True
    else:
        log(f"⚠️ STARTUP COMPLETE - Only {health['healthy_count']}/{health['total']} services healthy", "WARNING")
        return False

# ═══════════════════════════════════════════════════════════
# HEALTH MONITORING
# ═══════════════════════════════════════════════════════════

def check_all_services() -> Dict:
    """Check all services"""
    results = {}
    healthy = 0
    total = len(SERVICES)
    
    for name, config in SERVICES.items():
        try:
            if "health_check" in config:
                is_healthy = config["health_check"]()
            elif "port" in config:
                is_healthy = check_port(config["port"])
            else:
                is_healthy = check_process(name)
            
            results[name] = {
                "healthy": is_healthy,
                "checked": datetime.now().isoformat()
            }
            
            if is_healthy:
                healthy += 1
        except Exception as e:
            results[name] = {
                "healthy": False,
                "error": str(e),
                "checked": datetime.now().isoformat()
            }
    
    return {
        "services": results,
        "healthy_count": healthy,
        "total": total,
        "timestamp": datetime.now().isoformat()
    }

def monitor_loop(interval: int = 60):
    """Continuous health monitoring"""
    log("🎯 HEALTH MONITOR STARTED")
    
    consecutive_failures = {}
    restart_threshold = 3
    
    while True:
        try:
            health = check_all_services()
            save_health(health)
            
            state = load_state()
            state["last_health_check"] = datetime.now().isoformat()
            
            # Check each service
            for name, status in health["services"].items():
                if not status["healthy"]:
                    consecutive_failures[name] = consecutive_failures.get(name, 0) + 1
                    
                    # Critical service down
                    if SERVICES[name].get("critical", False) and consecutive_failures[name] >= restart_threshold:
                        log(f"🔴 CRITICAL: {name} down for {consecutive_failures[name]} checks - RESTARTING", "ERROR")
                        restart_service(name)
                        consecutive_failures[name] = 0
                    elif consecutive_failures[name] == 1:
                        log(f"🟡 WARNING: {name} unhealthy")
                else:
                    consecutive_failures[name] = 0
            
            # Calculate uptime
            if state.get("started"):
                started = datetime.fromisoformat(state["started"])
                state["uptime_hours"] = round((datetime.now() - started).total_seconds() / 3600, 1)
            
            save_state(state)
            
            # Check if we need daily report
            check_daily_report(state)
            
            # Check if we need git sync
            check_git_sync(state)
            
            # Check if we need backup
            check_backup(state)
            
        except Exception as e:
            log(f"Monitor error: {e}", "ERROR")
        
        time.sleep(interval)

def restart_service(name: str):
    """Restart a service"""
    log(f"Restarting {name}...")
    
    if name == "nginx":
        cmd("pkill nginx; sleep 1; nginx")
    elif name == "ollama":
        cmd("pkill ollama; sleep 1; nohup ollama serve > /dev/null 2>&1 &")
    elif name == "qmd":
        cmd("pkill -f qmd_service; sleep 1; cd ~/mortimer/services && nohup python3 -u qmd_service.py > qmd.log 2>&1 &")
    elif name == "patricia":
        cmd("pkill -f patricia_service; sleep 1; cd ~/mortimer/patricia && nohup python3 -u patricia_service.py > patricia.log 2>&1 &")
    
    time.sleep(3)

# ═══════════════════════════════════════════════════════════
# AUTOMATED TASKS
# ═══════════════════════════════════════════════════════════

def check_daily_report(state: Dict):
    """Generate daily report if needed"""
    now = datetime.now()
    
    # Run at 20:00 UTC
    if now.hour == 20 and now.minute < 5:
        last_report = state.get("last_daily_report", "")
        today = now.strftime("%Y-%m-%d")
        
        if last_report != today:
            log("📊 Generating daily report...")
            state["last_daily_report"] = today
            save_state(state)
            
            # Run daily ops
            subprocess.Popen(
                ["python3", f"{HOME}/mortimer/ops/daily_ops.py"],
                stdout=open(AUTOMATION_DIR / "daily_report.log", "a"),
                stderr=subprocess.STDOUT
            )

def check_git_sync(state: Dict):
    """Sync to GitHub if needed"""
    now = datetime.now()
    
    # Sync every 6 hours
    if now.hour in [6, 12, 18, 0]:
        last_sync = state.get("last_git_sync")
        
        if last_sync:
            last = datetime.fromisoformat(last_sync)
            hours_since = (now - last).total_seconds() / 3600
            
            if hours_since >= 6:
                log("🔄 Syncing to GitHub...")
                stdout, code = cmd("cd ~/mortimer && git add -A && git commit -m 'AUTOSAVE' 2>/dev/null && git push 2>/dev/null || true")
                state["last_git_sync"] = now.isoformat()
                save_state(state)

def check_backup(state: Dict):
    """Run backup if needed"""
    now = datetime.now()
    
    # Backup every 4 hours
    last_backup = state.get("last_backup")
    
    if last_backup:
        last = datetime.fromisoformat(last_backup)
        hours_since = (now - last).total_seconds() / 3600
        
        if hours_since >= 4:
            log("💾 Running automated backup...")
            subprocess.Popen(
                ["bash", f"{HOME}/mortimer/auto-backup.sh"],
                stdout=open(AUTOMATION_DIR / "backup.log", "a"),
                stderr=subprocess.STDOUT
            )
            state["last_backup"] = now.isoformat()
            save_state(state)

# ═══════════════════════════════════════════════════════════
# STATUS COMMANDS
# ═══════════════════════════════════════════════════════════

def status_report():
    """Generate current status report"""
    state = load_state()
    health = check_all_services()
    
    print("\n" + "="*60)
    print("🚀 SEED3 STATUS REPORT")
    print("="*60)
    
    if state.get("started"):
        started = datetime.fromisoformat(state["started"])
        uptime = round((datetime.now() - started).total_seconds() / 3600, 1)
        print(f"⏱️  Uptime: {uptime} hours")
    
    print(f"\n📊 Services: {health['healthy_count']}/{health['total']} healthy")
    
    for name, status in health["services"].items():
        icon = "✅" if status["healthy"] else "❌"
        critical = " [CRITICAL]" if SERVICES[name].get("critical") else ""
        print(f"  {icon} {name}{critical}")
    
    print("\n📅 Recent Activity:")
    if state.get("last_health_check"):
        print(f"  Health check: {state['last_health_check'][:19]}")
    if state.get("last_backup"):
        print(f"  Backup: {state['last_backup'][:19]}")
    if state.get("last_git_sync"):
        print(f"  Git sync: {state['last_git_sync'][:19]}")
    
    # Show recent alerts
    if ALERT_LOG.exists():
        with open(ALERT_LOG) as f:
            alerts = json.load(f)
        if alerts:
            print(f"\n🚨 Recent Alerts ({len(alerts)}):")
            for alert in alerts[-3:]:
                print(f"  [{alert['severity']}] {alert['message'][:50]}")
    
    print("="*60)

# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="SEED3 Automation Engine")
    parser.add_argument("action", choices=["start", "monitor", "status", "health", "restart"],
                        help="Action to perform")
    parser.add_argument("--service", help="Service name for restart")
    
    args = parser.parse_args()
    
    if args.action == "start":
        startup_sequence()
    elif args.action == "monitor":
        monitor_loop()
    elif args.action == "status":
        status_report()
    elif args.action == "health":
        health = check_all_services()
        print(json.dumps(health, indent=2))
    elif args.action == "restart" and args.service:
        restart_service(args.service)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
