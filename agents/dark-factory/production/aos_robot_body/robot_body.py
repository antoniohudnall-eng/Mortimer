#!/usr/bin/env python3
"""
AOS Complete Robot Body System

Components:
- Brain_Heart_Stomach: Mind integration
- BalanceSystem: Active balancing
- PhoneDock: Phone integration
- BodyParts: Hands, arms, legs control

Assembly: Complete humanoid robot control
"""

import json
import time
import math
from enum import Enum

from brain_heart_stomach import RobotBodyController
from balance_system import BalanceController, GaitController
from phone_dock import PhoneDock, PhoneConnection


class ServoJoint:
    """Individual servo/servo joint control"""
    
    def __init__(self, name, min_angle=-90, max_angle=90, default=0):
        self.name = name
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.current_angle = default
        self.target_angle = default
        self.speed = 0  # degrees per second
        
    def set_position(self, angle, speed=100):
        """Set target position with speed"""
        self.target_angle = max(self.min_angle, min(self.max_angle, angle))
        self.speed = speed
        
    def update(self, dt):
        """Move toward target (simulated)"""
        if abs(self.target_angle - self.current_angle) < 0.1:
            self.current_angle = self.target_angle
            return True
        
        direction = 1 if self.target_angle > self.current_angle else -1
        max_change = self.speed * dt
        
        if abs(self.target_angle - self.current_angle) <= max_change:
            self.current_angle = self.target_angle
        else:
            self.current_angle += direction * max_change
            
        return abs(self.target_angle - self.current_angle) < 0.1


class RobotHand:
    """
    Robotic hand with articulated fingers
    
    5 fingers: thumb, index, middle, ring, pinky
    Each finger: 2-3 joints
    """
    
    def __init__(self, side="left"):
        self.side = side
        self.joints = {}
        
        # Create fingers
        fingers = ["thumb", "index", "middle", "ring", "pinky"]
        
        for finger in fingers:
            self.joints[f"{finger}_base"] = ServoJoint(
                f"{side}_{finger}_base", -30, 30, 0)
            self.joints[f"{finger}_mid"] = ServoJoint(
                f"{side}_{finger}_mid", 0, 90, 0)
            self.joints[f"{finger}_tip"] = ServoJoint(
                f"{side}_{finger}_tip", 0, 90, 0)
        
        # Wrist
        self.joints["wrist_pitch"] = ServoJoint(
            f"{side}_wrist_pitch", -45, 45, 0)
        self.joints["wrist_roll"] = ServoJoint(
            f"{side}_wrist_roll", -90, 90, 0)
        
    def set_grip(self, grip_type):
        """Set hand to predefined grip"""
        grips = {
            "open": {
                "thumb_base": -20, "thumb_mid": 0, "thumb_tip": 0,
                "index_base": 0, "index_mid": 0, "index_tip": 0,
                "middle_base": 0, "middle_mid": 0, "middle_tip": 0,
                "ring_base": 0, "ring_mid": 0, "ring_tip": 0,
                "pinky_base": 0, "pinky_mid": 0, "pinky_tip": 0,
            },
            "fist": {
                "thumb_base": 20, "thumb_mid": 45, "thumb_tip": 45,
                "index_base": 0, "index_mid": 90, "index_tip": 90,
                "middle_base": 0, "middle_mid": 90, "middle_tip": 90,
                "ring_base": 0, "ring_mid": 90, "ring_tip": 90,
                "pinky_base": 0, "pinky_mid": 90, "pinky_tip": 90,
            },
            "point": {
                "thumb_base": -20, "thumb_mid": 45, "thumb_tip": 45,
                "index_base": 0, "index_mid": 0, "index_tip": 0,
                "middle_base": 0, "middle_mid": 90, "middle_tip": 90,
                "ring_base": 0, "ring_mid": 90, "ring_tip": 90,
                "pinky_base": 0, "pinky_mid": 90, "pinky_tip": 90,
            },
            "phone_hold": {
                "thumb_base": -10, "thumb_mid": 30, "thumb_tip": 30,
                "index_base": -5, "index_mid": 30, "index_tip": 30,
                "middle_base": 0, "middle_mid": 30, "middle_tip": 30,
                "ring_base": 0, "ring_mid": 90, "ring_tip": 90,
                "pinky_base": 0, "pinky_mid": 90, "pinky_tip": 90,
            },
        }
        
        if grip_type in grips:
            for joint_name, angle in grips[grip_type].items():
                full_name = f"{joint_name}"
                if full_name in self.joints:
                    self.joints[full_name].set_position(angle)
    
    def update(self, dt):
        """Update all joints"""
        for joint in self.joints.values():
            joint.update(dt)
    
    def get_positions(self):
        """Get current positions of all joints"""
        return {name: joint.current_angle 
                for name, joint in self.joints.items()}


