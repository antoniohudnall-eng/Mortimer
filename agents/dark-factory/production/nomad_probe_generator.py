#!/usr/bin/env python3
"""
Nomad Probe - STL Generator
Star Trek TOS "The Changeling"
Modified for drone compartments and rotor blades
"""

import numpy as np
from stl import mesh
import math

def write_ascii_stl(filename, name, vertices, faces):
    """Write ASCII STL file"""
    with open(filename, 'w') as f:
        f.write(f"solid {name}\n")
        
        for face in faces:
            # Calculate normal
            v0 = np.array(vertices[face[0]])
            v1 = np.array(vertices[face[1]])
            v2 = np.array(vertices[face[2]])
            
            edge1 = v1 - v0
            edge2 = v2 - v0
            normal = np.cross(edge1, edge2)
            norm = np.linalg.norm(normal)
            if norm > 0:
                normal = normal / norm
            
            f.write(f"  facet normal {normal[0]:.6f} {normal[1]:.6f} {normal[2]:.6f}\n")
            f.write("    outer loop\n")
            for v_idx in face:
                v = vertices[v_idx]
                f.write(f"      vertex {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
            f.write("    endloop\n")
            f.write("  endfacet\n")
        
        f.write(f"endsolid {name}\n")

class NomadProbe:
    """Generate Nomad probe with drone compartments"""
    
    def __init__(self, scale=1.0):
        self.scale = scale
        self.vertices = []
        self.faces = []
        
    def create_main_body(self):
        """Create main spherical body with internal compartments"""
        # Main sphere radius
        radius = 50 * self.scale
        segments = 64
        rings = 32
        
        start_idx = len(self.vertices)
        
        # Generate sphere vertices
        for ring in range(rings + 1):
            theta = (ring / rings) * math.pi
            sin_theta = math.sin(theta)
            cos_theta = math.cos(theta)
            
            for seg in range(segments):
                phi = (seg / segments) * 2 * math.pi
                sin_phi = math.sin(phi)
                cos_phi = math.cos(phi)
                
                x = radius * sin_theta * cos_phi
                y = radius * cos_theta
                z = radius * sin_theta * sin_phi
                
                self.vertices.append([x, y, z])
        
        # Create faces for sphere
        for ring in range(rings):
            for seg in range(segments):
                next_seg = (seg + 1) % segments
                next_ring = ring + 1
                
                v1 = start_idx + ring * segments + seg
                v2 = start_idx + ring * segments + next_seg
                v3 = start_idx + next_ring * segments + seg
                v4 = start_idx + next_ring * segments + next_seg
                
                # Skip faces where drones will be inserted (top and bottom)
                # Top drone compartment: rings 1-4, all segments
                # Bottom drone compartment: rings rings-5 to rings-1, all segments
                if (ring >= 1 and ring <= 4) or (ring >= rings - 5 and ring <= rings - 1):
                    continue
                
                self.faces.append([v1, v3, v2])
                self.faces.append([v2, v3, v4])
        
        return self
    
    def add_top_drone_compartment(self):
        """Add compartment for top drone"""
        # Cylinder opening on top
        radius = 25 * self.scale
        height = 30 * self.scale
        segments = 32
        
        start_idx = len(self.vertices)
        
        # Create cylinder walls
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            
            # Bottom rim (at y=40)
            self.vertices.append([x, 40 * self.scale, z])
            # Top (at y=70)
            self.vertices.append([x, 70 * self.scale, z])
        
        # Cylinder faces
        for i in range(segments):
            next_i = (i + 1) % segments
            v1 = start_idx + i * 2
            v2 = start_idx + i * 2 + 1
            v3 = start_idx + next_i * 2
            v4 = start_idx + next_i * 2 + 1
            
            self.faces.append([v1, v3, v2])
            self.faces.append([v2, v3, v4])
        
        # Add mounting points for drone
        for i in range(4):
            angle = (i / 4) * 2 * math.pi
            x = 15 * self.scale * math.cos(angle)
            z = 15 * self.scale * math.sin(angle)
            
            mount_idx = len(self.vertices)
            self.vertices.append([x, 55 * self.scale, z])  # Mount point
            self.vertices.append([x, 50 * self.scale, z])  # Base
            
            # Small mounting bracket
            self.faces.append([mount_idx, mount_idx + 1, (start_idx + i * 8) % (start_idx + segments * 2)])
        
        return self
    
    def add_bottom_drone_compartment(self):
        """Add compartment for bottom drone"""
        # Larger compartment for bottom drone
        radius = 30 * self.scale
        height = 35 * self.scale
        segments = 32
        
        start_idx = len(self.vertices)
        
        # Create cylinder walls
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            
            # Top rim (at y=-40)
            self.vertices.append([x, -40 * self.scale, z])
            # Bottom (at y=-75)
            self.vertices.append([x, -75 * self.scale, z])
        
        # Cylinder faces
        for i in range(segments):
            next_i = (i + 1) % segments
            v1 = start_idx + i * 2
            v2 = start_idx + i * 2 + 1
            v3 = start_idx + next_i * 2
            v4 = start_idx + next_i * 2 + 1
            
            self.faces.append([v1, v2, v3])
            self.faces.append([v2, v4, v3])
        
        return self
    
    def add_antenna_array(self):
        """Add Nomad's distinctive antenna probes"""
        # Main central antenna
        ant_radius = 2 * self.scale
        ant_height = 40 * self.scale
        segments = 16
        
        start_idx = len(self.vertices)
        
        # Central antenna base at top
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi
            x = ant_radius * math.cos(angle)
            z = ant_radius * math.sin(angle)
            
            self.vertices.append([x, 70 * self.scale, z])
            self.vertices.append([x, (70 + ant_height) * self.scale, z])
        
        # Antenna faces
        for i in range(segments):
            next_i = (i + 1) % segments
            v1 = start_idx + i * 2
            v2 = start_idx + i * 2 + 1
            v3 = start_idx + next_i * 2
            v4 = start_idx + next_i * 2 + 1
            
            self.faces.append([v1, v3, v2])
            self.faces.append([v2, v3, v4])
        
        # Side antennas (2 smaller ones)
        for offset in [-20, 20]:
            side_start = len(self.vertices)
            side_height = 25 * self.scale
            side_radius = 1.5 * self.scale
            
            for i in range(segments):
                angle = (i / segments) * 2 * math.pi
                x = offset * self.scale + side_radius * math.cos(angle)
                z = side_radius * math.sin(angle)
                
                self.vertices.append([x, 65 * self.scale, z])
                self.vertices.append([x, (65 + side_height) * self.scale, z])
            
            for i in range(segments):
                next_i = (i + 1) % segments
                v1 = side_start + i * 2
                v2 = side_start + i * 2 + 1
                v3 = side_start + next_i * 2
                v4 = side_start + next_i * 2 + 1
                
                self.faces.append([v1, v3, v2])
                self.faces.append([v2, v3, v4])
        
        return self
    
    def add_sensor_eye(self):
        """Add the red sensor eye"""
        # Eye on front of body
        eye_radius = 8 * self.scale
        eye_y = 10 * self.scale
        segments = 24
        
        start_idx = len(self.vertices)
        
        # Eye protrusion
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi
            x = eye_radius * math.cos(angle)
            z = 50 * self.scale + eye_radius * math.sin(angle) * 0.3  # Slight protrusion
            
            self.vertices.append([x, eye_y, z])
            self.vertices.append([x, eye_y, (50 + 5) * self.scale])  # Front of eye
        
        # Eye faces
        for i in range(segments):
            next_i = (i + 1) % segments
            v1 = start_idx + i * 2
            v2 = start_idx + i * 2 + 1
            v3 = start_idx + next_i * 2
            v4 = start_idx + next_i * 2 + 1
            
            self.faces.append([v1, v2, v3])
            self.faces.append([v2, v4, v3])
        
        return self
    
    def export_stl(self, filename):
        """Export to STL file"""
        write_ascii_stl(filename, "Nomad_Probe", self.vertices, self.faces)
        
        print(f"✅ Saved: {filename}")
        print(f"   Vertices: {len(self.vertices)}")
        print(f"   Faces: {len(self.faces)}")
        print(f"   Dimensions: ~100mm diameter x 160mm tall")
        print(f"   Print time: 12-16 hours")
        print(f"   Material: ~200g PLA")
        
        return filename


class SingleBladeRotor:
    """Generate single blade rotor for drone"""
    
    def __init__(self, scale=1.0, blade_length=80):
        self.scale = scale
        self.blade_length = blade_length * scale
        self.vertices = []
        self.faces = []
    
    def create_rotor(self):
        """Create single blade rotor"""
        # Central hub
        hub_radius = 5 * self.scale
        hub_height = 8 * self.scale
        segments = 16
        
        start_idx = len(self.vertices)
        
        # Hub vertices
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi
            x = hub_radius * math.cos(angle)
            z = hub_radius * math.sin(angle)
            
            self.vertices.append([x, 0, z])
            self.vertices.append([x, hub_height, z])
        
        # Hub faces
        for i in range(segments):
            next_i = (i + 1) % segments
            v1 = start_idx + i * 2
            v2 = start_idx + i * 2 + 1
            v3 = start_idx + next_i * 2
            v4 = start_idx + next_i * 2 + 1
            
            self.faces.append([v1, v3, v2])
            self.faces.append([v2, v3, v4])
        
        # Single blade
        blade_start = len(self.vertices)
        blade_width = 15 * self.scale
        blade_thickness = 2 * self.scale
        
        # Blade extends from hub
        self.vertices.extend([
            [0, hub_height/2, hub_radius],  # Root inner
            [0, hub_height/2 + blade_thickness, hub_radius],  # Root top
            [0, hub_height/2, hub_radius + blade_width],  # Tip inner
            [0, hub_height/2 + blade_thickness, hub_radius + blade_width],  # Tip top
            [self.blade_length, hub_height/2, hub_radius + blade_width/2],  # End
        ])
        
        # Blade faces (simplified)
        self.faces.extend([
            [blade_start, blade_start + 1, blade_start + 2],
            [blade_start + 1, blade_start + 3, blade_start + 2],
            [blade_start + 2, blade_start + 3, blade_start + 4],
        ])
        
        return self
    
    def export_stl(self, filename):
        """Export rotor to STL"""
        write_ascii_stl(filename, "Single_Blade_Rotor", self.vertices, self.faces)
        
        print(f"✅ Saved: {filename}")
        print(f"   Vertices: {len(self.vertices)}")
        print(f"   Blade length: {self.blade_length}mm")
        print(f"   Print time: 2-3 hours")
        print(f"   Material: ~25g PLA")
        
        return filename


def main():
    """Generate Nomad probe with drone compartments"""
    print("=" * 70)
    print("🏭 DARK FACTORY - Nomad Probe Production")
    print("=" * 70)
    print("Star Trek TOS 'The Changeling'")
    print("Modified: Drone compartments + Single blade rotors")
    print("=" * 70)
    
    # Create Nomad probe
    print("\n🔧 Generating Nomad main body...")
    nomad = NomadProbe(scale=1.0)
    nomad.create_main_body()
    nomad.add_top_drone_compartment()
    nomad.add_bottom_drone_compartment()
    nomad.add_antenna_array()
    nomad.add_sensor_eye()
    
    output_dir = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/production/stl/"
    nomad.export_stl(output_dir + "nomad_probe_main.stl")
    
    # Create rotors
    print("\n🔧 Generating top rotor (small)...")
    top_rotor = SingleBladeRotor(scale=0.6, blade_length=60)
    top_rotor.create_rotor()
    top_rotor.export_stl(output_dir + "nomad_top_rotor.stl")
    
    print("\n🔧 Generating bottom rotor (large)...")
    bottom_rotor = SingleBladeRotor(scale=1.0, blade_length=100)
    bottom_rotor.create_rotor()
    bottom_rotor.export_stl(output_dir + "nomad_bottom_rotor.stl")
    
    print("\n" + "=" * 70)
    print("✅ NOMAD PROBE ASSEMBLY KIT COMPLETE!")
    print("=" * 70)
    print("\nParts:")
    print("  1. nomad_probe_main.stl - Main body with compartments")
    print("  2. nomad_top_rotor.stl - Single blade rotor (small)")
    print("  3. nomad_bottom_rotor.stl - Single blade rotor (large)")
    print("\nAssembly:")
    print("  - Install top drone in upper compartment")
    print("  - Install bottom drone in lower compartment")
    print("  - Mount top rotor on upper drone")
    print("  - Mount bottom rotor on lower drone")
    print("  - Sensor eye glows red (use LED)")
    print("\nTotal print time: ~18-20 hours")
    print("Total material: ~250g PLA")
    print("=" * 70)


if __name__ == "__main__":
    main()
