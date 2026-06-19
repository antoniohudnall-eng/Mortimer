#!/usr/bin/env python3
"""
AOS Balance System
Active balancing for bipedal robots (Cylon, C-3PO style)

Uses IMU (MPU6050/9250) + PID control + servo feedback
Prevents falls, manages gait, dynamic stability
"""

import math
import time
from collections import deque

class BalanceController:
    """
    Active balance control for humanoid robots
    
    Sensors:
    - IMU (MPU6050): 6-axis accel + gyro
    - Optional: Force sensors in feet
    - Optional: Joint position feedback
    
    Control:
    - PID on pitch/roll
    - Ankle adjustments (primary)
    - Hip adjustments (secondary)
    - Arm counter-balance
    """
    
    def __init__(self, robot_height=1750):
        """
        robot_height: mm (center of mass height)
        """
        self.height = robot_height
        self.com_height = robot_height * 0.55  # Center of mass ~55% up
        
        # IMU state
        self.pitch = 0.0  # Forward/back tilt
        self.roll = 0.0   # Side tilt
        self.yaw = 0.0    # Rotation
        
        self.pitch_rate = 0.0
        self.roll_rate = 0.0
        
        # PID controllers
        self.pitch_pid = PIDController(kp=2.0, ki=0.1, kd=0.5)
        self.roll_pid = PIDController(kp=2.0, ki=0.1, kd=0.5)
        
        # Balance state
        self.balance_state = "stable"  # stable, correcting, falling, fallen
        self.stability_score = 1.0
        
        # History for prediction
        self.pitch_history = deque(maxlen=50)
        self.roll_history = deque(maxlen=50)
        
        # Servo corrections
        self.ankle_correction = [0.0, 0.0]  # Left, Right
        self.hip_correction = [0.0, 0.0]
        self.arm_correction = [0.0, 0.0]  # Left, Right arm
        
        print("⚖️  Balance System initialized")
        print(f"   Robot height: {robot_height}mm")
        print(f"   Center of mass: {self.com_height}mm")
    
    def update_imu(self, accel, gyro, dt=0.01):
        """
        Update balance from IMU data
        accel: [ax, ay, az] in g
        gyro: [gx, gy, gz] in deg/s
        """
        ax, ay, az = accel
        gx, gy, gz = gyro
        
        # Calculate pitch and roll from accelerometer
        accel_pitch = math.atan2(ax, math.sqrt(ay**2 + az**2)) * 180 / math.pi
        accel_roll = math.atan2(ay, math.sqrt(ax**2 + az**2)) * 180 / math.pi
        
        # Complementary filter with gyro
        alpha = 0.98
        self.pitch = alpha * (self.pitch + gx * dt) + (1 - alpha) * accel_pitch
        self.roll = alpha * (self.roll + gy * dt) + (1 - alpha) * accel_roll
        self.yaw += gz * dt
        
        self.pitch_rate = gx
        self.roll_rate = gy
        
        # Store history
        self.pitch_history.append(self.pitch)
        self.roll_history.append(self.roll)
        
        # Calculate stability
        self._calculate_stability()
    
    def _calculate_stability(self):
        """Calculate how stable the robot is"""
        # Variance in recent history
        if len(self.pitch_history) < 10:
            self.stability_score = 1.0
            return
        
        pitch_var = sum((p - self.pitch)**2 for p in list(self.pitch_history)[-10:]) / 10
        roll_var = sum((r - self.roll)**2 for r in list(self.roll_history)[-10:]) / 10
        
        total_var = pitch_var + roll_var
        
        # Score 0-1 (1 = perfectly stable)
        self.stability_score = max(0, 1 - (total_var / 100))
        
        # Update state
        if abs(self.pitch) > 20 or abs(self.roll) > 20:
            self.balance_state = "falling"
        elif abs(self.pitch) > 5 or abs(self.roll) > 5:
            self.balance_state = "correcting"
        else:
            self.balance_state = "stable"
    
    def compute_corrections(self):
        """Compute servo corrections to maintain balance"""
        
        if self.balance_state == "fallen":
            return None  # Can't recover from fallen
        
        # PID control on pitch and roll
        pitch_output = self.pitch_pid.update(self.pitch, 0)
        roll_output = self.roll_pid.update(self.roll, 0)
        
        # Convert to servo commands
        # Ankle: primary correction
        self.ankle_correction[0] = pitch_output + roll_output  # Left
        self.ankle_correction[1] = pitch_output - roll_output    # Right
        
        # Hip: secondary correction
        self.hip_correction[0] = pitch_output * 0.3
        self.hip_correction[1] = pitch_output * 0.3
        
        # Arms: counter-balance
        self.arm_correction[0] = -roll_output * 0.5   # Left arm
        self.arm_correction[1] = roll_output * 0.5    # Right arm
        
        return {
            "ankles": self.ankle_correction,
            "hips": self.hip_correction,
            "arms": self.arm_correction,
        }
    
    def predict_fall(self, horizon_sec=0.5):
        """Predict if robot will fall in horizon seconds"""
        if len(self.pitch_history) < 5:
            return False, 0.0
        
        # Simple linear extrapolation
        recent = list(self.pitch_history)[-5:]
        slope = (recent[-1] - recent[0]) / 5
        
        future_pitch = self.pitch + slope * (horizon_sec * 100)
        
        # Check if predicted to exceed balance limit
        if abs(future_pitch) > 25:
            confidence = min(1.0, abs(future_pitch) / 45)
            return True, confidence
        
        return False, 0.0
    
    def get_recovery_action(self):
        """Get action to recover from instability"""
        if self.balance_state == "falling":
            # Emergency: widen stance, arms out
            return {
                "stance": "wide",
                "knees": "slight_bend",
                "arms": "extended",
                "speed": "emergency",
            }
        
        elif self.balance_state == "correcting":
            # Normal correction
            return {
                "stance": "normal",
                "knees": "maintain",
                "arms": "counter_balance",
                "speed": "normal",
            }
        
        return None  # Stable, no action needed
    
    def get_status(self):
        return {
            "pitch": round(self.pitch, 2),
            "roll": round(self.roll, 2),
            "yaw": round(self.yaw, 2),
            "state": self.balance_state,
            "stability": round(self.stability_score, 2),
            "corrections": {
                "ankles": [round(c, 2) for c in self.ankle_correction],
                "hips": [round(c, 2) for c in self.hip_correction],
                "arms": [round(c, 2) for c in self.arm_correction],
            }
        }


