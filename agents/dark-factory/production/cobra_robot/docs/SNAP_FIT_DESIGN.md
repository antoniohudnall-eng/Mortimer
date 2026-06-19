# COBRA-Snap - Tool-Free Assembly System

**Philosophy:** No glue, no screws, no tools required  
**Method:** Precision snap-fit joints  
**Assembly Time:** 2 hours (vs 20+ hours with fasteners)  
**Disassembly:** Instant - for repair, transport, upgrade  
**Status:** Design Specification  
**Updated:** 2026-03-29

---

## WHY SNAP-FIT?

### Traditional Assembly Problems

| Method | Issues |
|--------|--------|
| **Glue** | Permanent, messy, cure time, can't repair |
| **Screws** | 500+ screws = 10 hours assembly, strips easily |
| **Nuts/Bolts** | Requires tools, rattles loose, heavy |
| **Welding** | Permanent, hot work, ugly seams |

### Snap-Fit Benefits

- **Speed:** Push together in seconds
- **Reversible:** Pull apart just as fast
- **No tools:** Hand assembly anywhere
- **Self-aligning:** Features guide placement
- **Tactile feedback:** "Click" confirms engagement
- **Vibration proof:** Proper design won't shake loose

---

## JOINT TYPES

### 1. Ball-and-Socket Joint (Spine)

```
        [UPPER VERTEBRA]
              │
         ╭────┴────╮
         │   ●     │ ← Ball (printed as part of upper)
         │  /│\    │
         │ / │ \   │
         ╰───┬───╯
             │
    ╭────────┴────────╮
    │   ╭─────────╮     │
    │   │ ◯     ◯ │     │ ← Socket fingers (flexible)
    │   │    ●    │     │ ← Socket cavity
    │   │ ◯     ◯ │     │
    │   ╰─────────╯     │
    │ [LOWER VERTEBRA]  │
    ╰───────────────────╯

Engagement: Push ball into socket
Retention: Socket fingers grip ball
Range: ±15° pitch, ±10° roll, ±5° yaw
Removal: Pull apart (moderate force)
```

**Design Parameters:**
```
Ball diameter: 8mm
Socket fingers: 4-6 petals
Wall thickness: 0.8mm (TPU) or 1.2mm (PETG)
Interference: 0.2mm (tight fit)
Engagement force: 5-8N
Removal force: 12-15N
```

### 2. Dovetail Slide Joint (Structural)

```
Side View:

    [PART A]              [PART B]
    ╭─────╮                ╭─────╮
    │    ╱│                │\    │
    │   ╱ │  ════════►    │ \   │
    │  ╱  │   Slide        │  \  │
    │ ╱   │                │   \ │
    │╱    │                │    \│
    ╰─────╯                ╰─────╯
    Male dovetail          Female socket
    (5° taper angle)

Top View:

    ╭──────────────╮
    │ ╭──────────╮ │ ← Entry (wider)
    │ │ ╭──────╮ │ │
    │ │ │      │ │ │ ← Lock position (narrower)
    │ │ ╰──────╯ │ │
    │ ╰──────────╯ │
    ╰──────────────╯
    
Engagement: Slide until "click"
Retention: Taper lock + friction
Removal: Slide reverse direction
```

**Design Parameters:**
```
Taper angle: 3-5° (self-locking)
Engagement length: 20-30mm
Clearance: 0.1mm (sliding fit)
Locking feature: 0.3mm bump at end
Material: PETG or Nylon
```

### 3. Living Hinge Snap (Panels)

```
    [PANEL A]          [PANEL B]
        │                  │
     ╭──┴──╮            ╭──┴──╮
     │     │            │     │
     │     │            │     │
     │     │   ═══════► │     │
     │     │    Hinge   │     │
     │     │            │     │
     │  ╭──╯            ╰──╮  │
     │  │     Flex tab     │  │
     │  │  ╭──────────╮    │  │
     │  │  │  ◯    ◯  │    │  │ ← Locking holes
     └──┴──┴──────────┴────┴──┘
              ↑
         Locking pin
         (part of Panel A)

Assembly: Fold hinge 180°, pins snap into holes
Removal: Push pins from back to release
```

**Design Parameters:**
```
Hinge thickness: 0.4-0.6mm (for PETG)
Hinge width: 10mm minimum
Pin diameter: 2mm
Hole diameter: 2.2mm (interference fit)
Cycles: 100+ before fatigue
```

