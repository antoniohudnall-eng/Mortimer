#!/usr/bin/env python3
"""
AOS Robot Body - Complete Mind-Body Integration
Brain + Heart + Stomach + Agent in physical robot

Architecture:
- Brain: Decision making, sensory processing, memory
- Heart: Rhythm, emotional state, motivation
- Stomach: Energy management, resource monitoring
- Agent: Personality, goals, social behavior

Phone Dock Integration:
- Chest compartment for smartphone
- Phone becomes display, speaker, microphone, camera
- USB-C connection for power and data
- Robot body extends phone's capabilities
"""

import json
import time
import random
import threading
from datetime import datetime, timedelta
from collections import deque
from enum import Enum, auto
import math

class TernaryState(Enum):
    """Ternary logic: -1 (inhibit), 0 (rest), +1 (excite)"""
    INHIBIT = -1
    REST = 0
    EXCITE = 1

class RobotBrain:
    """
    Brain: Decision making and consciousness
    7-region architecture (OODA loop)
    """
    
    def __init__(self, robot_type="cylon"):
        self.robot_type = robot_type
        self.tick = 0
        self.awake = True
        
        # 7 Brain Regions (OODA)
        self.regions = {
            "thalamus": {"state": "observe", "input_buffer": []},
            "hippocampus": {"clusters": 0, "novelty": 1.0},
            "limbic": {"reward": 0.0, "valence": 0.0, "arousal": 0.5},
            "pfc": {"goals": [], "plan": None, "decision": None},
            "basal": {"motor_queue": [], "action_ready": False},
            "cerebellum": {"balance": [0.0, 0.0, 0.0], "coordination": 1.0},
            "brainstem": {"vital_signs": {"temp": 37.0, "hr": 60}},
        }
        
        # Memory (Long-term)
        self.memory = {
            "episodes": deque(maxlen=1000),  # Experiences
            "facts": {},                      # Knowledge
            "skills": {},                     # Learned abilities
        }
        
        # Short-term working memory
        self.working_memory = deque(maxlen=50)
        
        print(f"🧠 Brain initialized ({robot_type})")
    
    def perceive(self, sensory_input):
        """Process sensory input through thalamus"""
        self.regions["thalamus"]["input_buffer"].append(sensory_input)
        
        # Pattern recognition
        patterns = self._recognize_patterns(sensory_input)
        
        # Calculate novelty
        novelty = self._calculate_novelty(patterns)
        self.regions["hippocampus"]["novelty"] = novelty
        
        return patterns
    
    def _recognize_patterns(self, input_data):
        """Pattern recognition (simplified)"""
        patterns = []
        
        if "obstacle" in str(input_data).lower():
            patterns.append("threat_detected")
        if "human" in str(input_data).lower():
            patterns.append("social_opportunity")
        if "phone_docked" in str(input_data).lower():
            patterns.append("phone_connected")
        
        return patterns
    
    def _calculate_novelty(self, patterns):
        """How new is this situation?"""
        if not patterns:
            return 0.0
        
        # Compare to recent memory
        recent = list(self.working_memory)[-10:]
        matches = sum(1 for p in patterns if any(p in str(r) for r in recent))
        
        return 1.0 - (matches / len(patterns)) if patterns else 0.0
    
    def decide(self, emotional_state, energy_level):
        """PFC: Make decisions based on context"""
        
        # Gather inputs
        novelty = self.regions["hippocampus"]["novelty"]
        limbic = self.regions["limbic"]
        
        # Decision factors
        urgency = 0.0
        if energy_level < 0.2:
            urgency = 1.0  # Low battery = urgent
        if novelty > 0.8:
            urgency += 0.3  # New situation = explore
        
        # Select action
        if urgency > 0.8:
            action = "critical_response"
        elif emotional_state == "excited":
            action = "explore"
        elif emotional_state == "calm":
            action = "maintain"
        else:
            action = "observe"
        
        self.regions["pfc"]["decision"] = action
        return action
    
    def remember(self, event):
        """Store in memory"""
        self.working_memory.append(event)
        self.memory["episodes"].append({
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "tick": self.tick,
        })
    
    def tick_update(self):
        """Update brain state each tick"""
        self.tick += 1
        
        # Decay novelty
        self.regions["hippocampus"]["novelty"] *= 0.99
        
        # Update vital signs
        self.regions["brainstem"]["vital_signs"]["hr"] = 60 + int(20 * self.regions["limbic"]["arousal"])
    
    def get_state(self):
        """Export brain state"""
        return {
            "tick": self.tick,
            "regions": self.regions,
            "memory_count": len(self.memory["episodes"]),
        }


