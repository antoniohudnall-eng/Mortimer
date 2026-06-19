// COBRA Spine Joint Gimbal

$fn = 32;

difference() {
    rotate([90, 0, 0])
    cylinder(h=12, d=20, center=true);
    
    rotate([90, 0, 0])
    cylinder(h=14, d=16, center=true);
    
    rotate([0, 90, 0])
    cylinder(h=22, d=4, center=true);
    
    rotate([90, 0, 0])
    cylinder(h=16, d=2.5, center=true);
}
