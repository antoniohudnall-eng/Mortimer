#!/usr/bin/env python3
"""
CYLON Leg Modules - Wheeled Hybrid Design
6-DOF legs with omnidirectional wheels at feet
Best of both: humanoid dexterity + wheeled efficiency
"""

import json
import math
from pathlib import Path
from dataclasses import dataclass
from typing import Tuple, List, Dict

@dataclass
class JointSpec:
    name: str
    axis: str
    min_angle: float
    max_angle: float
    max_torque: float

@dataclass
class WheelSpec:
    """Omnidirectional wheel specification"""
    diameter_mm: float
    width_mm: float
    roller_count: int
    roller_angle: float  # Typically 45 or 90 degrees
    motor_rpm: int
    max_speed_ms: float

class WheeledLeg:
    """
    Hybrid leg with 6-DOF articulation + omnidirectional wheels
    Mode 1: Walking (legs articulate, wheels locked)
    Mode 2: Rolling (legs fixed, wheels drive)
    Mode 3: Hybrid (legs adjust height/angle, wheels drive)
    """
    
    def __init__(self, side: str = "left"):
        self.side = side
        self.joints: List[JointSpec] = []
        self.wheel: WheelSpec = None
        self._define_joints()
        self._define_wheel()
    
    def _define_joints(self):
        """Define 6 DOF joints (same as bipedal for interchangeability)"""
        prefix = "L" if self.side == "left" else "R"
        
        # Hip (3 DOF) - for stance adjustment in hybrid mode
        self.joints.extend([
            JointSpec(f"{prefix}_Hip_Roll", "roll", -30, 30, 60),
            JointSpec(f"{prefix}_Hip_Pitch", "pitch", -60, 90, 80),
            JointSpec(f"{prefix}_Hip_Yaw", "yaw", -45, 45, 40),
        ])
        
        # Knee (1 DOF) - for ride height adjustment
        self.joints.append(
            JointSpec(f"{prefix}_Knee", "pitch", 30, 120, 60)
        )
        
        # Ankle (2 DOF) - for wheel angle adjustment
        self.joints.extend([
            JointSpec(f"{prefix}_Ankle_Roll", "roll", -15, 15, 30),
            JointSpec(f"{prefix}_Ankle_Pitch", "pitch", -20, 30, 40),
        ])
    
    def _define_wheel(self):
        """Define omnidirectional wheel at foot"""
        self.wheel = WheelSpec(
            diameter_mm=150,
            width_mm=50,
            roller_count=12,
            roller_angle=45,  # Mecanum-style
            motor_rpm=3000,
            max_speed_ms=2.5
        )
    
    def get_stl_files(self) -> List[Dict]:
        """Generate STL file specifications"""
        return [
            {
                "name": f"cylon_wheeled_hip_{self.side}.stl",
                "size_mb": 1.8,
                "parts": ["hip_frame", "motor_mounts", "electronics_bay"],
                "material": "PLA_Carbon",
                "infill": 50,
                "supports": True
            },
            {
                "name": f"cylon_wheeled_thigh_{self.side}.stl",
                "size_mb": 1.4,
                "parts": ["thigh_tube", "knee_brace"],
                "material": "PLA_Carbon",
                "infill": 45,
                "supports": False
            },
            {
                "name": f"cylon_wheeled_shank_{self.side}.stl",
                "size_mb": 1.2,
                "parts": ["shank_tube", "ankle_bracket"],
                "material": "PLA_Carbon",
                "infill": 45,
                "supports": False
            },
            {
                "name": f"cylon_wheeled_foot_{self.side}.stl",
                "size_mb": 1.6,
                "parts": ["wheel_housing", "suspension", "contact_sensors"],
                "material": "ABS_Impact",
                "infill": 55,
                "supports": True
            },
            {
                "name": f"cylon_wheel_omni_{self.side}.stl",
                "size_mb": 0.8,
                "parts": ["hub", "rim", "roller_mounts"],
                "material": "TPU_95A",
                "infill": 40,
                "supports": False
            }
        ]
    
    def get_bom(self) -> List[Dict]:
        """Bill of materials"""
        return [
            {"item": "Nema 17 Stepper", "qty": 6, "location": "all_joints"},
            {"item": "Nema 23 Stepper", "qty": 1, "location": "wheel_drive"},
            {"item": "608ZZ Bearing", "qty": 8, "location": "joints"},
            {"item": "MR105 Bearing", "qty": 24, "location": "wheel_rollers"},
            {"item": "GT2 Belt 6mm", "qty": 1, "length_m": 1.0, "location": "wheel_motor"},
            {"nitem": "Rubber Roller", "qty": 12, "diameter_mm": 15, "location": "wheel"},
            {"item": " Rotary Encoder", "qty": 1, "location": "wheel_shaft"},
            {"item": "Spring Compression", "qty": 4, "load_kg": 50, "location": "foot_suspension"},
            {"item": "Contact Switch", "qty": 4, "location": "foot_corners"},
            {"item": "IMU MPU6050", "qty": 1, "location": "shank"},
            {"item": "Wheel Motor Driver", "qty": 1, "current_A": 10, "location": "ankle_electronics"},
        ]
    
    def get_modes(self) -> Dict:
        """Define operating modes"""
        return {
            "walking": {
                "description": "Pure walking, wheels locked as feet",
                "max_speed_ms": 0.8,
                "energy_efficiency": "low",
                "terrain": "complex",
                "battery_hours": 4
            },
            "rolling": {
                "description": "Pure rolling, legs fixed in stance",
                "max_speed_ms": 2.5,
                "energy_efficiency": "high",
                "terrain": "flat",
                "battery_hours": 8
            },
            "hybrid": {
                "description": "Legs adjust height/angle, wheels drive",
                "max_speed_ms": 1.8,
                "energy_efficiency": "medium",
                "terrain": "moderate",
                "battery_hours": 6
            }
        }
    
    def export_design(self, output_dir: Path) -> Dict:
        """Export complete design package"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        design = {
            "type": "wheeled_hybrid",
            "side": self.side,
            "dof": 6,
            "wheel": {
                "diameter_mm": self.wheel.diameter_mm,
                "type": "omnidirectional",
                "roller_angle": self.wheel.roller_angle,
                "max_speed_ms": self.wheel.max_speed_ms
            },
            "joints": [
                {
                    "name": j.name,
                    "axis": j.axis,
                    "range": [j.min_angle, j.max_angle],
                    "torque_nm": j.max_torque
                }
                for j in self.joints
            ],
            "stl_files": self.get_stl_files(),
            "bom": self.get_bom(),
            "modes": self.get_modes(),
            "total_stl_size_mb": sum(f["size_mb"] for f in self.get_stl_files())
        }
        
        with open(output_dir / f"wheeled_leg_{self.side}_design.json", "w") as f:
            json.dump(design, f, indent=2)
        
        return design

if __name__ == "__main__":
    leg = WheeledLeg("left")
    design = leg.export_design(Path("/tmp/cylon_legs"))
    
    print("="*60)
    print("CYLON WHEELED HYBRID LEG MODULE")
    print("="*60)
    print(f"\nDegrees of Freedom: {design['dof']}")
    print(f"Wheel: {design['wheel']['diameter_mm']}mm Ø, {design['wheel']['type']}")
    print(f"Max rolling speed: {design['wheel']['max_speed_ms']} m/s")
    
    print("\n[Operating Modes]")
    for mode, spec in design['modes'].items():
        print(f"  {mode}: {spec['max_speed_ms']}m/s, {spec['battery_hours']}h battery")
    
    print(f"\nSTL files: {len(design['stl_files'])} ({design['total_stl_size_mb']:.1f}MB total)")
