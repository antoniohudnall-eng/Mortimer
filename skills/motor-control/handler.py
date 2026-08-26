#!/usr/bin/env python3
"""
Motor Control Skill - Brain to Body Interface

Translates cerebellum motor commands to BCSA V4 actuator instructions.
Bridges cognitive architecture to physical robot body (AOS-H1).

Joint Mapping (AOS-H1 Humanoid):
- Head: neck_pitch, neck_yaw
- Arms: shoulder_pitch, shoulder_roll, elbow_pitch, wrist_yaw
- Torso: waist_yaw, waist_pitch
- Legs: hip_pitch, hip_roll, knee_pitch, ankle_pitch, ankle_roll
"""

import time
import json
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class JointType(Enum):
    REVOLUTE = "revolute"      # Rotational joint
    PRISMATIC = "prismatic"    # Linear joint (rare in humanoids)
    FIXED = "fixed"            # No movement


@dataclass
class JointState:
    """State of a single robot joint."""
    name: str
    position: float           # Current angle/position (radians or meters)
    velocity: float           # Current velocity
    torque: float             # Current torque/load
    target_position: float    # Desired position (from brain)
    target_velocity: float    # Desired velocity
    limits: Tuple[float, float] = field(default_factory=lambda: (-math.pi, math.pi))
    joint_type: JointType = JointType.REVOLUTE
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'position': round(self.position, 4),
            'velocity': round(self.velocity, 4),
            'torque': round(self.torque, 4),
            'target_position': round(self.target_position, 4),
            'target_velocity': round(self.target_velocity, 4),
            'at_target': abs(self.position - self.target_position) < 0.01
        }


@dataclass
class BCSA_V4_Command:
    """Command structure for BCSA V4 actuator."""
    actuator_id: str
    torque: float             # Torque command (Nm)
    velocity: float         # Velocity limit (rad/s)
    position_target: float  # Target position (rad)
    stiffness: float        # Stiffness gain (0-1)
    damping: float          # Damping gain (0-1)
    
    def to_bcsa_packet(self) -> bytes:
        """Convert to BCSA V4 binary packet format."""
        # BCSA V4 uses CAN bus protocol
        # Format: [ID:2 bytes][CMD:1 byte][DATA:6 bytes][CRC:1 byte]
        packet = {
            'id': self.actuator_id,
            'torque': round(self.torque * 100),  # Scale to integer
            'velocity': round(self.velocity * 100),
            'position': round(self.position_target * 1000),
            'stiffness': int(self.stiffness * 255),
            'damping': int(self.damping * 255)
        }
        return json.dumps(packet).encode()  # Simplified - actual is binary


class AOS_H1_Kinematics:
    """
    Forward/Inverse kinematics for AOS-H1 humanoid robot.
    
    Maps end-effector positions (hands, feet) to joint angles
    and vice versa.
    """
    
    def __init__(self):
        # DH Parameters (Denavit-Hartenberg) for AOS-H1
        # Simplified - full model would have complete kinematic chain
        self.link_lengths = {
            'shoulder_to_elbow': 0.28,    # meters
            'elbow_to_wrist': 0.25,
            'hip_to_knee': 0.40,
            'knee_to_ankle': 0.40,
            'ankle_to_foot': 0.08,
            'torso_height': 0.50
        }
    
    def inverse_kinematics_arm(self, target_x: float, target_y: float, target_z: float,
                                side: str = 'right') -> Optional[Dict[str, float]]:
        """
        Calculate joint angles for arm to reach target position.
        
        Args:
            target_x, y, z: Target end-effector position (meters, relative to shoulder)
            side: 'right' or 'left'
        
        Returns:
            Dict of joint angles or None if unreachable
        """
        L1 = self.link_lengths['shoulder_to_elbow']
        L2 = self.link_lengths['elbow_to_wrist']
        
        # Distance to target
        d = math.sqrt(target_x**2 + target_y**2 + target_z**2)
        
        # Check reachability
        if d > L1 + L2 or d < abs(L1 - L2):
            return None  # Target unreachable
        
        # Law of cosines for elbow angle
        cos_elbow = (L1**2 + L2**2 - d**2) / (2 * L1 * L2)
        elbow_pitch = math.pi - math.acos(max(-1, min(1, cos_elbow)))
        
        # Shoulder angles (simplified - actual has multiple DOF)
        shoulder_pitch = math.atan2(target_z, math.sqrt(target_x**2 + target_y**2))
        shoulder_roll = math.atan2(target_y, target_x)
        
        return {
            f'{side}_shoulder_pitch': shoulder_pitch,
            f'{side}_shoulder_roll': shoulder_roll,
            f'{side}_elbow_pitch': elbow_pitch
        }
    
    def forward_kinematics_arm(self, shoulder_pitch: float, shoulder_roll: float,
                                elbow_pitch: float, side: str = 'right') -> Tuple[float, float, float]:
        """Calculate end-effector position from joint angles."""
        L1 = self.link_lengths['shoulder_to_elbow']
        L2 = self.link_lengths['elbow_to_wrist']
        
        # Elbow position
        elbow_x = L1 * math.cos(shoulder_pitch) * math.cos(shoulder_roll)
        elbow_y = L1 * math.cos(shoulder_pitch) * math.sin(shoulder_roll)
        elbow_z = L1 * math.sin(shoulder_pitch)
        
        # Wrist position (simplified - assumes elbow pitch in one plane)
        wrist_x = elbow_x + L2 * math.cos(shoulder_pitch + elbow_pitch) * math.cos(shoulder_roll)
        wrist_y = elbow_y + L2 * math.cos(shoulder_pitch + elbow_pitch) * math.sin(shoulder_roll)
        wrist_z = elbow_z + L2 * math.sin(shoulder_pitch + elbow_pitch)
        
        return (wrist_x, wrist_y, wrist_z)


