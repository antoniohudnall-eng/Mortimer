// COBRA Vertebra - T6 V12
// Height: 40.0mm, OD: 80.0mm

$fn = 64;

difference() {
    // Outer cylinder
    cylinder(h=40.0, d=80.0, center=true);
    
    // Inner channel
    cylinder(h=42.0, d=40.0, center=true);

    // Battery cavity 1
    rotate([0, 0, 0])
    translate([30.0, 0, 0])
    rotate([90, 0, 0])
    cylinder(h=74.0, d=18.5, center=true);

    // Battery cavity 2
    rotate([0, 0, 180])
    translate([30.0, 0, 0])
    rotate([90, 0, 0])
    cylinder(h=74.0, d=18.5, center=true);

    // Solar panel cavity
    translate([0, 38.0, 0])
    cube([50, 4, 30], center=true);

    // Pivot holes
    translate([0, 40.0, 17.0])
    rotate([90, 0, 0])
    cylinder(h=22.0, d=4, center=true);
    
    translate([0, 40.0, -17.0])
    rotate([90, 0, 0])
    cylinder(h=22.0, d=4, center=true);
}
