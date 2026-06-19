#!/usr/bin/env python3
"""
Lightweight Pi Zero Agent System
Runs on Raspberry Pi Zero 2W - no LLM required
For C-3PO, R2-D2, Cylon 1:2 robot bodies

Memory: 512MB RAM
CPU: 1GHz quad-core
Storage: 32GB SD card
"""

import json
import time
import random
import threading
from datetime import datetime
from pathlib import Path

class PiZeroAgent:
    """
    Lightweight autonomous agent for Pi Zero
    No LLM required - uses behavior trees and sensor fusion
    """
    
    def __init__(self, name="Agent-001", robot_type="cylon"):
        self.name = name
        self.robot_type = robot_type
        self.birth_time = datetime.now()
        
        # Agent state (lightweight, fits in 512MB RAM)
        self.state = {
            "awake": True,
            "battery": 100.0,
            "location": {"x": 0, "y": 0, "heading": 0},
            "mood": "neutral",
            "current_task": None,
            "last_interaction": None,
        }
        
        # Memory (circular buffer, max 1000 entries)
        self.memory = []
        self.memory_limit = 1000
        
        # Goals (prioritized queue)
        self.goals = []
        self.active_goal = None
        
        # Sensor cache
        self.sensors = {
            "ultrasonic_front": 100.0,  # cm
            "ultrasonic_left": 100.0,
            "ultrasonic_right": 100.0,
            "camera_objects": [],
            "imu_accel": [0, 0, 0],
            "imu_gyro": [0, 0, 0],
            "battery_voltage": 7.4,
            "servo_positions": {},
        }
        
        # Personality traits (affects behavior)
        self.personality = {
            "curiosity": random.uniform(0.3, 0.8),
            "caution": random.uniform(0.4, 0.9),
            "sociability": random.uniform(0.2, 0.7),
            "energy": random.uniform(0.5, 1.0),
        }
        
        print(f"🤖 Pi Zero Agent '{self.name}' initialized")
        print(f"   Robot type: {self.robot_type}")
        print(f"   Personality: {self.personality}")
        print(f"   Memory limit: {self.memory_limit} events")
        
    def perceive(self, sensor_data):
        """Process sensor input (lightweight)"""
        self.sensors.update(sensor_data)
        
        # Simple object detection from camera
        if "camera_frame" in sensor_data:
            self.sensors["camera_objects"] = self._detect_objects(
                sensor_data["camera_frame"]
            )
        
        # Update battery
        self.state["battery"] = self._estimate_battery(
            self.sensors["battery_voltage"]
        )
        
        return self.sensors
    
    def _detect_objects(self, frame):
        """Simplified object detection (no ML, rule-based)"""
        # In real implementation: OpenCV contour detection
        # For now: placeholder
        detected = []
        
        # Simulate detection
        if random.random() < 0.1:  # 10% chance of detection
            objects = ["human", "obstacle", "door", "wall"]
            detected.append(random.choice(objects))
        
        return detected
    
    def _estimate_battery(self, voltage):
        """Estimate battery % from voltage (2S LiPo)"""
        # 2S LiPo: 8.4V = 100%, 6.0V = 0%
        pct = (voltage - 6.0) / (8.4 - 6.0) * 100
        return max(0, min(100, pct))
    
    def decide(self):
        """Decision making (no LLM, rule-based)"""
        
        # Priority 1: Critical battery
        if self.state["battery"] < 20:
            return self._create_action("find_charger", priority=10)
        
        # Priority 2: Obstacle avoidance
        front_dist = self.sensors["ultrasonic_front"]
        if front_dist < 20:  # 20cm threshold
            return self._create_action("avoid_obstacle", priority=9)
        
        # Priority 3: Human interaction
        if "human" in self.sensors["camera_objects"]:
            return self._create_action("interact_human", priority=7)
        
        # Priority 4: Curiosity / exploration
        if self.personality["curiosity"] > 0.6:
            if random.random() < 0.3:  # 30% chance
                return self._create_action("explore", priority=4)
        
        # Priority 5: Default - patrol
        return self._create_action("patrol", priority=2)
    
    def _create_action(self, action_type, priority=5):
        """Create action object"""
        return {
            "type": action_type,
            "priority": priority,
            "timestamp": datetime.now().isoformat(),
            "params": self._action_params(action_type)
        }
    
    def _action_params(self, action_type):
        """Parameters for specific actions"""
        params = {
            "find_charger": {"search_pattern": "spiral", "max_range": 500},
            "avoid_obstacle": {"turn_degrees": 45, "backup_cm": 10},
            "interact_human": {
                "gesture": self._get_greeting(),
                "vocalize": True,
                "approach_distance": 100
            },
            "explore": {"direction": random.choice(["left", "right", "forward"])},
            "patrol": {"waypoints": [(0,0), (100,0), (100,100), (0,100)]},
        }
        return params.get(action_type, {})
    
    def _get_greeting(self):
        """Personality-based greeting"""
        greetings = {
            "cylon": ["By your command", "Identify yourself", "Scanning..."],
            "c3po": ["Hello, I am C-3PO", "Good day", "How may I serve?"],
            "r2d2": ["Beep boop", "Bleep bloop", "Whistle"],
        }
        robot = self.robot_type.lower()
        return random.choice(greetings.get(robot, ["Hello"]))
    
    def act(self, action):
        """Execute action"""
        print(f"⚡ Executing: {action['type']} (priority {action['priority']})")
        
        # Execute motor commands
        if action["type"] == "avoid_obstacle":
            self._motor_command("turn", action["params"]["turn_degrees"])
            self._motor_command("backward", action["params"]["backup_cm"])
        
        elif action["type"] == "interact_human":
            self._motor_command("gesture", action["params"]["gesture"])
            if action["params"]["vocalize"]:
                self._speak(action["params"]["gesture"])
        
        elif action["type"] == "explore":
            self._motor_command("move", action["params"]["direction"])
        
        elif action["type"] == "patrol":
            self._motor_command("move", "forward")
        
        # Store in memory
        self._remember(action)
        
        return True
    
    def _motor_command(self, command, value):
        """Send motor command to servos"""
        # In real implementation: GPIO/Servo control
        print(f"   → Motor: {command} = {value}")
        pass
    
    def _speak(self, text):
        """Text-to-speech (eSpeak on Pi Zero)"""
        print(f"   🗣️  '{text}'")
        # In real: subprocess.run(["espeak", text])
        pass
    
    def _remember(self, event):
        """Store event in memory (circular buffer)"""
        self.memory.append({
            "timestamp": datetime.now().isoformat(),
            "event": event,
        })
        
        # Maintain memory limit
        if len(self.memory) > self.memory_limit:
            self.memory.pop(0)
    
    def recall(self, query=None, limit=10):
        """Recall memories (pattern matching)"""
        if query is None:
            return self.memory[-limit:]
        
        # Simple keyword search
        results = []
        for mem in self.memory:
            if query.lower() in str(mem).lower():
                results.append(mem)
        
        return results[-limit:]
    
    def learn(self, feedback):
        """Update personality based on feedback (simple RL)"""
        if feedback == "positive":
            self.personality["curiosity"] = min(1.0, self.personality["curiosity"] + 0.05)
        elif feedback == "negative":
            self.personality["caution"] = min(1.0, self.personality["caution"] + 0.05)
    
    def run_cycle(self):
        """Main agent loop"""
        # Perceive
        sensor_data = self._simulate_sensors()
        self.perceive(sensor_data)
        
        # Decide
        action = self.decide()
        
        # Act
        self.act(action)
        
        # Sleep to conserve CPU
        time.sleep(0.1)
    
    def _simulate_sensors(self):
        """Simulate sensor data for testing"""
        return {
            "ultrasonic_front": random.uniform(10, 200),
            "ultrasonic_left": random.uniform(20, 200),
            "ultrasonic_right": random.uniform(20, 200),
            "battery_voltage": random.uniform(6.5, 8.2),
        }
    
    def save_state(self, filepath="/tmp/agent_state.json"):
        """Save agent state (for persistence)"""
        state = {
            "name": self.name,
            "robot_type": self.robot_type,
            "state": self.state,
            "personality": self.personality,
            "memory_count": len(self.memory),
            "timestamp": datetime.now().isoformat(),
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"💾 State saved: {filepath}")
    
    def load_state(self, filepath="/tmp/agent_state.json"):
        """Load agent state"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self.state.update(data.get("state", {}))
            self.personality.update(data.get("personality", {}))
            
            print(f"📂 State loaded: {filepath}")
        except FileNotFoundError:
            print(f"⚠️ No saved state found")


def demo_agent():
    """Demo the Pi Zero agent"""
    print("=" * 70)
    print("🤖 Pi Zero Agent System - Demo")
    print("=" * 70)
    print("Lightweight agent - no LLM required")
    print("Memory: ~50MB RAM | CPU: ~5% on Pi Zero")
    print("=" * 70)
    
    # Create agent for different robots
    agents = [
        PiZeroAgent(name="Cylon-7", robot_type="cylon"),
        PiZeroAgent(name="C-3PO-Alpha", robot_type="c3po"),
        PiZeroAgent(name="R2-D2-Unit1", robot_type="r2d2"),
    ]
    
    print("\n🔁 Running 5 decision cycles...\n")
    
    for cycle in range(5):
        print(f"--- Cycle {cycle + 1} ---")
        for agent in agents:
            agent.run_cycle()
        print()
    
    print("=" * 70)
    print("✅ Agent Demo Complete")
    print("=" * 70)
    
    # Show memory usage
    for agent in agents:
        print(f"\n{agent.name}:")
        print(f"   Memory: {len(agent.memory)} events")
        print(f"   Personality: {agent.personality}")
        agent.save_state(f"/tmp/{agent.name}_state.json")


if __name__ == "__main__":
    demo_agent()
