# COBRA-SKELETON - Lightweight CNC + Composite Build

**Codename:** COBRA-LITE  
**Construction:** CNC-cut core + Carbon fiber skin  
**Weight Reduction:** 40-50% vs 3D printed  
**Status:** Design Specification  
**Updated:** 2026-03-29

---

## MATERIAL ANALYSIS

### Why Not Balsa?

| Property | Balsa | Basswood | Better Alternative |
|----------|-------|----------|-------------------|
| **Density** | 0.16 g/cm³ | 0.40 g/cm³ | **XPS Foam: 0.03 g/cm³** |
| **Strength** | Very low | Low | **Nomex: Excellent** |
| **Machining** | Splinters | Clean | **Rohacell: Perfect** |
| **Cost** | $$$ | $$ | **$$ (worth it)** |
| **Availability** | Hobby shops | Lumber yards | **Industrial** |

**Recommendation:** Use **Rohacell IG-51** or **Divinycell H-60** structural foam.

### Recommended: Rohacell IG-51

- **Density:** 51 kg/m³ (0.051 g/cm³)
- **Compressive strength:** 0.7 MPa
- **Temperature resistance:** 180°C
- **Bonding:** Excellent with epoxy
- **Cost:** ~$200 for full robot worth

**Why it's better than balsa:**
- 3× lighter than balsa
- Uniform density (no grain issues)
- Doesn't splinter or crush
- Thermoformable (can bend after heating)
- Aerospace proven

### Alternative: Divinycell H-60

- Similar properties
- More available (marine industry)
- Slightly cheaper
- Good for first builds

---

## CONSTRUCTION METHOD

### Core + Skin Architecture

```
Cross-Section of Vertebra:

    [Carbon Fiber Skin - 0.2mm]
            ↓
    ┌─────────────────────┐
    │  ╭─────────────╮    │  ← CF wrap (tension)
    │  │             │    │
    │  │   ROHACELL  │    │  ← Foam core (compression)
    │  │    CORE     │    │
    │  │             │    │
    │  ╰─────────────╯    │  ← CF wrap (tension)
    └─────────────────────┘
            ↓
    [Carbon Fiber Skin - 0.2mm]

Weight comparison (per vertebra):
- Solid PETG:     45g
- Balsa solid:    12g  
- Rohacell + CF:  **8g**  ← Winner
```

### Layer Buildup

**Single Vertebra (T5-T9 with solar cavity):**

```
Step 1: CNC cut Rohacell core
        - Thickness: 18mm
        - Tolerances: +0.2mm for bond line
        - Features: Battery cavities, wiring channels

Step 2: Prepare carbon fiber prepregs
        - 2× layers of 200g/m² twill weave
        - Cut 20% oversize for wrapping

Step 3: Wet layup or vacuum infusion
        - Epoxy resin (low viscosity)
        - Vacuum bag: -0.8 bar
        - Cure: Room temp 24h or 60°C 4h

Step 4: Post-process
        - Trim CF flash
        - Drill mounting holes
        - Install threaded inserts
```

---

## CNC MACHINING SPECS

### Machine Requirements

| Parameter | Minimum | Recommended |
|-----------|---------|-------------|
| **Work area** | 300×300×100mm | 600×400×150mm |
| **Spindle** | 15,000 RPM | 25,000 RPM |
| **Tool** | 3mm end mill | 2mm end mill |
| **Feed rate** | 1000 mm/min | 2000 mm/min |
| **Cooling** | None needed | Vacuum hold-down |

### Tool Path Strategy

**Rohacell Machining:**
```
1. Face mill top surface (0.5mm skim)
2. Rough cut cavities (3mm stepdown)
3. Finish cut walls (1mm stepdown)
4. Drill through-holes
5. Flip and repeat for bottom
```

**Critical:** Use **spiral ramping** entry, never plunge. Foam tears easily.

### G-Code Example (Single Vertebra)

```gcode
; COBRA Vertebra T5 - Rohacell 18mm
; Tool: 2mm carbide end mill

G21 ; Metric
G90 ; Absolute
G17 ; XY plane

; Spindle on
M3 S20000

; Approach
G0 Z5
G0 X0 Y0

; Face top surface
G1 Z-0.5 F1000
G1 X40 F2000
Y5
X0
Y10
... (raster pattern)

; Mill battery cavity 1
G0 X10 Y10 Z5
G1 Z-18 F500
G1 X15 Y10 F1500
G1 X15 Y25
G1 X10 Y25
G1 X10 Y10

; Spiral finish
G2 X12.5 Y17.5 I2.5 J0 F1000
G2 X12.5 Y17.5 I-2.5 J0

; Drill pivot holes
G0 Z5
G81 X20 Y5 Z-18 R2 F500
G81 X20 Y35

; End
M5
G0 Z50
M30
```

---

## VERTEBRA DESIGN FOR CNC

### Core Modifications vs 3D Print

**3D Printed Vertebra → CNC Foam Core:**

