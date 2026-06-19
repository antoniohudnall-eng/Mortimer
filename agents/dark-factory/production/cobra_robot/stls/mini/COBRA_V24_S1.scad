// COBRA Vertebra - S1 V24
// Height: 9.9mm, OD: 16.5mm

$fn = 64;

difference() {
    // Outer cylinder
    cylinder(h=9.9, d=16.5, center=true);
    
    // Inner channel
    cylinder(h=11.9, d=8.25, center=true);

    // Pivot holes
    translate([0, 8.25, 1.9500000000000002])
    rotate([90, 0, 0])
    cylinder(h=6.125, d=4, center=true);
    
    translate([0, 8.25, -1.9500000000000002])
    rotate([90, 0, 0])
    cylinder(h=6.125, d=4, center=true);
}
