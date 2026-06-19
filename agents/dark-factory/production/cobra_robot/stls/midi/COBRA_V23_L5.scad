// COBRA Vertebra - L5 V23
// Height: 25.0mm, OD: 45.0mm

$fn = 64;

difference() {
    // Outer cylinder
    cylinder(h=25.0, d=45.0, center=true);
    
    // Inner channel
    cylinder(h=27.0, d=22.5, center=true);

    // Battery cavity 1
    rotate([0, 0, 0])
    translate([16.875, 0, 0])
    rotate([90, 0, 0])
    cylinder(h=74.0, d=18.5, center=true);

    // Battery cavity 2
    rotate([0, 0, 180])
    translate([16.875, 0, 0])
    rotate([90, 0, 0])
    cylinder(h=74.0, d=18.5, center=true);

    // Pivot holes
    translate([0, 22.5, 9.5])
    rotate([90, 0, 0])
    cylinder(h=13.25, d=4, center=true);
    
    translate([0, 22.5, -9.5])
    rotate([90, 0, 0])
    cylinder(h=13.25, d=4, center=true);
}
