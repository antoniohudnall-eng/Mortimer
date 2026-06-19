#!/usr/bin/env python3
"""
📖 Read Frankenstein using Android TTS
Much better voice than espeak!
"""

import subprocess
import time

def speak(text):
    """Speak using Android TTS via termux API"""
    subprocess.run([
        'am', 'broadcast',
        '--user', '0',
        '-a', 'com.termux.api.TextToSpeech',
        '--es', 'text', text
    ])

def read_file(filepath, chunk_size=500):
    """Read a text file and speak it in chunks"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find story start
    start = content.find("I am by birth")
    if start == -1:
        start = content.find("You will rejoice")
    
    story = content[start:]
    
    # Split into sentences
    sentences = story.replace('!', '.').replace('?', '.').split('.')
    
    current_chunk = ""
    
    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if len(sentence) < 20:
            continue
            
        current_chunk += sentence + ". "
        
        if len(current_chunk) >= chunk_size:
            speak(current_chunk)
            print(f"Speaking: {current_chunk[:50]}...")
            current_chunk = ""
            time.sleep(5)  # Pause between chunks
        elif i == len(sentences) - 1 and current_chunk:
            speak(current_chunk)
            print(f"Final: {current_chunk[:50]}...")
    
    return len(sentences)

def main():
    print("📖 Frankenstein - Android TTS Reading")
    print("=" * 40)
    
    # Introduction
    intro = "Frankenstein, by Mary Shelley. Chapter One. I am reading to you now."
    speak(intro)
    print("Introduction spoken...")
    time.sleep(5)
    
    # Read the book
    book_path = "/data/data/com.termux/files/home/AOS-Brain/curriculum/gutenberg/books/frankenstein.txt"
    
    sentences = read_file(book_path)
    print(f"Read {sentences} sentences")
    
    # Conclusion
    time.sleep(3)
    outro = "The end of Chapter One. Sleep well, Captain. I will be here when you wake."
    speak(outro)
    print("Goodnight spoken...")

if __name__ == "__main__":
    main()
