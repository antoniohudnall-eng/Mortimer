// COBRA Vertebra - C2 V1
// Height: 4.95mm, OD: 9.9mm

$fn = 64;

difference() {
    // Outer cylinder
    cylinder(h=4.95, d=9.9, center=true);
    
    // Inner channel
    cylinder(h=6.95, d=4.95, center=true);

    // Pivot holes
    translate([0, 4.95, -0.5249999999999999])
    rotate([90, 0, 0])
    cylinder(h=4.475, d=4, center=true);
    
    translate([0, 4.95, 0.5249999999999999])
    rotate([90, 0, 0])
    cylinder(h=4.475, d=4, center=true);
}
