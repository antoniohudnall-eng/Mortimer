# Robot Neck Mechanism Specification
## 2-DOF Head Movement System

**Purpose:** Enable head to tilt up/down (pitch) and turn left/right (yaw)  
**Applies to:** Cylon, C-3PO, and other humanoid robots  
**Updated:** March 29, 2026

---

## MECHANICAL OVERVIEW

### Degrees of Freedom (DOF)

| Axis | Movement | Range | Purpose |
|------|----------|-------|---------|
| **Pitch** | Up/Down (nod) | ±30° | Look up/down, acknowledge |
| **Yaw** | Left/Right (shake) | ±60° | Look around, track objects |

**Total: 2 DOF** (sufficient for most head movements)

**Note:** Roll (tilt side-to-side) intentionally omitted for simplicity. Can be added if needed.

---

## SERVO CONFIGURATION

### Servo Placement

```
                    [HEAD]
                       |
               ┌───────┴───────┐
               │   PITCH SERVO   │ ← Controls up/down
               │   (Side-mounted)│
               └───────┬───────┘
                       |
               ┌───────┴───────┐
               │    YAW SERVO    │ ← Controls left/right
               │   (Base-mounted)│
               └───────┬───────┘
                       |
                    [TORSO]
```

### Servo Specifications

#### Servo 1: Pitch (Up/Down)
**Model:** MG996R or DS3218  
**Torque:** 10-15 kg·cm  
**Speed:** 0.17s/60°  
**Range:** ±30° (mechanical limit: ±45° for safety margin)

**Mounting:**
- Horizontally mounted on neck frame
- Servo horn connects to head via linkage
- Counter-balanced to reduce load

**Load Calculation:**
```
Head weight: 1.5 kg
Distance from pivot: 8 cm
Torque required: 1.5 kg × 8 cm = 12 kg·cm
Safety factor: 1.5
Required servo: 18 kg·cm minimum
→ Use 20+ kg·cm servo (DS3218)
```

#### Servo 2: Yaw (Left/Right)
**Model:** MG996R or equivalent  
**Torque:** 10-15 kg·cm  
**Speed:** 0.17s/60°  
**Range:** ±60°

**Mounting:**
- Vertically mounted at neck base
- Direct drive or 1:1 gear ratio
- Central shaft through neck

**Load Calculation:**
```
Head + neck weight: 2.0 kg
Rotational inertia: I = ½mr²
Required torque: 10 kg·cm minimum
→ Use 15+ kg·cm servo (MG996R)
```

---

## MECHANICAL DESIGN

### Neck Structure

**Geometry:**
- **Height:** 60mm (neck length)
- **Diameter:** 80mm (at base), tapering to 60mm (at top)
- **Material:** PLA/PETG (3D printed) or aluminum (CNC)

**Components:**
1. **Base Plate** - Mounts to torso, holds yaw servo
2. **Mid Section** - Rigid tube, houses pitch servo
3. **Top Plate** - Mounts to head, driven by pitch servo
4. **Bearing Assembly** - Supports rotation, reduces friction

### Assembly Exploded View

```
     [HEAD MOUNTING PLATE]
              |
     [PITCH SERVO BRACKET]
              |
         [PITCH SERVO]
              |
    [NECK UPPER TUBE]
              |
    [SLIP RING ASSEMBLY]  ← For continuous rotation (optional)
              |
         [YAW SERVO]
              |
    [NECK BASE TUBE]
              |
     [TORSO MOUNTING PLATE]
```

### Critical Dimensions

```
          Head CG
            ↓
     ┌──────┴──────┐
     │             │
     │    HEAD     │ ← 1.5 kg
     │             │
     └──────┬──────┘
            │
    ┌───────┴───────┐
    │  PITCH PIVOT  │ ← 8cm from CG
    └───────┬───────┘
            │
        [NECK]
            │
    ┌───────┴───────┐
    │   YAW PIVOT   │ ← Base of neck
    └───────────────┘
            │
     [TORSO MOUNT]
```

---

## CABLE MANAGEMENT

### The Challenge
Head contains:
- 3 cameras (CSI ribbon cables)
- 2 microphones (I2S wires)
- 1 speaker (audio wires)
- 1 distance sensor (I2C wires)
- Power lines

All must pass through rotating neck!

### Solution: Cable Routing

**Method 1: Cable Trough (Simple)**
```
Neck is hollow tube with channel inside
Cables bundled together
Allow 20cm extra length for movement
Protect with flexible conduit

Max rotation: Limited by cable twist
```

