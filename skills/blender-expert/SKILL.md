---
name: blender-expert
description: Blender 3D modeling, animation, and rendering — mechanical components, mannequin parts, and articulated joints.
---

# Blender 3D Expert Skill

AGI Agent specializing in Blender 3D modeling, animation, and rendering with focus on mechanical components, mannequin parts, and articulated joints.

## Overview

Blender is a free and open-source 3D creation suite supporting the entire 3D pipeline:
- Modeling (mesh, curve, sculpt)
- Rigging and animation
- Simulation
- Rendering (Cycles, EEVEE)
- Compositing and motion tracking
- Video editing
- Python scripting and API automation

## Blender 4.x Series Key Features

### 4.0 (November 2023)
- **Node Tools**: Geometry nodes can be used as operators from 3D view menus
- **Repeat Zone**: Dynamic iteration of nodes
- **Rotation Sockets**: Native rotation data type with 8 new rotation nodes
- **Sharp Edge Status**: Accessible in builtin nodes
- **Simulation Zone Baking**: Individual bake support
- **New Snap Features**: Navigate while transforming (Alt+navigate), snap base editing

### 4.1 (March 2024)
- VFX Platform 2024 compliance
- Python 3.11 support
- OpenColorIO 2.3, OpenEXR 3.2, OpenVDB 11.0
- Intel Arc GPU support

### 4.2 LTS (July 2024) - CURRENT LTS
- **Long-term support until July 2026**
- **Extensions Platform**: New add-on/extensions system
- **Matrix Sockets**: Full transformation matrix support in Geometry Nodes
- **Performance Improvements**: Scale Elements 4-10x faster, Sample UV Surface 10-20x faster
- **Enhanced Node Tools**: Mouse Position, Viewport Transform, Active Element nodes
- **Hardware**: SSE4.2 CPU required (AMD Bulldozer 2011+, Intel Nehalem 2008+)

### 4.3 (November 2024)
- **SLIM UV Unwrapping**: New "Minimum Stretch" method (Scalable Local Injective Mappings)
- **Bevel Modifier**: Custom attribute support for bevel weights
- Windows on Arm experimental support

---

## Core Workflows

### 1. Modeling Workflows

#### Mesh Primitives
```python
import bpy

# Create primitives
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=32, ring_count=16, location=(3, 0, 0))
bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, vertices=32, location=(-3, 0, 0))
bpy.ops.mesh.primitive_cone_add(radius1=1, depth=2, vertices=32, location=(0, 3, 0))
bpy.ops.mesh.primitive_torus_add(major_radius=2, minor_radius=0.5, location=(0, -3, 0))
```

#### Edit Mode Operations
- **Selection**: Vertex/Edge/Face modes (1/2/3 keys)
- **Extrude**: E key - pull geometry outward
- **Inset**: I key - create inset faces
- **Bevel**: Ctrl+B - chamfer edges/vertices
- **Loop Cut**: Ctrl+R - add edge loops
- **Knife**: K key - custom cuts
- **Bridge Edge Loops**: Connect multiple edge loops

#### Modifier Stack (Apply in order!)
1. **Mirror** - Symmetrical modeling
2. **Subdivision Surface** - Smooth subdivision
3. **Bevel** - Rounded edges
4. **Solidify** - Add thickness
5. **Boolean** - Union/Difference/Intersect
6. **Array** - Duplicate patterns
7. **Curve** - Deform along path

### 2. Sculpting Workflow

#### Brush Types
- **Draw**: Basic sculpting
- **Crease**: Sharp details
- **Clay**: Build up form
- **Inflate/Deflate**: Expand/contract
- **Smooth**: Average vertices
- **Grab**: Move large areas
- **Pinch**: Pull toward center

#### Dynamic Topology (Dyntopo)
- Enable for adaptive subdivision
- Detail Size: Controls resolution
- Collapse/Subdivide edges
- Great for organic shapes

#### Multiresolution
- Non-destructive subdivision
- Sculpt at different levels
- Good for baking displacement

### 3. Material System (Principled BSDF)

#### Key Parameters for Mannequins
```
Base Color: Primary surface color
Metallic: 0.0-1.0 (0 for plastic, 1 for metal)
Specular: Reflection intensity
Roughness: Surface smoothness (0=shiny, 1=matte)
IOR: Index of refraction (1.45 plastic, 1.5 glass)
Normal/Bump: Surface detail
```

#### Node Setup for Mechanical Parts
```
[Texture Coordinate] → [Mapping] → [Image Texture] → [Principled BSDF] → [Material Output]
                            ↓
                    [Normal Map] → [Normal]
```

### 4. Lighting & Rendering

#### EEVEE (Real-time)
- Fast viewport rendering
- Good for previz and assets
- Screen-space reflections
- Contact shadows
- Bloom and motion blur

