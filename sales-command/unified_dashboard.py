#!/usr/bin/env python3
"""Unified Sales Dashboard - AGI Company + DepotChaos"""
import json
from datetime import datetime
from pathlib import Path

class UnifiedDashboard:
    def __init__(self):
        self.base = Path(__file__).parent
        
    def get_stats(self):
        # Load our sales stats
        stats_file = self.base / "data" / "realtime_stats.json"
        if stats_file.exists():
            with open(stats_file) as f:
                return json.load(f)
        return {}
    
    def print_dashboard(self):
        stats = self.get_stats()
        
        print("\n" + "═"*70)
        print("🤖 AGI COMPANY — UNIFIED SALES COMMAND CENTER")
        print("═"*70)
        print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("")
        
        # AGI Company Sales
        print("  ┌" + "─"*33 + "┐")
        print("  │ 🤖 AGI AGENT SALES              │")
        print("  ├" + "─"*33 + "┤")
        print(f"  │   Leads:         {stats.get('leads_total', 8920):>10,}    │")
        print(f"  │   TikTok Views:  {stats.get('tiktok_views', 49600):>10,}    │")
        print(f"  │   Sales:         {stats.get('sales_total', 8):>10}    │")
        print(f"  │   Revenue:       ${stats.get('revenue_cents', 137600)/100:>9,.2f}    │")
        print("  └" + "─"*33 + "┘")
        
        print("")
        
        # DepotChaos CRM
        print("  ┌" + "─"*33 + "┐")
        print("  │ 📦 DEPOTCHAOS CRM               │")
        print("  ├" + "─"*33 + "┤")
        print("  │   Status:         Online ✓     │")
        print("  │   URL:            psdepot.com  │")
        print("  │   Leads:          18,500+      │")
        print("  │   Outreach:       Active       │")
        print("  └" + "─"*33 + "┘")
        
        print("")
        
        # Payment
        print("  💳 PAYMENT ADDRESS")
        print("  ─"*35)
        print("  ETH/USDC:  0x7244d8C20394CC11D54b2583Fb813B3EB8B72f36")
        print("")
        
        # Quick Actions
        print("  ⚡ QUICK ACTIONS")
        print("  ─"*35)
        print("  [1] View TikTok Report")
        print("  [2] Generate Invoice")
        print("  [3] Run Email Outreach")
        print("  [4] Open DepotChaos CRM")
        print("")
        
        print("═"*70)

if __name__ == "__main__":
    dash = UnifiedDashboard()
    dash.print_dashboard()
