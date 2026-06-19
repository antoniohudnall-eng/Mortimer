// COBRA-Snap Hand Palm - RIGHT
// Dovetail sockets for fingers, snap-fit wrist

$fn = 32;

module palm() {
    difference() {
        union() {
            // Main block
            cube([65, 50, 15], center=true);
            
            // Wrist socket (bayonet)
            translate([0, -27, 0])
            rotate([90, 0, 0])
            cylinder(h=8, d=25, center=true);
        }
        
        // Finger dovetail sockets (5x)
        for(i = [0:4]) {
            translate([{(i - 2) * 13}, 22, 0])
            rotate([90, 0, 0])
            linear_extrude(height=8, center=true)
            polygon(points=[[-3.2, -2], [3.2, -2], [2.2, 8], [-2.2, 8]]);
        }
        
        // Motor cavities (5x)
        for(i = [0:4]) {
            translate([{(i - 2) * 13}, -15, 0])
            cylinder(h=17, d=12, center=true);
        }
        
        // Tendon routing channels
        for(i = [0:4]) {
            translate([{(i - 2) * 13}, 0, -6])
            rotate([90, 0, 0])
            cylinder(h=45, d=3, center=true);
        }
        
        // Wrist bayonet slots
        for(angle = [0, 90, 180, 270]) {
            rotate([90, 0, angle])
            translate([10, 0, -30])
            rotate([0, 0, 45])
            cube([8, 3, 6], center=true);
        }
        
        // Eject buttons for fingers
        for(i = [0:4]) {
            translate([{(i - 2) * 13}, 26, 0])
            cube([8, 4, 10], center=true);
        }
    }
}

palm();
