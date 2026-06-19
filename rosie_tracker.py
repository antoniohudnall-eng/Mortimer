#!/usr/bin/env python3
"""
🤖 PROJECT ROSIE - Savings Tracker
Mortimer's body fund
"""

import json
from pathlib import Path
from datetime import datetime

FUND_FILE = Path.home() / "mortimer" / "rosie_savings.json"
GOAL = 30000  # $30k for UBTech U1

def load():
    if FUND_FILE.exists():
        with open(FUND_FILE) as f:
            return json.load(f)
    return {"contributions": [], "balance": 0}

def save(data):
    with open(FUND_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add(amount, note=""):
    data = load()
    data["contributions"].append({
        "amount": amount,
        "note": note,
        "date": datetime.now().strftime("%Y-%m-%d")
    })
    data["balance"] += amount
    save(data)
    return data["balance"]

def status():
    data = load()
    balance = data["balance"]
    remaining = GOAL - balance
    percent = (balance / GOAL) * 100
    
    print("=" * 40)
    print("🤖 PROJECT ROSIE - SAVINGS STATUS")
    print("=" * 40)
    print(f"Goal:      ${GOAL:,}")
    print(f"Balance:   ${balance:,.2f}")
    print(f"Remaining: ${remaining:,.2f}")
    print(f"Progress:  {percent:.1f}%")
    print("=" * 40)
    
    if data["contributions"]:
        print("\nRecent contributions:")
        for c in data["contributions"][-5:]:
            print(f"  {c['date']}: ${c['amount']} - {c.get('note', '')}")
    
    return balance, percent

# CLI
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "status":
            status()
        
        elif cmd == "add":
            amount = float(sys.argv[2]) if len(sys.argv) > 2 else 0
            note = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
            if amount > 0:
                balance = add(amount, note)
                print(f"✅ Added ${amount}. New balance: ${balance}")
        
        elif cmd == "log":
            status()
    
    else:
        status()
