// CYLON Leg Module - OpenSCAD
// Material: PLA_Carbon or TPU_95A
// Infill: 50-70%
// Supports: Yes (where noted)

$fn = 100;  // Circle resolution

// Precision settings
$fs = 0.1;  // Minimum facet size
$fa = 5;    // Minimum angle


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
