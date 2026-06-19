// COBRA Vertebra - T11 V17
// Height: 6.6000000000000005mm, OD: 13.200000000000001mm

$fn = 64;

difference() {
    // Outer cylinder
    cylinder(h=6.6000000000000005, d=13.200000000000001, center=true);
    
    // Inner channel
    cylinder(h=8.600000000000001, d=6.6000000000000005, center=true);

    // Solar panel cavity
    translate([0, 4.6000000000000005, 0])
    cube([50, 4, 30], center=true);

    // Pivot holes
    translate([0, 6.6000000000000005, 0.30000000000000027])
    rotate([90, 0, 0])
    cylinder(h=5.300000000000001, d=4, center=true);
    
    translate([0, 6.6000000000000005, -0.30000000000000027])
    rotate([90, 0, 0])
    cylinder(h=5.300000000000001, d=4, center=true);
}
