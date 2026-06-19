# Lumen & Nanite Configuration Guide

## Lumen Global Illumination

### What is Lumen?
Lumen is UE5's fully dynamic global illumination and reflections system. It provides:
- Real-time diffuse indirect lighting (bounces)
- Dynamic reflections
- Works with any light type
- No lightmap baking required

### Project Settings

#### Enable Lumen
```
Edit → Project Settings → Engine - Rendering
├── Global Illumination: Lumen
├── Reflections: Lumen
└── Software Ray Tracing Mode: Global Tracing (default)
```

#### Engine.ini Configuration
```ini
[/Script/Engine.RendererSettings]
; Enable Lumen
r.DynamicGlobalIlluminationMethod=1
r.ReflectionMethod=1

; Lumen Quality
r.Lumen.Reflections.Allow=1
r.Lumen.Reflections.Reflections=1
r.Lumen.Reflections.SmoothBias=0.5

; Screen Tracing (for close-proximity GI)
r.Lumen.ScreenProbeGather.ScreenTraces=1

; Hardware Ray Tracing (if GPU supports)
r.RayTracing=1
r.Lumen.HardwareRayTracing=1
```

### Blueprint Control

#### BP_PostProcessVolume
```
Components:
└── PostProcessComponent

Settings:
├── Global Illumination Method: Lumen
├── Reflection Method: Lumen
├── Lumen Reflection Quality: 4 (0-5)
├── Lumen Final Gather Quality: 4 (0-5)
├── Lumen Max Reflection Bounces: 3
└── Lumen Max Trace Distance: 10000

Priority: 1.0 (overrides world settings)
Blend Weight: 1.0
Unbound: True (affects entire world)
```

### Performance Optimization

#### Quality vs Performance
```
High-End PC (RTX 3070+):
├── Reflection Quality: 5
├── Final Gather Quality: 5
├── Hardware Ray Tracing: On
└── Target: 1440p@60fps or 4K@30fps

Mid-Range PC (GTX 1660):
├── Reflection Quality: 3
├── Final Gather Quality: 3
├── Hardware Ray Tracing: Off
└── Target: 1080p@60fps

Low-End/Console:
├── Reflection Quality: 2
├── Final Gather Quality: 2
├── Screen Space Reflections: Fallback
└── Target: 1080p@30fps
```

## Nanite Virtualized Geometry

### What is Nanite?
Nanite is UE5's virtualized micropolygon geometry system:
- Import film-quality source assets
- Auto-LOD without manual setup
- Massive object counts
- Only renders visible pixels

### Enabling Nanite

#### Per-Asset
```
Static Mesh Editor → Details Panel
├── Nanite Settings
│   ├── Enable Nanite Support: ✓
│   ├── Position Precision: Auto
│   ├── Triangle Percent: 100%
│   └── Relative Error: 0%
```

#### Bulk Import Settings
```
Import Settings Dialog:
├── Build Nanite: ✓
├── Generate Lightmap UVs: ✓
├── Transform Vertex Color: ✓
└── LOD Group: Large Prop (adjust based on asset)
```

### Blueprint: Nanite Toggle System

```
BP_NaniteManager (Actor)

Variables:
├── IsNaniteEnabled (bool)
├── NaniteMeshes (Array of StaticMesh)
└── FallbackLODs (Array of StaticMesh)

Functions:

Function: ToggleNanite
    ├── For Each Mesh in NaniteMeshes
    │   ├── Get Mesh Component
    │   ├── Set Nanite Enabled = IsNaniteEnabled
    │   └── If Not Enabled: Set LOD Group = Small Prop
    └── Update UI Notification

Function: CheckPlatformSupport
    ├── Get Platform Name
    ├── Switch on Platform
    │   ├── PS5, XSX, PC: Enable Nanite
    │   ├── Switch, Mobile: Disable Nanite
    │   └── Use Fallback LODs
    └── Call ToggleNanite
```

### Material Considerations

#### Nanite-Compatible Materials
```
Material Domain: Surface
Blend Mode: Opaque (best performance)
Shading Model: Lit

Notes:
- Masked materials supported (r.Nanite.AllowMaskedMaterials=1)
- Translucent materials: Use traditional LOD
- World Position Offset: Supported
- Pixel Depth Offset: Supported
```