class RobotArm:
    """
    Complete arm: shoulder, elbow, wrist, hand
    """
    
    def __init__(self, side="left"):
        self.side = side
        
        # Shoulder (3 DOF)
        self.shoulder_pitch = ServoJoint(f"{side}_shoulder_pitch", -180, 60, 0)
        self.shoulder_roll = ServoJoint(f"{side}_shoulder_roll", -90, 90, 0)
        self.shoulder_yaw = ServoJoint(f"{side}_shoulder_yaw", -90, 90, 0)
        
        # Elbow (1 DOF)
        self.elbow = ServoJoint(f"{side}_elbow", 0, 135, 90)
        
        # Hand
        self.hand = RobotHand(side)
        
        # Current pose target
        self.pose_target = None
        
    def set_pose(self, pose_name):
        """Set arm to predefined pose"""
        poses = {
            "neutral": {
                "shoulder_pitch": 0, "shoulder_roll": 0, "shoulder_yaw": 0,
                "elbow": 90,
            },
            "raised": {
                "shoulder_pitch": -90, "shoulder_roll": 0, "shoulder_yaw": 0,
                "elbow": 45,
            },
            "wave": {
                "shoulder_pitch": -45, "shoulder_roll": 45, "shoulder_yaw": 0,
                "elbow": 45,
            },
            "phone_hold": {
                "shoulder_pitch": -30, "shoulder_roll": 10, "shoulder_yaw": 0,
                "elbow": 90,
            },
            "balance": {
                "shoulder_pitch": 0, "shoulder_roll": 45, "shoulder_yaw": 0,
                "elbow": 10,
            },
        }
        
        if pose_name in poses:
            p = poses[pose_name]
            self.shoulder_pitch.set_position(p["shoulder_pitch"])
            self.shoulder_roll.set_position(p["shoulder_roll"])
            self.shoulder_yaw.set_position(p["shoulder_yaw"])
            self.elbow.set_position(p["elbow"])
            
            if pose_name == "phone_hold":
                self.hand.set_grip("phone_hold")
            else:
                self.hand.set_grip("open")
    
    def reach(self, x, y, z):
        """
        Inverse kinematics to reach point (simplified)
        x, y, z in mm relative to shoulder
        """
        # Simplified IK - just point toward target
        # Real IK would solve joint angles analytically
        
        distance = math.sqrt(x**2 + y**2 + z**2)
        
        # Rough shoulder orientation
        pitch = -math.degrees(math.atan2(y, distance))
        yaw = math.degrees(math.atan2(z, x))
        
        self.shoulder_pitch.set_position(pitch)
        self.shoulder_yaw.set_position(yaw)
        
        # Bend elbow based on distance
        if distance < 300:
            self.elbow.set_position(135)
        elif distance < 500:
            self.elbow.set_position(90)
        else:
            self.elbow.set_position(45)
    
    def update(self, dt):
        """Update all joints"""
        self.shoulder_pitch.update(dt)
        self.shoulder_roll.update(dt)
        self.shoulder_yaw.update(dt)
        self.elbow.update(dt)
        self.hand.update(dt)
    
    def get_positions(self):
        """Get all joint positions"""
        return {
            "shoulder_pitch": self.shoulder_pitch.current_angle,
            "shoulder_roll": self.shoulder_roll.current_angle,
            "shoulder_yaw": self.shoulder_yaw.current_angle,
            "elbow": self.elbow.current_angle,
            "hand": self.hand.get_positions(),
        }


