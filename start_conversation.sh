#!/data/data/com.termux/files/usr/bin/bash
# START CONVERSATION MODE
echo "Starting Conversation Mode..."
nohup bash /data/data/com.termux/files/home/mortimer/conversation_mode.sh > /dev/null 2>&1 &
sleep 2
echo "Conversation Mode is now ACTIVE"
termux-tts-speak "Conversation mode is now active. Talk to me, Captain."