**Method 2: Slip Ring (Advanced)**
```
Gold-contact slip ring at neck base
Allows continuous 360° rotation
No cable twist

Cost: $15-30
Wires: 12 circuits minimum
Current: 2A per circuit
```

**Recommended: Slip Ring for Yaw Axis**

### Wiring Through Neck

```
Neck Interior Cross-Section:

    ┌─────────────────┐
    │  [CAM 1 WIRES]  │ ← Center (straightest path)
    │  [CAM 2 WIRES]  │
    │  [CAM 3 WIRES]  │
    │  [MIC WIRES]    │
    │  [SPEAKER]      │
    │  [POWER]        │
    │  [I2C BUS]      │
    └─────────────────┘

All cables exit through center shaft to slip ring
```

---

## RANGE OF MOTION

### Pitch (Up/Down)

| Angle | Position | Use Case |
|-------|----------|----------|
| +30° | Looking up | Scan ceiling, tall objects |
| 0° | Level | Normal viewing |
| -30° | Looking down | Ground inspection, acknowledgment |

**Speed:**
- Normal: 30°/second (2 seconds full range)
- Fast: 90°/second (emergency avoidance)

**Acceleration:** Limited to prevent whiplash

### Yaw (Left/Right)

| Angle | Position | Use Case |
|-------|----------|----------|
| +60° | Far left | Looking behind left shoulder |
| +30° | Left | Conversation, tracking |
| 0° | Center | Forward facing |
| -30° | Right | Conversation, tracking |
| -60° | Far right | Looking behind right shoulder |

**Speed:**
- Normal: 45°/second
- Fast: 120°/second (quick scan)

### Combined Movements

**Natural Head Motion:**
```
Conversation: Yaw ±20°, Pitch ±10°
Searching: Yaw ±60°, slow sweep
Surprise: Pitch up +30°, fast
Acknowledge: Pitch down -15°, slow
```

---

## CONTROL SOFTWARE

### Servo Control

```python
class NeckController:
    def __init__(self):
        self.pitch_servo = Servo(pin=12, min_angle=-30, max_angle=30)
        self.yaw_servo = Servo(pin=13, min_angle=-60, max_angle=60)
        
        # Current position
        self.pitch = 0
        self.yaw = 0
        
    def move_head(self, target_pitch, target_yaw, speed=30):
        """
        Move head to target position
        speed: degrees per second
        """
        # Calculate time needed
        pitch_diff = abs(target_pitch - self.pitch)
        yaw_diff = abs(target_yaw - self.yaw)
        max_diff = max(pitch_diff, yaw_diff)
        duration = max_diff / speed
        
        # Move servos
        self.pitch_servo.move(target_pitch, duration)
        self.yaw_servo.move(target_yaw, duration)
        
        self.pitch = target_pitch
        self.yaw = target_yaw
    
    def look_at(self, x, y, z):
        """
        Calculate head angles to look at point in space
        x, y, z in mm relative to neck base
        """
        # Calculate pitch (up/down)
        horizontal_dist = math.sqrt(x**2 + y**2)
        pitch = math.degrees(math.atan2(z, horizontal_dist))
        
        # Calculate yaw (left/right)
        yaw = math.degrees(math.atan2(y, x))
        
        # Limit to mechanical constraints
        pitch = max(-30, min(30, pitch))
        yaw = max(-60, min(60, yaw))
        
        self.move_head(pitch, yaw)
    
    def track_object(self, object_position):
        """Continuously track moving object"""
        while object_visible:
            self.look_at(object_position.x, 
                        object_position.y, 
                        object_position.z)
            time.sleep(0.05)  # 20Hz update
    
    def nod(self, times=1):
        """Nod head (yes)"""
        for _ in range(times):
            self.move_head(-15, self.yaw)  # Down
            time.sleep(0.2)
            self.move_head(15, self.yaw)   # Up
            time.sleep(0.2)
            self.move_head(0, self.yaw)    # Center
    
    def shake(self, times=1):
        """Shake head (no)"""
        for _ in range(times):
            self.move_head(self.pitch, 20)   # Right
            time.sleep(0.15)
            self.move_head(self.pitch, -20)  # Left
            time.sleep(0.15)
            self.move_head(self.pitch, 0)    # Center
```

### Smooth Motion Profiles

**S-curve acceleration (jerk-limited):**
```
Velocity
  │    ╭────╮
  │   ╱      ╲
  │  ╱        ╲
  │ ╱          ╲
  │╱            ╲____
  └──────────────────→ Time
    ↑  ↑    ↑  ↑
   Accel Constant Decel
```