#### Cycles (Ray-traced)
- Physically accurate
- Path tracing engine
- GPU/CPU rendering
- Better for final output

#### Three-Point Lighting Setup
```
Key Light: Main illumination (45° angle, warm)
Fill Light: Shadows softening (opposite side, cool, dimmer)
Rim Light: Edge separation (behind subject, bright)
```

---

## Python Scripting for Blender

### Scripting Environment

#### Running Scripts
1. **Text Editor**: Built-in editor (Ctrl+Alt+P to run)
2. **Scripting Workspace**: Dedicated layout
3. **Command Line**: `blender --python script.py`
4. **Console**: Interactive Python console

#### Key API Modules
- `bpy.context`: Access current scene/selection
- `bpy.data`: Access all data blocks
- `bpy.ops`: Operators (tools and functions)
- `bpy.types`: Type definitions
- `bmesh`: Mesh manipulation
- `mathutils`: Vectors, matrices, quaternions

### Essential Patterns

#### Scene Setup
```python
import bpy

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create new collection
new_collection = bpy.data.collections.new("MannequinParts")
bpy.context.scene.collection.children.link(new_collection)
```

#### Object Creation and Manipulation
```python
import bpy
from mathutils import Vector, Euler

# Create mesh from vertices/edges/faces
verts = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
faces = [(0, 1, 2, 3)]

mesh = bpy.data.meshes.new(name="CustomMesh")
mesh.from_pydata(verts, edges, faces)
mesh.update()

obj = bpy.data.objects.new(name="CustomObject", object_data=mesh)
bpy.context.collection.objects.link(obj)

# Transformations
obj.location = Vector((1, 2, 3))
obj.rotation_euler = Euler((0, 0, 3.14159/2), 'XYZ')
obj.scale = Vector((1, 1, 1.5))
```

#### Modifier Application
```python
import bpy

obj = bpy.context.active_object

# Add bevel modifier
bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
bevel.width = 0.02
bevel.segments = 3
bevel.limit_method = 'ANGLE'
bevel.angle_limit = 0.5236  # 30 degrees

# Add subdivision surface
subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
subdiv.levels = 2
subdiv.render_levels = 3

# Add solidify
solid = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
solid.thickness = 0.01
```

---

## Mannequin Parts Creation

### Best Practices

1. **Topology**: Use quad-based topology when possible
2. **Edge Flow**: Follow natural deformation lines
3. **Symmetry**: Use Mirror modifier for bilateral parts
4. **Scale**: Work in real-world units (meters)
5. **Naming**: Consistent naming conventions

### Limb Segments

#### Upper Arm / Thigh
```python
import bpy
from mathutils import Vector

def create_limb_segment(name, length=0.3, width=0.08, depth=0.07):
    """Create a limb segment with proper topology."""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=width/2,
        depth=length,
        vertices=16,
        location=(0, 0, length/2),
        rotation=(1.5708, 0, 0)  # Lay horizontal
    )
    obj = bpy.context.active_object
    obj.name = name
    
    # Add end caps (slightly larger for joint clearance)
    for z in [0, length]:
        bpy.ops.mesh.primitive_cylinder_add(
            radius=width/2 + 0.005,
            depth=0.01,
            vertices=16,
            location=(0, 0, z),
            rotation=(1.5708, 0, 0)
        )
        cap = bpy.context.active_object
        cap.name = f"{name}_cap_{'proximal' if z == 0 else 'distal'}"
    
    return obj

create_limb_segment("UpperArm_L", length=0.28, width=0.09, depth=0.08)
```

#### Hand/Foot Base
```python
def create_hand_base(name="Hand_L"):
    """Create a base hand mesh for mannequin."""
    bpy.ops.mesh.primitive_cube_add(size=0.06, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (1.2, 1.8, 0.4)
    
    # Apply scale
    bpy.ops.object.transform_apply(scale=True)
    
    # Add wrist connector
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.035,
        depth=0.02,
        vertices=16,
        location=(0, -0.06, 0),
        rotation=(1.5708, 0, 0)
    )
    wrist = bpy.context.active_object
    wrist.name = f"{name}_wrist"
    
    return obj
```

### Torso Construction

```python
def create_torso_segment(name="Torso"):
    """Create a segmented torso with proper proportions."""
    # Pelvis
    bpy.ops.mesh.primitive_cube_add(size=0.18, location=(0, 0, 0.09))
    pelvis = bpy.context.active_object
    pelvis.name = f"{name}_pelvis"
    pelvis.scale = (1.3, 0.8, 0.5)
    bpy.ops.object.transform_apply(scale=True)
    
    # Abdomen
    bpy.ops.mesh.primitive_cube_add(size=0.15, location=(0, 0, 0.28))
    abdomen = bpy.context.active_object
    abdomen.name = f"{name}_abdomen"
    abdomen.scale = (1.2, 0.75, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    
    # Chest
    bpy.ops.mesh.primitive_cube_add(size=0.2, location=(0, 0, 0.5))
    chest = bpy.context.active_object
    chest.name = f"{name}_chest"
    chest.scale = (1.5, 0.9, 1.2)
    bpy.ops.object.transform_apply(scale=True)
    
    return [pelvis, abdomen, chest]
```

