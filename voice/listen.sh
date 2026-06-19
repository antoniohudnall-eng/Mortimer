#!/bin/bash
# Mortimer Voice Command
# Run this to speak to Mortimer

cd ~/mortimer
source voice/config.sh

echo "🎤 Speak now..."
TEXT=$(termux-speech-to-text)
echo "📝 Heard: $TEXT"

if [ ! -z "$TEXT" ]; then
    # Echo back using TTS
    python3 voice/speak.py "$TEXT" 2>/dev/null
    termux-media-player play ~/mortimer/voice/output/tts_*.mp3 2>/dev/null
fi
