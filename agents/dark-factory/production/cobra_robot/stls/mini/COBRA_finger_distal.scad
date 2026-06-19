// COBRA Finger Segment - DISTAL
// Length: 4.95mm, Width: 8mm

$fn = 32;

module finger_segment() {
    difference() {
        hull() {
            translate([0, 0, -4])
            cylinder(h=8, d=8, center=true);
            
            translate([4.95, 0, -4])
            cylinder(h=8, d=6.4, center=true);
        }
        
        // Tendon channel
        translate([2.475, 0, 0])
        rotate([0, 90, 0])
        cylinder(h=6.95, d=2.5, center=true);
        
        // Pivot holes
        translate([0, 0, 0])
        rotate([0, 90, 0])
        cylinder(h=10, d=2.5, center=true);
        
        translate([4.95, 0, 0])
        rotate([0, 90, 0])
        cylinder(h=10, d=2.5, center=true);
    }
}

finger_segment();