class MotorControlSkill:
    """
    Motor control skill - bridges brain to body.
    
    Takes high-level motor commands from cerebellum,
    translates to BCSA V4 actuator commands,
    manages joint states and kinematics.
    """
    
    def __init__(self):
        self.kinematics = AOS_H1_Kinematics()
        self.joints: Dict[str, JointState] = {}
        self._init_joints()
        
        # Performance tracking
        self.commands_sent = 0
        self.errors = 0
        self.last_update = time.time()
    
    def _init_joints(self):
        """Initialize all AOS-H1 joints."""
        joint_definitions = [
            # Head
            ('neck_pitch', (-0.5, 0.5)),
            ('neck_yaw', (-1.0, 1.0)),
            # Right arm
            ('right_shoulder_pitch', (-1.5, 1.5)),
            ('right_shoulder_roll', (-0.5, 2.0)),
            ('right_elbow_pitch', (-2.5, 0)),
            ('right_wrist_yaw', (-1.0, 1.0)),
            # Left arm
            ('left_shoulder_pitch', (-1.5, 1.5)),
            ('left_shoulder_roll', (-2.0, 0.5)),
            ('left_elbow_pitch', (-2.5, 0)),
            ('left_wrist_yaw', (-1.0, 1.0)),
            # Torso
            ('waist_yaw', (-1.0, 1.0)),
            ('waist_pitch', (-0.3, 0.3)),
            # Right leg
            ('right_hip_pitch', (-1.5, 1.5)),
            ('right_hip_roll', (-0.5, 0.5)),
            ('right_knee_pitch', (-2.5, 0)),
            ('right_ankle_pitch', (-0.8, 0.8)),
            ('right_ankle_roll', (-0.5, 0.5)),
            # Left leg
            ('left_hip_pitch', (-1.5, 1.5)),
            ('left_hip_roll', (-0.5, 0.5)),
            ('left_knee_pitch', (-2.5, 0)),
            ('left_ankle_pitch', (-0.8, 0.8)),
            ('left_ankle_roll', (-0.5, 0.5)),
        ]
        
        for name, limits in joint_definitions:
            self.joints[name] = JointState(
                name=name,
                position=0.0,
                velocity=0.0,
                torque=0.0,
                target_position=0.0,
                target_velocity=0.0,
                limits=limits
            )
    
    def set_target_pose(self, end_effector: str, position: Tuple[float, float, float],
                       orientation: Optional[Tuple[float, float, float]] = None) -> bool:
        """
        Set target pose for end effector (inverse kinematics).
        
        Args:
            end_effector: 'right_hand', 'left_hand', 'right_foot', 'left_foot'
            position: (x, y, z) in meters
            orientation: Optional (roll, pitch, yaw) in radians
        
        Returns:
            True if pose is achievable, False otherwise
        """
        if 'hand' in end_effector:
            side = 'right' if 'right' in end_effector else 'left'
            angles = self.kinematics.inverse_kinematics_arm(
                position[0], position[1], position[2], side
            )
            
            if angles is None:
                return False  # Unreachable
            
            # Update joint targets
            for joint_name, angle in angles.items():
                if joint_name in self.joints:
                    self.joints[joint_name].target_position = self._clamp_angle(
                        joint_name, angle
                    )
            
            return True
        
        # Leg IK (simplified - would need full leg IK)
        return False
    
    def set_joint_target(self, joint_name: str, position: float, velocity: float = 1.0) -> bool:
        """Set target for specific joint."""
        if joint_name not in self.joints:
            return False
        
        joint = self.joints[joint_name]
        joint.target_position = self._clamp_angle(joint_name, position)
        joint.target_velocity = velocity
        return True
    
    def _clamp_angle(self, joint_name: str, angle: float) -> float:
        """Clamp angle to joint limits."""
        limits = self.joints[joint_name].limits
        return max(limits[0], min(limits[1], angle))
    
    def update(self, dt: float = 0.016) -> List[BCSA_V4_Command]:
        """
        Update all joints and generate actuator commands.
        
        Args:
            dt: Time step in seconds
        
        Returns:
            List of BCSA V4 commands to send
        """
        commands = []
        
        for joint_name, joint in self.joints.items():
            # Simple PD control
            error = joint.target_position - joint.position
            
            # Velocity limit
            max_vel = joint.target_velocity
            desired_vel = error / dt
            desired_vel = max(-max_vel, min(max_vel, desired_vel))
            
            # Update simulated position
            joint.position += desired_vel * dt
            joint.velocity = desired_vel
            
            # Compute torque (simplified PD)
            kp = 100.0  # Proportional gain
            kd = 10.0   # Derivative gain
            torque = kp * error + kd * (desired_vel - joint.velocity)
            joint.torque = torque
            
            # Create BCSA V4 command
            cmd = BCSA_V4_Command(
                actuator_id=joint_name,
                torque=torque,
                velocity=abs(desired_vel),
                position_target=joint.target_position,
                stiffness=0.8,
                damping=0.3
            )
            commands.append(cmd)
        
        self.last_update = time.time()
        return commands
    
    def get_body_state(self) -> Dict:
        """Get complete body state."""
        return {
            'joints': {name: joint.to_dict() for name, joint in self.joints.items()},
            'timestamp': time.time(),
            'commands_sent': self.commands_sent,
            'errors': self.errors
        }


