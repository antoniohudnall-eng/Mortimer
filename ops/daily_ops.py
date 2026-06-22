#!/usr/bin/env python3
"""
🎯 SEED3 DAILY OPERATIONS
Mortimer's automated task execution system
Runs all department tasks automatically
"""

import os
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

# Paths
HOME = Path.home()
OPS_DIR = HOME / "mortimer" / "ops"
LOGS_DIR = OPS_DIR / "daily"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Timestamp
TS = datetime.now().strftime("%Y-%m-%d %H:%M")
TODAY = datetime.now().strftime("%Y-%m-%d")

def log(msg, category="INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{category}] {msg}"
    print(line)
    log_file = LOGS_DIR / f"{TODAY}.log"
    with open(log_file, "a") as f:
        f.write(line + "\n")

def cmd(command, timeout=30):
    """Run shell command safely"""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, 
            text=True, timeout=timeout
        )
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", 1
    except Exception as e:
        return str(e), 1

# ═══════════════════════════════════════════════════════════
# DEPARTMENT OPERATIONS
# ═══════════════════════════════════════════════════════════

def security_ops():
    """SENTINEL - Security Department"""
    log("=== SECURITY OPS ===", "SENTINEL")
    
    # Check fail2ban
    stdout, code = cmd("fail2ban-client status 2>/dev/null | head -5")
    if code == 0 and stdout:
        log(f"fail2ban status: {stdout[:100]}", "SENTINEL")
    
    # Check failed SSH attempts
    stdout, code = cmd("grep 'Failed password' /var/log/auth.log 2>/dev/null | tail -3 | wc -l")
    if code == 0:
        failed = int(stdout.strip()) if stdout.strip().isdigit() else 0
        log(f"Recent failed SSH: {failed}", "SENTINEL")
        if failed > 10:
            log("⚠️ HIGH ALERT: Multiple failed SSH attempts", "SENTINEL")
    
    # Check UFW status
    stdout, code = cmd("ufw status 2>/dev/null | head -3")
    if code == 0:
        log(f"UFW: {stdout}", "SENTINEL")
    
    log("Security check complete", "SENTINEL")

def service_health():
    """SPINDLE - Engineering Department"""
    log("=== SERVICE HEALTH ===", "SPINDLE")
    
    ports = [7777, 7778, 7779, 3333, 3334, 8000, 11434]
    all_healthy = True
    
    # Check QMD on health endpoint
    stdout, code = cmd("curl -s http://127.0.0.1:8000/health 2>/dev/null | grep -q ok && echo '200' || echo '404'")
    status = "✅" if stdout == "200" else "❌"
    log(f"Port 8000 (QMD): {stdout} {status}", "SPINDLE")
    if stdout != "200":
        all_healthy = False
    
    # Check nginx
    stdout, code = cmd("pgrep -a nginx | head -2")
    if code == 0 and stdout:
        log(f"nginx running: PID {stdout.split()[0]}", "SPINDLE")
    else:
        log("⚠️ nginx not running!", "SPINDLE")
        all_healthy = False
    
    # Check ollama
    stdout, code = cmd("pgrep -a ollama | head -1")
    if code == 0 and stdout:
        log(f"Ollama running: {stdout[:50]}", "SPINDLE")
    
    return all_healthy

def finance_check():
    """LEDGER-9 - Finance Department"""
    log("=== FINANCE CHECK ===", "LEDGER-9")
    
    # Check wallet addresses exist (not balances - that needs API)
    wallets = [
        ("EVM", "0x7244d8C20394CC11D54b2583Fb813B3EB8B72f36"),
        ("BTC", "placeholder"),  # Add actual BTC address
    ]
    
    for name, addr in wallets:
        if addr != "placeholder":
            log(f"{name} wallet configured: {addr[:10]}...{addr[-4:]}", "LEDGER-9")
        else:
            log(f"{name} wallet: NEEDS ADDRESS", "LEDGER-9")
    
    # Check for any price data
    stdout, code = cmd("ls ~/mortimer/wallets/ 2>/dev/null | head -5")
    if stdout:
        log(f"Wallet files: {stdout[:100]}", "LEDGER-9")
    
    log("Finance check complete", "LEDGER-9")

def sales_pipeline():
    """PULP/HUME - Sales Department"""
    log("=== SALES PIPELINE ===", "PULP")
    
    # Check dashboard
    stdout, code = cmd("curl -s http://127.0.0.1:3333/ | grep -c 'html' 2>/dev/null || echo 0")
    if code == 0 and stdout == "1":
        log("Sales Dashboard: ✅ Online (port 3333)", "PULP")
    else:
        log("Sales Dashboard: ⚠️ Check status", "PULP")
    
    # Check for new leads
    stdout, code = cmd("ls ~/mortimer/sales-command/data/ 2>/dev/null | wc -l")
    if code == 0:
        files = int(stdout.strip()) if stdout.strip().isdigit() else 0
        log(f"Sales data files: {files}", "PULP")
    
    log("Sales pipeline check complete", "PULP")

