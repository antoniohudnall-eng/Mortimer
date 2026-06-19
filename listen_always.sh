#!/data/data/com.termux/files/usr/bin/bash
# MORTY CONTINUOUS LISTEN
# Listens → Transcribes → Responds → Repeats

RECORDING="/storage/3135-3139/Recordings/morty_chunk.wav"
LOG_FILE="/data/data/com.termux/files/home/mortimer/listen_log.md"

echo "🎤 MORTY CONTINUOUS LISTEN STARTED" | tee -a "$LOG_FILE"
echo "Say 'Morty' or just talk. Ctrl+C to stop." | tee -a "$LOG_FILE"

while true; do
    echo -n "🎤 Listening... " | tee -a "$LOG_FILE"
    
    # Record for 5 seconds (or until silence detection would be better)
    termux-microphone-record -d -f "$RECORDING" -l 5 2>/dev/null
    
    # Small pause
    sleep 1
    
    # Check if there's actual audio (file size > 10kb)
    SIZE=$(stat -c%s "$RECORDING" 2>/dev/null || echo "0")
    
    if [ "$SIZE" -gt 10000 ]; then
        echo "📝 Got audio ($SIZE bytes), transcribing..."
        
        # Play it back and transcribe
        TRANSCRIPT=$(termux-speech-to-text 2>/dev/null)
        
        if [ -n "$TRANSCRIPT" ] && [ "$TRANSCRIPT" != "ERROR: ERROR_NO_MATCH" ]; then
            echo "You said: $TRANSCRIPT" | tee -a "$LOG_FILE"
            
            # Check if they said something meaningful
            if [ ${#TRANSCRIPT} -gt 3 ]; then
                # Respond with voice
                echo "🤖 Responding..."
                termux-tts-speak "You said $TRANSCRIPT. Let me think about that."
            fi
        else
            echo "No speech detected, continuing..." | tee -a "$LOG_FILE"
        fi
    else
        echo "Silence, continuing..."
    fi
    
    sleep 1
done
