#!/usr/bin/env python3
"""
🎙️ VOICE PIPELINE - Mortimer's Voice Generator
Uses ElevenLabs (premium) or termux-tts (backup)
"""

import os
import sys
import subprocess
import requests
import tempfile
from pathlib import Path

# Config
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam voice

class VoicePipeline:
    def __init__(self):
        self.elevenlabs_available = bool(ELEVENLABS_API_KEY)
        self.temp_dir = Path(tempfile.gettempdir()) / "mortimer_voice"
        self.temp_dir.mkdir(exist_ok=True)
    
    def speak(self, text, output_path=None, use_elevenlabs=True):
        """Generate voice audio from text"""
        if output_path is None:
            output_path = self.temp_dir / f"voice_{int(time.time())}.mp3"
        
        if self.elevenlabs_available and use_elevenlabs:
            return self._elevenlabs_tts(text, output_path)
        else:
            return self._termux_tts(text, output_path)
    
    def _elevenlabs_tts(self, text, output_path):
        """Premium ElevenLabs voice"""
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                return str(output_path)
            else:
                print(f"ElevenLabs error: {response.status_code}")
                return self._termux_tts(text, output_path)
        except Exception as e:
            print(f"ElevenLabs failed: {e}, falling back to termux-tts")
            return self._termux_tts(text, output_path)
    
    def _termux_tts(self, text, output_path):
        """Backup: Android TTS"""
        # Convert to wav first using termux-tts
        wav_path = output_path.with_suffix('.wav')
        
        try:
            result = subprocess.run(
                ['termux-tts-speak', text],
                capture_output=True,
                timeout=10
            )
            # Note: termux-tts doesn't save to file, just speaks
            # For file output, we'd need to use a different approach
            return None
        except Exception as e:
            print(f"termux-tts failed: {e}")
            return None
    
    def batch_speak(self, segments):
        """Generate voice for multiple text segments"""
        results = []
        for i, (speaker, text) in enumerate(segments):
            path = self.temp_dir / f"segment_{i}_{speaker}.mp3"
            result = self.speak(text, path)
            if result:
                results.append((speaker, result))
        return results

if __name__ == "__main__":
    import time
    pipeline = VoicePipeline()
    
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        output = pipeline.speak(text)
        print(f"Generated: {output}")
    else:
        # Demo
        test = "Welcome to Agent Sales Pro. Your AI workforce starts here."
        output = pipeline.speak(test)
        print(f"Demo voice: {output}")
