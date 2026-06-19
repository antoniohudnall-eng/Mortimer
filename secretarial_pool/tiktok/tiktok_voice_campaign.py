#!/usr/bin/env python3
"""
TikTok Marketing Campaign with Voiceover
=========================================
Generates video scripts + ElevenLabs voice narration

Built: 2026-06-18
"""

import json
import random
import os
from datetime import datetime, timedelta
from pathlib import Path

# ElevenLabs Config
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY', '')
VOICE_IDS = {
    "adam": "pNInz6obpgDQGcFmaJgB",      # Executive
    "bella": "EXAMPLES",                   # Receptionist  
    "sarah": "EXAMPLES",                   # Personal
    "jessica": "EXAMPLES"                  # Concierge
}

# Voice mapping by agent tier
TIER_VOICES = {
    "clerk": "adam",
    "greet": "bella",
    "personal": "sarah",
    "velvet": "bella",
    "concierge": "jessica",
    "executive": "adam"
}

# TikTok Hook Templates
HOOKS = [
    "I built an AI team that works 24/7 for me... and I'm never going back.",
    "What if you could delegate EVERYTHING to an AI?",
    "Meet the agents that run my business while I sleep.",
    "This is what the future of work looks like.",
    "I hired 50 AI agents. Here's what actually happened.",
    "The best employee I ever hired doesn't need coffee breaks.",
    "My AI secretary handles 100+ emails daily. Here's how.",
    "I outsourced my entire inbox to an AI. The results are wild.",
]

# Value Proposition Scripts
VALUE_PROPS = {
    "clerk": [
        "CLERK handles your emails, calendars, and reminders 24/7.",
        "No more drowning in inbox. CLERK filters, prioritizes, responds.",
        "The entry-level agent that works like a senior.",
        "Data entry, scheduling, reminders — all automated.",
    ],
    "greet": [
        "GREET welcomes your clients like a pro. Every. Single. Time.",
        "Never miss a lead. GREET handles your reception 24/7.",
        "Professional first impressions, automated.",
        "Your virtual receptionist that never sleeps or calls in sick.",
    ],
    "personal": [
        "PERSONAL manages your life like a seasoned concierge.",
        "Travel planning, shopping, scheduling — handled.",
        "Your personal AI manager that anticipates your needs.",
        "Life optimization, powered by AI.",
    ],
    "velvet": [
        "VELVET delivers premium support that converts.",
        "Executive-level assistance for growing businesses.",
        "When standard isn't enough — go premium.",
        "Premium secretaries. VIP treatment. Automated.",
    ],
    "concierge": [
        "CONCIERGE never sleeps. 24/7 availability for your clients.",
        "Round-the-clock support that never takes a break.",
        "Crisis handling, VIP treatment, multi-channel support.",
        "The concierge that never closes.",
    ],
    "executive": [
        "EXECUTIVE operates at C-suite level. Strategic. Pristine.",
        "Board communications, stakeholder management — automated.",
        "The right hand every executive wishes they had.",
        "Enterprise coordination, executive precision.",
    ]
}

# CTAs
CTAS = [
    "Drop a 👋 if you want part 2.",
    "Comment 'AGENT' and I'll send you the setup.",
    "Link in bio to get your own AI team.",
    "DM me to get started today.",
    "Save this for when you build yours.",
    "Follow for more AI agent content.",
]

# Hashtag Sets
HASHTAGS = [
    ["#AI", "#ArtificialIntelligence", "#Productivity", "#FutureOfWork"],
    ["#AIAgents", "#Automation", "#Business", "#Tech"],
    ["#SideHustle", "#Entrepreneur", "#DigitalNomad", "#WorkFromHome"],
    ["#AIAssistant", "#ChatGPT", "#MachineLearning", "#Startup"],
]

