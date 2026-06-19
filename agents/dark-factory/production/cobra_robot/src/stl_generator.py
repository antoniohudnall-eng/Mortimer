#!/usr/bin/env python3
"""
COBRA Robot - STL File Generator
Generates all 3D printable parts for snake spine robot
"""

import os


class STLOpenscadExporter:
    """Generate OpenSCAD files that can be exported to STL"""
    
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_vertebra(self, vid, region, height, od, has_battery, has_solar):
        """Generate OpenSCAD code for a vertebra"""
        id_d = od * 0.5
        wall = (od - id_d) / 2
        
        cell_dia = 18.5 if region.startswith("T") or region.startswith("L") else 14.5
        
        scad = f"""// COBRA Vertebra - {region} V{vid}
// Height: {height}mm, OD: {od}mm

$fn = 64;

difference() {{
    // Outer cylinder
    cylinder(h={height}, d={od}, center=true);
    
    // Inner channel
    cylinder(h={height + 2}, d={id_d}, center=true);
"""
        
        if has_battery:
            for i in range(2):
                angle = i * 180
                scad += f"""
    // Battery cavity {i+1}
    rotate([0, 0, {angle}])
    translate([{(od + id_d)/4}, 0, 0])
    rotate([90, 0, 0])
    cylinder(h={cell_dia * 4}, d={cell_dia}, center=true);
"""
        
        if has_solar:
            scad += f"""
    // Solar panel cavity
    translate([0, {od/2 - 2}, 0])
    cube([50, 4, 30], center=true);
"""
        
        scad += f"""
    // Pivot holes
    translate([0, {od/2}, {height/2 - 3}])
    rotate([90, 0, 0])
    cylinder(h={wall + 2}, d=4, center=true);
    
    translate([0, {od/2}, {-height/2 + 3}])
    rotate([90, 0, 0])
    cylinder(h={wall + 2}, d=4, center=true);
}}
"""
        return scad
    
    def generate_finger_segment(self, seg_type, length):
        """Generate finger segment"""
        width = {"proximal": 12, "middle": 10, "distal": 8}.get(seg_type, 10)
        
        return f"""// COBRA Finger Segment - {seg_type.upper()}
// Length: {length}mm, Width: {width}mm

$fn = 32;

module finger_segment() {{
    difference() {{
        hull() {{
            translate([0, 0, -4])
            cylinder(h=8, d={width}, center=true);
            
            translate([{length}, 0, -4])
            cylinder(h=8, d={width * 0.8}, center=true);
        }}
        
        // Tendon channel
        translate([{length/2}, 0, 0])
        rotate([0, 90, 0])
        cylinder(h={length + 2}, d=2.5, center=true);
        
        // Pivot holes
        translate([0, 0, 0])
        rotate([0, 90, 0])
        cylinder(h={width + 2}, d=2.5, center=true);
        
        translate([{length}, 0, 0])
        rotate([0, 90, 0])
        cylinder(h={width + 2}, d=2.5, center=true);
    }}
}}

finger_segment();
"""
    
    def generate_palm(self, side):
        """Generate palm"""
        return """// COBRA Hand Palm - """ + side.upper() + """

$fn = 32;

module palm() {
    difference() {
        cube([60, 50, 15], center=true);
        
        // Motor cavities
        for(i = [0:4]) {
            translate([(i - 2) * 12, -20, 0])
            cylinder(h=17, d=12, center=true);
        }
        
        // Tendon channels
        for(i = [0:4]) {
            translate([(i - 2) * 12, 0, -6])
            rotate([90, 0, 0])
            cylinder(h=50, d=3, center=true);
        }
        
        // Mounting holes
        for(x = [-25, 25]) {
            for(y = [-20, 20]) {
                translate([x, y, 0])
                cylinder(h=17, d=3, center=true);
            }
        }
    }
}

palm();
"""
    
    def generate_pulley(self, diameter):
        """Generate pulley"""
        return f"""// COBRA Tendon Pulley - {diameter}mm

$fn = 32;

module pulley() {{
    difference() {{
        cylinder(h=6, d={diameter}, center=true);
        cylinder(h=8, d=2, center=true);
        
        // Groove
        rotate_extrude(angle=360) {{
            translate([{diameter/2 - 1}, 0])
            circle(d=2);
        }}
    }}
}}

pulley();
"""
    
    def generate_tendon_guide(self, length):
        """Generate tendon guide"""
        return f"""// COBRA Tendon Guide - {length}mm

$fn = 16;

difference() {{
    cylinder(h={length}, d=4, center=true);
    cylinder(h={length + 2}, d=2.5, center=true);
}}
"""
    
    def generate_joint_gimbal(self):
        """Generate joint gimbal"""
        return """// COBRA Spine Joint Gimbal

$fn = 32;

difference() {
    rotate([90, 0, 0])
    cylinder(h=12, d=20, center=true);
    
    rotate([90, 0, 0])
    cylinder(h=14, d=16, center=true);
    
    rotate([0, 90, 0])
    cylinder(h=22, d=4, center=true);
    
    rotate([90, 0, 0])
    cylinder(h=16, d=2.5, center=true);
}
"""
    
    def generate_brain_case(self):
        """Generate brain housing"""
        return """// COBRA Brain Housing (Sacrum)

$fn = 32;

difference() {
    cube([80, 60, 25], center=true);
    
    // RPi5 cavity
    translate([0, -5, 2])
    cube([56, 85, 20], center=true);
    
    // Wiring channel
    rotate([0, 90, 0])
    cylinder(h=82, d=10, center=true);
    
    // Mounting holes
    for(x = [-35, 35]) {
        for(y = [-25, 25]) {
            translate([x, y, 0])
            cylinder(h=27, d=3, center=true);
        }
    }
}
"""
    
    def generate_all_files(self, model_size):
        """Generate all STL files for COBRA robot"""
        files = []
        
        scale = {"mini": 0.33, "midi": 1.0, "max": 2.0}.get(model_size, 1.0)
        
        # Vertebrae
        # C1-C7 (cervical)
        for i in range(7):
            filename = f"COBRA_V{i:02d}_C{i+1}.scad"
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w') as f:
                f.write(self.generate_vertebra(i, f"C{i+1}", 15*scale, 30*scale, False, False))
            files.append(filename)
        
        # T1-T12 (thoracic) - with batteries and solar
        for i in range(7, 19):
            filename = f"COBRA_V{i:02d}_T{i-6}.scad"
            filepath = os.path.join(self.output_dir, filename)
            has_bat = model_size != "mini"
            with open(filepath, 'w') as f:
                f.write(self.generate_vertebra(i, f"T{i-6}", 20*scale, 40*scale, has_bat, True))
            files.append(filename)
        
        # L1-L5 (lumbar) - with batteries
        for i in range(19, 24):
            filename = f"COBRA_V{i:02d}_L{i-18}.scad"
            filepath = os.path.join(self.output_dir, filename)
            has_bat = model_size != "mini"
            with open(filepath, 'w') as f:
                f.write(self.generate_vertebra(i, f"L{i-18}", 25*scale, 45*scale, has_bat, False))
            files.append(filename)
        
        # S1 (sacrum)
        filename = "COBRA_V24_S1.scad"
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            f.write(self.generate_vertebra(24, "S1", 30*scale, 50*scale, has_bat, False))
        files.append(filename)
        
        # Fingers
        for seg_type in ["proximal", "middle", "distal"]:
            length = {"proximal": 25, "middle": 20, "distal": 15}.get(seg_type, 20)
            filename = f"COBRA_finger_{seg_type}.scad"
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w') as f:
                f.write(self.generate_finger_segment(seg_type, length * scale))
            files.append(filename)
        
        # Palms
        for side in ["left", "right"]:
            filename = f"COBRA_palm_{side}.scad"
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w') as f:
                f.write(self.generate_palm(side))
            files.append(filename)
        
        # Pulleys
        for dia in [10, 15, 20]:
            filename = f"COBRA_pulley_{dia}mm.scad"
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w') as f:
                f.write(self.generate_pulley(dia))
            files.append(filename)
        
        # Tendon guides
        for length in [50, 100, 200]:
            filename = f"COBRA_guide_{length}mm.scad"
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w') as f:
                f.write(self.generate_tendon_guide(length * scale))
            files.append(filename)
        
        # Joint gimbals
        for i in range(24):
            filename = f"COBRA_gimbal_{i:02d}.scad"
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w') as f:
                f.write(self.generate_joint_gimbal())
            files.append(filename)
        
        # Brain case
        filename = "COBRA_brain_sacrum.scad"
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            f.write(self.generate_brain_case())
        files.append(filename)
        
        return files


def main():
    print("=" * 70)
    print("🐍 COBRA Robot - STL Generator")
    print("=" * 70)
    
    output_base = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/production/cobra_robot/stls"
    
    for model_size in ["mini", "midi", "max"]:
        print("\n📐 Generating " + model_size.upper() + " model files...")
        
        model_dir = os.path.join(output_base, model_size)
        generator = STLOpenscadExporter(model_dir)
        files = generator.generate_all_files(model_size)
        
        print("   Created " + str(len(files)) + " OpenSCAD files")
        print("   Location: " + model_dir)
    
    print("\n" + "=" * 70)
    print("✅ STL Generation Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
