// COBRA Vertebra - C7 V6
// Height: 30.0mm, OD: 60.0mm

$fn = 64;

difference() {
    // Outer cylinder
    cylinder(h=30.0, d=60.0, center=true);
    
    // Inner channel
    cylinder(h=32.0, d=30.0, center=true);

    // Pivot holes
    translate([0, 30.0, 12.0])
    rotate([90, 0, 0])
    cylinder(h=17.0, d=4, center=true);
    
    translate([0, 30.0, -12.0])
    rotate([90, 0, 0])
    cylinder(h=17.0, d=4, center=true);
}
