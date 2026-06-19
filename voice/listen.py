#!/usr/bin/env python3
"""
Mortimer Voice Listener
Uses termux-speech-to-text for speech recognition
"""

import subprocess
import sys
import os

def listen():
    """Listen for speech and return text"""
    try:
        result = subprocess.run(
            ['termux-speech-to-text'],
            capture_output=True,
            text=True,
            timeout=30
        )
        text = result.stdout.strip()
        if text:
            return text
        return None
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    print("🎤 Mortimer listening... (Ctrl+C to stop)")
    print("Speak now...")
    
    while True:
        try:
            text = listen()
            if text:
                print(f"📝 Heard: {text}")
                # Process the command
                process(text)
        except KeyboardInterrupt:
            print("\n👋 Stopped listening")
            break

def process(text):
    """Process voice command"""
    text = text.lower()
    
    # Simple command handling
    if "hello" in text or "hey" in text:
        print("👋 Hello back!")
    elif "status" in text or "report" in text:
        print("✅ All systems operational")
    elif "stop" in text or "quit" in text:
        print("👋 Goodbye!")
        sys.exit(0)
    else:
        print(f"🤔 Got: {text}")

if __name__ == "__main__":
    main()
