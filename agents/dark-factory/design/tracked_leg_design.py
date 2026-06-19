#!/usr/bin/env python3
"""
CYLON Leg Modules - Tracked Base Design
Lower body replaced with tracked drivetrain
Maximum terrain capability, zero balance complexity
"""

import json
import math
from pathlib import Path
from dataclasses import dataclass
from typing import Tuple, List, Dict

@dataclass
class TrackSpec:
    """Continuous track specification"""
    width_mm: float
    length_mm: float
    ground_contact_mm: float
    track_pitch_mm: float
    shoe_count: int
    max_speed_ms: float
    climbing_angle_deg: float

class TrackedLeg:
    """
    Tracked base replaces legs entirely
    Torso mounts on articulated platform with:
    - 2 DOF (pitch, roll) for terrain adaptation
    - Hydraulic/electric height adjustment
    - Gyro-stabilized platform
    
    Best for: Rough terrain, stairs, slopes
    Trade-off: No leg articulation, bulkier
    """
    
    def __init__(self, side: str = "left"):
        self.side = side
        self.track: TrackSpec = None
        self.height_range_mm = (400, 800)  # Adjustable ride height
        self._define_track()
    
    def _define_track(self):
        """Define track system"""
        self.track = TrackSpec(
            width_mm=150,
            length_mm=600,
            ground_contact_mm=400,
            track_pitch_mm=40,
            shoe_count=50,
            max_speed_ms= 3.0,
            climbing_angle_deg= 35
        )
    
    def get_stl_files(self) -> List[Dict]:
        """Generate STL file specifications"""
        return [
            {
                "name": f"cylon_tracked_suspension_{self.side}.stl",
                "size_mb": 2.5,
                "parts": ["suspension_arm", "pivot_housing", "shock_mount"],
                "material": "ABS_Impact",
                "infill": 70,
                "supports": True
            },
            {
                "name": f"cylon_tracked_drive_sprocket_{self.side}.stl",
                "size_mb": 0.6,
                "parts": ["sprocket", "hub", "bearing_seat"],
                "material": "PLA_Carbon",
                "infill": 80,
                "supports": False
            },
            {
                "name": f"cylon_tracked_idler_{self.side}.stl",
                "size_mb": 0.5,
                "parts": ["idler_wheel", "tensioner"],
                "material": "PLA_Carbon",
                "infill": 70,
                "supports": False
            },
            {
                "name": f"cylon_tracked_shoe_{self.side}.stl",
                "size_mb": 0.4,
                "parts": ["shoe_plate", "grousers", "pin_holes"],
                "material": "TPU_95A",
                "infill": 50,
                "supports": False
            },
            {
                "name": f"cylon_tracked_roadwheel_{self.side}.stl",
                "size_mb": 0.3,
                "parts": ["wheel", "bearing_seat"],
                "material": "TPU_95A",
                "infill": 40,
                "supports": False
            },
            {
                "name": f"cylon_tracked_frame_{self.side}.stl",
                "size_mb": 1.8,
                "parts": ["side_plate", "cross_members", "motor_mount"],
                "material": "PLA_Carbon",
                "infill": 60,
                "supports": True
            }
        ]
    
    def get_bom(self) -> List[Dict]:
        """Bill of materials"""
        return [
            {"item": "Brushless Motor 1kW", "qty": 1, "location": "track_drive"},
            {"item": "Planetary Gearbox 50:1", "qty": 1, "location": "track_drive"},
            {"item": "Track Shoes", "qty": 50, "material": "TPU_95A", "location": "track"},
            {"item": "Road Wheels", "qty": 6, "diameter_mm": 80, "location": "suspension"},
            {"item": "Torsion Bar Springs", "qty": 6, "torque_nm": 20, "location": "roadwheel_suspension"},
            {"item": "Drive Sprocket", "qty": 1, "teeth": 15, "location": "motor_output"},
            {"item": "Idler Wheel", "qty": 1, "diameter_mm": 100, "location": "track_return"},
            {"item": "Track Pins", "qty": 50, "diameter_mm": 8, "material": "steel", "location": "track_shoes"},
            {"item": "Linear Actuator", "qty": 1, "stroke_mm": 400, "force_N": 2000, "location": "height_adjust"},
            {"item": "Gyro Stabilizer", "qty": 1, "axes": 3, "location": "platform"},
            {"item": "Hydraulic Cylinder", "qty": 2, "stroke_mm": 200, "location": "articulation"},
        ]
    
    def get_capabilities(self) -> Dict:
        """Terrain capabilities"""
        return {
            "max_speed": self.track.max_speed_ms,
            "climbing_angle": self.track.climbing_angle_deg,
            "step_height_mm": 200,  # Can climb stairs
            "trench_crossing_mm": 400,
            "ground_pressure_kpa": 15,  # Low for soft terrain
            "ride_height_range_mm": self.height_range_mm,
            "articulation": {
                "pitch": "±15° (terrain following)",
                "roll": "±10° (side slope compensation)"
            }
        }
    
    def export_design(self, output_dir: Path) -> Dict:
        """Export complete design package"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        design = {
            "type": "tracked_base",
            "side": self.side,
            "dof": 2,  # Articulation only
            "track": {
                "width_mm": self.track.width_mm,
                "length_mm": self.track.length_mm,
                "ground_contact_mm": self.track.ground_contact_mm,
                "shoe_count": self.track.shoe_count,
                "max_speed_ms": self.track.max_speed_ms
            },
            "height_adjustment": {
                "min_mm": self.height_range_mm[0],
                "max_mm": self.height_range_mm[1],
                "actuator": "linear_electric"
            },
            "stl_files": self.get_stl_files(),
            "bom": self.get_bom(),
            "capabilities": self.get_capabilities(),
            "total_stl_size_mb": sum(f["size_mb"] for f in self.get_stl_files()),
            "interchangeable": False,  # Cannot swap with bipedal/wheeled
            "notes": "Complete lower body replacement, not leg modules"
        }
        
        with open(output_dir / f"tracked_leg_{self.side}_design.json", "w") as f:
            json.dump(design, f, indent=2)
        
        return design

if __name__ == "__main__":
    leg = TrackedLeg("left")
    design = leg.export_design(Path("/tmp/cylon_legs"))
    
    print("="*60)
    print("CYLON TRACKED BASE MODULE")
    print("="*60)
    print(f"\nTrack: {design['track']['width_mm']}mm × {design['track']['length_mm']}mm")
    print(f"Max speed: {design['track']['max_speed_ms']} m/s")
    print(f"Climbing angle: {design['track']['climbing_angle_deg']}°")
    
    print("\n[Capabilities]")
    for k, v in design['capabilities'].items():
        if isinstance(v, dict):
            print(f"  {k}:")
            for kk, vv in v.items():
                print(f"    {kk}: {vv}")
        else:
            print(f"  {k}: {v}")
    
    print(f"\nSTL files: {len(design['stl_files'])} ({design['total_stl_size_mb']:.1f}MB total)")
    print("\n⚠️  NOTE: This replaces entire lower body, not interchangeable with leg modules")
