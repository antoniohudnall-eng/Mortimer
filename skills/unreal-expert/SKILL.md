---
name: unreal-expert
description: Unreal Engine 5 — photorealistic 3D, virtual production, real-time rendering, Blueprints visual scripting, and C++ development.
---

# Unreal Engine 5 Expert Skill

**Version:** 1.0  
**Last Updated:** 2026-03-28  
**Specialization:** High-fidelity 3D, Real-time Rendering, Virtual Production, Photorealistic Visualization

---

## Overview

This skill provides comprehensive expertise in Unreal Engine 5 for creating photorealistic 3D experiences, virtual production workflows, and high-end interactive applications. Covers Nanite virtualized geometry, Lumen dynamic global illumination, MetaHuman characters, Blueprints visual scripting, C++ development, and complete asset pipelines.

---

## Core Technologies

### 1. Nanite - Virtualized Geometry

**What it is:** A virtualized micropolygon geometry system that allows importing film-quality source art with millions/billions of polygons directly into UE5.

**Key Capabilities:**
- Import ZBrush sculpts, photogrammetry scans, CAD models without polygon reduction
- Automatic LOD management - no manual LOD creation needed
- No loss of detail at any distance
- Supports massive scene complexity

**Best Practices:**
```
✓ Enable Nanite on static meshes with >2000 triangles
✓ Use Nanite for: terrain, architecture, hero props, background assets
✓ Keep non-Nanite for: foliage (use WPO), translucent materials, sky spheres, skeletal meshes
✓ Memory: Nanite uses 20-40% more VRAM than traditional LODs but eliminates pop-in
```

**Performance Considerations:**
- Primary View Rays: Nanite renders only visible triangles
- Shadow Maps: Nanite can increase shadow rendering cost
- Lumen Reflections: Higher cost with Nanite geometry
- Translucency: Keep non-Nanite for glass/water

**Import Settings:**
- FBX/OBJ/USD formats supported
- Enable "Build Nanite" in Import Settings
- Adjust "Position Precision" for memory optimization
- Use "Reduction Settings" only if memory is constrained

---

### 2. Lumen - Dynamic Global Illumination

**What it is:** A fully dynamic global illumination and reflections system that reacts immediately to scene and light changes.

**Key Capabilities:**
- Real-time GI without light baking
- Emissive materials contribute to lighting
- Infinite bounces with Final Gather
- Mirror-quality reflections on all surfaces
- Software and Hardware (RTX) ray tracing modes

**Lumen vs. Static Lighting:**
| Feature | Lumen | Baked Lighting |
|---------|-------|----------------|
| Setup Time | Minimal | Hours of baking |
| Iteration Speed | Real-time | Re-bake required |
| Memory | Lower | Higher (lightmaps) |
| Quality | Excellent | Perfect (static) |
| Performance | GPU intensive | CPU/GPU balanced |

**Software Ray Tracing (Default):**
- Uses Screen Space Traces + Signed Distance Fields
- Works on all GPUs
- Fallback for off-screen geometry
- Configurable in Project Settings → Rendering → Global Illumination

**Hardware Ray Tracing (RTX):**
- Requires DX12 and RT-capable GPU
- Higher quality reflections and GI
- Enable: Project Settings → Rendering → Hardware Ray Tracing
- Combine with "Generate Mesh Distance Fields" for best results

**Lumen Settings:**
```
PostProcessVolume Settings:
- Lumen Global Illumination: Enabled
- Final Gather Quality: 1-4 (2 default, 4 for production)
- Final Gather Lighting Update Speed: 1-4
- Reflections Method: Lumen
- Reflections Quality: 1-4
- Max Reflection Bounces: 1-8
```

**Optimization:**
- Use Console Command: `Stat GPU` to monitor Lumen cost
- Reduce `r.Lumen.Reflections.Allow` for scenes without mirror needs
- Limit emissive surface count (each adds cost)
- Use Lumen Scene Direct Lighting for outdoor scenes

---

### 3. MetaHuman Creator

**What it is:** A cloud-based tool for creating photorealistic digital humans, fully rigged and ready for animation in UE5.

**Pipeline:**
1. Create in MetaHuman Creator (web-based)
2. Download to Quixel Bridge
3. Import to UE5 via Bridge Plugin
4. Animate with Control Rig or Live Link Face