### 4. Twist-Lock Bayonet (Cylindrical)

```
Exploded View:

    [MALE PART]          [FEMALE PART]
    ╭─────────╮          ╭─────────╮
    │    ┌──┐ │          │  ╭──╮   │
    │    │  │ │          │  │  │   │ ← L-shaped slot
    │   ╱    ╲│  ═══►   │ ╱    ╲  │
    │  │  ●   ││ Insert ││  ●    │ │
    │  │      ││ Rotate ││       │ │
    └──┴──────┴┘        └┴───────┴─┘
         ↑
    Locking lug (2-4x)

Assembly:
1. Align lugs with slots
2. Push together
3. Rotate 30-45°
4. "Click" into detent

Removal: Reverse rotation
```

**Design Parameters:**
```
Lugs: 2-4 evenly spaced
Rotation angle: 30-45°
Detent depth: 0.5mm
Engagement force: 10-15N
Torque to lock: 2-3 N·m
```

### 5. Cantilever Snap-Fit (Compliant)

```
    [BASE]              [MATING PART]
      │                      │
      │  ╭──────────────╮    │
      │  │              │    │
      │  │  Flexible    │    │
      │  │  beam        │    │
      │  │     ↓        │    │
      │  │    ╭──╮      │    │
      │  │    │  │      │ ╭──┴──╮
      └──┴────┤  ├──────┼─┤     │
              │  │      │ │     │
              ╰──╯      │ │     │
             Hook       │ ╰─────╯
                       Undercut

Deflection: δ = (F·L³)/(3·E·I)

Where:
F = insertion force
L = beam length
E = modulus (PETG: 2.1 GPa, TPU: 0.1 GPa)
I = moment of inertia
```

**Design Parameters:**
```
Beam thickness (h): 1.0-2.0mm
Beam length (L): 15-30mm
Deflection: 1-2mm (10% of length)
Strain limit: 5% (PETG can handle 10%)
Retention force: 20-50N typical
```

---

## COBRA SNAP-FIT IMPLEMENTATION

### Spine Assembly

**Each Joint (2 per vertebra):**
```
Components:
├── Ball socket (integrated in lower vertebra)
├── Ball stud (integrated in upper vertebra)
└── Retention clip (optional, for heavy loads)

Assembly (per joint):
Time: 3 seconds
Force: 5N push
Tactile: "Click" confirms lock
```

**Full Spine (24 joints):**
```
Traditional (screws):     2 hours
Snap-fit (ball-socket):    2 minutes
```

### Battery Cartridge System

```
[BATTERY CARTRIDGE]
        ╭─────────╮
        │ ╭─────╮ │
        │ │18650│ │  × 2 cells
        │ │     │ │
        │ ╰─────╯ │
        │ ╭─────╮ │
        │ │18650│ │
        │ ╰─────╯ │
        ╰────┬────╯
             │
        ╭────┴────╮
        │ ●     ● │ ← Contact pins
        │    ●    │
        ╰─────────╯
             │
             ▼
    ╭─────────────────╮
    │ [VERTEBRA BODY] │
    │                 │
    │   ╭───────╮     │
    │   │ ○   ○ │     │ ← Socket contacts
    │   │   ○   │     │
    │   ╰───────╯     │
    │      ▲          │
    │      │          │
    │  [Cartridge     │
    │   slides in]    │
    ╰─────────────────╯

Features:
- Keyed insertion (won't go in backwards)
- Locking tab at rear
- Electrical contacts mate automatically
- Eject button for removal
```

### Hand Assembly

**Finger Attachment:**
```
[PALM]
   │
   │  ╭────────╮
   │  │        │
   ├──┤  ◯  ◯  │ ← Dovetail socket
   │  │        │
   │  ╰────┬───╯
   │       │
   │       ▼
   │  ╭────────╮
   │  │   ╭─╮  │
   └──┤   │ │  │ ← Finger dovetail (male)
      │   ╰─╯  │
      ╰────────╯
      [FINGER]

Assembly: Slide finger into palm (2 seconds)
Retention: Taper lock + 0.3mm detent
Removal: Push small release button, slide out
```

