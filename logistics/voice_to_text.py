#!/usr/bin/env python3
"""
🎤 Telegram Voice → Transcription
Download voice from Telegram, transcribe with termux-speech-to-text
"""

import os
import json
import subprocess
import time
from pathlib import Path

TOKEN = "8467857363:AAGofPQ6RtppzI8EwsA5GrC5ZAnLaGztvlY"
CAPTAIN_ID = 1611228942
LOGISTICS_DIR = Path.home() / "mortimer" / "logistics"
TRANSCRIPTS_FILE = LOGISTICS_DIR / "transcripts.json"

def load_transcripts():
    if TRANSCRIPTS_FILE.exists():
        with open(TRANSCRIPTS_FILE) as f:
            return json.load(f)
    return []

def save_transcripts(data):
    with open(TRANSCRIPTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_updates():
    """Get recent messages"""
    result = subprocess.run([
        "curl", "-s",
        f"https://api.telegram.org/bot{TOKEN}/getUpdates?limit=20"
    ], capture_output=True, text=True)
    try:
        return json.loads(result.stdout).get("result", [])
    except:
        return []

def download_voice(file_path):
    """Download voice file from Telegram"""
    output = str(LOGISTICS_DIR / "voice_msg.ogg")
    subprocess.run([
        "curl", "-s",
        f"https://api.telegram.org/file/bot{TOKEN}/{file_path}",
        "-o", output
    ], check=True)
    return output

def transcribe(audio_path):
    """Transcribe audio using termux-speech-to-text"""
    result = subprocess.run(
        ["termux-speech-to-text"],
        capture_output=True,
        text=True,
        timeout=30
    )
    return result.stdout.strip()

def process_new_voices():
    """Check for new voice messages and transcribe them"""
    updates = get_updates()
    transcripts = load_transcripts()
    new_count = 0
    
    # Get last processed update ID
    last_id = transcripts[0].get("update_id", 0) if transcripts else 0
    
    for update in updates:
        update_id = update.get("update_id", 0)
        if update_id <= last_id:
            continue
        
        msg = update.get("message", {})
        voice = msg.get("voice")
        
        if voice:
            file_id = voice.get("file_id")
            duration = voice.get("duration", 0)
            
            # Check if already transcribed
            if any(t.get("file_id") == file_id for t in transcripts):
                continue
            
            # Download voice
            file_path = f"voice/{file_id}.ogg"
            try:
                dl_result = subprocess.run([
                    "curl", "-s",
                    f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}"
                ], capture_output=True, text=True)
                file_data = json.loads(dl_result.stdout)
                if file_data.get("ok"):
                    path = file_data["result"]["file_path"]
                    local_path = download_voice(path)
                    
                    # Play and transcribe
                    print(f"🎤 Transcribing {duration}s voice message...")
                    text = transcribe(local_path)
                    
                    if text:
                        transcripts.insert(0, {
                            "update_id": update_id,
                            "file_id": file_id,
                            "text": text,
                            "duration": duration,
                            "time": time.strftime("%Y-%m-%d %H:%M")
                        })
                        print(f"✅: {text[:100]}...")
                        new_count += 1
            except Exception as e:
                print(f"❌ Error: {e}")
    
    if new_count > 0:
        save_transcripts(transcripts)
    
    return new_count, transcripts[:10]

if __name__ == "__main__":
    print("🎤 Checking for voice messages...")
    new, recent = process_new_voices()
    print(f"\nFound {new} new voice messages")
    
    if recent:
        print("\nRecent transcripts:")
        for t in recent[:5]:
            print(f"  [{t.get('time')}] {t.get('text', '')[:80]}...")