class RobotLeg:
    """
    Complete leg: hip, knee, ankle
    """
    
    def __init__(self, side="left"):
        self.side = side
        
        # Hip (3 DOF)
        self.hip_pitch = ServoJoint(f"{side}_hip_pitch", -45, 45, 0)
        self.hip_roll = ServoJoint(f"{side}_hip_roll", -30, 30, 0)
        self.hip_yaw = ServoJoint(f"{side}_hip_yaw", -45, 45, 0)
        
        # Knee (1 DOF)
        self.knee = ServoJoint(f"{side}_knee", 0, 135, 0)
        
        # Ankle (2 DOF)
        self.ankle_pitch = ServoJoint(f"{side}_ankle_pitch", -30, 30, 0)
        self.ankle_roll = ServoJoint(f"{side}_ankle_roll", -20, 20, 0)
        
        # Foot contact sensor (simulated)
        self.foot_contact = False
        
    def set_stance(self, stance="standing"):
        """Set leg to stance position"""
        stances = {
            "standing": {
                "hip_pitch": 0, "hip_roll": 0, "hip_yaw": 0,
                "knee": 0,
                "ankle_pitch": 0, "ankle_roll": 0,
            },
            "step_forward": {
                "hip_pitch": 15, "hip_roll": 0, "hip_yaw": 0,
                "knee": 30,
                "ankle_pitch": -10, "ankle_roll": 0,
            },
            "step_backward": {
                "hip_pitch": -10, "hip_roll": 0, "hip_yaw": 0,
                "knee": 10,
                "ankle_pitch": 5, "ankle_roll": 0,
            },
            "kneel": {
                "hip_pitch": 0, "hip_roll": 0, "hip_yaw": 0,
                "knee": 90,
                "ankle_pitch": -10, "ankle_roll": 0,
            },
        }
        
        if stance in stances:
            s = stances[stance]
            self.hip_pitch.set_position(s["hip_pitch"])
            self.hip_roll.set_position(s["hip_roll"])
            self.hip_yaw.set_position(s["hip_yaw"])
            self.knee.set_position(s["knee"])
            self.ankle_pitch.set_position(s["ankle_pitch"])
            self.ankle_roll.set_position(s["ankle_roll"])
    
    def apply_balance_correction(self, correction):
        """Apply balance correction to ankle"""
        ankle_p, ankle_r = correction
        
        # Add to current position
        new_pitch = self.ankle_pitch.current_angle + ankle_p
        new_roll = self.ankle_roll.current_angle + ankle_r
        
        self.ankle_pitch.set_position(new_pitch)
        self.ankle_roll.set_position(new_roll)
    
    def update(self, dt):
        """Update all joints"""
        self.hip_pitch.update(dt)
        self.hip_roll.update(dt)
        self.hip_yaw.update(dt)
        self.knee.update(dt)
        self.ankle_pitch.update(dt)
        self.ankle_roll.update(dt)


