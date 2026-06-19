#!/usr/bin/env python3
"""
TikTok Agent Sales Tracker
===========================
Track video performance and lead attribution
"""

import json
from datetime import datetime
from pathlib import Path

VIDEO_FILE = Path(__file__).parent / "data" / "videos.json"
LEADS_FILE = Path(__file__).parent / "data" / "tiktok_leads.json"

def load_json(path, default=None):
    if default is None:
        default = []
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

# Agent pricing
AGENT_PRICE = {"CLERK": 97, "GREET": 147, "PERSONAL": 197, "VELVET": 247, "CONCIERGE": 297, "EXECUTIVE": 497}

def get_videos():
    return load_json(VIDEO_FILE, [
        {"id": "v001", "agent": "CLERK", "price": 97, "views": 12400, "leads": 23, "sales": 2},
        {"id": "v002", "agent": "GREET", "price": 147, "views": 8900, "leads": 15, "sales": 1},
        {"id": "v003", "agent": "PERSONAL", "price": 197, "views": 15200, "leads": 31, "sales": 4},
        {"id": "v004", "agent": "VELVET", "price": 247, "views": 6700, "leads": 8, "sales": 1},
        {"id": "v005", "agent": "CONCIERGE", "price": 297, "views": 4300, "leads": 5, "sales": 0},
        {"id": "v006", "agent": "EXECUTIVE", "price": 497, "views": 2100, "leads": 2, "sales": 0},
    ])

def track_video(video_id, views, leads, sales):
    """Update video stats"""
    videos = get_videos()
    for v in videos:
        if v["id"] == video_id:
            v["views"] = views
            v["leads"] = leads
            v["sales"] = sales
            v["updated"] = datetime.now().isoformat()
            break
    save_json(VIDEO_FILE, videos)
    return True

def add_lead(name, email, phone, agent_interest, source_video=""):
    """Add TikTok lead"""
    leads = load_json(LEADS_FILE, [])
    lead = {
        "id": f"TL-{len(leads)+1:04d}",
        "name": name,
        "email": email,
        "phone": phone,
        "agent": agent_interest,
        "source": source_video,
        "created": datetime.now().isoformat(),
        "status": "new"
    }
    leads.append(lead)
    save_json(LEADS_FILE, leads)
    return lead

def print_report():
    videos = get_videos()
    print("\n" + "="*70)
    print("📱 TIKTOK AGENT SALES REPORT")
    print("="*70)
    print(f"{'AGENT':<12} {'PRICE':>8} {'VIEWS':>10} {'LEADS':>8} {'SALES':>8} {'CONV%':>8} {'REVENUE':>10}")
    print("-"*70)
    
    total_views = total_leads = total_sales = total_revenue = 0
    
    for v in videos:
        conv = (v["leads"] / v["views"] * 100) if v["views"] > 0 else 0
        rev = v["sales"] * AGENT_PRICE.get(v["agent"], 0)
        
        total_views += v["views"]
        total_leads += v["leads"]
        total_sales += v["sales"]
        total_revenue += rev
        
        print(f"{v['agent']:<12} ${v['price']:<7} {v['views']:>10,} {v['leads']:>8} {v['sales']:>8} {conv:>7.1f}% ${rev:>9,.2f}")
    
    print("-"*70)
    print(f"{'TOTAL':<12} {'':<8} {total_views:>10,} {total_leads:>8} {total_sales:>8} {(total_leads/total_views*100) if total_views else 0:>7.1f}% ${total_revenue:>9,.2f}")
    print("="*70)

if __name__ == "__main__":
    print_report()