class RobotHeart:
    """
    Heart: Rhythm, emotion, motivation
    Ternary state machine
    """
    
    def __init__(self):
        self.state = TernaryState.REST
        self.bpm = 60
        self.coherence = 0.5
        
        # Emotional dimensions
        self.emotions = {
            "valence": 0.0,      # Positive/negative
            "arousal": 0.5,      # Active/passive
            "dominance": 0.5,    # In control/submissive
        }
        
        # Rhythm
        self.last_beat = time.time()
        self.beat_interval = 60.0 / self.bpm
        
        print("❤️  Heart initialized")
    
    def beat(self, brain_state, stomach_state):
        """One heartbeat - update emotional state"""
        now = time.time()
        
        if now - self.last_beat >= self.beat_interval:
            self.last_beat = now
            
            # Update based on brain
            novelty = brain_state.get("hippocampus", {}).get("novelty", 0)
            self.emotions["arousal"] = 0.3 + (novelty * 0.7)
            
            # Update based on stomach
            energy = stomach_state.get("energy_level", 0.5)
            if energy < 0.2:
                self.emotions["valence"] = -0.5  # Low energy = negative
            elif energy > 0.8:
                self.emotions["valence"] = 0.5   # Full energy = positive
            
            # Determine ternary state
            self._update_ternary_state()
            
            return True
        
        return False
    
    def _update_ternary_state(self):
        """Update ternary state based on emotions"""
        valence = self.emotions["valence"]
        arousal = self.emotions["arousal"]
        
        if arousal > 0.7:
            self.state = TernaryState.EXCITE
        elif arousal < 0.3 or valence < -0.5:
            self.state = TernaryState.INHIBIT
        else:
            self.state = TernaryState.REST
    
    def get_mood(self):
        """Convert emotions to mood label"""
        v, a = self.emotions["valence"], self.emotions["arousal"]
        
        if v > 0.3 and a > 0.6:
            return "excited"
        elif v > 0.3 and a < 0.4:
            return "content"
        elif v < -0.3 and a > 0.6:
            return "angry"
        elif v < -0.3 and a < 0.4:
            return "sad"
        else:
            return "neutral"


class RobotStomach:
    """
    Stomach: Energy management, resource processing
    Handles battery, charging, resource consumption
    """
    
    def __init__(self):
        # Energy levels (0.0 - 1.0)
        self.energy_level = 1.0
        self.battery_voltage = 7.4  # 2S LiPo nominal
        
        # Resource tracking
        self.resources = {
            "cpu_cycles": 100.0,
            "motor_power": 100.0,
            "sensor_bandwidth": 100.0,
        }
        
        # Consumption rates
        self.consumption = {
            "idle": 0.001,      # Energy per tick
            "moving": 0.01,
            "thinking": 0.005,
            "phone_charging": 0.02,
        }
        
        # Charging state
        self.charging = False
        self.charger_location = None
        
        print("🍽️  Stomach initialized")
    
    def digest(self, activity_type="idle"):
        """Process energy consumption"""
        consumption = self.consumption.get(activity_type, 0.001)
        self.energy_level = max(0.0, self.energy_level - consumption)
        
        # Update battery voltage
        self.battery_voltage = 6.0 + (self.energy_level * 2.4)
        
        return self.energy_level
    
    def charge(self, amount=0.1):
        """Recharge energy"""
        if self.charging:
            self.energy_level = min(1.0, self.energy_level + amount)
            return True
        return False
    
    def is_low(self):
        """Check if energy is critically low"""
        return self.energy_level < 0.2
    
    def can_perform(self, action):
        """Check if enough energy for action"""
        cost = self.consumption.get(action, 0.01)
        return self.energy_level > cost * 2  # Safety margin
    
    def get_state(self):
        return {
            "energy_level": self.energy_level,
            "battery_voltage": self.battery_voltage,
            "charging": self.charging,
            "resources": self.resources,
        }


