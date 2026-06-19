#!/bin/bash
# SECRETARY ASSISTANT LAUNCHER
PERSONALITY=${1:-morty}
echo "🧑‍💼 Starting Secretary Bot: $PERSONALITY"
cd ~/mortimer/secretary_assistant
python3 secretary_app.py