def learning_progress():
    """LILLY - Learning Department"""
    log("=== LILLY LEARNING ===", "LILLY")
    
    progress_file = HOME / "mortimer" / "memory" / "lilly_progress.json"
    if progress_file.exists():
        with open(progress_file) as f:
            progress = json.load(f)
        
        books_read = len(progress.get("books_read", []))
        total = progress.get("total_learned", 0)
        log(f"Books read: {books_read}, Total learned: {total}", "LILLY")
        
        # Check curriculum
        catalog = HOME / "AOS-Brain" / "curriculum" / "gutenberg" / "bookshelf_catalog.json"
        if catalog.exists():
            with open(catalog) as f:
                cat = json.load(f)
            total_books = sum(len(v["books"]) for v in cat.get("categories", {}).values())
            log(f"Curriculum total: {total_books} books", "LILLY")
            
            if books_read >= total_books:
                log("🎓 Curriculum complete! Reset needed.", "LILLY")
            else:
                remaining = total_books - books_read
                log(f"📚 {remaining} books remaining", "LILLY")
    else:
        log("No progress file - run LILLY first", "LILLY")
    
    log("Learning progress check complete", "LILLY")

def memory_backup():
    """MORTIMER - General's Duty"""
    log("=== MEMORY BACKUP ===", "MORTIMER")
    
    # Ensure today's memory exists
    mem_file = HOME / "mortimer" / "memory" / f"{TODAY}.md"
    if not mem_file.exists():
        log(f"Creating today's memory file: {TODAY}.md", "MORTIMER")
        with open(mem_file, "w") as f:
            f.write(f"# {TODAY} - Daily Log\n\n")
    
    # Check memory size
    stdout, code = cmd(f"wc -l {mem_file}")
    if code == 0:
        lines = stdout.split()[0] if stdout else "0"
        log(f"Today's memory: {lines} lines", "MORTIMER")
    
    log("Memory backup check complete", "MORTIMER")

def nginx_check():
    """SPINDLE - Engineering (Rule #12)"""
    log("=== NGINX CONFIG ===", "SPINDLE")
    
    conf = "/data/data/com.termux/files/usr/etc/nginx/nginx.conf"
    stdout, code = cmd(f"nginx -t -c {conf} 2>&1")
    if "syntax is ok" in stdout:
        log("nginx config: ✅ Valid", "SPINDLE")
    else:
        log(f"⚠️ nginx config error: {stdout[:100]}", "SPINDLE")
    
    # List servers configured
    stdout, code = cmd(f"grep -E '^    server' {conf}")
    if stdout:
        servers = stdout.count("listen")
        log(f"Servers configured: {servers}", "SPINDLE")
    
    log("Nginx check complete", "SPINDLE")

def daily_summary():
    """Generate end-of-day summary"""
    log("=== DAILY SUMMARY ===", "SUMMARY")
    
    log_file = LOGS_DIR / f"{TODAY}.log"
    if log_file.exists():
        with open(log_file) as f:
            lines = f.readlines()
        
        departments = set()
        for line in lines:
            for dept in ["SENTINEL", "SPINDLE", "LEDGER-9", "PULP", "LILLY", "MORTIMER"]:
                if dept in line:
                    departments.add(dept)
        
        log(f"Departments active today: {', '.join(departments)}", "SUMMARY")
        log(f"Total log entries: {len(lines)}", "SUMMARY")
    
    log("Daily operations complete!", "SUMMARY")
    print("\n" + "="*50)
    print("🎯 SEED3 DAILY OPS COMPLETE")
    print("="*50)

# ═══════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════

def run_daily_ops():
    print("\n" + "="*50)
    print("🎯 SEED3 DAILY OPERATIONS")
    print(f"Started: {TS}")
    print("="*50 + "\n")
    
    log("Starting daily operations")
    
    # Run in order of priority
    security_ops()
    print()
    
    service_health()
    print()
    
    nginx_check()
    print()
    
    finance_check()
    print()
    
    sales_pipeline()
    print()
    
    learning_progress()
    print()
    
    memory_backup()
    print()
    
    daily_summary()
    
    # Save to memory
    save_to_memory()

def save_to_memory():
    """Save ops results to memory file"""
    log_file = LOGS_DIR / f"{TODAY}.log"
    mem_file = HOME / "mortimer" / "memory" / f"{TODAY}.md"
    
    if log_file.exists():
        with open(log_file) as f:
            content = f.read()
        
        # Append to daily memory
        with open(mem_file, "a") as f:
            f.write("\n## SEED3 Daily Ops\n")
            f.write(content)
        
        log(f"Saved ops log to {TODAY}.md")

if __name__ == "__main__":
    run_daily_ops()