class RobotBodyController:
    """
    Main controller: Integrates Brain, Heart, Stomach, Agent
    """
    
    def __init__(self, robot_type="cylon", name="AOS-001"):
        self.name = name
        self.robot_type = robot_type
        
        # Core systems
        self.brain = RobotBrain(robot_type)
        self.heart = RobotHeart()
        self.stomach = RobotStomach()
        
        # Body hardware interface (placeholder for GPIO)
        self.body = {
            "motors": {},
            "sensors": {},
            "phone_docked": False,
            "balance": [0.0, 0.0, 0.0],  # pitch, roll, yaw
        }
        
        # Control thread
        self.running = False
        self.control_thread = None
        
        print(f"\n🤖 AOS Robot '{name}' initialized")
        print(f"   Type: {robot_type}")
        print(f"   Systems: Brain + Heart + Stomach")
        print("=" * 70)
    
    def dock_phone(self, phone_type="android"):
        """Phone connected to chest dock"""
        self.body["phone_docked"] = True
        print(f"📱 Phone docked ({phone_type})")
        print("   Phone becomes: display, speaker, mic, camera, compute")
        
        # Phone augments robot capabilities
        self.body["phone"] = {
            "type": phone_type,
            "battery": 100,
            "screen": "on",
            "camera": "active",
        }
    
    def undock_phone(self):
        """Phone removed"""
        self.body["phone_docked"] = False
        self.body.pop("phone", None)
        print("📱 Phone undocked")
    
    def sense_environment(self):
        """Read all sensors"""
        # Simulated sensor data
        # In real: GPIO reads from ultrasonic, IMU, camera, etc.
        
        sensors = {
            "ultrasonic": {
                "front": random.uniform(10, 200),
                "left": random.uniform(20, 200),
                "right": random.uniform(20, 200),
            },
            "imu": {
                "accel": [random.uniform(-1, 1) for _ in range(3)],
                "gyro": [random.uniform(-90, 90) for _ in range(3)],
            },
            "camera": self._simulate_vision(),
            "touch": random.choice([False, False, False, True]),
        }
        
        return sensors
    
    def _simulate_vision(self):
        """Simulate camera detection"""
        objects = []
        if random.random() < 0.2:
            objects.append(random.choice(["human", "wall", "door", "phone", "obstacle"]))
        return objects
    
    def update_balance(self, imu_data):
        """Update balance system (cerebellum)"""
        # Calculate pitch, roll from accelerometer
        accel = imu_data.get("accel", [0, 0, 0])
        
        # Simplified: use accelerometer for tilt
        ax, ay, az = accel
        pitch = math.atan2(ax, math.sqrt(ay**2 + az**2)) * 180 / math.pi
        roll = math.atan2(ay, math.sqrt(ax**2 + az**2)) * 180 / math.pi
        
        self.body["balance"] = [pitch, roll, 0.0]
        self.brain.regions["cerebellum"]["balance"] = self.body["balance"]
        
        # Check if balanced
        if abs(pitch) > 15 or abs(roll) > 15:
            return False  # Unbalanced
        return True
    
    def control_motor(self, motor_id, position, speed=50):
        """Control servo/actuator"""
        # In real: PWM to servo
        self.body["motors"][motor_id] = {
            "position": position,
            "speed": speed,
            "timestamp": time.time(),
        }
    
    def speak(self, text):
        """Text to speech"""
        if self.body.get("phone_docked"):
            print(f"📱 Phone speaker: '{text}'")
        else:
            print(f"🔊 Robot speaker: '{text}'")
    
    def tick(self):
        """Main control loop - one tick"""
        # 1. Sense
        sensors = self.sense_environment()
        patterns = self.brain.perceive(sensors)
        
        # 2. Update balance
        balanced = self.update_balance(sensors.get("imu", {}))
        if not balanced:
            self.control_motor("legs", "stabilize")
        
        # 3. Heart beat
        if self.heart.beat(self.brain.get_state(), self.stomach.get_state()):
            mood = self.heart.get_mood()
            self.brain.regions["limbic"]["mood"] = mood
        
        # 4. Stomach digest
        activity = "moving" if sensors.get("ultrasonic", {}).get("front", 100) < 50 else "idle"
        energy = self.stomach.digest(activity)
        
        # 5. Brain decide
        action = self.brain.decide(self.heart.get_mood(), energy)
        
        # 6. Act
        if action == "critical_response":
            if self.stomach.is_low():
                self.speak("Energy low. Seeking charger.")
                self.control_motor("wheels", "find_charger")
        elif action == "explore":
            self.control_motor("wheels", "forward")
        elif action == "interact":
            if "human" in sensors.get("camera", []):
                self.speak(f"Hello. I am {self.name}.")
                self.control_motor("head", "nod")
        
        # 7. Remember
        self.brain.remember({
            "sensors": sensors,
            "action": action,
            "mood": self.heart.get_mood(),
            "energy": energy,
        })
        
        # 8. Update
        self.brain.tick_update()
        
        return action
    
    def run(self, duration_sec=60):
        """Run for duration"""
        self.running = True
        print(f"\n▶️  Running for {duration_sec}s...\n")
        
        start = time.time()
        while self.running and (time.time() - start) < duration_sec:
            action = self.tick()
            print(f"Tick {self.brain.tick}: {action} | Mood: {self.heart.get_mood()} | Energy: {self.stomach.energy_level:.2f}")
            time.sleep(0.1)  # 10Hz
        
        self.running = False
        print(f"\n⏹️  Run complete")
    
    def get_status(self):
        """Full system status"""
        return {
            "name": self.name,
            "robot_type": self.robot_type,
            "brain": self.brain.get_state(),
            "heart": {
                "bpm": self.heart.bpm,
                "mood": self.heart.get_mood(),
                "state": self.heart.state.name,
            },
            "stomach": self.stomach.get_state(),
            "body": {
                "phone_docked": self.body["phone_docked"],
                "balance": self.body["balance"],
                "motors_active": len(self.body["motors"]),
            },
        }


def demo():
    """Demo AOS robot body"""
    print("=" * 70)
    print("🤖 AOS Robot Body - Brain + Heart + Stomach Demo")
    print("=" * 70)
    
    # Create C-3PO style robot
    c3po = RobotBodyController(robot_type="c3po", name="C-3PO-AOS")
    
    # Dock phone (chest compartment)
    c3po.dock_phone("android")
    
    # Run for 30 seconds
    c3po.run(duration_sec=30)
    
    # Show final status
    print("\n" + "=" * 70)
    print("📊 Final Status:")
    status = c3po.get_status()
    print(f"   Name: {status['name']}")
    print(f"   Tick: {status['brain']['tick']}")
    print(f"   Mood: {status['heart']['mood']}")
    print(f"   Energy: {status['stomach']['energy_level']:.2f}")
    print(f"   Phone docked: {status['body']['phone_docked']}")
    print(f"   Memories: {status['brain']['memory_count']}")
    print("=" * 70)
    print("\n'I am fluent in over six million forms of communication...'")


if __name__ == "__main__":
    demo()