**MetaHuman Components:**
- **Face:** 52 ARKit blend shapes, wrinkle maps, subsurface scattering
- **Body:** 8K textures, LOD system, compatible with Mixamo/UE5 skeleton
- **Hair:** Strand-based grooming, physics simulation
- **Clothing:** Modular outfit system

**Performance Levels:**
| Level | Triangles | Use Case |
|-------|-----------|----------|
| LOD0 | ~80K | Cinematic close-up |
| LOD1 | ~40K | Gameplay close-up |
| LOD2 | ~20K | Mid-distance |
| LOD3 | ~10K | Background |

**Animation Methods:**
1. **Live Link Face:** iPhone TrueDepth camera → real-time face capture
2. **ARKit Blendshapes:** Standard iOS face tracking
3. **Control Rig:** Manual/keyframe animation in Sequencer
4. **Motion Capture:** Vicon, Rokoko, XSens integration

**MetaHuman Blueprint Setup:**
```cpp
// Get Face Mesh for blendshape control
USkeletalMeshComponent* FaceMesh = GetFaceMesh();

// Set blendshape value
FaceMesh->SetMorphTarget("EyeBlinkLeft", 0.5f);
```

---

## Blueprints Visual Scripting

### Core Concepts

**Event Graph:** Visual node-based programming
- **White Lines:** Execution flow
- **Blue Lines:** Data flow (variables, returns)
- **Green Lines:** Object references
- **Pink Lines:** Strings/Text
- **Light Blue:** Structs/Vectors

**Key Nodes:**

| Node | Function |
|------|----------|
| Event BeginPlay | Runs once when actor spawns |
| Event Tick | Runs every frame |
| Event ActorBeginOverlap | Triggered on collision enter |
| Branch | If/Then/Else logic |
| For Each Loop | Iterate through arrays |
| Timeline | Animation curves over time |
| Set Timer by Function Name | Delayed/repeating execution |

### Variable Types

```cpp
// Blueprint Variable Categories
Boolean     // True/False
Integer     // Whole numbers
Float       // Decimal numbers
String      // Text
Name        // Optimized string for identifiers
Text        // Localized text
Vector      // X,Y,Z coordinates
Rotator     // Pitch, Yaw, Roll
Transform   // Location + Rotation + Scale
Object      // Reference to UObject
Class       // Reference to UClass
Array       // Ordered collection
Set         // Unique unordered collection
Map         // Key-Value pairs
```

### Communication Methods

**1. Direct Reference:**
```blueprint
Get Actor of Class → Store in Variable → Call Function
```

**2. Event Dispatchers:**
```blueprint
// Broadcasting Actor:
Create Event Dispatcher "OnHealthChanged"
Bind Event in receiving actors
Call "OnHealthChanged" when health changes

// Receiving Actor:
Bind Event to Dispatcher
Execute custom logic on event
```

**3. Blueprint Interfaces:**
```blueprint
// Create Interface with function "Interact"
// Implement Interface in multiple Blueprints
// Call "Interact" on any actor implementing it
```

**4. Casting:**
```blueprint
Get Player Character → Cast To MyCharacter → Access custom variables/functions
```

---

## C++ Development

### Project Setup

**Module Structure:**
```
Source/
├── MyProject/
│   ├── MyProject.Build.cs          # Module dependencies
│   ├── MyProject.h                 # Precompiled header
│   ├── MyProject.cpp               # Module implementation
│   ├── Public/
│   │   └── MyCharacter.h
│   └── Private/
│       └── MyCharacter.cpp
```

**Basic Actor Class:**
```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "MyActor.generated.h"

UCLASS()
class MYPROJECT_API AMyActor : public AActor
{
    GENERATED_BODY()
    
public:
    AMyActor();
    
    // Called every frame
    virtual void Tick(float DeltaTime) override;
    
    // Called when game starts
    virtual void BeginPlay() override;
    
protected:
    // Visible in Editor
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="My Properties")
    float MyFloatProperty;
    
    UPROPERTY(EditDefaultsOnly, Category="My Properties")
    UStaticMeshComponent* MeshComponent;
    
    UPROPERTY(EditAnywhere, Category="My Properties")
    FVector TargetLocation;
    
    // Callable from Blueprint
    UFUNCTION(BlueprintCallable, Category="My Functions")
    void MyFunction();
    
    UFUNCTION(BlueprintPure, Category="My Functions")
    float GetMyValue() const;
    
    UFUNCTION(BlueprintImplementableEvent, Category="My Events")
    void OnCustomEvent();
    
    UFUNCTION(BlueprintNativeEvent, Category="My Events")
    void OnEventWithCpp();
    virtual void OnEventWithCpp_Implementation();
};
```