class PIDController:
    """Simple PID controller"""
    
    def __init__(self, kp=1.0, ki=0.0, kd=0.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        self.integral = 0.0
        self.last_error = 0.0
        self.last_time = time.time()
    
    def update(self, current, target):
        error = target - current
        now = time.time()
        dt = now - self.last_time
        
        if dt <= 0:
            dt = 0.001
        
        # Proportional
        p = self.kp * error
        
        # Integral
        self.integral += error * dt
        self.integral = max(-100, min(100, self.integral))  # Anti-windup
        i = self.ki * self.integral
        
        # Derivative
        d = self.kd * (error - self.last_error) / dt
        
        self.last_error = error
        self.last_time = now
        
        return p + i + d


class GaitController:
    """Walking gait control for bipedal robots"""
    
    def __init__(self, balance_controller):
        self.balance = balance_controller
        self.step_phase = 0.0  # 0-1 cycle
        self.walking = False
        
        # Step parameters
        self.step_length = 100  # mm
        self.step_height = 30   # mm lift
        self.step_duration = 1.0  # seconds per step
        
        # Current leg positions
        self.left_foot = [0, 0, 0]
        self.right_foot = [0, 0, 0]
    
    def start_walking(self, speed=1.0):
        """Start walking at given speed"""
        self.walking = True
        self.step_duration = 1.0 / speed
        print(f"🚶 Walking started (speed: {speed}x)")
    
    def stop_walking(self):
        """Stop and return to standing"""
        self.walking = False
        self.step_phase = 0.0
        print("🧍 Walking stopped")
    
    def update(self, dt):
        """Update gait, return joint angles"""
        if not self.walking:
            return self._get_standing_pose()
        
        # Advance phase
        self.step_phase += dt / self.step_duration
        if self.step_phase >= 1.0:
            self.step_phase -= 1.0
        
        # Calculate positions based on phase
        if self.step_phase < 0.5:
            # Left foot swing, right foot stance
            left_pos = self._swing_leg(self.step_phase * 2)
            right_pos = self._stance_leg(self.step_phase * 2)
        else:
            # Right foot swing, left foot stance
            left_pos = self._stance_leg((self.step_phase - 0.5) * 2)
            right_pos = self._swing_leg((self.step_phase - 0.5) * 2)
        
        # Convert to joint angles
        return self._positions_to_angles(left_pos, right_pos)
    
    def _swing_leg(self, phase):
        """Calculate swing leg position"""
        # Phase 0-1: lift, move forward, lower
        x = phase * self.step_length
        z = math.sin(phase * math.pi) * self.step_height
        return [x, 0, z]
    
    def _stance_leg(self, phase):
        """Calculate stance leg position"""
        # Stays on ground, moves back
        x = -phase * self.step_length
        return [x, 0, 0]
    
    def _get_standing_pose(self):
        """Return standing joint angles"""
        return {
            "left_hip": 0, "left_knee": 0, "left_ankle": 0,
            "right_hip": 0, "right_knee": 0, "right_ankle": 0,
        }
    
    def _positions_to_angles(self, left_pos, right_pos):
        """Convert foot positions to joint angles"""
        # Inverse kinematics (simplified)
        # In real: use full IK solver
        
        left_angles = {
            "hip": math.degrees(math.atan2(left_pos[0], 400)),
            "knee": -abs(left_pos[2]) * 0.5,
            "ankle": -self.balance.pitch * 0.5,
        }
        
        right_angles = {
            "hip": math.degrees(math.atan2(right_pos[0], 400)),
            "knee": -abs(right_pos[2]) * 0.5,
            "ankle": -self.balance.pitch * 0.5,
        }
        
        return {"left": left_angles, "right": right_angles}


def demo_balance():
    """Demo balance system"""
    print("=" * 70)
    print("⚖️  AOS Balance System Demo")
    print("=" * 70)
    
    balance = BalanceController(robot_height=1750)
    gait = GaitController(balance)
    
    # Simulate standing with perturbations
    print("\n🧍 Standing mode...")
    for i in range(50):
        # Simulate IMU data with small perturbations
        accel = [random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), 1.0]
        gyro = [random.uniform(-2, 2), random.uniform(-2, 2), random.uniform(-0.5, 0.5)]
        
        balance.update_imu(accel, gyro, dt=0.01)
        corrections = balance.compute_corrections()
        
        if i % 10 == 0:
            status = balance.get_status()
            print(f"   Pitch: {status['pitch']:+.2f}° | "
                  f"Stability: {status['stability']:.2f} | "
                  f"State: {status['state']}")
    
    print("\n🚶 Walking mode...")
    gait.start_walking(speed=0.5)
    
    for i in range(100):
        # Simulate walking IMU
        accel = [random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2), 0.9]
        gyro = [random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-2, 2)]
        
        balance.update_imu(accel, gyro, dt=0.01)
        gait.update(0.01)
        
        if i % 20 == 0:
            status = balance.get_status()
            predict, conf = balance.predict_fall(0.5)
            print(f"   Phase: {gait.step_phase:.2f} | "
                  f"Stability: {status['stability']:.2f} | "
                  f"Fall risk: {conf:.2f}")
    
    gait.stop_walking()
    
    print("\n" + "=" * 70)
    print("✅ Balance Demo Complete")
    print("=" * 70)


if __name__ == "__main__":
    import random
    demo_balance()
