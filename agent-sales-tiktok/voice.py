#!/usr/bin/env python3
"""
🎙️ VOICE MODULE - Agent Sales TikTok
Priority: Native (termux-tts, espeak-ng) PRIMARY, ElevenLabs OPTIONAL

Patricia consulted - Implementation based on workflow patterns
"""

import os
import sys
import subprocess
import requests
import tempfile
import time
from pathlib import Path
from typing import Optional, Tuple

# Voice configuration from wiki (Golden Ratio φ)
PHI = 1.618033988749895
VOICE_CONFIG = {
    "speed": int(PHI * 100),      # 161
    "pitch": int((PHI / 3.14159) * 100),  # 51
    "amplitude": int(PHI * 70),   # 113
}

class VoiceModule:
    """
    Voice generation for Agent Sales TikTok
    
    Priority:
    1. termux-tts-speak (Android native, natural)
    2. espeak-ng (fast, consistent)
    3. ElevenLabs (premium, optional)
    """
    
    def __init__(self, output_dir: str = None):
        self.temp_dir = Path(output_dir) if output_dir else Path(tempfile.gettempdir()) / "voice"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Check available voices
        self.termux_tts = self._check_termux_tts()
        self.espeak = self._check_espeak()
        self.elevenlabs = self._check_elevenlabs()
        
        # Priority order
        self.provider_priority = []
        if self.termux_tts:
            self.provider_priority.append("termux")
        if self.espeak:
            self.provider_priority.append("espeak")
        if self.elevenlabs:
            self.provider_priority.append("elevenlabs")
    
    def _check_termux_tts(self) -> bool:
        """Check if termux-tts-speak available"""
        try:
            result = subprocess.run(["termux-tts-speak", "--help"], 
                                 capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def _check_espeak(self) -> bool:
        """Check if espeak-ng available"""
        try:
            result = subprocess.run(["espeak-ng", "--version"], 
                                 capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def _check_elevenlabs(self) -> bool:
        """Check if ElevenLabs API key available"""
        api_key = os.environ.get("ELEVENLABS_API_KEY", "")
        if api_key and api_key.startswith("sk_"):
            return True
        return False
    
    def get_status(self) -> dict:
        """Get voice provider status"""
        return {
            "termux_tts": self.termux_tts,
            "espeak": self.espeak,
            "elevenlabs": self.elevenlabs,
            "primary": self.provider_priority[0] if self.provider_priority else None,
            "all": self.provider_priority
        }
    
    def speak(self, text: str, output_path: str = None, 
              provider: str = None) -> Tuple[str, str]:
        """
        Generate voice audio from text
        
        Args:
            text: Text to speak
            output_path: Optional output file path
            provider: Force specific provider (termux/espeak/elevenlabs)
        
        Returns:
            (file_path, provider_used)
        """
        if not output_path:
            output_path = str(self.temp_dir / f"voice_{int(time.time())}.mp3")
        
        # Use requested provider or fall back to priority
        if provider and provider in self.provider_priority:
            providers = [provider] + [p for p in self.provider_priority if p != provider]
        else:
            providers = self.provider_priority
        
        errors = []
        
        for prov in providers:
            try:
                if prov == "termux":
                    result = self._termux_tts(text, output_path)
                    if result:
                        return result, "termux-tts"
                
                elif prov == "espeak":
                    result = self._espeak_ng(text, output_path)
                    if result:
                        return result, "espeak-ng"
                
                elif prov == "elevenlabs":
                    result = self._elevenlabs(text, output_path)
                    if result:
                        return result, "elevenlabs"
                        
            except Exception as e:
                errors.append(f"{prov}: {e}")
                continue
        
        # All failed
        raise Exception(f"Voice generation failed: {errors}")
    
    def _termux_tts(self, text: str, output_path: str) -> Optional[str]:
        """Android native TTS"""
        if not self.termux_tts:
            return None
        
        # termux-tts-speak doesn't save to file directly
        # Use espeak as fallback for file output
        return None
    
    def _espeak_ng(self, text: str, output_path: str) -> Optional[str]:
        """espeak-ng TTS - saves to file"""
        if not self.espeak:
            return None
        
        # Convert to wav first, then mp3
        wav_path = output_path.replace('.mp3', '.wav')
        
        try:
            # Use shell=True for pipes, simpler command
            result = subprocess.run(
                f'espeak-ng -w "{wav_path}" -s {VOICE_CONFIG["speed"]} -p {VOICE_CONFIG["pitch"]} "{text}"',
                shell=True, capture_output=True, timeout=30
            )
            
            if result.returncode == 0 and Path(wav_path).exists():
                # Convert to MP3 using ffmpeg
                ffmpeg_result = subprocess.run(
                    f'ffmpeg -y -i "{wav_path}" -codec:a libmp3lame -qscale:a 2 "{output_path}"',
                    shell=True, capture_output=True, timeout=30
                )
                
                if ffmpeg_result.returncode == 0:
                    Path(wav_path).unlink(missing_ok=True)
                    return output_path
                    
        except Exception as e:
            print(f"espeak-ng error: {e}")
        
        return None
    
    def _elevenlabs(self, text: str, output_path: str) -> Optional[str]:
        """ElevenLabs premium TTS"""
        if not self.elevenlabs:
            return None
        
        api_key = os.environ.get("ELEVENLABS_API_KEY")
        voice_id = "pNInz6obpgDQGcFmaJgB"  # Adam
        
        try:
            response = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json={
                    "text": text,
                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
                },
                headers={
                    "xi-api-key": api_key,
                    "Content-Type": "application/json",
                    "Accept": "audio/mpeg"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                Path(output_path).write_bytes(response.content)
                return output_path
                
        except Exception as e:
            print(f"ElevenLabs error: {e}")
        
        return None
    
    def speak_and_play(self, text: str, provider: str = None):
        """Speak text and play immediately (no file save)"""
        providers = [provider] if provider else self.provider_priority
        
        for prov in providers:
            try:
                if prov == "termux":
                    subprocess.Popen(["termux-tts-speak", text])
                    return "termux-tts"
                
                elif prov == "espeak":
                    cmd = ["espeak-ng", "-s", str(VOICE_CONFIG["speed"]), "-p", str(VOICE_CONFIG["pitch"]), text]
                    subprocess.Popen(cmd)
                    return "espeak-ng"
                    
            except Exception as e:
                print(f"{prov} error: {e}")
                continue
        
        return None
    
    def test_all(self) -> dict:
        """Test all available voice providers"""
        test_text = "AI agents working 24 hours a day."
        results = {}
        
        for prov in self.provider_priority:
            output = str(self.temp_dir / f"test_{prov}.mp3")
            try:
                path, used = self.speak(test_text, output, provider=prov)
                size = Path(path).stat().st_size if Path(path).exists() else 0
                results[prov] = {"status": "success", "path": path, "size": size}
            except Exception as e:
                results[prov] = {"status": "failed", "error": str(e)}
        
        return results


def main():
    """Test voice module"""
    voice = VoiceModule()
    
    print("🎙️ VOICE MODULE - Status")
    print("=" * 40)
    
    status = voice.get_status()
    print(f"\nAvailable providers: {status['all']}")
    print(f"Primary: {status['primary']}")
    
    print("\n🧪 Testing all providers...")
    results = voice.test_all()
    
    for prov, result in results.items():
        if result["status"] == "success":
            print(f"  ✅ {prov}: {result['size']} bytes")
        else:
            print(f"  ❌ {prov}: {result.get('error', 'failed')}")
    
    print("\n🎤 Quick speak test...")
    voice.speak_and_play("AI agents ready. Pipeline complete.")
    print("(You should hear audio)")


if __name__ == "__main__":
    main()
