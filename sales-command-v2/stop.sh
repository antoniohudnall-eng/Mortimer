#!/bin/bash
pkill -f "http.server 3333"
rm -f server.pid
echo "✅ Command Center stopped"
