#!/usr/bin/env python3
"""
N'og nog Brain Bridge Server
Connects AOS Brain socket to WebSocket clients (the game)
Bidirectional: Game state → Brain decisions → Game actions
"""

import asyncio
import websockets
import json
import socket
import threading
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger('nognog_bridge')

# Configuration
BRAIN_SOCKET_PATH = "/tmp/aos_brain.sock"
BRIDGE_WS_PORT = 8765
BRIDGE_HOST = "0.0.0.0"

class BrainBridge:
    """
    Bridge between Brain Unix Socket and WebSocket clients
    """
    def __init__(self):
        self.clients = set()
        self.brain_socket = None
        self.brain_connected = False
        self.brain_state = {}
        self.game_state = {}
        
    async def register_client(self, websocket):
        """Register a new WebSocket client"""
        self.clients.add(websocket)
        logger.info(f"Client connected. Total clients: {len(self.clients)}")
        
    async def unregister_client(self, websocket):
        """Unregister a WebSocket client"""
        self.clients.discard(websocket)
        logger.info(f"Client disconnected. Total clients: {len(self.clients)}")
        
    async def broadcast_to_clients(self, message: dict):
        """Send message to all connected WebSocket clients"""
        if not self.clients:
            return
            
        disconnected = set()
        for client in self.clients:
            try:
                await client.send(json.dumps(message))
            except Exception as e:
                logger.error(f"Failed to send to client: {e}")
                disconnected.add(client)
                
        # Clean up disconnected clients
        self.clients -= disconnected
        
    def query_brain(self, cmd: str, params: Optional[dict] = None) -> dict:
        """
        Send command to brain via Unix socket and return response
        """
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            sock.connect(BRAIN_SOCKET_PATH)
            
            request = {"cmd": cmd}
            if params:
                request["params"] = params
                
            sock.sendall(json.dumps(request).encode() + b'\n')
            
            # Receive response
            response = b''
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
                try:
                    # Try to parse as JSON - if it works, we have full message
                    json.loads(response.decode())
                    break
                except json.JSONDecodeError:
                    continue
                    
            sock.close()
            return json.loads(response.decode())
            
        except Exception as e:
            logger.error(f"Brain query failed: {e}")
            return {"error": str(e), "brain_connected": False}
            
    async def handle_game_state(self, game_state: dict) -> dict:
        """
        Process game state and get brain decision
        Returns: brain action to take
        """
        self.game_state = game_state
        
        # Build context for brain decision
        context = {
            "source": "nognog_universe",
            "player_position": game_state.get("player_pos", [0, 0, 0]),
            "player_velocity": game_state.get("player_vel", [0, 0, 0]),
            "nearby_objects": game_state.get("nearby", []),
            "threats": game_state.get("threats", []),
            "universe_type": game_state.get("universe", "PRIME"),
            "avatar_position": game_state.get("avatar_pos", [0, 0, 0]),
            "avatar_health": game_state.get("avatar_health", 100),
            "avatar_fuel": game_state.get("avatar_fuel", 100),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Query brain for decision
        response = self.query_brain("decide", {"context": context})
        
        # Extract action from brain response
        decision = response.get("decision", {})
        action = decision.get("action", "idle")
        
        # Map brain decision to game action
        game_action = {
            "type": action,
            "target": decision.get("target"),
            "thrust": decision.get("thrust", 0),
            "rotation": decision.get("rotation", [0, 0, 0]),
            "fire": decision.get("fire", False),
            "brain_state": response.get("state", "unknown"),
            "brain_mode": response.get("mode", "unknown"),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return game_action
        
    async def handle_client(self, websocket, path):
        """Handle WebSocket client connection"""
        await self.register_client(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    msg_type = data.get("type", "unknown")
                    
                    if msg_type == "game_state":
                        # Process game state and get brain action
                        game_state = data.get("state", {})
                        action = await self.handle_game_state(game_state)
                        
                        # Send action back to client
                        await websocket.send(json.dumps({
                            "type": "brain_action",
                            "action": action
                        }))
                        
                    elif msg_type == "ping":
                        await websocket.send(json.dumps({
                            "type": "pong",
                            "brain_connected": True,
                            "clients": len(self.clients)
                        }))
                        
                    elif msg_type == "brain_status":
                        # Query brain status
                        status = self.query_brain("status")
                        await websocket.send(json.dumps({
                            "type": "brain_status",
                            "status": status
                        }))
                        
                    elif msg_type == "brain_direct":
                        # Direct command to brain
                        cmd = data.get("cmd", "status")
                        params = data.get("params")
                        response = self.query_brain(cmd, params)
                        await websocket.send(json.dumps({
                            "type": "brain_response",
                            "response": response
                        }))
                        
                    else:
                        await websocket.send(json.dumps({
                            "type": "error",
                            "message": f"Unknown message type: {msg_type}"
                        }))
                        
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Invalid JSON"
                    }))
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client connection closed")
        finally:
            await self.unregister_client(websocket)
            
    async def start(self):
        """Start the bridge server"""
        logger.info(f"Starting N'og nog Brain Bridge on ws://{BRIDGE_HOST}:{BRIDGE_WS_PORT}")
        logger.info(f"Brain socket: {BRAIN_SOCKET_PATH}")
        
        # Test brain connection
        status = self.query_brain("status")
        if "error" in status:
            logger.warning(f"Brain not available: {status['error']}")
        else:
            logger.info(f"Brain connected! Status: {status.get('status', 'unknown')}")
            
        # Start WebSocket server
        async with websockets.serve(
            self.handle_client,
            BRIDGE_HOST,
            BRIDGE_WS_PORT,
            ping_interval=20,
            ping_timeout=10
        ):
            logger.info("Bridge server running. Waiting for connections...")
            await asyncio.Future()  # Run forever

def main():
    """Main entry point"""
    bridge = BrainBridge()
    
    try:
        asyncio.run(bridge.start())
    except KeyboardInterrupt:
        logger.info("Bridge server stopped by user")
    except Exception as e:
        logger.error(f"Bridge error: {e}")
        
if __name__ == "__main__":
    main()
