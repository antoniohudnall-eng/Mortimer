// COBRA Vertebra - L1 V19
// Height: 8.25mm, OD: 14.850000000000001mm

$fn = 64;

difference() {
    // Outer cylinder
    cylinder(h=8.25, d=14.850000000000001, center=true);
    
    // Inner channel
    cylinder(h=10.25, d=7.425000000000001, center=true);

    // Pivot holes
    translate([0, 7.425000000000001, 1.125])
    rotate([90, 0, 0])
    cylinder(h=5.7125, d=4, center=true);
    
    translate([0, 7.425000000000001, -1.125])
    rotate([90, 0, 0])
    cylinder(h=5.7125, d=4, center=true);
}
