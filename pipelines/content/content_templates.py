#!/usr/bin/env python3
"""
📝 CONTENT TEMPLATES - Script Templates for Agent Sales
Hook-Value-CTA pattern for viral content
"""

AGENT_SALES_TEMPLATES = {
    "hook_intro": [
        "What if you could clone your best employee?",
        "Stop hiring. Start deploying AI agents.",
        "This agent works 24/7 and never calls in sick.",
        "Your competitors are already using AI agents.",
        "I built 50+ AI agents. Here's the one you need.",
    ],
    
    "value_propositions": [
        "Handle 1000s of customer inquiries simultaneously",
        "Never miss a lead again - instant response",
        "Cut your workforce costs by 80%",
        "Scale your business without scaling your team",
        "Work while you sleep - your agent doesn't",
    ],
    
    "agent_types": {
        "sales": {
            "name": "Sales Agent",
            "tagline": "Closes deals while you rest",
            "price": 297,
            "features": [
                "24/7 lead response",
                "Multi-platform outreach",
                "CRM integration",
                "Follow-up automation",
                "Deal tracking"
            ]
        },
        "support": {
            "name": "Support Agent", 
            "tagline": "Your 24/7 customer service team",
            "price": 397,
            "features": [
                "Instant response time",
                "Knowledge base access",
                "Ticket routing",
                "Customer history",
                "Multi-language support"
            ]
        },
        "marketing": {
            "name": "Marketing Agent",
            "tagline": "Your content machine never stops",
            "price": 347,
            "features": [
                "Daily content creation",
                "Social scheduling",
                "Analytics reporting",
                "Campaign management",
                "A/B testing"
            ]
        },
        "operations": {
            "name": "Operations Agent",
            "tagline": "Runs your business like clockwork",
            "price": 427,
            "features": [
                "Task automation",
                "Calendar management",
                "Vendor coordination",
                "Workflow optimization",
                "Reporting dashboard"
            ]
        },
        "research": {
            "name": "Research Agent",
            "tagline": "Knows everything about your market",
            "price": 277,
            "features": [
                "Competitor analysis",
                "Market trends",
                "Lead generation",
                "Data synthesis",
                "Real-time alerts"
            ]
        }
    },
    
    "cta_phrases": [
        "Reply 'AGENT' to get started",
        "Link in bio to deploy yours",
        "DM me to learn more",
        "Comment 'FLEET' for details",
        "Start your free trial today"
    ],
    
    "hashtags": [
        "#AIAgents #ArtificialIntelligence #FutureOfWork",
        "#ChatGPT #MachineLearning #Automation",
        "#BusinessGrowth #StartupLife #Entrepreneur",
        "#WorkSmarter #AIAutomation #SideHustle",
        "#DigitalMarketing #SalesHacks #Productivity"
    ]
}


class ContentGenerator:
    def __init__(self):
        self.templates = AGENT_SALES_TEMPLATES
    
    def generate_script(self, agent_type, length="medium"):
        """Generate a video script for an agent type"""
        import random
        
        agent = self.templates["agent_types"].get(agent_type, self.templates["agent_types"]["sales"])
        
        hooks = self.templates["hook_intro"]
        value_props = self.templates["value_propositions"]
        ctas = self.templates["cta_phrases"]
        
        hook = random.choice(hooks)
        value = random.choice(value_props)
        cta = random.choice(ctas)
        
        if length == "short":
            script = f"""
SCENE 1 (0-3s):
"{hook}"

SCENE 2 (3-8s):
"{agent['name']}: {agent['tagline']}"

SCENE 3 (8-15s):
"Features: {', '.join(agent['features'][:2])}"

SCENE 4 (15-20s):
"${agent['price']}/month. {cta}"
"""
        elif length == "medium":
            script = f"""
SCENE 1 (0-3s):
"{hook}"

SCENE 2 (3-8s):
"Meet {agent['name']}"

SCENE 3 (8-15s):
"{agent['tagline']}"

SCENE 4 (15-22s):
"What it does: {', '.join(agent['features'][:3])}"

SCENE 5 (22-30s):
"Price: ${agent['price']}/month"

SCENE 6 (30-35s):
"{cta}"
"""
        else:  # long
            script = f"""
SCENE 1 (0-3s):
"{hook}"

SCENE 2 (3-7s):
"Stop doing everything yourself"

SCENE 3 (7-12s):
"Meet {agent['name']}"

SCENE 4 (12-18s):
"{agent['tagline']}"

SCENE 5 (18-28s):
"FEATURES:"
{chr(10).join(f'  • {f}' for f in agent['features'])}

SCENE 6 (28-35s):
"Imagine having {agent['name']} working right now..."

SCENE 7 (35-42s):
"Pricing: ${agent['price']}/month"

SCENE 8 (42-50s):
"{cta}"

SCENE 9 (50-55s):
"{' '.join(random.sample(self.templates['hashtags'], 2))}"
"""
        
        return {
            "agent": agent,
            "script": script.strip(),
            "scenes": self._parse_scenes(script.strip()),
            "hashtags": random.choice(self.templates["hashtags"])
        }
    
    def _parse_scenes(self, script):
        """Extract scene timings from script"""
        import re
        scenes = []
        pattern = r'SCENE \d+ \((\d+)-(\d+)s\):\s*"(.*?)"'
        
        for match in re.finditer(pattern, script, re.DOTALL):
            start, end, text = match.groups()
            scenes.append({
                "start": int(start),
                "end": int(end),
                "text": text.strip()
            })
        
        return scenes
    
    def batch_generate(self, count=10):
        """Generate multiple scripts for variety"""
        import random
        agent_types = list(self.templates["agent_types"].keys())
        lengths = ["short", "medium", "long"]
        
        scripts = []
        for _ in range(count):
            agent_type = random.choice(agent_types)
            length = random.choice(lengths)
            scripts.append(self.generate_script(agent_type, length))
        
        return scripts


if __name__ == "__main__":
    gen = ContentGenerator()
    
    # Generate one of each
    for agent_type in ["sales", "support", "marketing"]:
        script = gen.generate_script(agent_type, "medium")
        print(f"\n{'='*50}")
        print(f"AGENT: {script['agent']['name']}")
        print(f"{'='*50}")
        print(script["script"])