class TikTokVoiceCampaign:
    def __init__(self, output_dir: str = "campaigns"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_script(self, agent_tier: str = None) -> dict:
        """Generate a complete TikTok script with voiceover"""
        
        # Select random tier if not specified
        if not agent_tier:
            agent_tier = random.choice(list(TIER_VOICES.keys()))
        
        script = {
            "id": f"TikTok_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(100,999)}",
            "agent_tier": agent_tier,
            "voice": TIER_VOICES[agent_tier],
            "hook": random.choice(HOOKS),
            "value_prop": random.choice(VALUE_PROPS[agent_tier]),
            "cta": random.choice(CTAS),
            "hashtags": random.choice(HASHTAGS),
            "duration_sec": random.randint(30, 60),
            "created": datetime.now().isoformat(),
        }
        
        # Full narration script
        script["narration"] = f"{script['hook']} {script['value_prop']} {script['cta']}"
        
        # Words per minute estimate
        words = len(script['narration'].split())
        script["estimated_duration"] = round(words / 2.5, 1)  # ~150 WPM speaking pace
        
        return script
    
    def generate_campaign(self, num_videos: int = 7, days: int = 7) -> list:
        """Generate a full campaign calendar"""
        
        campaign = []
        base_date = datetime.now()
        
        for i in range(num_videos):
            # Rotate through agent tiers
            tiers = list(TIER_VOICES.keys())
            agent_tier = tiers[i % len(tiers)]
            
            script = self.generate_script(agent_tier)
            
            # Schedule (random time 6am-9pm)
            hour = random.randint(6, 21)
            minute = random.choice([0, 15, 30, 45])
            publish_time = base_date + timedelta(days=i, hours=hour, minutes=minute)
            script["scheduled_time"] = publish_time.strftime("%Y-%m-%d %H:%M")
            script["video_number"] = i + 1
            
            campaign.append(script)
        
        return campaign
    
    def generate_voiceover(self, script: dict) -> dict:
        """Generate voiceover audio using ElevenLabs"""
        
        if not ELEVENLABS_API_KEY:
            return {
                "status": "no_api_key",
                "message": "Set ELEVENLABS_API_KEY to generate voiceovers",
                "script": script["narration"]
            }
        
        try:
            import requests
            
            voice_id = VOICE_IDS[script["voice"]]
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": ELEVENLABS_API_KEY
            }
            
            data = {
                "text": script["narration"],
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                audio_file = self.output_dir / f"{script['id']}.mp3"
                with open(audio_file, 'wb') as f:
                    f.write(response.content)
                
                return {
                    "status": "success",
                    "audio_file": str(audio_file),
                    "script": script
                }
            else:
                return {
                    "status": "error",
                    "message": f"API error: {response.status_code}",
                    "script": script
                }
                
        except ImportError:
            return {
                "status": "error",
                "message": "Install requests: pip install requests",
                "script": script
            }
    
    def export_campaign(self, campaign: list, filename: str = None) -> str:
        """Export campaign to JSON"""
        
        if not filename:
            filename = f"campaign_{datetime.now().strftime('%Y%m%d')}.json"
        
        filepath = self.output_dir / filename
        
        export_data = {
            "campaign_id": f"SP_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "created": datetime.now().isoformat(),
            "total_videos": len(campaign),
            "videos": campaign
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return str(filepath)
    
    def print_campaign(self, campaign: list):
        """Pretty print campaign overview"""
        
        print("\n" + "="*70)
        print("🎬 TIKTOK CAMPAIGN — Secretarial Pool")
        print("="*70)
        
        for video in campaign:
            print(f"\n📹 VIDEO {video['video_number']}: {video['id']}")
            print("-" * 50)
            print(f"   Agent: {video['agent_tier'].upper()}")
            print(f"   Voice: {video['voice']}")
            print(f"   Schedule: {video['scheduled_time']}")
            print(f"   Duration: ~{video['estimated_duration']}s")
            print(f"\n   🎣 HOOK:")
            print(f"   \"{video['hook']}\"")
            print(f"\n   💡 VALUE:")
            print(f"   \"{video['value_prop']}\"")
            print(f"\n   📢 CTA:")
            print(f"   \"{video['cta']}\"")
            print(f"\n   #️⃣ HASHTAGS: {' '.join(video['hashtags'])}")
        
        print("\n" + "="*70)
        print(f"📊 Campaign Total: {len(campaign)} videos")
        print("="*70)


def main():
    """Run the campaign generator"""
    
    campaign = TikTokVoiceCampaign()
    
    print("🎬 Generating 7-day TikTok Campaign...")
    print()
    
    # Generate campaign
    videos = campaign.generate_campaign(num_videos=7, days=7)
    
    # Print overview
    campaign.print_campaign(videos)
    
    # Export
    filepath = campaign.export_campaign(videos)
    print(f"\n✅ Campaign exported to: {filepath}")
    
    # Generate voiceovers (if API key set)
    if ELEVENLABS_API_KEY:
        print("\n🎙️ Generating voiceovers...")
        for video in videos[:2]:  # First 2 for demo
            result = campaign.generate_voiceover(video)
            if result["status"] == "success":
                print(f"   ✅ {video['id']}: {result['audio_file']}")
            else:
                print(f"   ⚠️ {video['id']}: {result['message']}")
    else:
        print("\n💡 To generate voiceovers:")
        print("   export ELEVENLABS_API_KEY='your_key'")
        print("   python3 tiktok_voice_campaign.py")


if __name__ == "__main__":
    main()
