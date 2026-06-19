#!/bin/bash
echo "Testing voice profiles..."
echo ""
echo "Profile 1: Phi Settings (Speed 161, Pitch 51, Amp 113, Key 4)"
termux-tts speak -r 1.0 -p 51 "Profile one. Phi settings. Golden ratio modulation."
sleep 2

echo "Profile 2: Deep Authority (Speed 140, Pitch 45, Amp 120, Key 5)"
termux-tts speak -r 0.9 -p 0.7 "Profile two. Deep authority. Slow and commanding."
sleep 2

echo "Profile 3: Clear Professional (Speed 150, Pitch 55, Amp 100, Key 3)"
termux-tts speak -r 1.0 -p 0.85 "Profile three. Clear and professional."
sleep 2

echo "Profile 4: Energetic (Speed 170, Pitch 58, Amp 110, Key 4)"
termux-tts speak -r 1.1 -p 0.9 "Profile four. Energetic and sharp."
sleep 2

echo "Done!"
