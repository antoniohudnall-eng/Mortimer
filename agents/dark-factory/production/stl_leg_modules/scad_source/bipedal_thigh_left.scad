// CYLON Leg Module - OpenSCAD
// Material: PLA_Carbon or TPU_95A
// Infill: 50-70%
// Supports: Yes (where noted)

$fn = 100;  // Circle resolution

// Precision settings
$fs = 0.1;  // Minimum facet size
$fa = 5;    // Minimum angle


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
