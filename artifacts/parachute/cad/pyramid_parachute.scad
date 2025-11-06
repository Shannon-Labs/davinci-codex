
// da Vinci Pyramid Parachute - Parametric Model
// Based on Codex Atlanticus folio 381v

// Parameters
size = 6996.0;  // Convert to mm
frame_diameter = 25;    // Frame pole diameter in mm
canopy_thickness = 0.5; // Canopy material thickness in mm

// Calculate pyramid height (equilateral triangles)
pyramid_height = size * 0.866;

module pyramid_frame() {
    // Base square frame
    color("brown", 0.8)
    union() {
        // Four base edges
        for (i = [0:3]) {
            rotate([0, 0, i*90])
            translate([size/2, 0, 0])
            rotate([0, 90, 0])
            cylinder(h=size, d=frame_diameter, center=true);
        }

        // Four apex edges
        for (i = [0:3]) {
            rotate([0, 0, i*90])
            translate([size/2, size/2, 0])
            rotate([atan(pyramid_height/(size/sqrt(2))), 0, 45])
            cylinder(h=sqrt(pow(size/sqrt(2), 2) + pow(pyramid_height, 2)), d=frame_diameter);
        }
    }
}

module canopy() {
    // Pyramid canopy (simplified as solid for visualization)
    color("lightblue", 0.7)
    translate([0, 0, pyramid_height/2])
    scale([1, 1, pyramid_height/(size/2)])
    rotate([0, 0, 45])
    cylinder(h=size/2, d1=size*sqrt(2), d2=0, center=true, $fn=4);
}

module suspension_lines() {
    // Simplified suspension lines from apex to payload
    color("gray", 0.5)
    for (i = [0:3]) {
        rotate([0, 0, i*90])
        translate([size/3, size/3, 0])
        cylinder(h=pyramid_height*1.2, d=2);
    }
}

module payload_harness() {
    // Simplified payload attachment point
    color("darkgray")
    translate([0, 0, -200])
    cylinder(h=50, d=100, center=true);
}

// Assembly
pyramid_frame();
canopy();
suspension_lines();
payload_harness();

// Export note
echo(str("Parachute size: ", size/1000, " meters"));
echo(str("Pyramid height: ", pyramid_height/1000, " meters"));
echo(str("Estimated canopy area: ", 2*size*sqrt(pow(size/2,2)+pow(pyramid_height,2))/1000000, " m²"));
