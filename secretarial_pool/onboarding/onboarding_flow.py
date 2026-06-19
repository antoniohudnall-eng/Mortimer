#!/usr/bin/env python3
"""
Client Onboarding Flow
Automated welcome sequence for new secretarial clients
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional

ONBOARDING_STEPS = [
    {
        "step": 1,
        "name": "Welcome Email",
        "description": "Send welcome email with agent introduction",
        "template": "welcome_email.txt",
        "automated": True
    },
    {
        "step": 2,
        "name": "Agent Assignment",
        "description": "Assign appropriate agent based on tier",
        "template": "agent_intro.txt",
        "automated": True
    },
    {
        "step": 3,
        "name": "Requirements Collection",
        "description": "Gather client needs and preferences",
        "template": "intake_form.txt",
        "automated": True
    },
    {
        "step": 4,
        "name": "Agent Configuration",
        "description": "Configure agent voice, personality, tasks",
        "template": "setup_config.json",
        "automated": False
    },
    {
        "step": 5,
        "name": "First Task Assignment",
        "description": "Assign first real task to agent",
        "template": "first_task.txt",
        "automated": True
    },
    {
        "step": 6,
        "name": "Status Check (Day 3)",
        "description": "Follow up on agent performance",
        "template": "checkin_day3.txt",
        "automated": True
    },
    {
        "step": 7,
        "name": "Status Check (Day 7)",
        "description": "Week 1 review and optimization",
        "template": "checkin_day7.txt",
        "automated": True
    }
]

WELCOME_EMAIL = """
Hi {name},

Welcome to the Secretarial Pool! 🎉

You've selected {agent_name} ({agent_tier}) as your new {role}.

WHAT HAPPENS NEXT:
1. You'll receive your agent's introduction shortly
2. Share your first task or request
3. We'll configure your agent to match your style

YOUR AGENT CAN:
- Handle emails and inquiries
- Manage schedules and appointments
- Respond to clients 24/7
- Process orders and requests
- And much more...

Questions? Just reply to this email.

Best,
The Secretarial Pool Team

---
Tier: {agent_tier}
Price: ${price}/month
"""

class OnboardingManager:
    def __init__(self, data_dir: str = "clients"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs("templates", exist_ok=True)
    
    def create_client(self, email: str, name: str, tier: str, payment_tx: str = "") -> Dict:
        """Create new client profile"""
        
        client = {
            "client_id": f"CLI-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "email": email,
            "name": name,
            "tier": tier,
            "agent_assigned": None,
            "payment_tx": payment_tx,
            "status": "onboarding",
            "onboarding_step": 0,
            "created": datetime.now().isoformat(),
            "completed_steps": []
        }
        
        # Save client profile
        client_file = f"{self.data_dir}/{email.replace('@', '_at_')}.json"
        with open(client_file, 'w') as f:
            json.dump(client, f, indent=2)
        
        return client
    
    def assign_agent(self, client_email: str) -> Dict:
        """Assign an agent to a client"""
        
        agent_map = {
            "clerk": "CLERK",
            "greet": "GREET", 
            "personal": "PERSONAL",
            "velvet": "VELVET",
            "concierge": "CONCIERGE",
            "executive": "EXECUTIVE"
        }
        
        # Load client
        client_file = f"{self.data_dir}/{client_email.replace('@', '_at_')}.json"
        if not os.path.exists(client_file):
            return {"error": "Client not found"}
        
        with open(client_file, 'r') as f:
            client = json.load(f)
        
        tier = client.get("tier", "clerk")
        agent_name = agent_map.get(tier, "CLERK")
        
        client["agent_assigned"] = agent_name
        client["onboarding_step"] = 2
        
        # Save updated client
        with open(client_file, 'w') as f:
            json.dump(client, f, indent=2)
        
        return {
            "client": client_email,
            "agent": agent_name,
            "status": "assigned"
        }
    
    def advance_step(self, client_email: str) -> Dict:
        """Advance onboarding to next step"""
        
        client_file = f"{self.data_dir}/{client_email.replace('@', '_at_')}.json"
        if not os.path.exists(client_file):
            return {"error": "Client not found"}
        
        with open(client_file, 'r') as f:
            client = json.load(f)
        
        step = client.get("onboarding_step", 0)
        if step < len(ONBOARDING_STEPS):
            step += 1
            client["onboarding_step"] = step
            client["completed_steps"].append(step)
        
        if step == len(ONBOARDING_STEPS):
            client["status"] = "active"
        
        with open(client_file, 'w') as f:
            json.dump(client, f, indent=2)
        
        return {
            "client": client_email,
            "current_step": step,
            "status": client["status"]
        }
    
    def get_client_status(self, client_email: str) -> Dict:
        """Get full onboarding status"""
        
        client_file = f"{self.data_dir}/{client_email.replace('@', '_at_')}.json"
        if not os.path.exists(client_file):
            return {"error": "Client not found"}
        
        with open(client_file, 'r') as f:
            client = json.load(f)
        
        return {
            "client_id": client["client_id"],
            "name": client["name"],
            "tier": client["tier"],
            "agent": client.get("agent_assigned", "pending"),
            "status": client["status"],
            "onboarding_step": client["onboarding_step"],
            "total_steps": len(ONBOARDING_STEPS),
            "progress_pct": round((client["onboarding_step"] / len(ONBOARDING_STEPS)) * 100, 1)
        }


if __name__ == "__main__":
    manager = OnboardingManager()
    
    # Demo: Create a test client
    print("👤 Creating test client...")
    client = manager.create_client(
        email="test@example.com",
        name="Test User",
        tier="executive"
    )
    print(f"   Created: {client['client_id']}")
    
    # Assign agent
    print("\n🤖 Assigning agent...")
    result = manager.assign_agent("test@example.com")
    print(f"   Assigned: {result['agent']}")
    
    # Check status
    print("\n📊 Onboarding Status:")
    status = manager.get_client_status("test@example.com")
    for key, value in status.items():
        print(f"   {key}: {value}")
