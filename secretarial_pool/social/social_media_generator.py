#!/usr/bin/env python3
"""
SOCIAL MEDIA CONTENT GENERATOR
============================
X.com (Twitter) + YouTube content based on trending AI topics

Trending Insights from Research:
- AI agents = $19.9T economic impact by 2030
- 75% of knowledge workers use AI at work
- 82% of companies will integrate AI agents in 3 years
- AI productivity ROI = 3.7x ($10.3x for leaders)
- 90% of automation pros use/plan AI
- Services-as-Software era emerging
"""

import json
import random
from datetime import datetime
from pathlib import Path

# Trending data points to leverage
TRENDING_INSIGHTS = {
    "stats": [
        ("$19.9T", "AI will contribute to global economy by 2030"),
        ("75%", "of knowledge workers now use AI at work"),
        ("82%", "of companies will integrate AI agents in 3 years"),
        ("3.7x", "average ROI on AI investments"),
        ("$10.3x", "ROI for AI-leading companies"),
        ("90%", "of automation professionals using AI"),
        ("66%", "of leaders won't hire without AI skills"),
        ("71%", "prefer less experienced candidate WITH AI skills"),
        ("23M", "people trained in AI skills by Microsoft"),
        ("$3.5T", "of global GDP from AI by 2030"),
    ],
    "pain_points": [
        "email overload",
        "meeting fatigue", 
        "talent shortages",
        "inability to scale",
        "hiring challenges",
        "workload overwhelm",
        "burnout from digital debt",
    ],
    " trends": [
        "AI agents replacing services",
        "Services-as-Software transformation",
        "Multi-agent systems",
        "Custom AI agents for enterprises",
        "AI power users reshaping work",
        "BYOAI (Bring Your Own AI)",
    ]
}

# Agent-specific talking points
AGENT_TALKING_POINTS = {
    "clerk": "Handles emails, calendars, data entry — the work that drowns you",
    "greet": "24/7 reception that never calls in sick",
    "personal": "Your personal life manager that anticipates your needs",
    "velvet": "Premium support that converts leads into customers",
    "concierge": "White-glove service, always available, VIP treatment",
    "executive": "Strategic coordination at C-suite level",
}