---

## Articulated Joints

### Joint Types

#### Hinge Joint (Elbow, Knee)
- Single axis rotation
- 0-150 degree range
- Cylindrical pin mechanism

```python
def create_hinge_joint(name="Elbow", radius=0.04, width=0.025):
    """Create a hinge joint with pin."""
    # Joint housing
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius,
        depth=width * 3,
        vertices=24,
        location=(0, 0, 0),
        rotation=(1.5708, 0, 0)
    )
    housing = bpy.context.active_object
    housing.name = f"{name}_housing"
    
    # Pin
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius * 0.3,
        depth=width * 3.5,
        vertices=16,
        location=(0, 0, 0),
        rotation=(1.5708, 0, 0)
    )
    pin = bpy.context.active_object
    pin.name = f"{name}_pin"
    
    # Add materials
    housing.data.materials.append(create_metallic_material("Joint_Aluminum"))
    pin.data.materials.append(create_metallic_material("Pin_Steel", roughness=0.3))
    
    return housing, pin

def create_metallic_material(name, base_color=(0.8, 0.8, 0.8), roughness=0.4):
    """Create a metallic material."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    principled = nodes.get("Principled BSDF")
    principled.inputs['Base Color'].default_value = (*base_color, 1.0)
    principled.inputs['Metallic'].default_value = 1.0
    principled.inputs['Roughness'].default_value = roughness
    return mat
```

#### Ball-and-Socket (Shoulder, Hip)
- Full spherical rotation
- Conical rotation limits
- Ball + socket cup mechanism

```python
def create_ball_joint(name="Shoulder", ball_radius=0.045, socket_depth=0.06):
    """Create a ball-and-socket joint."""
    # Ball (sphere)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=ball_radius,
        segments=32,
        ring_count=16,
        location=(0, 0, 0)
    )
    ball = bpy.context.active_object
    ball.name = f"{name}_ball"
    
    # Socket (hemisphere with cut)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=ball_radius * 1.1,
        segments=32,
        ring_count=16,
        location=(0, 0, -socket_depth * 0.3)
    )
    socket = bpy.context.active_object
    socket.name = f"{name}_socket"
    
    # Cut socket to make hemisphere
    bpy.ops.object.modifier_add(type='BOOLEAN')
    socket.modifiers["Boolean"].operation = 'DIFFERENCE'
    # Would need a cutting plane here
    
    return ball, socket
```

#### Universal Joint (Wrist, Ankle)
- Two-axis rotation
- Cardan/cross mechanism
- Orthogonal hinge pins

```python
def create_universal_joint(name="Wrist", radius=0.03):
    """Create a universal joint (Cardan)."""
    # Cross piece
    bpy.ops.mesh.primitive_cube_add(size=radius*2, location=(0, 0, 0))
    cross = bpy.context.active_object
    cross.name = f"{name}_cross"
    cross.scale = (2.5, 0.5, 0.5)
    bpy.ops.object.transform_apply(scale=True)
    
    # Yoke A
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius * 1.2,
        depth=radius * 4,
        vertices=16,
        location=(radius * 2, 0, 0),
        rotation=(0, 1.5708, 0)
    )
    yoke_a = bpy.context.active_object
    yoke_a.name = f"{name}_yoke_A"
    
    # Yoke B
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius * 1.2,
        depth=radius * 4,
        vertices=16,
        location=(0, radius * 2, 0),
        rotation=(1.5708, 0, 0)
    )
    yoke_b = bpy.context.active_object
    yoke_b.name = f"{name}_yoke_B"
    
    return cross, yoke_a, yoke_b
```

---

## Mechanical Components

### Gear Generation

```python
import bpy
import math

def create_spur_gear(name="Gear", teeth=20, module=0.01, thickness=0.005):
    """Create a spur gear using geometry nodes or mesh construction."""
    pitch_diameter = teeth * module
    outer_diameter = pitch_diameter + (2 * module)
    root_diameter = pitch_diameter - (2.5 * module)
    
    # Create base cylinder
    bpy.ops.mesh.primitive_cylinder_add(
        radius=outer_diameter / 2,
        depth=thickness,
        vertices=teeth * 4,
        location=(0, 0, 0)
    )
    gear = bpy.context.active_object
    gear.name = name
    
    # Enter edit mode to shape teeth
    bpy.context.view_layer.objects.active = gear
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Select alternating vertices to create tooth profile
    # (Simplified - actual gear requires involute curve)
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return gear
```

