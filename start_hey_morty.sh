#!/data/data/com.termux/files/usr/bin/bash
# Start Hey Morty listener
echo "Starting Hey Morty listener..."
nohup bash /data/data/com.termux/files/home/mortimer/hey_morty_listener.sh > /data/data/com.termux/files/home/mortimer/hey_morty.log 2>&1 &
echo "Hey Morty listener started (PID: $!)"
