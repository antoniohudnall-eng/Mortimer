#!/usr/bin/env python3
"""
Dark Factory Vendor System
Actually finds manufacturers and manages outsourced production
"""

import sqlite3
import json
import os
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

DB_PATH = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/vendor_system.db"

@dataclass
class Vendor:
    name: str
    website: str
    email: str
    capabilities: List[str]  # ["3d_printing", "cnc", "pcb", "assembly"]
    min_order: float
    location: str
    rating: float = 0.0
    status: str = "uncontacted"  # uncontacted, quoted, approved, rejected

class VendorSystem:
    """Actually manages vendor relationships for outsourced manufacturing"""
    
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self._init_db()
    
    def _init_db(self):
        """Create tables"""
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS vendors (
                id INTEGER PRIMARY KEY,
                name TEXT,
                website TEXT,
                email TEXT,
                capabilities TEXT,
                min_order REAL,
                location TEXT,
                rating REAL DEFAULT 0,
                status TEXT DEFAULT 'uncontacted',
                created_at TIMESTAMP
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY,
                vendor_id INTEGER,
                item TEXT,
                quantity INTEGER,
                unit_price REAL,
                total_price REAL,
                lead_time_days INTEGER,
                status TEXT,
                created_at TIMESTAMP
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                vendor_id INTEGER,
                quote_id INTEGER,
                po_number TEXT,
                status TEXT,  # pending, confirmed, in_production, shipped, delivered
                milestone TEXT,
                created_at TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def add_vendor(self, vendor: Vendor) -> int:
        """Add a vendor to the database"""
        c = self.conn.cursor()
        c.execute('''
            INSERT INTO vendors (name, website, email, capabilities, min_order, location, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (vendor.name, vendor.website, vendor.email, json.dumps(vendor.capabilities),
              vendor.min_order, vendor.location, vendor.status, datetime.now()))
        self.conn.commit()
        return c.lastrowid
    
    def find_vendors_by_capability(self, capability: str) -> List[Vendor]:
        """Find vendors who can do a specific type of manufacturing"""
        c = self.conn.cursor()
        c.execute("SELECT * FROM vendors WHERE capabilities LIKE ?", (f'%"{capability}"%',))
        rows = c.fetchall()
        
        vendors = []
        for row in rows:
            vendors.append(Vendor(
                name=row[1],
                website=row[2],
                email=row[3],
                capabilities=json.loads(row[4]),
                min_order=row[5],
                location=row[6],
                rating=row[7],
                status=row[8]
            ))
        return vendors
    
    def request_quote(self, vendor_id: int, item: str, quantity: int):
        """Generate an RFQ email for a vendor"""
        c = self.conn.cursor()
        c.execute("SELECT name, email FROM vendors WHERE id=?", (vendor_id,))
        vendor = c.fetchone()
        
        if not vendor:
            return None
        
        email_body = f"""
Hello {vendor[0]},

We are requesting a quote for:

Item: {item}
Quantity: {quantity} units

Please provide:
- Unit price
- Total price
- Lead time (days)
- Any setup fees

Best regards,
Dark Factory Procurement
"""
        
        print(f"\n{'='*70}")
        print(f"RFQ for {item}")
        print(f"To: {vendor[1]}")
        print(f"{'='*70}")
        print(email_body)
        
        return email_body
    
    def compare_quotes(self, item: str) -> List[dict]:
        """Compare all quotes for an item"""
        c = self.conn.cursor()
        c.execute('''
            SELECT v.name, q.unit_price, q.total_price, q.lead_time_days
            FROM quotes q
            JOIN vendors v ON q.vendor_id = v.id
            WHERE q.item = ? AND q.status = 'received'
            ORDER BY q.total_price ASC
        ''', (item,))
        
        return [{"vendor": r[0], "unit_price": r[1], "total": r[2], "lead_time": r[3]} 
                for r in c.fetchall()]
    
    def place_order(self, quote_id: int) -> str:
        """Place an order based on a quote"""
        c = self.conn.cursor()
        
        # Get quote details
        c.execute("SELECT vendor_id, item, quantity, total_price FROM quotes WHERE id=?", (quote_id,))
        quote = c.fetchone()
        
        if not quote:
            return "Quote not found"
        
        # Generate PO number
        po = f"DF-{datetime.now().strftime('%Y%m%d')}-{quote_id:04d}"
        
        # Create order
        c.execute('''
            INSERT INTO orders (vendor_id, quote_id, po_number, status, milestone, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (quote[0], quote_id, po, 'confirmed', 'order_placed', datetime.now()))
        
        self.conn.commit()
        
        print(f"\n{'='*70}")
        print(f"PURCHASE ORDER CREATED: {po}")
        print(f"{'='*70}")
        print(f"Item: {quote[1]}")
        print(f"Quantity: {quote[2]}")
        print(f"Total: ${quote[3]:,.2f}")
        print(f"Status: Confirmed")
        
        return po
    
    def update_milestone(self, po_number: str, milestone: str):
        """Update production milestone"""
        c = self.conn.cursor()
        c.execute('''
            UPDATE orders SET milestone = ?, status = ? WHERE po_number = ?
        ''', (milestone, milestone.replace('_', ' '), po_number))
        self.conn.commit()
        
        print(f"\nPO {po_number}: {milestone}")

def main():
    """Demo the vendor system"""
    print("=" * 70)
    print("DARK FACTORY VENDOR SYSTEM")
    print("=" * 70)
    
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    system = VendorSystem()
    
    # Add some real vendors
    print("\nAdding vendors to database...")
    
    vendors = [
        Vendor("Protolabs", "https://www.protolabs.com", "quotes@protolabs.com", 
               ["3d_printing", "cnc", "injection_molding"], 1000.0, "MN, USA", 4.5),
        Vendor("Xometry", "https://www.xometry.com", "rfq@xometry.com",
               ["3d_printing", "cnc", "sheet_metal"], 500.0, "MD, USA", 4.3),
        Vendor("JLCPCB", "https://jlcpcb.com", "support@jlcpcb.com",
               ["pcb", "pcb_assembly"], 5.0, "China", 4.7),
        Vendor("PCBWay", "https://www.pcbway.com", "service@pcbway.com",
               ["pcb", "pcb_assembly", "cnc"], 5.0, "China", 4.6),
        Vendor("Hubs", "https://www.hubs.com", "support@hubs.com",
               ["3d_printing", "cnc", "injection_molding"], 1000.0, "Netherlands/USA", 4.4),
    ]
    
    for v in vendors:
        vid = system.add_vendor(v)
        print(f"  ✓ Added: {v.name} ({v.capabilities[0]})")
    
    # Find vendors for Cobra robot parts
    print("\n" + "=" * 70)
    print("FINDING VENDORS FOR COBRA ROBOT PARTS")
    print("=" * 70)
    
    print("\n3D Printing vendors:")
    vendors_3d = system.find_vendors_by_capability("3d_printing")
    for v in vendors_3d:
        print(f"  • {v.name} (MOQ: ${v.min_order:,.0f}, Rating: {v.rating})")
    
    print("\nPCB vendors:")
    vendors_pcb = system.find_vendors_by_capability("pcb")
    for v in vendors_pcb:
        print(f"  • {v.name} (MOQ: ${v.min_order:,.0f}, Rating: {v.rating})")
    
    # Generate RFQ
    print("\n" + "=" * 70)
    print("GENERATING RFQs")
    print("=" * 70)
    
    if vendors_3d:
        system.request_quote(1, "Cobra Robot Vertebrae (25 units, nylon)", 25)
    
    # Simulate receiving quotes
    print("\n" + "=" * 70)
    print("SIMULATING QUOTE RECEIPT")
    print("=" * 70)
    
    c = system.conn.cursor()
    c.execute('''
        INSERT INTO quotes (vendor_id, item, quantity, unit_price, total_price, lead_time_days, status, created_at)
        VALUES 
        (1, "Cobra Robot Vertebrae", 25, 45.00, 1125.00, 10, "received", ?),
        (2, "Cobra Robot Vertebrae", 25, 38.50, 962.50, 14, "received", ?),
        (5, "Cobra Robot Vertebrae", 25, 42.00, 1050.00, 12, "received", ?)
    ''', (datetime.now(), datetime.now(), datetime.now()))
    system.conn.commit()
    
    # Compare quotes
    quotes = system.compare_quotes("Cobra Robot Vertebrae")
    print("\nQuote Comparison:")
    for i, q in enumerate(quotes, 1):
        print(f"  {i}. {q['vendor']}: ${q['total']:,.2f} total, {q['lead_time']} days")
    
    # Place order with best vendor
    if quotes:
        best = min(quotes, key=lambda x: x['total'])
        print(f"\n✓ Best option: {best['vendor']} at ${best['total']:,.2f}")
        
        # Place order (would be quote_id from database)
        po = system.place_order(2)  # Xometry quote
        
        # Track milestones
        system.update_milestone(po, "materials_sourced")
        system.update_milestone(po, "in_production")
        system.update_milestone(po, "qc_passed")
        system.update_milestone(po, "shipped")
    
    print("\n" + "=" * 70)
    print("VENDOR SYSTEM READY")
    print("=" * 70)
    print(f"\nDatabase: {DB_PATH}")
    print("Next steps:")
    print("  1. Add more vendors from directories (ThomasNet, Alibaba)")
    print("  2. Send actual RFQ emails")
    print("  3. Receive quotes and compare")
    print("  4. Place orders")
    print("  5. Track production")

if __name__ == "__main__":
    main()
