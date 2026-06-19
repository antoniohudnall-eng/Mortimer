#!/data/data/com.termux/files/usr/bin/bash
# 🎤 HEY MORTY - Wake Word Listener
# Listens for "Hey Morty" and activates conversation mode

LOG_FILE="/data/data/com.termux/files/home/mortimer/hey_morty.log"
ACTIVE_FILE="/data/data/com.termux/files/home/mortimer/hey_morty.active"
OLLAMA_URL="http://127.0.0.1:11434"

echo "🎤 HEY MORTY LISTENER ACTIVE"
echo "$(date): Hey Morty listener started" >> "$LOG_FILE"

while true; do
    # Listen for speech
    TRANSCRIPT=$(termux-speech-to-text 2>/dev/null)
    
    if [ -n "$TRANSCRIPT" ] && [ "$TRANSCRIPT" != "ERROR: ERROR_NO_MATCH" ]; then
        LOWER=$(echo "$TRANSCRIPT" | tr '[:upper:]' '[:lower:]')
        
        # Check for wake word
        if echo "$LOWER" | grep -q "hey morty\|hey mortimer\|hey mort"; then
            echo "$(date): Wake word detected: $TRANSCRIPT" >> "$LOG_FILE"
            
            # Speak acknowledgment
            termux-tts-speak "Yes, Captain? I am here."
            
            # Start conversation mode
            echo "Starting conversation mode..."
            nohup bash /data/data/com.termux/files/home/mortimer/conversation_mode.sh > /dev/null 2>&1 &
            
            # Wait for conversation to end
            while [ -f /data/data/com.termux/files/home/mortimer/conversation_mode.active ]; do
                sleep 2
            done
            
            echo "$(date): Conversation ended, resuming listener" >> "$LOG_FILE"
        fi
    fi
    
    sleep 0.5
done
