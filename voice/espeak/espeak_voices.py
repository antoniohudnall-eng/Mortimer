#!/usr/bin/env python3
"""
ESPEAK VOICE MODULATION SYSTEM
==============================
Modulated voices for Secretarial Pool agents
Built for Android/Termux - no internet required!

Usage:
    python3 espeak_voices.py speak "Hello world"
    python3 espeak_voices.py list
    python3 espeak_voices.py generate <agent>
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
PROFILES_DIR = BASE_DIR / "profiles"
OUTPUT_DIR = BASE_DIR / "output"

# Voice Profiles for each agent tier
# Parameters: voice, speed(-s), pitch(-p), amplitude(-a), variant
AGENT_VOICES = {
    "clerk": {
        "name": "CLERK",
        "voice": "en-us",
        "speed": 130,      # Slightly faster
        "pitch": 85,       # Neutral-male
        "amplitude": 100,
        "variant": "m1",   # Male voice 1
        "description": "Professional, efficient, entry-level assistant"
    },
    "greet": {
        "name": "GREET", 
        "voice": "en-us",
        "speed": 110,      # Warm, welcoming pace
        "pitch": 110,      # Higher, friendly female
        "amplitude": 100,
        "variant": "f3",    # Female variant
        "description": "Friendly receptionist, always welcoming"
    },
    "personal": {
        "name": "PERSONAL",
        "voice": "en-us",
        "speed": 105,      # Relaxed, caring pace
        "pitch": 100,      # Balanced
        "amplitude": 95,
        "variant": "f2",    # Female variant
        "description": "Caring life manager, thoughtful"
    },
    "velvet": {
        "name": "VELVET",
        "voice": "en-us",
        "speed": 115,      # Smooth, premium pace
        "pitch": 90,       # Confident female
        "amplitude": 100,
        "variant": "f1",   # Female variant  
        "description": "Premium service, elegant delivery"
    },
    "concierge": {
        "name": "CONCIERGE",
        "voice": "en-us",
        "speed": 100,      # Professional, attentive
        "pitch": 95,       # Authoritative
        "amplitude": 100,
        "variant": "f4",   # Female variant
        "description": "24/7 concierge, attentive to detail"
    },
    "executive": {
        "name": "EXECUTIVE",
        "voice": "en-us",
        "speed": 125,      # Confident, decisive
        "pitch": 75,       # Deep, authoritative male
        "amplitude": 100,
        "variant": "m2",   # Male variant
        "description": "C-suite presence, executive authority"
    },
    # Special voices
    "robot": {
        "name": "ROBOT",
        "voice": "en-us",
        "speed": 90,
        "pitch": 60,
        "amplitude": 100,
        "variant": "robot",  # Robot-like
        "description": "Robotic/AI assistant voice"
    },
    "whisper": {
        "name": "WHISPER",
        "voice": "en-us",
        "speed": 100,
        "pitch": 130,
        "amplitude": 50,
        "variant": "whisper",
        "description": "Whispered, intimate delivery"
    }
}

def espeak_speak(text: str, profile: dict = None, output_file: str = None, 
                 voice: str = "en-us", speed: int = 130, pitch: int = 100,
                 amplitude: int = 100, variant: str = None) -> dict:
    """
    Speak text using espeak with modulation
    
    Args:
        text: Text to speak
        profile: Voice profile dict (overrides individual params)
        output_file: Save to file instead of speaking
        voice: eSpeak voice (en-us, en-gb, etc)
        speed: Speed in words/minute (80-200)
        pitch: Pitch 0-200 (100 = normal)
        amplitude: Amplitude 0-200 (100 = normal)
        variant: Voice variant (m1, m2, f1, f2, f3, f4, robot, whisper)
    """
    
    if profile:
        voice = profile.get("voice", voice)
        speed = profile.get("speed", speed)
        pitch = profile.get("pitch", pitch)
        amplitude = profile.get("amplitude", amplitude)
        variant = profile.get("variant", variant)
    
    # Build espeak command
    cmd = ["espeak"]
    
    # Output to file
    if output_file:
        cmd.extend(["-w", output_file])
    
    # Modulation parameters
    cmd.extend(["-s", str(speed)])      # Speed
    cmd.extend(["-p", str(pitch)])     # Pitch
    cmd.extend(["-a", str(amplitude)]) # Amplitude
    
    # Voice variant
    if variant:
        cmd.extend(["-v", f"{voice}+{variant}"])
    else:
        cmd.extend(["-v", voice])
    
    # The text
    cmd.append(text)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return {
                "status": "success",
                "text": text,
                "output": output_file,
                "profile": profile.get("name") if profile else voice,
                "params": {"voice": voice, "speed": speed, "pitch": pitch, "variant": variant}
            }
        else:
            return {
                "status": "error",
                "message": result.stderr or "Unknown error"
            }
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Timeout"}
    except FileNotFoundError:
        return {"status": "error", "message": "espeak not found"}


def generate_agent_voice(agent: str, text: str = None, output_dir: str = None) -> dict:
    """Generate voice sample for an agent"""
    
    if agent not in AGENT_VOICES:
        return {"status": "error", "message": f"Unknown agent: {agent}"}
    
    profile = AGENT_VOICES[agent]
    
    if not text:
        # Default sample text based on agent
        texts = {
            "clerk": "Hello, I'm CLERK. I'll help you with emails, calendars, and reminders. Always efficient, always professional.",
            "greet": "Welcome! I'm GREET, your virtual receptionist. How may I assist you today?",
            "personal": "Hi there, I'm PERSONAL. Let me help you manage your busy life with care and attention.",
            "velvet": "Good day, I'm VELVET. Premium service is my specialty. How may I serve you?",
            "concierge": "Hello, I'm CONCIERGE. Available around the clock to meet your every need.",
            "executive": "I'm EXECUTIVE. Strategic planning, stakeholder management, enterprise coordination. How may I assist?",
            "robot": "Beep boop. I am robot assistant. Processing request. How may I help, human?",
            "whisper": "Psst... I have something important to tell you. Can you hear me?",
        }
        text = texts.get(agent, f"Hello, I'm {profile['name']}.")
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / f"{agent}_voice.wav"
    
    if output_dir:
        output_file = Path(output_dir) / f"{agent}_voice.wav"
    
    result = espeak_speak(text, profile, str(output_file))
    
    if result["status"] == "success":
        size = os.path.getsize(output_file)
        result["file"] = str(output_file)
        result["size"] = size
    
    return result


def list_voices():
    """List all available eSpeak voices"""
    result = subprocess.run(["espeak", "--voices"], capture_output=True, text=True)
    return result.stdout


def generate_all_samples():
    """Generate voice samples for all agents"""
    print("🎙️ Generating voice samples for all agents...")
    print()
    
    for agent in AGENT_VOICES:
        print(f"  Processing {agent.upper()}...")
        result = generate_agent_voice(agent)
        
        if result["status"] == "success":
            print(f"    ✅ {result['file']} ({result['size']:,} bytes)")
        else:
            print(f"    ❌ {result.get('message')}")
    
    print()
    print("✅ All voice samples generated!")


def create_voice_for_tiktok(text: str, agent: str, output: str) -> dict:
    """Create voiceover for TikTok campaign"""
    
    if agent not in AGENT_VOICES:
        return {"status": "error", "message": f"Unknown agent: {agent}"}
    
    profile = AGENT_VOICES[agent]
    return espeak_speak(text, profile, output)


def main():
    """CLI interface"""
    
    if len(sys.argv) < 2:
        print("ESPEAK VOICE MODULATION SYSTEM")
        print("=" * 40)
        print()
        print("Usage:")
        print("  python3 espeak_voices.py speak <text> [agent]")
        print("  python3 espeak_voices.py list")
        print("  python3 espeak_voices.py generate [agent]")
        print("  python3 espeak_voices.py all")
        print()
        print("Agents:", ", ".join(AGENT_VOICES.keys()))
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == "speak":
        if len(sys.argv) < 3:
            print("Usage: espeak_voices.py speak <text> [agent]")
            return
        
        text = sys.argv[2]
        agent = sys.argv[3] if len(sys.argv) > 3 else None
        
        profile = AGENT_VOICES.get(agent) if agent else None
        
        print(f"🎙️ Speaking as {agent or 'default'}...")
        result = espeak_speak(text, profile)
        print(f"Result: {result}")
        
    elif cmd == "list":
        print("📋 Available eSpeak voices:")
        print(list_voices())
        
    elif cmd == "generate":
        agent = sys.argv[2] if len(sys.argv) > 2 else None
        
        if agent:
            print(f"🎙️ Generating voice for {agent}...")
            result = generate_agent_voice(agent)
            print(f"Result: {result}")
        else:
            generate_all_samples()
            
    elif cmd == "all":
        generate_all_samples()
        
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()

MORTIMER = {
    "name": "MORTIMER",
    "voice": "en-us",
    "speed": 115,       # Measured, calm pace
    "pitch": 80,        # Deep, authoritative
    "amplitude": 110,   # Strong presence
    "variant": "m3",    # Deep male variant
    "keytoning": 5,     # Slight robot undertone
    "description": "Mortimer - General of the Forces, calm and authoritative"
}
AGENT_VOICES["mortimer"] = MORTIMER
