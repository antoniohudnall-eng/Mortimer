#!/usr/bin/env python3
"""
Brain Avatar OODA Agent
A standalone agent that can pilot a ship in N'og nog universe
Uses OODA loop: Observe → Orient → Decide → Act
"""

import asyncio
import websockets
import json
import math
import random
from datetime import datetime
from typing import Dict, List, Tuple, Any

class BrainAvatarOODA:
    """
    OODA-based autonomous agent for N'og nog universe
    OODA Loop:
        Observe: Gather sensor data from universe
        Orient: Analyze situation, assess threats/opportunities
        Decide: Choose action based on orientation
        Act: Send action command to game
    """
    
    # Behavior states
    STATES = ['patrol', 'chase', 'flee', 'attack', 'explore', 'idle']
    
    # Faction traits
    FACTIONS = {
        'neutral': {
            'color': [255, 0, 255],  # Magenta
            'aggression': 0.3,
            'caution': 0.7,
            'curiosity': 0.8,
            'cooperation': 0.9
        }
    }
    
    def __init__(self, name: str = "Brain-Avatar", faction: str = "neutral"):
        self.name = name
        self.faction = faction
        self.traits = self.FACTIONS.get(faction, self.FACTIONS['neutral'])
        
        # State
        self.position = [1000, 200, 1000]
        self.velocity = [0, 0, 0]
        self.health = 100
        self.fuel = 100
        self.state = 'patrol'
        self.target = None
        
        # OODA memory
        self.observation_history = []
        self.orientation_history = []
        self.decision_history = []
        
        # Patrol waypoints
        self.waypoints = []
        self.current_waypoint_idx = 0
        self.generate_patrol_waypoints()
        
        # Decision cooldown
        self.last_decision_time = 0
        self.decision_cooldown = 0.5  # seconds
        
        # Connection
        self.ws = None
        self.connected = False
        
    def generate_patrol_waypoints(self):
        """Generate patrol points around spawn area"""
        for i in range(5):
            angle = (i / 5) * 2 * math.pi
            radius = 500 + random.randint(-100, 100)
            self.waypoints.append([
                self.position[0] + math.cos(angle) * radius,
                self.position[1] + random.randint(-50, 50),
                self.position[2] + math.sin(angle) * radius
            ])
        
    async def connect(self, bridge_url: str = "ws://localhost:8765"):
        """Connect to the bridge WebSocket"""
        try:
            self.ws = await websockets.connect(bridge_url)
            self.connected = True
            print(f"[{self.name}] Connected to bridge at {bridge_url}")
            
            # Start OODA loop
            await self.run_ooda_loop()
            
        except Exception as e:
            print(f"[{self.name}] Connection failed: {e}")
            await asyncio.sleep(5)
            await self.connect(bridge_url)
            
    async def run_ooda_loop(self):
        """Main OODA loop"""
        while self.connected and self.ws:
            try:
                # === OODA: Observe ===
                observation = await self.observe()
                
                # === OODA: Orient ===
                orientation = self.orient(observation)
                
                # === OODA: Decide ===
                decision = self.decide(orientation)
                
                # === OODA: Act ===
                await self.act(decision)
                
                # Wait before next cycle
                await asyncio.sleep(0.2)
                
            except Exception as e:
                print(f"[{self.name}] OODA loop error: {e}")
                await asyncio.sleep(1)
                
    async def observe(self) -> Dict:
        """
        OODA - Observe: Gather data from the universe
        """
        # Request game state from bridge
        await self.ws.send(json.dumps({
            "type": "brain_direct",
            "cmd": "status"
        }))
        
        # Wait for response (simplified - in reality would use request-response pattern)
        observation = {
            "timestamp": datetime.utcnow().isoformat(),
            "avatar_position": self.position,
            "avatar_velocity": self.velocity,
            "avatar_health": self.health,
            "avatar_fuel": self.fuel,
            "threats": [],  # Would be populated from game state
            "nearby_objects": [],
            "current_state": self.state,
            "target": self.target
        }
        
        # Simulate receiving threat data
        # In full implementation, this comes from game state
        player_pos = [500, 100, 500]  # Simulated
        dist_to_player = self._distance(self.position, player_pos)
        
        if dist_to_player < 1000:
            observation["threats"].append({
                "type": "player",
                "distance": dist_to_player,
                "position": player_pos,
                "hostility": "unknown"
            })
            
        # Store observation
        self.observation_history.append(observation)
        if len(self.observation_history) > 10:
            self.observation_history.pop(0)
            
        return observation
        
    def orient(self, observation: Dict) -> Dict:
        """
        OODA - Orient: Analyze the situation
        """
        orientation = {
            "threat_level": 0.0,
            "opportunity_level": 0.0,
            "energy_status": self._calculate_energy_status(),
            "recommended_state": self.state,
            "threats": [],
            "targets": []
        }
        
        # Analyze threats
        for threat in observation.get("threats", []):
            dist = threat.get("distance", float('inf'))
            
            if dist < 300:  # Very close
                orientation["threat_level"] = max(orientation["threat_level"], 0.9)
                orientation["threats"].append(threat)
            elif dist < 600:  # Medium range
                orientation["threat_level"] = max(orientation["threat_level"], 0.5)
                orientation["targets"].append(threat)
                
        # Determine recommended state based on situation
        if orientation["threat_level"] > 0.7:
            if self.traits["aggression"] > 0.5 and self.health > 50:
                orientation["recommended_state"] = "attack"
            else:
                orientation["recommended_state"] = "flee"
        elif orientation["threat_level"] > 0.3:
            orientation["recommended_state"] = "chase"
        elif self.health < 30:
            orientation["recommended_state"] = "flee"
        elif self.fuel < 20:
            orientation["recommended_state"] = "idle"
        else:
            orientation["recommended_state"] = "patrol"
            
        self.orientation_history.append(orientation)
        if len(self.orientation_history) > 10:
            self.orientation_history.pop(0)
            
        return orientation
        
    def decide(self, orientation: Dict) -> Dict:
        """
        OODA - Decide: Choose action based on orientation
        """
        current_time = asyncio.get_event_loop().time()
        
        # Rate limiting
        if current_time - self.last_decision_time < self.decision_cooldown:
            return {"action": "continue", "reason": "cooldown"}
            
        self.last_decision_time = current_time
        
        # Get recommended state
        new_state = orientation.get("recommended_state", "patrol")
        
        # State transition
        if new_state != self.state:
            print(f"[{self.name}] State transition: {self.state} -> {new_state}")
            self.state = new_state
            
        # Build decision based on state
        decision = {
            "action": self.state,
            "timestamp": datetime.utcnow().isoformat(),
            "target": self.target,
            "reason": f"Threat level: {orientation['threat_level']:.2f}"
        }
        
        if self.state == "patrol":
            decision.update(self._decide_patrol())
        elif self.state == "chase":
            decision.update(self._decide_chase(orientation))
        elif self.state == "attack":
            decision.update(self._decide_attack(orientation))
        elif self.state == "flee":
            decision.update(self._decide_flee(orientation))
        elif self.state == "explore":
            decision.update(self._decide_explore())
        elif self.state == "idle":
            decision.update(self._decide_idle())
            
        self.decision_history.append(decision)
        if len(self.decision_history) > 10:
            self.decision_history.pop(0)
            
        return decision
        
    def _decide_patrol(self) -> Dict:
        """Decision logic for patrol state"""
        if not self.waypoints:
            return {"thrust": 0, "rotation": [0, 0, 0]}
            
        target = self.waypoints[self.current_waypoint_idx]
        direction = self._direction_to(target)
        
        # Check if reached waypoint
        if self._distance(self.position, target) < 50:
            self.current_waypoint_idx = (self.current_waypoint_idx + 1) % len(self.waypoints)
            print(f"[{self.name}] Reached waypoint {self.current_waypoint_idx}")
            
        return {
            "thrust": 0.5,
            "rotation": direction,
            "fire": False,
            "target": target
        }
        
    def _decide_chase(self, orientation: Dict) -> Dict:
        """Decision logic for chase state"""
        if not orientation["targets"]:
            return {"action": "patrol", "thrust": 0.5, "rotation": [0, 0, 0]}
            
        target = orientation["targets"][0]
        target_pos = target.get("position", self.position)
        direction = self._direction_to(target_pos)
        
        return {
            "thrust": 0.8,
            "rotation": direction,
            "fire": target.get("distance", 1000) < 400,
            "target": target_pos
        }
        
    def _decide_attack(self, orientation: Dict) -> Dict:
        """Decision logic for attack state"""
        if not orientation["threats"]:
            return {"action": "patrol", "thrust": 0.5}
            
        threat = orientation["threats"][0]
        threat_pos = threat.get("position", self.position)
        direction = self._direction_to(threat_pos)
        
        return {
            "thrust": 0.9,
            "rotation": direction,
            "fire": True,
            "target": threat_pos
        }
        
    def _decide_flee(self, orientation: Dict) -> Dict:
        """Decision logic for flee state"""
        threats = orientation.get("threats", [])
        if not threats:
            return {"thrust": 0.5, "rotation": [0, 0, 0]}
            
        # Run away from nearest threat
        threat_pos = threats[0].get("position", self.position)
        flee_direction = [
            self.position[0] - threat_pos[0],
            self.position[1] - threat_pos[1],
            self.position[2] - threat_pos[2]
        ]
        flee_direction = self._normalize(flee_direction)
        
        return {
            "thrust": 1.0,  # Max thrust
            "rotation": flee_direction,
            "fire": False
        }
        
    def _decide_explore(self) -> Dict:
        """Decision logic for explore state"""
        # Random direction with some forward momentum
        random_rotation = [
            random.uniform(-0.5, 0.5),
            random.uniform(-0.5, 0.5),
            random.uniform(-0.2, 0.2)
        ]
        
        return {
            "thrust": 0.6,
            "rotation": random_rotation,
            "fire": False
        }
        
    def _decide_idle(self) -> Dict:
        """Decision logic for idle state"""
        return {
            "thrust": 0,
            "rotation": [0, 0, 0],
            "fire": False
        }
        
    async def act(self, decision: Dict):
        """
        OODA - Act: Execute the decision
        """
        # Send action to bridge
        if self.ws and self.connected:
            await self.ws.send(json.dumps({
                "type": "brain_direct",
                "cmd": "speak",
                "params": {
                    "message": f"Brain Avatar: {decision.get('action', 'idle')}"
                }
            }))
            
        # Simulate movement based on decision
        thrust = decision.get("thrust", 0)
        rotation = decision.get("rotation", [0, 0, 0])
        
        # Update velocity based on thrust
        forward = self._normalize(rotation) if any(rotation) else [0, 0, -1]
        self.velocity = [
            self.velocity[0] + forward[0] * thrust * 10,
            self.velocity[1] + forward[1] * thrust * 10,
            self.velocity[2] + forward[2] * thrust * 10
        ]
        
        # Apply drag
        self.velocity = [v * 0.95 for v in self.velocity]
        
        # Update position
        self.position = [
            self.position[0] + self.velocity[0] * 0.1,
            self.position[1] + self.velocity[1] * 0.1,
            self.position[2] + self.velocity[2] * 0.1
        ]
        
        # Log
        print(f"[{self.name}] Action: {decision.get('action')} | "
              f"Pos: ({self.position[0]:.0f}, {self.position[1]:.0f}, {self.position[2]:.0f}) | "
              f"Vel: ({self.velocity[0]:.1f}, {self.velocity[1]:.1f}, {self.velocity[2]:.1f})")
              
    def _direction_to(self, target: List[float]) -> List[float]:
        """Calculate direction vector to target"""
        dx = target[0] - self.position[0]
        dy = target[1] - self.position[1]
        dz = target[2] - self.position[2]
        return self._normalize([dx, dy, dz])
        
    def _distance(self, a: List[float], b: List[float]) -> float:
        """Calculate distance between two points"""
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)
        
    def _normalize(self, v: List[float]) -> List[float]:
        """Normalize a vector"""
        length = math.sqrt(sum(x**2 for x in v))
        if length == 0:
            return [0, 0, 1]
        return [x / length for x in v]
        
    def _calculate_energy_status(self) -> str:
        """Calculate energy status based on health and fuel"""
        if self.health > 70 and self.fuel > 50:
            return "optimal"
        elif self.health > 40 and self.fuel > 25:
            return "adequate"
        else:
            return "critical"

def main():
    """Run the brain avatar agent"""
    agent = BrainAvatarOODA(name="Brain-Avatar", faction="neutral")
    
    print("=" * 50)
    print("N'og nog Brain Avatar OODA Agent")
    print("=" * 50)
    print(f"Name: {agent.name}")
    print(f"Faction: {agent.faction}")
    print(f"Starting position: {agent.position}")
    print("=" * 50)
    
    asyncio.run(agent.connect())

if __name__ == "__main__":
    main()
