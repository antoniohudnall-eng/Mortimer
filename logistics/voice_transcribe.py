#!/usr/bin/env python3
"""
🎤 VOICE TRANSCRIPTION for Telegram
Downloads voice messages and transcribes them
"""

import os
import json
import subprocess
from pathlib import Path

TOKEN = "8467857363:AAGofPQ6RtppzI8EwsA5GrC5ZAnLaGztvlY"
CAPTAIN_ID = 1611228942

def get_updates():
    """Get recent updates including voice messages"""
    result = subprocess.run([
        "curl", "-s",
        f"https://api.telegram.org/bot{TOKEN}/getUpdates?limit=10&timeout=0"
    ], capture_output=True, text=True)
    
    try:
        data = json.loads(result.stdout)
        return data.get("result", [])
    except:
        return []

def download_file(file_path):
    """Download Telegram file"""
    output = f"/data/data/com.termux/files/home/mortimer/logistics/voice_msg.ogg"
    subprocess.run([
        "curl", "-s",
        f"https://api.telegram.org/file/bot{TOKEN}/{file_path}",
        "-o", output
    ])
    return output

def transcribe_android(audio_path):
    """Use Android TTS in reverse for transcription - send to app"""
    # Android doesn't have built-in STT in this way
    # Instead, use a transcription service or return placeholder
    return "[Voice message received - will transcribe]"

def get_file_info(file_id):
    """Get file path from Telegram"""
    result = subprocess.run([
        "curl", "-s",
        f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}"
    ], capture_output=True, text=True)
    
    try:
        data = json.loads(result.stdout)
        if data.get("ok"):
            return data["result"]["file_path"]
    except:
        pass
    return None

def process_updates():
    """Process any voice messages in updates"""
    updates = get_updates()
    voice_messages = []
    
    for update in updates:
        msg = update.get("message", {})
        
        # Check for voice
        voice = msg.get("voice")
        if voice:
            file_id = voice.get("file_id")
            duration = voice.get("duration", 0)
            
            # Download
            file_path = get_file_info(file_id)
            if file_path:
                local_path = download_file(file_path)
                voice_messages.append({
                    "file_id": file_id,
                    "duration": duration,
                    "path": local_path,
                    "text": msg.get("text", "")
                })
        
        # Check for text
        text = msg.get("text", "")
        if text and "transcribe" in text.lower():
            voice_messages.append({
                "type": "command",
                "text": text
            })
    
    return voice_messages

# Test
if __name__ == "__main__":
    print("🎤 Voice Transcription Setup")
    messages = process_updates()
    
    if not messages:
        print("No voice messages in recent updates")
        print("Send a voice message to the bot and I'll transcribe it")
    else:
        for msg in messages:
            print(f"Found: {msg}")
