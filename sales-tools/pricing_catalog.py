#!/usr/bin/env python3
"""AGI Agent Pricing Catalog"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class AgentTier:
    name: str
    emoji: str
    price: int  # cents
    price_monthly: int  # cents
    description: str
    capabilities: list
    response_time: str
    support: str

AGENTS = {
    "CLERK": AgentTier(
        name="Clerk",
        emoji="📋",
        price=9700,
        price_monthly=4900,
        description="Entry-level agent for basic tasks",
        capabilities=["Data entry", "Scheduling", "Email responses", "File organization"],
        response_time="< 30 seconds",
        support="Community"
    ),
    "GREET": AgentTier(
        name="Greet",
        emoji="🤝",
        price=14700,
        price_monthly=7900,
        description="Customer engagement specialist",
        capabilities=["Lead qualification", "Appointment setting", "Follow-ups", "CRM updates"],
        response_time="< 15 seconds",
        support="Email"
    ),
    "PERSONAL": AgentTier(
        name="Personal",
        emoji="👤",
        price=19700,
        price_monthly=9900,
        description="Dedicated personal assistant",
        capabilities=["All Greet features", "Project coordination", "Research", "Travel planning"],
        response_time="< 10 seconds",
        support="Priority Email"
    ),
    "VELVET": AgentTier(
        name="Velvet",
        emoji="🎩",
        price=24700,
        price_monthly=12900,
        description="Premium agent with advanced capabilities",
        capabilities=["All Personal features", "Multi-channel outreach", "Analytics", "Custom workflows"],
        response_time="< 5 seconds",
        support="Priority + Chat"
    ),
    "CONCIERGE": AgentTier(
        name="Concierge",
        emoji="🛎️",
        price=29700,
        price_monthly=15900,
        description="White-glove service agent",
        capabilities=["All Velvet features", "24/7 availability", "Dedicated line", "Executive support"],
        response_time="< 3 seconds",
        support="Dedicated"
    ),
    "EXECUTIVE": AgentTier(
        name="Executive",
        emoji="👑",
        price=49700,
        price_monthly=29900,
        description="Full-spectrum executive agent",
        capabilities=["All Concierge features", "Strategic planning", "Team coordination", "ROI reporting"],
        response_time="< 1 second",
        support="VIP Dedicated"
    ),
}

def format_price(cents, period="one-time"):
    if period == "monthly":
        return f"${cents/100:.0f}/mo"
    return f"${cents/100:.0f}"

def print_catalog():
    print("\n" + "="*70)
    print("🤖 AGI COMPANY — AGENT PRICING CATALOG")
    print("="*70)
    for agent_id, agent in AGENTS.items():
        print(f"\n{agent.emoji} {agent_id} — {agent.name}")
        print(f"   One-time: {format_price(agent.price)}")
        print(f"   Monthly:  {format_price(agent.price, 'monthly')}")
        print(f"   {agent.description}")
        print(f"   Response: {agent.response_time} | Support: {agent.support}")
    print("\n" + "="*70)

if __name__ == "__main__":
    print_catalog()
