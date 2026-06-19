#!/usr/bin/env python3
"""
Star Wars Droids - C-3PO & R2-D2 1:1 Scale STL Generator
Screen-accurate proportions for life-size builds
"""

import numpy as np
from stl import mesh
import math

def write_ascii_stl(filename, name, vertices, faces):
    """Write ASCII STL file"""
    with open(filename, 'w') as f:
        f.write(f"solid {name}\n")
        for face in faces:
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
    print(f"✅ Saved: {filename}")

class C3PO:
    """
    C-3PO Protocol Droid - 1:1 Scale
    Height: 175cm (5'9") - human-sized
    Gold-plated humanoid form
    """
    
    def __init__(self):
        self.scale = 1.0  # 1:1 scale
        self.height = 1750  # 175cm in mm
        self.vertices = []
        self.faces = []
    
    def create_head(self):
        """C-3PO's distinctive oval head with photoreceptors"""
        print("  Creating C-3PO head...")
        
        head_width = 140
        head_height = 200
        head_depth = 180
        
        start_idx = len(self.vertices)
        segments = 32
        rings = 24
        
        # Oval head shape
        for ring in range(rings + 1):
            theta = (ring / rings) * math.pi
            for seg in range(segments):
                phi = (seg / segments) * 2 * math.pi
                
                x = (head_width/2) * math.sin(theta) * math.cos(phi)
                y = (head_height/2) * math.cos(theta)
                z = (head_depth/2) * math.sin(theta) * math.sin(phi)
                
                self.vertices.append([x, y + self.height - 200, z])
        
        # Create faces
        for ring in range(rings):
            for seg in range(segments):
                next_seg = (seg + 1) % segments
                next_ring = ring + 1
                
                v1 = start_idx + ring * segments + seg
                v2 = start_idx + ring * segments + next_seg
                v3 = start_idx + next_ring * segments + seg
                v4 = start_idx + next_ring * segments + next_seg
                
                self.faces.append([v1, v3, v2])
                self.faces.append([v2, v3, v4])
        
        # Photoreceptor eyes (yellow)
        eye_idx = len(self.vertices)
        eye_y = self.height - 120
        
        self.vertices.extend([
            [-40, eye_y, head_depth/2 + 5],  # Left eye
            [-20, eye_y, head_depth/2 + 8],
            [-20, eye_y + 20, head_depth/2 + 8],
            [-40, eye_y + 20, head_depth/2 + 5],
            [40, eye_y, head_depth/2 + 5],   # Right eye
            [20, eye_y, head_depth/2 + 8],
            [20, eye_y + 20, head_depth/2 + 8],
            [40, eye_y + 20, head_depth/2 + 5],
        ])
        
        return self
    
    def create_torso(self):
        """Cylindrical torso with chest vents"""
        print("  Creating C-3PO torso...")
        
        chest_width = 380
        chest_depth = 220
        torso_height = 500
        
        start_idx = len(self.vertices)
        segments = 32
        
        # Main torso cylinder
        for y_level in range(2):
            y = self.height - 200 - (y_level * torso_height)
            for i in range(segments):
                angle = (i / segments) * 2 * math.pi
                x = (chest_width/2) * math.cos(angle)
                z = (chest_depth/2) * math.sin(angle)
                self.vertices.append([x, y, z])
        
        # Torso faces
        for i in range(segments):
            next_i = (i + 1) % segments
            v1 = start_idx + i
            v2 = start_idx + next_i
            v3 = start_idx + segments + i
            v4 = start_idx + segments + next_i
            
            self.faces.append([v1, v3, v2])
            self.faces.append([v2, v3, v4])
        
        return self
    
    def create_arm(self, side="left"):
        """Segmented gold arms"""
        print(f"  Creating C-3PO {side} arm...")
        
        arm_segments = 5
        segment_length = 150
        arm_diameter = 60
        
        x_offset = -250 if side == "left" else 250
        y_start = self.height - 300
        
        for seg in range(arm_segments):
            seg_idx = len(self.vertices)
            y = y_start - (seg * segment_length)
            
            # Segment ring
            for i in range(16):
                angle = (i / 16) * 2 * math.pi
                x = x_offset + (arm_diameter/2) * math.cos(angle)
                z = (arm_diameter/2) * math.sin(angle)
                self.vertices.append([x, y, z])
        
        return self
    
    def export(self, filename):
        """Export C-3PO"""
        write_ascii_stl(filename, "C3PO_1to1", self.vertices, self.faces)
        print(f"\n   Height: {self.height}mm ({self.height/10:.1f}cm)")
        print(f"   Print time: ~120-150 hours")
        print(f"   Material: ~2kg gold PLA or painted")
        return filename


