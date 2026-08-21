#!/bin/bash
# Start all Dusty MVP services

echo "Starting Dusty MVP services..."

# Start core-agent
cd /root/.openclaw/workspace/dusty_mvp_sandbox/core-agent
npm install > /dev/null 2>&1
nohup node src/index.js > /tmp/core-agent.log 2>&1 &
echo $! > /tmp/core-agent.pid
echo "✓ core-agent started (port 3000)"

# Start bridge-mock
cd /root/.openclaw/workspace/dusty_mvp_sandbox/bridge_mock
npm install > /dev/null 2>&1
nohup node bridge_mock.js > /tmp/bridge.log 2>&1 &
echo $! > /tmp/bridge.pid
echo "✓ bridge-mock started (port 3001)"

# Start openclaw-mock
cd /root/.openclaw/workspace/dusty_mvp_sandbox/openclaw_mock
npm install > /dev/null 2>&1
nohup node openclaw_mock.js > /tmp/openclaw.log 2>&1 &
echo $! > /tmp/openclaw.pid
echo "✓ openclaw-mock started (port 4000)"

sleep 2

# Health check
echo ""
echo "Health check:"
curl -s http://localhost:3000/status | grep -o '"status":"[^"]*"' || echo "  ✗ core-agent not responding"
curl -s http://localhost:3001/health | grep -o '"status":"[^"]*"' || echo "  ✗ bridge-mock not responding"
curl -s http://localhost:4000/status | grep -o '"status":"[^"]*"' || echo "  ✗ openclaw-mock not responding"
