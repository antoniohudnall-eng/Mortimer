#!/usr/bin/env python3
"""
COBRA Robot - Complete Control System
Snake spine + tendon hands + integrated power
"""

import time
import math
import json
from dataclasses import dataclass
from typing import List, Tuple, Dict
from enum import Enum


class JointState(Enum):
    IDLE = "idle"
    MOVING = "moving"
    HOLDING = "holding"
    ERROR = "error"


@dataclass
class VertebraStatus:
    id: int
    pitch: float
    roll: float
    temp: float
    battery_voltage: float
    battery_soc: float
    imu_accel: Tuple[float, float, float]
    imu_gyro: Tuple[float, float, float]
    state: JointState


class VertebralBattery:
    """Battery management per vertebra"""
    
    def __init__(self, segment_id: int, cell_count: int = 2):
        self.segment_id = segment_id
        self.cell_count = cell_count
        self.voltage = 4.2
        self.capacity_mah = 3000 * cell_count
        self.current_draw = 0.0
        self.temperature = 25.0
        self.soc = 100.0
        self.cycle_count = 0
        
    def discharge(self, current: float, dt: float) -> bool:
        """Draw current from battery"""
        if self.soc <= 5.0:
            return False
        
        self.current_draw = current
        mah_used = (current * 1000 * dt) / 3600
        self.soc -= (mah_used / self.capacity_mah) * 100
        self.voltage = 4.2 - (1.2 * (100 - self.soc) / 100)
        self.temperature += current * 0.01
        return True
    
    def charge(self, current: float, dt: float):
        """Charge battery from solar/external"""
        mah_added = (current * 1000 * dt) / 3600
        self.soc = min(100, self.soc + (mah_added / self.capacity_mah) * 100)
        self.voltage = min(4.2, 3.0 + (1.2 * self.soc / 100))
        
    def get_status(self) -> dict:
        return {
            "segment_id": self.segment_id,
            "voltage": round(self.voltage, 2),
            "soc": round(self.soc, 1),
            "current": round(self.current_draw, 3),
            "temp": round(self.temperature, 1),
            "capacity_remaining": round(self.capacity_mah * self.soc / 100, 0)
        }


class Vertebra:
    """Individual vertebra controller with 2 DOF"""
    
    def __init__(self, id: int, region: str, has_battery: bool = False):
        self.id = id
        self.region = region  # cervical, thoracic, lumbar, sacrum
        self.has_battery = has_battery
        
        # Joint angles
        self.pitch = 0.0
        self.roll = 0.0
        self.target_pitch = 0.0
        self.target_roll = 0.0
        
        # Limits based on region
        if region == "cervical":
            self.pitch_limit = 15
            self.roll_limit = 10
        elif region == "thoracic":
            self.pitch_limit = 10
            self.roll_limit = 5
        else:  # lumbar
            self.pitch_limit = 15
            self.roll_limit = 10
        
        # IMU
        self.accel = [0.0, 0.0, 1.0]
        self.gyro = [0.0, 0.0, 0.0]
        
        # Battery
        self.battery = VertebralBattery(id) if has_battery else None
        
        # State
        self.state = JointState.IDLE
        self.servo_pwm = [1500, 1500]  # Microseconds
        
    def set_target(self, pitch: float, roll: float, speed: float = 100.0):
        """Set target angles with speed (deg/sec)"""
        self.target_pitch = max(-self.pitch_limit, min(self.pitch_limit, pitch))
        self.target_roll = max(-self.roll_limit, min(self.roll_limit, roll))
        self.state = JointState.MOVING
        
    def update(self, dt: float):
        """Update joint position toward target"""
        if self.state != JointState.MOVING:
            return
            
        # Smooth movement
        pitch_error = self.target_pitch - self.pitch
        roll_error = self.target_roll - self.roll
        
        max_step = 100.0 * dt
        
        if abs(pitch_error) < 0.5 and abs(roll_error) < 0.5:
            self.pitch = self.target_pitch
            self.roll = self.target_roll
            self.state = JointState.HOLDING
        else:
            self.pitch += max(-max_step, min(max_step, pitch_error))
            self.roll += max(-max_step, min(max_step, roll_error))
            
        # Simulate power draw (servos + microcontroller)
        if self.battery:
            self.battery.discharge(0.05, dt)
            
    def get_status(self) -> VertebraStatus:
        return VertebraStatus(
            id=self.id,
            pitch=self.pitch,
            roll=self.roll,
            temp=25.0 + (abs(self.pitch) + abs(self.roll)) * 0.1,
            battery_voltage=self.battery.voltage if self.battery else 0.0,
            battery_soc=self.battery.soc if self.battery else 0.0,
            imu_accel=tuple(self.accel),
            imu_gyro=tuple(self.gyro),
            state=self.state
        )


