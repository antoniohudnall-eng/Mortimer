#!/bin/bash
# CREAM Web App Startup Script
# Port: 8084

cd /root/.openclaw/workspace/cream-web

# Check if Python dependencies are available
python3 -c "import fastapi" 2>/dev/null || echo "Note: FastAPI should be installed"

# Start the FastAPI app
echo "Starting CREAM on port 8084..."
echo "Access at: http://localhost:8084"
echo "Demo login: demo@cream.app / demo123"
python3 app/main.py
