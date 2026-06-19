// CYLON Leg Module - OpenSCAD
// Material: PLA_Carbon or TPU_95A
// Infill: 50-70%
// Supports: Yes (where noted)

$fn = 100;  // Circle resolution

// Precision settings
$fs = 0.1;  // Minimum facet size
$fa = 5;    // Minimum angle


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
