#!/usr/bin/env python3
"""AGI Company Sales Funnel Manager"""
import json
import csv
from datetime import datetime
from pathlib import Path

LEADS_FILE = Path(__file__).parent / "leads" / "leads.json"
PROPOSALS_DIR = Path(__file__).parent / "proposals"

class SalesFunnel:
    def __init__(self):
        self.stages = ["Lead", "Contacted", "Qualified", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]
        self.leads = self.load_leads()
    
    def load_leads(self):
        if LEADS_FILE.exists():
            with open(LEADS_FILE) as f:
                return json.load(f)
        return {}
    
    def save_leads(self):
        PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
        with open(LEADS_FILE, 'w') as f:
            json.dump(self.leads, f, indent=2)
    
    def add_lead(self, name, email, company, source="tiktok"):
        lead_id = f"LEAD-{len(self.leads)+1:04d}"
        self.leads[lead_id] = {
            "id": lead_id,
            "name": name,
            "email": email,
            "company": company,
            "source": source,
            "stage": "Lead",
            "created": datetime.now().isoformat(),
            "notes": [],
            "agent_interest": None
        }
        self.save_leads()
        return lead_id
    
    def update_stage(self, lead_id, stage):
        if lead_id in self.leads and stage in self.stages:
            self.leads[lead_id]["stage"] = stage
            self.leads[lead_id]["updated"] = datetime.now().isoformat()
            self.save_leads()
            return True
        return False
    
    def get_pipeline_summary(self):
        summary = {stage: 0 for stage in self.stages}
        for lead in self.leads.values():
            summary[lead["stage"]] = summary.get(lead["stage"], 0) + 1
        return summary
    
    def print_pipeline(self):
        print("\n📊 SALES PIPELINE")
        print("=" * 50)
        summary = self.get_pipeline_summary()
        for stage, count in summary.items():
            bar = "█" * count
            print(f"  {stage:15} | {bar} {count}")
        print("=" * 50)
        print(f"  TOTAL LEADS:   | {len(self.leads)}")

if __name__ == "__main__":
    funnel = SalesFunnel()
    funnel.print_pipeline()
