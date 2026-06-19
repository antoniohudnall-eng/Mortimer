#!/usr/bin/env python3
"""
CYLON Leg Control Systems
Unified control architecture for all three leg types
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum

class LegMode(Enum):
    """Operating modes for hybrid systems"""
    WALKING = "walking"
    ROLLING = "rolling"
    HYBRID = "hybrid"
    CLIMBING = "climbing"
    STAIR = "stair_mode"
    BALANCE = "balance_recovery"

class BipedalController:
    """
    Control system for bipedal walking
    - ZMP (Zero Moment Point) balance
    - Trajectory generation
    - Footstep planning
    - Fall detection
    """
    
    def __init__(self):
        self.balance_active = True
        self.zmp_threshold = 0.05  # meters
        self.walking_speed = 0.5  # m/s
        self.step_height = 0.05  # meters
    
    def get_software_stack(self) -> Dict:
        return {
            "firmware": "ODrive_v0.5.4",
            "motor_drivers": "ODrive_56V",
            "balance_controller": "ZMP_MPC_v2",
            "trajectory_planner": "Crocoddyl_or_RBDL",
            "sensors": {
                "IMU": "VectorNav_VN-100",
                "force_plates": "4x_LoadCell_50kg",
                "encoders": "Absolute_14bit",
                "cameras": "Intel_D435i_depth"
            },
            "control_rate_hz": 1000,
            "algorithms": [
                "ZMP_preview_control",
                "MPC_trajectory_optimization",
                "Quadratic_programming_IK",
                "Kalman_filter_state_estimation"
            ]
        }

class WheeledController:
    """
    Control system for wheeled hybrid
    - Mode switching
    - Wheel coordination
    - Hybrid gait planning
    """
    
    def __init__(self):
        self.current_mode = LegMode.HYBRID
        self.wheel_speed = 0.0
        self.leg_angle = 0.0
    
    def get_software_stack(self) -> Dict:
        return {
            "firmware": "ODrive_v0.5.4",
            "motor_drivers": "ODrive_24V",
            "wheel_controller": "Mecanum_4WD",
            "hybrid_planner": "Gait_Wheel_Blend",
            "sensors": {
                "IMU": "MPU6050_or_BNO055",
                "wheel_encoders": "Incremental_1024ppr",
                "contact_switches": "4x_per_foot",
                "current_sensors": "INA226"
            },
            "control_rate_hz": 500,
            "algorithms": [
                "Mode_state_machine",
                "Mecanum_kinematics",
                "Hybrid_gait_generator",
                "Ride_height_PID"
            ]
        }

class TrackedController:
    """
    Control system for tracked base
    - Track coordination
    - Terrain adaptation
    - Articulated platform stabilization
    """
    
    def __init__(self):
        self.track_speed_left = 0.0
        self.track_speed_right = 0.0
        self.platform_pitch = 0.0
        self.platform_roll = 0.0
    
    def get_software_stack(self) -> Dict:
        return {
            "firmware": "VESC_or_ODrive",
            "motor_drivers": "VESC_75V_300A",
            "track_controller": "Differential_drive",
            "stabilization": "Gyroscopically_controlled_platform",
            "sensors": {
                "IMU": "VectorNav_VN-100",
                "gyro_stabilizer": "3_axis_control_moment",
                "height_sensor": "LiDAR_or_ultrasonic",
                "track_encoders": "Absolute_14bit"
            },
            "control_rate_hz": 500,
            "algorithms": [
                "Tank_drive_kinematics",
                "Skid_steering_control",
                "Platform_stabilization_PID",
                "Terrain_adaptation_heuristic"
            ]
        }

class LegSystemComparison:
    """Compare all three leg systems"""
    
    def __init__(self):
        self.systems = {
            "bipedal": BipedalController(),
            "wheeled": WheeledController(),
            "tracked": TrackedController()
        }
    
    def generate_comparison(self) -> Dict:
        """Generate comprehensive comparison"""
        return {
            "bipedal": {
                "complexity": "Very High",
                "max_speed_ms": 0.8,
                "terrain": "Complex (stairs, obstacles)",
                "energy_efficiency": "Low",
                "battery_hours": 4,
                "balance_requirement": "Active ZMP control",
                "software_difficulty": "PhD-level robotics",
                "fall_recovery": "Difficult",
                "cost_estimate": "$8,000-12,000",
                "best_for": "Human environments, dexterity"
            },
            "wheeled": {
                "complexity": "Medium",
                "max_speed_ms": 2.5,
                "terrain": "Flat + moderate slopes",
                "energy_efficiency": "High",
                "battery_hours": 8,
                "balance_requirement": "Minimal (in hybrid mode)",
                "software_difficulty": "Advanced undergraduate",
                "fall_recovery": "Easy (wheels always stable)",
                "cost_estimate": "$4,000-6,000",
                "best_for": "Warehouses, offices, mixed terrain"
            },
            "tracked": {
                "complexity": "Low",
                "max_speed_ms": 3.0,
                "terrain": "Rough (stairs, slopes, debris)",
                "energy_efficiency": "Medium",
                "battery_hours": 6,
                "balance_requirement": "Passive gyro stabilization",
                "software_difficulty": "Intermediate",
                "fall_recovery": "N/A (cannot fall)",
                "cost_estimate": "$5,000-7,000",
                "best_for": "Outdoor, construction, exploration"
            }
        }
    
    def export_all(self, output_dir: Path):
        """Export all control systems"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Export individual systems
        for name, controller in self.systems.items():
            with open(output_dir / f"{name}_control.json", "w") as f:
                json.dump(controller.get_software_stack(), f, indent=2)
        
        # Export comparison
        with open(output_dir / "leg_system_comparison.json", "w") as f:
            json.dump(self.generate_comparison(), f, indent=2)
        
        # Generate markdown report
        self._generate_report(output_dir)
    
    def _generate_report(self, output_dir: Path):
        """Generate markdown comparison report"""
        comp = self.generate_comparison()
        
        report = """# CYLON Leg Systems Comparison

## Overview

Three locomotion architectures for the CYLON humanoid platform:

1. **Bipedal** (6-DOF legs) - Human-like walking
2. **Wheeled Hybrid** (6-DOF + omni wheels) - Efficient rolling + stepping
3. **Tracked Base** - Maximum terrain capability

## Comparison Table

| Metric | Bipedal | Wheeled | Tracked |
|--------|---------|---------|---------|
"""
        
        for metric, values in comp.items():
            report += f"| {metric.replace('_', ' ').title()} | {values['bipedal']} | {values['wheeled']} | {values['tracked']} |\n"
        
        report += """
## Software Requirements

### Bipedal (Hardest)
- Real-time ZMP balance (1000Hz)
- Trajectory optimization (MPC)
- Full inverse kinematics
- State estimation (Kalman filter)
- Fall detection & recovery

### Wheeled Hybrid (Medium)
- Mode switching state machine
- Mecanum wheel kinematics
- Hybrid gait blending
- Simpler balance (static stability)

### Tracked (Easiest)
- Differential drive control
- Gyroscopic stabilization
- Height adjustment PID
- No dynamic balance needed

## Recommendation

**For development:** Start with **Wheeled Hybrid**
- Fastest to implement
- Most forgiving
- Real-world useful

**For ultimate capability:** **Bipedal**
- Most human-like
- Most complex
- Longest development time

**For rough terrain:** **Tracked**
- Cannot fall over
- Best obstacle handling
- Replaces legs entirely

## Files Generated

- `bipedal_control.json` - Software stack for walking
- `wheeled_control.json` - Software stack for hybrid
- `tracked_control.json` - Software stack for tracks
- `leg_system_comparison.json` - All metrics

---

*Generated by CYLON Leg Design System*
"""
        
        with open(output_dir / "LEG_SYSTEM_COMPARISON.md", "w") as f:
            f.write(report)

if __name__ == "__main__":
    comparison = LegSystemComparison()
    output = Path("/tmp/cylon_legs/control_systems")
    comparison.export_all(output)
    
    print("="*60)
    print("CYLON LEG CONTROL SYSTEMS")
    print("="*60)
    
    comp = comparison.generate_comparison()
    
    print("\n[Quick Comparison]")
    print(f"{'':20} {'Bipedal':<12} {'Wheeled':<12} {'Tracked':<12}")
    print("-" * 56)
    for metric, values in comp.items():
        print(f"{metric.replace('_', ' ')[:18]:<20} {str(values['bipedal'])[:10]:<12} {str(values['wheeled'])[:10]:<12} {str(values['tracked'])[:10]:<12}")
    
    print(f"\nExported to: {output}")
    print("="*60)
