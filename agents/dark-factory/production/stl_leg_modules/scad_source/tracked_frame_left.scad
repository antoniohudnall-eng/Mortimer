// CYLON Leg Module - OpenSCAD
// Material: PLA_Carbon or TPU_95A
// Infill: 50-70%
// Supports: Yes (where noted)

$fn = 100;  // Circle resolution

// Precision settings
$fs = 0.1;  // Minimum facet size
$fa = 5;    // Minimum angle


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
