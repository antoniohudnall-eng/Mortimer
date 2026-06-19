# Tendon Actuation System

**Purpose:** Lightweight, strong tendon-driven actuation for fingers, toes, and limb assist  
**Primary Material:** Braided fishing line (Dyneema/Spectra)  
**Status:** Design Specification  
**Updated:** 2026-03-29

---

## OVERVIEW

Tendon actuation moves motors **away from the joint** to reduce moving mass. Similar to human anatomy where muscles are in the forearm and tendons extend to the fingers.

**Advantages:**
- 60-80% reduction in hand/foot weight
- Smaller, lighter distal segments
- Natural compliance (fishing line stretches slightly)
- Bidirectional actuation (pull to open AND close)
- Power assist possible with motor coupling

---

## FISHING LINE SPECIFICATIONS

### Recommended Line Types

| Type | Strength | Diameter | Stretch | Use Case |
|------|----------|----------|---------|----------|
| **Dyneema Braided** | 50-100 lb | 0.2-0.4mm | <1% | Fingers, precision |
| **Spectra Hollow** | 100-200 lb | 0.3-0.5mm | <2% | Limbs, high load |
| **Kevlar Cord** | 200+ lb | 0.5-0.8mm | <0.5% | Heavy duty, no stretch |
| **Nylon Monofilament** | 20-50 lb | 0.3-0.6mm | 10-15% | Spring return (not recommended) |

**Recommended: Dyneema Braided 80 lb test**
- Zero stretch under load
- Abrasion resistant
- Low friction through guides
- Thin profile (0.3mm)

### Material Properties

**Dyneema/Spectra (UHMWPE):**
- Tensile strength: 3,000 MPa (stronger than steel by weight)
- Density: 0.97 g/cm³ (floats in water)
- Melting point: 147°C
- UV resistance: Excellent
- Chemical resistance: Excellent

**Comparison:**
```
Material        Strength/Density    Flexibility    Cost
─────────────────────────────────────────────────────
Steel cable     Good                Poor           Low
Nylon           Poor                Excellent      Low
Dyneema         EXCELLENT           Good           Medium
Kevlar          Excellent           Poor           High
```

---

## FINGER/TENDON HAND DESIGN

### Anatomy Reference

```
HUMAN HAND (for reference):

        [FINGERS]
           │
     ┌─────┴─────┐
     │  METACARPAL │ ← Motors mount here (palm)
     │   (PALM)    │
     └─────┬─────┘
           │
    [TENDON SHEATH] ← Fishing line runs through
           │
     [PROXIMAL PHALANGE] ← Base finger segment
           │
     [INTERMEDIATE PHALANGE] ← Middle segment
           │
     [DISTAL PHALANGE] ← Tip
```

### Robotic Implementation

#### 3D Printed Finger Segments

**Segment Design:**
```
Proximal Phalange (25mm long):
┌──────────────────────────────────┐
│  ╭──────╮                [GUIDE]│ ← Tendon channel
│  │      │─────────●─────────────│    (2mm diameter)
│  ╰──────╯                       │
│       [JOINT PIVOT]             │
└──────────────────────────────────┘
```

**Joint Design:**
- **Pivot:** 2mm steel pin or printed press-fit
- **Bushing:** PTFE sleeve for low friction
- **Return spring:** Optional for one-tendon design
- **Range:** 0-90° flexion

### Tendon Routing

```
SINGLE TENDON PER FINGER (simplified):

Motor (in forearm)
   │
   ├──[PULLEY]──┐
   │             │
   │            [RETURN SPRING]
   │             │
   │    ┌────────┘
   │    │
   │   [GUIDE TUBE]──→ through forearm
   │    │
   │   [GUIDE TUBE]──→ through wrist
   │    │
   └──→[FINGER TENDON CHANNEL]
        │
   ┌────┴────┐
   │Proximal │ ← Tendon attaches here
   │Phalange │   (pulley doubles mechanical advantage)
   └────┬────┘
        │
   ┌────┴────┐
   │Middle   │ ← Passive coupling
   │Phalange │
   └────┬────┘
        │
   ┌────┴────┐
   │Distal   │ ← Passive coupling
   │Phalange │
   └─────────┘

Action: Motor pulls → finger curls (grasp)
        Spring returns → finger extends (release)
```

