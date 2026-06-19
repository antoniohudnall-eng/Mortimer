#!/usr/bin/env python3
"""
Dark Factory Production Manager
Actually manages outsourced production for Cobra/Prometheus robots

5 Phases:
1. Design & Prototyping
2. Vendor Sourcing  
3. Production
4. Quality Control
5. Distribution
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

DB_PATH = "/data/factory/production.db"

@dataclass
class ProductionOrder:
    order_id: str
    product: str  # "cobra_v1", "prometheus_v1"
    quantity: int
    phase: int  # 1-5
    vendor_id: Optional[int]
    status: str  # "pending", "active", "complete", "failed"
    created_at: str
    updated_at: str

class DarkFactoryProduction:
    """Actually manages robot production through outsourced vendors"""
    
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self._init_db()
        print("[Dark Factory] Production Manager initialized")
    
    def _init_db(self):
        """Create production database"""
        c = self.conn.cursor()
        
        # Production orders
        c.execute('''
            CREATE TABLE IF NOT EXISTS production_orders (
                id INTEGER PRIMARY KEY,
                order_id TEXT UNIQUE,
                product TEXT,
                quantity INTEGER,
                phase INTEGER,
                vendor_id INTEGER,
                status TEXT,
                bom_sent BOOLEAN DEFAULT 0,
                prototype_received BOOLEAN DEFAULT 0,
                production_started BOOLEAN DEFAULT 0,
                qc_passed BOOLEAN DEFAULT 0,
                shipped BOOLEAN DEFAULT 0,
                delivered BOOLEAN DEFAULT 0,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        ''')
        
        # BOM (Bill of Materials)
        c.execute('''
            CREATE TABLE IF NOT EXISTS bom_items (
                id INTEGER PRIMARY KEY,
                product TEXT,
                item_name TEXT,
                quantity INTEGER,
                unit_cost REAL,
                vendor_sku TEXT,
                lead_time_days INTEGER
            )
        ''')
        
        # Production milestones
        c.execute('''
            CREATE TABLE IF NOT EXISTS milestones (
                id INTEGER PRIMARY KEY,
                order_id TEXT,
                phase INTEGER,
                milestone TEXT,
                status TEXT,
                timestamp TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def create_order(self, product: str, quantity: int) -> str:
        """Create a new production order"""
        order_id = f"DF-{datetime.now().strftime('%Y%m%d')}-{hash(product + str(quantity)) % 10000:04d}"
        
        c = self.conn.cursor()
        c.execute('''
            INSERT INTO production_orders 
            (order_id, product, quantity, phase, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (order_id, product, quantity, 1, "pending", datetime.now(), datetime.now()))
        
        self.conn.commit()
        
        print(f"\n[Dark Factory] Order created: {order_id}")
        print(f"  Product: {product}")
        print(f"  Quantity: {quantity}")
        print(f"  Status: Phase 1 - Design & Prototyping")
        
        return order_id
    
    def advance_phase(self, order_id: str, vendor_id: Optional[int] = None):
        """Advance order to next phase"""
        c = self.conn.cursor()
        c.execute("SELECT phase, status FROM production_orders WHERE order_id=?", (order_id,))
        result = c.fetchone()
        
        if not result:
            print(f"Order {order_id} not found")
            return False
        
        current_phase, status = result
        
        if current_phase >= 5:
            print(f"Order {order_id} already complete")
            return False
        
        new_phase = current_phase + 1
        
        phase_names = {
            1: "Design & Prototyping",
            2: "Vendor Sourcing",
            3: "Production",
            4: "Quality Control",
            5: "Distribution"
        }
        
        c.execute('''
            UPDATE production_orders 
            SET phase=?, vendor_id=?, status=?, updated_at=?
            WHERE order_id=?
        ''', (new_phase, vendor_id, "active", datetime.now(), order_id))
        
        # Log milestone
        c.execute('''
            INSERT INTO milestones (order_id, phase, milestone, status, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (order_id, new_phase, f"Entered {phase_names[new_phase]}", "complete", datetime.now()))
        
        self.conn.commit()
        
        print(f"\n[Dark Factory] {order_id} -> Phase {new_phase}: {phase_names[new_phase]}")
        return True
    
    def get_order_status(self, order_id: str) -> Dict:
        """Get full order status"""
        c = self.conn.cursor()
        c.execute('''
            SELECT * FROM production_orders WHERE order_id=?
        ''', (order_id,))
        
        row = c.fetchone()
        if not row:
            return {"error": "Order not found"}
        
        return {
            "order_id": row[1],
            "product": row[2],
            "quantity": row[3],
            "phase": row[4],
            "vendor_id": row[5],
            "status": row[6],
            "bom_sent": row[7],
            "prototype_received": row[8],
            "production_started": row[9],
            "qc_passed": row[10],
            "shipped": row[11],
            "delivered": row[12],
            "created": row[13]
        }
    
    def list_active_orders(self) -> List[Dict]:
        """List all active production orders"""
        c = self.conn.cursor()
        c.execute('''
            SELECT order_id, product, quantity, phase, status 
            FROM production_orders 
            WHERE status IN ('pending', 'active')
            ORDER BY created_at DESC
        ''')
        
        return [
            {"order_id": r[0], "product": r[1], "quantity": r[2], "phase": r[3], "status": r[4]}
            for r in c.fetchall()
        ]

def main():
    """Demo Dark Factory production"""
    print("=" * 70)
    print("DARK FACTORY PRODUCTION MANAGER")
    print("5-Phase Outsourced Manufacturing")
    print("=" * 70)
    
    factory = DarkFactoryProduction()
    
    # Create sample orders for all 5 phases
    print("\nCreating production orders...")
    
    orders = [
        factory.create_order("cobra_v1", 10),  # Phase 1
        factory.create_order("prometheus_v1", 5),  # Phase 1
    ]
    
    # Advance first order through phases
    print("\n" + "=" * 70)
    print("ADVANCING COBRA ORDER THROUGH ALL 5 PHASES")
    print("=" * 70)
    
    cobra_order = orders[0]
    
    # Phase 1 -> Phase 2 (Prototype complete, sourcing vendors)
    print("\n1. Design & Prototyping -> 2. Vendor Sourcing")
    factory.advance_phase(cobra_order, vendor_id=1)
    
    # Phase 2 -> Phase 3 (Vendor selected, start production)
    print("\n2. Vendor Sourcing -> 3. Production")
    factory.advance_phase(cobra_order, vendor_id=1)
    
    # Phase 3 -> Phase 4 (Production complete, QC)
    print("\n3. Production -> 4. Quality Control")
    factory.advance_phase(cobra_order)
    
    # Phase 4 -> Phase 5 (QC passed, shipping)
    print("\n4. Quality Control -> 5. Distribution")
    factory.advance_phase(cobra_order)
    
    # Show final status
    print("\n" + "=" * 70)
    print("FINAL STATUS")
    print("=" * 70)
    
    for order_id in orders:
        status = factory.get_order_status(order_id)
        print(f"\n{order_id}:")
        print(f"  Product: {status['product']}")
        print(f"  Quantity: {status['quantity']}")
        print(f"  Phase: {status['phase']}")
        print(f"  Status: {status['status']}")
    
    # Active orders
    active = factory.list_active_orders()
    print(f"\n\nActive Orders: {len(active)}")
    for o in active:
        print(f"  • {o['order_id']}: {o['product']} x{o['quantity']} (Phase {o['phase']})")
    
    print("\n" + "=" * 70)
    print("DARK FACTORY PRODUCTION SYSTEM READY")
    print("=" * 70)
    print(f"\nDatabase: {DB_PATH}")
    print("\nNext: Send actual BOMs to vendors, track real production")

if __name__ == "__main__":
    main()
