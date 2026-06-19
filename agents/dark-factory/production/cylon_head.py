#!/usr/bin/env python3
"""
Cylon Head/Helmet - STL Generator
For Dark Factory 3D Printing
"""

import numpy as np
from stl import mesh
import math

class CylonHead:
    """Generate Cylon Centurion head for 3D printing"""
    
    def __init__(self, scale=1.0):
        self.scale = scale
        self.vertices = []
        self.faces = []
        
    def create_helmet(self):
        """Create main helmet shape"""
        # Cylon helmet is roughly cylindrical with visor
        height = 60 * self.scale
        radius = 25 * self.scale
        
        # Create cylinder with 32 segments
        segments = 32
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            
            # Bottom rim
            self.vertices.append([x, 0, z])
            # Top
            self.vertices.append([x * 0.8, height, z * 0.8])
            
        # Create faces
        for i in range(segments):
            next_i = (i + 1) % segments
            v1 = i * 2
            v2 = i * 2 + 1
            v3 = next_i * 2
            v4 = next_i * 2 + 1
            
            # Two triangles per segment
            self.faces.append([v1, v3, v2])
            self.faces.append([v2, v3, v4])
            
        return self
    
    def add_visor(self):
        """Add the distinctive red visor slit"""
        # Visor is a horizontal slit on the front
        visor_y = 35 * self.scale
        visor_width = 30 * self.scale
        visor_height = 4 * self.scale
        
        # Create visor frame
        start_idx = len(self.vertices)
        
        # Front face vertices
        self.vertices.extend([
            [-visor_width/2, visor_y - visor_height/2, 25 * self.scale],
            [visor_width/2, visor_y - visor_height/2, 25 * self.scale],
            [visor_width/2, visor_y + visor_height/2, 25 * self.scale],
            [-visor_width/2, visor_y + visor_height/2, 25 * self.scale],
        ])
        
        # Frame faces
        self.faces.extend([
            [start_idx, start_idx + 1, start_idx + 2],
            [start_idx, start_idx + 2, start_idx + 3]
        ])
        
        return self
    
    def add_mohawk(self):
        """Add the Cylon mohawk/cooling vents on top"""
        mohawk_height = 8 * self.scale
        mohawk_width = 6 * self.scale
        mohawk_length = 40 * self.scale
        
        start_idx = len(self.vertices)
        y_base = 60 * self.scale
        
        # Mohawk vertices
        self.vertices.extend([
            [-mohawk_width/2, y_base, -mohawk_length/2],
            [mohawk_width/2, y_base, -mohawk_length/2],
            [mohawk_width/2, y_base, mohawk_length/2],
            [-mohawk_width/2, y_base, mohawk_length/2],
            [-mohawk_width/2, y_base + mohawk_height, -mohawk_length/2],
            [mohawk_width/2, y_base + mohawk_height, -mohawk_length/2],
            [mohawk_width/2, y_base + mohawk_height, mohawk_length/2],
            [-mohawk_width/2, y_base + mohawk_height, mohawk_length/2],
        ])
        
        # Mohawk faces
        faces = [
            [0, 1, 5], [0, 5, 4],  # Front
            [1, 2, 6], [1, 6, 5],  # Right
            [2, 3, 7], [2, 7, 6],  # Back
            [3, 0, 4], [3, 4, 7],  # Left
            [4, 5, 6], [4, 6, 7],  # Top
        ]
        
        for face in faces:
            self.faces.append([start_idx + i for i in face])
            
        return self
    
    def export_stl(self, filename="cylon_head.stl"):
        """Export to STL file"""
        if not self.vertices or not self.faces:
            raise ValueError("No geometry to export")
            
        # Create mesh
        vertices = np.array(self.vertices)
        faces = np.array(self.faces)
        
        # Create the mesh
        cylong_head_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        
        for i, face in enumerate(faces):
            for j in range(3):
                cylong_head_mesh.vectors[i][j] = vertices[face[j]]
        
        # Save to file
        cylong_head_mesh.save(filename)
        print(f"✅ Saved: {filename}")
        print(f"   Vertices: {len(vertices)}")
        print(f"   Faces: {len(faces)}")
        print(f"   Estimated print time: 4-6 hours")
        print(f"   Material: ~80g PLA")
        
        return filename


def main():
    """Generate Cylon head STL"""
    print("=" * 70)
    print("🏭 DARK FACTORY - Cylon Head Production")
    print("=" * 70)
    
    cylon = CylonHead(scale=1.0)
    cylon.create_helmet()
    cylon.add_visor()
    cylon.add_mohawk()
    
    output_file = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/production/stl/cylon_head.stl"
    cylon.export_stl(output_file)
    
    print("\n" + "=" * 70)
    print("✅ Cylon head STL ready for printing!")
    print("=" * 70)


if __name__ == "__main__":
    main()
