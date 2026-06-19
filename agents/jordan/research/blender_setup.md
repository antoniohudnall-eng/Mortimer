# Blender Setup Guide
## Research Document for Performance Supply Depot
**Prepared by:** Jordan, Executive Assistant  
**Date:** 2026-03-16  
**Status:** URGENT - For CYLON-PRIME 3D Printing

---

## Overview
Blender is a free, open-source 3D creation suite. It's essential for the **CYLON-PRIME** project for 3D modeling and STL export for 3D printing. Blender 5.0 is the latest major release with significant improvements.

---

## System Requirements

### Minimum Requirements (Blender 5.0)

| Component | Specification |
|-----------|---------------|
| **OS** | Windows 10/11, macOS 13+, Linux (glibc 2.28+) |
| **CPU** | 64-bit quad-core CPU with SSE4.2 support |
| **RAM** | 8 GB |
| **Graphics** | OpenGL 4.3 compatible graphics with 2 GB VRAM |
| **Display** | 1920×1080 resolution |
| **Storage** | 1 GB for installation |

### Recommended for 3D Printing Work

| Component | Specification |
|-----------|---------------|
| **CPU** | 8-core or better (for faster rendering) |
| **RAM** | 16 GB or more |
| **Graphics** | NVIDIA GTX/RTX or AMD RX series with 4+ GB VRAM |
| **Storage** | SSD with 10+ GB free |
| **Mouse** | Three-button mouse with scroll wheel |
| **Numpad** | External numpad (optional but recommended) |

---

## Installation Process

### Step 1: Download Blender
1. Visit: https://www.blender.org/download/
2. Click "Download Blender 5.0"
3. Select your operating system
4. Choose appropriate version:
   - **Installer** (Windows) - Recommended
   - **Portable** (Windows) - No installation required
   - **macOS** - Intel or Apple Silicon
   - **Linux** - Various distributions

### Step 2: Install Blender

#### Windows (Installer)
1. Run downloaded `.exe`
2. Follow installation wizard
3. Choose components:
   - ✅ Blender application
   - ✅ Desktop shortcut (optional)
   - ✅ Add to PATH (recommended)

#### Windows (Portable)
1. Extract `.zip` to desired location
2. Run `blender.exe` directly
3. No installation required

#### macOS
1. Open `.dmg` file
2. Drag Blender to Applications folder
3. May need to allow in Security settings

#### Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install blender