```
DUAL TENDON PER FINGER (full control):

Motor A (Flexion)          Motor B (Extension)
   │                           │
   ├──[PULLEY]                 [PULLEY]──┤
   │                                   │
  [FLEXOR TENDON]              [EXTENSOR TENDON]
   │                                   │
   │    ┌──────────────────────────────┘
   │    │
   │   [FINGER - flexor attaches to proximal]
   │   [FINGER - extensor attaches to distal]
   │    │
   └──→│←──┘

Action: Motor A pulls → finger curls
        Motor B pulls → finger extends
        Both pull → rigid grasp
```

### Mechanical Advantage

**Pulley System for 2:1 advantage:**
```
    [MOTOR PULLEY]──→ pulls 10mm
           │
    ┌──────┴──────┐
    │             │
    │   ╭───╮     │
    └──→│ ● │←──┘│  [FINGER PULLEY] moves 5mm
        ╰───╯        with 2× force
           │
      [ATTACHED TO FINGER]

Force multiplication: 2×
Speed reduction: ½×
```

**Why this matters:**
- Small motor (0.5 kg·cm) → 1.0 kg·cm at finger
- Allows smaller, cheaper motors
- Increases effective grip strength

### Hand Assembly BOM

| Component | Qty | Material | Cost |
|-----------|-----|----------|------|
| Finger segments | 15 (5×3) | PETG/TPU | $3 |
| Dyneema line 80lb | 5m | - | $5 |
| 2mm steel pins | 12 | Stainless | $2 |
| PTFE tubing 2mm ID | 2m | - | $4 |
| Micro servos 9g | 5-10 | - | $25 |
| Pulleys 10mm | 15 | Printed/brass | $5 |
| Return springs | 5 | Piano wire | $2 |
| **TOTAL** | - | - | **$46/hand** |

---

## TOE/TENDON FOOT DESIGN

### Simplified 3-Toe Foot

```
[HEEL / ANKLE MOTOR MOUNT]
           │
    ┌──────┴──────┐
    │ [ANKLE]     │
    └──────┬──────┘
           │
    ┌──────┴──────┐
    │  [METATARSAL] │ ← Motors here
    │   (MIDFOOT)   │
    └──────┬──────┘
           │
     ┌─────┼─────┐
     │     │     │
   [T1]  [T2]  [T3] ← Three toes
   Big   Mid   Small
```

### Toe Configuration

**Human-like 5 toes** (for realism):
- Hallux (big toe): 2 joints, 1 tendon
- Toes 2-5: 2 joints each, 1 tendon per toe
- **Total:** 5 tendons, 2 motors (grouped)

**Simplified 3 toes** (for function):
- Center toe: Main balance, 1 tendon
- Side toes: Stability, 1 tendon each
- **Total:** 3 tendons, 1-2 motors

### Tendon Path Through Leg

```
[KNEE MOTOR MOUNT]
       │
   ┌───┴───┐
   │TENDON │──→ Through hollow femur
   │GUIDE  │
   └───┬───┘
       │
   [KNEE JOINT] ← Tendon crosses joint with sheath
       │
   ┌───┴───┐
   │TENDON │──→ Through hollow tibia
   │GUIDE  │
   └───┬───┘
       │
   [ANKLE]
       │
   ┌───┴───┐
   │ TOES  │ ← Tendons split to individual toes
   └───┬───┘
       │
   [GROUND]
```

---

## LIMB MOTOR ASSIST

### Concept: Tendon Assist Springs

**Problem:** Holding a pose requires constant motor torque (wastes power, generates heat)

**Solution:** Springs store energy, motors only move between positions

```
ELBOW ASSIST:

    [UPPER ARM]
         │
    ┌────┴────┐
    │ ELBOW   │ ← Joint
    │  ●      │
    └───┬─────┘
        │
   [FOREARM]
        │
     [SPRING] ← Extension spring or torsion spring
        │
   [ANCHOR ON UPPER ARM]

Spring helps: Extend elbow (against gravity)
Motor provides: Flex elbow (curl)
Net result: 50% less power for holding extended pose
```

### Gravity Compensation

**Shoulder Counterbalance:**
```
    [TORSO]
      │
   [SHOULDER JOINT]
      │
   [UPPER ARM + FOREARM + HAND]
      │
   [COUNTERWEIGHT] ← Via cable over pulley at shoulder
      │
   [SPRING OR ELASTIC]

Weight of arm = Counterweight force
Motor only moves arm, doesn't hold it up
```

### Tendon-driven Joint Assist

