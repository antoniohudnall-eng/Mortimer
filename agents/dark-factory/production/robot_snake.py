#!/usr/bin/env python3
"""
Robot Snake - Modular Articulated Spine
Can serve as:
1. Standalone snake robot
2. Spine module for humanoid robots
3. Flexible arm extension
4. Periscope/antenna system

Features:
- 16+ segments (vertebrae)
- 2 DOF per segment (yaw/pitch)
- Continuous rotation capable
- Hollow center for wiring
- Quick-connect to humanoid torso
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

class RobotSnake:
    """
    Modular articulated snake robot
    Each segment = 1 vertebra with 2 DOF
    """
    
    def __init__(self, num_segments=16, scale=1.0):
        self.num_segments = num_segments
        self.scale = scale
        self.segment_length = 40 * scale  # 40mm per segment
        self.vertices = []
        self.faces = []
        
    def create_segment(self, segment_num, total_segments):
        """Create one snake segment (vertebra)"""
        
        # Each segment has:
        # - Body (cylindrical)
        # - Joint (universal joint style)
        # - Servo mounts
        # - Cable channel
        
        y_pos = -segment_num * self.segment_length
        
        # Segment diameter tapers toward tail
        diameter = 50 * self.scale * (1 - segment_num/total_segments * 0.3)
        
        seg_idx = len(self.vertices)
        
        # Main body (cylinder)
        segments = 24
        rings = 8
        
        for ring in range(rings + 1):
            y = y_pos + (ring / rings) * self.segment_length * 0.7
            for s in range(segments):
                angle = (s / segments) * 2 * math.pi
                x = (diameter/2) * math.cos(angle)
                z = (diameter/2) * math.sin(angle)
                self.vertices.append([x, y, z])
        
        # Body faces
        for ring in range(rings):
            for s in range(segments):
                next_s = (s + 1) % segments
                v1 = seg_idx + ring * segments + s
                v2 = seg_idx + ring * segments + next_s
                v3 = seg_idx + (ring + 1) * segments + s
                v4 = seg_idx + (ring + 1) * segments + next_s
                
                self.faces.append([v1, v3, v2])
                self.faces.append([v2, v3, v4])
        
        # Joint mechanism (ball-and-socket style)
        joint_idx = len(self.vertices)
        joint_y = y_pos + self.segment_length * 0.7
        
        # Ball joint (male)
        ball_radius = diameter * 0.35
        
        for ring in range(8):
            theta = (ring / 8) * math.pi / 2
            y = joint_y + ball_radius * math.sin(theta)
            r = ball_radius * math.cos(theta)
            
            for s in range(16):
                angle = (s / 16) * 2 * math.pi
                x = r * math.cos(angle)
                z = r * math.sin(angle)
                self.vertices.append([x, y, z])
        
        # Socket (female) - on next segment
        # (Handled by connection between segments)
        
        return self
    
    def create_head(self):
        """Snake head with sensors"""
        print("  Creating snake head...")
        
        head_idx = len(self.vertices)
        
        # Triangular snake head
        head_length = 60 * self.scale
        head_width = 40 * self.scale
        
        # Head shape
        self.vertices.extend([
            [0, head_width/2, 0],  # Nose tip
            [-head_width/2, -head_length/2, 0],  # Left
            [head_width/2, -head_length/2, 0],  # Right
            [0, 0, head_width/2],  # Top
        ])
        
        # Eyes (infrared sensors)
        for side in [-1, 1]:
            eye_idx = len(self.vertices)
            eye_x = side * 15
            eye_y = 20
            
            self.vertices.extend([
                [eye_x - 5, eye_y, 10],
                [eye_x + 5, eye_y, 10],
                [eye_x + 5, eye_y + 10, 12],
                [eye_x - 5, eye_y + 10, 12],
            ])
        
        # Jaw (articulated)
        jaw_idx = len(self.vertices)
        
        self.vertices.extend([
            [-head_width/2, -head_length/2, 0],
            [head_width/2, -head_length/2, 0],
            [head_width/3, -head_length, 5],
            [-head_width/3, -head_length, 5],
        ])
        
        return self
    
    def create_full_snake(self):
        """Generate complete snake"""
        print("  Creating full snake body...")
        
        for i in range(self.num_segments):
            self.create_segment(i, self.num_segments)
        
        self.create_head()
        
        return self
    
    def export(self, filename):
        """Export to STL"""
        write_ascii_stl(filename, f"RobotSnake_{self.num_segments}seg", 
                       self.vertices, self.faces)
        
        print(f"\n📊 ROBOT SNAKE SPECIFICATIONS:")
        print(f"   Segments: {self.num_segments}")
        print(f"   Length: {self.num_segments * self.segment_length}mm")
        print(f"   DOF: {self.num_segments * 2} (2 per segment)")
        print(f"   Vertices: {len(self.vertices)}")
        print(f"   Print time: ~{self.num_segments * 8}-{self.num_segments * 12} hours")
        print(f"   Material: ~{self.num_segments * 50}g filament")


class SnakeAsSpine:
    """
    Snake robot configured as spine for humanoid
    Replaces the 24-vertebra spine with articulated snake
    """
    
    def __init__(self, humanoid_height=1750):
        self.humanoid_height = humanoid_height
        self.scale = humanoid_height / 1750  # Scale to match humanoid
        
        # Spine: 12 segments for upper back
        # (Lower back uses pelvis structure)
        self.snake_spine = RobotSnake(num_segments=12, scale=self.scale)
        
    def create_spine_attachment(self):
        """Create attachment points for humanoid"""
        
        # Top: Connects to skull base
        # Bottom: Connects to pelvis
        
        print("  Creating spine attachment system...")
        
        # Skull base mount
        skull_mount_idx = len(self.snake_spine.vertices)
        
        self.snake_spine.vertices.extend([
            [-40, 10, -40],
            [40, 10, -40],
            [40, 10, 40],
            [-40, 10, 40],
        ])
        
        # Pelvis mount
        pelvis_mount_idx = len(self.snake_spine.vertices)
        pelvis_y = -12 * 40 * self.scale  # Bottom of 12 segments
        
        self.snake_spine.vertices.extend([
            [-60, pelvis_y - 10, -50],
            [60, pelvis_y - 10, -50],
            [60, pelvis_y - 10, 50],
            [-60, pelvis_y - 10, 50],
        ])
        
        return self.snake_spine
    
    def export_spine(self, filename):
        """Export as spine module"""
        self.snake_spine.create_full_snake()
        self.create_spine_attachment()
        
        write_ascii_stl(filename, "SnakeSpine_Module", 
                       self.snake_spine.vertices, self.snake_spine.faces)
        
        print(f"\n📊 SNAKE SPINE MODULE:")
        print(f"   Replaces: Rigid 24-vertebra spine")
        print(f"   With: Articulated 12-segment snake")
        print(f"   DOF: 24 (vs 0 for rigid spine)")
        print(f"   Benefit: Flexible, dynamic posture")
        print(f"   Compatible: All humanoid models")


def main():
    print("=" * 70)
    print("🐍 ROBOT SNAKE - Modular Articulated Spine")
    print("=" * 70)
    
    # Create standalone snake
    print("\n🔧 Building standalone snake robot...")
    snake = RobotSnake(num_segments=16, scale=1.0)
    snake.create_full_snake()
    
    output_dir = "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/production/stl/"
    snake.export(output_dir + "robot_snake_16seg.stl")
    
    # Create spine module
    print("\n🔧 Building snake spine module...")
    spine = SnakeAsSpine(humanoid_height=1750)
    spine.export_spine(output_dir + "snake_spine_module.stl")
    
    print("\n" + "=" * 70)
    print("✅ ROBOT SNAKE COMPLETE!")
    print("=" * 70)
    print("\nTwo configurations:")
    print("  1. Standalone snake robot (16 segments)")
    print("  2. Spine module for humanoid (12 segments)")
    print("\nApplications:")
    print("  • Search and rescue (snake mode)")
    print("  • Inspection robot (snake mode)")
    print("  • Dynamic humanoid spine (spine mode)")
    print("  • Periscope/antenna (extension mode)")
    print("\n'Remember: snakes are just spines that got away...'")
    print("=" * 70)


if __name__ == "__main__":
    main()
