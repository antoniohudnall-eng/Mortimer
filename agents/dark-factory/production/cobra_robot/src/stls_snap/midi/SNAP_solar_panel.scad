// COBRA-Snap Solar Panel Module
// Bayonet twist-lock mounting

$fn = 32;

module solar_panel() {
    difference() {
        union() {
            // Panel body
            cube([60, 40, 4], center=true);
            
            // Bayonet lugs (4x)
            for(angle = [45, 135, 225, 315]) {
                rotate([0, 0, angle])
                translate([25, 0, 0])
                rotate([0, 0, 30])  // L-shape
                cube([12, 4, 6], center=true);
            }
            
            // Alignment pins (4x)
            for(angle = [0, 90, 180, 270]) {
                rotate([0, 0, angle])
                translate([20, 0, 4])
                cylinder(h=4, d=2.8, center=true);
            }
        }
        
        // Wire exit channel
        translate([0, 0, -2])
        cube([50, 3, 2], center=true);
    }
    
    // Solar cells (simplified)
    for(x = [-20:10:20]) {
        for(y = [-15:10:15]) {
            translate([x, y, 2])
            cube([9, 9, 0.5], center=true);
        }
    }
}

solar_panel();
