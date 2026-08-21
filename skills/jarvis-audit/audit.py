#!/usr/bin/env python3
"""
Jarvis Audit — executable audit of your recurring work.

Reads the canonical task list (master-schedule + startup-cadence), classifies
every task as a deterministic workflow vs an AI agent, and writes a persisted
candidate report. This is the "run without you" audit from the jarvis-audit skill.

Usage:
  python3 audit.py                 # full audit -> writes report to research/
  python3 audit.py --dry-run       # print only, don't write
  python3 audit.py --out path.md   # write report to a specific path
  python3 audit.py --meter         # also record 25 QL to jarvis-audit in the ledger
  python3 audit.py --no-memory     # skip appending a note to today's memory file
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import date, datetime

HOME = os.path.expanduser("~")
MASTER = os.path.join(HOME, ".pi", "agent", "skills", "master-schedule", "SKILL.md")
STARTUP = os.path.join(HOME, ".pi", "agent", "skills", "startup-cadence", "SKILL.md")
MEMORY_DIR = os.path.join(HOME, "downloads", "mortimer-v1", "memory")
REPORT_DIR = os.path.join(HOME, "downloads", "mortimer-v1", "research")
LEDGER = os.path.join(HOME, ".pi", "agent", "skills", "credit-ledger", "ledger.py")

AI_KEYWORDS = [
    "draft", "write", "script", "content", "post", "engage", "reply", "respond",
    "research", "analy", "review", "report", "summar", "plan", "enrich", "tier",
    "dedup", "recommend", "spotlight", "newsletter", "email", "carousel",
    "caption", "hashtag", "outreach", "prospect", "competitor", "strategy",
    "calendar", "deep dive", "deep-dive", "retro", "vendor",
]

METRIC_HINTS = [
    ("health factor", "alerts with 0 false positives"),
    ("post", "posts shipped/week"),
    ("competitor", "competitors checked/week"),
    ("sync", "sync succeeds 100%"),
    ("memory", "memory file created daily"),
    ("lead", "leads processed/week"),
    ("shopify", "stock alerts actioned within 24h"),
    ("aave", "positions reviewed on schedule"),
    ("report", "reports delivered on time"),
    ("email", "emails sent/week"),
    ("content", "pieces shipped/week"),
    ("calendar", "calendar planned ahead"),
]


def _cells(line):
    s = line.strip()
    if not s.startswith("|"):
        return None
    return [c.replace("*", "").strip() for c in s.strip("|").split("|")]


def _is_separator(cells):
    return all(set(c) <= set("-: ") for c in cells)


def _is_header(cells):
    joined = " ".join(cells).lower()
    return any(h in joined for h in ("task", "time", "owner", "duration", "trigger", "action", "escalate"))


def parse_master():
    tasks = []
    with open(MASTER, encoding="utf-8") as f:
        lines = f.readlines()
    section = None
    day = None
    for line in lines:
        s = line.strip()
        if s.startswith("## "):
            up = s.upper()
            if "DAILY" in up:
                section = "daily"
            elif "WEEKLY" in up:
                section = "weekly"
            elif "MONTHLY" in up:
                section = "monthly"
            elif "ALERT" in up:
                section = "alerts"
            else:
                section = None
            day = None
            continue
        if s.startswith("### "):
            title = s.strip("# ").strip()
            day = title.split(" — ")[0].strip() if " — " in title else title
            continue
        cells = _cells(line)
        if cells is None or _is_separator(cells) or _is_header(cells):
            continue
        if section == "alerts":
            if len(cells) >= 2 and cells[0]:
                tasks.append({
                    "task": cells[1],
                    "trigger": cells[0],
                    "freq": "event",
                    "owner": cells[2] if len(cells) > 2 else "",
                    "duration": cells[3] if len(cells) > 3 else "",
                })
        elif section == "daily":
            if len(cells) >= 2 and cells[1]:
                tasks.append({
                    "task": cells[1],
                    "trigger": cells[0] if cells[0] else "daily",
                    "freq": "daily",
                    "owner": cells[2] if len(cells) > 2 else "",
                    "duration": cells[3] if len(cells) > 3 else "",
                })
        elif section in ("weekly", "monthly"):
            if cells[0]:
                tasks.append({
                    "task": cells[0],
                    "trigger": day or section,
                    "freq": section,
                    "owner": cells[1] if len(cells) > 1 else "",
                    "duration": cells[2] if len(cells) > 2 else "",
                })
    return tasks


def parse_startup():
    tasks = []
    with open(STARTUP, encoding="utf-8") as f:
        lines = f.readlines()
    phase = "startup"
    for line in lines:
        s = line.strip()
        if s.startswith("## "):
            phase = "shutdown" if "SHUTDOWN" in s.upper() else "startup"
            continue
        m = re.match(r"^\d+\.\s*(.+?)\s*→\s*(.+)$", s)
        if m:
            tasks.append({
                "task": f"{m.group(1)} — {m.group(2)}",
                "trigger": "session start" if phase == "startup" else "session end",
                "freq": "session",
                "owner": "Startup Cadence",
                "duration": "",
            })
    return tasks


def needs_ai(text):
    t = text.lower()
    return any(k in t for k in AI_KEYWORDS)


FREQ_WEIGHT = {"daily": 4, "session": 3, "weekly": 2, "monthly": 1, "event": 0}


def classify(t):
    auto = t["freq"] in ("daily", "weekly", "monthly", "event")
    ai = needs_ai(t["task"])
    typ = "agent" if ai else "workflow"
    return auto, ai, typ


def metric_for(task):
    t = task.lower()
    for k, v in METRIC_HINTS:
        if k in t:
            return v
    return "define one metric before building"


def first_step(typ):
    return "cron / temporal-brain script" if typ == "workflow" else "agent + shadow mode (approve first)"


def render_report(tasks, out_path):
    rows = []
    n_workflow = n_agent = n_auto = n_manual = 0
    for t in tasks:
        auto, ai, typ = classify(t)
        if typ == "workflow":
            n_workflow += 1
        else:
            n_agent += 1
        if auto:
            n_auto += 1
        else:
            n_manual += 1
        rows.append((t, auto, ai, typ))

    lines = []
    lines.append(f"# Jarvis Audit Report — {date.today().isoformat()}")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Inputs: master-schedule + startup-cadence ({len(tasks)} tasks)")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- Total recurring tasks: **{len(tasks)}**")
    lines.append(f"- Deterministic (workflow): **{n_workflow}**")
    lines.append(f"- Needs AI (agent): **{n_agent}**")
    lines.append(f"- Can fire without you: **{n_auto}**")
    lines.append(f"- Needs you as trigger (session lifecycle): **{n_manual}**")
    lines.append("")
    lines.append("## Candidate Table")
    lines.append("")
    lines.append("| Task | Trigger | Freq | Owner | Auto? | Needs AI? | Type | Suggested metric | First step |")
    lines.append("|------|---------|------|-------|-------|-----------|------|------------------|------------|")
    for t, auto, ai, typ in sorted(rows, key=lambda r: -FREQ_WEIGHT.get(r[0]["freq"], 0)):
        lines.append(
            f"| {t['task']} | {t['trigger']} | {t['freq']} | {t['owner']} | "
            f"{'yes' if auto else 'no'} | {'yes' if ai else 'no'} | {typ} | "
            f"{metric_for(t['task'])} | {first_step(typ)} |"
        )
    lines.append("")
    lines.append("## Top 3 'Vending Machine' Wins (ship first)")
    lines.append("")
    wins = [r for r in rows if r[3] == "workflow" and r[0]["freq"] in ("daily", "weekly", "monthly", "session")]
    wins.sort(key=lambda r: -FREQ_WEIGHT.get(r[0]["freq"], 0))
    for i, (t, auto, ai, typ) in enumerate(wins[:3], 1):
        lines.append(f"{i}. **{t['task']}** — {t['trigger']}, {t['freq']} → simple script/cron, never fails.")
    if not wins[:3]:
        lines.append("(none — all candidates need AI review)")
    lines.append("")
    lines.append("## Guardrails (apply before anything ships)")
    lines.append("- [ ] Run in shadow mode first (log what it *would* do)")
    lines.append("- [ ] Human approval for anything customer-facing or money-moving")
    lines.append("- [ ] Failure alert — never fail silently")
    lines.append("- [ ] Dry-run / revert for every automation")
    lines.append("- [ ] Meter agent spend in QL via Paymaster")
    lines.append("")
    lines.append("## Notes")
    lines.append("- 'Needs AI?' is a keyword heuristic — review the column with human judgment (taste).")
    lines.append("- Session-lifecycle tasks (startup/shutdown) are already partly automated by `startup-cadence`.")
    lines.append("")

    text = "\n".join(lines)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Report written: {out_path}")
    else:
        print(text)
    return text


def meter():
    r = subprocess.run(
        [sys.executable, LEDGER, "earn", "jarvis-audit", "25", "completed jarvis audit"],
        capture_output=True, text=True,
    )
    out = (r.stdout or "").strip() or (r.stderr or "").strip()
    print(f"[meter] {out}")


def append_memory(report_path):
    today = date.today().isoformat()
    os.makedirs(MEMORY_DIR, exist_ok=True)
    mem = os.path.join(MEMORY_DIR, f"{today}.md")
    line = f"\n- **Jarvis audit** — ran {datetime.now().strftime('%H:%M')}; report: `{report_path}`\n"
    with open(mem, "a", encoding="utf-8") as f:
        f.write(line)
    print(f"[memory] appended note to {mem}")


def main():
    ap = argparse.ArgumentParser(description="Jarvis audit — classify recurring work.")
    ap.add_argument("--dry-run", action="store_true", help="print report, don't write")
    ap.add_argument("--out", default=None, help="write report to this path")
    ap.add_argument("--meter", action="store_true", help="record 25 QL to jarvis-audit in the ledger")
    ap.add_argument("--no-memory", action="store_true", help="skip appending to today's memory file")
    args = ap.parse_args()

    if not os.path.exists(MASTER):
        print(f"ERROR: master-schedule not found: {MASTER}", file=sys.stderr)
        sys.exit(1)

    tasks = parse_master()
    tasks += parse_startup()
    if not tasks:
        print("No recurring tasks parsed — nothing to audit.", file=sys.stderr)
        sys.exit(1)

    out_path = args.out
    if not args.dry_run and out_path is None:
        out_path = os.path.join(REPORT_DIR, f"jarvis-audit-report-{date.today().isoformat()}.md")

    render_report(tasks, None if args.dry_run else out_path)

    if not args.dry_run:
        if args.meter:
            meter()
        if not args.no_memory:
            append_memory(out_path)


if __name__ == "__main__":
    main()
