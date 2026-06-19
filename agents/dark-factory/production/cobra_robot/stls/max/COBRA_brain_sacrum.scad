// COBRA Brain Housing (Sacrum)

$fn = 32;

difference() {
    cube([80, 60, 25], center=true);
    
    // RPi5 cavity
    translate([0, -5, 2])
    cube([56, 85, 20], center=true);
    
    // Wiring channel
    rotate([0, 90, 0])
    cylinder(h=82, d=10, center=true);
    
    // Mounting holes
    for(x = [-35, 35]) {
        for(y = [-25, 25]) {
            translate([x, y, 0])
            cylinder(h=27, d=3, center=true);
        }
    }
}
