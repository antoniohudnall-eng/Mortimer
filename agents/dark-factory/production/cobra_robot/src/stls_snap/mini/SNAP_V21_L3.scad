// COBRA-Snap Vertebra - L3 V21
// Tool-free assembly with ball-and-socket joints

$fn = 64;

// Main vertebra body with integrated snap features
module vertebra() {
    difference() {
        union() {
            // Main cylinder
            cylinder(h=8.25, d=14.850000000000001, center=true);
            
            // Upper ball stud (for connection to vertebra above)
            translate([0, 0, 7.125])
            sphere(d=8);
            
            // Lower socket housing (for connection to vertebra below)
            translate([0, 0, -2.125])
            cylinder(h=6, d=16, center=true);
        }
        
        // Inner channel (for wiring)
        cylinder(h=18.25, d=7.425000000000001, center=true);
        
        // Ball stud hole (accepts ball from above)
        translate([0, 0, 6.125])
        sphere(d=8.4);  // 0.4mm clearance
        
        // Socket cavity (4 flex fingers)
        for(angle = [0, 90, 180, 270]) {
            rotate([0, 0, angle])
            translate([6, 0, -2.125])
            rotate([90, 0, 0])
            cylinder(h=3, d=4, center=true);
        }
        
        // Retention groove for ball (locking feature)
        translate([0, 0, 5.125])
        torus(d=8.5, d2=0.5);

        // Cable management channels
        for(angle = [0, 45, 90, 135, 180, 225, 270, 315]) {
            rotate([0, 0, angle])
            translate([5.2125, 0, 0])
            cylinder(h=8.25, d=3, center=true);
        }
    }
    
    // Flex fingers for socket (4x)
    for(angle = [0, 90, 180, 270]) {
        rotate([0, 0, angle])
        translate([4, 0, -2.125])
        flex_finger();
    }
}

module flex_finger() {
    // Living hinge flex finger
    difference() {
        union() {
            // Finger body
            translate([0, 0, 3])
            cylinder(h=6, d=3, center=true);
            
            // Retention bump
            translate([0, 0, 5])
            sphere(d=2);
        }
        
        // Flex gap
        translate([2, 0, 3])
        cube([4, 1, 7], center=true);
    }
}

module torus(d, d2) {
    rotate_extrude(angle=360)
    translate([d/2, 0])
    circle(d=d2);
}

vertebra();