| Feature | 3D Print | CNC Foam | Reason |
|---------|----------|----------|--------|
| Walls | 2-3mm solid | 1mm CF skin | Weight |
| Cavities | Limited | Optimized | Easy machining |
| Undercuts | Difficult | Impossible | Design out |
| Threads | Heat-set inserts | Helicoil | Strength |
| Surface | Layer lines | Smooth CF | Aesthetics |

### Optimized Geometry

**Split Design for Assembly:**

```
Traditional (3D print - one piece):
┌─────────────────┐
│  ╭──────────╮   │
│  │  CORE    │   │
│  ╰──────────╯   │
└─────────────────┘

CNC Version (two halves):
┌─────────────────┐    ┌─────────────────┐
│  ╭──────────╮   │    │  ╭──────────╮   │
│  │  LEFT    │   │ +  │  │  RIGHT   │   │
│  │  HALF    │   │    │  │  HALF    │   │
│  ╰──────────╯   │    │  ╰──────────╯   │
└─────────────────┘    └─────────────────┘
      Bonded together
```

**Why two halves?**
- Machines flat (no flipping needed)
- Internal features accessible
- Perfect symmetry
- Easier assembly

### Joint Design

**Gimbal Joint (CNC + 3D Print Hybrid):**

```
[Rohacell Core]
     │
     │ CF skin wraps around
     ↓
┌─────────────────┐
│   ┌───────┐     │
│   │ 3D    │     │  ← Printed joint ends
│   │PRINT  │     │    (PETG CF)
│   │CAPS   │     │
│   └───┬───┘     │
│       │         │
│   [Rohacell]    │
│       │         │
│   ┌───┴───┐     │
│   │3D     │     │
│   │PRINT  │     │
│   │CAP    │     │
└───┴───────┴─────┘

Metal pivot pin through printed caps
Foam core carries compression loads
CF skin carries tension loads
```

---

## BILL OF MATERIALS (COBRA-SKELETON)

### Core Materials

| Item | Qty | Cost | Notes |
|------|-----|------|-------|
| Rohacell IG-51 20mm | 2 sheets 600×400mm | $180 | Main structure |
| Rohacell IG-51 10mm | 1 sheet 600×400mm | $90 | Fingers, thin parts |
| **Core Subtotal** | | **$270** | |

### Composite Materials

| Item | Qty | Cost | Notes |
|------|-----|------|-------|
| Carbon fiber 200g/m² twill | 20m² | $200 | Skin material |
| Epoxy resin (low vis) | 5kg | $75 | Infusion grade |
| Peel ply | 30m² | $40 | Release fabric |
| Breather fabric | 20m² | $30 | Vacuum consumable |
| Vacuum bag film | 10m² | $35 | Seal film |
| Vacuum tape | 2 rolls | $25 | Sealant |
| **Composite Subtotal** | | **$405** | |

### CNC Hardware

| Item | Qty | Cost | Notes |
|------|-----|------|-------|
| 2mm carbide end mills | 10 | $80 | Foam cutting |
| Helicoil inserts M3 | 200 | $50 | Threaded mounts |
| Helicoil inserts M4 | 100 | $30 | Heavy loads |
| Installation tool | 1 | $25 | For inserts |
| **CNC Subtotal** | | **$185** | |

### Comparison to 3D Printed

| Aspect | 3D Printed | CNC + CF | Savings |
|--------|------------|----------|---------|
| **Material cost** | $36 | $860 | -$824 |
| **Labor time** | 120h printing | 40h CNC + layup | 67% less |
| **Weight** | 8kg | **4.5kg** | 44% lighter |
| **Strength** | Moderate | **High** | CF is 10× stiffer |
| **Surface finish** | Layer lines | **Smooth** | Better aesthetics |
| **Total time** | 120h | **80h** | Faster |

**Verdict:** More expensive materials but faster build and much better result.

---

## ASSEMBLY PROCESS

### Step-by-Step

**Day 1: CNC Machining**
```
Hour 0-8:   Set up Rohacell sheets on CNC
Hour 8-16:  Cut all 25 vertebrae cores
Hour 16-24: Cut finger segments, gimbals, caps
```

**Day 2: Preparation**
```
Hour 24-28: Clean foam edges, sand lightly
Hour 28-32: Cut CF prepregs to size
Hour 32-36: Prepare vacuum bags, tools
```

**Day 3: Layup (Batch 1 - Thoracic)**
```
Hour 36-40: Apply first CF layer to T1-T6
Hour 40-44: Vacuum bag and seal
Hour 44-52: Cure (room temp + heat gun boost)
```

**Day 4: Layup (Batch 2 - Rest)**
```
Hour 52-56: Apply CF to C1-L5
Hour 56-60: Vacuum bag and cure
```

**Day 5: Post-Processing**
```
Hour 60-68: Trim flash, drill holes
Hour 68-72: Install Helicoil inserts
Hour 72-76: Surface finish (sand clear coat)
```

