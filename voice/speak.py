#!/usr/bin/env python3
"""ElevenLabs TTS - Mortimer Voice"""

import os
import sys
import time
import requests
import subprocess

def speak(text, voice_id="pNInz6obpgDQGcFmaJgB", output_file=None):
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("❌ ELEVENLABS_API_KEY not set")
        return False
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    print(f"🎙️ Speaking: {text[:50]}...")
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        
        if output_file is None:
            output_file = f"/data/data/com.termux/files/home/mortimer/voice/output/tts_{int(time.time())}.mp3"
        
        with open(output_file, "wb") as f:
            f.write(response.content)
        
        print(f"✅ Saved to: {output_file}")
        
        # Play via Termux API (works without interactive shell)
        subprocess.run(
            ["am", "broadcast", "--user", "0", "-a", "com.termux.api.MediaPlayer",
             "--es", "text", output_file],
            capture_output=True
        )
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "Hello Captain. ElevenLabs is online."
    speak(text)
