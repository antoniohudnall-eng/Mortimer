// Milk Man Action Figure - OpenSCAD Parametric Design
// Based on CYLON-PRIME chassis
// Modified for heroic proportions
// Project 5912 - AOCROS Toys

// === CONFIGURATION ===
$fn = 50;           // Smoothness
scale_factor = 1.0;  // Adjust for 1:6 scale (12 inches)
part_mode = "preview";  // Options: "head", "torso", "arm", "leg", "accessory_churn", "preview"

// === MILK MAN COLORS ===
mm_primary = [0.95, 0.95, 0.95];     // White
mm_secondary = [0.85, 0.75, 0.2];  // Gold
mm_accent = [0.2, 0.4, 0.8];        // Blue

// === DIMENSIONS (mm) ===
head_height = 35;
head_width = 30;
torso_height = 45;
arm_length = 60;
leg_length = 80;

// === HELPER MODULES ===

// Milk Bottle Shape
module milk_bottle(scale=1) {
    scale([scale, scale, scale]) {
        // Body
        cylinder(h=20, d1=10, d2=12, center=false);
        // Neck
        translate([0, 0, 20])
            cylinder(h=8, d=6, center=false);
        // Cap
        translate([0, 0, 28])
            cylinder(h=4, d=8, center=false);
    }
}

// MM Logo
module mm_logo(size=10, depth=2) {
    linear_extrude(height=depth) {
        text("MM", size=size, font="Impact", halign="center", valign="center");
    }
}

// Joint Peg (ball and socket)
module joint_peg(diameter=8, length=10) {
    cylinder(h=length, d=diameter, center=true);
    sphere(d=diameter+2);
}

// Joint Socket
module joint_socket(diameter=10, depth=8) {
    difference() {
        sphere(d=diameter+4);
        sphere(d=diameter);
    }
}

// === HEAD MODULES ===

module milkman_helmet_front() {
    difference() {
        // Base helmet
        intersection() {
            sphere(d=head_width);
            translate([0, 0, -5])
                cube([head_width, head_width, head_height], center=true);
        }
        
        // Visor cutout
        translate([0, head_width/2-5, 5])
            cube([20, 10, 12], center=true);
        
        // Face opening
        translate([0, -5, -5])
            cube([22, 20, 25], center=true);
    }
    
    // MM Logo on forehead
    translate([-6, 12, 15])
        rotate([90, 0, 0])
        mm_logo(size=6, depth=1.5);
    
    // Milk bottle crown decoration
    translate([0, 0, head_width/2-3])
        rotate([90, 0, 0])
        milk_bottle(scale=0.4);
}

module milkman_helmet_back() {
    difference() {
        intersection() {
            sphere(d=head_width);
            translate([0, 0, -5])
                cube([head_width, head_width, head_height], center=true);
        }
        
        // Remove front half
        translate([0, 8, 0])
            cube([head_width+2, head_width, head_height+2], center=true);
    }
    
    // Cape attachment point
    translate([0, -12, 0])
        cylinder(h=5, d=8, center=true);
}

module milkman_face() {
    // Jaw/chin
    translate([0, 0, -head_height/4])
        scale([1, 0.8, 0.6])
            sphere(d=head_width-4);
    
    // Eyes
    translate([-6, 8, 5])
        sphere(d=6);
    translate([6, 8, 5])
        sphere(d=6);
    
    // Mouth
    translate([0, 10, -2])
        rotate([90, 0, 0])
        scale([1, 0.3, 1])
            cylinder(h=3, d=12, center=true);
}

// === TORSO MODULES ===

module milkman_chest_front() {
    difference() {
        // Base chest
        intersection() {
            sphere(d=50);
            translate([0, 0, 0])
                cube([40, 35, 50], center=true);
        }
        
        // MM logo recess (raised)
        translate([0, 17, 15])
            rotate([90, 0, 0])
            scale([1.2, 1.2, 1])
            mm_logo(size=10, depth=2);
    }
    
    // Pecs
    translate([-10, 15, 10])
        scale([1, 0.5, 0.8])
            sphere(d=18);
    translate([10, 15, 10])
        scale([1, 0.5, 0.8])
            sphere(d=18);
    
    // Abs ridges
    for(i=[0:2]) {
        translate([0, 15, -5-i*8])
            scale([0.8, 0.3, 0.2])
                sphere(d=20);
    }
}

module milkman_chest_back() {
    difference() {
        intersection() {
            sphere(d=48);
            translate([0, -5, 0])
                cube([38, 30, 48], center=true);
        }
        
        // Cape mount hole
        translate([0, -18, 15])
            cylinder(h=5, d=6, center=true);
    }
    
    // Cape attachment points (4 magnets)
    for(pos=[[-12, -18, 20], [12, -18, 20], [-12, -18, 5], [12, -18, 5]]) {
        translate(pos)
            cylinder(h=3, d=6, center=true);
    }
}

// === ARM MODULES ===