#### BP_MaterialOptimizer
```
Function: SetupNaniteMaterial
    ├── Input: MaterialInstance
    ├── If Nanite Mesh:
    │   ├── Set Parent = M_Nanite_Master
    │   └── Set Scalar Parameter: Nanite_Dither=0
    └── Return: Optimized Material Instance
```

## Virtual Shadow Maps (VSM)

### Configuration
```ini
[/Script/Engine.RendererSettings]
r.Shadow.Virtual.MaxResolutionBits=23
r.Shadow.Virtual.MaxPhysicalPages=2048
r.Shadow.Virtual.ClipmapVirtualMaxResolution=1024
```

### Blueprint Settings
```
Directional Light Component:
├── Cast Shadows: On
├── Shadow Map Method: Virtual Shadow Maps
├── Virtual Shadow Map Clipmaps: 5
└── Max Draw Distance: 0 (infinite)

Point/Spot Lights:
├── Cast Shadows: On (for key lights only)
└── Shadow Map Method: Virtual Shadow Maps
```

## Optimization Checklist

### Scene Setup
```
World Settings:
├── Force No Precomputed Lighting: ✓ (for full dynamic)
├── Static Lighting Level Scale: 1.0
├── Num Indirect Lighting Bounces: 3
└── Generate Lightmap UVs: Off (if using Lumen)

Post Process Volume:
├── Global Illumination: Lumen
├── Reflections: Lumen
├── Dynamic Global Illumination: 1.0
├── Reflections Quality: 1.0
└── Motion Blur: Off (performance)
```

### Performance Commands (Console)
```
Stat Lumen                # View Lumen stats
Stat Nanite               # View Nanite stats
Stat VirtualShadowMap     # View VSM stats
r.Lumen.Reflections.Allow 0    # Disable reflections
r.Nanite.MaxPixelsPerEdge 2.0  # Reduce Nanite quality
r.Shadow.Virtual.MaxResolutionBits 22  # Lower shadow res
```

### Platform-Specific Profiles

#### BP_PlatformProfile (Data Asset)
```
Structure: FPlatformGraphicsSettings
├── PlatformName (String)
├── UseLumen (bool)
├── UseNanite (bool)
├── UseHardwareRT (bool)
├── ShadowResolution (int)
├── ViewDistanceScale (float)
├── PostProcessQuality (int)
└── EffectsQuality (int)

Default Profiles:
├── Profile_PC_High
├── Profile_PC_Medium
├── Profile_PC_Low
├── Profile_PS5
├── Profile_XSX
└── Profile_Mobile
```

## Blueprint: Dynamic Quality Adjuster

```
BP_QualityManager (GameInstance Subsystem)

Event Initialize
    ├── Detect Hardware (via C++ or Console Command)
    ├── Load Platform Profile
    └── Apply Settings

Function: ApplySettings
    ├── Set Post Process Values
    ├── Update Console Variables
    │   ├── Execute Console Command: r.Lumen.*
    │   ├── Execute Console Command: r.Nanite.*
    │   └── Execute Console Command: r.Shadow.*
    └── Save to Game User Settings

Event OnFrameTimeSpike
    ├── If Frame Time > Target:
    │   ├── Reduce Shadow Quality
    │   ├── Reduce Lumen Quality
    │   └── Log: "Quality reduced due to performance"
    └── If Frame Time < Target - Threshold:
        ├── Increase Quality
        └── Log: "Quality increased"
```

## Testing & Validation

### Console Commands
```
ShowFlag.LumenDiffuseIndirect 1    # Visualize GI
ShowFlag.LumenReflections 1          # Visualize reflections
ShowFlag.NaniteClusters 1            # Show Nanite clusters
ShowFlag.VirtualShadowMap 1           # Show VSM pages
```

### Blueprint Debug Widget
```
W_DebugInfo
├── Overlay (Screen)
│   ├── Vertical Box (Top Left)
│   │   ├── Text: "Lumen: " + GetSetting
│   │   ├── Text: "Nanite: " + GetStat
│   │   ├── Text: "Shadows: " + GetMethod
│   │   └── Text: "FPS: " + Calculate FPS
```
