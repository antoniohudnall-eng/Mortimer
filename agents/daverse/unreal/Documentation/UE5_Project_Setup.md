# DaVerse & AGI Company UE5 Project Setup Guide

## Project Structure

```
DaVerse/
├── Config/
│   ├── DefaultEngine.ini          # Engine settings, Lumen/Nanite config
│   ├── DefaultGame.ini            # Game-specific settings
│   ├── DefaultInput.ini           # Input mappings
│   └── DefaultScalability.ini     # Quality presets
├── Content/
│   ├── Characters/                 # Player & NPC assets
│   ├── Environment/                # World assets
│   ├── UI/                         # UMG widgets
│   └── Sounds/                     # Audio assets
├── Source/
│   └── DaVerse/                    # C++ modules (if needed)
└── DaVerse.uproject
```

## Engine Configuration

### DefaultEngine.ini
```ini
[/Script/Engine.RendererSettings]
r.DefaultFeature.AutoExposure.ExtendDefaultLuminanceRange=True
r.DefaultFeature.AutoExposure.ExtendDefaultLuminanceRange=True
r.DefaultFeature.LocalExposure.HighlightContrastScale=0.8
r.DefaultFeature.LocalExposure.ShadowContrastScale=0.8
r.DefaultFeature.LocalExposure.DetailStrength=1.0
r.DefaultFeature.LocalExposure.BlurredLuminanceBlend=0.6

; Lumen Global Illumination
r.DynamicGlobalIlluminationMethod=1
r.ReflectionMethod=1

; Nanite
r.Nanite.AllowMaskedMaterials=1
r.Nanite.MaxPixelsPerEdge=1.0

; Virtual Shadow Maps
r.Shadow.Virtual.MaxResolutionBits=23
```

## Quality Presets

### Scalability Settings

| Setting | Low | Medium | High | Epic | Cinematic |
|---------|-----|--------|------|------|-----------|
| View Distance | 3 | 4 | 5 | 6 | 8 |
| Anti-Aliasing | 1 | 2 | 3 | 4 | 6 |
| Post-Process | 2 | 4 | 5 | 6 | 8 |
| Shadows | 2 | 4 | 5 | 6 | 8 |
| Global Illumination | 3 | 4 | 5 | 6 | 8 |
| Reflections | 2 | 4 | 5 | 6 | 8 |
| Effects | 2 | 4 | 5 | 6 | 8 |
| Foliage | 2 | 4 | 5 | 6 | 8 |

## Platform-Specific Notes

### Console (PS5/Xbox Series X)
- Lumen: Hardware Ray Tracing
- Nanite: Full support
- Target: 4K@60fps or 1080p@120fps

### PC High-End
- Lumen: Software or Hardware RT
- Nanite: Full support
- DLSS/FSR integration recommended

### Mobile/Meta Quest
- Lumen: Off (use Static Lighting)
- Nanite: Off (fallback to traditional LOD)