module milkman_upper_arm() {
    // Shoulder
    translate([0, 0, 20])
        sphere(d=22);
    
    // Bicep
    translate([0, 0, 0])
        cylinder(h=30, d1=18, d2=16, center=true);
    
    // MM logo on shoulder
    translate([0, 10, 25])
        rotate([90, 0, 0])
        mm_logo(size=5, depth=1);
    
    // Wrist peg
    translate([0, 0, -20])
        joint_peg(diameter=8, length=8);
}

module milkman_forearm() {
    // Forearm
    cylinder(h=25, d1=14, d2=12, center=true);
    
    // Wrist socket
    translate([0, 0, 15])
        joint_socket(diameter=10, depth=8);
    
    // Hand (simplified)
    translate([0, 0, -15])
        scale([1, 0.6, 1.2])
            sphere(d=12);
}

// === LEG MODULES ===

module milkman_thigh() {
    // Hip joint
    translate([0, 0, 30])
        sphere(d=24);
    
    // Thigh
    translate([0, 0, 10])
        cylinder(h=25, d1=20, d2=18, center=true);
    
    // Knee
    translate([0, 0, -8])
        sphere(d=18);
    
    // MM logo on hip
    translate([10, 0, 25])
        rotate([0, 90, 0])
        mm_logo(size=4, depth=1);
}

module milkman_shin() {
    // Shin
    cylinder(h=30, d1=16, d2=14, center=true);
    
    // Ankle peg
    translate([0, 0, -18])
        joint_peg(diameter=8, length=6);
    
    // Boot
    translate([0, 0, -25])
        union() {
            cylinder(h=15, d=16, center=true);
            // Boot detail
            translate([0, 8, -5])
                cube([14, 6, 12], center=true);
        }
}

// === ACCESSORIES ===

module churn_staff() {
    // Staff shaft
    cylinder(h=150, d=8, center=true);
    
    // Handle (churn mechanism)
    translate([0, 0, 70])
        rotate([90, 0, 0])
        difference() {
            cylinder(h=30, d=25, center=true);
            cylinder(h=32, d=8, center=true);
        }
    
    // Churn crank handle
    translate([15, 0, 70])
        rotate([90, 0, 0])
        cylinder(h=15, d=6, center=true);
    
    // Bottom weight
    translate([0, 0, -70])
        sphere(d=20);
    
    // Milk bottle decorations (x3)
    for(angle=[0:120:240]) {
        rotate([0, 0, angle])
            translate([12, 0, 60])
                milk_bottle(scale=0.6);
    }
}

module milk_bottle_acessory() {
    milk_bottle(scale=0.8);
    // Connector peg on base
    translate([0, 0, -8])
        cylinder(h=5, d=4, center=true);
}

module display_base() {
    // Street base
    difference() {
        cube([120, 80, 10], center=true);
        // Cobblestone texture (grid pattern)
        for(x=[-50:20:50])
            for(y=[-30:20:30])
                translate([x+10, y+10, 4])
                    cube([18, 18, 3], center=true);
    }
    
    // Peg for figure
    translate([0, 0, 8])
        cylinder(h=8, d=10, center=true);
    
    // "Dairyopolis" text
    translate([0, -30, 5])
        linear_extrude(height=3)
            text("DAIRYOPOLIS", size=8, font="Impact", halign="center");
    
    // Overturned cheese cart (decorative)
    translate([30, 15, 5])
        rotate([0, 20, 45])
            cube([30, 20, 15], center=true);
}

// === ASSEMBLY PREVIEW ===

module full_assembly() {
    // Head
    translate([0, 0, 120])
        milkman_helmet_front();
    
    // Torso
    translate([0, 0, 80])
        milkman_chest_front();
    
    // Arms (angled)
    translate([-25, 0, 90])
        rotate([0, 0, 20])
            milkman_upper_arm();
    translate([25, 0, 90])
        rotate([0, 0, -20])
            milkman_upper_arm();
    
    // Legs (stance)
    translate([-15, 0, 40])
        rotate([0, 10, 0])
            milkman_thigh();
    translate([15, 0, 40])
        rotate([0, -10, 0])
            milkman_thigh();
    
    // Churn staff in hand
    translate([40, 15, 100])
        rotate([0, 30, 0])
            churn_staff();
    
    // Base
    translate([0, 0, -5])
        display_base();
}

// === MAIN RENDER ===

if (part_mode == "preview") {
    full_assembly();
} else if (part_mode == "head") {
    milkman_helmet_front();
} else if (part_mode == "torso") {
    milkman_chest_front();
} else if (part_mode == "arm") {
    milkman_upper_arm();
} else if (part_mode == "leg") {
    milkman_thigh();
} else if (part_mode == "accessory_churn") {
    churn_staff();
}

// === PRINT LAYOUT ===
// Uncomment to generate print sheets
// part_mode = "head";
// part_mode = "torso";
// part_mode = "arm";
// part_mode = "leg";
// part_mode = "accessory_churn";
