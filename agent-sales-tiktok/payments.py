#!/usr/bin/env python3
"""
💰 PAYMENT COLLECTION SYSTEM
Agent Sales TikTok - Fund Collection

Methods:
1. Stripe - Subscriptions (SaaS agents)
2. PayPal - One-time & subscriptions
3. Link in Bio - Cart.com, Beacons, etc.
4. TikTok Shop - Native (when available)
"""

import os
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

# Agent pricing
AGENT_PRICING = {
    "clerk": {"price": 97, "name": "CLERK", "interval": "monthly"},
    "greet": {"price": 147, "name": "GREET", "interval": "monthly"},
    "personal": {"price": 197, "name": "PERSONAL", "interval": "monthly"},
    "velvet": {"price": 247, "name": "VELVET", "interval": "monthly"},
    "concierge": {"price": 297, "name": "CONCIERGE", "interval": "monthly"},
    "executive": {"price": 497, "name": "EXECUTIVE", "interval": "monthly"},
}

# One-time setup fees
SETUP_FEES = {
    "basic": 99,
    "pro": 299,
    "enterprise": 999,
}

@dataclass
class PaymentLink:
    agent: str
    price: int
    interval: str
    url: str
    method: str  # stripe, paypal, link

@dataclass
class Lead:
    tiktok_handle: str
    agent_interest: str
    email: Optional[str] = None
    timestamp: str = None
    status: str = "new"  # new, contacted, converted, paid

