#!/bin/bash
# Auto-Outreach Engine - Scale email campaigns

echo "🚀 AGI SALES AUTO-OUTREACH"
echo "==========================="
echo ""

# Load leads
LEADS=$(python3 << 'PY'
import json
from pathlib import Path

# Get generated leads
gen = Path("$HOME/mortimer/sales-command/data/generated_leads.json")
if gen.exists():
    with open(gen) as f:
        leads = json.load(f)
        print(len(leads))
PY
)

echo "📋 Loaded $LEADS leads"
echo ""

# Email templates
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📧 Sending intro emails..."
python3 << PY
import json
import sys
sys.path.insert(0, "$SCRIPT_DIR")
from email_outreach import EmailOutreach

outreach = EmailOutreach()

# Load leads
with open("$HOME/mortimer/sales-command/data/generated_leads.json") as f:
    leads = json.load(f)

# Send to first 100 leads
count = 0
for lead in leads[:100]:
    outreach.send_email(lead, "intro")
    count += 1

print(f"✅ Sent {count} intro emails")
outreach.print_report()
PY

echo ""
echo "⏰ Scheduling follow-ups..."
python3 << PY
import json
sys.path.insert(0, "$SCRIPT_DIR")
from datetime import datetime, timedelta
from pathlib import Path

# Schedule follow-ups for next week
schedule = []
with open("$HOME/mortimer/sales-command/data/generated_leads.json") as f:
    leads = json.load(f)

for lead in leads[:50]:
    schedule.append({
        "lead_id": lead["id"],
        "email": lead["email"],
        "template": "followup",
        "scheduled_for": (datetime.now() + timedelta(days=7)).isoformat()
    })

Path("$HOME/mortimer/sales-command/data/followup_schedule.json").write_text(json.dumps(schedule, indent=2))
print(f"✅ Scheduled {len(schedule)} follow-ups for next week")
PY

echo ""
echo "✅ Auto-outreach complete!"
