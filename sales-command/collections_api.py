#!/usr/bin/env python3
"""PSDepot Collections API Client"""
import json
import requests
from datetime import datetime
from pathlib import Path

COLLECTIONS_API = "https://psdepot.com/collections/api"

class CollectionsAPI:
    def __init__(self):
        self.base = COLLECTIONS_API
        self.cache_dir = Path(__file__).parent / "data"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get_invoices(self):
        """Get all invoices"""
        resp = requests.get(self.base, timeout=10)
        return resp.json()
    
    def analyze(self):
        """Analyze collections"""
        data = self.get_invoices()
        invoices = data["invoices"]
        
        overdue = [i for i in invoices if i["status"] == "Overdue"]
        unpaid = [i for i in invoices if i["status"] == "Unpaid"]
        draft = [i for i in invoices if i["status"] == "Draft"]
        
        return {
            "total": len(invoices),
            "overdue_count": len(overdue),
            "overdue_total": sum(i["amount"] for i in overdue),
            "unpaid_count": len(unpaid),
            "unpaid_total": sum(i["amount"] for i in unpaid),
            "draft_count": len(draft),
            "draft_total": sum(i["amount"] for i in draft),
            "outstanding": sum(i["amount"] for i in overdue + unpaid),
            "critical": sum(i["amount"] for i in invoices if i["days"] > 30),
            "last_updated": data["lastUpdated"]
        }
    
    def print_report(self):
        """Full report"""
        stats = self.analyze()
        
        print("\n" + "="*60)
        print("💰 PSDEPOT COLLECTIONS — LIVE FROM MILES")
        print("="*60)
        print(f"  Last Updated: {stats['last_updated'][:19]}")
        print("")
        print(f"  📊 SUMMARY")
        print(f"    Total Invoices:  {stats['total']}")
        print(f"    Overdue:        {stats['overdue_count']} (${stats['overdue_total']:,.2f})")
        print(f"    Unpaid:         {stats['unpaid_count']} (${stats['unpaid_total']:,.2f})")
        print(f"    Draft:          {stats['draft_count']} (${stats['draft_total']:,.2f})")
        print("")
        print(f"  ⚠️  OUTSTANDING:  ${stats['outstanding']:,.2f}")
        print(f"  🚨 CRITICAL:     ${stats['critical']:,.2f}")
        print("="*60)
        
        return stats

if __name__ == "__main__":
    api = CollectionsAPI()
    api.print_report()
