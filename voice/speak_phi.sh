#!/bin/bash
# Mortimer φ-Voice Speak Script
# Golden Ratio modulated: speed=161, pitch=51, amp=113, kt=4

VOICE="-v en-us+m3 -s 161 -p 51 -a 113 -k 4"

if [ -z "$1" ]; then
    echo "Usage: $0 \"Your message\""
    echo "Mortimer φ-Voice: speed=161, pitch=51, amp=113, kt=4"
    exit 1
fi

espeak $VOICE "$*" 2>/dev/null
