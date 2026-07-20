#!/bin/bash
# Sweet Female Voice - Golden Mean Voice Settings
# Found from voice logs: female voices with fluid sound

# Voice settings from VOICE_LOG.md
# female1.wav: en-us+f1, s=162, p=52, a=110, k=0
# female2.wav: en-us+f2, s=160, p=55, a=105, k=0
# female3.wav: en-uk+f3, s=158, p=54, a=108, k=0

# Best sweet voice (f1 - American female)
VOICE="en-us+f1"
SPEED=162
PITCH=52
AMP=110
KEYTONE=0

# Speak function
speak() {
    espeak -v "$VOICE" -s "$SPEED" -p "$PITCH" -a "$AMP" -k "$KEYTONE" "$1"
}

# Quick command
alias say='speak'

echo "✅ Sweet voice loaded: en-us+f1, s=162, p=52, a=110"
