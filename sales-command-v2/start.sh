#!/bin/bash
cd /data/data/com.termux/files/home/mortimer/sales-command-v2
python3 -m http.server 3333 > logs/server.log 2>&1 &
echo $! > server.pid
echo "✅ Command Center started"