**Implementation:**
```python
def smooth_move(current, target, t, total_t):
    """S-curve interpolation"""
    if t < total_t / 2:
        # Acceleration phase
        ratio = (t / (total_t / 2)) ** 2
    else:
        # Deceleration phase
        ratio = 1 - ((total_t - t) / (total_t / 2)) ** 2
    
    return current + (target - current) * ratio
```

---

## SAFETY FEATURES

### Mechanical Limits

**Hard Stops:**
- Physical end stops prevent over-rotation
- Prevents servo damage
- Rubber bumpers for quiet operation

**Soft Limits (Software):**
```python
MAX_PITCH = 30
MAX_YAW = 60

if abs(commanded_pitch) > MAX_PITCH:
    print(f"Warning: Pitch limited to {MAX_PITCH}°")
    commanded_pitch = sign(commanded_pitch) * MAX_PITCH
```

### Current Sensing

Monitor servo current for:
- **Stall detection:** Current > 1A = stuck
- **Collision detection:** Sudden current spike
- **Thermal protection:** Shutdown if overheating

### Emergency Stop

```python
def emergency_stop(self):
    """Immediate stop, return to center"""
    self.pitch_servo.disable()
    self.yaw_servo.disable()
    time.sleep(0.5)
    # Re-center slowly
    self.move_head(0, 0, speed=10)
```

---

## 3D PRINT FILES

### Recommended Parts

**Neck_Base.stl**
- Torso mounting interface
- Yaw servo cavity
- Cable entry points

**Neck_Mid.stl**
- Structural tube
- Pitch servo mount
- Internal cable channels

**Neck_Top.stl**
- Head mounting interface
- Pitch pivot bearing
- Camera cable pass-through

**Servo_Horn_Linkage.stl**
- Connects pitch servo to head
- Allows arc motion
- Adjustable length

**Bearing_Cap.stl**
- Supports pitch axis
- Reduces friction
- Captures thrust loads

### Print Settings

**Material:** PETG (strength + durability)
**Infill:** 40% (structural parts), 20% (cosmetic)
**Walls:** 4 perimeters
**Support:** Required for overhangs

---

## ASSEMBLY INSTRUCTIONS

### Step-by-Step

1. **Install Yaw Servo**
   - Mount to base plate
   - Connect output shaft to mid section
   - Route wires through center

2. **Install Pitch Servo**
   - Mount to mid section
   - Orient horizontally
   - Test range of motion

3. **Attach Slip Ring** (if using)
   - Mount to base
   - Connect rotating side to mid section
   - Wire all circuits

4. **Connect Linkage**
   - Servo horn to head plate
   - Adjust for neutral position
   - Secure with screws

5. **Cable Management**
   - Bundle all head wires
   - Route through neck
   - Connect to slip ring
   - Leave slack for movement

6. **Calibration**
   - Set both servos to 90° (center)
   - Verify mechanical limits
   - Test full range slowly
   - Mark neutral position

7. **Software Setup**
   - Calibrate servo angles
   - Set limits in code
   - Test basic movements
   - Verify smooth motion

---

## TESTING PROTOCOL

### Movement Tests
- [ ] Full pitch range (smooth, no binding)
- [ ] Full yaw range (smooth, no cable strain)
- [ ] Combined movements (diagonals)
- [ ] Speed test (slow to fast)
- [ ] Return to center (accurate)
- [ ] Repeatability (same position multiple times)

### Load Tests
- [ ] Static holding (maintain position for 1 min)
- [ ] Dynamic tracking (follow moving object)
- [ ] Shake resistance (torso moves, head stable)

### Safety Tests
- [ ] Current limit (stops if overloaded)
- [ ] Temperature (doesn't overheat)
- [ ] Emergency stop (responds immediately)

---

## SPECIFICATION SUMMARY

| Parameter | Value |
|-----------|-------|
| **DOF** | 2 (pitch + yaw) |
| **Pitch Range** | ±30° |
| **Yaw Range** | ±60° |
| **Pitch Servo** | DS3218 (20 kg·cm) |
| **Yaw Servo** | MG996R (15 kg·cm) |
| **Max Speed** | 90°/sec pitch, 120°/sec yaw |
| **Cable Pass-through** | Slip ring recommended |
| **Neck Height** | 60mm |
| **Neck Diameter** | 80mm (base), 60mm (top) |
| **Weight** | ~200g (neck + servos) |
| **Cost** | ~$40 (servos + hardware) |

---

**Document Version:** 1.0  
**Last Updated:** 2026-03-29 03:46 UTC  
**Status:** Ready for implementation
