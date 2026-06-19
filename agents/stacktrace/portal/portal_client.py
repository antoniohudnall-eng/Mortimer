#!/usr/bin/env python3
"""
🌀 PORTAL CLIENT — STACKTRACE
Connects to Fleet Portal Network
"""

import asyncio
import websockets
import json
import ssl
import sys

PORTAL_URL = "wss://mortimer:9000"
AGENT_ID = "stacktrace"
TOKEN = "stacktrace-portal-2024-secure"

async def connect():
    """Connect to portal hub"""
    ctx = ssl.SSLContext()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE  # Self-signed cert
    
    async with websockets.connect(PORTAL_URL, ssl=ctx) as ws:
        # Authenticate
        await ws.send(json.dumps({
            "agent_id": AGENT_ID,
            "token": TOKEN
        }))
        
        auth_response = await ws.recv()
        data = json.loads(auth_response)
        
        if "error" in data:
            print(f"❌ Auth failed: {data['error']}")
            return
            
        print(f"✅ {AGENT_ID} connected to Portal")
        print(f"🌀 Standing by for recall/dispatch...")
        
        while True:
            try:
                msg = await ws.recv()
                data = json.loads(msg)
                
                action = data.get('action')
                
                if action == 'recall':
                    print(f"🚨 RECALL from {data.get('from')}: {data.get('priority', 'normal')}}")
                    print(f"   Mission: {data.get('mission', 'None specified')}")
                    
                elif action == 'dispatch':
                    print(f"📡 DISPATCH: {data.get('mission', 'New assignment')}")
                    
                elif action == 'status':
                    await ws.send(json.dumps({
                        "agent": AGENT_ID,
                        "status": "online",
                        "timestamp": asyncio.get_event_loop().time()
                    }))
                    
                else:
                    print(f"📨 Message: {data}")
                    
            except websockets.exceptions.ConnectionClosed:
                print("⚠ Portal connection closed")
                break

if __name__ == "__main__":
    try:
        asyncio.run(connect())
    except KeyboardInterrupt:
        print(f"\n👋 {AGENT_ID} disconnecting from Portal")