# Or download from blender.org and extract
# Run: ./blender
```

### Step 3: First Launch Setup
1. Open Blender
2. Initial setup wizard:
   - Select language
   - Choose keymap (Blender or industry compatible)
   - Select theme (Dark recommended)
3. Save preferences

---

## STL Export Workflow for 3D Printing

### What is STL?
STL (STereoLithography) is the standard file format for 3D printing. It describes only the surface geometry of a 3D object using triangular facets.

### Creating Models for 3D Printing

#### Step 1: Set Up for 3D Printing
1. **Units Setup:**
   - Edit → Preferences → Units
   - Set to Metric (millimeters for 3D printing)

2. **Add-ons for 3D Printing:**
   - Edit → Preferences → Add-ons
   - Search "3D Print Toolbox"
   - Enable "3D Print Toolbox"

#### Step 2: Modeling Best Practices
1. **Manifold Geometry:**
   - Model must be "watertight" (no holes)
   - All edges must connect to exactly two faces
   - No floating geometry

2. **Scale Appropriately:**
   - Design in real-world millimeters
   - Check printer build volume

3. **Wall Thickness:**
   - Minimum 0.8mm for FDM printing
   - Check printer specifications

#### Step 3: Export to STL
1. **Select Object:**
   - Right-click on model to select

2. **Apply Modifiers:**
   - Object → Apply → All Modifiers
   - Ensures geometry is finalized

3. **Export:**
   - File → Export → STL (.stl)
   - Or use 3D Print Toolbox: Sidebar (N) → 3D Print → Export

4. **Export Settings:**
   - ✅ Selection Only (if multiple objects)
   - Scale: 1.0 (if units set correctly)
   - Forward: Y Forward
   - Up: Z Up
   - ASCII or Binary (Binary is smaller)

#### Step 4: Validate STL
1. **Check in 3D Print Toolbox:**
   - Sidebar → 3D Print → Check All
   - Fix any errors (non-manifold edges, etc.)

2. **Alternative Validation:**
   - Import to slicer software (Cura, PrusaSlicer)
   - Check for errors before printing

---

## Learning Resources

### Official Blender Resources
- **Blender Manual:** https://docs.blender.org/manual/en/latest/
- **Blender Cloud:** https://cloud.blender.org/ (subscription)
- **Blender Studio:** Free tutorials and assets

### YouTube Channels
- **Blender Guru:** Excellent beginner tutorials (Donut tutorial is famous)
- **CGDive:** Technical tutorials
- **Imphenzia:** Quick tips and techniques
- **CrossMind Studio:** Hard surface modeling

### Free Learning Paths
1. **Blender Beginner Tutorial (Blender Guru)**
   - Part 1: Interface and navigation
   - Part 2: Modeling the donut
   - Part 3: Materials and rendering

2. **Official Blender Fundamentals**
   - https://www.youtube.com/playlist?list=PLa1F2ddGya_-UvuAqHAksYnB0qL9yWDO6

3. **3D Printing Specific**
   - Search: "Blender 3D printing tutorial"
   - Focus on precision modeling techniques

---

## Basics for CYLON-PRIME

### Essential Modeling Techniques
1. **Box Modeling:**
   - Start with primitive shapes
   - Extrude, scale, rotate to form robot parts

2. **Hard Surface Modeling:**
   - Bevel edges for realistic corners
   - Use modifiers (Mirror, Array, Boolean)

3. **Precision Modeling:**
   - Use snapping (Vertex, Edge, Face)
   - Grid snapping for alignment
   - Numeric input for exact dimensions

### Recommended Workflow for Robot Parts
1. **Reference Images:**
   - Import blueprints to background
   - Model over reference

2. **Component Breakdown:**
   - Model parts separately
   - Use collections for organization

3. **Assembly:**
   - Parent parts to main body
   - Maintain separate objects for printing

4. **Export Strategy:**
   - Export parts individually
   - Name files descriptively
   - Include tolerances for assembly

---

## Add-ons for 3D Printing

### Built-in (Enable in Preferences)
- **3D Print Toolbox:** Essential for 3D printing
  - Volume calculation
  - Overhang detection
  - Export tools
  - Error checking

### Recommended Community Add-ons
- **Mesh Machine:** Advanced mesh tools
- **Hard Ops:** Hard surface modeling
- **BoxCutter:** Boolean operations
- **CAD Transform:** Precision transformations

---

## Cost
**Blender is completely FREE** (open source under GPL license)
- No licensing fees
- No subscription
- Free updates forever

---

## Quick Reference: Keyboard Shortcuts

### Essential Navigation
| Action | Shortcut |
|--------|----------|
| Rotate View | Middle Mouse Drag |
| Pan View | Shift + Middle Mouse |
| Zoom | Scroll Wheel |
| Focus on Object | Numpad . (period) |
| Front View | Numpad 1 |
| Top View | Numpad 7 |
| Side View | Numpad 3 |

### Essential Modeling
| Action | Shortcut |
|--------|----------|
| Grab/Move | G |
| Rotate | R |
| Scale | S |
| Extrude | E |
| Loop Cut | Ctrl + R |
| Bevel | Ctrl + B |
| Knife Tool | K |
| Undo | Ctrl + Z |
| Redo | Ctrl + Shift + Z |

---

## Next Steps
1. [ ] Download and install Blender 5.0
2. [ ] Complete Blender Guru's beginner tutorial (donut)
3. [ ] Enable 3D Print Toolbox add-on
4. [ ] Practice STL export with simple model
5. [ ] Review CYLON-PRIME STL_MANIFEST.md for specific parts

---

**Document Status:** COMPLETE  
**Next Review:** After Blender installation
