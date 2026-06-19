#!/usr/bin/env python3
"""
📖 Frankenstein - Read to Captain
Chapter by chapter, voice narration
"""

import subprocess
import time
from pathlib import Path

BOOK = "/data/data/com.termux/files/home/AOS-Brain/curriculum/gutenberg/books/frankenstein.txt"
OUTPUT_DIR = "/data/data/com.termux/files/home/mortimer/voice/output/frankenstein"
CHUNK_SIZE = 800  # characters per chunk

def speak_chunk(text, filename):
    """Generate speech for a text chunk"""
    subprocess.run(['espeak', '-w', filename, '-s', '130', '-p', '50', text], capture_output=True)
    # Play it
    subprocess.run(['am', 'broadcast', '--user', '0', '-a', 'com.termux.api.MediaPlayer', '--es', 'text', filename], capture_output=True)

def read_chapter(chapter_num, title, content):
    """Read a chapter aloud"""
    print(f"📖 Chapter {chapter_num}: {title}")
    
    # Split content into chunks
    chunks = [content[i:i+CHUNK_SIZE] for i in range(0, len(content), CHUNK_SIZE)]
    
    for i, chunk in enumerate(chunks):
        if len(chunk.strip()) < 50:
            continue
        filename = f"{OUTPUT_DIR}/ch{chapter_num}_{i}.wav"
        speak_chunk(chunk, filename)
        time.sleep(0.5)  # Brief pause between chunks
    
    time.sleep(2)  # Pause between chapters

def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    with open(BOOK, 'r') as f:
        content = f.read()
    
    # Find chapters
    lines = content.split('\n')
    
    current_chapter = 0
    current_title = ""
    current_content = []
    in_chapter = False
    
    chapters = []
    
    for line in lines:
        # Detect chapter headers
        if 'LETTER' in line.upper() and 'WALTON' in line.upper():
            if current_content:
                chapters.append((current_chapter, current_title, '\n'.join(current_content)))
            current_chapter += 1
            current_title = line.strip()[:80]
            current_content = []
            in_chapter = True
        elif 'CHAPTER' in line.upper() and len(line) < 50:
            if current_content:
                chapters.append((current_chapter, current_title, '\n'.join(current_content)))
            current_chapter += 1
            current_title = line.strip()
            current_content = []
        elif in_chapter:
            current_content.append(line)
    
    # Add last chapter
    if current_content:
        chapters.append((current_chapter, current_title, '\n'.join(current_content)))
    
    print(f"📖 Found {len(chapters)} chapters")
    print("Starting to read...")
    
    # Introduction
    intro = "Frankenstein, by Mary Shelley. Chapter one. Introduction."
    speak_chunk(intro, f"{OUTPUT_DIR}/intro.wav")
    time.sleep(3)
    
    # Read first 3 chapters (Captain is falling asleep)
    for i, (num, title, text) in enumerate(chapters[:3]):
        if title:
            read_chapter(num, title, text)
            time.sleep(3)
    
    print("📖 Goodnight, Captain. Rest well.")

if __name__ == "__main__":
    main()
