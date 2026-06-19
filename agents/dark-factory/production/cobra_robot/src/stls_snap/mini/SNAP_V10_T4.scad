// COBRA-Snap Vertebra - T4 V10
// Tool-free assembly with ball-and-socket joints

$fn = 64;

// Main vertebra body with integrated snap features
module vertebra() {
    difference() {
        union() {
            // Main cylinder
            cylinder(h=6.6000000000000005, d=13.200000000000001, center=true);
            
            // Upper ball stud (for connection to vertebra above)
            translate([0, 0, 6.300000000000001])
            sphere(d=8);
            
            // Lower socket housing (for connection to vertebra below)
            translate([0, 0, -1.3000000000000003])
            cylinder(h=6, d=16, center=true);
        }
        
        // Inner channel (for wiring)
        cylinder(h=16.6, d=6.6000000000000005, center=true);
        
        // Ball stud hole (accepts ball from above)
        translate([0, 0, 5.300000000000001])
        sphere(d=8.4);  // 0.4mm clearance
        
        // Socket cavity (4 flex fingers)
        for(angle = [0, 90, 180, 270]) {
            rotate([0, 0, angle])
            translate([6, 0, -1.3000000000000003])
            rotate([90, 0, 0])
            cylinder(h=3, d=4, center=true);
        }
        
        // Retention groove for ball (locking feature)
        translate([0, 0, 4.300000000000001])
        torus(d=8.5, d2=0.5);

        // Solar panel bayonet slots (L-shaped)
        for(angle = [45, 135, 225, 315]) {
            rotate([0, 0, angle])
            translate([1.6000000000000005, 0, 0])
            rotate([0, 0, 30])  // L-shape rotation
            cube([20, 4, 4], center=true);
        }
        
        // Solar panel alignment pins
        for(angle = [0, 90, 180, 270]) {
            rotate([0, 0, angle])
            translate([-3.3999999999999995, 0, 0])
            cylinder(h=8.600000000000001, d=3, center=true);
        }

        // Cable management channels
        for(angle = [0, 45, 90, 135, 180, 225, 270, 315]) {
            rotate([0, 0, angle])
            translate([4.800000000000001, 0, 0])
            cylinder(h=6.6000000000000005, d=3, center=true);
        }
    }
    
    // Flex fingers for socket (4x)
    for(angle = [0, 90, 180, 270]) {
        rotate([0, 0, angle])
        translate([4, 0, -1.3000000000000003])
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
