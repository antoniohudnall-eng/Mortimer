// COBRA Finger Segment - PROXIMAL
// Length: 25.0mm, Width: 12mm

$fn = 32;

module finger_segment() {
    difference() {
        hull() {
            translate([0, 0, -4])
            cylinder(h=8, d=12, center=true);
            
            translate([25.0, 0, -4])
            cylinder(h=8, d=9.600000000000001, center=true);
        }
        
        // Tendon channel
        translate([12.5, 0, 0])
        rotate([0, 90, 0])
        cylinder(h=27.0, d=2.5, center=true);
        
        // Pivot holes
        translate([0, 0, 0])
        rotate([0, 90, 0])
        cylinder(h=14, d=2.5, center=true);
        
        translate([25.0, 0, 0])
        rotate([0, 90, 0])
        cylinder(h=14, d=2.5, center=true);
    }
}

finger_segment();