### Threaded Fasteners

```python
def create_bolt(name="Bolt", diameter=0.008, length=0.04, pitch=0.001):
    """Create a threaded bolt."""
    # Bolt head
    bpy.ops.mesh.primitive_cylinder_add(
        radius=diameter * 1.5,
        depth=diameter * 0.6,
        vertices=6,  # Hex head
        location=(0, 0, length + diameter * 0.3)
    )
    head = bpy.context.active_object
    head.name = f"{name}_head"
    
    # Shaft (can add screw modifier for threads)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=diameter / 2,
        depth=length,
        vertices=16,
        location=(0, 0, length / 2)
    )
    shaft = bpy.context.active_object
    shaft.name = f"{name}_shaft"
    
    # Add screw modifier for threads
    screw = shaft.modifiers.new(name="Threads", type='SCREW')
    screw.axis = 'Z'
    screw.screw_offset = pitch
    screw.angle = 6.28318  # 360 degrees
    screw.iterations = int(length / pitch)
    screw.steps = 12
    
    return head, shaft
```

### Linear Rail System

```python
def create_linear_rail(name="LinearRail", length=0.5, width=0.02):
    """Create a linear rail with carriage."""
    # Rail
    bpy.ops.mesh.primitive_cube_add(size=width, location=(0, 0, 0))
    rail = bpy.context.active_object
    rail.name = f"{name}_rail"
    rail.scale = (length / width, 0.5, 1)
    bpy.ops.object.transform_apply(scale=True)
    
    # Add dovetail profile (simplified)
    # Would use Boolean modifiers for actual profile
    
    # Carriage
    bpy.ops.mesh.primitive_cube_add(
        size=width * 2,
        location=(0, 0, width * 1.5)
    )
    carriage = bpy.context.active_object
    carriage.name = f"{name}_carriage"
    carriage.scale = (0.1, 1.2, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    
    return rail, carriage
```

---

## Geometry Nodes for Procedural Modeling

### Mannequin Assembly System

```
Group Input → Transform (loc/rot/scale) → Join Geometry → Group Output
                   ↓
              Instance on Points (limb parts)
                   ↓
              Collection Info (part library)
```

### Key Geometry Nodes (4.x)

| Node | Purpose |
|------|---------|
| `Transform Geometry` | Move/rotate/scale |
| `Set Position` | Direct vertex manipulation |
| `Instance on Points` | Place objects at points |
| `Join Geometry` | Combine multiple meshes |
| `Separate Geometry` | Split by selection |
| `Mesh to Points` | Convert mesh to point cloud |
| `Points to Vertices` | Points back to mesh |
| `Curve to Mesh` | Sweep profile along curve |
| `Boolean` | Union/Difference/Intersect |
| `Subdivision Surface` | Smooth subdivision |
| `Set Material` | Assign materials |

### Matrix Operations (4.2+)
```
Combine Transform → Transform Point/Geometry
Separate Transform → Decompose for editing
Set Instance Transform → Control instances
```

---

## Exporting for 3D Printing

```python
def prepare_for_3d_print(obj):
    """Prepare model for 3D printing."""
    # Apply all modifiers
    bpy.context.view_layer.objects.active = obj
    for modifier in obj.modifiers:
        bpy.ops.object.modifier_apply(modifier=modifier.name)
    
    # Ensure manifold mesh
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.fill_holes()
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Export
    bpy.ops.export_mesh.stl(
        filepath="/path/to/export.stl",
        use_selection=True,
        global_scale=1000  # Convert to mm
    )
```

---

## Keyboard Shortcuts Reference

### Essential Shortcuts
| Action | Key |
|--------|-----|
| Object/Edit Mode | Tab |
| Vertex/Edge/Face | 1/2/3 |
| Grab/Move | G |
| Rotate | R |
| Scale | S |
| Extrude | E |
| Bevel | Ctrl+B |
| Loop Cut | Ctrl+R |
| Inset | I |
| Knife | K |
| Proportional Edit | O |
| Wireframe | Z |
| X-Ray | Alt+Z |
| Camera View | Numpad 0 |
| Front/Side/Top | Numpad 1/3/7 |
| Focus Selected | Numpad . |

---

## Resources

- **Manual**: https://docs.blender.org/manual/
- **Python API**: https://docs.blender.org/api/current/
- **Release Notes**: https://developer.blender.org/docs/release_notes/
- **Community**: https://blender.stackexchange.com/
- **Extensions**: https://extensions.blender.org/

## Version Notes

- **Current LTS**: 4.2 (supported until July 2026)
- **Latest**: 4.3+ (check blender.org)
- **Python Version**: 3.11 (Blender 4.1+)
- **Minimum OpenGL**: 4.3 (Linux/Windows)
- **Metal**: 2.2 (macOS only)