class CompleteAOSRobot:
    """
    Complete AOS Robot with all systems
    """
    
    def __init__(self, name="AOS-Robot", robot_type="cylon"):
        self.name = name
        self.robot_type = robot_type
        
        # Core systems
        self.brain_heart_stomach = RobotBodyController(robot_type, name)
        self.balance = BalanceController(robot_height=1750)
        self.gait = GaitController(self.balance)
        self.phone_dock = PhoneDock(PhoneConnection.USB)
        
        # Body parts
        self.left_arm = RobotArm("left")
        self.right_arm = RobotArm("right")
        self.left_leg = RobotLeg("left")
        self.right_leg = RobotLeg("right")
        
        # State
        self.running = False
        self.current_action = "idle"
        
        print(f"\n🤖 {name} Fully Assembled")
        print(f"   Type: {robot_type}")
        print(f"   Systems: Brain+Heart+Stomach, Balance, Phone, Body")
        
    def dock_phone(self):
        """Dock phone to chest"""
        success = self.phone_dock.dock_phone()
        if success:
            self.phone_dock.set_face("awake")
            self.brain_heart_stomach.speak("Phone connected. Systems online.")
        return success
    
    def calibrate_balance(self):
        """Calibrate standing balance"""
        print("⚖️  Calibrating balance...")
        
        # Set neutral stance
        self.left_leg.set_stance("standing")
        self.right_leg.set_stance("standing")
        self.left_arm.set_pose("neutral")
        self.right_arm.set_pose("neutral")
        
        # Wait for joints to settle
        for _ in range(100):  # 1 second at 100Hz
            dt = 0.01
            self.left_leg.update(dt)
            self.right_leg.update(dt)
            self.left_arm.update(dt)
            self.right_arm.update(dt)
        
        print("✅ Calibration complete")
    
    def perform_action(self, action):
        """Perform high-level action"""
        self.current_action = action
        
        if action == "stand":
            self.left_leg.set_stance("standing")
            self.right_leg.set_stance("standing")
            self.left_arm.set_pose("neutral")
            self.right_arm.set_pose("neutral")
            
        elif action == "wave":
            self.right_arm.set_pose("wave")
            self.phone_dock.speak("Hello!")
            
        elif action == "hold_phone":
            # Use left hand to hold phone from dock
            self.left_arm.set_pose("phone_hold")
            
        elif action == "walk_forward":
            self.gait.start_walking(speed=0.5)
            
        elif action == "stop":
            self.gait.stop_walking()
            
        elif action == "balance_correction":
            # Apply balance corrections
            corrections = self.balance.compute_corrections()
            if corrections:
                self.left_leg.apply_balance_correction(
                    corrections["ankles"])
                self.right_leg.apply_balance_correction(
                    corrections["ankles"])
    
    def update(self, dt=0.01):
        """
        Main update loop
        Integrate all systems
        """
        # 1. Update brain-heart-stomach
        self.brain_heart_stomach.tick()
        
        # 2. Read sensors (simulated)
        accel = [0, 0, 1]  # Would come from IMU
        gyro = [0, 0, 0]  # Would come from IMU
        
        # 3. Update balance
        self.balance.update_imu(accel, gyro, dt)
        
        # 4. Update gait if walking
        if self.gait.walking:
            gait_angles = self.gait.update(dt)
            # Apply gait angles to legs
            self._apply_gait_angles(gait_angles)
        
        # 5. Apply balance corrections
        if self.balance.balance_state == "correcting":
            corrections = self.balance.compute_corrections()
            if corrections:
                self.left_leg.apply_balance_correction(
                    corrections["ankles"])
                self.right_leg.apply_balance_correction(
                    corrections["ankles"])
        
        # 6. Update all joints
        self.left_arm.update(dt)
        self.right_arm.update(dt)
        self.left_leg.update(dt)
        self.right_leg.update(dt)
        
        # 7. Update phone dock
        status = self.get_status()
        self.phone_dock.show_status(status)
    
    def _apply_gait_angles(self, angles):
        """Apply gait controller angles to legs"""
        if "left" in angles:
            l = angles["left"]
            self.left_leg.hip_pitch.set_position(l.get("hip", 0))
            self.left_leg.knee.set_position(l.get("knee", 0))
            self.left_leg.ankle_pitch.set_position(l.get("ankle", 0))
        
        if "right" in angles:
            r = angles["right"]
            self.right_leg.hip_pitch.set_position(r.get("hip", 0))
            self.right_leg.knee.set_position(r.get("knee", 0))
            self.right_leg.ankle_pitch.set_position(r.get("ankle", 0))
    
    def run(self, duration_sec=30):
        """Run for duration"""
        print(f"\n▶️  Running for {duration_sec}s...\n")
        self.running = True
        
        start = time.time()
        while self.running and (time.time() - start) < duration_sec:
            self.update(dt=0.01)
            time.sleep(0.01)
        
        self.running = False
        print("\n⏹️  Run complete")
    
    def get_status(self):
        """Full system status"""
        return {
            "name": self.name,
            "robot_type": self.robot_type,
            "current_action": self.current_action,
            "brain": self.brain_heart_stomach.get_status(),
            "balance": self.balance.get_status(),
            "phone": self.phone_dock.get_status(),
            "left_arm": self.left_arm.get_positions(),
            "right_arm": self.right_arm.get_positions(),
        }


def demo_complete_robot():
    """Demo complete AOS robot"""
    print("=" * 70)
    print("🤖 AOS COMPLETE ROBOT DEMO")
    print("=" * 70)
    print("Brain + Heart + Stomach + Balance + Phone + Body")
    print("=" * 70)
    
    # Create robot
    robot = CompleteAOSRobot(name="C-3PO-Alpha", robot_type="c3po")
    
    # Dock phone
    robot.dock_phone()
    
    # Calibrate
    robot.calibrate_balance()
    
    # Perform actions
    print("\n🎭 Performing actions...")
    
    robot.perform_action("stand")
    time.sleep(2)
    
    robot.perform_action("wave")
    time.sleep(2)
    
    robot.phone_dock.speak("I am fluent in over six million forms of communication.")
    
    # Run main loop
    robot.run(duration_sec=10)
    
    # Final status
    print("\n📊 Final Status:")
    status = robot.get_status()
    print(f"   Name: {status['name']}")
    print(f"   Mood: {status['brain']['heart']['mood']}")
    print(f"   Balance: {status['balance']['state']}")
    print(f"   Phone: {'Docked' if status['phone']['docked'] else 'None'}")
    
    print("\n" + "=" * 70)
    print("✅ Complete Robot Demo Finished")
    print("=" * 70)


if __name__ == "__main__":
    import time
    import random
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    demo_complete_robot()
