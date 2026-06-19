#!/usr/bin/env python3
"""
Generate Voiceover Audio for TikTok Campaign
Uses termux-tts-speak or local Ollama TTS
"""

import os
import sys
import subprocess
from pathlib import Path

def speak_local(text: str, output_file: str = None, voice: str = "default"):
    """Generate audio using termux-tts-speak"""
    
    if output_file:
        # Use termux-tts to generate audio file
        try:
            result = subprocess.run(
                ['termux-tts', '-f', '-', '-o', output_file],
                input=text.encode(),
                capture_output=True,
                timeout=30
            )
            if result.returncode == 0:
                return {"status": "success", "file": output_file}
            else:
                return {"status": "error", "message": result.stderr.decode()}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    else:
        # Speak aloud
        os.system(f'termux-tts-speak "{text}"')
        return {"status": "spoken"}

def speak_ollama(text: str, output_file: str = None):
    """Generate audio using Ollama with TTS model"""
    # Check if we have a TTS model
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        has_tts = 'tts' in result.stdout.lower()
        
        if has_tts:
            # Use ollama tts command
            cmd = ['ollama', 'run', 'tts']
            if output_file:
                cmd.extend(['-f', output_file])
            result = subprocess.run(cmd, input=text.encode(), capture_output=True)
            return {"status": "success" if result.returncode == 0 else "error"}
    except:
        pass
    
    return {"status": "fallback", "message": "Use termux-tts or ElevenLabs"}

def generate_campaign_audio(campaign_json: str):
    """Generate audio for all videos in a campaign"""
    
    import json
    
    with open(campaign_json, 'r') as f:
        campaign = json.load(f)
    
    output_dir = Path(campaign_json).parent / "audio"
    output_dir.mkdir(exist_ok=True)
    
    results = []
    
    for video in campaign.get('videos', []):
        video_id = video.get('id', 'unknown')
        narration = video.get('narration', '')
        agent = video.get('agent_tier', 'unknown')
        
        output_file = output_dir / f"{video_id}.wav"
        
        print(f"🎙️ Generating audio for {video_id} ({agent})...")
        print(f"   Text: {narration[:60]}...")
        
        # Try termux-tts
        result = speak_local(narration, str(output_file))
        
        if result['status'] == 'success':
            print(f"   ✅ Saved: {output_file}")
        else:
            print(f"   ⚠️ {result.get('message', 'Will need manual TTS')}")
        
        results.append({
            "video_id": video_id,
            "agent": agent,
            "audio": str(output_file) if result['status'] == 'success' else None,
            "status": result['status']
        })
    
    return results

def test_voice():
    """Test voice generation"""
    test_text = "I built an AI team that works 24 hours a day, 7 days a week. And I'm never going back."
    
    print("🧪 Testing voice...")
    print(f"   Text: {test_text}")
    print()
    
    # Test termux-tts
    print("1️⃣ Testing termux-tts-speak...")
    result = os.system(f'termux-tts-speak "{test_text}"')
    print(f"   Result: {'✅' if result == 0 else '❌'}")
    print()
    
    # Test file generation
    print("2️⃣ Testing audio file generation...")
    output = "/data/data/com.termux/files/home/downloads/test_voice.wav"
    result = subprocess.run(
        ['termux-tts', '-f', '-', '-o', output],
        input=test_text.encode(),
        capture_output=True,
        timeout=30
    )
    print(f"   Result: {'✅' if result.returncode == 0 else '❌'}")
    if result.returncode == 0:
        print(f"   File: {output}")
    
    return result.returncode == 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            test_voice()
        else:
            generate_campaign_audio(sys.argv[1])
    else:
        print("Usage:")
        print("  python3 generate_voiceover.py test")
        print("  python3 generate_voiceover.py campaigns/campaign_20260618.json")
