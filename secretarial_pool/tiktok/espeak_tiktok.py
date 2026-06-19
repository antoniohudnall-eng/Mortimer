#!/usr/bin/env python3
"""
ESPEAK TikTok Integration
========================
Generate voiceovers for TikTok using espeak modulation
Works offline on Android/Termux!
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Add espeak module to path
sys.path.insert(0, '/data/data/com.termux/files/home/mortimer/voice/espeak')
from espeak_voices import AGENT_VOICES, espeak_speak

def speak_to_file(text: str, agent: str, output_file: str) -> dict:
    """Generate espeak voiceover to file"""
    profile = AGENT_VOICES.get(agent)
    return espeak_speak(text, profile, output_file)

def create_campaign_espeak(campaign_file: str):
    """Create espeak voiceovers for campaign"""
    
    with open(campaign_file, 'r') as f:
        campaign = json.load(f)
    
    output_dir = Path(campaign_file).parent / "audio_espeak"
    output_dir.mkdir(exist_ok=True)
    
    results = []
    
    for video in campaign.get('videos', []):
        video_id = video.get('id', 'unknown')
        narration = video.get('narration', '')
        agent = video.get('agent_tier', 'clerk')
        
        output_file = output_dir / f"{video_id}.wav"
        
        print(f"🎙️ {agent.upper()}: {video_id}")
        print(f"   \"{narration[:50]}...\"")
        
        result = speak_to_file(narration, agent, str(output_file))
        
        if result['status'] == 'success':
            size = os.path.getsize(output_file)
            print(f"   ✅ {output_file} ({size:,} bytes)")
        else:
            print(f"   ❌ {result.get('message')}")
        
        results.append({
            "video_id": video_id,
            "agent": agent,
            "audio": str(output_file) if result['status'] == 'success' else None,
            "status": result['status']
        })
    
    return results

def test_agent(agent: str):
    """Test espeak voice for agent"""
    profile = AGENT_VOICES.get(agent)
    if not profile:
        print(f"Unknown agent: {agent}")
        return
    
    texts = {
        "clerk": "Your emails are handled. Your calendars are managed. Efficiency at its finest.",
        "greet": "Welcome! I'm here to assist you with a smile.",
        "personal": "Let me take care of the details so you can focus on what matters.",
        "velvet": "Premium service is my commitment to you.",
        "concierge": "Available whenever you need me. Around the clock, every day.",
        "executive": "Strategic. Decisive. Ready to elevate your operations."
    }
    
    text = texts.get(agent, f"I am {agent}.")
    output = f"/data/data/com.termux/files/home/downloads/test_{agent}.wav"
    
    print(f"🎙️ Testing {agent.upper()} voice...")
    result = espeak_speak(text, profile, output)
    print(f"Result: {result}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            agent = sys.argv[2] if len(sys.argv) > 2 else "executive"
            test_agent(agent)
        else:
            create_campaign_espeak(sys.argv[1])
    else:
        print("Usage:")
        print("  python3 espeak_tiktok.py test [agent]")
        print("  python3 espeak_tiktok.py campaigns/campaign_xxx.json")
