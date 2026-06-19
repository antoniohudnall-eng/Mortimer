#!/usr/bin/env python3
"""
COBRA-Snap - STL Generator with Snap-Fit Features
Tool-free assembly design
"""

import os


class SnapFitGenerator:
    """Generate STL files with integrated snap-fit joints"""
    
    def __init__(self, output_dir="stls_snap"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_snap_vertebra(self, vid, region, height, od, has_battery, has_solar):
        """Generate OpenSCAD for snap-fit vertebra"""
        
        id_d = od * 0.5
        
        scad = f"""// COBRA-Snap Vertebra - {region} V{vid}
// Tool-free assembly with ball-and-socket joints

$fn = 64;

// Main vertebra body with integrated snap features
module vertebra() {{
    difference() {{
        union() {{
            // Main cylinder
            cylinder(h={height}, d={od}, center=true);
            
            // Upper ball stud (for connection to vertebra above)
            translate([0, 0, {height/2 + 3}])
            sphere(d=8);
            
            // Lower socket housing (for connection to vertebra below)
            translate([0, 0, -{height/2 - 2}])
            cylinder(h=6, d=16, center=true);
        }}
        
        // Inner channel (for wiring)
        cylinder(h={height + 10}, d={id_d}, center=true);
        
        // Ball stud hole (accepts ball from above)
        translate([0, 0, {height/2 + 2}])
        sphere(d=8.4);  // 0.4mm clearance
        
        // Socket cavity (4 flex fingers)
        for(angle = [0, 90, 180, 270]) {{
            rotate([0, 0, angle])
            translate([6, 0, -{height/2 - 2}])
            rotate([90, 0, 0])
            cylinder(h=3, d=4, center=true);
        }}
        
        // Retention groove for ball (locking feature)
        translate([0, 0, {height/2 + 1}])
        torus(d=8.5, d2=0.5);
"""
        
        if has_battery:
            od_half = od / 2
            scad += f"""
        // Battery cartridge slot (slides in from side)
        translate([0, 0, 0])
        rotate([90, 0, 0])
        cube([40, 20, 25], center=true);
        
        // Battery locking tab cavity
        translate([0, -{od_half - 3}, 0])
        cube([15, 4, 8], center=true);
"""
        
        if has_solar:
            od_half = od / 2
            scad += f"""
        // Solar panel bayonet slots (L-shaped)
        for(angle = [45, 135, 225, 315]) {{
            rotate([0, 0, angle])
            translate([{od_half - 5}, 0, 0])
            rotate([0, 0, 30])  // L-shape rotation
            cube([20, 4, 4], center=true);
        }}
        
        // Solar panel alignment pins
        for(angle = [0, 90, 180, 270]) {{
            rotate([0, 0, angle])
            translate([{od_half - 10}, 0, 0])
            cylinder(h={height + 2}, d=3, center=true);
        }}
"""
        
        scad += f"""
        // Cable management channels
        for(angle = [0, 45, 90, 135, 180, 225, 270, 315]) {{
            rotate([0, 0, angle])
            translate([{id_d/2 + 1.5}, 0, 0])
            cylinder(h={height}, d=3, center=true);
        }}
    }}
    
    // Flex fingers for socket (4x)
    for(angle = [0, 90, 180, 270]) {{
        rotate([0, 0, angle])
        translate([4, 0, -{height/2 - 2}])
        flex_finger();
    }}
}}

module flex_finger() {{
    // Living hinge flex finger
    difference() {{
        union() {{
            // Finger body
            translate([0, 0, 3])
            cylinder(h=6, d=3, center=true);
            
            // Retention bump
            translate([0, 0, 5])
            sphere(d=2);
        }}
        
        // Flex gap
        translate([2, 0, 3])
        cube([4, 1, 7], center=true);
    }}
}}

module torus(d, d2) {{
    rotate_extrude(angle=360)
    translate([d/2, 0])
    circle(d=d2);
}}

vertebra();
"""
        return scad
    
    def generate_battery_cartridge(self):
        """Generate battery cartridge with snap-fit"""
        
        return """// COBRA-Snap Battery Cartridge
// Holds 2x 18650 cells, slides into vertebra

$fn = 32;

module battery_cartridge() {
    difference() {
        union() {
            // Main housing
            cube([40, 22, 66], center=true);
            
            // Locking tab (flexible)
            translate([0, -12, 10])
            rotate([-15, 0, 0])
            cube([15, 4, 8], center=true);
            
            // Grip texture
            for(i = [-30:10:30]) {
                translate([0, 11, i])
                cylinder(h=2, d=38, center=true);
            }
        }
        
        // Cell cavities (2x)
        translate([0, 0, 18])
        rotate([90, 0, 0])
        cylinder(h=24, d=19, center=true);
        
        translate([0, 0, -18])
        rotate([90, 0, 0])
        cylinder(h=24, d=19, center=true);
        
        // Contact pin holes
        translate([0, -10, 33])
        cylinder(h=6, d=4, center=true);
        
        translate([0, -10, -33])
        cylinder(h=6, d=4, center=true);
        
        // Ejector button access
        translate([0, 11, 10])
        cylinder(h=4, d=10, center=true);
    }
    
    // Spring contacts (simplified)
    for(z = [33, -33]) {
        translate([0, -10, z])
        difference() {
            cylinder(h=2, d=6, center=true);
            cylinder(h=3, d=4, center=true);
        }
    }
}

battery_cartridge();
"""
    
    def generate_solar_panel_mount(self):
        """Generate solar panel with bayonet mount"""
        
        return """// COBRA-Snap Solar Panel Module
// Bayonet twist-lock mounting

$fn = 32;

module solar_panel() {
    difference() {
        union() {
            // Panel body
            cube([60, 40, 4], center=true);
            
            // Bayonet lugs (4x)
            for(angle = [45, 135, 225, 315]) {
                rotate([0, 0, angle])
                translate([25, 0, 0])
                rotate([0, 0, 30])  // L-shape
                cube([12, 4, 6], center=true);
            }
            
            // Alignment pins (4x)
            for(angle = [0, 90, 180, 270]) {
                rotate([0, 0, angle])
                translate([20, 0, 4])
                cylinder(h=4, d=2.8, center=true);
            }
        }
        
        // Wire exit channel
        translate([0, 0, -2])
        cube([50, 3, 2], center=true);
    }
    
    // Solar cells (simplified)
    for(x = [-20:10:20]) {
        for(y = [-15:10:15]) {
            translate([x, y, 2])
            cube([9, 9, 0.5], center=true);
        }
    }
}

solar_panel();
"""
    
    def generate_snap_finger(self, seg_type, length):
        """Generate finger segment with dovetail joints"""
        
        width = {"proximal": 12, "middle": 10, "distal": 8}.get(seg_type, 10)
        
        return f"""// COBRA-Snap Finger Segment - {seg_type}
// Dovetail slide joints, no glue needed

$fn = 32;

module finger_segment() {{
    difference() {{
        union() {{
            // Main body
            hull() {{
                translate([0, 0, -4])
                cylinder(h=8, d={width}, center=true);
                
                translate([{length}, 0, -4])
                cylinder(h=8, d={width * 0.8}, center=true);
            }}
            
            // Male dovetail (proximal end)
            translate([0, 0, 0])
            rotate([90, 0, 0])
            linear_extrude(height={width + 2}, center=true)
            polygon(points=[[-3, 0], [3, 0], [2, 6], [-2, 6]]);
        }}
        
        // Female dovetail socket (distal end) - skip for distal
        """ + (f"""
        translate([{length}, 0, 0])
        rotate([90, 0, 0])
        linear_extrude(height={width * 0.8 + 2}, center=true)
        polygon(points=[[-3.2, -1], [3.2, -1], [2.2, 7], [-2.2, 7]]);
        """ if seg_type != "distal" else "") + f"""
        
        // Tendon channel
        translate([{length/2}, 0, 0])
        rotate([0, 90, 0])
        cylinder(h={length + 2}, d=2.5, center=true);
        
        // Quick-connect socket for tendon
        translate([5, 0, 0])
        sphere(d=4);
    }}
}}

finger_segment();
"""
    
    def generate_snap_palm(self, side):
        """Generate hand palm with integrated sockets"""
        
        return """// COBRA-Snap Hand Palm - """ + side.upper() + """
// Dovetail sockets for fingers, snap-fit wrist

$fn = 32;

module palm() {
    difference() {
        union() {
            // Main block
            cube([65, 50, 15], center=true);
            
            // Wrist socket (bayonet)
            translate([0, -27, 0])
            rotate([90, 0, 0])
            cylinder(h=8, d=25, center=true);
        }
        
        // Finger dovetail sockets (5x)
        for(i = [0:4]) {
            translate([{(i - 2) * 13}, 22, 0])
            rotate([90, 0, 0])
            linear_extrude(height=8, center=true)
            polygon(points=[[-3.2, -2], [3.2, -2], [2.2, 8], [-2.2, 8]]);
        }
        
        // Motor cavities (5x)
        for(i = [0:4]) {
            translate([{(i - 2) * 13}, -15, 0])
            cylinder(h=17, d=12, center=true);
        }
        
        // Tendon routing channels
        for(i = [0:4]) {
            translate([{(i - 2) * 13}, 0, -6])
            rotate([90, 0, 0])
            cylinder(h=45, d=3, center=true);
        }
        
        // Wrist bayonet slots
        for(angle = [0, 90, 180, 270]) {
            rotate([90, 0, angle])
            translate([10, 0, -30])
            rotate([0, 0, 45])
            cube([8, 3, 6], center=true);
        }
        
        // Eject buttons for fingers
        for(i = [0:4]) {
            translate([{(i - 2) * 13}, 26, 0])
            cube([8, 4, 10], center=true);
        }
    }
}

palm();
"""
    
    def generate_tendon_coupler(self):
        """Generate quick-connect tendon fitting"""
        
        return """// COBRA-Snap Tendon Coupler
// Ball-end quick connect for Dyneema line

$fn = 32;

module tendon_coupler() {
    difference() {
        union() {
            // Coupler body
            cylinder(h=10, d=8, center=true);
            
            // Ball end
            translate([0, 0, 7])
            sphere(d=6);
            
            // Strain relief
            translate([0, 0, -8])
            cylinder(h=6, d1=8, d2=4, center=true);
        }
        
        // Tendon channel
        translate([0, 0, -8])
        cylinder(h=20, d=1, center=true);
        
        // Crimp slot
        translate([0, 0, -10])
        cube([2, 8, 4], center=true);
    }
}

tendon_coupler();
"""
    
    def generate_wrist_joint(self):
        """Generate snap-fit wrist joint"""
        
        return """// COBRA-Snap Wrist Joint
// Bayonet twist-lock connection

$fn = 32;

module wrist_male() {
    // Male side (attached to forearm)
    difference() {
        union() {
            cylinder(h=15, d=20, center=true);
            
            // Bayonet lugs
            for(angle = [0, 90, 180, 270]) {
                rotate([0, 0, angle])
                translate([8, 0, 6])
                rotate([0, 0, 45])
                cube([6, 3, 4], center=true);
            }
        }
        
        // Wiring channel
        cylinder(h=20, d=12, center=true);
    }
}

module wrist_female() {
    // Female side (part of palm)
    difference() {
        cylinder(h=10, d=26, center=true);
        
        // Bayonet slots (L-shaped)
        for(angle = [0, 90, 180, 270]) {
            rotate([0, 0, angle])
            translate([8, 0, 0])
            rotate([0, 0, 45])
            cube([7, 4, 12], center=true);
        }
        
        // Alignment detent
        for(angle = [45, 135, 225, 315]) {
            rotate([0, 0, angle])
            translate([10, 0, 3])
            sphere(d=3);
        }
    }
}

// Preview both
translate([0, 20, 0])
wrist_male();

wrist_female();
"""
    
    def generate_all_files(self, model_size="midi"):
        """Generate all snap-fit STL files"""
        
        files = []
        scale = {"mini": 0.33, "midi": 1.0, "max": 2.0}.get(model_size, 1.0)
        
        # Vertebrae with snap joints
        # C1-C7
        for i in range(7):
            filename = f"SNAP_V{i:02d}_C{i+1}.scad"
            filepath = os.path.join(self.output_dir, model_size, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w') as f:
                f.write(self.generate_snap_vertebra(
                    i, f"C{i+1}", 15*scale, 30*scale, False, False
                ))
            files.append(filename)
        
        # T1-T12 with battery and solar
        for i in range(7, 19):
            filename = f"SNAP_V{i:02d}_T{i-6}.scad"
            filepath = os.path.join(self.output_dir, model_size, filename)
            
            has_bat = model_size != "mini"
            with open(filepath, 'w') as f:
                f.write(self.generate_snap_vertebra(
                    i, f"T{i-6}", 20*scale, 40*scale, has_bat, True
                ))
            files.append(filename)
        
        # L1-L5
        for i in range(19, 24):
            filename = f"SNAP_V{i:02d}_L{i-18}.scad"
            filepath = os.path.join(self.output_dir, model_size, filename)
            
            has_bat = model_size != "mini"
            with open(filepath, 'w') as f:
                f.write(self.generate_snap_vertebra(
                    i, f"L{i-18}", 25*scale, 45*scale, has_bat, False
                ))
            files.append(filename)
        
        # S1
        filename = "SNAP_V24_S1.scad"
        filepath = os.path.join(self.output_dir, model_size, filename)
        has_bat = model_size != "mini"
        with open(filepath, 'w') as f:
            f.write(self.generate_snap_vertebra(
                24, "S1", 30*scale, 50*scale, has_bat, False
            ))
        files.append(filename)
        
        # Battery cartridge
        if model_size != "mini":
            filename = "SNAP_battery_cartridge.scad"
            filepath = os.path.join(self.output_dir, model_size, filename)
            with open(filepath, 'w') as f:
                f.write(self.generate_battery_cartridge())
            files.append(filename)
        
        # Solar panel
        filename = "SNAP_solar_panel.scad"
        filepath = os.path.join(self.output_dir, model_size, filename)
        with open(filepath, 'w') as f:
            f.write(self.generate_solar_panel_mount())
        files.append(filename)
        
        # Fingers with dovetail
        for seg_type in ["proximal", "middle", "distal"]:
            length = {"proximal": 25, "middle": 20, "distal": 15}.get(seg_type, 20)
            filename = f"SNAP_finger_{seg_type}.scad"
            filepath = os.path.join(self.output_dir, model_size, filename)
            
            with open(filepath, 'w') as f:
                f.write(self.generate_snap_finger(seg_type, length * scale))
            files.append(filename)
        
        # Palms
        for side in ["left", "right"]:
            filename = f"SNAP_palm_{side}.scad"
            filepath = os.path.join(self.output_dir, model_size, filename)
            with open(filepath, 'w') as f:
                f.write(self.generate_snap_palm(side))
            files.append(filename)
        
        # Tendon coupler
        filename = "SNAP_tendon_coupler.scad"
        filepath = os.path.join(self.output_dir, model_size, filename)
        with open(filepath, 'w') as f:
            f.write(self.generate_tendon_coupler())
        files.append(filename)
        
        # Wrist joint
        filename = "SNAP_wrist_joint.scad"
        filepath = os.path.join(self.output_dir, model_size, filename)
        with open(filepath, 'w') as f:
            f.write(self.generate_wrist_joint())
        files.append(filename)
        
        return files


def main():
    print("=" * 70)
    print("🐍 COBRA-Snap - Tool-Free Assembly Generator")
    print("=" * 70)
    
    generator = SnapFitGenerator("stls_snap")
    
    for model_size in ["mini", "midi", "max"]:
        print("\n🔧 Generating " + model_size.upper() + " snap-fit files...")
        
        files = generator.generate_all_files(model_size)
        
        print("   Created " + str(len(files)) + " OpenSCAD files")
        print("   Location: stls_snap/" + model_size + "/")
        
        # Categorize
        vertebrae = [f for f in files if f.startswith("SNAP_V")]
        accessories = [f for f in files if "cartridge" in f or "solar" in f]
        hands = [f for f in files if "finger" in f or "palm" in f or "wrist" in f or "tendon" in f]
        
        print("      Vertebrae: " + str(len(vertebrae)) + " files")
        print("      Accessories: " + str(len(accessories)) + " files")
        print("      Hands: " + str(len(hands)) + " files")
    
    print("\n" + "=" * 70)
    print("✅ Snap-Fit Generation Complete")
    print("=" * 70)
    print("\nAssembly Features:")
    print("  • Ball-and-socket spine joints")
    print("  • Slide-in battery cartridges")
    print("  • Bayonet solar panels")
    print("  • Dovetail finger segments")
    print("  • Twist-lock wrist joints")
    print("\nAssembly Time: ~2 hours (no tools required)")


if __name__ == "__main__":
    main()
