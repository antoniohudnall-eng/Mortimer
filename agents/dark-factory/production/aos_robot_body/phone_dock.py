#!/usr/bin/env python3
"""
Phone Dock Integration System
Chest-mounted phone becomes robot's display, speaker, camera, compute

Connection: USB-C or Wireless (ADB/TCP)
Phone runs companion app that communicates with Pi Zero
"""

import json
import subprocess
import time
import random
from enum import Enum

class PhoneConnection(Enum):
    USB = "usb"
    WIRELESS = "wireless"
    BLUETOOTH = "bluetooth"
    NONE = "none"

class PhoneDock:
    """
    Chest-mounted phone integration
    
    Hardware:
    - Chest cavity: 160mm x 80mm x 12mm (fits most phones)
    - USB-C dock connector with power passthrough
    - Qi wireless charging coil (optional)
    - Camera window aligned with phone camera
    - Speaker acoustic channels
    
    Software:
    - ADB over USB for control
    - Custom Android app or web interface
    - Communication protocol: JSON over TCP
    """
    
    def __init__(self, connection_type=PhoneConnection.USB):
        self.connection = connection_type
        self.phone = None
        self.docked = False
        
        # Phone capabilities
        self.capabilities = {
            "display": False,
            "camera": False,
            "speaker": False,
            "microphone": False,
            "internet": False,
            "touch": False,
        }
        
        # Status
        self.battery = 0
        self.screen_on = False
        self.camera_active = False
        
        print("📱 Phone Dock initialized")
    
    def dock_phone(self, device_id=None):
        """
        Detect and connect to docked phone
        
        In real implementation:
        - Detect USB connection via udev rules
        - Establish ADB connection
        - Launch companion app if not running
        """
        self.docked = True
        
        # Detect phone (simulated)
        if device_id:
            self.phone = {
                "id": device_id,
                "model": "Android Device",
                "os_version": "13+",
            }
        else:
            # Try to detect via ADB
            result = self._run_adb("devices")
            if "device" in result:
                self.phone = {
                    "id": "auto-detected",
                    "model": "Detected Phone",
                    "os_version": "unknown",
                }
        
        if self.phone:
            self.capabilities = {
                "display": True,
                "camera": True,
                "speaker": True,
                "microphone": True,
                "internet": True,
                "touch": True,
            }
            print(f"📱 Phone docked: {self.phone['model']}")
            self._launch_companion_app()
            return True
        
        print("⚠️ No phone detected")
        return False
    
    def undock(self):
        """Phone removed"""
        self.docked = False
        self.phone = None
        self.capabilities = {k: False for k in self.capabilities}
        print("📱 Phone undocked")
    
    def _run_adb(self, command):
        """Run ADB command (in real: subprocess)"""
        # Placeholder - real implementation would use subprocess
        return f"adb {command}: simulated"
    
    def _launch_companion_app(self):
        """Launch AOS Robot app on phone"""
        print("   Launching AOS Robot app...")
        # In real: adb shell am start -n com.agi.robot/.MainActivity
    
    # === Display Functions ===
    
    def set_face(self, expression):
        """
        Set facial expression on phone screen
        
        Expressions:
        - neutral, happy, sad, angry, surprised, thinking
        - cylon_scan (red eye sweep)
        - r2_beeps (animated droid face)
        """
        if not self.capabilities["display"]:
            return False
        
        print(f"   📱 Display: {expression}")
        
        # In real: Send to phone app via TCP/WebSocket
        message = {
            "type": "face",
            "expression": expression,
            "timestamp": time.time(),
        }
        self._send_to_phone(message)
        
        return True
    
    def show_text(self, text, duration=3.0):
        """Display text on phone screen"""
        if not self.capabilities["display"]:
            return False
        
        print(f"   📱 Display text: '{text}'")
        
        message = {
            "type": "text",
            "content": text,
            "duration": duration,
        }
        self._send_to_phone(message)
        
        return True
    
    def show_status(self, robot_status):
        """Show robot status dashboard on phone"""
        if not self.capabilities["display"]:
            return False
        
        message = {
            "type": "status",
            "battery": robot_status.get("battery", 0),
            "mood": robot_status.get("mood", "neutral"),
            "activity": robot_status.get("activity", "idle"),
        }
        self._send_to_phone(message)
        
        return True
    
    # === Camera Functions ===
    
    def capture_image(self):
        """Capture photo from phone camera"""
        if not self.capabilities["camera"]:
            return None
        
        print("   📸 Capturing image...")
        
        # In real: Trigger camera capture, return image data
        message = {
            "type": "camera_capture",
            "mode": "single",
        }
        self._send_to_phone(message)
        
        # Simulated return
        return {"width": 1920, "height": 1080, "objects": []}
    
    def start_video_stream(self, callback=None):
        """Start continuous video stream"""
        if not self.capabilities["camera"]:
            return False
        
        print("   🎥 Video stream started")
        self.camera_active = True
        
        message = {
            "type": "camera_stream",
            "action": "start",
        }
        self._send_to_phone(message)
        
        return True
    
    def stop_video_stream(self):
        """Stop video stream"""
        if not self.capabilities["camera"]:
            return False
        
        print("   🎥 Video stream stopped")
        self.camera_active = False
        
        message = {
            "type": "camera_stream",
            "action": "stop",
        }
        self._send_to_phone(message)
        
        return True
    
    def detect_objects(self, image):
        """
        Object detection using phone's ML (if available)
        
        Runs TensorFlow Lite on phone for:
        - Person detection
        - Face detection
        - Object classification
        """
        if not self.capabilities["camera"]:
            return []
        
        # In real: Run TFLite model on phone
        # Returns: [{"class": "person", "confidence": 0.95, "bbox": [x,y,w,h]}]
        
        return []
    
    # === Audio Functions ===
    
    def speak(self, text, emotion="neutral"):
        """
        Text-to-speech using phone speaker
        
        Uses phone's TTS engine with emotion modification
        """
        if not self.capabilities["speaker"]:
            return False
        
        print(f"   🔊 Speaking: '{text}' ({emotion})")
        
        message = {
            "type": "tts",
            "text": text,
            "emotion": emotion,
            "pitch": 1.0,
            "speed": 1.0,
        }
        self._send_to_phone(message)
        
        return True
    
    def play_sound(self, sound_id):
        """Play sound effect"""
        sounds = {
            "startup": "boot_sound.mp3",
            "beep": "beep.mp3",
            "scan": "scan.mp3",
            "cylon": "cylon_scan.mp3",
            "r2": "r2_beep.mp3",
        }
        
        if sound_id in sounds and self.capabilities["speaker"]:
            print(f"   🔊 Playing: {sounds[sound_id]}")
            return True
        
        return False
    
    def listen(self, duration=5.0):
        """
        Speech recognition using phone microphone
        
        Returns: transcribed text
        """
        if not self.capabilities["microphone"]:
            return None
        
        print(f"   🎤 Listening for {duration}s...")
        
        message = {
            "type": "listen",
            "duration": duration,
        }
        self._send_to_phone(message)
        
        # Simulated return
        return "hello robot"
    
    # === Communication ===
    
    def _send_to_phone(self, message):
        """Send message to phone companion app"""
        # In real: TCP socket or WebSocket to phone app
        # Port: 8765 (example)
        
        json_msg = json.dumps(message)
        # socket.send(json_msg.encode())
        
        pass
    
    def receive_from_phone(self):
        """Receive messages from phone"""
        # Touch events, sensor data, commands
        
        return None
    
    # === Power Management ===
    
    def get_phone_battery(self):
        """Get phone battery level"""
        if not self.docked:
            return 0
        
        # In real: adb shell dumpsys battery
        return random.randint(20, 100)  # Simulated
    
    def charge_phone(self, enable=True):
        """Enable/disable phone charging from robot battery"""
        # In real: Control USB-C power delivery
        
        if enable:
            print("   ⚡ Phone charging enabled")
        else:
            print("   ⚡ Phone charging disabled")
    
    def get_status(self):
        """Full phone dock status"""
        return {
            "docked": self.docked,
            "connection": self.connection.value,
            "phone": self.phone,
            "capabilities": self.capabilities,
            "battery": self.get_phone_battery(),
            "screen_on": self.screen_on,
            "camera_active": self.camera_active,
        }


