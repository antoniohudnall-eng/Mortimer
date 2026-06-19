#!/usr/bin/env python3
"""Lead Generation Engine for AGI Sales"""
import random
import json
from datetime import datetime
from pathlib import Path

# Realistic business types for agent sales
BUSINESS_TYPES = ["SaaS Startup", "E-commerce", "Agency", "Consulting", "Real Estate", "Healthcare", "Finance", "Legal", "Marketing", "Tech Company"]
ROLES = ["Founder", "CEO", "CTO", "COO", "VP Operations", "Director of Ops", "Operations Manager", "Executive Assistant"]
STATES = ["CA", "TX", "FL", "NY", "IL", "PA", "OH", "GA", "NC", "MI"]

FIRST_NAMES = ["James", "Michael", "Robert", "David", "William", "Jennifer", "Linda", "Patricia", "Elizabeth", "Barbara", "Maria", "Sarah", "Jessica", "Karen", "Lisa"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Anderson", "Taylor", "Thomas", "Moore", "Jackson"]

def generate_lead(source="generated"):
    return {
        "id": f"LEAD-{random.randint(10000, 99999)}",
        "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
        "email": f"contact@{random.choice(FIRST_NAMES).lower()}{random.choice(LAST_NAMES).lower()}.com",
        "phone": f"555-{random.randint(100,999)}-{random.randint(1000,9999)}",
        "company": f"{random.choice(['Apex', 'Global', 'Prime', 'Elite', 'Summit', 'Nova', 'Vertex', 'Pinnacle', 'Horizon', 'Atlas'])} {random.choice(['Solutions', 'Systems', 'Group', 'Partners', 'Ventures', 'Corp', 'Inc', 'Labs'])}",
        "business_type": random.choice(BUSINESS_TYPES),
        "role": random.choice(ROLES),
        "state": random.choice(STATES),
        "employees": random.choice(["1-10", "11-50", "51-200", "201-500", "500+"]),
        "agent_interest": random.choice(["CLERK", "GREET", "PERSONAL", "VELVET", "CONCIERGE", "EXECUTIVE", None]),
        "source": source,
        "score": random.randint(1, 100),
        "created": datetime.now().isoformat()
    }

def generate_leads(count=1000):
    return [generate_lead() for _ in range(count)]

if __name__ == "__main__":
    leads = generate_leads(1000)
    print(f"✅ Generated {len(leads)} leads")
    
    # Save to cache
    cache = Path(__file__).parent / "data" / "generated_leads.json"
    cache.parent.mkdir(parents=True, exist_ok=True)
    with open(cache, 'w') as f:
        json.dump(leads, f, indent=2)
    print(f"💾 Saved to {cache}")
