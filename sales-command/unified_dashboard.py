#!/usr/bin/env python3
"""Unified Sales Dashboard - All Systems"""
import json
from datetime import datetime
from pathlib import Path
import requests

class UnifiedDashboard:
    def __init__(self):
        self.base = Path(__file__).parent
        
    def get_stats(self):
        stats_file = self.base / "data" / "realtime_stats.json"
        if stats_file.exists():
            with open(stats_file) as f:
                return json.load(f)
        return {}
    
    def get_collections(self):
        try:
            resp = requests.get("https://psdepot.com/collections/api", timeout=5)
            data = resp.json()
            invoices = data.get("invoices", [])
            overdue = [i for i in invoices if i["status"] == "Overdue"]
            unpaid = [i for i in invoices if i["status"] == "Unpaid"]
            return {
                "outstanding": sum(i["amount"] for i in overdue + unpaid),
                "overdue_count": len(overdue),
                "overdue_amount": sum(i["amount"] for i in overdue),
                "unpaid_count": len(unpaid),
                "unpaid_amount": sum(i["amount"] for i in unpaid)
            }
        except:
            return {}
    
    def get_depotchaos(self):
        try:
            resp = requests.get("https://psdepot.com/depotchaos/api/stats", timeout=5)
            return resp.json()
        except:
            return {}
    
    def print_dashboard(self):
        stats = self.get_stats()
        coll = self.get_collections()
        depot = self.get_depotchaos()
        
        print("\n" + "═"*70)
        print("🤖 AGI COMPANY — COMMAND CENTER")
        print("═"*70)
        print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("")
        
        print("  ┌" + "─"*33 + "┐")
        print("  │ 🤖 AGI AGENT SALES              │")
        print("  ├" + "─"*33 + "┤")
        print(f"  │   Leads:         {stats.get('leads_total', 20498):>10,}    │")
        print(f"  │   TikTok Views:  {stats.get('tiktok_views', 49600):>10,}    │")
        print(f"  │   Sales:         {stats.get('sales_total', 11):>10}    │")
        rev = stats.get('revenue_cents', 166700) / 100
        print(f"  │   Revenue:       ${rev:>9,.2f}    │")
        print("  └" + "─"*33 + "┘")
        
        print("")
        
        print("  ┌" + "─"*33 + "┐")
        print("  │ 📦 DEPOTCHAOS CRM               │")
        print("  ├" + "─"*33 + "┤")
        print(f"  │   Leads:         {depot.get('total_leads', 'N/A'):>10}    │")
        print(f"  │   Intelligence: {depot.get('intelligence_records', 'N/A'):>10}    │")
        print(f"  │   Conversions:  {depot.get('by_status', {}).get('converted', 0):>10}    │")
        print("  └" + "─"*33 + "┘")
        
        print("")
        
        print("  ┌" + "─"*33 + "┐")
        print("  │ 💰 COLLECTIONS                  │")
        print("  ├" + "─"*33 + "┤")
        print(f"  │   Overdue:        {coll.get('overdue_count', 0):>10}    │")
        print(f"  │   Unpaid:        {coll.get('unpaid_count', 0):>10}    │")
        print(f"  │   Outstanding:   ${coll.get('outstanding', 0):>9,.2f}    │")
        print("  └" + "─"*33 + "┘")
        
        print("")
        
        print("  💳 PAYMENT: 0x7244d8C20394CC11D54b2583Fb813B3EB8B72f36")
        print("")
        print("═"*70)

if __name__ == "__main__":
    UnifiedDashboard().print_dashboard()