**Property Specifiers:**
```cpp
EditAnywhere          // Editable in BP and instances
EditDefaultsOnly      // Editable in BP only
EditInstanceOnly      // Editable in placed instances only
VisibleAnywhere       // Visible but not editable
BlueprintReadOnly     // Readable in BP, not writable
BlueprintReadWrite    // Full access in BP
Category="Name"       // Organizes in Details panel
Meta=(ClampMin="0")   // Validation
```

**Common UE5 Types:**
```cpp
// Core Types
FString     // Dynamic string
FName       // Immutable, hashed string
FText       // Localized string
FVector     // 3D vector (X,Y,Z)
FRotator    // Rotation (Pitch, Yaw, Roll)
FTransform  // Location + Rotation + Scale
FColor      // RGBA 0-255
FLinearColor // RGBA 0.0-1.0

// UObject types
AActor*     // Actor pointer
UObject*    // Object pointer
TSubclassOf<AActor>  // Class reference
TArray<T>   // Dynamic array
TMap<K,V>   // Hash map
TSet<T>     // Hash set
```

---

## Lighting Systems

### Light Types

**Directional Light:**
- Simulates sun/moon (infinite distance)
- Uses Cascaded Shadow Maps (CSM)
- Settings: Num Cascades, Cascade Distribution, Shadow Distance
- Enable "Atmosphere Sun Light" for Time of Day systems

**Point Light:**
- Omnidirectional light source
- Attenuation Radius defines influence
- Use "Inverse Square Falloff" for physically correct light
- IES profiles for realistic distribution

**Spot Light:**
- Cone-shaped light
- Inner/Outer Cone Angles for softness
- Good for flashlights, stage lights

**Rect Light:**
- Area light source
- Soft shadows by default
- Higher quality but more expensive
- Best for windows, fluorescent tubes

**Sky Light:**
- Captures environment for ambient lighting
- Real Time Capture for dynamic skies
- Static for baked lighting

### Lighting Mobility

| Mobility | Shadows | Performance | Use Case |
|----------|---------|-------------|----------|
| Static | Baked | Best | Never moves, unchanging |
| Stationary | Baked + Dynamic | Good | Light moves, geometry static |
| Movable | Fully dynamic | Worst | Characters, vehicles, FX |

### Post Processing

**Essential Settings for Photorealism:**
```
PostProcessVolume (Unbound = affects all):
├─ Lens
│  ├─ Bloom: Intensity 0.5-1.0, Threshold 1.0
│  ├─ Lens Flares: Intensity 0.1-0.3
│  └─ Chromatic Aberration: 0.1-0.3
├─ Color Grading
│  ├─ Temperature: Adjust warmth/coolness
│  ├─ Tint: Green/Magenta balance
│  ├─ Saturation: 0.8-1.2
│  └─ Contrast: 1.0-1.1
├─ Film
│  ├─ Slope: 0.88
│  ├─ Toe: 0.55
│  ├─ Shoulder: 0.26
│  └─ Black Clip: 0.0
├─ Motion Blur: Amount 0.5, Max 1.0
├─ Depth of Field: Bokeh, adjust F-stop
└─ Auto Exposure: Histogram mode, Speed Up/Down
```

---

## Materials System

### Material Domains

**Surface:** Default opaque/transparent materials
**Deferred Decal:** Projected onto surfaces
**Light Function:** Animated light patterns
**Volume:** Fog, clouds, atmospheric effects
**Post Process:** Screen-space effects

### Blend Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| Opaque | No transparency | Most materials |
| Masked | Binary transparency (clip) | Foliage, chainlink |
| Translucent | Full transparency | Glass, water |
| Additive | Adds to background | Glow, particles |
| Modulate | Multiplies with background | Darkening effects |

