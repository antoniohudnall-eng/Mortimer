#!/usr/bin/env python3
"""
SECRETARIAL POOL — Full Service Platform
========================================
Complete agent management, payments, onboarding, and marketing

Built: 2026-06-18
Status: READY FOR DEPLOYMENT
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Color output
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

class SecretarialPool:
    """Main controller for the Secretarial Pool platform"""
    
    VERSION = "1.0.0"
    
    # Agent Tiers with full details
    TIERS = {
        "clerk": {
            "name": "CLERK",
            "role": "Entry-Level Secretary",
            "price": 99,
            "voice": "Adam",
            "color": "#4CAF50",
            "emoji": "📝",
            "capabilities": ["email filtering", "calendars", "reminders", "data entry"]
        },
        "greet": {
            "name": "GREET",
            "role": "Receptionist Secretary",
            "price": 249,
            "voice": "Bella",
            "color": "#2196F3",
            "emoji": "👋",
            "capabilities": ["call handling", "client intake", "scheduling", "follow-ups"]
        },
        "personal": {
            "name": "PERSONAL",
            "role": "Personal Life Manager",
            "price": 449,
            "voice": "Sarah",
            "color": "#9C27B0",
            "emoji": "⭐",
            "capabilities": ["lifestyle management", "travel planning", "personal shopping", "concierge tasks"]
        },
        "velvet": {
            "name": "VELVET",
            "role": "Premium Secretary",
            "price": 599,
            "voice": "Bella",
            "color": "#E91E63",
            "emoji": "💎",
            "capabilities": ["executive support", "project coordination", "vendor management", "priority handling"]
        },
        "concierge": {
            "name": "CONCIERGE",
            "role": "24/7 Concierge",
            "price": 799,
            "voice": "Jessica",
            "color": "#FF5722",
            "emoji": "🏆",
            "capabilities": ["24/7 availability", "multi-channel support", "crisis handling", "VIP treatment"]
        },
        "executive": {
            "name": "EXECUTIVE",
            "role": "C-Suite Secretary",
            "price": 1299,
            "voice": "Adam",
            "color": "#FFD700",
            "emoji": "👑",
            "capabilities": ["strategic planning", "board communications", "stakeholder management", "enterprise coordination"]
        }
    }
    
    WALLET = "0x7244d8C20394CC11D54b2583Fb813B3EB8B72f36"
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.clients_path = self.base_path / "clients"
        self.templates_path = self.base_path / "templates"
        self.assets_path = self.base_path / "assets"
        
        # Ensure directories exist
        for path in [self.clients_path, self.templates_path, self.assets_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        # Image paths
        self.images_path = self.assets_path / "images"
        self.images_path.mkdir(exist_ok=True)
    
    def print_banner(self):
        """Print the main banner"""
        banner = f"""
{GREEN}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🤖 SECRETARIAL POOL — Agent Management Platform 🤖      ║
║                                                           ║
║   Version: {self.VERSION:<47}║
║   Wallet:  {self.WALLET:<47}║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝{RESET}
"""
        print(banner)
    
    def list_agents(self):
        """Display all available agents"""
        print(f"\n{BLUE}═══ AVAILABLE AGENTS ═══{RESET}\n")
        
        for key, agent in self.TIERS.items():
            print(f"  {agent['emoji']} {GREEN}{agent['name']}{RESET}")
            print(f"     Role: {agent['role']}")
            print(f"     Price: ${agent['price']}/month")
            print(f"     Voice: {agent['voice']}")
            print(f"     Color: {agent['color']}")
            print(f"     Image: {self.get_image_path(key)}")
            print()
    
    def get_image_path(self, agent_key: str) -> str:
        """Get the expected image path for an agent"""
        return str(self.images_path / f"{agent_key}.png")
    
    def check_images(self):
        """Check which agent images are present"""
        print(f"\n{BLUE}═══ IMAGE STATUS ═══{RESET}\n")
        
        missing = []
        found = []
        
        for key in self.TIERS.keys():
            img_path = self.get_image_path(key)
            if os.path.exists(img_path):
                found.append((key, img_path))
            else:
                missing.append((key, img_path))
        
        for key, path in found:
            print(f"  {GREEN}✅{RESET} {key}: {path}")
        
        print()
        for key, path in missing:
            print(f"  {YELLOW}⬜{RESET} {key}: {path} {YELLOW}[MISSING]{RESET}")
        
        return len(found), len(missing)
    
    def generate_client_report(self):
        """Generate report of all clients"""
        print(f"\n{BLUE}═══ CLIENT REPORT ═══{RESET}\n")
        
        clients = list(self.clients_path.glob("*.json"))
        
        if not clients:
            print(f"  {YELLOW}No clients yet.{RESET}")
            print(f"  Add clients via: python3 -c 'from secretarial_pool import *; sp = SecretarialPool(); sp.add_client()'")
            return
        
        total_revenue = 0
        
        for client_file in clients:
            with open(client_file) as f:
                client = json.load(f)
            
            tier_price = self.TIERS.get(client.get('tier', 'clerk'), {}).get('price', 0)
            total_revenue += tier_price
            
            status_color = GREEN if client.get('status') == 'active' else YELLOW
            
            print(f"  📋 {client.get('name', 'Unknown')}")
            print(f"     Email: {client.get('email', 'N/A')}")
            print(f"     Tier: {client.get('tier', 'clerk').upper()}")
            print(f"     Agent: {client.get('agent_assigned', 'pending')}")
            print(f"     Status: {status_color}{client.get('status', 'unknown')}{RESET}")
            print()
        
        print(f"  Monthly Revenue: {GREEN}${total_revenue}{RESET}/month")
    
    def generate_revenue_table(self):
        """Show revenue potential"""
        print(f"\n{BLUE}═══ REVENUE POTENTIAL ═══{RESET}\n")
        
        tiers_by_price = sorted(self.TIERS.items(), key=lambda x: x[1]['price'])
        
        print(f"  {'Tier':<12} {'Price':<10} {'5 Clients':<12} {'10 Clients':<12} {'20 Clients':<12}")
        print(f"  {'-'*12} {'-'*10} {'-'*12} {'-'*12} {'-'*12}")
        
        for key, tier in tiers_by_price:
            price = tier['price']
            print(f"  {tier['name']:<12} ${price:<9} ${price*5:<11} ${price*10:<11} ${price*20:<11}")
        
        print()
        
        # Total market potential
        total_potential = sum(t['price'] for t in self.TIERS.values())
        print(f"  {YELLOW}Total Monthly Potential (1 of each): ${total_potential}{RESET}")
        print(f"  {YELLOW}Annual Potential (1 of each): ${total_potential * 12}{RESET}")
    
    def check_wallet(self):
        """Check wallet balance"""
        print(f"\n{BLUE}═══ WALLET STATUS ═══{RESET}\n")
        print(f"  Address: {self.WALLET}")
        print(f"  Network: Ethereum Mainnet")
        print(f"  Balance: Run 'check_wallet' command for on-chain check")
    
    def show_tiktok_preview(self):
        """Preview TikTok content ideas"""
        print(f"\n{BLUE}═══ TIKTOK CONTENT PREVIEW ═══{RESET}\n")
        
        hooks = [
            "I built an AI team that works 24/7 for me...",
            "What if you could delegate EVERYTHING?",
            "Meet the agents that run my business while I sleep",
            "This is what the future of work looks like",
            "I hired 50 AI agents. Here's what happened."
        ]
        
        for i, hook in enumerate(hooks, 1):
            print(f"  🎬 Video {i}: {hook}")
        
        print(f"\n  {GREEN}Run: python3 tiktok/tiktok_marketing.py{RESET} for full content calendar")
    
    def run_portal(self, port: int = 5555):
        """Start the web portal"""
        print(f"\n{GREEN}🚀 Starting Portal on port {port}...{RESET}")
        print(f"  URL: http://localhost:{port}")
        print(f"  Press Ctrl+C to stop\n")
        
        # Import and run Flask app
        try:
            from portal.portal_server import app
            app.run(host='0.0.0.0', port=port, debug=False)
        except ImportError:
            print(f"{RED}Flask not installed. Run: pip install flask{RESET}")
    
    def generate_marketing_kit(self):
        """Generate complete marketing kit"""
        print(f"\n{BLUE}═══ MARKETING KIT ═══{RESET}\n")
        
        # Generate email templates
        templates = {
            "welcome.txt": "Welcome email template for new clients",
            "onboarding.txt": "Day 1 onboarding sequence",
            "upsell.txt": "Tier upgrade promotion",
            "referral.txt": "Referral program email"
        }
        
        for filename, desc in templates.items():
            path = self.templates_path / filename
            if not path.exists():
                path.write_text(f"# {desc}\n\n[TEMPLATE CONTENT]\n")
                print(f"  ✅ Created: {path}")
            else:
                print(f"  📄 Ready: {path}")
        
        # Generate social media posts
        posts_path = self.templates_path / "social_posts.json"
        posts = [
            {
                "platform": "tiktok",
                "content": "I built an AI team that works 24/7 for me...",
                "hashtags": ["#AI", "#Productivity", "#FutureOfWork"]
            },
            {
                "platform": "twitter",
                "content": "My AI secretary handles 100+ emails daily while I focus on strategy.",
                "hashtags": ["#AIAssistants", "#Automation"]
            },
            {
                "platform": "linkedin",
                "content": "The future of executive support isn't human — it's algorithmic.",
                "hashtags": ["#Leadership", "#AI", "#Productivity"]
            }
        ]
        
        posts_path.write_text(json.dumps(posts, indent=2))
        print(f"  ✅ Created: {posts_path}")
        
        print(f"\n  {GREEN}Marketing kit ready!{RESET}")


def main():
    """Main CLI interface"""
    sp = SecretarialPool()
    sp.print_banner()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "agents":
            sp.list_agents()
        elif command == "images":
            sp.check_images()
        elif command == "clients":
            sp.generate_client_report()
        elif command == "revenue":
            sp.generate_revenue_table()
        elif command == "wallet":
            sp.check_wallet()
        elif command == "tiktok":
            sp.show_tiktok_preview()
        elif command == "portal":
            port = int(sys.argv[2]) if len(sys.argv) > 2 else 5555
            sp.run_portal(port)
        elif command == "marketing":
            sp.generate_marketing_kit()
        elif command == "all":
            sp.list_agents()
            sp.check_images()
            sp.generate_revenue_table()
            sp.show_tiktok_preview()
        else:
            print(f"{RED}Unknown command: {command}{RESET}")
            print_help()
    else:
        print_help()


def print_help():
    """Print help message"""
    help_text = f"""
{GREEN}USAGE:{RESET}
  python3 secretarial_pool.py <command>

{GREEN}COMMANDS:{RESET}
  agents     - List all available agents
  images     - Check agent image status
  clients    - Show client report
  revenue    - Show revenue potential
  wallet     - Show wallet info
  tiktok     - Preview TikTok content
  portal     - Start web portal (port 5555)
  marketing  - Generate marketing kit
  all        - Run all checks

{GREEN}EXAMPLES:{RESET}
  python3 secretarial_pool.py agents
  python3 secretarial_pool.py portal
  python3 secretarial_pool.py all
"""
    print(help_text)


if __name__ == "__main__":
    main()