**Tendon Connection:**
```
Quick-connect tendon coupler:

[TENDON FROM FOREARM]
        │
        │
     ╭──┴──╮
     │ ~~~~│ ← Dyneema line
     │ ~~~~│
     ╰──┬──╯
        │
   ╭────┴────╮
   │ ╭─────╮ │
   │ │ ◯───┼─┼──► Ball-end crimp
   │ ╰─────╯ │
   ╰────┬────╯
        │
   ╭────┴────╮
   │ [FINGER]│
   │ ╭─────╮ │
   │ │  ●  │ │ ← Socket accepts ball
   │ ╰─────╯ │
   │  (flex) │
   ╰─────────╯

Connection: Push tendon ball into socket (1 second)
Disconnection: Push socket sides, pull tendon
```

### Solar Panel Mount

```
[THORACIC VERTEBRA]
        ╭─────────────╮
        │             │
        │  ╭───────╮  │
        │  │ ◯   ◯ │  │ ← Alignment pins
        │  │       │  │
        │  │ ╭───╮ │  │ ← Recessed cavity
        │  │ │   │ │  │
        │  │ ╰───╯ │  │
        │  │ ◯   ◯ │  │ ← Magnetic locks
        │  ╰───────╯  │
        │             │
        ╰─────────────╯
                ▲
                │
                │  ╭─────────────╮
                │  │             │
                └──┤ ╭───────╮   │
                   │ │ SOLAR   │   │
                   │ │ PANEL   │   │
                   │ │         │   │
                   │ ╰───────┯━│   │ ← Contacts
                   │         │ │   │
                   ╰─────────┴─┴───╯

Features:
- 4 alignment pins (won't fit wrong)
- Magnets hold in place
- Spring contacts for power
- Weather seal gasket integrated
```

---

## MATERIAL CONSIDERATIONS

### Snap-Fit Material Properties

| Material | Flexibility | Strength | Fatigue | Best For |
|----------|-------------|----------|---------|----------|
| **TPU 95A** | Excellent | Good | Excellent | Living hinges, fingers |
| **PETG** | Good | Very Good | Good | Structural snaps |
| **Nylon** | Very Good | Excellent | Excellent | High-cycle joints |
| **ABS** | Moderate | Good | Moderate | General purpose |
| **PLA** | Poor | Moderate | Poor | Prototypes only |

### Dual-Material Printing

**Optimal: Rigid + Flexible**
```
[RIGID STRUCTURE] + [FLEXIBLE JOINT]

Print sequence:
1. Print rigid parts (PETG) - 0.4mm nozzle
2. Switch to TPU nozzle or pause
3. Print flex features (TPU) - 0.4mm nozzle
4. Bond interface (chemical or mechanical)

OR: Multi-material printer (MMU)
- Prusa MMU2S
- Bambu Lab AMS
- Mosaic Palette
```

---

## DESIGN RULES

### Critical Dimensions

**Wall Thickness:**
```
Minimum for snap features:
- TPU: 0.6mm
- PETG: 1.0mm
- Nylon: 0.8mm

For structural walls:
- All materials: 2.0mm minimum
```

**Tolerances:**
```
Clearance fit: +0.15mm per side
Transition fit: +0.05mm per side
Interference fit: -0.10mm per side (for press)
```

**Radii:**
```
Internal corners: Minimum 0.5mm radius
Prevents stress concentration
Improves layer adhesion
```

### Stress Relief

**Avoid sharp corners:**
```
WRONG:          RIGHT:
    │              ╭
   ─┼─            │╮
    │             ││
   (crack)        (strong)
```

**Add fillets:**
```
Beam attachment:

    ╭────╮           ╭────╮
    │    │           │    │
    │    │    →      │   ╭╯
    │    │           │ ╭─╯
    ├──┬─┤           ├──┴─┤
    │  │ │           │    │
    ╰──┴─╯           ╰────╯
    (stress)         (relieved)
```

---

## ASSEMBLY SEQUENCE

### Step-by-Step (No Tools)

**Preparation:**
```
□ Unpack all printed parts (48 hours)
□ Sort by region (cervical/thoracic/lumbar/sacrum)
□ Check fit of critical joints
□ Have rubber mallet handy (for tight fits)
```

