// COBRA-Snap Finger Segment - distal
// Dovetail slide joints, no glue needed

$fn = 32;

module finger_segment() {
    difference() {
        union() {
            // Main body
            hull() {
                translate([0, 0, -4])
                cylinder(h=8, d=8, center=true);
                
                translate([30.0, 0, -4])
                cylinder(h=8, d=6.4, center=true);
            }
            
            // Male dovetail (proximal end)
            translate([0, 0, 0])
            rotate([90, 0, 0])
            linear_extrude(height=10, center=true)
            polygon(points=[[-3, 0], [3, 0], [2, 6], [-2, 6]]);
        }
        
        // Female dovetail socket (distal end) - skip for distal
        
        
        // Tendon channel
        translate([15.0, 0, 0])
        rotate([0, 90, 0])
        cylinder(h=32.0, d=2.5, center=true);
        
        // Quick-connect socket for tendon
        translate([5, 0, 0])
        sphere(d=4);
    }
}

finger_segment();
