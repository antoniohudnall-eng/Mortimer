// COBRA-Snap Finger Segment - middle
// Dovetail slide joints, no glue needed

$fn = 32;

module finger_segment() {
    difference() {
        union() {
            // Main body
            hull() {
                translate([0, 0, -4])
                cylinder(h=8, d=10, center=true);
                
                translate([40.0, 0, -4])
                cylinder(h=8, d=8.0, center=true);
            }
            
            // Male dovetail (proximal end)
            translate([0, 0, 0])
            rotate([90, 0, 0])
            linear_extrude(height=12, center=true)
            polygon(points=[[-3, 0], [3, 0], [2, 6], [-2, 6]]);
        }
        
        // Female dovetail socket (distal end) - skip for distal
        
        translate([40.0, 0, 0])
        rotate([90, 0, 0])
        linear_extrude(height=10.0, center=true)
        polygon(points=[[-3.2, -1], [3.2, -1], [2.2, 7], [-2.2, 7]]);
        
        
        // Tendon channel
        translate([20.0, 0, 0])
        rotate([0, 90, 0])
        cylinder(h=42.0, d=2.5, center=true);
        
        // Quick-connect socket for tendon
        translate([5, 0, 0])
        sphere(d=4);
    }
}

finger_segment();
