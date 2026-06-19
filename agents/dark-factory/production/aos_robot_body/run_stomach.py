#!/usr/bin/env python3
import sys
sys.path.insert(0, '/root/.openclaw/workspace/aos_brain_py/stomach')
from ternary_stomach import TernaryStomach, StomachState
import time

stomach = TernaryStomach()
print("Stomach continuous runner started")

# Feed it some initial data
stomach.consume("Webster's Dictionary", complexity=0.3, nutrition=0.8)
stomach.consume("Brain Framework", complexity=0.5, nutrition=0.6)
stomach.consume("Agent Training Data", complexity=0.4, nutrition=0.7)

while True:
    stomach.digest()
    # Auto-feed if hungry
    if stomach.state == StomachState.HUNGRY:
        stomach.consume("Auto-feed data", complexity=0.2, nutrition=0.5)
    time.sleep(1)
