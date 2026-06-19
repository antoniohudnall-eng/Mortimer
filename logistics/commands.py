#!/usr/bin/env python3
"""
📦 LOGISTICS COMMANDS for Telegram Bot
Add these to the main bot handler
"""

from pathlib import Path
import json
from datetime import datetime

DATA_DIR = Path.home() / "mortimer" / "logistics"
DATA_DIR.mkdir(exist_ok=True)

PICKUP_FILE = DATA_DIR / "pickups.json"
DELIVERY_FILE = DATA_DIR / "deliveries.json"

def load_json(filepath, default=[]):
    if filepath.exists():
        with open(filepath) as f:
            return json.load(f)
    return default

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def cmd_pickup_add(text):
    """Add /pickup <item>"""
    pickups = load_json(PICKUP_FILE)
    pickups.append({
        "item": text,
        "added": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "pending"
    })
    save_json(PICKUP_FILE, pickups)
    return f"📦 Added: {text}"

def cmd_pickup_list():
    pickups = load_json(PICKUP_FILE)
    if not pickups:
        return "📦 No pickups pending"
    
    msg = "📦 **PICKUPS:**\n"
    for i, p in enumerate(pickups, 1):
        icon = "⏳" if p['status'] == "pending" else "✅"
        msg += f"{icon} {i}. {p['item']}\n"
    msg += f"\nTotal: {len(pickups)}"
    return msg

def cmd_pickup_done(num):
    pickups = load_json(PICKUP_FILE)
    try:
        idx = int(num) - 1
        if 0 <= idx < len(pickups):
            pickups[idx]['status'] = 'done'
            pickups[idx]['completed'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_json(PICKUP_FILE, pickups)
            return f"✅ Pickup {num} done!"
        return f"❌ Invalid pickup #{num}"
    except:
        return "❌ Use: /pickup_done <number>"

def cmd_delivery_add(text):
    """Add /delivery <item> to <address>"""
    parts = text.split(' to ')
    if len(parts) == 2:
        item, address = parts
    else:
        item = text
        address = "TBD"
    
    deliveries = load_json(DELIVERY_FILE)
    deliveries.append({
        "item": item.strip(),
        "address": address.strip(),
        "added": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "pending"
    })
    save_json(DELIVERY_FILE, deliveries)
    return f"🚚 Added: {item.strip()} → {address.strip()}"

def cmd_delivery_list():
    deliveries = load_json(DELIVERY_FILE)
    if not deliveries:
        return "🚚 No deliveries pending"
    
    msg = "🚚 **DELIVERIES:**\n"
    for i, d in enumerate(deliveries, 1):
        icon = "⏳" if d['status'] == "pending" else "✅"
        msg += f"{icon} {i}. {d['item']} → {d['address']}\n"
    msg += f"\nTotal: {len(deliveries)}"
    return msg

def cmd_delivery_done(num):
    deliveries = load_json(DELIVERY_FILE)
    try:
        idx = int(num) - 1
        if 0 <= idx < len(deliveries):
            deliveries[idx]['status'] = 'done'
            deliveries[idx]['completed'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_json(DELIVERY_FILE, deliveries)
            return f"✅ Delivery {num} done!"
        return f"❌ Invalid delivery #{num}"
    except:
        return "❌ Use: /delivery_done <number>"

def cmd_logistics_help():
    return """📦 **LOGISTICS COMMANDS:**

/pickup <item> - Add pickup
/pickups - List pickups
/pickup_done <#>- Mark pickup complete

/delivery <item> to <address> - Add delivery
/deliveries - List deliveries
/delivery_done <#> - Mark delivery complete

/start - Welcome message
/status - System status
/help - This help"""

# Test
if __name__ == "__main__":
    print(cmd_logistics_help())
    print()
    print(cmd_pickup_add("50 boxes from Amazon"))
    print(cmd_delivery_add("Invoice to John to 123 Main St"))
    print()
    print(cmd_pickup_list())
