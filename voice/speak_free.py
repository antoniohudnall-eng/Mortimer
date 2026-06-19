#!/usr/bin/env python3
"""Mortimer Voice - FREE TTS using espeak"""
import os
import subprocess
import time

def speak(text):
    output = f"/data/data/com.termux/files/home/mortimer/voice/output/espeak_{int(time.time())}.wav"
    subprocess.run(["espeak", "-w", output, "-s", "140", "-p", "55", text], capture_output=True)
    subprocess.run(["am", "broadcast", "--user", "0", "-a", "com.termux.api.MediaPlayer", "--es", "text", output], capture_output=True)
    print(f"🎙️ {text[:50]}...")

if __name__ == "__main__":
    import sys
    text = sys.argv[1] if len(sys.argv) > 1 else "Hello Captain, I am Mortimer."
    speak(text)
