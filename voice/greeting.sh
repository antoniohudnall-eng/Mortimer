#!/bin/bash
# Mortimer Wake Greeting
# Speaks appropriate greeting based on time of day

source ~/mortimer/voice/responses.sh

HOUR=$(date +%H)

if [ "$HOUR" -ge 5 ] && [ "$HOUR" -lt 12 ]; then
    # Morning: 5am - noon
    morning
elif [ "$HOUR" -ge 12 ] && [ "$HOUR" -lt 17 ]; then
    # Afternoon: noon - 5pm
    termux-tts-speak "Good afternoon, Captain. SEED3 at your service."
elif [ "$HOUR" -ge 17 ] && [ "$HOUR" -lt 21 ]; then
    # Evening: 5pm - 9pm
    evening
else
    # Night: 9pm - 5am
    night
fi
