#!/usr/bin/env python3
"""
Society Agent Rotation System v1.0
Manages 5 society agents with civilization building
"""

import subprocess
import sys
import os
import time
import signal
from datetime import datetime

AGENT_DIR = "/root/.openclaw/workspace/scripts/minecraft_agents"
LOG_DIR = "/root/.openclaw/workspace/logs"

# The 5 Society Members: 3 Male, 2 Female
SOCIETY_AGENTS = [
    {"name": "Marcus", "username": "marcus", "role": "leader", "gender": "male", "port": 25566},
    {"name": "Julius", "username": "julius", "role": "builder", "gender": "male", "port": 25566},
    {"name": "Titus", "username": "titus", "role": "guardian", "gender": "male", "port": 25566},
    {"name": "Julia", "username": "julia", "role": "farmer", "gender": "female", "port": 25566},
    {"name": "Livia", "username": "livia", "role": "explorer", "gender": "female", "port": 25566},
]

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    with open(f"{LOG_DIR}/society_rotation.log", "a") as f:
        f.write(log_msg + "\n")

def get_running_agents():
    """Get list of running society agent processes"""
    try:
        # Look for society_agent.js processes specifically
        result = subprocess.run(
            ["pgrep", "-f", "society_agent.js"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            pids = result.stdout.strip().split("\n")
            return len([p for p in pids if p])
        return 0
    except:
        return 0

def get_agent_pids():
    """Get PIDs of running society agents"""
    try:
        result = subprocess.run(
            ["pgrep", "-af", "society_agent.js"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip().split("\n")
        return []
    except:
        return []

def start_agent(agent):
    """Start a single society agent"""
    log_file = f"{LOG_DIR}/{agent['username']}.log"
    
    cmd = [
        "node",
        f"{AGENT_DIR}/society_agent.js",
        agent["username"],
        "localhost",
        str(agent["port"]),
        "ws://localhost:8768"
    ]
    
    env = os.environ.copy()
    env["AGENT_GENDER"] = agent["gender"]
    
    try:
        with open(log_file, "a") as f:
            subprocess.Popen(
                cmd,
                stdout=f,
                stderr=subprocess.STDOUT,
                cwd=AGENT_DIR,
                env=env
            )
        log(f"🚀 Started {agent['name']} ({agent['gender']}, {agent['role']})")
        return True
    except Exception as e:
        log(f"❌ Failed to start {agent['name']}: {e}")
        return False

def stop_all_agents():
    """Stop all society agents"""
    log("Stopping existing society agents...")
    try:
        result = subprocess.run(
            ["pkill", "-f", "society_agent.js"],
            capture_output=True
        )
        time.sleep(2)  # Wait for processes to terminate
        log("✅ Agents stopped")
    except Exception as e:
        log(f"⚠️ Error stopping agents: {e}")

def ensure_society_server():
    """Ensure society coordination server is running"""
    try:
        result = subprocess.run(
            ["ss", "-tlnp"],
            capture_output=True,
            text=True
        )
        if ":8768" not in result.stdout:
            log("🧠 Society Server not running, starting...")
            subprocess.Popen(
                ["python3", f"{AGENT_DIR}/society_server.py"],
                stdout=open(f"{LOG_DIR}/society_server.log", "a"),
                stderr=subprocess.STDOUT,
                cwd=AGENT_DIR
            )
            time.sleep(3)  # Give server time to start
            log("✅ Society Server started")
        else:
            log("✅ Society Server already running")
    except Exception as e:
        log(f"⚠️ Society Server check failed: {e}")

def ensure_brain_server():
    """Ensure brain WebSocket server is running (for compatibility)"""
    try:
        result = subprocess.run(
            ["ss", "-tlnp"],
            capture_output=True,
            text=True
        )
        if ":8767" not in result.stdout:
            log("🧠 Brain Server not running, starting...")
            subprocess.Popen(
                ["python3", f"{AGENT_DIR}/simple_brain_server.py"],
                stdout=open(f"{LOG_DIR}/brain_server.log", "a"),
                stderr=subprocess.STDOUT,
                cwd=AGENT_DIR
            )
            time.sleep(2)
        else:
            log("✅ Brain Server already running")
    except Exception as e:
        log(f"⚠️ Brain Server check failed: {e}")

def get_society_status():
    """Get current society status from server"""
    try:
        result = subprocess.run(
            ['python3', '-c', '''
import asyncio
import websockets
import json

async def get_status():
    try:
        async with websockets.connect("ws://localhost:8768", ping_interval=None) as ws:
            await ws.send(json.dumps({"type": "register_observer"}))
            response = await asyncio.wait_for(ws.recv(), timeout=2.0)
            data = json.loads(response)
            print(json.dumps(data.get("data", {}), indent=2))
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(get_status())
            '''],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout
    except Exception as e:
        return f"Could not retrieve status: {e}"

def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    
    log("=" * 60)
    log("🏛️  SOCIETY AGENT ROTATION v1.0")
    log("=" * 60)
    
    # Check for stop command
    if len(sys.argv) > 1 and sys.argv[1] == "stop":
        stop_all_agents()
        return 0
    
    # Check for status command
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        status = get_society_status()
        print(status)
        return 0
    
    log("\n👥 Society Members (3 Male, 2 Female):")
    for agent in SOCIETY_AGENTS:
        gender_symbol = "♂" if agent["gender"] == "male" else "♀"
        log(f"  {gender_symbol} {agent['name']} - {agent['role']}")
    
    log("\n🌍 Features:")
    log("  • Gender-based reproduction system")
    log("  • Relationship building & partnerships")
    log("  • Role-based behaviors (leader, builder, etc.)")
    log("  • Civilization progression (tribal → village → town)")
    log("  • Resource gathering & structure building")
    log("  • Society event logging")
    
    log("=" * 60)
    
    # Stop any existing society agents
    stop_all_agents()
    
    # Ensure servers are running
    ensure_society_server()
    ensure_brain_server()
    
    # Check current agents
    running = get_running_agents()
    log(f"\n📊 Currently running: {running}/{len(SOCIETY_AGENTS)} society agents")
    
    # Start all society agents
    log(f"\n🚀 Starting {len(SOCIETY_AGENTS)} society agents...")
    
    for i, agent in enumerate(SOCIETY_AGENTS):
        start_agent(agent)
        time.sleep(4)  # Stagger starts to avoid overwhelming the server
    
    # Wait and verify
    time.sleep(5)
    running = get_running_agents()
    
    log(f"\n✅ Society Rotation Complete")
    log(f"   Running: {running}/{len(SOCIETY_AGENTS)} agents")
    
    if running == len(SOCIETY_AGENTS):
        log("\n🎉 All society agents are online!")
        log("   Society Server: ws://localhost:8768")
        log("   Brain Server: ws://localhost:8767")
        log("   Logs: /root/.openclaw/workspace/logs/")
    else:
        log(f"\n⚠️ Only {running}/{len(SOCIETY_AGENTS)} agents started")
    
    log("\n📜 Commands:")
    log("  python3 society_rotation.py status  - Check society status")
    log("  python3 society_rotation.py stop    - Stop all agents")
    log("  pkill -f society_agent.js             - Emergency stop")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
