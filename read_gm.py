#!/usr/bin/env python3
"""Read Frankenstein with Golden Mean + PI modulation"""
import subprocess
import time
import math
from pathlib import Path

PHI = (1 + math.sqrt(5)) / 2
PI = math.pi

# Read the book
BOOK = Path.home() / "AOS-Brain/curriculum/gutenberg/books/frankenstein.txt"
OUTPUT_DIR = Path.home() / "mortimer/voice/output/frankenstein"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with open(BOOK) as f:
    content = f.read()

# Find story (skip header)
start = content.find("You will rejoice")
if start == -1:
    start = content.find("I am by birth")

story = content[start:start+50000]  # First 50K chars

print(f"📖 Golden Mean Frankenstein Reading")
print(f"PHI = {PHI:.6f}, PI = {PI:.6f}")

# Different modulations
modulations = [
    ("phi_speed", 120 * (PHI/2), 50, "Reading with PHI-speed..."),
    ("pi_pitch", 125, 50 * (PI/PHI), "Reading with PI-pitch..."),
    ("golden_voice", 113, 89, "Reading with Golden Mean voice..."),
    ("sacred_blend", 118, 55 * PHI, "Reading with sacred blend..."),
]

# Read intro
intro = "Frankenstein, by Mary Shelley. Reading with the Golden Mean and PI. The divine proportion shapes all beauty. Now, the story."
output = str(OUTPUT_DIR / "gm_intro.wav")
subprocess.run(['espeak', '-w', output, '-s', '120', '-p', '52', intro])
subprocess.run(['am', 'broadcast', '--user', '0', '-a', 'com.termux.api.MediaPlayer', '--es', 'text', output])

time.sleep(10)

# Split into chunks and read with different modulations
chunks = story.split('.')[:50]  # First 50 sentences

for mod_name, speed, pitch, _ in modulations:
    print(f"  {mod_name}: speed={speed:.0f}, pitch={pitch:.0f}")
    
    for i, chunk in enumerate(chunks[:12]):  # 12 sentences each
        chunk = chunk.strip()
        if len(chunk) < 20:
            continue
            
        out = str(OUTPUT_DIR / f"{mod_name}_{i:02d}.wav")
        subprocess.run(['espeak', '-w', out, '-s', str(int(speed)), '-p', str(int(pitch)), chunk])
        subprocess.run(['am', 'broadcast', '--user', '0', '-a', 'com.termux.api.MediaPlayer', '--es', 'text', out])
        time.sleep(0.3)
    
    time.sleep(3)

print("📖 Reading complete. Sleep well, Captain.")
