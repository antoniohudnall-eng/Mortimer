#!/usr/bin/env python3
"""Unified Command Center - ALL SYSTEMS"""
import json
from datetime import datetime
from pathlib import Path
import requests

def get_all_data():
    try:
        psd = requests.get("https://psdepot.com/psd-api/dashboard/overview", timeout=5).json()
    except: psd = {}
    try:
        coll = requests.get("https://psdepot.com/collections/api", timeout=5).json()
        invoices = coll.get("invoices", [])
        overdue = [i for i in invoices if i["status"] == "Overdue"]
        unpaid = [i for i in invoices if i["status"] == "Unpaid"]
        coll_out = sum(i["amount"] for i in overdue + unpaid)
        coll_over = len(overdue)
    except: coll_out = coll_over = 0
    try:
        depot = requests.get("https://psdepot.com/depotchaos/api/stats", timeout=5).json()
    except: depot = {}
    return psd, coll_out, coll_over, depot

def main():
    psd, coll_out, coll_over, depot = get_all_data()
    
    print("\n" + "═"*70)
    print("🏭 PERFORMANCE SUPPLY DEPOT — COMMAND CENTER")
    print("═"*70)
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("")
    
    # PSD Main
    print("  ┌" + "─"*33 + "┐")
    print("  │ 🏭 PERFORMANCE SUPPLY DEPOT        │")
    print("  ├" + "─"*33 + "┤")
    print(f"  │   Customers:      {psd.get('total_customers', 'N/A'):>10}    │")
    print(f"  │   Revenue:       ${psd.get('total_revenue_2025', 0):>9,.0f}    │")
    print(f"  │   Forecast:      ${18055:>9,.0f}    │")
    print("  └" + "─"*33 + "┘")
    
    print("")
    
    # DepotChaos
    print("  ┌" + "─"*33 + "┐")
    print("  │ 📦 DEPOTCHAOS CRM                  │")
    print("  ├" + "─"*33 + "┤")
    print(f"  │   Leads:          {depot.get('total_leads', 'N/A'):>10}    │")
    print(f"  │   Intelligence:  {depot.get('intelligence_records', 'N/A'):>10}    │")
    print("  └" + "─"*33 + "┘")
    
    print("")
    
    # Collections
    print("  ┌" + "─"*33 + "┐")
    print("  │ 💰 COLLECTIONS                     │")
    print("  ├" + "─"*33 + "┤")
    print(f"  │   Overdue:         {coll_over:>10}    │")
    print(f"  │   Outstanding:   ${coll_out:>9,.2f}    │")
    print("  └" + "─"*33 + "┘")
    
    print("")
    
    # Agent Sales
    print("  ┌" + "─"*33 + "┐")
    print("  │ 🤖 AGI AGENT SALES                 │")
    print("  ├" + "─"*33 + "┤")
    print(f"  │   Leads:          {49600 + depot.get('total_leads', 0):>10,}    │")
    print(f"  │   Sales:                11    │")
    print(f"  │   Revenue:       ${1667:>9,.2f}    │")
    print("  └" + "─"*33 + "┘")
    
    print("")
    
    # Total Value
    total = psd.get('total_revenue_2025', 0) + coll_out + 1667
    print(f"  💎 TOTAL VALUE: ${total:,.2f}")
    print("")
    print("═"*70)

if __name__ == "__main__":
    main()
