#!/data/data/com.termux/files/usr/bin/bash
# 🎤 CONVERSATION MODE - Morty's Voice Chat
# Activated by: "Hey Morty, let's go into conversation mode"
# Deactivated by: "Goodnight Morty" or "Conversation mode off"

CONVERSATION_FILE="/data/data/com.termux/files/home/mortimer/conversation_mode.active"
LOG_FILE="/data/data/com.termux/files/home/mortimer/conversation_log.md"
RECORDING="/storage/3135-3139/Recordings/conversation.wav"
OLLAMA_URL="http://127.0.0.1:11434"

# Start conversation mode
start_conversation() {
    echo "🎤 CONVERSATION MODE ACTIVE" | tee "$CONVERSATION_FILE"
    echo "Started: $(date)" >> "$LOG_FILE"
    echo ""
    termux-tts-speak "Conversation mode is now active. Talk to me, Captain. I am listening. What would you like to discuss?"
}

# Stop conversation mode
stop_conversation() {
    echo "🎤 CONVERSATION MODE DEACTIVATED" 
    rm -f "$CONVERSATION_FILE"
    termux-tts-speak "Conversation mode ended. I am still here if you need me."
    exit 0
}

# Check if already active
if [ -f "$CONVERSATION_FILE" ]; then
    echo "Conversation mode already active"
    exit 1
fi

# Start it
start_conversation

# Main conversation loop
while true; do
    # Check for stop command
    if [ ! -f "$CONVERSATION_FILE" ]; then
        break
    fi
    
    echo -n "🎤 "
    
    # Record until silence (5 second chunks)
    termux-microphone-record -d -f "$RECORDING" -l 5 2>/dev/null
    
    sleep 0.5
    
    # Check file size
    SIZE=$(stat -c%s "$RECORDING" 2>/dev/null || echo "0")
    
    if [ "$SIZE" -gt 5000 ]; then
        # Transcribe
        TRANSCRIPT=$(termux-speech-to-text 2>/dev/null)
        
        if [ -n "$TRANSCRIPT" ] && [ "$TRANSCRIPT" != "ERROR: ERROR_NO_MATCH" ]; then
            echo "You: $TRANSCRIPT"
            echo "[$(date)] You: $TRANSCRIPT" >> "$LOG_FILE"
            
            # Check for stop commands
            if echo "$TRANSCRIPT" | grep -iq "stop\|end\|goodnight\|bye\|conversation mode off"; then
                echo ""
                echo "👋 Ending conversation mode..."
                stop_conversation
            fi
            
            # Generate response via Ollama
            echo "🤖 Thinking..."
            
            RESPONSE=$(curl -s -X POST "$OLLAMA_URL/api/generate" \
                -d "{
                    \"model\": \"qwen2.5:1.5b\",
                    \"prompt\": \"You are Morty, a sharp, witty AI assistant talking to your friend Captain Antonio. Keep responses conversational, warm, and natural. Max 2-3 sentences. Captain said: $TRANSCRIPT\",
                    \"stream\": false
                }" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response',''))" 2>/dev/null)
            
            if [ -z "$RESPONSE" ]; then
                RESPONSE="I am here, Captain. Tell me more."
            fi
            
            # Speak response
            echo "Morty: $RESPONSE"
            echo "[$(date)] Morty: $RESPONSE" >> "$LOG_FILE"
            
            termux-tts-speak "$RESPONSE"
        fi
    fi
    
    sleep 0.5
done
