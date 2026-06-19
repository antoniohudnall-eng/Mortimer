#!/usr/bin/env python3
"""
FreeCAD Python script to generate CYLON leg modules
Run with: freecadcmd generate_legs.py
Or: python3 generate_legs.py (if FreeCAD module available)
"""

import sys
import os
from pathlib import Path

# FreeCAD paths (if available)
freecad_paths = [
    "/usr/lib/freecad/lib",
    "/usr/lib/freecad/Mod",
    "/usr/local/lib/freecad/lib",
]

for p in freecad_paths:
    if os.path.exists(p):
        sys.path.append(p)

try:
    import FreeCAD
    import Part
    import Mesh
    FREECAD_AVAILABLE = True
except ImportError:
    FREECAD_AVAILABLE = False
    print("⚠️  FreeCAD not available. Install with: sudo apt install freecad")

class CylonLegGenerator:
    """Generate CYLON leg modules using FreeCAD"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Standard dimensions (mm)
        self.hip_width = 160
        self.hip_height = 120
        self.thigh_length = 450
        self.shank_length = 450
        self.joint_diameter = 50
        
    def generate_bipedal_hip(self):
        """Generate bipedal hip joint module"""
        if not FREECAD_AVAILABLE:
            return self._create_openscad_placeholder("bipedal_hip")
        
        doc = FreeCAD.newDocument("BipedalHip")
        
        # Main hip block
        hip_box = Part.makeBox(self.hip_width, 80, self.hip_height)
        hip_box.translate(FreeCAD.Vector(-self.hip_width/2, -40, 0))
        
        # Motor mount cylinders
        motor_left = Part.makeCylinder(25, 60, FreeCAD.Vector(-60, 0, 60))
        motor_right = Part.makeCylinder(25, 60, FreeCAD.Vector(60, 0, 60))
        
        # Bearing housings
        bearing_left = Part.makeCylinder(35, 20, FreeCAD.Vector(-60, -30, 50))
        bearing_right = Part.makeCylinder(35, 20, FreeCAD.Vector(60, -30, 50))
        
        # Combine
        hip_shape = hip_box.fuse(motor_left).fuse(motor_right).fuse(bearing_left).fuse(bearing_right)
        
        # Create mesh and export
        mesh = Mesh.Mesh(hip_shape.tessellate(0.1))
        mesh.write(str(self.output_dir / "cylon_bipedal_hip_left.stl"))
        
        doc.recompute()
        return True
    
    def generate_bipedal_thigh(self):
        """Generate bipedal thigh"""
        if not FREECAD_AVAILABLE:
            return self._create_openscad_placeholder("bipedal_thigh")
        
        doc = FreeCAD.newDocument("BipedalThigh")
        
        # Thigh tube (hollow cylinder)
        outer = Part.makeCylinder(35, self.thigh_length)
        inner = Part.makeCylinder(28, self.thigh_length)
        thigh_tube = outer.cut(inner)
        
        # Knee joint at bottom
        knee = Part.makeCylinder(40, 30)
        knee.translate(FreeCAD.Vector(0, 0, -30))
        
        thigh_shape = thigh_tube.fuse(knee)
        
        mesh = Mesh.Mesh(thigh_shape.tessellate(0.1))
        mesh.write(str(self.output_dir / "cylon_bipedal_thigh_left.stl"))
        
        doc.recompute()
        return True
    
    def generate_wheeled_foot(self):
        """Generate wheeled foot with omni wheel housing"""
        if not FREECAD_AVAILABLE:
            return self._create_openscad_placeholder("wheeled_foot")
        
        doc = FreeCAD.newDocument("WheeledFoot")
        
        # Foot plate
        foot = Part.makeBox(120, 80, 20)
        
        # Wheel housing
        housing = Part.makeCylinder(85, 60)
        housing.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 90)
        housing.translate(FreeCAD.Vector(0, 0, -40))
        
        # Cutout for wheel
        wheel_cut = Part.makeCylinder(75, 65)
        wheel_cut.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 90)
        wheel_cut.translate(FreeCAD.Vector(0, 0, -40))
        
        housing = housing.cut(wheel_cut)
        foot_shape = foot.fuse(housing)
        
        mesh = Mesh.Mesh(foot_shape.tessellate(0.1))
        mesh.write(str(self.output_dir / "cylon_wheeled_foot_left.stl"))
        
        doc.recompute()
        return True
    
    def generate_omni_wheel(self):
        """Generate omni wheel"""
        if not FREECAD_AVAILABLE:
            return self._create_openscad_placeholder("omni_wheel")
        
        doc = FreeCAD.newDocument("OmniWheel")
        
        # Hub
        hub = Part.makeCylinder(30, 50)
        
        # Rim
        rim = Part.makeCylinder(75, 50)
        rim_outer = Part.makeCylinder(78, 50)
        rim = rim_outer.cut(rim)
        
        # Rollers (simplified as 12 small cylinders)
        wheel_shape = hub.fuse(rim)
        
        for i in range(12):
            angle = i * 30
            roller = Part.makeCylinder(8, 50)
            roller.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), 45)
            roller.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), angle)
            roller.translate(FreeCAD.Vector(75 * 0.9 * 0.707, 75 * 0.9 * 0.707, 0))
            wheel_shape = wheel_shape.fuse(roller)
        
        mesh = Mesh.Mesh(wheel_shape.tessellate(0.1))
        mesh.write(str(self.output_dir / "cylon_omni_wheel.stl"))
        
        doc.recompute()
        return True
    
    def generate_tracked_frame(self):
        """Generate tracked base frame"""
        if not FREECAD_AVAILABLE:
            return self._create_openscad_placeholder("tracked_frame")
        
        doc = FreeCAD.newDocument("TrackedFrame")
        
        # Side plate
        side_plate = Part.makeBox(10, 150, 600)
        
        # Add mounting points
        for z in [100, 300, 500]:
            mount = Part.makeCylinder(20, 15)
            mount.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 90)
            mount.translate(FreeCAD.Vector(-5, 75, z))
            side_plate = side_plate.fuse(mount)
        
        mesh = Mesh.Mesh(side_plate.tessellate(0.1))
        mesh.write(str(self.output_dir / "cylon_tracked_frame_left.stl"))
        
        doc.recompute()
        return True
    
    def _create_openscad_placeholder(self, name: str) -> bool:
        """Create OpenSCAD placeholder when FreeCAD unavailable"""
        scad_content = f"""
