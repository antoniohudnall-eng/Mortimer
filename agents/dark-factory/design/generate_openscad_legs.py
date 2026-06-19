#!/usr/bin/env python3
"""
OpenSCAD-based CYLON Leg Module STL Generator
Creates .scad files and renders them to STL using OpenSCAD
"""

import subprocess
import json
from pathlib import Path
from typing import List, Dict

class OpenSCADLegGenerator:
    """Generate CYLON legs using OpenSCAD"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.scad_dir = self.output_dir / "scad_source"
        self.scad_dir.mkdir(exist_ok=True)
    
    def _scad_header(self) -> str:
        """Common OpenSCAD header"""
        return """// CYLON Leg Module - OpenSCAD
// Material: PLA_Carbon or TPU_95A
// Infill: 50-70%
// Supports: Yes (where noted)

$fn = 100;  // Circle resolution

// Precision settings
$fs = 0.1;  // Minimum facet size
$fa = 5;    // Minimum angle

"""
    
    def generate_bipedal_hip(self, side: str = "left"):
        """Generate bipedal hip module"""
        scad = self._scad_header()
        scad += """
// BIPEDAL HIP MODULE
// DOF: 3 (roll, pitch, yaw)
// Motors: Nema 23 (pitch), Nema 17 (roll, yaw)

module bipedal_hip() {
    // Main hip block
    difference() {
        union() {
            // Hip body
            translate([-80, -40, 0])
                cube([160, 80, 120]);
            
            // Motor mount - pitch (front)
            translate([0, 45, 60])
                rotate([90, 0, 0])
                cylinder(h=30, d=58);
            
            // Bearing housing - roll (side)
            translate([-80, 0, 60])
                rotate([0, 90, 0])
                cylinder(h=40, d=70);
            
            // Bearing housing - other side
            translate([40, 0, 60])
                rotate([0, 90, 0])
                cylinder(h=40, d=70);
        }
        
        // Motor shaft hole
        translate([0, 50, 60])
            rotate([90, 0, 0])
            cylinder(h=100, d=8);
        
        // Roll shaft holes
        translate([-100, 0, 60])
            rotate([0, 90, 0])
            cylinder(h=200, d=12);
        
        // Weight reduction pockets
        translate([-60, -20, 30])
            cube([40, 40, 60]);
        translate([20, -20, 30])
            cube([40, 40, 60]);
    }
    
    // Thigh attachment (simplified)
    translate([0, 0, -50])
        cylinder(h=50, d=45);
}

bipedal_hip();
"""
        scad_file = self.scad_dir / f"bipedal_hip_{side}.scad"
        scad_file.write_text(scad)
        return scad_file
    
    def generate_bipedal_thigh(self, side: str = "left"):
        """Generate bipedal thigh"""
        scad = self._scad_header()
        scad += """
// BIPEDAL THIGH MODULE
// Length: 450mm
// Material: PLA_Carbon (hollow for weight reduction)

module bipedal_thigh() {
    // Upper thigh (near hip)
    difference() {
        union() {
            // Main tube - outer
            cylinder(h=400, d=70);
            
            // Hip joint mount
            translate([0, 0, 380])
                cylinder(h=50, d=60);
        }
        
        // Inner bore (weight reduction + wiring channel)
        translate([0, 0, -10])
            cylinder(h=420, d=56);
        
        // Wire exit ports
        for(i = [0:3]) {
            rotate([0, 0, i * 90])
            translate([30, 0, 200])
                cylinder(h=20, d=8);
        }
    }
    
    // Knee joint housing (at bottom)
    translate([0, 0, -60]) {
        difference() {
            cylinder(h=70, d=80);
            
            // Knee shaft hole
            translate([0, 0, -10])
                cylinder(h=90, d=12);
            
            // Bearing seat
            translate([0, 0, 35])
                cylinder(h=15, d=62);
        }
    }
}

bipedal_thigh();
"""
        scad_file = self.scad_dir / f"bipedal_thigh_{side}.scad"
        scad_file.write_text(scad)
        return scad_file
    
    def generate_wheeled_foot(self, side: str = "left"):
        """Generate wheeled foot"""
        scad = self._scad_header()
        scad += """
// WHEELED FOOT MODULE
// Wheel: 150mm omni-directional
// Housing: ABS_Impact

module wheeled_foot() {
    // Foot plate
    difference() {
        cube([120, 80, 20], center=true);
        
        // Contact sensor holes
        for(x = [-50, 50]) {
            for(y = [-30, 30]) {
                translate([x, y, 0])
                    cylinder(h=25, d=6, center=true);
            }
        }
    }
    
    // Wheel housing (U-shape)
    translate([0, 0, -50]) {
        difference() {
            // Outer housing
            hull() {
                cylinder(h=60, d=90);
                translate([0, 0, 60])
                    cube([100, 60, 20], center=true);
            }
            
            // Wheel cavity
            rotate([90, 0, 0])
                cylinder(h=80, d=82, center=true);
            
            // Axle holes
            rotate([90, 0, 0])
                cylinder(h=100, d=10, center=true);
        }
    }
    
    // Ankle connector
    translate([0, 0, 20])
        cylinder(h=40, d=45);
}

wheeled_foot();
"""
        scad_file = self.scad_dir / f"wheeled_foot_{side}.scad"
        scad_file.write_text(scad)
        return scad_file
    
    def generate_omni_wheel(self):
        """Generate omni wheel"""
        scad = self._scad_header()
        scad += """
// OMNI-DIRECTIONAL WHEEL
// Diameter: 150mm
// Rollers: 12 at 45°
// Material: Hub=PLA, Rollers=TPU_95A