class SnakeSpine:
    """Complete 25-vertebra snake spine"""
    
    def __init__(self, model_size: str = "midi"):
        self.model_size = model_size
        self.vertebrae: List[Vertebra] = []
        
        # Create vertebrae
        # C1-C7 (cervical) - no batteries
        for i in range(7):
            self.vertebrae.append(Vertebra(i, "cervical", has_battery=False))
            
        # T1-T12 (thoracic) - with batteries + solar
        for i in range(7, 19):
            self.vertebrae.append(Vertebra(i, "thoracic", has_battery=True))
            
        # L1-L5 (lumbar) - with batteries
        for i in range(19, 24):
            self.vertebrae.append(Vertebra(i, "lumbar", has_battery=True))
            
        # S1 (sacrum) - brain housing
        self.vertebrae.append(Vertebra(24, "sacrum", has_battery=True))
        
        # Current posture
        self.current_profile = [(0.0, 0.0)] * 25
        
    def set_posture(self, curvature_profile: List[Tuple[float, float]]):
        """Set spine to curved posture"""
        for i, (pitch, roll) in enumerate(curvature_profile[:25]):
            self.vertebrae[i].set_target(pitch, roll)
            
    def natural_standing(self):
        """S-curve like human standing"""
        profile = []
        # Cervical: slight forward
        for _ in range(7):
            profile.append((5.0, 0.0))
        # Thoracic: backward
        for _ in range(12):
            profile.append((-3.0, 0.0))
        # Lumbar: forward
        for _ in range(5):
            profile.append((8.0, 0.0))
        # Sacrum: neutral
        profile.append((0.0, 0.0))
        self.set_posture(profile)
        
    def forward_bend(self, angle: float = 30.0):
        """Bend forward at waist"""
        bend_per = angle / 5
        profile = self.current_profile.copy()
        for i in range(19, 24):  # L1-L5
            profile[i] = (bend_per, 0.0)
        self.set_posture(profile)
        
    def lateral_bend(self, side: str = "left", angle: float = 20.0):
        """Side bend"""
        direction = 1.0 if side == "left" else -1.0
        profile = self.current_profile.copy()
        for i in range(7, 19):  # Thoracic
            profile[i] = (profile[i][0], angle * direction * 0.5)
        for i in range(19, 24):  # Lumbar
            profile[i] = (profile[i][0], angle * direction)
        self.set_posture(profile)
        
    def twist(self, angle: float = 30.0):
        """Rotate spine (distributed across vertebrae)"""
        twist_per = angle / 24
        profile = self.current_profile.copy()
        for i in range(24):
            profile[i] = (profile[i][0], profile[i][1] + twist_per)
        self.set_posture(profile)
        
    def balance_adjustment(self, pitch_error: float, roll_error: float):
        """Active balancing via spine"""
        correction = 0.3
        profile = self.current_profile.copy()
        for i in range(10, 20):  # Thoracic-lumbar
            current = profile[i]
            profile[i] = (
                current[0] - pitch_error * correction,
                current[1] - roll_error * correction
            )
        self.set_posture(profile)
        
    def update(self, dt: float = 0.01):
        """Update all vertebrae"""
        for v in self.vertebrae:
            v.update(dt)
        self.current_profile = [(v.pitch, v.roll) for v in self.vertebrae]
        
    def get_total_power(self) -> dict:
        """Calculate available power from all batteries"""
        total_capacity = 0
        total_remaining = 0
        total_voltage = 0
        count = 0
        
        for v in self.vertebrae:
            if v.battery:
                total_capacity += v.battery.capacity_mah
                total_remaining += v.battery.capacity_mah * v.battery.soc / 100
                total_voltage += v.battery.voltage
                count += 1
                
        return {
            "total_capacity_wh": round(total_remaining * (total_voltage / count if count else 0) / 1000, 2),
            "average_soc": round(sum(v.battery.soc for v in self.vertebrae if v.battery) / count if count else 0, 1),
            "battery_count": count,
            "individual_status": [v.battery.get_status() for v in self.vertebrae if v.battery]
        }
        
    def solar_charge(self, irradiance_w_m2: float, dt: float):
        """Charge from solar panels"""
        # Thoracic vertebrae have solar
        panel_efficiency = 0.20
        panel_area_m2 = 0.06 * 0.04  # 60mm x 40mm per panel
        
        for v in self.vertebrae:
            if v.region == "thoracic" and v.battery:
                power = irradiance_w_m2 * panel_area_m2 * panel_efficiency
                current = power / v.battery.voltage
                v.battery.charge(current, dt)


