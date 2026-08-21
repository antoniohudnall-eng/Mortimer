# Game Creation Skill

## Overview
Capability to create browser-based games using Three.js, HTML5, and JavaScript with modular architecture.

## Version History
| Version | Date | Notes |
|---------|------|-------|
| v1.0 | 2026-04-07 | Initial capability - Universal Explorer style voxel games |

## Capabilities
- **3D Voxel Games**: Infinite procedurally generated universes
- **Physics**: Real gravitational mechanics, orbital dynamics
- **Multi-Platform**: Keyboard, mouse, touch controls
- **Audio**: Spatial sound effects, ambient audio
- **UI**: Canvas-based HUDs, mini-maps

## Architecture Pattern
```
game/
├── index.html          # Main entry
├── nognog-pro.html     # Pro enhanced version
├── css/
│   └── styles.css
├── js/
│   ├── core/           # Component system, ECS
│   ├── universe/       # Procedural generation
│   ├── player/         # Controls, physics
│   ├── render/         # Three.js rendering
│   └── game.js         # Main game loop
└── assets/
    └── audio/          # .wav/.ogg files
```

## Key Libraries
- Three.js (r128+) - 3D rendering
- Simplex Noise - Procedural generation
- Web Audio API - Spatial audio

## Deployment
1. Deploy to `/var/www/<domain>/nog/`
2. Symlink from workspace `nognog/game/`
3. Git commit to AOS-Brain repo

## Examples
- N'og nog (2026-04-07): Universal Explorer
  - 100x100x100 voxel universe
  - 6 universe types
  - Multi-camera modes
  - Full physics

## Usage
```bash
# Create new game
mkdir -p games/<name>/
# Follow architecture pattern
# Deploy
sudo cp -r games/<name>/* /var/www/<domain>/
```

## Created By
Miles (AOS-Brain) + Antonio Hudnall
Agent Verse Technology
