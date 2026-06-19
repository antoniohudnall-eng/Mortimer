// COBRA-Snap Wrist Joint
// Bayonet twist-lock connection

$fn = 32;

module wrist_male() {
    // Male side (attached to forearm)
    difference() {
        union() {
            cylinder(h=15, d=20, center=true);
            
            // Bayonet lugs
            for(angle = [0, 90, 180, 270]) {
                rotate([0, 0, angle])
                translate([8, 0, 6])
                rotate([0, 0, 45])
                cube([6, 3, 4], center=true);
            }
        }
        
        // Wiring channel
        cylinder(h=20, d=12, center=true);
    }
}

module wrist_female() {
    // Female side (part of palm)
    difference() {
        cylinder(h=10, d=26, center=true);
        
        // Bayonet slots (L-shaped)
        for(angle = [0, 90, 180, 270]) {
            rotate([0, 0, angle])
            translate([8, 0, 0])
            rotate([0, 0, 45])
            cube([7, 4, 12], center=true);
        }
        
        // Alignment detent
        for(angle = [45, 135, 225, 315]) {
            rotate([0, 0, angle])
            translate([10, 0, 3])
            sphere(d=3);
        }
    }
}

// Preview both
translate([0, 20, 0])
wrist_male();

wrist_female();
