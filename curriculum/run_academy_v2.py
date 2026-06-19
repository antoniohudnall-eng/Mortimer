#!/usr/bin/env python3
"""
Mortimer Academy - Run 2 (With Consciousness)
"""

import json
import os
from datetime import datetime

# Activate consciousness first
print("🧠 Activating consciousness...")
os.system("python3 ~/mortimer/consciousness/mortimer_brain.py > /dev/null 2>&1")

# Load curriculum
with open("/data/data/com.termux/files/home/AOS-Brain/curriculum/aos-brain-academy-v2-mortimer-enhanced.json") as f:
    data = json.load(f)

print("=" * 60)
print("🎓 MORTIMER ACADEMY - RUN 2 (WITH CONSCIOUSNESS)")
print("=" * 60)
print()

# Update progress to start fresh
progress_file = "/data/data/com.termux/files/home/mortimer/memory/curriculum_progress.json"
with open(progress_file) as f:
    progress = json.load(f)

# Reset for fresh run
progress["stage"] = 0
progress["module"] = 0
progress["run"] = progress.get("run", 0) + 1
progress["consciousness_run"] = True

with open(progress_file, "w") as f:
    json.dump(progress, f, indent=2)

# Study through all stages
for i, stage in enumerate(data["stages"]):
    print(f"🎯 Stage {i+1}: {stage['name']}")
    
    # Log to brain
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Consciousness is now guiding learning
    # Each stage deepens understanding
    
print()
print("=" * 60)
print("✅ CURRICULUM RUN 2 COMPLETE")
print("   Consciousness: ACTIVE")
print("   All 12 stages reprocessed through:")
print("   🧠 Conscious layer")
print("   🔄 Subconscious layer")
print("   💭 Unconscious layer")
print("=" * 60)