def demo_phone_dock():
    """Demo phone dock functionality"""
    print("=" * 70)
    print("📱 Phone Dock System Demo")
    print("=" * 70)
    
    dock = PhoneDock(connection_type=PhoneConnection.USB)
    
    # Simulate docking
    print("\n📲 User docks phone...")
    dock.dock_phone(device_id="ABC123")
    
    print("\n🎭 Setting expressions...")
    dock.set_face("neutral")
    time.sleep(1)
    dock.set_face("happy")
    time.sleep(1)
    dock.set_face("thinking")
    
    print("\n💬 Speaking...")
    dock.speak("Hello, I am an AOS robot. How may I assist you?", emotion="friendly")
    
    print("\n📝 Displaying text...")
    dock.show_text("System Status: ONLINE", duration=2.0)
    
    print("\n📸 Using camera...")
    dock.start_video_stream()
    time.sleep(2)
    image = dock.capture_image()
    dock.stop_video_stream()
    
    print("\n🎤 Listening...")
    heard = dock.listen(duration=3.0)
    print(f"   Heard: '{heard}'")
    
    print("\n📊 Status...")
    status = dock.get_status()
    print(f"   Docked: {status['docked']}")
    print(f"   Battery: {status['battery']}%")
    print(f"   Capabilities: {sum(status['capabilities'].values())}/6 active")
    
    print("\n📲 User removes phone...")
    dock.undock()
    
    print("\n" + "=" * 70)
    print("✅ Phone Dock Demo Complete")
    print("=" * 70)


if __name__ == "__main__":
    import time
    import random
    demo_phone_dock()
