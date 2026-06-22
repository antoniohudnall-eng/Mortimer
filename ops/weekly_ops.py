#!/usr/bin/env python3
"""
📅 SEED3 WEEKLY OPERATIONS
Mortimer's weekly task execution
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

HOME = Path.home()
OPS_DIR = HOME / "mortimer" / "ops"
WEEKLY_DIR = OPS_DIR / "weekly"
REPORTS_DIR = OPS_DIR / "reports"
WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

TS = datetime.now().strftime("%Y-%m-%d")
WEEK = datetime.now().strftime("%Y-W%U")

def log(msg, category="INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{category}] {msg}"
    print(line)

def cmd(command, timeout=60):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return str(e), 1

# ═══════════════════════════════════════════════════════════
# WEEKLY OPERATIONS
# ═══════════════════════════════════════════════════════════

def full_curriculum_run():
    """LILLY - Run full curriculum cycle (Sunday)"""
    log("=== LILLY FULL CURRICULUM ===", "LILLY")
    
    # Reset progress for fresh run
    progress_file = HOME / "mortimer" / "memory" / "lilly_progress.json"
    if progress_file.exists():
        with open(progress_file, "w") as f:
            json.dump({"books_read": [], "current": 0, "total_learned": 0}, f)
        log("Progress reset for new cycle", "LILLY")
    
    # Run LILLY
    log("Starting full curriculum run...", "LILLY")
    stdout, code = cmd(f"cd {HOME}/mortimer && python3 lilly_reading_loop.py", timeout=600)
    
    if code == 0:
        log("Full curriculum complete!", "LILLY")
    else:
        log(f"Error: {stdout[:200]}", "LILLY")
    
    return code == 0

def maintenance_day():
    """SPINDLE - Wednesday maintenance"""
    log("=== MAINTENANCE DAY ===", "SPINDLE")
    
    # nginx config review
    log("Reviewing nginx configs...", "SPINDLE")
    conf = "/data/data/com.termux/files/usr/etc/nginx/nginx.conf"
    stdout, code = cmd(f"nginx -t -c {conf} 2>&1")
    if "syntax is ok" in stdout:
        log("✅ nginx config valid", "SPINDLE")
    
    # Check all services
    log("Checking all services...", "SPINDLE")
    ports = [7777, 7778, 7779, 3333, 3334, 8000, 11434]
    all_up = True
    for port in ports:
        stdout, code = cmd(f"curl -s -o /dev/null -w '%{{http_code}}' http://127.0.0.1:{port}/")
        if stdout != "200":
            all_up = False
            log(f"⚠️ Port {port} DOWN", "SPINDLE")
    
    if all_up:
        log("✅ All services healthy", "SPINDLE")
    
    # GitHub sync check
    log("Checking GitHub sync status...", "SPINDLE")
    stdout, code = cmd("cd ~/mortimer && git status --short 2>/dev/null | head -5")
    if code == 0 and stdout:
        log(f"Git changes pending:\n{stdout[:200]}", "SPINDLE")
    else:
        log("Git: No pending changes", "SPINDLE")
    
    # AGENTS.md review reminder
    agents_file = HOME / "mortimer" / "AGENTS.md"
    if agents_file.exists():
        with open(agents_file) as f:
            lines = len(f.readlines())
        log(f"AGENTS.md: {lines} lines", "SPINDLE")
    
    log("Maintenance day complete", "SPINDLE")
    return True

def financial_report():
    """LEDGER-9 - Weekly financial summary"""
    log("=== WEEKLY FINANCIAL REPORT ===", "LEDGER-9")
    
    report = []
    report.append(f"# Weekly Financial Report - {TS}")
    report.append("")
    
    # Revenue (placeholder - would come from actual data)
    report.append("## Revenue")
    report.append("- Sales: Check with PULP/HUME")
    report.append("- Crypto gains: Check with Cryptonio")
    report.append("")
    
    # Costs
    report.append("## Costs")
    report.append("- Server costs: mortimer.cloud")
    report.append("- Agent compute: Ollama models")
    report.append("- External services: TBD")
    report.append("")
    
    # Actions needed
    report.append("## Actions Required")
    report.append("- [ ] Get sales numbers from PSD")
    report.append("- [ ] Check crypto portfolio status")
    report.append("- [ ] Review expense reports")
    report.append("")
    
    # Save report
    report_file = REPORTS_DIR / f"financial-{WEEK}.md"
    with open(report_file, "w") as f:
        f.write("\n".join(report))
    
    log(f"Financial report saved: {report_file}", "LEDGER-9")
    return True

def security_audit():
    """SENTINEL - Weekly security audit"""
    log("=== WEEKLY SECURITY AUDIT ===", "SENTINEL")
    
    audit = []
    audit.append(f"# Security Audit - {TS}")
    audit.append("")
    
    # Check fail2ban
    stdout, code = cmd("fail2ban-client status 2>/dev/null | head -10")
    if code == 0:
        audit.append("## Fail2Ban")
        audit.append(stdout)
        audit.append("")
    
    # Failed attempts summary
    stdout, code = cmd("grep 'Failed password' /var/log/auth.log 2>/dev/null | wc -l")
    if code == 0:
        total = stdout.strip() if stdout.strip().isdigit() else "0"
        audit.append(f"## Total Failed SSH Attempts: {total}")
        audit.append("")
    
    # NetProbes status
    audit.append("## NetProbes")
    stdout, code = cmd("ls ~/mortimer/netprobes/ 2>/dev/null | wc -l")
    if code == 0:
        probes = stdout.strip() if stdout.strip().isdigit() else "0"
        audit.append(f"Active probes: {probes}")
        audit.append("")
    
    # Recommendations
    audit.append("## Recommendations")
    audit.append("- Continue monitoring")
    audit.append("- Update block lists if needed")
    audit.append("- Review any new IPs")
    
    # Save audit
    audit_file = REPORTS_DIR / f"security-audit-{WEEK}.md"
    with open(audit_file, "w") as f:
        f.write("\n".join(audit))
    
    log(f"Security audit saved: {audit_file}", "SENTINEL")
    return True

def sales_review():
    """PULP - Weekly sales review"""
    log("=== WEEKLY SALES REVIEW ===", "PULP")
    
    review = []
    review.append(f"# Weekly Sales Review - {TS}")
    review.append("")
    
    # Pipeline status
    review.append("## Pipeline Status")
    stdout, code = cmd("ls ~/mortimer/sales-command/data/ 2>/dev/null | wc -l")
    if code == 0:
        files = stdout.strip() if stdout.strip().isdigit() else "0"
        review.append(f"Data files: {files}")
    
    review.append("")
    review.append("## Leads")
    review.append("- [ ] Count new leads")
    review.append("- [ ] Conversion rate")
    review.append("- [ ] Revenue closed")
    review.append("")
    
    review.append("## Actions")
    review.append("- [ ] Follow up on warm leads")
    review.append("- [ ] Review dead leads")
    review.append("- [ ] Update pipeline")
    
    # Save
    review_file = REPORTS_DIR / f"sales-review-{WEEK}.md"
    with open(review_file, "w") as f:
        f.write("\n".join(review))
    
    log(f"Sales review saved: {review_file}", "PULP")
    return True

def learning_report():
    """LILLY - Weekly learning summary"""
    log("=== WEEKLY LEARNING REPORT ===", "LILLY")
    
    report = []
    report.append(f"# Weekly Learning Report - {TS}")
    report.append("")
    
    # Progress
    progress_file = HOME / "mortimer" / "memory" / "lilly_progress.json"
    if progress_file.exists():
        with open(progress_file) as f:
            progress = json.load(f)
        
        report.append("## Books Completed")
        for book_id in progress.get("books_read", []):
            report.append(f"- ID: {book_id}")
        report.append("")
        report.append(f"Total: {len(progress.get('books_read', []))}")
        report.append("")
    
    # Curriculum status
    catalog = HOME / "AOS-Brain" / "curriculum" / "gutenberg" / "bookshelf_catalog.json"
    if catalog.exists():
        with open(catalog) as f:
            cat = json.load(f)
        
        report.append("## Curriculum")
        for category, data in cat.get("categories", {}).items():
            books = len(data.get("books", []))
            report.append(f"- {category}: {books} books")
    
    # Topics covered
    report.append("")
    report.append("## Topics Covered")
    report.append("- Engineering")
    report.append("- Philosophy")
    report.append("- Science")
    report.append("- Literature")
    report.append("- History")
    report.append("- Mathematics")
    report.append("- Psychology")
    
    # Save
    report_file = REPORTS_DIR / f"learning-{WEEK}.md"
    with open(report_file, "w") as f:
        f.write("\n".join(report))
    
    log(f"Learning report saved: {report_file}", "LILLY")
    return True

def executive_summary():
    """MORTIMER - Weekly executive summary to Captain"""
    log("=== EXECUTIVE SUMMARY ===", "MORTIMER")
    
    summary = []
    summary.append(f"# SEED3 Weekly Executive Summary")
    summary.append(f"**Week:** {WEEK}")
    summary.append(f"**Date:** {TS}")
    summary.append("")
    summary.append("---")
    summary.append("")
    
    summary.append("## Security (SENTINEL)")
    summary.append("- Status: Monitoring active")
    summary.append("- Threats: See security audit")
    summary.append("")
    
    summary.append("## Finance (LEDGER-9)")
    summary.append("- See financial report")
    summary.append("")
    
    summary.append("## Engineering (SPINDLE)")
    summary.append("- Services: 7777/7778/7779/3333/3334")
    summary.append("- nginx: Configured")
    summary.append("")
    
    summary.append("## Sales (PULP)")
    summary.append("- See sales review")
    summary.append("")
    
    summary.append("## Learning (LILLY)")
    summary.append("- Curriculum: 23 books")
    summary.append("- Status: See learning report")
    summary.append("")
    
    summary.append("## The Question")
    summary.append("> What did we do this week that made money or saved money?")
    summary.append("")
    
    summary.append("---")
    summary.append("*Generated by SEED3 Operations*")
    
    # Save
    summary_file = REPORTS_DIR / f"executive-summary-{WEEK}.md"
    with open(summary_file, "w") as f:
        f.write("\n".join(summary))
    
    log(f"Executive summary saved: {summary_file}", "MORTIMER")
    
    # Print to console
    print("\n" + "="*60)
    print("📊 WEEKLY EXECUTIVE SUMMARY")
    print("="*60)
    for line in summary:
        print(line)
    
    return True

def run_weekly():
    """Run all weekly operations"""
    day = datetime.now().weekday()  # 0=Monday, 6=Sunday
    
    print("\n" + "="*50)
    print("📅 SEED3 WEEKLY OPERATIONS")
    print(f"Day: {['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][day]}")
    print("="*50 + "\n")
    
    log("Starting weekly operations")
    
    # Everyone does maintenance on Wednesday
    if day == 2:  # Wednesday
        maintenance_day()
        print()
    
    # Sunday = Full curriculum
    if day == 6:  # Sunday
        full_curriculum_run()
        print()
    
    # Everyone does these
    security_audit()
    print()
    
    financial_report()
    print()
    
    sales_review()
    print()
    
    learning_report()
    print()
    
    executive_summary()
    
    print("\n" + "="*50)
    print("✅ WEEKLY OPERATIONS COMPLETE")
    print("="*50)

if __name__ == "__main__":
    run_weekly()
