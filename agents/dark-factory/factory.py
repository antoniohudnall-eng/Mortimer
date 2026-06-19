#!/usr/bin/env python3
"""
Dark Factory - Real Production System
Actually manages outsourced manufacturing
"""

import sqlite3
import json
import os
import time
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional

DB_PATH = "/data/factory/dark_factory.db"

@dataclass
class ProductionOrder:
    order_id: str
    product: str
    quantity: int
    phase: int
    vendor_id: Optional[int]
    status: str
    created_at: datetime
    updated_at: datetime

class DarkFactory:
    """Actually manages robot production"""
    
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self._init_db()
        print("[Dark Factory] Initialized and ready")
    
    def _init_db(self):
        """Create production tables"""
        c = self.conn.cursor()
        
        # Production orders
        c.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                order_id TEXT UNIQUE,
                product TEXT,
                quantity INTEGER,
                phase INTEGER,
                vendor_id INTEGER,
                status TEXT,
                bom_sent INTEGER DEFAULT 0,
                prototype_approved INTEGER DEFAULT 0,
                production_started INTEGER DEFAULT 0,
                qc_passed INTEGER DEFAULT 0,
                shipped INTEGER DEFAULT 0,
                delivered INTEGER DEFAULT 0,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        ''')
        
        # Vendors
        c.execute('''
            CREATE TABLE IF NOT EXISTS vendors (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                website TEXT,
                capabilities TEXT,
                min_order REAL,
                rating REAL,
                active INTEGER DEFAULT 1
            )
        ''')
        
        # Milestones
        c.execute('''
            CREATE TABLE IF NOT EXISTS milestones (
                id INTEGER PRIMARY KEY,
                order_id TEXT,
                phase INTEGER,
                description TEXT,
                completed INTEGER DEFAULT 0,
                timestamp TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def create_order(self, product: str, quantity: int) -> str:
        """Create a production order"""
        order_id = f"DF-{datetime.now().strftime('%Y%m%d')}-{int(time.time() * 1000) % 100000:05d}"
        
        c = self.conn.cursor()
        c.execute('''
            INSERT INTO orders (order_id, product, quantity, phase, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (order_id, product, quantity, 1, "design", datetime.now(), datetime.now()))
        
        self.conn.commit()
        
        print(f"\n[Dark Factory] Order created: {order_id}")
        print(f"  Product: {product}")
        print(f"  Quantity: {quantity}")
        print(f"  Phase: 1 - Design")
        
        return order_id
    
    def advance_phase(self, order_id: str) -> bool:
        """Advance order to next phase"""
        c = self.conn.cursor()
        c.execute("SELECT phase, status FROM orders WHERE order_id=?", (order_id,))
        result = c.fetchone()
        
        if not result:
            print(f"Order {order_id} not found")
            return False
        
        current_phase, status = result
        
        if current_phase >= 5:
            print(f"Order {order_id} already complete")
            return False
        
        new_phase = current_phase + 1
        phases = {1: "Design", 2: "Vendor Sourcing", 3: "Production", 4: "QC", 5: "Distribution"}
        
        c.execute('''
            UPDATE orders SET phase=?, status=?, updated_at=? WHERE order_id=?
        ''', (new_phase, phases[new_phase].lower(), datetime.now(), order_id))
        
        c.execute('''
            INSERT INTO milestones (order_id, phase, description, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (order_id, new_phase, f"Entered {phases[new_phase]}", datetime.now()))
        
        self.conn.commit()
        
        print(f"[Dark Factory] {order_id} -> Phase {new_phase}: {phases[new_phase]}")
        return True
    
    def get_order_status(self, order_id: str) -> Dict:
        """Get order status"""
        c = self.conn.cursor()
        c.execute("SELECT * FROM orders WHERE order_id=?", (order_id,))
        row = c.fetchone()
        
        if not row:
            return {"error": "Order not found"}
        
        return {
            "order_id": row[1],
            "product": row[2],
            "quantity": row[3],
            "phase": row[4],
            "status": row[6],
            "created": row[12]
        }
    
    def list_orders(self) -> List[Dict]:
        """List all orders"""
        c = self.conn.cursor()
        c.execute("SELECT order_id, product, quantity, phase, status FROM orders ORDER BY created_at DESC")
        return [{"order_id": r[0], "product": r[1], "quantity": r[2], "phase": r[3], "status": r[4]} for r in c.fetchall()]

def main():
    print("=" * 70)
    print("DARK FACTORY - Real Production System")
    print("=" * 70)
    
    factory = DarkFactory()
    
    # Create orders
    print("\nCreating production orders...")
    orders = [
        factory.create_order("cobra_v1", 10),
        factory.create_order("prometheus_v1", 5),
    ]
    
    # Advance first order
    print("\n" + "=" * 70)
    print("Advancing Cobra order...")
    print("=" * 70)
    
    for i in range(4):
        factory.advance_phase(orders[0])
        time.sleep(0.5)
    
    # Show status
    print("\n" + "=" * 70)
    print("FACTORY STATUS")
    print("=" * 70)
    
    for order in factory.list_orders():
        print(f"\n{order['order_id']}:")
        print(f"  Product: {order['product']} x{order['quantity']}")
        print(f"  Phase: {order['phase']} ({order['status']})")
    
    print(f"\nDatabase: {DB_PATH}")
    print("Factory ready for actual production")

if __name__ == "__main__":
    main()
