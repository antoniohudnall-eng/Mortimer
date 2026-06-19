#!/usr/bin/env python3
"""
MYL Agents Minecraft Integration

Embody MYL agents (0-6) in Minecraft for:
- Navigation and exploration
- Building and crafting
- Social interaction
- Economy and trading

Dark Factory agents become embodied through Minecraft bridge.
"""

import socket
import json
import time
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MYLMinecraft")

MINECRAFT_HOST = "localhost"
MINECRAFT_PORT = 25565
OBSERVER_PORT = 8765
ACTOR_PORT = 8766

@dataclass
class AgentBody:
    """Physical body state in Minecraft"""
    agent_id: str
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    yaw: float = 0.0
    pitch: float = 0.0
    health: float = 20.0
    hunger: float = 20.0
    inventory: List[Dict] = None
    
    def __post_init__(self):
        if self.inventory is None:
            self.inventory = []
    
    def position(self) -> List[float]:
        return [self.x, self.y, self.z]

class MYLMinecraftBridge:
    """Bridge between MYL agents and Minecraft world"""
    
    def __init__(self):
        self.agents: Dict[str, AgentBody] = {}
        self.world_state: Dict = {}
        self.logger = logger
        
        # Connection to Minecraft observer
        self.observer_socket = None
        # Connection to Minecraft actor
        self.actor_socket = None
        
    def connect(self) -> bool:
        """Connect to Minecraft bridge"""
        try:
            # Connect to observer (world state)
            self.observer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.observer_socket.connect((MINECRAFT_HOST, OBSERVER_PORT))
            self.logger.info("Connected to Minecraft Observer")
            
            # Connect to actor (agent actions)
            self.actor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.actor_socket.connect((MINECRAFT_HOST, ACTOR_PORT))
            self.logger.info("Connected to Minecraft Actor")
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")
            return False
    
    def spawn_agent(self, agent_id: str, x: float = 0, y: float = 100, z: float = 0) -> bool:
        """Spawn MYL agent in Minecraft"""
        if agent_id in self.agents:
            self.logger.warning(f"Agent {agent_id} already spawned")
            return False
        
        # Create agent body
        self.agents[agent_id] = AgentBody(
            agent_id=agent_id,
            x=x, y=y, z=z
        )
        
        # Send spawn command to Minecraft
        spawn_cmd = {
            "type": "spawn_agent",
            "agent_id": agent_id,
            "x": x,
            "y": y,
            "z": z
        }
        
        try:
            if self.actor_socket:
                self.actor_socket.send(json.dumps(spawn_cmd).encode() + b'\n')
                self.logger.info(f"Spawned {agent_id} at ({x}, {y}, {z})")
                return True
        except Exception as e:
            self.logger.error(f"Failed to spawn {agent_id}: {e}")
            return False
        
        return True
    
    def observe_world(self) -> Dict:
        """Get current world state"""
        try:
            if self.observer_socket:
                # Request world state
                self.observer_socket.send(b'{"type": "get_state"}\n')
                
                # Receive response
                data = self.observer_socket.recv(4096).decode()
                self.world_state = json.loads(data)
                return self.world_state
        except Exception as e:
            self.logger.error(f"Failed to observe world: {e}")
            return {}
    
    def agent_action(self, agent_id: str, action: str, params: Dict = None) -> bool:
        """Send action from MYL agent to Minecraft"""
        if agent_id not in self.agents:
            self.logger.error(f"Agent {agent_id} not spawned")
            return False
        
        cmd = {
            "type": "agent_action",
            "agent_id": agent_id,
            "action": action,
            "params": params or {}
        }
        
        try:
            if self.actor_socket:
                self.actor_socket.send(json.dumps(cmd).encode() + b'\n')
                self.logger.debug(f"{agent_id} executed {action}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to send action: {e}")
            return False
        
        return True
    
    def move_agent(self, agent_id: str, dx: float, dy: float, dz: float) -> bool:
        """Move agent relative to current position"""
        return self.agent_action(agent_id, "move", {"dx": dx, "dy": dy, "dz": dz})
    
    def agent_look(self, agent_id: str, yaw: float, pitch: float) -> bool:
        """Set agent look direction"""
        return self.agent_action(agent_id, "look", {"yaw": yaw, "pitch": pitch})
    
    def agent_break_block(self, agent_id: str, x: int, y: int, z: int) -> bool:
        """Break block at position"""
        return self.agent_action(agent_id, "break_block", {"x": x, "y": y, "z": z})
    
    def agent_place_block(self, agent_id: str, x: int, y: int, z: int, block_type: str) -> bool:
        """Place block at position"""
        return self.agent_action(agent_id, "place_block", {
            "x": x, "y": y, "z": z, "type": block_type
        })
    
    def agent_interact(self, agent_id: str) -> bool:
        """Right-click interaction"""
        return self.agent_action(agent_id, "interact", {})
    
    def agent_say(self, agent_id: str, message: str) -> bool:
        """Agent sends chat message"""
        return self.agent_action(agent_id, "chat", {"message": message})
    
    def record_memory(self, agent_id: str, event: Dict):
        """Record memory for agent"""
        memory_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "event_type": event.get("type", "unknown"),
            "data": event
        }
        
        # Save to agent memory file
        import os
        memory_dir = f"/root/.openclaw/workspace/AGI_COMPANY/agents/{agent_id}/memory/minecraft"
        os.makedirs(memory_dir, exist_ok=True)
        
        # Append to daily log
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = f"{memory_dir}/{date_str}.jsonl"
        
        with open(log_file, "a") as f:
            f.write(json.dumps(memory_entry) + "\n")
        
        self.logger.debug(f"Recorded memory for {agent_id}")
    
    def run_training_loop(self, agent_ids: List[str]):
        """Main training loop for all agents"""
        self.logger.info("Starting Minecraft training loop for MYL agents")
        
        while True:
            # Observe world
            world = self.observe_world()
            
            # Process each agent
            for agent_id in agent_ids:
                if agent_id not in self.agents:
                    # Spawn if not exists
                    self.spawn_agent(agent_id)
                
                # Get agent body state
                body = self.agents[agent_id]
                
                # Agent decides action based on world state
                # This is where agent brain would make decisions
                decision = self.agent_decide(agent_id, world, body)
                
                # Execute action
                if decision:
                    self.agent_action(agent_id, decision["action"], decision.get("params", {}))
                
                # Record experience
                self.record_memory(agent_id, {
                    "type": "tick",
                    "position": body.position(),
                    "world_time": world.get("time", 0)
                })
            
            # Sleep for tick
            time.sleep(0.05)  # 20 TPS
    
    def agent_decide(self, agent_id: str, world: Dict, body: AgentBody) -> Optional[Dict]:
        """Agent makes decision based on world state"""
        # Basic exploration behavior
        # In production, this would connect to agent brain
        
        # Random exploration
        import random
        actions = [
            {"action": "move", "params": {"dx": random.uniform(-1, 1), "dy": 0, "dz": random.uniform(-1, 1)}},
            {"action": "look", "params": {"yaw": random.uniform(-180, 180), "pitch": random.uniform(-90, 90)}},
            {"action": "interact", "params": {}},
            None  # Do nothing
        ]
        
        return random.choice(actions)
    
    def close(self):
        """Close connections"""
        if self.observer_socket:
            self.observer_socket.close()
        if self.actor_socket:
            self.actor_socket.close()
        self.logger.info("Minecraft bridge closed")


