// COBRA Vertebra - T5 V11
// Height: 20.0mm, OD: 40.0mm

$fn = 64;

difference() {
    // Outer cylinder
    cylinder(h=20.0, d=40.0, center=true);
    
    // Inner channel
    cylinder(h=22.0, d=20.0, center=true);

    // Battery cavity 1
    rotate([0, 0, 0])
    translate([15.0, 0, 0])
    rotate([90, 0, 0])
    cylinder(h=74.0, d=18.5, center=true);

    // Battery cavity 2
    rotate([0, 0, 180])
    translate([15.0, 0, 0])
    rotate([90, 0, 0])
    cylinder(h=74.0, d=18.5, center=true);

    // Solar panel cavity
    translate([0, 18.0, 0])
    cube([50, 4, 30], center=true);

    // Pivot holes
    translate([0, 20.0, 7.0])
    rotate([90, 0, 0])
    cylinder(h=12.0, d=4, center=true);
    
    translate([0, 20.0, -7.0])
    rotate([90, 0, 0])
    cylinder(h=12.0, d=4, center=true);
}
