#!/usr/bin/env python3
"""
📋 SUPPORT LOG - Pickup & Delivery Tracking
Ticket-style system with status tracking
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime

DATA_DIR = Path.home() / "mortimer" / "logistics"
DATA_DIR.mkdir(exist_ok=True)

LOG_FILE = DATA_DIR / "support_log.json"

def load():
    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            return json.load(f)
    return {"tickets": [], "next_id": 1}

def save(data):
    with open(LOG_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_ticket(ticket_type, subject, details=""):
    """Add pickup or delivery ticket"""
    data = load()
    
    ticket = {
        "id": data["next_id"],
        "type": ticket_type,  # "pickup" or "delivery"
        "subject": subject,
        "details": details,
        "status": "open",  # open, in_progress, done
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "history": [
            {"action": "created", "time": datetime.now().strftime("%Y-%m-%d %H:%M")}
        ]
    }
    
    data["tickets"].append(ticket)
    data["next_id"] += 1
    save(data)
    
    return ticket["id"]

def update_ticket(ticket_id, action, new_status=None, note=""):
    """Update ticket status"""
    data = load()
    
    for ticket in data["tickets"]:
        if ticket["id"] == ticket_id:
            ticket["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            if new_status:
                ticket["status"] = new_status
            
            history_entry = {"action": action, "time": datetime.now().strftime("%Y-%m-%d %H:%M")}
            if note:
                history_entry["note"] = note
            ticket["history"].append(history_entry)
            
            save(data)
            return True
    return False

def list_tickets(ticket_type=None, status=None):
    """List tickets with optional filters"""
    data = load()
    
    tickets = data["tickets"]
    if ticket_type:
        tickets = [t for t in tickets if t["type"] == ticket_type]
    if status:
        tickets = [t for t in tickets if t["status"] == status]
    
    return sorted(tickets, key=lambda x: x["id"], reverse=True)

def format_ticket(ticket):
    """Format ticket for display"""
    status_icon = {"open": "📋", "in_progress": "🔄", "done": "✅"}.get(ticket["status"], "📋")
    type_icon = {"pickup": "📦", "delivery": "🚚"}.get(ticket["type"], "📋")
    
    msg = f"{status_icon} *Ticket #{ticket['id']}* ({ticket['type'].upper()})\n"
    msg += f"{type_icon} {ticket['subject']}\n"
    
    if ticket.get("details"):
        msg += f"   📝 {ticket['details']}\n"
    
    msg += f"   Status: {ticket['status']} | Created: {ticket['created']}\n"
    
    return msg

def format_log():
    """Format full log"""
    tickets = list_tickets()
    
    if not tickets:
        return "📋 Support Log is empty"
    
    open_pickups = [t for t in tickets if t["type"] == "pickup" and t["status"] == "open"]
    open_deliveries = [t for t in tickets if t["type"] == "delivery" and t["status"] == "open"]
    in_progress = [t for t in tickets if t["status"] == "in_progress"]
    done = [t for t in tickets if t["status"] == "done"]
    
    msg = "📋 *SUPPORT LOG*\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"📦 Pickups (open): {len(open_pickups)}\n"
    msg += f"🚚 Deliveries (open): {len(open_deliveries)}\n"
    msg += f"🔄 In Progress: {len(in_progress)}\n"
    msg += f"✅ Done Today: {len(done)}\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    if open_pickups:
        msg += "📦 *OPEN PICKUPS:*\n"
        for t in open_pickups[:10]:
            msg += f"#{t['id']} - {t['subject']}\n"
        msg += "\n"
    
    if open_deliveries:
        msg += "🚚 *OPEN DELIVERIES:*\n"
        for t in open_deliveries[:10]:
            msg += f"#{t['id']} - {t['subject']}\n"
        msg += "\n"
    
    if in_progress:
        msg += "🔄 *IN PROGRESS:*\n"
        for t in in_progress[:5]:
            msg += f"#{t['id']} - {t['subject']}\n"
        msg += "\n"
    
    if done:
        msg += "✅ *RECENTLY DONE:*\n"
        for t in done[:5]:
            msg += f"#{t['id']} - {t['subject']}\n"
    
    return msg

# Command-line interface
if __name__ == "__main__":
    import sys
    
    cmd = sys.argv[1] if len(sys.argv) > 1 else "log"
    
    if cmd == "log":
        print(format_log())
    
    elif cmd == "add":
        ticket_type = sys.argv[2] if len(sys.argv) > 2 else "pickup"
        subject = sys.argv[3] if len(sys.argv) > 3 else "New item"
        details = sys.argv[4] if len(sys.argv) > 4 else ""
        ticket_id = add_ticket(ticket_type, subject, details)
        print(f"✅ Ticket #{ticket_id} created: {subject}")
    
    elif cmd == "done":
        ticket_id = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        if update_ticket(ticket_id, "completed", "done"):
            print(f"✅ Ticket #{ticket_id} marked as done")
        else:
            print(f"❌ Ticket #{ticket_id} not found")
    
    elif cmd == "progress":
        ticket_id = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        note = sys.argv[3] if len(sys.argv) > 3 else ""
        if update_ticket(ticket_id, "in progress", "in_progress", note):
            print(f"🔄 Ticket #{ticket_id} in progress")
        else:
            print(f"❌ Ticket #{ticket_id} not found")
    
    elif cmd == "pickups":
        tickets = list_tickets("pickup")
        if not tickets:
            print("📦 No pickups")
        else:
            for t in tickets:
                print(format_ticket(t))
    
    elif cmd == "deliveries":
        tickets = list_tickets("delivery")
        if not tickets:
            print("🚚 No deliveries")
        else:
            for t in tickets:
                print(format_ticket(t))
    
    else:
        print("Commands: log, add <type> <subject> [details], done <id>, progress <id> [note], pickups, deliveries")