# Skill handler
def motor_control_handler(input_data: Dict) -> Dict:
    """
    Motor control skill - brain to body interface.
    
    Input:
        action: 'set_pose' | 'set_joint' | 'update' | 'status'
        end_effector: (for set_pose) 'right_hand', 'left_hand', etc.
        position: (x, y, z) in meters
        joint: joint name
        joint_position: target angle in radians
        
    Output:
        success: bool
        commands: List of BCSA V4 commands
        body_state: Current joint states
    """
    if not hasattr(motor_control_handler, '_motor_control'):
        motor_control_handler._motor_control = MotorControlSkill()
    
    mc = motor_control_handler._motor_control
    action = input_data.get('action', 'status')
    
    if action == 'set_pose':
        success = mc.set_target_pose(
            input_data.get('end_effector', ''),
            tuple(input_data.get('position', [0, 0, 0])),
            input_data.get('orientation')
        )
        return {
            'success': success,
            'message': 'Pose set successfully' if success else 'Pose unreachable',
            'body_state': mc.get_body_state()
        }
    
    elif action == 'set_joint':
        success = mc.set_joint_target(
            input_data.get('joint', ''),
            input_data.get('joint_position', 0.0),
            input_data.get('velocity', 1.0)
        )
        return {
            'success': success,
            'message': f"Joint {input_data.get('joint')} set" if success else "Invalid joint",
            'body_state': mc.get_body_state()
        }
    
    elif action == 'update':
        commands = mc.update(input_data.get('dt', 0.016))
        return {
            'success': True,
            'commands': [cmd.to_dict() for cmd in commands],
            'command_count': len(commands),
            'body_state': mc.get_body_state()
        }
    
    else:  # status
        return {
            'success': True,
            'body_state': mc.get_body_state()
        }


if __name__ == '__main__':
    # Demo motor control
    print("🤖 AOS-H1 Motor Control Skill")
    print("=" * 60)
    
    mc = MotorControlSkill()
    
    # Set target pose for right hand
    print("\nSetting right hand target pose...")
    success = mc.set_target_pose('right_hand', (0.3, -0.2, 0.1))
    print(f"Reachable: {success}")
    
    # Update and get commands
    commands = mc.update()
    print(f"\nGenerated {len(commands)} BCSA V4 commands")
    
    # Show some joint states
    print("\nJoint States (sample):")
    for name in ['right_shoulder_pitch', 'right_elbow_pitch']:
        joint = mc.joints[name]
        print(f"  {name}:")
        print(f"    Current: {math.degrees(joint.position):.1f}°")
        print(f"    Target:  {math.degrees(joint.target_position):.1f}°")
    
    print("\n✅ Motor control ready for BCSA V4 integration!")