class TendonFinger:
    """Fishing line tendon-driven finger"""
    
    def __init__(self, name: str, motor_id: int, joints: int = 3):
        self.name = name
        self.motor_id = motor_id
        self.joints = joints
        self.position = 0.0  # 0=extended, 1=curled
        self.target = 0.0
        self.tension = 0.0
        self.mechanical_advantage = 2.0
        self.spring_return = True
        self.max_force = 5.0  # kg
        
    def set_position(self, target: float, speed: float = 2.0):
        """Set curl position 0.0-1.0"""
        self.target = max(0.0, min(1.0, target))
        
    def update(self, dt: float):
        """Move toward target"""
        error = self.target - self.position
        max_step = 2.0 * dt
        
        if abs(error) < 0.02:
            self.position = self.target
        else:
            self.position += max(-max_step, min(max_step, error))
            
        # Calculate tension
        if self.spring_return:
            # Tension proportional to curl
            self.tension = self.position * self.max_force
        else:
            # Dual tendon - tension depends on direction
            pass
            
    def get_force(self) -> float:
        """Current grip force in kg"""
        return self.position * self.max_force * self.mechanical_advantage


class TendonHand:
    """Complete tendon-driven hand"""
    
    def __init__(self, side: str = "left"):
        self.side = side
        self.fingers = {
            "thumb": TendonFinger("thumb", 0, joints=2),
            "index": TendonFinger("index", 1, joints=3),
            "middle": TendonFinger("middle", 2, joints=3),
            "ring": TendonFinger("ring", 3, joints=3),
            "pinky": TendonFinger("pinky", 4, joints=3),
        }
        self.wrist_pitch = 0.0
        self.wrist_roll = 0.0
        
    def set_grip(self, grip_type: str):
        """Set predefined grip"""
        grips = {
            "open": {"thumb": 0.0, "index": 0.0, "middle": 0.0, "ring": 0.0, "pinky": 0.0},
            "fist": {"thumb": 0.8, "index": 1.0, "middle": 1.0, "ring": 1.0, "pinky": 1.0},
            "point": {"thumb": 0.2, "index": 0.0, "middle": 1.0, "ring": 1.0, "pinky": 1.0},
            "pinch": {"thumb": 0.9, "index": 0.9, "middle": 0.0, "ring": 0.0, "pinky": 0.0},
            "phone_hold": {"thumb": 0.5, "index": 0.3, "middle": 0.3, "ring": 0.0, "pinky": 0.0},
            "okay": {"thumb": 0.9, "index": 0.0, "middle": 1.0, "ring": 1.0, "pinky": 1.0},
        }
        
        if grip_type in grips:
            for name, pos in grips[grip_type].items():
                self.fingers[name].set_position(pos)
                
    def get_total_force(self) -> float:
        """Sum of all finger forces"""
        return sum(f.get_force() for f in self.fingers.values())
        
    def update(self, dt: float):
        for finger in self.fingers.values():
            finger.update(dt)


class CobraPowerManager:
    """Manage distributed battery system + solar"""
    
    def __init__(self, spine: SnakeSpine):
        self.spine = spine
        self.solar_enabled = True
        self.charge_rate = 0.0
        self.total_draw = 0.0
        
    def calculate_load(self, active_servos: int, brain_compute: float) -> float:
        """Calculate current power draw in amps"""
        servo_draw = active_servos * 0.5  # 500mA per active servo
        brain_draw = brain_compute * 2.0  # 2A for RPi5 + AI HAT
        sensors_draw = 0.5
        return servo_draw + brain_draw + sensors_draw
        
    def solar_charge(self, sun_level: str = "full"):
        """
        sun_level: "dark", "cloudy", "partial", "full"
        """
        irradiance = {
            "dark": 0,
            "cloudy": 100,
            "partial": 500,
            "full": 1000
        }
        self.spine.solar_charge(irradiance.get(sun_level, 0), dt=1.0)
        
    def get_time_remaining(self, active_servos: int = 20) -> dict:
        """Estimate runtime at current load"""
        power = self.spine.get_total_power()
        total_wh = power["total_capacity_wh"]
        
        current_a = self.calculate_load(active_servos, 0.5)
        voltage = 3.7
        power_w = current_a * voltage
        
        if power_w > 0:
            hours = (total_wh / power_w)
            return {
                "hours": round(hours, 1),
                "minutes": round(hours * 60, 0),
                "at_load": f"{active_servos} servos + brain",
                "power_consumption_w": round(power_w, 2)
            }
        return {"hours": 0, "minutes": 0}


