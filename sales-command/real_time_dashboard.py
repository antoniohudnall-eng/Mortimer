#!/usr/bin/env python3
"""Real-time Sales Dashboard"""
import json
from datetime import datetime
from pathlib import Path

class RealtimeDashboard:
    def __init__(self):
        self.base = Path(__file__).parent
        self.stats_file = self.base / "data" / "realtime_stats.json"
        self.load_stats()
    
    def load_stats(self):
        if self.stats_file.exists():
            with open(self.stats_file) as f:
                self.stats = json.load(f)
        else:
            self.stats = self.init_stats()
    
    def init_stats(self):
        return {
            "leads_total": 8820,
            "leads_new": 0,
            "tiktok_views": 49600,
            "tiktok_leads": 84,
            "emails_sent": 0,
            "sales_total": 8,
            "revenue_cents": 137600,
            "conversion_rate": 0.17,
            "last_updated": datetime.now().isoformat()
        }
    
    def update(self, key, value):
        self.stats[key] = value
        self.stats["last_updated"] = datetime.now().isoformat()
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def add_sale(self, agent_type, amount_cents):
        self.stats["sales_total"] += 1
        self.stats["revenue_cents"] += amount_cents
        self.stats["conversion_rate"] = round(self.stats["tiktok_leads"] / self.stats["tiktok_views"] * 100, 2)
        self.stats["last_updated"] = datetime.now().isoformat()
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def print_dashboard(self):
        print("\n" + "═"*60)
        print("🤖 AGI COMPANY — REAL-TIME SALES DASHBOARD")
        print("═"*60)
        print(f"  Last Updated: {self.stats['last_updated'][:19]}")
        print("")
        print("  📈 PIPELINE")
        print(f"    Total Leads:      {self.stats['leads_total']:,}")
        print(f"    New Today:        {self.stats['leads_new']}")
        print("")
        print("  📱 TIKTOK")
        print(f"    Total Views:      {self.stats['tiktok_views']:,}")
        print(f"    Leads Captured:  {self.stats['tiktok_leads']}")
        print(f"    Conversion Rate: {self.stats['conversion_rate']}%")
        print("")
        print("  📧 OUTREACH")
        print(f"    Emails Sent:     {self.stats['emails_sent']}")
        print("")
        print("  💰 REVENUE")
        print(f"    Total Sales:     {self.stats['sales_total']}")
        print(f"    Revenue:         ${self.stats['revenue_cents']/100:,.2f}")
        print("")
        print("  💳 PAYMENT ADDRESS")
        print("    ETH/USDC:        0x7244d8C20394CC11D54b2583Fb813B3EB8B72f36")
        print("═"*60)

if __name__ == "__main__":
    dash = RealtimeDashboard()
    dash.print_dashboard()
