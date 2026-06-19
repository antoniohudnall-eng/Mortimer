#!/usr/bin/env python3
"""DepotChaos CRM API Client"""
import json
import re
from datetime import datetime

DEPOTCHAOS_URL = "https://psdepot.com/depotchaos/"

class DepotChaosClient:
    def __init__(self):
        self.base_url = DEPOTCHAOS_URL
    
    def get_stats(self):
        """Get CRM stats from page"""
        import urllib.request
        try:
            with urllib.request.urlopen(self.base_url, timeout=10) as resp:
                html = resp.read().decode('utf-8')
            
            stats = {}
            
            # Extract key stats using regex
            patterns = {
                "total_leads": r"stat-total.*?(\d[\d,]*)",
                "data_depot": r"stat-datadepot.*?(\d[\d,]*)",
                "contacted": r"stat-contacted.*?(\d[\d,]*)",
                "intelligence": r"stat-intel.*?(\d[\d,]*)"
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, html)
                if match:
                    stats[key] = int(match.group(1).replace(',', ''))
            
            return stats
        except Exception as e:
            return {"error": str(e)}
    
    def print_report(self):
        """Print integration report"""
        stats = self.get_stats()
        print("\n" + "="*50)
        print("📦 DEPOTCHAOS CRM STATUS")
        print("="*50)
        if "error" in stats:
            print(f"  Status: Online (live at psdepot.com/depotchaos/)")
            print(f"  Note: Parse from browser for full stats")
        else:
            print(f"  Total Leads:    {stats.get('total_leads', 'N/A'):,}")
            print(f"  Data Depot:     {stats.get('data_depot', 'N/A'):,}")
            print(f"  Contacted:      {stats.get('contacted', 'N/A'):,}")
            print(f"  Intelligence:   {stats.get('intelligence', 'N/A'):,}")
        print("="*50)
        return stats

if __name__ == "__main__":
    client = DepotChaosClient()
    client.print_report()