module omni_wheel() {
    // Central hub
    difference() {
        cylinder(h=50, d=60, center=true);
        cylinder(h=60, d=10, center=true);  // Axle hole
    }
    
    // Outer rim (two disks)
    for(z = [-22, 22]) {
        translate([0, 0, z])
            difference() {
                cylinder(h=6, d=150, center=true);
                cylinder(h=8, d=75, center=true);
            }
    }
    
    // Spokes
    for(i = [0:5]) {
        rotate([0, 0, i * 60])
        translate([40, 0, 0])
            cube([60, 8, 44], center=true);
    }
    
    // Roller positions (simplified - actual rollers printed separately)
    for(i = [0:11]) {
        rotate([0, 0, i * 30])
        translate([65, 0, 0])
            rotate([45, 0, 0])
            cube([20, 6, 6], center=true);
    }
}

omni_wheel();

// Roller module (print 12x in TPU)
module roller() {
    rotate([0, 90, 0])
        cylinder(h=15, d=12);
}
"""
        scad_file = self.scad_dir / "omni_wheel.scad"
        scad_file.write_text(scad)
        return scad_file
    
    def generate_tracked_frame(self, side: str = "left"):
        """Generate tracked base frame"""
        scad = self._scad_header()
        scad += """
// TRACKED BASE FRAME
// Material: PLA_Carbon (high infill 70%+)
// Dimensions: 150mm wide × 600mm long

module tracked_frame() {
    // Main side plate
    difference() {
        linear_extrude(height=10)
            polygon([
                [0, 0],
                [0, 600],
                [80, 550],
                [100, 300],
                [100, 200],
                [80, 50],
                [0, 0]
            ]);
        
        // Drive sprocket hole (front)
        translate([60, 80, -5])
            cylinder(h=20, d=50);
        
        // Idler hole (rear)
        translate([40, 520, -5])
            cylinder(h=20, d=40);
        
        // Road wheel holes
        for(y = [150, 250, 350, 450]) {
            translate([50, y, -5])
                cylinder(h=20, d=35);
        }
        
        // Mounting holes for torso
        for(y = [300, 400]) {
            translate([20, y, -5])
                cylinder(h=20, d=8);
        }
        
        // Weight reduction (if not in stress areas)
        translate([30, 500, -5])
            cylinder(h=20, d=30);
    }
    
    // Bearing housings
    translate([60, 80, 10])
        cylinder(h=15, d=55);
    
    translate([40, 520, 10])
        cylinder(h=15, d=45);
}

tracked_frame();
"""
        scad_file = self.scad_dir / f"tracked_frame_{side}.scad"
        scad_file.write_text(scad)
        return scad_file
    
    def render_scad(self, scad_file: Path) -> bool:
        """Render SCAD file to STL using OpenSCAD"""
        stl_file = self.output_dir / (scad_file.stem + ".stl")
        
        cmd = [
            "openscad",
            "-o", str(stl_file),
            str(scad_file)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                return True
            else:
                print(f"  OpenSCAD error: {result.stderr[:200]}")
                return False
        except subprocess.TimeoutExpired:
            print(f"  Timeout rendering {scad_file.name}")
            return False
        except Exception as e:
            print(f"  Error: {e}")
            return False
    
    def generate_all(self):
        """Generate all modules"""
        print("="*60)
        print("CYLON LEG MODULE STL GENERATION")
        print("Using OpenSCAD for parametric CAD")
        print("="*60)
        
        modules = [
            ("Bipedal Hip (Left)", lambda: self.generate_bipedal_hip("left")),
            ("Bipedal Hip (Right)", lambda: self.generate_bipedal_hip("right")),
            ("Bipedal Thigh (Left)", lambda: self.generate_bipedal_thigh("left")),
            ("Bipedal Thigh (Right)", lambda: self.generate_bipedal_thigh("right")),
            ("Wheeled Foot (Left)", lambda: self.generate_wheeled_foot("left")),
            ("Wheeled Foot (Right)", lambda: self.generate_wheeled_foot("right")),
            ("Omni Wheel", self.generate_omni_wheel),
            ("Tracked Frame (Left)", lambda: self.generate_tracked_frame("left")),
            ("Tracked Frame (Right)", lambda: self.generate_tracked_frame("right")),
        ]
        
        generated = []
        stl_files = []
        
        # Generate SCAD files
        print("\n[Step 1] Generating OpenSCAD source files...")
        for name, func in modules:
            try:
                scad_file = func()
                print(f"  ✅ {name}: {scad_file.name}")
                generated.append(scad_file)
            except Exception as e:
                print(f"  ❌ {name}: {e}")
        
        # Render to STL
        print(f"\n[Step 2] Rendering to STL (this may take several minutes)...")
        for scad_file in generated:
            print(f"  Rendering: {scad_file.name}...")
            if self.render_scad(scad_file):
                stl_name = scad_file.stem + ".stl"
                print(f"    ✅ {stl_name}")
                stl_files.append(stl_name)
            else:
                print(f"    ⚠️  Failed (kept SCAD source)")
        
        print(f"\n{'='*60}")
        print(f"Generated {len(stl_files)} STL files")
        print(f"Location: {self.output_dir}")
        print(f"SCAD sources: {self.scad_dir}")
        print(f"{'='*60}")
        
        return stl_files

if __name__ == "__main__":
    output = Path("/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/production/stl_leg_modules")
    generator = OpenSCADLegGenerator(output)
    files = generator.generate_all()
    
    print("\n[Files Generated]")
    for f in sorted(files):
        print(f"  • {f}")
