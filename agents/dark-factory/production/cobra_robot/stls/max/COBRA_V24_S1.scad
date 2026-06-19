// COBRA Vertebra - S1 V24
// Height: 60.0mm, OD: 100.0mm

$fn = 64;

difference() {
    // Outer cylinder
    cylinder(h=60.0, d=100.0, center=true);
    
    // Inner channel
    cylinder(h=62.0, d=50.0, center=true);

    // Battery cavity 1
    rotate([0, 0, 0])
    translate([37.5, 0, 0])
    rotate([90, 0, 0])
    cylinder(h=58.0, d=14.5, center=true);

    // Battery cavity 2
    rotate([0, 0, 180])
    translate([37.5, 0, 0])
    rotate([90, 0, 0])
    cylinder(h=58.0, d=14.5, center=true);

    // Pivot holes
    translate([0, 50.0, 27.0])
    rotate([90, 0, 0])
    cylinder(h=27.0, d=4, center=true);
    
    translate([0, 50.0, -27.0])
    rotate([90, 0, 0])
    cylinder(h=27.0, d=4, center=true);
}
