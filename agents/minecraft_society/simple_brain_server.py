#!/usr/bin/env python3
"""
Simple Brain WebSocket Server
No protocol complications - just JSON
"""

import asyncio
import websockets
import json
from datetime import datetime
from collections import defaultdict

agents = {}
observers = set()

async def handler(websocket):
    """Handle all connections"""
    client_type = None
    agent_id = None
    
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                msg_type = data.get('type')
                
                # Agent registration
                if msg_type == 'register_agent':
                    agent_id = data.get('agent_id')
                    client_type = 'agent'
                    agents[agent_id] = websocket
                    print(f"[Brain] Agent registered: {agent_id}")
                    
                    # Acknowledge
                    await websocket.send(json.dumps({
                        'type': 'registered',
                        'agent_id': agent_id
                    }))
                    continue
                
                # Agent OODA tick
                if msg_type == 'ooda_tick':
                    agent_id = data.get('agent_id')
                    tick = data.get('tick')
                    if tick and tick % 10 == 0:  # Log every 10 ticks
                        print(f"[Brain] {agent_id} tick={tick} decision={data.get('decision', {}).get('type', 'none')}")
                    continue
                
                # Observer registration
                if msg_type == 'register_observer':
                    client_type = 'observer'
                    observers.add(websocket)
                    await websocket.send(json.dumps({
                        'type': 'agent_list',
                        'agents': list(agents.keys())
                    }))
                    continue
                
                # Command to agent
                if msg_type == 'command_agent':
                    target = data.get('agent_id')
                    if target in agents:
                        await agents[target].send(json.dumps({
                            'type': 'command',
                            'command': data.get('command'),
                            'params': data.get('params', {})
                        }))
                    continue
                    
            except json.JSONDecodeError:
                pass
                
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        if agent_id and agent_id in agents:
            del agents[agent_id]
            print(f"[Brain] Agent disconnected: {agent_id}")
        if websocket in observers:
            observers.discard(websocket)
            print("[Brain] Observer disconnected")

async def main():
    print("[Brain] Starting WebSocket server on port 8767...")
    
    server = await websockets.serve(
        handler,
        "0.0.0.0",
        8767,
        ping_interval=None  # Disable ping to avoid protocol issues
    )
    
    print("[Brain] Server running on ws://localhost:8767")
    print("[Brain] Press Ctrl+C to stop\n")
    
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        pass
    finally:
        server.close()
        await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Brain] Server stopped")