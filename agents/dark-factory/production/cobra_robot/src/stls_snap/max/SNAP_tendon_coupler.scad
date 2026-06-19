// COBRA-Snap Tendon Coupler
// Ball-end quick connect for Dyneema line

$fn = 32;

module tendon_coupler() {
    difference() {
        union() {
            // Coupler body
            cylinder(h=10, d=8, center=true);
            
            // Ball end
            translate([0, 0, 7])
            sphere(d=6);
            
            // Strain relief
            translate([0, 0, -8])
            cylinder(h=6, d1=8, d2=4, center=true);
        }
        
        // Tendon channel
        translate([0, 0, -8])
        cylinder(h=20, d=1, center=true);
        
        // Crimp slot
        translate([0, 0, -10])
        cube([2, 8, 4], center=true);
    }
}

tendon_coupler();
