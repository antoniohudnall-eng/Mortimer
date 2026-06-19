#!/usr/bin/env python3
"""
AGI COMPANY SALES COMMAND CENTER
=================================
Unified sales pipeline leveraging:
- 7,872+ existing leads from AOS-Brain
- Agent sales pipeline (TikTok)
- Pricing catalog
- Invoice generation
"""

import json
import sqlite3
import csv
from datetime import datetime
from pathlib import Path

class SalesCommandCenter:
    def __init__(self):
        self.base = Path(__file__).parent
        self.db_path = self.base / "data" / "sales.db"
        self.leads_cache = self.base / "data" / "leads_cache.json"
        self.init_db()
        self.load_leads()
    
    def init_db(self):
        """Initialize sales database"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        # Leads with TikTok attribution
        c.execute('''CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY,
            name TEXT, email TEXT, phone TEXT,
            company TEXT, source TEXT,
            status TEXT DEFAULT 'new',
            stage TEXT DEFAULT 'lead',
            agent_interest TEXT,
            tiktok_video_id TEXT,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated TIMESTAMP
        )''')
        
        # Agent sales
        c.execute('''CREATE TABLE IF NOT EXISTS agent_sales (
            id INTEGER PRIMARY KEY,
            lead_id INTEGER,
            agent_type TEXT,
            amount_cents INTEGER,
            status TEXT DEFAULT 'pending',
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Communications
        c.execute('''CREATE TABLE IF NOT EXISTS comms (
            id INTEGER PRIMARY KEY,
            lead_id INTEGER,
            direction TEXT,
            channel TEXT,
            message TEXT,
            response TEXT,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        conn.commit()
        conn.close()
    
    def load_leads(self):
        """Load existing leads from AOS-Brain"""
        if self.leads_cache.exists():
            with open(self.leads_cache) as f:
                data = json.load(f)
                print(f"📥 Loaded {len(data)} leads from cache")
                return data
        
        # Load from AOS-Brain
        leads = []
        consolidated = Path("/data/data/com.termux/files/home/AOS-Brain/AGI_COMPANY/data/leads_consolidated")
        
        if consolidated.exists():
            for csv_file in consolidated.glob("COMPLETED_*.csv"):
                try:
                    with open(csv_file) as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            leads.append({
                                "name": row.get("name", ""),
                                "email": row.get("email", ""),
                                "phone": row.get("phone", ""),
                                "company": row.get("business", row.get("company", "")),
                                "state": row.get("state", ""),
                                "source": "aosbrain"
                            })
                except Exception as e:
                    print(f"⚠️ Error reading {csv_file}: {e}")
        
        # Cache for next time
        with open(self.leads_cache, 'w') as f:
            json.dump(leads, f)
        
        print(f"📥 Loaded {len(leads)} leads from AOS-Brain")
        return leads
    
    def import_lead(self, name, email, phone="", company="", source="tiktok", agent_interest=""):
        """Add new lead"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute('''INSERT INTO leads (name, email, phone, company, source, agent_interest)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (name, email, phone, company, source, agent_interest))
        lead_id = c.lastrowid
        conn.commit()
        conn.close()
        return lead_id
    
    def create_agent_sale(self, lead_id, agent_type, amount_cents):
        """Create agent sale"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute('''INSERT INTO agent_sales (lead_id, agent_type, amount_cents)
                     VALUES (?, ?, ?)''',
                  (lead_id, agent_type, amount_cents))
        sale_id = c.lastrowid
        conn.commit()
        conn.close()
        return sale_id
    
    def get_pipeline_summary(self):
        """Get pipeline stats"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        stages = {}
        for row in c.execute('SELECT stage, COUNT(*) FROM leads GROUP BY stage'):
            stages[row[0]] = row[1]
        
        total = sum(stages.values())
        
        agent_sales = {}
        for row in c.execute('SELECT agent_type, COUNT(*), SUM(amount_cents) FROM agent_sales GROUP BY agent_type'):
            agent_sales[row[0]] = {"count": row[1], "revenue": row[2] or 0}
        
        conn.close()
        
        return {
            "total_leads": total,
            "by_stage": stages,
            "agent_sales": agent_sales,
            "total_revenue": sum(s["revenue"] for s in agent_sales.values())
        }
    
    def print_dashboard(self):
        """Print command center dashboard"""
        summary = self.get_pipeline_summary()
        leads = self.load_leads()
        
        print("\n" + "="*60)
        print("🤖 AGI COMPANY SALES COMMAND CENTER")
        print("="*60)
        
        print(f"\n📊 PIPELINE SUMMARY")
        print("-"*40)
        print(f"  Total Leads:        {summary['total_leads']}")
        print(f"  AOS-Brain Cache:    {len(leads)}")
        
        print(f"\n📈 STAGE BREAKDOWN")
        print("-"*40)
        for stage, count in summary.get("by_stage", {}).items():
            bar = "█" * min(count, 20)
            print(f"  {stage:15} {bar} {count}")
        
        print(f"\n🤖 AGENT SALES")
        print("-"*40)
        for agent, data in summary.get("agent_sales", {}).items():
            revenue = data["revenue"] / 100
            print(f"  {agent:12} {data['count']:3} sold | ${revenue:,.2f}")
        
        total_rev = summary.get("total_revenue", 0) / 100
        print(f"\n  💰 TOTAL REVENUE: ${total_rev:,.2f}")
        
        print("\n" + "="*60)
        return summary

if __name__ == "__main__":
    center = SalesCommandCenter()
    center.print_dashboard()
