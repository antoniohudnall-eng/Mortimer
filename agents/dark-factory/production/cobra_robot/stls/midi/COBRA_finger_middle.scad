// COBRA Finger Segment - MIDDLE
// Length: 20.0mm, Width: 10mm

$fn = 32;

module finger_segment() {
    difference() {
        hull() {
            translate([0, 0, -4])
            cylinder(h=8, d=10, center=true);
            
            translate([20.0, 0, -4])
            cylinder(h=8, d=8.0, center=true);
        }
        
        // Tendon channel
        translate([10.0, 0, 0])
        rotate([0, 90, 0])
        cylinder(h=22.0, d=2.5, center=true);
        
        // Pivot holes
        translate([0, 0, 0])
        rotate([0, 90, 0])
        cylinder(h=12, d=2.5, center=true);
        
        translate([20.0, 0, 0])
        rotate([0, 90, 0])
        cylinder(h=12, d=2.5, center=true);
    }
}

finger_segment();
