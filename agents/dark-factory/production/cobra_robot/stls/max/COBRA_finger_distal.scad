// COBRA Finger Segment - DISTAL
// Length: 30.0mm, Width: 8mm

$fn = 32;

module finger_segment() {
    difference() {
        hull() {
            translate([0, 0, -4])
            cylinder(h=8, d=8, center=true);
            
            translate([30.0, 0, -4])
            cylinder(h=8, d=6.4, center=true);
        }
        
        // Tendon channel
        translate([15.0, 0, 0])
        rotate([0, 90, 0])
        cylinder(h=32.0, d=2.5, center=true);
        
        // Pivot holes
        translate([0, 0, 0])
        rotate([0, 90, 0])
        cylinder(h=10, d=2.5, center=true);
        
        translate([30.0, 0, 0])
        rotate([0, 90, 0])
        cylinder(h=10, d=2.5, center=true);
    }
}

finger_segment();