**Knee Extension Assist (for walking):**
```
[THIGH MOTOR]
    │
    ├──[TENDON]──→ [KNEE] (flexion - curl knee)
    │
    └──[SPRING]──→ [KNEE ANCHOR] (extension - push knee straight)

When knee bends:
- Spring stretches, stores energy
- Releases energy to help straighten
- Motor provides control, spring provides power
```

**Calculated Assist Force:**
```
Spring constant k = 10 N/mm
Extension x = 30mm (knee bend)
Stored energy E = ½kx² = ½ × 10 × 30² = 4,500 mJ = 4.5 J

This energy returns during extension
Reducing motor power requirement by ~40%
```

---

## MANUFACTURING CONSIDERATIONS

### From "Manufacturing Fundamentals" Principles

#### 1. Design for Assembly (DFA)

**Current design:**
- 15 finger segments per hand
- Each needs pin insertion
- Tedious assembly

**Improved (snap-fit):**
- Living hinges for joints
- Snap-in pins
- Single-print finger chains

```
SNAP-FIT JOINT:

    ┌────────┐
    │Segment │
    │    ╭───┴──╮ ← Flex tab
    │    │  ●   │ ← Pin boss
    │    ╰──┬───╯
    └───────┼────┘
            │
    ┌───────┴────┐
    │    ●──╮    │ ← Receiving hole
    │Segment  │ ← Flex groove
    └───────────┘

Press together, tabs snap in
No tools needed, reversible
```

#### 2. Tolerance Stack-up

**Problem:** 20 joints × 0.2mm tolerance = 4mm error

**Solution:**
- Self-aligning features (conical pins)
- Adjustable tendon tensioners
- Compensating mechanisms

```
TENSION ADJUSTER:

[TENDON]──→[THREADED SLEEVE]──→[MOTOR PULLEY]
                │
            [ADJUST NUT]

Turn nut → changes tendon length
Compensates for tolerance stack-up
```

#### 3. Material Selection Matrix

| Part | Options | Selection Criteria |
|------|---------|-------------------|
| Finger segments | PLA, PETG, TPU, Nylon | TPU (flexible, grippy, durable) |
| Tendon guides | PTFE, POM, Brass | PTFE (lowest friction) |
| Pulleys | Printed, Aluminum, Brass | Aluminum (lightweight, strong) |
| Pins | Steel, Titanium, Carbon | Stainless steel (cost/durability) |
| Housing | PETG, ABS, Nylon | PETG (easy print, strong enough) |

#### 4. Economies of Scale

**Single hand print time:** 4 hours
**Batch of 4 hands:** 12 hours (3× not 4×)

**Manufacturing optimization:**
- Print plates with multiple parts
- Use 0.6mm nozzle for faster printing
- Automated tendon threading with jig

---

## INTEGRATION WITH AOS ROBOT BODY

### Modified RobotArm Class

```python
class TendonDrivenHand:
    """Fishing line tendon hand for AOS robot"""
    
    def __init__(self, side="left"):
        self.side = side
        self.fingers = {
            "thumb": TendonFinger(motor_id=0, joints=2),
            "index": TendonFinger(motor_id=1, joints=3),
            "middle": TendonFinger(motor_id=2, joints=3),
            "ring": TendonFinger(motor_id=3, joints=3),
            "pinky": TendonFinger(motor_id=4, joints=3),
        }
        self.wrist_flex = Servo(wrist_motor_id)
        
    def set_grip(self, grip_type):
        """
        grip_type: "open", "fist", "point", "pinch", "phone"
        """
        grips = {
            "open": {
                "thumb": 0, "index": 0, "middle": 0,
                "ring": 0, "pinky": 0
            },
            "fist": {
                "thumb": 0.8, "index": 1.0, "middle": 1.0,
                "ring": 1.0, "pinky": 1.0
            },
            "pinch": {
                "thumb": 0.9, "index": 0.9, "middle": 0,
                "ring": 0, "pinky": 0
            },
            "phone": {
                "thumb": 0.5, "index": 0.3, "middle": 0.3,
                "ring": 0, "pinky": 0
            }
        }
        
        if grip_type in grips:
            for finger_name, position in grips[grip_type].items():
                self.fingers[finger_name].set_position(position)
    
    def calibrate_tendons(self):
        """Set zero tension point"""
        for finger in self.fingers.values():
            finger.calibrate()


class TendonFinger:
    """Single tendon-driven finger"""
    
    def __init__(self, motor_id, joints=3):
        self.motor = Motor(motor_id)
        self.joints = joints
        self.tension = 0
        self.position = 0  # 0=extended, 1=curled
        self.mechanical_advantage = 2.0  # From pulley system
        
    def set_position(self, target):
        """
        target: 0.0 to 1.0 (extended to curled)
        Accounts for mechanical advantage
        """
        motor_position = target / self.mechanical_advantage
        self.motor.move_to(motor_position)
        self.position = target
        
    def get_force(self):
        """Calculate grip force based on motor torque and MA"""
        motor_torque = self.motor.current_torque()
        return motor_torque * self.mechanical_advantage
        
    def calibrate(self):
        """Find zero point (finger fully extended)"""
        # Release tension
        self.motor.set_torque(0)
        time.sleep(0.1)
        # Apply small tension to remove slack
        self.motor.set_position(0.05)
        self.zero_point = self.motor.position
```

