# Unreal Engine 4 Setup Guide
## Research Document for Performance Supply Depot
**Prepared by:** Jordan, Executive Assistant  
**Date:** 2026-03-16  
**Status:** URGENT - For Da Verse Voxel Project

---

## Overview
Unreal Engine 4 (UE4) is a powerful game engine with industry-leading graphics capabilities. It's the chosen engine for the **Da Verse** voxel planet project due to its robust voxel plugin support and procedural generation capabilities.

**Note:** Unreal Engine 5 is now available, but UE4 is specified for Da Verse due to Voxel Plugin compatibility and established project foundation.

---

## System Requirements

### Minimum Requirements (UE4)

| Component | Specification |
|-----------|---------------|
| **OS** | Windows 10 64-bit (version 20H2 or newer) |
| **Processor** | Quad-core Intel or AMD, 2.5 GHz or faster |
| **Memory** | 8 GB RAM |
| **Graphics Card** | DirectX 11 or 12 compatible GPU |
| **VRAM** | 2 GB minimum |
| **Storage** | 15-20 GB free space (SSD strongly recommended) |

### Recommended for Da Verse (Voxel Generation)

| Component | Specification |
|-----------|---------------|
| **Processor** | Intel i5-8400 or AMD Ryzen 5 2600 or better |
| **Memory** | 16 GB RAM |
| **Graphics Card** | NVIDIA GTX 1060 6GB or AMD RX 580 or better |
| **VRAM** | 6 GB |
| **Storage** | SSD with 50+ GB free |

### For Voxel Plugin Pro
- **Additional RAM:** 32GB recommended for large voxel worlds
- **GPU:** NVIDIA RTX series for best performance with HDRP

---

## Installation Process

### Step 1: Create Epic Games Account
1. Visit: https://www.unrealengine.com/
2. Click "Sign In" → "Create Account"
3. Complete registration

### Step 2: Download Epic Games Launcher
1. Go to: https://www.unrealengine.com/en-US/download
2. Download launcher for your OS
3. Install and sign in

### Step 3: Install Unreal Engine 4
1. Open Epic Games Launcher
2. Navigate to "Unreal Engine" tab
3. Click "Library" in left sidebar
4. Click "+" button to add engine version
5. Select **UE 4.27** (latest stable 4.x version)
   - Or UE 4.26 if specified by Voxel Plugin requirements
6. Click "Install"
7. Select components:
   - **Starter Content** (recommended for learning)
   - **Engine Source** (optional, for advanced users)
   - **Templates and Feature Packs**

### Step 4: Install Voxel Plugin
1. Open Epic Games Launcher
2. Go to "Marketplace" tab
3. Search for "Voxel Plugin"
4. Purchase/download **Voxel Plugin Pro**
   - Price: ~$100-200 (check current pricing)
5. Add to project after creation

### Step 5: Create First Project
1. Open UE4 from Launcher
2. Select "Games" category
3. Choose template:
   - **Blank** (for Da Verse - custom voxel setup)
   - **First Person** (for learning basics)
4. Set project settings:
   - **Blueprint vs C++:** Blueprint recommended for beginners
   - **Raytracing:** Off (for performance)
   - **Starter Content:** Optional
5. Click "Create Project"

---

## Voxel Plugin Information

### What is Voxel Plugin?
Voxel Plugin is a procedural voxel generation system for Unreal Engine that enables:
- Real-time voxel world generation
- Destructible terrain
- Procedural planet generation
- Custom voxel graphs

### Key Features for Da Verse
1. **3D Perlin Noise Support** - For continental generation
2. **Voxel Graph System** - Visual scripting for terrain
3. **Multi-threaded Generation** - Performance optimization
4. **HDRP Compatible** - High-quality rendering

### Installation into Project
1. Open Epic Games Launcher
2. Go to "Library" → "Vault"
3. Find Voxel Plugin
4. Click "Add to Project"
5. Select your Da Verse project
6. Restart Unreal Engine

### Learning Resources for Voxel Plugin
- **Official Wiki:** https://wiki.voxelplugin.com/
- **World Generators:** https://wiki.voxelplugin.com/World_Generators
- **Examples:** https://wiki.voxelplugin.com/Examples
- **Discord Community:** Active support channel

---

## Learning Resources

### Official Epic Resources
- **Unreal Online Learning:** https://www.unrealengine.com/en-US/onlinelearning-courses
  - Free courses for all skill levels
  - "Your First Hour with Unreal Engine"
  - "Blueprint Essentials"

### YouTube Channels
- **Unreal Engine:** Official tutorials
- **Mathew Wadstein:** Blueprint explanations
- **Ryan Laley:** Game development tutorials
- **Voxel Plugin Channel:** Specific to voxel development

### Documentation
- **UE4 Documentation:** https://docs.unrealengine.com/4.27/en-US/
- **Blueprint Reference:** https://docs.unrealengine.com/4.27/en-US/ProgrammingAndScripting/Blueprints/
- **Voxel Plugin Docs:** https://voxelplugin.com/

### Community
- **Unreal Engine Forums:** https://forums.unrealengine.com/
- **Reddit r/unrealengine:** https://www.reddit.com/r/unrealengine/
- **Voxel Plugin Discord:** Check official site for invite

---

## Da Verse Specific Setup

### Project Configuration
1. **Enable Voxel Plugin** in Plugins menu
2. **Set up HDRP** (High Definition Render Pipeline)
3. **Configure World Settings:**
   - Voxel World Actor
   - Voxel Generator (Perlin noise-based)
   - Material setup for single-index + vertex colors

### Recommended Learning Order
1. **Week 1:** UE4 basics, Blueprint fundamentals
2. **Week 2:** Voxel Plugin basics, simple terrain
3. **Week 3:** Perlin noise, continental generation
4. **Week 4:** Biome system, temperature gradients
5. **Week 5:** Materials, foliage placement
6. **Week 6:** Optimization, LOD system

### Reference Projects
- **Voxel Planets (Unity):** https://github.com/josebasierra/voxel-planets
  - Study approach (even though Unity, concepts transfer)
- **Astroneer:** Similar voxel planet aesthetic

---

## Cost Breakdown

| Item | Cost |
|------|------|
| Unreal Engine 4 | FREE (5% royalty after $1M revenue) |
| Voxel Plugin Pro | ~$100-200 (one-time) |
| Marketplace Assets | Varies (optional) |

**Total Initial Investment:** $0-200

---

## Comparison: UE4 vs Unity for Da Verse

| Feature | UE4 | Unity |
|---------|-----|-------|
| Voxel Plugin | ✅ Native, mature | ⚠️ Third-party options |
| Graphics Quality | ✅ Industry-leading | Good |
| Learning Curve | Steeper | Gentler |
| Blueprints | ✅ Visual scripting | C# only |
| Performance | ✅ Excellent for large worlds | Good |
| Asset Store | Good | ✅ Larger selection |

**Verdict:** UE4 is the right choice for Da Verse due to Voxel Plugin maturity and procedural generation capabilities.

---

## Next Steps
1. [ ] Create Epic Games account
2. [ ] Download Epic Games Launcher
3. [ ] Install UE 4.27
4. [ ] Complete "Your First Hour with Unreal Engine"
5. [ ] Purchase Voxel Plugin Pro
6. [ ] Create test voxel project

---

**Document Status:** COMPLETE  
**Next Review:** After UE4 installation
