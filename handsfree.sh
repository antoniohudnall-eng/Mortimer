#!/data/data/com.termux/files/usr/bin/bash
# 🎤 MORTY HANDS-FREE - Simple Version
# Just listen → respond → listen
# Say "stop" to end

ACTIVE_FILE="/data/data/com.termux/files/home/mortimer/handsfree.active"
LOG_FILE="/data/data/com.termux/files/home/mortimer/conversation_log.md"
OLLAMA_URL="http://127.0.0.1:11434"

# Cleanup on exit
cleanup() {
    rm -f "$ACTIVE_FILE"
    termux-tts-speak "Hands-free mode ended."
    exit 0
}
trap cleanup SIGINT SIGTERM

# Check if already running
if [ -f "$ACTIVE_FILE" ]; then
    echo "Already active"
    exit 1
fi

# Start
echo "🎤 HANDS-FREE ACTIVE" > "$ACTIVE_FILE"
echo "[$(date)] HANDS-FREE SESSION STARTED" >> "$LOG_FILE"
termux-tts-speak "Hands-free mode is active. Talk to me."

echo "👂 Listening... (say 'stop' to end)"

while true; do
    [ ! -f "$ACTIVE_FILE" ] && break
    
    # Direct speech-to-text - waits for you to speak
    TRANSCRIPT=$(termux-speech-to-text 2>/dev/null)
    
    if [ -n "$TRANSCRIPT" ] && [ "$TRANSCRIPT" != "ERROR: ERROR_NO_MATCH" ]; then
        echo "You: $TRANSCRIPT"
        echo "[$(date)] You: $TRANSCRIPT" >> "$LOG_FILE"
        
        # Check for stop
        if echo "$TRANSCRIPT" | grep -iq "stop\|end\|goodnight\|bye"; then
            cleanup
        fi
        
        # Generate response
        echo "🤖 Thinking..."
        
        RESPONSE=$(curl -s -X POST "$OLLAMA_URL/api/generate" \
            -d "{
                \"model\": \"qwen2.5:1.5b\",
                \"prompt\": \"You are Morty, Captain's AI assistant. Brief, natural response. Captain said: $TRANSCRIPT\",
                \"stream\": false
            }" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response',''))" 2>/dev/null)
        
        [ -z "$RESPONSE" ] && RESPONSE="I'm here, Captain."
        
        echo "Morty: $RESPONSE"
        echo "[$(date)] Morty: $RESPONSE" >> "$LOG_FILE"
        
        termux-tts-speak "$RESPONSE"
    fi
done