### Limb Assist Integration

```python
class AssistedJoint:
    """Motor + spring assist for major joints"""
    
    def __init__(self, name, motor, spring_constant, assist_ratio=0.5):
        self.name = name
        self.motor = motor
        self.spring = Spring(k=spring_constant)
        self.assist_ratio = assist_ratio  # 0.5 = spring provides 50% of torque
        
    def move_to(self, angle, speed=100):
        """
        Move joint to angle with spring assist
        Spring helps in one direction, motor fights it in other
        """
        current = self.motor.position
        delta = angle - current
        
        # Spring always tries to return to neutral
        spring_torque = self.spring.torque_at(angle)
        
        if delta > 0:  # Moving against spring
            motor_torque = target_torque + spring_torque * self.assist_ratio
        else:  # Moving with spring
            motor_torque = target_torque - spring_torque * self.assist_ratio
            
        self.motor.move_with_torque(angle, motor_torque)
        
    def hold_position(self, angle):
        """Hold position - spring does most of the work"""
        spring_torque = self.spring.torque_at(angle)
        if abs(spring_torque) > 0.1:  # Spring is helping
            # Motor only provides control, minimal holding torque
            self.motor.set_torque(spring_torque * 0.1)  # 10% override
        else:
            # Near neutral, motor must hold
            self.motor.hold()
```

---

## TESTING & CALIBRATION

### Tendon Tension Calibration

```python
def calibrate_tendons():
    """Procedure for initial setup"""
    
    # 1. Release all tension
    for motor in motors:
        motor.set_torque(0)
    
    # 2. Manually extend all fingers
    print("Manually extend all fingers to flat position")
    input("Press ENTER when ready...")
    
    # 3. Apply minimum tension to remove slack
    for motor in motors:
        motor.set_current(0.1)  # Low current
        time.sleep(0.5)
        motor.zero_position = motor.encoder.read()
        
    # 4. Test range of motion
    print("Testing range of motion...")
    for i in range(101):
        pos = i / 100.0
        for finger in fingers:
            finger.set_position(pos)
        time.sleep(0.05)
        
    print("Calibration complete!")
```

### Friction Measurement

```
Test: Pull tendon with known force, measure movement

Force: 1N → Movement: 0mm (static friction)
Force: 2N → Movement: 5mm (overcame friction)

Friction coefficient = (2N - 1N) / Normal force
Target: <0.1 coefficient for smooth operation
```

### Fatigue Testing

```
Cycle test: 10,000 open/close cycles
- Check for tendon wear
- Monitor for stretch >2%
- Verify no guide tube damage

Expected life: 100,000+ cycles with Dyneema
```

---

## REFERENCES

### Manufacturing Fundamentals Principles Applied

1. **Geometric Dimensioning & Tolerancing (GD&T)**
   - Self-aligning features reduce tolerance requirements
   - Adjustable tensioners compensate for stack-up

2. **Material Selection**
   - Specific strength (strength/weight) prioritizes Dyneema
   - Friction coefficient prioritizes PTFE guides

3. **Assembly Design**
   - Snap-fit joints reduce part count
   - Modular fingers allow individual replacement

4. **Quality Control**
   - Calibrated tension ensures consistent performance
   - Force feedback enables adaptive grasping

### Additional Resources

- **"Tendon-Driven Robot Hands"** - Shadow Robot Company whitepaper
- **Dyneema® Technical Data Sheets** - DSM
- **PTFE Friction Coefficients** - McMaster-Carr engineering data
- **Robotis Dynamixel Servo Specs** - For motor selection

---

**Document Version:** 1.0  
**Last Updated:** 2026-03-29 04:07 UTC  
**Status:** Ready for COBRA hand prototyping
