// COBRA Hand Palm - RIGHT

$fn = 32;

module palm() {
    difference() {
        cube([60, 50, 15], center=true);
        
        // Motor cavities
        for(i = [0:4]) {
            translate([(i - 2) * 12, -20, 0])
            cylinder(h=17, d=12, center=true);
        }
        
        // Tendon channels
        for(i = [0:4]) {
            translate([(i - 2) * 12, 0, -6])
            rotate([90, 0, 0])
            cylinder(h=50, d=3, center=true);
        }
        
        // Mounting holes
        for(x = [-25, 25]) {
            for(y = [-20, 20]) {
                translate([x, y, 0])
                cylinder(h=17, d=3, center=true);
            }
        }
    }
}

palm();
