#!/usr/bin/env python3
"""
CYLON Leg Modules - Bipedal Design
6-DOF humanoid legs with IMU-based balance control
"""

import json
import math
from pathlib import Path
from dataclasses import dataclass
from typing import Tuple, List, Dict

@dataclass
class JointSpec:
    """Joint specification"""
    name: str
    axis: str  # pitch, roll, yaw
    min_angle: float  # degrees
    max_angle: float
    max_torque: float  # Nm
    gear_ratio: float

@dataclass
class LinkSpec:
    """Link (segment) specification"""
    name: str
    length: float  # mm
    material: str
    mass: float  # kg
    inertia: Tuple[float, float, float]  # Ixx, Iyy, Izz

class BipedalLeg:
    """
    Humanoid leg with 6 degrees of freedom
    Hip: 3 DOF (roll, pitch, yaw)
    Knee: 1 DOF (pitch)
    Ankle: 2 DOF (roll, pitch)
    """
    
    def __init__(self, side: str = "left"):
        self.side = side
        self.joints: List[JointSpec] = []
        self.links: List[LinkSpec] = []
        self._define_joints()
        self._define_links()
    
    def _define_joints(self):
        """Define all 6 joints"""
        prefix = "L" if self.side == "left" else "R"
        
        # Hip (3 DOF)
        self.joints.extend([
            JointSpec(f"{prefix}_Hip_Roll", "roll", -30, 30, 80, 100),
            JointSpec(f"{prefix}_Hip_Pitch", "pitch", -45, 120, 120, 80),
            JointSpec(f"{prefix}_Hip_Yaw", "yaw", -45, 45, 60, 120),
        ])
        
        # Knee (1 DOF)
        self.joints.append(
            JointSpec(f"{prefix}_Knee", "pitch", 0, 140, 100, 60)
        )
        
        # Ankle (2 DOF)
        self.joints.extend([
            JointSpec(f"{prefix}_Ankle_Roll", "roll", -20, 20, 40, 80),
            JointSpec(f"{prefix}_Ankle_Pitch", "pitch", -30, 45, 50, 60),
        ])
    
    def _define_links(self):
        """Define leg segments"""
        prefix = "L" if self.side == "left" else "R"
        
        # Thigh (hip to knee)
        self.links.append(LinkSpec(
            f"{prefix}_Thigh", 450, "PLA_Carbon", 2.8,
            (0.08, 0.08, 0.02)
        ))
        
        # Shank (knee to ankle)
        self.links.append(LinkSpec(
            f"{prefix}_Shank", 450, "PLA_Carbon", 2.2,
            (0.06, 0.06, 0.015)
        ))
        
        # Foot (ankle to ground)
        self.links.append(LinkSpec(
            f"{prefix}_Foot", 100, "TPU_Flex", 0.8,
            (0.01, 0.02, 0.01)
        ))
    
    def get_stl_files(self) -> List[Dict]:
        """Generate STL file specifications"""
        return [
            {
                "name": f"cylon_bipedal_hip_{self.side}.stl",
                "size_mb": 2.1,
                "parts": ["hip_frame", "bearing_housings", "motor_mounts"],
                "material": "PLA_Carbon",
                "infill": 60,
                "supports": True
            },
            {
                "name": f"cylon_bipedal_thigh_{self.side}.stl",
                "size_mb": 1.8,
                "parts": ["thigh_tube", "knee_joint"],
                "material": "PLA_Carbon",
                "infill": 50,
                "supports": False
            },
            {
                "name": f"cylon_bipedal_shank_{self.side}.stl",
                "size_mb": 1.5,
                "parts": ["shank_tube", "ankle_joint"],
                "material": "PLA_Carbon",
                "infill": 50,
                "supports": False
            },
            {
                "name": f"cylon_bipedal_foot_{self.side}.stl",
                "size_mb": 0.9,
                "parts": ["foot_plate", "sole_grip"],
                "material": "TPU_Flex",
                "infill": 30,
                "supports": True
            }
        ]
    
    def get_bom(self) -> List[Dict]:
        """Bill of materials"""
        return [
            {"item": "Nema 23 Stepper", "qty": 2, "location": "hip_pitch, knee"},
            {"item": "Nema 17 Stepper", "qty": 4, "location": "hip_roll, hip_yaw, ankle_roll, ankle_pitch"},
            {"item": "608ZZ Bearing", "qty": 12, "location": "all_joints"},
            {"item": "GT2 Belt 6mm", "qty": 2, "length_m": 1.5, "location": "hip_pitch, knee"},
            {"item": "GT2 Pulley 20T", "qty": 4, "location": "motor_drives"},
            {"item": "Linear Rail MGN12", "qty": 2, "length_mm": 200, "location": "knee_brace"},
            {"item": "Spring Torsion", "qty": 2, "torque_nm": 5, "location": "knee_assist"},
            {"item": "Load Cell 50kg", "qty": 4, "location": "feet_corners"},
            {"item": "IMU MPU6050", "qty": 1, "location": "shank_lower"},
        ]
    
    def get_workspace(self) -> Dict:
        """Calculate leg workspace"""
        # Simplified forward kinematics for workspace
        L1 = 450  # thigh
        L2 = 450  # shank
        L3 = 100  # foot
        
        max_reach = L1 + L2 + L3
        min_reach = abs(L1 - L2) + L3
        
        return {
            "max_reach_mm": max_reach,
            "min_reach_mm": min_reach,
            "workspace_height_mm": (L1 + L2) * 0.8,
            "step_length_max_mm": 600,
            "step_height_max_mm": 150,
            "footprint_radius_mm": 120
        }
    
    def export_design(self, output_dir: Path):
        """Export complete design package"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        design = {
            "type": "bipedal",
            "side": self.side,
            "dof": 6,
            "joints": [
                {
                    "name": j.name,
                    "axis": j.axis,
                    "range": [j.min_angle, j.max_angle],
                    "torque_nm": j.max_torque
                }
                for j in self.joints
            ],
            "links": [
                {
                    "name": l.name,
                    "length_mm": l.length,
                    "mass_kg": l.mass,
                    "material": l.material
                }
                for l in self.links
            ],
            "stl_files": self.get_stl_files(),
            "bom": self.get_bom(),
            "workspace": self.get_workspace()
        }
        
        with open(output_dir / f"bipedal_leg_{self.side}_design.json", "w") as f:
            json.dump(design, f, indent=2)
        
        return design

if __name__ == "__main__":
    leg = BipedalLeg("left")
    design = leg.export_design(Path("/tmp/cylon_legs"))
    
    print("="*60)
    print("CYLON BIPEDAL LEG MODULE")
    print("="*60)
    print(f"\nDegrees of Freedom: {design['dof']}")
    print(f"Joints: {len(design['joints'])}")
    print(f"Links: {len(design['links'])}")
    
    print("\n[Joints]")
    for j in design['joints']:
        print(f"  {j['name']}: {j['axis']} [{j['range'][0]}° to {j['range'][1]}°]")
    
    print("\n[Workspace]")
    for k, v in design['workspace'].items():
        print(f"  {k}: {v}mm")
    
    print(f"\nTotal mass: {sum(l.mass for l in leg.links):.2f}kg")
    print(f"STL files: {len(design['stl_files'])}")
