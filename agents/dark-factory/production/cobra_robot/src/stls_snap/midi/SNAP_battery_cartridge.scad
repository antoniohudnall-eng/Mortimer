// COBRA-Snap Battery Cartridge
// Holds 2x 18650 cells, slides into vertebra

$fn = 32;

module battery_cartridge() {
    difference() {
        union() {
            // Main housing
            cube([40, 22, 66], center=true);
            
            // Locking tab (flexible)
            translate([0, -12, 10])
            rotate([-15, 0, 0])
            cube([15, 4, 8], center=true);
            
            // Grip texture
            for(i = [-30:10:30]) {
                translate([0, 11, i])
                cylinder(h=2, d=38, center=true);
            }
        }
        
        // Cell cavities (2x)
        translate([0, 0, 18])
        rotate([90, 0, 0])
        cylinder(h=24, d=19, center=true);
        
        translate([0, 0, -18])
        rotate([90, 0, 0])
        cylinder(h=24, d=19, center=true);
        
        // Contact pin holes
        translate([0, -10, 33])
        cylinder(h=6, d=4, center=true);
        
        translate([0, -10, -33])
        cylinder(h=6, d=4, center=true);
        
        // Ejector button access
        translate([0, 11, 10])
        cylinder(h=4, d=10, center=true);
    }
    
    // Spring contacts (simplified)
    for(z = [33, -33]) {
        translate([0, -10, z])
        difference() {
            cylinder(h=2, d=6, center=true);
            cylinder(h=3, d=4, center=true);
        }
    }
}

battery_cartridge();
