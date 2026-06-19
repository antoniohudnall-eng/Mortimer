# N'OG NOG v3.0 - Universal Explorer

A browser-based 3D procedural galaxy exploration game using Three.js.

## Overview

N'OG NOG is a Universal Explorer game that generates infinite procedural galaxies with:
- Multiple galaxy types (Spiral, Barred Spiral, Elliptical, Irregular, Ring)
- Procedurally generated stars with realistic colors and sizes
- Multi-platform support (Desktop, Mobile, Tablet)
- Platform-optimized rendering settings
- Touch controls for mobile devices
- Spatial audio

## Features

### Galaxy Types
- **Spiral** - Logarithmic arms with young stars
- **Barred Spiral** - Central bar connecting spiral arms
- **Elliptical** - Smooth, featureless, older stars
- **Irregular** - Chaotic, no defined structure
- **Ring** - Central void surrounded by star ring

### Platform Tiers

The game automatically detects device capabilities and optimizes:

| Tier | Stars | Pixel Ratio | Shadows | Bloom |
|------|-------|-------------|---------|-------|
| ULTRA | 50000 | 1.5 | Yes | Yes |
| HIGH | 25000 | 1.25 | Yes | No |
| MEDIUM | 10000 | 1.0 | No | No |
| LOW | 5000 | 0.8 | No | No |
| MINIMAL | 2500 | 0.6 | No | No |

## Quick Start

### Web (Browser)
```bash
cd /root/.openclaw/workspace/nognog/v3
# Serve with any static server
python3 -m http.server 8080
# Open http://localhost:8080
```

### Desktop PWA
1. Open the game in Chrome/Edge
2. Click "Install" in the address bar
3. Launch as standalone app

### Mobile APK
```bash
cd /root/.openclaw/workspace/nognog/v3/mobile
# Build with Capacitor
npm run build:android
```

## Controls

### Desktop
- **WASD** - Movement
- **Mouse** - Look around
- **G** - Toggle galaxy view
- **ESC** - Open menu

### Mobile
- **Left joystick** - Movement
- **Thrust button** - Accelerate
- **Touch drag** - Look around

## Tech Stack

- **Three.js r128** - 3D rendering
- **Simplex Noise** - Procedural generation
- **Capacitor** - Mobile wrapper
- **Web Audio API** - Spatial sound

## Architecture

```
nognog/v3/
├── index.html          # Main game entry
├── js/
│   ├── core/           # Platform detection, game loop
│   ├── universe/       # Galaxy generation
│   └── player/         # Player controller
├── mobile/             # Capacitor wrapper
└── assets/             # Audio, textures
```

## Building

### Prerequisites
- Node.js 18+
- Android SDK (for APK)
- Xcode (for iOS)

### Build Commands
```bash
# Web version
npm run build:web

# Android APK
cd mobile && npx cap sync && ./gradlew assembleRelease

# iOS IPA
cd mobile && npx cap open ios
```

## Deployment

- **Web:** Deploy `index.html` and `js/` to any static host
- **APK:** `./mobile/android/app/build/outputs/apk/release/app-release.apk`
- **PWA:** Serve with HTTPS, install from browser

## License

MIT - See LICENSE file

---
*Built for the AGI Company Universe*
