// COBRA Tendon Pulley - 20mm

$fn = 32;

module pulley() {
    difference() {
        cylinder(h=6, d=20, center=true);
        cylinder(h=8, d=2, center=true);
        
        // Groove
        rotate_extrude(angle=360) {
            translate([9.0, 0])
            circle(d=2);
        }
    }
}

pulley();