class CobraRobot:
    """Complete COBRA robot integration"""
    
    def __init__(self, model_size: str = "midi", name: str = "COBRA-1"):
        self.name = name
        self.model_size = model_size
        
        print(f"\n🐍 Initializing {name} ({model_size.upper()})")
        
        # Core systems
        self.spine = SnakeSpine(model_size)
        self.power = CobraPowerManager(self.spine)
        
        # Body
        self.left_hand = TendonHand("left")
        self.right_hand = TendonHand("right")
        
        # State
        self.running = False
        self.tick_count = 0
        
        print(f"   Vertebrae: 25 (7C + 12T + 5L + 1S)")
        print(f"   Batteries: 17 cells (thoracic + lumbar + sacrum)")
        print(f"   Solar: Thoracic vertebrae panels")
        print(f"   Tendon hands: 10 fingers with Dyneema")
        print(f"   ✅ Systems initialized\n")
        
    def calibrate(self):
        """Calibration sequence"""
        print("🔧 Calibrating COBRA...")
        
        # Center spine
        self.spine.natural_standing()
        print("   Spine: Neutral S-curve set")
        
        # Open hands
        self.left_hand.set_grip("open")
        self.right_hand.set_grip("open")
        print("   Hands: Tendons zeroed")
        
        # Wait for settling
        for _ in range(100):
            self.spine.update(0.01)
            self.left_hand.update(0.01)
            self.right_hand.update(0.01)
            time.sleep(0.01)
            
        print("✅ Calibration complete\n")
        
    def demo_sequence(self):
        """Demo movements"""
        print(f"🎭 {self.name} Demo Sequence\n")
        
        # 1. Standing posture
        print("1. Natural standing posture")
        self.spine.natural_standing()
        self._run_for(2.0)
        
        # 2. Forward bend
        print("2. Forward bend (bow)")
        self.spine.forward_bend(30)
        self._run_for(2.0)
        self.spine.natural_standing()
        self._run_for(1.0)
        
        # 3. Side bend
        print("3. Side bend")
        self.spine.lateral_bend("left", 20)
        self._run_for(2.0)
        self.spine.natural_standing()
        self._run_for(1.0)
        
        # 4. Hand grips
        print("4. Hand demonstrations")
        self.right_hand.set_grip("fist")
        self._run_for(1.0)
        self.right_hand.set_grip("point")
        self._run_for(1.0)
        self.right_hand.set_grip("pinch")
        self._run_for(1.0)
        self.right_hand.set_grip("open")
        self._run_for(1.0)
        
        # 5. Power status
        print("5. Power system status")
        status = self.spine.get_total_power()
        runtime = self.power.get_time_remaining(active_servos=20)
        print(f"   Battery: {status['average_soc']}% ({status['battery_count']} cells)")
        print(f"   Capacity: {status['total_capacity_wh']} Wh")
        print(f"   Runtime: {runtime['hours']} hours ({runtime['at_load']})")
        
        print(f"\n✅ Demo complete\n")
        
    def _run_for(self, duration: float):
        """Run update loop for duration"""
        start = time.time()
        while time.time() - start < duration:
            self.update()
            time.sleep(0.01)
            
    def update(self):
        """Main update loop"""
        dt = 0.01
        
        # Update spine
        self.spine.update(dt)
        
        # Update hands
        self.left_hand.update(dt)
        self.right_hand.update(dt)
        
        # Solar charging if enabled
        if self.tick_count % 100 == 0:  # Every second
            self.power.solar_charge("partial")
            
        self.tick_count += 1
        
    def get_status(self) -> dict:
        """Full system status"""
        power = self.spine.get_total_power()
        runtime = self.power.get_time_remaining()
        
        return {
            "name": self.name,
            "model": self.model_size,
            "spine": {
                "vertebrae": len(self.spine.vertebrae),
                "posture": self.spine.current_profile[:5]  # First 5 for brevity
            },
            "power": power,
            "runtime": runtime,
            "hands": {
                "left_grip": sum(f.position for f in self.left_hand.fingers.values()),
                "right_grip": sum(f.position for f in self.right_hand.fingers.values())
            }
        }
        
    def run(self, duration: float = 30.0):
        """Run main loop"""
        print(f"▶️  Running for {duration}s...")
        self.running = True
        
        start = time.time()
        try:
            while self.running and (time.time() - start) < duration:
                self.update()
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("\n⏹️  Stopped by user")
            
        self.running = False
        print("⏹️  Run complete")


def main():
    """COBRA Robot Demo"""
    print("=" * 70)
    print("🐍 COBRA ROBOT - Complete Build Demo")
    print("=" * 70)
    print("Snake spine + Tendon hands + Solar power")
    print("=" * 70)
    
    # Create robot
    robot = CobraRobot(model_size="midi", name="COBRA-Alpha")
    
    # Calibrate
    robot.calibrate()
    
    # Demo
    robot.demo_sequence()
    
    # Final status
    print("📊 Final Status:")
    status = robot.get_status()
    print(json.dumps(status, indent=2))
    
    print("\n" + "=" * 70)
    print("✅ COBRA Robot Demo Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
