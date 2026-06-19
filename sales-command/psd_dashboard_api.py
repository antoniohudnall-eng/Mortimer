#!/usr/bin/env python3
"""PSD Dashboard API - Full Company Dashboard"""
import json
import requests
from datetime import datetime
from pathlib import Path

PSD_API = "https://psdepot.com/psd-api"

class PSDDashboardAPI:
    def __init__(self):
        self.base = PSD_API
        self.cache_dir = Path(__file__).parent / "data"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get_overview(self):
        """Get dashboard overview"""
        resp = requests.get(f"{self.base}/dashboard/overview", timeout=10)
        return resp.json()
    
    def get_system_dist(self):
        """Get system distribution"""
        resp = requests.get(f"{self.base}/dashboard/system-distribution", timeout=10)
        return resp.json()
    
    def get_forecast(self, year=2026):
        """Get revenue forecast"""
        resp = requests.get(f"{self.base}/forecast/{year}", timeout=10)
        return resp.json()
    
    def get_customers(self, limit=100):
        """Get customers"""
        resp = requests.get(f"{self.base}/customers", params={"limit": limit}, timeout=10)
        return resp.json()
    
    def analyze(self):
        """Full analysis"""
        overview = self.get_overview()
        forecast = self.get_forecast()
        customers = self.get_customers(limit=10)
        
        return {
            "total_customers": overview["total_customers"],
            "active_customers": overview["active_customers"],
            "total_revenue": overview["total_revenue_2025"],
            "avg_monthly": overview["avg_monthly_revenue"],
            "by_category": overview["by_category"],
            "by_tier": overview["by_tier"],
            "forecast_2026": forecast["total_2026_projected"],
            "sample_customers": customers["customers"][:5]
        }
    
    def print_report(self):
        """Full report"""
        data = self.analyze()
        
        print("\n" + "="*60)
        print("🏭 PERFORMANCE SUPPLY DEPOT — DASHBOARD")
        print("="*60)
        print(f"  Timestamp: {datetime.now().strftime('%H:%M:%S')}")
        print("")
        
        print(f"  👥 CUSTOMERS")
        print(f"    Total:       {data['total_customers']:,}")
        print(f"    Active:      {data['active_customers']:,}")
        print("")
        
        print(f"  💰 REVENUE")
        print(f"    Total (2022-2025):  ${data['total_revenue']:,.2f}")
        print(f"    Avg Monthly:         ${data['avg_monthly']:,.2f}")
        print(f"    Forecast (2026):   ${data['forecast_2026']:,.2f}")
        print("")
        
        print(f"  🎯 BY TIER")
        for tier, count in data["by_tier"].items():
            print(f"    {tier:10} {count:,}")
        print("")
        
        print(f"  🍽️  TOP CATEGORIES")
        sorted_cats = sorted(data["by_category"].items(), key=lambda x: -x[1])[:5]
        for cat, count in sorted_cats:
            print(f"    {cat:15} {count}")
        print("="*60)
        
        return data

if __name__ == "__main__":
    PSDDashboardAPI().print_report()
