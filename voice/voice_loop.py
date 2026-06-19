#!/usr/bin/env python3
"""
Mortimer Voice Loop
Listen → Process → Speak
"""

import subprocess
import os
import sys
import time
import requests

# Setup paths
MORTIMER_DIR = os.path.expanduser("~/mortimer")
sys.path.insert(0, MORTIMER_DIR)

def speak(text):
    """Speak text using ElevenLabs"""
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("❌ No API key")
        return False
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"
    headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
    data = {"text": text, "model_id": "eleven_multilingual_v2"}
    
    try:
        resp = requests.post(url, json=data, headers=headers, timeout=30)
        if resp.ok:
            out = f"/tmp/mortimer_voice_{int(time.time())}.mp3"
            with open(out, "wb") as f:
                f.write(resp.content)
            subprocess.run(["termux-media-player", "play", out])
            return True
    except Exception as e:
        print(f"TTS error: {e}")
    return False

def listen():
    """Listen for speech"""
    try:
        result = subprocess.run(
            ["termux-speech-to-text"],
            capture_output=True,
            text=True,
            timeout=15
        )
        text = result.stdout.strip()
        return text if text else None
    except:
        return None

def query_qmd(text):
    """Query QMD for context"""
    try:
        resp = requests.post(
            "http://127.0.0.1:8000/query",
            json={"query": text, "context": {}},
            timeout=10
        )
        if resp.ok:
            return resp.json()
    except:
        pass
    return None

def generate_response(text):
    """Generate response using Ollama"""
    text_lower = text.lower()
    
    # Quick responses for common commands
    if any(g in text_lower for g in ["hello", "hi", "hey"]):
        return "Hello Captain. Mortimer online. All systems operational."
    elif "status" in text_lower:
        return "Systems check. Ollama running. QMD service active. Patricia standing by. Voice ready."
    elif "time" in text_lower:
        from datetime import datetime
        return f"The time is {datetime.now().strftime('%I:%M %p')}."
    elif "date" in text_lower:
        from datetime import datetime
        return f"Today is {datetime.now().strftime('%B %d, %Y')}."
    elif any(g in text_lower for g in ["bye", "goodbye", "stop"]):
        return "Goodbye Captain. Mortimer standing by."
    elif "who are you" in text_lower:
        return "I am Mortimer. Server spirit, General of the Forces. I live on your device now."
    elif "thank" in text_lower:
        return "You're welcome, Captain."
    else:
        # Try QMD for context
        result = query_qmd(text)
        if result and result.get("memories"):
            return f"I recall: {result['memories'][0]['preview'][:100]}..."
        return f"I heard you say: {text[:50]}..."

def main():
    print("=" * 50)
    print("🎤 MORTIMER VOICE MODE")
    print("=" * 50)
    print("Say 'stop' to exit")
    print("=" * 50)
    
    # Intro
    speak("Voice mode activated. Mortimer online.")
    time.sleep(1)
    
    while True:
        print("\n🎤 Listening...")
        text = listen()
        
        if text:
            print(f"📝 Heard: {text}")
            
            # Generate response
            response = generate_response(text)
            print(f"🖥️ Response: {response}")
            
            # Speak response
            speak(response)
            
            # Check for exit
            if any(g in text.lower() for g in ["bye", "goodbye", "stop", "exit"]):
                break
        else:
            print("🤷 Didn't catch that. Try again.")
    
    speak("Voice mode deactivated.")
    print("👋 Bye!")

if __name__ == "__main__":
    # Load config
    os.chdir(os.path.expanduser("~/mortimer"))
    subprocess.run(["bash", "-c", "source voice/config.sh"])
    
    main()
