#!/usr/bin/env python3
"""
Create Voiceovers for TikTok Campaign
Uses gTTS for local TTS (no API key needed)
"""

import os
import sys
import json
from pathlib import Path
from gtts import gTTS

def create_voiceover(text: str, output_file: str, lang: str = 'en') -> dict:
    """Create MP3 voiceover using gTTS"""
    
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_file)
        return {"status": "success", "file": output_file}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_campaign_audio(campaign_file: str):
    """Generate audio for all videos in campaign"""
    
    with open(campaign_file, 'r') as f:
        campaign = json.load(f)
    
    output_dir = Path(campaign_file).parent / "audio"
    output_dir.mkdir(exist_ok=True)
    
    results = []
    
    for video in campaign.get('videos', []):
        video_id = video.get('id', 'unknown')
        narration = video.get('narration', '')
        agent = video.get('agent_tier', 'unknown')
        
        output_file = output_dir / f"{video_id}.mp3"
        
        print(f"🎙️ {agent.upper()}: {video_id}")
        print(f"   \"{narration[:60]}...\"")
        
        result = create_voiceover(narration, str(output_file))
        
        if result['status'] == 'success':
            size = os.path.getsize(output_file)
            print(f"   ✅ {output_file} ({size} bytes)")
        else:
            print(f"   ❌ {result.get('message')}")
        
        results.append({
            "video_id": video_id,
            "agent": agent,
            "audio": str(output_file) if result['status'] == 'success' else None,
            "status": result['status']
        })
    
    return results

def test():
    """Test gTTS"""
    print("🧪 Testing gTTS...")
    text = "I built an AI team that works 24 hours a day, 7 days a week. And I'm never going back."
    
    output = "/data/data/com.termux/files/home/downloads/test_gtts.mp3"
    result = create_voiceover(text, output)
    
    print(f"Result: {result}")
    if result['status'] == 'success':
        print(f"✅ Test file: {output}")
        # Try to play it
        os.system(f"termux-open '{output}'")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            test()
        else:
            create_campaign_audio(sys.argv[1])
    else:
        print("Usage:")
        print("  python3 create_voiceovers.py test")
        print("  python3 create_voiceovers.py campaigns/campaign_20260618.json")
