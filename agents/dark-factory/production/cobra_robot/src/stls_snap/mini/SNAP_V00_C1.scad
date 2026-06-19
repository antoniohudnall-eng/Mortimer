// COBRA-Snap Vertebra - C1 V0
// Tool-free assembly with ball-and-socket joints

$fn = 64;

// Main vertebra body with integrated snap features
module vertebra() {
    difference() {
        union() {
            // Main cylinder
            cylinder(h=4.95, d=9.9, center=true);
            
            // Upper ball stud (for connection to vertebra above)
            translate([0, 0, 5.475])
            sphere(d=8);
            
            // Lower socket housing (for connection to vertebra below)
            translate([0, 0, -0.4750000000000001])
            cylinder(h=6, d=16, center=true);
        }
        
        // Inner channel (for wiring)
        cylinder(h=14.95, d=4.95, center=true);
        
        // Ball stud hole (accepts ball from above)
        translate([0, 0, 4.475])
        sphere(d=8.4);  // 0.4mm clearance
        
        // Socket cavity (4 flex fingers)
        for(angle = [0, 90, 180, 270]) {
            rotate([0, 0, angle])
            translate([6, 0, -0.4750000000000001])
            rotate([90, 0, 0])
            cylinder(h=3, d=4, center=true);
        }
        
        // Retention groove for ball (locking feature)
        translate([0, 0, 3.475])
        torus(d=8.5, d2=0.5);

        // Cable management channels
        for(angle = [0, 45, 90, 135, 180, 225, 270, 315]) {
            rotate([0, 0, angle])
            translate([3.975, 0, 0])
            cylinder(h=4.95, d=3, center=true);
        }
    }
    
    // Flex fingers for socket (4x)
    for(angle = [0, 90, 180, 270]) {
        rotate([0, 0, angle])
        translate([4, 0, -0.4750000000000001])
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