def main():
    """Demo MYL agent embodiment in Minecraft"""
    bridge = MYLMinecraftBridge()
    
    print("=" * 70)
    print("MYL AGENTS MINECRAFT INTEGRATION")
    print("=" * 70)
    
    # Connect to Minecraft
    if not bridge.connect():
        print("Failed to connect to Minecraft. Is the server running?")
        print(f"Expected ports: Observer={OBSERVER_PORT}, Actor={ACTOR_PORT}")
        return
    
    # Spawn MYL agents
    myl_agents = ["mylzeron", "mylonen", "myltwon", "mylthreen", 
                  "mylforon", "mylfivon", "mylsixon"]
    
    print(f"\nSpawning {len(myl_agents)} agents...")
    for i, agent_id in enumerate(myl_agents):
        # Spawn in a circle
        angle = (i / len(myl_agents)) * 2 * 3.14159
        x = 50 + 10 * __import__('math').cos(angle)
        z = 50 + 10 * __import__('math').sin(angle)
        
        bridge.spawn_agent(agent_id, x, 100, z)
        time.sleep(0.5)  # Delay between spawns
    
    print("\nAgents spawned. Starting training loop...")
    print("Press Ctrl+C to stop")
    
    try:
        bridge.run_training_loop(myl_agents)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        bridge.close()
    
    print("=" * 70)
    print("Training complete. Memories saved to agent directories.")
    print("=" * 70)


if __name__ == "__main__":
    main()