// {name} - CYLON Leg Module
// Generated from design specs

$fn = 100;

// Module: {name}
// Material: PLA_Carbon (or TPU_95A for wheels)
// Infill: 50-70%

// NOTE: This is a simplified placeholder
// Full parametric model requires FreeCAD or manual CAD

// Dimensions from spec
hip_width = 160;
hip_height = 120;
thigh_length = 450;
shank_length = 450;

// Simplified geometry for {name}
module {name}() {{
    // TODO: Full geometry from design specs
    cube([100, 100, 100], center=true);
}}

{name}();
"""
        scad_file = self.output_dir / f"{name}.scad"
        scad_file.write_text(scad_content)
        print(f"  Created OpenSCAD: {scad_file.name}")
        return False
    
    def generate_all(self):
        """Generate all leg modules"""
        print("="*60)
        print("CYLON LEG MODULE STL GENERATION")
        print("="*60)
        
        if FREECAD_AVAILABLE:
            print("✅ FreeCAD available - generating meshes\n")
        else:
            print("⚠️  FreeCAD not available - creating OpenSCAD placeholders")
            print("   Install FreeCAD: sudo apt install freecad")
            print("   Then run: freecadcmd generate_legs.py\n")
        
        modules = [
            ("Bipedal Hip", self.generate_bipedal_hip),
            ("Bipedal Thigh", self.generate_bipedal_thigh),
            ("Wheeled Foot", self.generate_wheeled_foot),
            ("Omni Wheel", self.generate_omni_wheel),
            ("Tracked Frame", self.generate_tracked_frame),
        ]
        
        generated = []
        for name, func in modules:
            print(f"Generating: {name}...")
            try:
                if func():
                    print(f"  ✅ STL exported")
                    generated.append(f"{name}.stl")
                else:
                    print(f"  ⚠️  OpenSCAD placeholder created")
                    generated.append(f"{name}.scad")
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        print(f"\n{'='*60}")
        print(f"Generated {len(generated)} files in:")
        print(f"  {self.output_dir}")
        print(f"{'='*60}")
        
        return generated

if __name__ == "__main__":
    output = Path("/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/production/stl_leg_modules")
    generator = CylonLegGenerator(output)
    generator.generate_all()