### Key Material Nodes

**Base Color:** Surface color (albedo) - no lighting info
**Metallic:** 0 = dielectric (plastic), 1 = metal (uses base color as reflectivity)
**Specular:** Legacy, use Metallic workflow instead
**Roughness:** 0 = mirror, 1 = diffuse
**Normal:** Surface detail without geometry
**Emissive:** Self-illumination (light emitting)
**Ambient Occlusion:** Cavity shadows
**Subsurface:** Skin, wax, jade scattering

### Advanced Techniques

**Parallax Occlusion Mapping (POM):**
- Deep surface relief without geometry
- Enable in Material → Tessellation
- Heightmap input
- Performance: Medium cost

**Subsurface Scattering:**
- Enable in Material Settings
- Use Subsurface Profile for skin
- Adjust Scatter Radius, Color
- Essential for MetaHumans

**Clear Coat:**
- Dual-layer shading
- Top layer: Clear coat (paint, lacquer)
- Base layer: Underlying material
- Roughness for each layer separately

**Material Functions:**
- Reusable node networks
- Create library of effects
- Inputs/Outputs for flexibility
- Organize complex materials

---

## Physics Systems

### Chaos Physics Engine

**Collision Types:**
- **Query Only:** Traces/overlaps only, no physics response
- **Physics Only:** Physical response, no queries
- **Collision Enabled:** Both query and physics

**Collision Presets:**
```
Pawn                // Character movement
Vehicle             // Car physics
PhysicsActor        // Simulated objects
Destructible        // Breakable objects
BlockAll            // Solid wall
OverlapAll          // Trigger volumes
Custom...           // User-defined
```

**Physics Bodies:**
```cpp
// In Blueprint
Add Impulse           // Instant force
Add Force             // Continuous force
Add Torque            // Rotational force
Set Physics Linear Velocity
Set Physics Angular Velocity
Set Simulate Physics  // Enable/disable
Wake Rigid Body       // Activate sleeping body
```

**Physical Materials:**
- Define surface properties
- Friction, Restitution (bounciness)
- Density for mass calculation
- SoundFX and Footstep mapping

### Constraints

**Physics Constraint Component:**
- Hinge, Prismatic, Skeletal constraints
- Linear/Angular limits
- Motors and springs
- Breakable thresholds

---

## Asset Pipeline

### Importing Assets

**3D Models (FBX/OBJ/USD):**
```
Import Settings:
├─ Mesh
│  ├─ Generate Lightmap UVs: On (for baked lighting)
│  ├─ Transform Vertex Color: If needed
│  ├─ Build Nanite: On for hero assets
│  └─ Combine Meshes: Per object or single
├─ Materials
│  ├─ Import Materials: Usually OFF (rebuild in UE)
│  └─ Import Textures: Usually OFF
└─ Animation
   ├─ Animation Length: Key Range/Exported Time
   └─ Import Animations: On for skeletal meshes
```

**Textures:**
```
Supported: PNG, TGA, BMP, HDR, EXR, TIFF, JPEG, DDS
Recommended: PNG (RGBA), TGA (legacy), EXR (HDR)

Texture Types:
├─ Default          // Standard textures
├─ Normal Map       // Tangent space normals
├─ Mask             // Single channel data
├─ Linear Color     // Non-color data (roughness, metallic)
├─ HDR              // High dynamic range
├─ Subsurface       // Skin scattering
└─ Vector Displacement // Advanced displacement

Compression Settings:
├─ Default (DXT1/5)    // Color textures
├─ Normalmap (BC5)     // Normal maps
├─ Displacementmap     // Height/displacement
├─ VectorDisplacementmap
└─ UserInterface2D     // UI elements (uncompressed)
```

### Optimization

**Texture Streaming:**
- Automatically loads appropriate resolution
- Console command: `Stat Streaming`
- Pool size in engine settings
- Memory budget per platform

**LODs (Level of Detail):**
```
For Nanite: Automatic
For Traditional:
├─ Create 3-4 LOD levels
├─ 50% triangle reduction per level
├─ Screen Size determines switch
└─ Use Simplygon or manual reduction
```

**Draw Call Optimization:**
- Merge actors (Modular to Static)
- Use instanced static meshes
- Limit unique materials
- Hierarchical LOD (HLOD) for distant views

