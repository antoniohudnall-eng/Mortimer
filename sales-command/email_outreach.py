#!/usr/bin/env python3
"""Email Outreach Engine for AGI Agent Sales"""
import json
from datetime import datetime, timedelta
from pathlib import Path

TEMPLATES = {
    "intro": """
Hi {name},

I noticed {company} is in the {business_type} space. As operations scale, most teams get buried in repetitive tasks — scheduling, follow-ups, data entry, customer responses.

We deploy AI agents that handle this for you. Real workers, not just chatbots.

Your options:
• CLERK ($97/mo) — Basic task automation
• GREET ($147/mo) — Customer engagement  
• PERSONAL ($197/mo) — Dedicated assistant
• VELVET ($247/mo) — Premium operations
• CONCIERGE ($297/mo) — White-glove service
• EXECUTIVE ($497/mo) — Full executive support

Most clients see ROI within the first week.

Interested in a demo?

— Morty
AGI Company
""",
    "followup": """
Hey {name},

Following up on my last note about AI agents for {company}.

Quick question: Is delegation something you're looking to solve this quarter?

Our agents handle:
✓ Scheduling & calendar management
✓ Email & customer responses
✓ Lead qualification & follow-ups
✓ Data entry & reporting

Would love to show you how it works. 15 minutes, no pitch — just a live demo.

Let me know if you're open to chatting this week.

— Morty
""",
    "close": """
{name},

I haven't heard back and I get it — you're busy.

Here's what I'll do: Send me your biggest operational headache (the one that eats the most time), and I'll show you exactly how an agent would solve it.

No cost. No commitment. Just a quick screen share to see if it's worth exploring.

Still interested?

— Morty
"""
}

class EmailOutreach:
    def __init__(self):
        self.sent_file = Path(__file__).parent / "data" / "emails_sent.json"
        self.sent = self.load_sent()
    
    def load_sent(self):
        if self.sent_file.exists():
            with open(self.sent_file) as f:
                return json.load(f)
        return []
    
    def save_sent(self):
        with open(self.sent_file, 'w') as f:
            json.dump(self.sent, f, indent=2)
    
    def send_email(self, lead, template="intro"):
        """Simulate sending email (replace with actual SMTP/API)"""
        email = {
            "id": f"EMAIL-{len(self.sent)+1:05d}",
            "lead_id": lead.get("id", "unknown"),
            "to": lead["email"],
            "name": lead["name"],
            "template": template,
            "sent_at": datetime.now().isoformat(),
            "status": "sent"
        }
        self.sent.append(email)
        self.save_sent()
        return email
    
    def get_stats(self):
        by_template = {}
        for e in self.sent:
            t = e["template"]
            by_template[t] = by_template.get(t, 0) + 1
        return {
            "total_sent": len(self.sent),
            "by_template": by_template
        }
    
    def print_report(self):
        stats = self.get_stats()
        print("\n" + "="*50)
        print("📧 EMAIL OUTREACH REPORT")
        print("="*50)
        print(f"  Total Emails Sent: {stats['total_sent']}")
        for t, count in stats.get("by_template", {}).items():
            print(f"  {t:12} {count}")
        print("="*50)

if __name__ == "__main__":
    outreach = EmailOutreach()
    outreach.print_report()
