// COBRA Vertebra - L3 V21
// Height: 50.0mm, OD: 90.0mm

$fn = 64;

difference() {
    // Outer cylinder
    cylinder(h=50.0, d=90.0, center=true);
    
    // Inner channel
    cylinder(h=52.0, d=45.0, center=true);

    // Battery cavity 1
    rotate([0, 0, 0])
    translate([33.75, 0, 0])
    rotate([90, 0, 0])
    cylinder(h=74.0, d=18.5, center=true);

    // Battery cavity 2
    rotate([0, 0, 180])
    translate([33.75, 0, 0])
    rotate([90, 0, 0])
    cylinder(h=74.0, d=18.5, center=true);

    // Pivot holes
    translate([0, 45.0, 22.0])
    rotate([90, 0, 0])
    cylinder(h=24.5, d=4, center=true);
    
    translate([0, 45.0, -22.0])
    rotate([90, 0, 0])
    cylinder(h=24.5, d=4, center=true);
}