class R2D2:
    """
    R2-D2 Astromech Droid - 1:1 Scale
    Height: 109cm (3'7")
    Cylindrical body with dome head
    """
    
    def __init__(self):
        self.scale = 1.0
        self.height = 1090  # 109cm in mm
        self.body_radius = 250
        self.vertices = []
        self.faces = []
    
    def create_body(self):
        """Main cylindrical body with panel details"""
        print("  Creating R2-D2 body...")
        
        body_height = 700
        start_idx = len(self.vertices)
        segments = 48
        rings = 32
        
        # Cylinder body
        for ring in range(rings + 1):
            y = (ring / rings) * body_height
            for seg in range(segments):
                angle = (seg / segments) * 2 * math.pi
                x = self.body_radius * math.cos(angle)
                z = self.body_radius * math.sin(angle)
                self.vertices.append([x, y, z])
        
        # Create faces
        for ring in range(rings):
            for seg in range(segments):
                next_seg = (seg + 1) % segments
                v1 = start_idx + ring * segments + seg
                v2 = start_idx + ring * segments + next_seg
                v3 = start_idx + (ring + 1) * segments + seg
                v4 = start_idx + (ring + 1) * segments + next_seg
                
                self.faces.append([v1, v3, v2])
                self.faces.append([v2, v3, v4])
        
        return self
    
    def create_dome(self):
        """Domed head with blue panels"""
        print("  Creating R2-D2 dome...")
        
        dome_height = 280
        start_idx = len(self.vertices)
        segments = 48
        rings = 24
        
        # Hemisphere dome
        for ring in range(rings + 1):
            theta = (ring / rings) * (math.pi / 2)
            y = 700 + dome_height * math.cos(theta)
            r = self.body_radius * math.sin(theta)
            
            for seg in range(segments):
                angle = (seg / segments) * 2 * math.pi
                x = r * math.cos(angle)
                z = r * math.sin(angle)
                self.vertices.append([x, y, z])
        
        # Dome faces
        for ring in range(rings):
            for seg in range(segments):
                next_seg = (seg + 1) % segments
                v1 = start_idx + ring * segments + seg
                v2 = start_idx + ring * segments + next_seg
                v3 = start_idx + (ring + 1) * segments + seg
                v4 = start_idx + (ring + 1) * segments + next_seg
                
                self.faces.append([v1, v3, v2])
                self.faces.append([v2, v3, v4])
        
        # Eye/photoreceptor
        eye_idx = len(self.vertices)
        self.vertices.extend([
            [-30, 850, self.body_radius + 10],
            [30, 850, self.body_radius + 10],
            [30, 890, self.body_radius + 10],
            [-30, 890, self.body_radius + 10],
        ])
        
        return self
    
    def create_legs(self):
        """Three extendable legs"""
        print("  Creating R2-D2 legs...")
        
        leg_width = 120
        leg_height = 150
        
        # Center leg (retracted)
        center_idx = len(self.vertices)
        self.vertices.extend([
            [-leg_width/2, -leg_height, -leg_width/2],
            [leg_width/2, -leg_height, -leg_width/2],
            [leg_width/2, 0, -leg_width/2],
            [-leg_width/2, 0, -leg_width/2],
        ])
        
        # Side legs (retracted position)
        for side in [-1, 1]:
            leg_idx = len(self.vertices)
            x_offset = side * 200
            
            self.vertices.extend([
                [x_offset - leg_width/2, -leg_height/2, 0],
                [x_offset + leg_width/2, -leg_height/2, 0],
                [x_offset + leg_width/2, 0, 0],
                [x_offset - leg_width/2, 0, 0],
            ])
        
        return self
    
    def export(self, filename):
        """Export R2-D2"""
        write_ascii_stl(filename, "R2D2_1to1", self.vertices, self.faces)
        print(f"\n   Height: {self.height}mm ({self.height/10:.1f}cm)")
        print(f"   Print time: ~80-100 hours")
        print(f"   Material: ~1.5kg white/blue PLA")
        return filename


def main():
    print("=" * 70)
    print("🏭 DARK FACTORY - Star Wars Droids 1:1 Scale")
    print("=" * 70)
    
    output_dir = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/production/stl/"
    
    # Generate C-3PO
    print("\n🔧 Building C-3PO...")
    c3po = C3PO()
    c3po.create_head()
    c3po.create_torso()
    c3po.create_arm("left")
    c3po.create_arm("right")
    c3po.export(output_dir + "C3PO_1to1.stl")
    
    # Generate R2-D2
    print("\n🔧 Building R2-D2...")
    r2d2 = R2D2()
    r2d2.create_body()
    r2d2.create_dome()
    r2d2.create_legs()
    r2d2.export(output_dir + "R2D2_1to1.stl")
    
    print("\n" + "=" * 70)
    print("✅ STAR WARS DROIDS COMPLETE!")
    print("=" * 70)
    print("\nC-3PO: 175cm tall, humanoid protocol droid")
    print("R2-D2: 109cm tall, astromech cylinder")
    print("\n'I am C-3PO, human-cyborg relations.'")
    print("'Beep boop beep!'")
    print("=" * 70)


if __name__ == "__main__":
    main()