**Spine Assembly:**
```
Hour 0:00 - Snap C1 onto C2
Hour 0:05 - Continue C3-C7 (7 vertebrae, 6 joints)
Hour 0:10 - Snap T1-T12 (12 vertebrae, 11 joints)
Hour 0:25 - Snap L1-L5 (5 vertebrae, 4 joints)
Hour 0:30 - Attach S1 (sacrum)

Total spine time: 30 minutes
Traditional screw method: 4 hours
```

**Power System:**
```
Hour 0:30 - Insert battery cartridges into T1-L5
Hour 0:45 - Snap solar panels onto T5-T9
Hour 0:50 - Connect power bus (plug-and-socket)
Hour 0:55 - Test power distribution
```

**Hands:**
```
Hour 1:00 - Slide fingers into palms (5 per hand)
Hour 1:10 - Thread tendons through guides
Hour 1:20 - Snap tendon couplers to fingers
Hour 1:30 - Test hand actuation
```

**Integration:**
```
Hour 1:30 - Snap hands to forearms
Hour 1:40 - Attach arms to shoulders (if present)
Hour 1:50 - Install brain in sacrum
Hour 2:00 - POWER ON!
```

**Total Assembly Time: 2 hours**
**Disassembly for transport: 10 minutes**

---

## QUALITY CHECKS

### Visual Inspection

```
□ No cracked snap features
□ All joints "click" audibly
□ No visible gaps at interfaces
□ Solar panels seated flush
```

### Functional Tests

```
□ Each joint rotates smoothly
□ No binding in any position
□ Battery cartridges eject properly
□ Tendons don't slip
□ Hands curl and extend fully
```

### Durability

```
□ Cycle test: Open/close spine 100×
□ Drop test: 30cm to concrete (should survive)
□ Vibration test: Run servos, check for loosening
```

---

## REPAIR & UPGRADE

### Modular Replacement

**Broken vertebra?**
1. Pull apart at joints (20 seconds)
2. Remove battery cartridge (5 seconds)
3. Snap in new vertebra (10 seconds)
4. Reassemble (1 minute)

**Total repair time: 2 minutes**

**Upgrade battery?**
1. Press eject button on old cartridge
2. Slide in new higher-capacity cartridge
3. Done - no disassembly needed

**Upgrade brain?**
1. Remove sacrum cover (4 snaps)
2. Disconnect 2 power plugs
3. Swap Raspberry Pi
4. Reassemble (2 minutes)

---

## FILES GENERATED

### Snap-Fit Design Files

| File | Description |
|------|-------------|
| `COBRA_snap_spine_C01-C07.stl` | Cervical vertebrae with ball joints |
| `COBRA_snap_spine_T01-T12.stl` | Thoracic with battery snaps |
| `COBRA_snap_spine_L01-L05.stl` | Lumbar vertebrae |
| `COBRA_snap_sacrum_S01.stl` | Sacrum with brain bay |
| `COBRA_snap_battery_cart.stl` | Universal battery cartridge |
| `COBRA_snap_solar_mount.stl` | Solar panel bayonet mount |
| `COBRA_snap_finger_*.stl` | Dovetail finger segments |
| `COBRA_snap_palm_*.stl` | Hand palm with sockets |
| `COBRA_snap_tendon_coupler.stl` | Quick-connect tendon fitting |

### Documentation

| File | Description |
|------|-------------|
| `assembly_animation.gif` | Visual assembly guide |
| `snap_fit_calculator.xlsx` | Design parameter calculator |
| `tolerance_check_guide.pdf` | Quality control procedures |

---

## COMPARISON

### Assembly Time

| Method | Spine | Hands | Power | Total |
|--------|-------|-------|-------|-------|
| **Glue** | 4h | 2h | 1h | 7h + 24h cure |
| **Screws** | 4h | 3h | 2h | 9h |
| **Snap-Fit** | **0.5h** | **0.5h** | **0.5h** | **1.5h** |

### Disassembly

| Method | Time | Tools | Damage |
|--------|------|-------|--------|
| Glue | ∞ | Destructive | Yes |
| Screws | 2h | Screwdrivers | Possible |
| Snap-Fit | **10min** | **None** | **None** |

---

**Document Version:** 1.0  
**Last Updated:** 2026-03-29 04:15 UTC  
**Status:** Design complete - ready for prototyping

**Design Philosophy:** 
> *"The best assembly is the one you never think about."*