class SocialMediaGenerator:
    def __init__(self):
        self.output_dir = Path("social_content")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_x_posts(self, num_posts: int = 10) -> list:
        """Generate X.com posts based on trending data"""
        
        posts = []
        
        templates = [
            # Stat-driven posts
            lambda s: f"{s['stat'][0]} ROI on AI. {s['stat'][1]}. Meanwhile, most businesses are still manually handling what AI could automate. The gap between leaders and laggards has never been wider.",
            lambda s: f"82% of companies will integrate AI agents in 3 years.\n\nThe other 18%? They're hoping their competitors move slower.\n\n{s['agent']} handles {s['pain']} so you don't have to.",
            
            # Question-driven
            lambda s: f"What if your AI agent could handle 100% of your {s['pain']}?\n\nThat's not a dream. That's {s['agent']}.",
            
            # Pain point to solution
            lambda s: f"{s['stat'][0]} of leaders won't hire without AI skills.\n\nThe future isn't about replacing humans — it's about humans WITH AI agents.\n\nReady to build your team?",
            
            # Bold claim
            lambda s: f"Hot take: Every business needs an AI agent.\n\nNot because humans are replaceable.\nBecause {s['pain']} shouldn't be what keeps you up at night.\n\n{s['agent']} — from ${s['price']}/mo",
            
            # Story format
            lambda s: f"I hired an AI agent to handle my {s['pain']}.\n\nFirst week: skeptical.\nSecond week: curious.\nThird week: wondering why I didn't do this sooner.\n\n{s['agent']} from ${s['price']}/mo. Worth it.",
            
            # Trending topic
            lambda s: f"Services-as-Software is replacing Services-as-Humans.\n\nThe businesses winning? They're delegating to AI agents.\n\n{s['agent']} handles {s['pain']}. 24/7. No benefits. No vacation days.",
            
            # ROI focus
            lambda s: f"AI leaders see {s['stat'][0]} ROI.\n\nWhat's your excuse for not automating {s['pain']}?\n\n{s['agent']} starting at ${s['price']}/mo.",
            
            # Comparison
            lambda s: f"Human assistant: $40K+/year, 40 hrs/week, needs sleep.\n\n{s['agent']}: ${s['price']}/mo, 168 hrs/week, never sleeps.\n\nThe math isn't complicated.",
            
            # CTA style
            lambda s: f"Drop a 🏴‍☠️ if you're tired of {s['pain']}.\n\nThen DM me — {s['agent']} might be your solution.",
        ]
        
        agents = list(AGENT_TALKING_POINTS.keys())
        
        for i in range(num_posts):
            stat = random.choice(TRENDING_INSIGHTS["stats"])
            agent = random.choice(agents)
            pain = random.choice(TRENDING_INSIGHTS["pain_points"])
            template = random.choice(templates)
            
            post = template({
                "stat": stat,
                "agent": agent.upper(),
                "pain": pain,
                "price": self._get_price(agent),
            })
            
            # Ensure under 280 chars
            if len(post) > 280:
                post = post[:277] + "..."
            
            posts.append({
                "platform": "x.com",
                "id": f"X_{datetime.now().strftime('%Y%m%d')}_{i+1:02d}",
                "content": post,
                "char_count": len(post),
                "hashtags": self._get_hashtags(agent),
                "created": datetime.now().isoformat(),
            })
        
        return posts
    
    def _get_price(self, agent: str) -> str:
        prices = {
            "clerk": "99", "greet": "249", "personal": "449",
            "velvet": "599", "concierge": "799", "executive": "1,299"
        }
        return prices.get(agent, "99")
    
    def _get_hashtags(self, agent: str) -> list:
        base = ["#AI", "#Automation", "#Productivity"]
        agent_tags = {
            "clerk": ["#AdminAutomation"],
            "greet": ["#CustomerService", "#Receptionist"],
            "personal": ["#LifeHacks", "#PersonalAssistant"],
            "velvet": ["#PremiumService", "#VIP"],
            "concierge": ["#Concierge", "#Luxury"],
            "executive": ["#Executive", "#Leadership"],
        }
        return base + agent_tags.get(agent, [])
    
    def generate_youtube_content(self, num_videos: int = 5) -> list:
        """Generate YouTube video ideas based on trends"""
        
        video_templates = [
            {
                "title": "I Built an AI Team That Works 24/7 — Here's What Happened",
                "hook": "After 30 days with AI agents, the results shocked me.",
                "script_intro": "What if you could clone yourself? Not science fiction — AI agents make it possible. Today I'm showing you exactly how I built an AI team that never sleeps, never calls in sick, and costs a fraction of a human employee.",
                "key_points": [
                    "Setup: Which AI agents I deployed (CLERK, GREET, EXECUTIVE)",
                    "Week 1: The learning curve and first wins",
                    "Week 2: Emails cut by 70%, leads doubled",
                    "Week 3: My AI agent handled a customer crisis while I slept",
                    "Month 1: The ROI was insane",
                ],
                "cta": "Link in description to build your own AI team",
                "tags": ["AI agents", "automation", "productivity", "business"],
                "duration_min": "12-15 min",
            },
            {
                "title": "The $19.9 Trillion AI Shift Nobody's Talking About",
                "hook": "AI is about to transform every business. Most are completely unprepared.",
                "script_intro": "IDC predicts AI will contribute $19.9 TRILLION to the global economy by 2030. That's not a typo. We're talking about a fundamental restructuring of how business works. Today I'm breaking down what's actually happening and how you can position yourself to win.",
                "key_points": [
                    "The $19.9T prediction explained",
                    "Who are the winners and losers",
                    "Why 82% of companies WILL integrate AI in 3 years",
                    "What this means for YOUR business",
                    "The one move you need to make NOW",
                ],
                "cta": "Comment 'AGENTS' and I'll send you my AI playbook",
                "tags": ["AI economy", "future of business", "AI trends", "business transformation"],
                "duration_min": "18-22 min",
            },
            {
                "title": "AI Agents vs Human Employees: The ROI Nobody Expected",
                "hook": "The math is clearer than ever. And it favors AI.",
                "script_intro": "Leaders using AI see 3.7x ROI. For top performers? $10.3x. But what does that actually mean in practice? I'm breaking down real numbers from real businesses making this transition.",
                "key_points": [
                    "The shocking ROI stats explained",
                    "Real cost comparison: AI vs Human",
                    "Case study: Which tasks AI handles best",
                    "The tasks humans should STILL do",
                    "How to start YOUR AI transformation",
                ],
                "cta": "Link in description for free AI audit",
                "tags": ["AI ROI", "business costs", "AI comparison", "efficiency"],
                "duration_min": "15-18 min",
            },
            {
                "title": "Services-as-Software: The End of Traditional Jobs?",
                "hook": "A massive shift is happening. Are you ready?",
                "script_intro": "Every decade brings a new wave of automation. First it was factory robots. Then software ate software. Now? Services-as-Software is replacing services-that-were-human. This is bigger than most people realize.",
                "key_points": [
                    "What is Services-as-Software",
                    "Examples of the transformation happening NOW",
                    "Why AI agents are the new normal",
                    "Who benefits, who suffers",
                    "Your action plan for the transition",
                ],
                "cta": "Subscribe for weekly AI business breakdowns",
                "tags": ["Services-as-Software", "AI disruption", "future of work"],
                "duration_min": "20-25 min",
            },
            {
                "title": "Why 66% of Leaders Won't Hire You Without AI Skills",
                "hook": "The job market just changed. Here's what you need to know.",
                "script_intro": "66% of business leaders say they won't hire someone without AI skills. 71% would choose a less experienced candidate WITH AI skills over a more experienced one WITHOUT. This is the biggest shift in hiring criteria in decades.",
                "key_points": [
                    "The hiring statistics explained",
                    "Why AI skills are now non-negotiable",
                    "How to add AI skills to your toolkit",
                    "The career boost nobody's talking about",
                    "My recommended AI learning path",
                ],
                "cta": "Like and subscribe — more career content coming",
                "tags": ["AI skills", "career advice", "hiring", "job market"],
                "duration_min": "14-17 min",
            },
            {
                "title": "Building Your First AI Agent: A Complete Guide",
                "hook": "Step-by-step setup of your first AI employee",
                "script_intro": "Everyone talks about AI agents but nobody shows you HOW to actually build one. Today I'm walking through the complete process — from choosing your agent type to deployment to measuring ROI.",
                "key_points": [
                    "Choosing the right agent for your needs",
                    "Setup and configuration walkthrough",
                    "Training your agent on your business",
                    "Integration with existing tools",
                    "Measuring success: KPIs that matter",
                ],
                "cta": "Link in description to get your own AI agent setup",
                "tags": ["how to", "AI setup", "tutorial", "AI agents"],
                "duration_min": "22-28 min",
            },
        ]
        
        videos = []
        for i, template in enumerate(video_templates[:num_videos]):
            video = {
                "platform": "youtube",
                "id": f"YT_{datetime.now().strftime('%Y%m%d')}_{i+1:02d}",
                "title": template["title"],
                "hook": template["hook"],
                "script_intro": template["script_intro"],
                "key_points": template["key_points"],
                "cta": template["cta"],
                "tags": template["tags"],
                "estimated_duration": template["duration_min"],
                "created": datetime.now().isoformat(),
            }
            videos.append(video)
        
        return videos
    
    def export_content(self, posts: list, videos: list) -> dict:
        """Export all content to JSON"""
        
        content = {
            "campaign_id": f"SOCIAL_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "created": datetime.now().isoformat(),
            "x_posts": posts,
            "youtube_videos": videos,
            "trending_insights_used": [s[0] for s in TRENDING_INSIGHTS["stats"][:5]],
        }
        
        filename = f"social_content_{datetime.now().strftime('%Y%m%d')}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(content, f, indent=2)
        
        return {"filepath": str(filepath), "content": content}
    
    def print_posts(self, posts: list):
        """Pretty print X posts"""
        print("\n" + "="*70)
        print("📱 X.com (TWITTER) POSTS")
        print("="*70)
        
        for post in posts:
            print(f"\n[{post['id']}] ({post['char_count']} chars)")
            print("-" * 50)
            print(post['content'])
            print(f"\nTags: {' '.join(post['hashtags'])}")
        
        print("\n" + "="*70)
    
    def print_videos(self, videos: list):
        """Pretty print YouTube ideas"""
        print("\n" + "="*70)
        print("🎬 YOUTUBE VIDEO IDEAS")
        print("="*70)
        
        for video in videos:
            print(f"\n[{video['id']}] ~{video['estimated_duration']}")
            print("-" * 50)
            print(f"🎣 HOOK: {video['hook']}")
            print(f"\n📝 TITLE: {video['title']}")
            print(f"\n📖 SCRIPT INTRO:")
            print(f"   {video['script_intro']}")
            print(f"\n📌 KEY POINTS:")
            for point in video['key_points']:
                print(f"   • {point}")
            print(f"\n📢 CTA: {video['cta']}")
            print(f"\n🏷️ TAGS: {', '.join(video['tags'])}")
        
        print("\n" + "="*70)
    
    def print_full_report(self, posts: list, videos: list):
        """Print complete content report"""
        self.print_posts(posts)
        self.print_videos(videos)
        
        print("\n" + "🎉" * 20)
        print("\n✅ GENERATED:")
        print(f"   📱 {len(posts)} X.com posts")
        print(f"   🎬 {len(videos)} YouTube videos")
        print("\n   All based on trending AI data:")
        for stat in TRENDING_INSIGHTS["stats"][:5]:
            print(f"   • {stat[0]}: {stat[1]}")


def main():
    """Generate all social media content"""
    
    print("🚀 SOCIAL MEDIA CONTENT GENERATOR")
    print("   Based on Trending AI Insights 2024")
    print()
    
    generator = SocialMediaGenerator()
    
    # Generate content
    print("📝 Generating X.com posts...")
    posts = generator.generate_x_posts(10)
    
    print("🎬 Generating YouTube ideas...")
    videos = generator.generate_youtube_content(6)
    
    # Export
    result = generator.export_content(posts, videos)
    print(f"\n💾 Exported to: {result['filepath']}")
    
    # Print report
    generator.print_full_report(posts, videos)


if __name__ == "__main__":
    main()
