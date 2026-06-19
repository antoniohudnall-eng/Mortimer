# Unity Engine Setup Guide
## Research Document for Performance Supply Depot
**Prepared by:** Jordan, Executive Assistant  
**Date:** 2026-03-16  
**Status:** URGENT - For Miles' Game Development Training

---

## Overview
Unity is a powerful cross-platform game engine ideal for 2D and 3D game development. It's particularly well-suited for the Milk Man Game (2D platformer) and can also support future 3D projects.

---

## System Requirements

### Minimum Requirements (Unity 6.3)

| Component | Windows | macOS | Linux |
|-----------|---------|-------|-------|
| **OS Version** | Windows 10 v21H1+ (x64) / Windows 11 21H2+ (Arm64) | Ventura 13+ | Ubuntu 22.04/24.04 |
| **CPU** | x64 with SSE2 / Arm64 | x64 with SSE2 / Apple M1+ | x64 with SSE2 |
| **GPU** | DX10/DX11/DX12 or Vulkan | Metal-capable Intel/AMD | OpenGL 3.2+ or Vulkan |
| **RAM** | 4GB minimum, 8GB recommended | 4GB minimum, 8GB recommended | 4GB minimum, 8GB recommended |
| **Storage** | 10GB+ free space | 10GB+ free space | 10GB+ free space |

### For 2D Games (Milk Man Game)
- **Recommended:** Intel i5/AMD Ryzen 5 or better
- **GPU:** Any dedicated GPU from 2015+ or modern integrated graphics
- **RAM:** 8GB minimum for smooth workflow

---

## Installation Process

### Step 1: Download Unity Hub
1. Visit: https://unity.com/download
2. Download Unity Hub for your OS
3. Unity Hub is the recommended way to manage Unity installations

### Step 2: Install Unity Hub
- **Windows:** Run installer, follow prompts
- **macOS:** Drag to Applications folder
- **Linux:** Extract and run AppImage or install via package manager

### Step 3: Create Unity Account
- Sign up at https://id.unity.com/
- Choose license type:
  - **Personal:** Free (revenue <$100K/year)
  - **Plus/Pro:** Paid tiers with additional features

### Step 4: Install Unity Editor
1. Open Unity Hub
2. Go to "Installs" tab
3. Click "Install Editor"
4. Select version (recommend Unity 6 LTS for stability)
5. Choose modules:
   - **Android Build Support** (for DroidScript/Milk Man Game)
   - **Windows/Mac/Linux Build Support**
   - **Documentation**
   - **Visual Studio Code** (optional but recommended)

### Step 5: Create First Project
1. Click "New Project"
2. Select template:
   - **2D (URP)** for Milk Man Game
   - **3D** for future projects
3. Name project and choose location
4. Click "Create Project"

---

## Learning Resources

### Official Unity Learn (Free)
- **URL:** https://learn.unity.com/
- **Get Started with Unity:** Guided tour ending in your first 3D scene
- **Game Development Pathway:** Validated foundational skills for job seekers
- **Courses:** Step-by-step tutorials with projects
- **Pathways:** Guided learning experiences for beginners

### Recommended Learning Path for 2D Games

#### Week 1: Basics
1. **Unity Essentials** (learn.unity.com)
   - Editor interface
   - GameObjects and Components
   - Scene building

2. **2D Game Kit** (Unity Asset Store - Free)
   - Pre-built 2D game to study
   - Learn platformer mechanics

#### Week 2: Scripting
1. **C# Fundamentals**
   - Variables, functions, classes
   - Unity-specific APIs
   - MonoBehaviour lifecycle

2. **2D Physics**
   - Rigidbody2D
   - Colliders
   - Movement scripts

#### Week 3: Game Mechanics
1. **Animation**
   - Sprite animation
   - Animator Controller
   - State machines

2. **Input System**
   - Touch controls (for mobile)
   - Keyboard controls (for testing)

### YouTube Channels
- **Brackeys:** Excellent beginner tutorials (archived but still relevant)
- **Code Monkey:** Unity-specific tutorials
- **Unity:** Official channel with live sessions

### Documentation
- **Unity Manual:** https://docs.unity3d.com/Manual/
- **Scripting API:** https://docs.unity3d.com/ScriptReference/
- **Community Forums:** https://forum.unity.com/

---

## Best Practices for 2D Games

### Project Structure
```
Assets/
├── Scripts/           # C# scripts
├── Sprites/           # 2D graphics
├── Animations/        # Animation clips
├── Audio/             # Sound effects & music
├── Prefabs/           # Reusable game objects
├── Scenes/            # Level files
└── Resources/         # Runtime-loaded assets
```

### Performance Tips
1. **Sprite Atlasing:** Combine sprites to reduce draw calls
2. **Object Pooling:** Reuse objects instead of instantiating/destroying
3. **Mobile Optimization:**
   - Use Sprite Renderer, not Mesh Renderer
   - Limit particle effects
   - Optimize collision detection

### Version Control
- Use Git for version control
- Add `.gitignore` for Unity projects
- Commit frequently

---

## For Milk Man Game Specifically

### Recommended Approach
Since Milk Man Game is built in DroidScript, Unity would be for:
1. **Porting** the game to Unity for better performance
2. **Building a sequel** with more features
3. **Learning** for future projects like Da Verse

### Migration Considerations
- DroidScript uses JavaScript-like syntax
- Unity uses C#
- Similar concepts: sprites, physics, input handling
- Unity offers much more power and flexibility

---

## Cost
- **Unity Personal:** FREE (if revenue <$100K/year)
- **Unity Plus:** $399/year per seat
- **Unity Pro:** $2,040/year per seat

**Recommendation:** Start with Personal license.

---

## Next Steps
1. [ ] Download Unity Hub
2. [ ] Install Unity 6 LTS
3. [ ] Complete "Get Started with Unity" tutorial
4. [ ] Import 2D Game Kit and explore
5. [ ] Create test project with Milk Man sprites

---

**Document Status:** COMPLETE  
**Next Review:** After installation
