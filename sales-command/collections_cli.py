#!/usr/bin/env python3
"""
Collections CLI - Manage collections accounts
Usage:
    python3 collections_cli.py status
    python3 collections_cli.py mark <invoice_id> <status>
    python3 collections_cli.py update <invoice_id> <field> <value>
    python3 collections_cli.py add <customer> <invoice> <amount>
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

# Collections API endpoint (read-only)
API_URL = "https://psdepot.com/collections/api"

class CollectionsCLI:
    def __init__(self):
        self.db_path = Path(__file__).parent / "data" / "collections.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
    
    def init_db(self):
        """Initialize local database"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            invoice TEXT UNIQUE,
            customer TEXT,
            amount REAL,
            status TEXT,
            days INTEGER,
            note TEXT,
            phone TEXT,
            address TEXT,
            last_contact TIMESTAMP,
            contact_result TEXT,
            updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        conn.commit()
        conn.close()
    
    def sync_from_api(self):
        """Sync from psdepot.com API"""
        import requests
        resp = requests.get(API_URL, timeout=10)
        data = resp.json()
        
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        for inv in data.get("invoices", []):
            c.execute('''INSERT OR REPLACE INTO accounts 
                (invoice, customer, amount, status, days, note, phone, address, updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (inv["invoice"], inv["customer"], inv["amount"], inv["status"],
                 inv["days"], inv.get("note",""), inv.get("phone",""), 
                 inv.get("address",""), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        print(f"✅ Synced {len(data.get('invoices', []))} accounts")
    
    def status(self):
        """Show status"""
        self.sync_from_api()
        
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        c.execute("SELECT status, COUNT(*), SUM(amount) FROM accounts GROUP BY status")
        rows = c.fetchall()
        
        print("\n📊 COLLECTIONS STATUS")
        print("="*70)
        
        total = 0
        total_amount = 0
        for status, count, amount in rows:
            total += count
            total_amount += amount or 0
            print(f"  {status:15} {count:3} accounts | ${(amount or 0):>10,.2f}")
        
        print("-"*70)
        print(f"  {'TOTAL':15} {total:3} accounts | ${total_amount:>10,.2f}")
        
        # Priority accounts
        print("\n🚨 PRIORITY ACCOUNTS (30+ days overdue)")
        print("-"*70)
        c.execute("SELECT customer, invoice, amount, days FROM accounts WHERE days > 30 ORDER BY days DESC")
        for row in c.fetchall():
            print(f"  {row[3]:3}d | {row[0][:25]:25} | ${row[2]:>8.2f} | {row[1]}")
        
        conn.close()
    
    def mark_delivered(self, location):
        """Mark deliveries complete for a location"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        # Find undelivered in that area
        c.execute("SELECT invoice, customer, amount FROM accounts WHERE address LIKE ? AND status = 'Undelivered'",
                  (f"%{location}%",))
        rows = c.fetchall()
        
        for inv, cust, amt in rows:
            c.execute("UPDATE accounts SET status = 'Delivered', updated = ? WHERE invoice = ?",
                      (datetime.now().isoformat(), inv))
            print(f"✅ {inv} - {cust} - ${amt:.2f}")
        
        conn.commit()
        conn.close()
        print(f"\n📦 Marked {len(rows)} as delivered for {location}")
    
    def update_status(self, invoice, status):
        """Update invoice status"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        c.execute("UPDATE accounts SET status = ?, updated = ? WHERE invoice = ?",
                  (status, datetime.now().isoformat(), invoice))
        
        if c.rowcount > 0:
            print(f"✅ {invoice} marked as {status}")
        else:
            print(f"❌ {invoice} not found")
        
        conn.commit()
        conn.close()
    
    def priority(self):
        """Show priority list"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        c.execute("SELECT customer, invoice, amount, days, note, phone FROM accounts WHERE status IN ('Overdue', 'Unpaid') ORDER BY days DESC")
        rows = c.fetchall()
        
        print("\n🚨 PRIORITY COLLECTIONS LIST")
        print("="*80)
        print(f"{'Customer':<25} {'Invoice':<12} {'Amount':>10} {'Days':>6} {'Phone':<15}")
        print("-"*80)
        
        for row in rows:
            print(f"{row[0][:25]:<25} {row[1]:<12} ${row[2]:>8.2f} {row[3]:>6}d {row[5] or 'N/A':<15}")
        
        conn.close()
        print(f"\nTotal: {len(rows)} accounts")

if __name__ == "__main__":
    import sys
    
    cli = CollectionsCLI()
    
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "status":
        cli.status()
    elif cmd == "delivered" and len(sys.argv) > 2:
        cli.mark_delivered(sys.argv[2])
    elif cmd == "update" and len(sys.argv) > 3:
        cli.update_status(sys.argv[2], sys.argv[3])
    elif cmd == "priority":
        cli.priority()
    elif cmd == "sync":
        cli.sync_from_api()
    else:
        print(__doc__)