**Day 6-7: Assembly**
```
Hour 76-88: Assemble spine with servos
Hour 88-100: Wire and test
```

**Total: 100 hours vs 120 hours for 3D print**

---

## REINFORCEMENT PATTERNS

### Carbon Fiber Layup Schedules

**High-Load Vertebra (L1-L5, Sacrum):**
```
[0°/90°] - 2 layers bidirectional
[+45°/-45°] - 2 layers bias
[0°/90°] - 2 layers bidirectional

Total: 6 layers = 1.2mm thickness
Weight: 1.2g per 10cm²
```

**Standard Vertebra (C1-T12):**
```
[0°/90°] - 2 layers
[+45°/-45°] - 1 layer

Total: 3 layers = 0.6mm thickness
Weight: 0.6g per 10cm²
```

**Finger Segments:**
```
[0°] - 1 layer unidirectional (along length)

Total: 1 layer = 0.2mm thickness
Weight: negligible
```

### Vacuum Infusion Setup

```
Layer Stack (bottom to top):
┌─────────────────────────┐
│ Vacuum bag film         │ ← Seal
│ Breather fabric         │ ← Air path
│ Peel ply                │ ← Release
│ CF layer 2 (45°/-45°)   │
│ CF layer 1 (0°/90°)     │
│ Rohacell core           │
│ CF layer 1 (0°/90°)     │
│ CF layer 2 (45°/-45°)   │
│ Peel ply                │
│ Flow media              │ ← Resin distribution
│ Vacuum bag film         │
└─────────────────────────┘
         ↓
    Resin inlet
```

---

## INTEGRATION WITH 3D PRINTED PARTS

### Hybrid Approach (Recommended)

**CNC + CF:**
- Vertebrae cores
- Long structural members
- Panels and covers

**3D Printed:**
- Joint gimbals (complex geometry)
- Servo mounts (threaded inserts)
- Wiring channels (internal routing)
- End caps (attachment points)

**Metal:**
- Pivot pins
- Threaded inserts
- Bearing races

### Example: T5 Vertebra

```
Components:
├── T5_core_left.cnc    (Rohacell)
├── T5_core_right.cnc   (Rohacell)
├── T5_gimbal_top.stl   (PETG CF)
├── T5_gimbal_bot.stl   (PETG CF)
├── T5_servo_mount.stl  (PETG CF)
├── CF_skin_top.cut     (Carbon fiber)
├── CF_skin_bot.cut     (Carbon fiber)
└── M3 inserts.helicoil (Metal)

Assembly:
1. Bond left/right cores
2. Wrap with CF, cure
3. Install gimbal caps
4. Install servo mount
5. Install inserts
6. Done!
```

---

## TESTING & QUALITY

### Non-Destructive Testing

**Ultrasonic C-Scan:**
- Detects voids in CF layup
- Identifies delamination
- Standard in aerospace

**Simple Alternative:**
- Tap test (listen for voids)
- Visual inspection
- Bend test (should return to shape)

### Strength Testing

**Compression Test:**
```
Setup: Instron or hydraulic press
Load: 100kg on single vertebra
Pass: No permanent deformation
Fail: Core crush or skin wrinkling

Expected: Rohacell handles 200kg+ before failure
```

**Flex Test:**
```
Setup: Three-point bend
Span: 100mm
Load: 50kg center
Deflection: Should be <5mm
```

---

## COST JUSTIFICATION

### Why Spend More?

| Factor | 3D Print | CNC+CF | Benefit |
|--------|----------|--------|---------|
| **Material** | $800 | $1,200 | +$400 |
| **Time** | 120h | 80h | -40h saved |
| **Weight** | 8kg | 4.5kg | 44% lighter |
| **Stiffness** | Moderate | Very high | Better precision |
| **Wow factor** | Cool | **Amazing** | CF weave visible |

**For production:** CNC+CF is worth it.
**For prototypes:** 3D print first, iterate, then CF.

---

## SUPPLIERS

### Rohacell Foam
- **Evonik** (manufacturer)
- **Composites Canada** (distributor)
- **Fibre Glast** (small quantities)

### Carbon Fiber
- **Soller Composites**
- **DragonPlate**
- **Rock West Composites**

### CNC Services (if no machine)
- **Ponoko** (online, laser cut foam)
- **Protolabs** (professional CNC)
- **Local makerspace**

---

## DOCUMENTATION

### Files Generated

| File | Purpose |
|------|---------|
| `CNC_T01-T12.nc` | Thoracic vertebrae toolpaths |
| `CNC_L01-L05.nc` | Lumbar vertebrae toolpaths |
| `CNC_C01-C07.nc` | Cervical vertebrae toolpaths |
| `CNC_fingers.nc` | Finger segments |
| `CF_patterns.dxf` | CF cutting templates |
| `Assembly_guide.pdf` | Step-by-step assembly |

---

**Document Version:** 1.0  
**Last Updated:** 2026-03-29 04:14 UTC  
**Status:** Ready for prototype
