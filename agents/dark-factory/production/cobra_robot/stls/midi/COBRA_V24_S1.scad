// COBRA Vertebra - S1 V24
// Height: 30.0mm, OD: 50.0mm

$fn = 64;

difference() {
    // Outer cylinder
    cylinder(h=30.0, d=50.0, center=true);
    
    // Inner channel
    cylinder(h=32.0, d=25.0, center=true);

    // Battery cavity 1
    rotate([0, 0, 0])
    translate([18.75, 0, 0])
    rotate([90, 0, 0])
    cylinder(h=58.0, d=14.5, center=true);

    // Battery cavity 2
    rotate([0, 0, 180])
    translate([18.75, 0, 0])
    rotate([90, 0, 0])
    cylinder(h=58.0, d=14.5, center=true);

    // Pivot holes
    translate([0, 25.0, 12.0])
    rotate([90, 0, 0])
    cylinder(h=14.5, d=4, center=true);
    
    translate([0, 25.0, -12.0])
    rotate([90, 0, 0])
    cylinder(h=14.5, d=4, center=true);
}
