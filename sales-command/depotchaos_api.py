#!/usr/bin/env python3
"""DepotChaos API Client - Full Integration"""
import json
import requests
from datetime import datetime
from pathlib import Path

DEPOTCHAOS_API = "https://psdepot.com/depotchaos/api"

class DepotChaosAPI:
    def __init__(self):
        self.base = DEPOTCHAOS_API
        self.cache_dir = Path(__file__).parent / "data"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get_stats(self):
        """Get all stats"""
        resp = requests.get(f"{self.base}/stats", timeout=10)
        return resp.json()
    
    def get_leads(self, page=1, limit=100):
        """Get leads"""
        resp = requests.get(f"{self.base}/leads", params={"page": page, "limit": limit}, timeout=10)
        return resp.json()
    
    def update_lead(self, lead_id, data):
        """Update a lead"""
        resp = requests.put(f"{self.base}/leads/{lead_id}", json=data, timeout=10)
        return resp.json()
    
    def add_note(self, lead_id, note):
        """Add note to lead"""
        resp = requests.post(f"{self.base}/leads/{lead_id}/notes", json={"note": note}, timeout=10)
        return resp.json()
    
    def sync_to_sales_center(self):
        """Sync leads to our sales command center"""
        stats = self.get_stats()
        
        # Save to cache
        cache_file = self.cache_dir / "depotchaos_stats.json"
        with open(cache_file, 'w') as f:
            json.dump(stats, f, indent=2)
        
        # Get sample leads
        leads_data = self.get_leads(limit=100)
        
        leads_cache = self.cache_dir / "depotchaos_leads.json"
        with open(leads_cache, 'w') as f:
            json.dump(leads_data, f, indent=2)
        
        return stats, leads_data
    
    def print_report(self):
        """Full report"""
        stats = self.get_stats()
        
        print("\n" + "="*60)
        print("📦 DEPOTCHAOS CRM — LIVE DATA FROM MILES")
        print("="*60)
        print(f"  Connected: {datetime.now().strftime('%H:%M:%S')}")
        print("")
        
        print(f"  📊 DATABASE")
        print(f"    Total Leads:      {stats['total_leads']:>10,}")
        print(f"    New Today:        {stats['new_today']:>10,}")
        print(f"    Intelligence:     {stats['intelligence_records']:>10,}")
        print(f"    DataDepot:        {stats['datadepot_leads']:>10,}")
        print("")
        
        print(f"  📈 BY STATUS")
        for status, count in stats['by_status'].items():
            if count > 0:
                print(f"    {status or 'unknown':15} {count:>10,}")
        print("")
        
        print(f"  🎯 BY TIER")
        for tier, count in stats['by_tier'].items():
            if count > 0:
                print(f"    {tier or 'unassigned':15} {count:>10,}")
        print("")
        
        print(f"  ✅ CONVERSIONS: {stats['by_status'].get('converted', 0)}")
        print("="*60)
        
        return stats

if __name__ == "__main__":
    api = DepotChaosAPI()
    api.print_report()
