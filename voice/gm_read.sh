#!/bin/bash
# GM/PI Voice Reading Script
# Golden Mean voice settings for espeak

# Settings from MyL0n ROS
GM=1.6180339887
PI=3.1415926535

# espeak parameters (scaled × 100)
SPEED=161
PITCH=51
AMP=113
KEYTONE=4
VOICE="en-us"

# Output file
OUTPUT="${1:-/tmp/gm_voice.wav}"

# Read from file or stdin
if [ -f "$1" ] && [ -n "$1" ]; then
    TEXT=$(cat "$1")
else
    TEXT="$*"
fi

if [ -z "$TEXT" ]; then
    echo "Usage: gm_read.sh \"text\" or gm_read.sh <file.txt>"
    exit 1
fi

# Generate voice
espeak -v "$VOICE" -s "$SPEED" -p "$PITCH" -a "$AMP" -k "$KEYTONE" -w "$OUTPUT" "$TEXT"

# Play
termux-media-player play "$OUTPUT"

echo "✅ Played: $OUTPUT"