**Culling:**
```
Distance Culling: Fade out distant objects
Frustum Culling: Automatic (objects outside camera)
Occlusion Culling: Objects behind others
Precomputed Visibility: Bake for static scenes
```

### Packaging

**Build Configurations:**
| Config | Optimization | Debug | Use Case |
|--------|--------------|-------|----------|
| Debug | None | Full | Engine debugging |
| DebugGame | Some | Full | Game debugging |
| Development | Some | Some | Iteration |
| Test | Full | Some | QA testing |
| Shipping | Full | None | Release |

**Packaging Settings:**
```
Project Settings → Packaging:
├─ Build Configuration: Shipping/Development
├─ Include Debug Files: Off for Shipping
├─ Use Pak File: On (single package)
├─ Create Compressed Cooked Packages: On
├─ Cook everything in the project: As needed
└─ List of maps to include in a packaged build

Platforms:
├─ Windows (64-bit)
├─ Linux
├─ macOS
├─ Android (ES3.1, Vulkan)
├─ iOS (Metal)
├─ PlayStation 5
├─ Xbox Series X|S
└─ HTML5 (WebAssembly)
```

---

## Virtual Production

### In-Camera VFX (ICVFX)

**LED Volume Setup:**
- nDisplay for multi-display rendering
- Camera tracking (Motive, Vicon, Antilatency)
- Live sync with physical camera
- Genlock for frame synchronization

**Key Components:**
1. **nDisplay Config:** Define display topology
2. **Camera Calibration:** Match physical to virtual
3. **Live Link:** Real-time data streaming
4. **Timecode Sync:** Frame-accurate recording

**Optimization for ICVFX:**
- Target 24fps+ for real-time playback
- Use Nanite for set extension geometry
- Optimize inner frustum (camera view) only
- Outer frustum (LED walls) can use lower quality

### Remote Control

**Web Interface:**
- Control UE5 from tablet/browser
- Adjust lights, camera, environment
- HTTP API for external integration

**OSC (Open Sound Control):**
- Protocol for entertainment systems
- Control from lighting boards, audio mixers
- Real-time parameter adjustment

---

## Common Blueprint Patterns

See `/blueprints/` directory for complete examples.

### Pattern Summary:

1. **Interaction System** - Raycast-based interactables
2. **Health/Damage** - Component-based damage handling
3. **Inventory** - Data-driven item management
4. **State Machine** - Enum-based state switching
5. **Timeline Animation** - Smooth value interpolation
6. **Event Queue** - Buffered action system
7. **Pooling** - Object reuse for performance

---

## Console Commands Reference

```
Stat FPS              // Show frame rate
Stat Unit             // Frame time breakdown
Stat GPU              // GPU profiling
Stat Memory           // Memory usage
Stat Streaming        // Texture streaming

ShowFlag.PostProcessing 0/1  // Toggle post FX
ShowFlag.Lighting 0/1        // Toggle all lighting
ShowFlag.Shadows 0/1         // Toggle shadows

r.ScreenPercentage    // Render scale (50-200)
r.VSync               // VSync on/off
r.TemporalAA.Quality  // TAA quality 0-4
r.MipMap.LodBias      // Texture quality offset

stat sceneupdate      // Scene update stats
stat initviews        // Visibility stats
stat game             // Game thread stats

ke * 1                // Show all collisions
show collision        // Toggle collision visibility
```

---

## Resources & References

- **Official Docs:** https://docs.unrealengine.com/
- **Learn Portal:** https://www.unrealengine.com/en-US/learn
- **Marketplace:** https://www.unrealengine.com/marketplace
- **Quixel Megascans:** https://quixel.com/megascans
- **MetaHuman:** https://metahuman.unrealengine.com
- **Forums:** https://forums.unrealengine.com/
- **Discord:** Unreal Slackers

---

## Skill Usage

This skill is loaded automatically for UE5 development tasks. Key capabilities:

- Generate optimized Blueprints for common systems
- Provide C++ code patterns and best practices
- Troubleshoot performance and rendering issues
- Guide asset import and optimization workflows
- Configure virtual production setups
- Debug lighting, materials, and physics

See `/examples/` for sample implementations and `/references/` for external documentation.
