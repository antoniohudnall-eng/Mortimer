#!/usr/bin/env python3
"""
DepotChaos Diagnostic Tool
Checks service health, database connectivity, and common issues
"""

import subprocess
import json
import sqlite3
import sys
import os
import time
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def check(msg, status, details=""):
    """Print check result"""
    icon = "✅" if status else "❌"
    color = Colors.GREEN if status else Colors.RED
    print(f"{color}{icon} {msg}{Colors.RESET}")
    if details:
        print(f"   {Colors.YELLOW}{details}{Colors.RESET}")
    return status

def info(msg):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.RESET}")

def run_checks():
    """Run all diagnostic checks"""
    results = {}
    
    print(f"\n{Colors.BLUE}=== DepotChaos Diagnostic ==={Colors.RESET}\n")
    
    # 1. Service Status
    result = subprocess.run(
        ['systemctl', 'is-active', 'depotchaos'],
        capture_output=True, text=True
    )
    service_active = result.stdout.strip() == 'active'
    results['service'] = check(
        "Systemd Service",
        service_active,
        "Active" if service_active else result.stdout.strip()
    )
    
    # 2. Port Check
    result = subprocess.run(
        ['lsof', '-t', '-i', ':8082'],
        capture_output=True, text=True
    )
    port_listening = result.returncode == 0 and result.stdout.strip()
    results['port'] = check(
        "Port 8082 Listening",
        port_listening,
        f"PID(s): {result.stdout.strip()}" if port_listening else "No process found"
    )
    
    # 3. API Connectivity
    try:
        import urllib.request
        with urllib.request.urlopen(
            'http://localhost:8082/api/stats',
            timeout=5
        ) as resp:
            data = json.loads(resp.read())
            api_working = True
            results['api'] = check(
                "API Endpoint",
                True,
                f"{data.get('total_leads', 0)} leads, {data.get('intelligence_records', 0)} intel records"
            )
    except Exception as e:
        results['api'] = check("API Endpoint", False, str(e))
        data = {}
    
    # 4. Database Connectivity
    try:
        conn = sqlite3.connect('/root/.openclaw/workspace/data/depot_chaos/unified.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM leads WHERE deleted = 0")
        lead_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM datadepot_intelligence")
        intel_count = c.fetchone()[0]
        conn.close()
        results['database'] = check(
            "Database Connection",
            True,
            f"{lead_count} leads, {intel_count} intelligence records"
        )
    except Exception as e:
        results['database'] = check("Database Connection", False, str(e))
    
    # 5. Static Files
    static_dir = Path('/var/www/psdepot.com/depotchaos')
    index_exists = (static_dir / 'index.html').exists()
    results['static'] = check(
        "Web Static Files",
        index_exists,
        f"{static_dir}/index.html exists" if index_exists else "Missing"
    )
    
    # 6. Nginx Configuration (optional)
    try:
        result = subprocess.run(
            ['nginx', '-t'],
            capture_output=True, text=True
        )
        nginx_valid = result.returncode == 0
        results['nginx'] = check(
            "Nginx Configuration",
            nginx_valid,
            "Valid" if nginx_valid else result.stderr.strip()
        )
    except FileNotFoundError:
        results['nginx'] = check("Nginx Configuration", True, "Not installed (optional)")
    
    # 7. Email Queue
    queue_file = Path('/root/.openclaw/workspace/datadepot/queue/pending_emails.json')
    if queue_file.exists():
        try:
            with open(queue_file) as f:
                queue = json.load(f)
            queue_count = len(queue)
            results['queue'] = check(
                "Email Queue",
                True,
                f"{queue_count} pending emails"
            )
        except:
            results['queue'] = check("Email Queue", False, "Corrupted queue file")
    else:
        results['queue'] = check("Email Queue", True, "Empty queue (file not found)")
    
    # Summary
    print(f"\n{Colors.BLUE}=== Summary ==={Colors.RESET}\n")
    all_healthy = all(results.values())
    
    if all_healthy:
        print(f"{Colors.GREEN}✅ All systems operational{Colors.RESET}")
        print(f"\n📊 Current Stats:")
        print(f"   • Leads: {lead_count:,}")
        print(f"   • Intelligence: {intel_count:,}")
        print(f"   • New Today: {data.get('new_today', 0)}")
    else:
        print(f"{Colors.RED}⚠️  Issues detected:{Colors.RESET}")
        for component, status in results.items():
            if not status:
                print(f"   ❌ {component}")
        
        print(f"\n{Colors.YELLOW}Recommended Actions:{Colors.RESET}")
        if not results.get('service'):
            print("   1. systemctl restart depotchaos")
        if not results.get('port'):
            print("   2. sudo kill -9 $(lsof -t -i:8082); systemctl restart depotchaos")
        if not results.get('api'):
            print("   3. Check journalctl -u depotchaos -n 50")
        if not results.get('database'):
            print("   4. Check database integrity: sqlite3 unified.db 'PRAGMA integrity_check;'")
    
    print()
    return 0 if all_healthy else 1

def auto_fix():
    """Attempt automatic fixes"""
    print(f"\n{Colors.BLUE}=== Auto-Fix Mode ==={Colors.RESET}\n")
    
    # Check if port conflict
    result = subprocess.run(
        ['lsof', '-t', '-i', ':8082'],
        capture_output=True, text=True
    )
    
    if result.returncode == 0 and result.stdout.strip():
        pids = result.stdout.strip().split('\n')
        print(f"Found {len(pids)} process(es) on port 8082")
        
        for pid in pids:
            if pid:
                try:
                    subprocess.run(['kill', '-9', pid], check=False)
                    print(f"   Killed PID {pid}")
                except:
                    pass
        
        time.sleep(2)
    
    # Restart service
    print("Restarting depotchaos service...")
    subprocess.run(['systemctl', 'restart', 'depotchaos'], check=False)
    time.sleep(3)
    
    # Verify
    result = subprocess.run(
        ['systemctl', 'is-active', 'depotchaos'],
        capture_output=True, text=True
    )
    
    if result.stdout.strip() == 'active':
        print(f"{Colors.GREEN}✅ Service restarted successfully{Colors.RESET}")
        return 0
    else:
        print(f"{Colors.RED}❌ Service failed to restart{Colors.RESET}")
        return 1

def main():
    import argparse
    parser = argparse.ArgumentParser(description='DepotChaos Diagnostic Tool')
    parser.add_argument('--fix', action='store_true', help='Attempt automatic fixes')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()
    
    if args.fix:
        return auto_fix()
    
    if args.json:
        # JSON output for programmatic use
        result = subprocess.run(
            ['curl', '-s', 'http://localhost:8082/api/stats'],
            capture_output=True, text=True
        )
        try:
            stats = json.loads(result.stdout) if result.returncode == 0 else {}
        except:
            stats = {}
        
        subprocess.run(['systemctl', 'is-active', 'depotchaos'], capture_output=True)
        
        output = {
            'status': 'healthy' if result.returncode == 0 else 'unhealthy',
            'service': 'active' if result.returncode == 0 else 'inactive',
            'stats': stats
        }
        print(json.dumps(output, indent=2))
        return 0
    
    return run_checks()

if __name__ == '__main__':
    sys.exit(main())