class PaymentCollector:
    """
    Collect payments for AI agents sold via TikTok
    
    Flow:
    1. TikTok video → Link in Bio (cart.com/beacons)
    2. Potential customer → Landing page
    3. Checkout → Stripe/PayPal
    4. Welcome email → Agent delivery
    """
    
    def __init__(self, config_dir: str = "~/.mortimer/payments"):
        self.config_dir = Path(config_dir).expanduser()
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.leads_file = self.config_dir / "leads.json"
        self.orders_file = self.config_dir / "orders.json"
        self.config_file = self.config_dir / "config.json"
        
        self.leads = self._load_leads()
        self.orders = self._load_orders()
        self.config = self._load_config()
    
    def _load_leads(self) -> List[Lead]:
        if self.leads_file.exists():
            return [Lead(**l) for l in json.loads(self.leads_file.read_text())]
        return []
    
    def _load_orders(self) -> List[dict]:
        if self.orders_file.exists():
            return json.loads(self.orders_file.read_text())
        return []
    
    def _load_config(self) -> dict:
        if self.config_file.exists():
            return json.loads(self.config_file.read_text())
        return {
            "stripe_key": os.environ.get("STRIPE_API_KEY", ""),
            "paypal_client_id": os.environ.get("PAYPAL_CLIENT_ID", ""),
            "landing_page_url": "https://agentfleet.com/checkout",
            "link_in_bio": "beacons.ai/agentfleet",
        }
    
    def _save_leads(self):
        self.leads_file.write_text(json.dumps([l.__dict__ for l in self.leads], indent=2))
    
    def _save_orders(self):
        self.orders_file.write_text(json.dumps(self.orders, indent=2))
    
    def generate_payment_links(self) -> dict:
        """Generate payment links for all agents"""
        links = {}
        
        # Stripe (if configured)
        if self.config.get("stripe_key"):
            links["stripe"] = {
                "clerk": f"https://buy.stripe.com/{self._stripe_price_id('clerk')}",
                "greet": f"https://buy.stripe.com/{self._stripe_price_id('greet')}",
                # ... etc
            }
        
        # PayPal buttons (standard links)
        links["paypal"] = {}
        for agent, data in AGENT_PRICING.items():
            links["paypal"][agent] = self._paypal_link(data["price"], agent)
        
        # Link in Bio
        links["link_in_bio"] = {
            "primary": self.config.get("link_in_bio", "beacons.ai/agentfleet"),
            "landing": self.config.get("landing_page_url"),
        }
        
        return links
    
    def _stripe_price_id(self, agent: str) -> str:
        """Get Stripe price ID for agent"""
        # Would integrate with Stripe API
        return f"price_{agent}_monthly"
    
    def _paypal_link(self, price: int, agent: str) -> str:
        """Generate PayPal payment link"""
        return f"https://paypal.me/agentfleet/{price}?note=Agent+{agent}"
    
    def add_lead(self, tiktok_handle: str, agent_interest: str, email: str = None):
        """Add new lead from TikTok engagement"""
        lead = Lead(
            tiktok_handle=tiktok_handle,
            agent_interest=agent_interest,
            email=email,
            timestamp=datetime.now().isoformat(),
            status="new"
        )
        self.leads.append(lead)
        self._save_leads()
        return lead
    
    def record_payment(self, agent: str, customer: dict, method: str, amount: int):
        """Record successful payment"""
        order = {
            "id": f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "agent": agent,
            "customer": customer,
            "method": method,
            "amount": amount,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        self.orders.append(order)
        self._save_orders()
        return order
    
    def get_revenue(self, period: str = "all") -> dict:
        """Calculate revenue"""
        total = sum(o["amount"] for o in self.orders)
        by_agent = {}
        for o in self.orders:
            agent = o["agent"]
            by_agent[agent] = by_agent.get(agent, 0) + o["amount"]
        
        return {
            "total": total,
            "orders": len(self.orders),
            "by_agent": by_agent,
            "monthly_recurring": sum(
                AGENT_PRICING[a]["price"] 
                for a in by_agent.keys()
            )
        }
    
    def generate_checkout_page(self) -> str:
        """Generate HTML checkout page"""
        html = """<!DOCTYPE html>
<html>
<head>
    <title>AgentFleet - AI Agents for Your Business</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #0a0a0f; color: #fff; }
        .container { max-width: 800px; margin: 0 auto; padding: 40px 20px; }
        h1 { text-align: center; font-size: 2.5em; margin-bottom: 10px; }
        .subtitle { text-align: center; color: #888; margin-bottom: 40px; }
        .agents { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
        .agent-card { background: #1a1a2e; border-radius: 16px; padding: 24px; border: 1px solid #333; }
        .agent-card h3 { color: #FFD700; font-size: 1.5em; }
        .price { font-size: 2em; color: #4CAF50; margin: 15px 0; }
        .price span { font-size: 0.5em; color: #888; }
        .features { list-style: none; margin: 20px 0; }
        .features li { padding: 8px 0; border-bottom: 1px solid #333; }
        .features li:before { content: "✓ "; color: #4CAF50; }
        .btn { display: block; width: 100%; padding: 15px; background: #4CAF50; color: #fff; text-align: center; text-decoration: none; border-radius: 8px; font-weight: bold; margin-top: 20px; }
        .btn:hover { background: #45a049; }
        .footer { text-align: center; margin-top: 40px; color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AgentFleet</h1>
        <p class="subtitle">AI Agents Working 24/7 for Your Business</p>
        
        <div class="agents">
"""
        
        for agent, data in AGENT_PRICING.items():
            html += f"""
            <div class="agent-card">
                <h3>{data['name']}</h3>
                <div class="price">${data['price']}<span>/month</span></div>
                <ul class="features">
                    <li>24/7 Availability</li>
                    <li>Your Voice & Personality</li>
                    <li>Multi-platform Support</li>
                    <li>Dedicated Support</li>
                </ul>
                <a href="#" class="btn" onclick="alert('Contact us to get started!')">Get Started</a>
            </div>
"""
        
        html += """
        </div>
        
        <div class="footer">
            <p>Questions? DM us on TikTok @agentfleet</p>
            <p>© 2026 AgentFleet. All rights reserved.</p>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def get_checkout_url(self) -> str:
        """Get primary checkout URL"""
        return self.config.get("landing_page_url", "https://agentfleet.com")


def main():
    collector = PaymentCollector()
    
    print("💰 PAYMENT COLLECTION SYSTEM")
    print("=" * 50)
    
    # Generate links
    print("\n📋 PAYMENT LINKS:")
    links = collector.generate_payment_links()
    
    print(f"\n🔗 Link in Bio: {links['link_in_bio']['primary']}")
    print(f"🌐 Landing Page: {links['link_in_bio']['landing']}")
    
    print("\n💳 PAYPAL LINKS:")
    for agent, url in links.get("paypal", {}).items():
        print(f"  {agent}: {url}")
    
    print("\n📊 REVENUE:")
    rev = collector.get_revenue()
    print(f"  Total: ${rev['total']}")
    print(f"  Orders: {rev['orders']}")
    print(f"  MRR: ${rev['monthly_recurring']}")
    
    # Generate checkout page
    checkout_dir = Path("/storage/emulated/0/Documents/AgentSales")
    checkout_dir.mkdir(parents=True, exist_ok=True)
    
    html = collector.generate_checkout_page()
    checkout_file = checkout_dir / "checkout.html"
    checkout_file.write_text(html)
    print(f"\n📄 Checkout page: {checkout_file}")


if __name__ == "__main__":
    main()
