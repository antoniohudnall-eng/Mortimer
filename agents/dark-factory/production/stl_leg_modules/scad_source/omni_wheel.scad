// CYLON Leg Module - OpenSCAD
// Material: PLA_Carbon or TPU_95A
// Infill: 50-70%
// Supports: Yes (where noted)

$fn = 100;  // Circle resolution

// Precision settings
$fs = 0.1;  // Minimum facet size
$fa = 5;    // Minimum angle


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
