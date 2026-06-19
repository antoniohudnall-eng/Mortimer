// COBRA Vertebra - C7 V6
// Height: 15.0mm, OD: 30.0mm

$fn = 64;

difference() {
    // Outer cylinder
    cylinder(h=15.0, d=30.0, center=true);
    
    // Inner channel
    cylinder(h=17.0, d=15.0, center=true);

    // Pivot holes
    translate([0, 15.0, 4.5])
    rotate([90, 0, 0])
    cylinder(h=9.5, d=4, center=true);
    
    translate([0, 15.0, -4.5])
    rotate([90, 0, 0])
    cylinder(h=9.5, d=4, center=true);
}
