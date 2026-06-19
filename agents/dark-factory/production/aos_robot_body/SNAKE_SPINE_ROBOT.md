# Snake Spine Robot - Design Specification

**Codename:** COBRA (COordinated Biomimetic Robotic Architecture)  
**Type:** Vertebrate-inspired humanoid with flexible spine  
**Status:** Design Phase  
**Updated:** 2026-03-29

---

## OVERVIEW

Traditional robots use rigid torsos. COBRA replaces this with a **segmented vertebral column** - like a human spine with individual vertebrae connected by joints. This provides:
- Natural weight distribution
- Shock absorption
- Dynamic posture adjustment
- **Integrated battery storage** within vertebrae
- **Solar panel mounting** on spine segments

---

## SPINE ARCHITECTURE

### Vertebral Segments

```
                    [HEAD]
                       │
                   [Atlas] ← C1 - Supports head, minimal rotation
                       │
                  [Axis] ← C2 - Head rotation joint
                       │
                 [C3-C7] ← Cervical vertebrae (neck)
                       │
              [T1-T12] ← Thoracic vertebrae (chest/ribs)
                       │
              [L1-L5] ← Lumbar vertebrae (lower back)
                       │
                [Sacrum] ← Pelvis connection
                       │
                   [Pelvis]
                  /        \
              [Leg]      [Leg]
```

### Segment Specifications

| Region | Count | Height Each | Total Height | Function |
|--------|-------|-------------|--------------|----------|
| **Cervical** (C1-C7) | 7 | 15mm | 105mm | Neck flexibility |
| **Thoracic** (T1-T12) | 12 | 20mm | 240mm | Chest cavity, arm mounts |
| **Lumbar** (L1-L5) | 5 | 25mm | 125mm | Weight bearing, balance |
| **Sacrum** | 1 | 30mm | 30mm | Pelvis anchor |
| **TOTAL** | **25 segments** | - | **500mm** | Full spine |

### Joint Configuration (Per Vertebra)

Each intervertebral joint provides **2 DOF**:
- **Flexion/Extension** (forward/back bend): ±15°
- **Lateral Flexion** (side bend): ±10°
- **Rotation** (twist): ±5° (limited to prevent cable twist)

**Total spine flexibility:**
- Forward bend: 375mm arc
- Side bend: 250mm arc
- Twist: 125° total

---

## BATTERY STORAGE SYSTEM

### Vertebrae-as-Batteries Concept

Each thoracic and lumbar vertebra houses **cylindrical Li-ion cells** arranged around a central channel:

```
Vertebra Cross-Section:

     ┌─────────────────────┐
     │  ▓  ┌─────────┐  ▓  │  ← Solar panel on outer surface
     │ ▓▓  │  CORE   │ ▓▓ │  ▓ = 18650 Li-ion cells
     │  ▓  │ CHANNEL │  ▓  │  CORE = Wiring, cooling, sensors
     │ ▓▓  │ (wires, │ ▓▓ │
     │  ▓  │ coolant)│  ▓  │
     └─────────────────────┘
           │ ▲ │ ▲ │ ▲ │
           └─┴─┴─┴─┴─┘
              Servo
```

### Battery Configuration by Size

#### 1. COBRA-MINI (Desktop/Companion)
- **Scale:** 1:6 (30cm tall)
- **Battery type:** 14500 Li-ion (AA-size)
- **Storage:** Lumbar vertebrae only (L1-L5)
- **Capacity:** 5 × 800mAh = **4,000mAh @ 3.7V = 14.8Wh**
- **Solar:** Integrated cells on T1-T6 (6 × 30mm × 20mm cells)
- **Charge rate:** ~200mA in full sun = 20-hour full charge
- **Runtime:** 8-12 hours active, 48 hours standby

#### 2. COBRA-MIDI (Human-scale)
- **Scale:** 1:2 (90cm tall)
- **Battery type:** 18650 Li-ion
- **Storage:** Thoracic T1-T12 + Lumbar L1-L5
- **Capacity:** 17 × 3,000mAh = **51,000mAh @ 3.7V = 188.7Wh**
- **Solar:** Foldable panels on backpack, T5-T9 integrated
- **Charge rate:** 2A = 25-hour full charge
- **Runtime:** 16-24 hours active, 1 week standby

#### 3. COBRA-MAX (Life-size)
- **Scale:** 1:1 (175cm tall)
- **Battery type:** 21700 Li-ion (high capacity)
- **Storage:** All thoracic + lumbar + cervical C3-C7
- **Capacity:** 24 × 5,000mAh = **120,000mAh @ 3.7V = 444Wh**
- **Solar:** Flexible panels on back/shoulders + removable solar cloak
- **Charge rate:** 5A with solar cloak = 24-hour full charge
- **Runtime:** 24-48 hours active, 2 weeks standby

### Battery Management System (BMS)

Each vertebra includes:
- **Cell protection:** Overcharge, overdischarge, short-circuit
- **Cell balancing:** Passive balancing every charge cycle
- **Temperature monitoring:** Thermistor per 2 cells
- **Communication:** I2C to central brain

```python
class VertebralBattery:
    """Battery management per vertebra"""
    
    def __init__(self, segment_id, cell_count):
        self.segment_id = segment_id
        self.cell_count = cell_count
        self.cells = [LiIonCell() for _ in range(cell_count)]
        self.bms = BMSController(cells)
        
    def get_status(self):
        return {
            "voltage": self.bms.pack_voltage(),
            "current": self.bms.current_draw(),
            "soc": self.bms.state_of_charge(),  # %
            "temp": self.bms.max_temperature(),
            "health": self.bms.soh(),  # State of health
        }
    
    def charge(self, current):
        """Accept charge from solar or external"""
        self.bms.charge(current)
    
    def discharge(self, current):
        """Provide power to systems"""
        if self.bms.can_discharge(current):
            return self.bms.discharge(current)
        return False  # Insufficient charge
```

---

## SOLAR INTEGRATION

### Solar Panel Placement

#### COBRA-MINI (Embedded)
```
[T5-T6 vertebrae outer surface]
┌─────────────────┐
│ ╔═══╗ ╔═══╗     │  ╔═══╗ = 30×20mm solar cell
│ ║ █ ║ ║ █ ║     │  █ = Connection to charge controller
│ ╚═══╝ ╚═══╝     │
└─────────────────┘
Total: 4 cells × 0.5V × 100mA = 2V @ 200mA = 0.4W
```

#### COBRA-MIDI (Backpack + Embedded)
- **Embedded:** T5-T9 vertebrae (5 × 60mm × 40mm cells)
- **Backpack:** Detachable solar panel array (200mm × 150mm)
- **Total:** ~8W peak output

#### COBRA-MAX (Cloak + Embedded)
- **Embedded:** T1-L5 all have curved solar cells (20 × 100mm × 50mm)
- **Cloak:** Wearable flexible solar fabric (400mm × 300mm)
- **Total:** ~25W peak output

### Solar Charge Controller

Located in L3 (center of gravity):
```
┌─────────────────────────┐
│  MPPT Charge Controller │
│  - Input: 6-24V solar   │
│  - Output: 4.2V Li-ion  │
│  - Efficiency: 95%      │
│  - Max current: 2A      │
└─────────────────────────┘
```

### Power Flow

```
Solar Panels → MPPT Controller → Vertebrae Batteries → DC-DC Converter → 5V/12V Rails
                                    ↓                        ↓
                              BMS Monitoring           Brain + Servos + Sensors
```

---

## MECHANICAL DESIGN

### Vertebrae Construction

**Material:** Carbon fiber reinforced nylon (PA12-CF)
- **Strength:** 80 MPa tensile
- **Weight:** 1.2g/cm³ (vs 2.7g/cm³ for aluminum)
- **Flexibility:** Slight give for shock absorption
- **Printability:** Standard FDM with hardened nozzle

### Joint Mechanism

**Dual-Axis Gimbal per Joint:**
```
    [Upper Vertebra]
          │
    ┌─────┴─────┐
    │   [X]     │ ← Pitch servo (forward/back)
    │    │      │
    │   [Y]     │ ← Roll servo (side bend)
    │    │      │
    └─────┬─────┘
          │
    [Lower Vertebra]
```

**Actuation:**
- **Micro servos** (for COBRA-MINI): 9g servos, 1.5 kg·cm
- **Standard servos** (for COBRA-MIDI/MAX): MG90S, 2.2 kg·cm
- **Tendon drive** (alternative): Single motor pulls cable that bends multiple vertebrae

### Tendon Drive Option (Advanced)

Instead of 24 individual servos, use **4 motors + cable tendons**:
```
Motor 1: Left tendons (bends spine right)
Motor 2: Right tendons (bends spine left)
Motor 3: Front tendons (bends spine back)
Motor 4: Back tendons (bends spine forward)

[Cable routing through vertebrae core channel]
```

**Advantages:**
- 4 motors vs 48 servos (COBRA-MAX)
- Lighter weight
- Lower power consumption
- Smoother, more organic movement

**Disadvantages:**
- Complex cable routing
- Requires tension maintenance
- Less precise per-vertebra control

---

## ELECTRONICS INTEGRATION

### Spine-as-Backbone Concept

The spine is not just mechanical—it's the **central nervous system**:

```
Vertebrae Core Channel Contents:
├── Power bus (12V main, 5V regulated)
├── CAN bus (communication between vertebrae)
├── I2C bus (sensor data)
├── PWM lines (servo control)
├── Cooling tube (air or liquid)
└── Spare wires (expansion)
```

### Distributed Computing

Each vertebra is a **smart node**:

```
[Vertebra Microcontroller - STM32F103 or RP2040]
├── Functions:
│   ├── Local servo control (2 DOF)
│   ├── BMS monitoring
│   ├── IMU (accel/gyro for that segment)
│   ├── Temperature sensor
│   └── CAN bus communication
├── Power: 5V from spine bus
├── Data: CAN bus to brain
└── Update rate: 100Hz
```

### Brain Location

**Primary brain:** S2-S3 vertebrae (sacral, protected by pelvis)
- **Why:** Lowest center of gravity, protected by pelvis/hips
- **Secondary:** Can also mount in skull (head-brain) for shorter signal paths to cameras

```
[S2 Vertebra - Brain Housing]
┌─────────────────────────┐
│  ┌───────────────────┐  │
│  │   Raspberry Pi 5  │  │ ← Main compute
│  │   8GB RAM, AI HAT │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │   AOS Brain PCB   │  │ ← Custom 7-region neural board
│  │   (548k nodes)    │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │  Power Management │  │ ← DC-DC, distribution
│  └───────────────────┘  │
└─────────────────────────┘
```

---

## COBRA MODELS COMPARISON

| Feature | COBRA-MINI | COBRA-MIDI | COBRA-MAX |
|---------|------------|------------|-----------|
| **Scale** | 1:6 (30cm) | 1:2 (90cm) | 1:1 (175cm) |
| **Vertebrae** | 12 (simplified) | 25 (full) | 25 (full) |
| **Battery** | 14500 cells | 18650 cells | 21700 cells |
| **Capacity** | 14.8Wh | 188.7Wh | 444Wh |
| **Solar** | Embedded 0.4W | Embedded 8W | Embedded 25W |
| **Weight** | 800g | 8kg | 45kg |
| **Servos** | 18 micro + tendons | 24 standard + tendons | 48 standard + tendons |
| **Cost** | $299 | $1,299 | $4,999 |
| **Target** | Hobbyist/educational | Research/prosumer | Commercial/enterprise |

---

## MANUFACTURING

### 3D Print Files Needed

**COBRA-MINI (Simplified spine):**
- `COBRA_mini_vertebra_cervical.stl` × 4
- `COBRA_mini_vertebra_thoracic.stl` × 4 (with battery cavity)
- `COBRA_mini_vertebra_lumbar.stl` × 3 (with battery cavity)
- `COBRA_mini_sacrum.stl` × 1
- `COBRA_mini_joint_gimbal.stl` × 11
- `COBRA_mini_tendon_collar.stl` × 12

**COBRA-MIDI/MAX (Full spine):**
- `COBRA_cervical_C1_atlas.stl`
- `COBRA_cervical_C2_axis.stl`
- `COBRA_cervical_C3-7.stl` × 5
- `COBRA_thoracic_T1-12.stl` × 12 (with solar + battery)
- `COBRA_lumbar_L1-5.stl` × 5 (with battery)
- `COBRA_sacrum.stl`
- `COBRA_pelvis.stl`
- `COBRA_joint_*.stl` (various for each region)

### BOM (COBRA-MINI)

| Component | Qty | Cost |
|-----------|-----|------|
| 14500 Li-ion cells | 5 | $15 |
| BMS modules | 1 | $8 |
| Solar cells 30×20mm | 4 | $12 |
| MPPT controller | 1 | $15 |
| 9g micro servos | 18 | $36 |
| STM32 microcontrollers | 12 | $24 |
| Carbon fiber nylon filament | 200g | $15 |
| Cables, connectors | 1 set | $20 |
| **TOTAL** | - | **$145** |

Retail price: $299 (2× materials cost)

---

## SOFTWARE

### Spine Controller

```python
class SnakeSpineController:
    """Control the entire vertebral column"""
    
    def __init__(self, vertebrae_count=25):
        self.vertebrae = [Vertebra(i) for i in range(vertebrae_count)]
        self.servos = [Servo(i) for i in range(vertebrae_count * 2)]
        self.tendons = TendonSystem()  # Optional
        
    def set_posture(self, curvature_profile):
        """
        Set spine to curved posture
        curvature_profile: list of (pitch, roll) for each vertebra
        """
        for i, (pitch, roll) in enumerate(curvature_profile):
            self.vertebrae[i].set_angle(pitch, roll)
            
    def natural_standing(self):
        """S-curve alignment like human standing"""
        # Cervical: slight forward (lordosis)
        # Thoracic: backward (kyphosis)
        # Lumbar: forward (lordosis)
        profile = [
            # Cervical C1-C7: lordotic curve
            *[(5, 0) for _ in range(7)],
            # Thoracic T1-T12: kyphotic curve
            *[(-3, 0) for _ in range(12)],
            # Lumbar L1-L5: lordotic curve
            *[(8, 0) for _ in range(5)],
        ]
        self.set_posture(profile)
    
    def forward_bend(self, angle=30):
        """Bend forward at waist"""
        # Distribute bend across lumbar vertebrae
        bend_per_vertebra = angle / 5
        for i in range(17, 22):  # L1-L5
            self.vertebrae[i].set_angle(bend_per_vertebra, 0)
    
    def balance_adjustment(self, imu_data):
        """Active balancing via spine adjustment"""
        # Detect tilt from IMU
        pitch_error = imu_data['pitch']  # Forward/back tilt
        roll_error = imu_data['roll']    # Side tilt
        
        # Counter-bend spine
        correction_factor = 0.5
        for v in self.vertebrae[10:20]:  # Thoracic-lumbar region
            v.adjust_angle(
                -pitch_error * correction_factor,
                -roll_error * correction_factor
            )

class Vertebra:
    """Individual vertebra controller"""
    
    def __init__(self, id):
        self.id = id
        self.pitch = 0
        self.roll = 0
        self.imu = IMU()
        self.battery = VertebralBattery()
        
    def set_angle(self, pitch, roll):
        """Set joint angles with limits"""
        self.pitch = clamp(pitch, -15, 15)
        self.roll = clamp(roll, -10, 10)
        self._update_servos()
        
    def get_status(self):
        return {
            "id": self.id,
            "angle": (self.pitch, self.roll),
            "imu": self.imu.read(),
            "battery": self.battery.get_status(),
            "temp": self.read_temperature(),
        }
```

### Power Management

```python
class CobraPowerManager:
    """Manage distributed battery system"""
    
    def __init__(self, vertebrae):
        self.vertebrae = vertebrae
        self.solar_controller = MPPTController()
        self.load_balancer = LoadBalancer()
        
    def get_total_power(self):
        """Calculate available power"""
        total = 0
        for v in self.vertebrae:
            status = v.battery.get_status()
            total += status['voltage'] * status['max_current']
        return total
    
    def optimize_discharge(self, power_demand):
        """Pull power from best vertebrae first"""
        # Prioritize:
        # 1. Highest SOC vertebrae (wear leveling)
        # 2. Thermally cool vertebrae
        # 3. Distributed load across all
        
    def solar_charge(self, irradiance):
        """Charge from available solar"""
        available = self.solar_controller.get_output(irradiance)
        self.distribute_charge(available)
        
    def emergency_power(self):
        """Enter low-power mode"""
        # Shutdown non-critical vertebrae
        # Keep only brain + balance active
        # Rely on sacrum battery only
```

---

## ADVANTAGES OVER RIGID TORSO

| Aspect | Rigid Torso | Snake Spine |
|--------|-------------|-------------|
| **Weight distribution** | Fixed | Dynamic, adjustable |
| **Shock absorption** | Minimal | Distributed across 25 joints |
| **Balance recovery** | Ankle only | Spine + ankle combined |
| **Battery capacity** | Central pack | Distributed, 2-3× more volume |
| **Solar area** | Back only | Full spine surface |
| **Repairability** | Replace whole torso | Replace individual vertebra |
| **Customization** | Fixed height | Add/remove vertebrae |
| **Cost** | Single large mold | Print individual parts |
| **Shipping** | Bulky | Flat-pack vertebrae kits |

---

## IMPLEMENTATION ROADMAP

### Phase 1: COBRA-MINI (4 weeks)
- [ ] Design simplified 12-vertebra spine
- [ ] Integrate 14500 batteries
- [ ] Build solar charging system
- [ ] Test tendon vs servo actuation
- [ ] Validate 8-hour runtime target

### Phase 2: COBRA-MIDI (8 weeks)
- [ ] Scale to 25-vertebra full spine
- [ ] Integrate 18650 batteries with BMS
- [ ] Backpack solar array
- [ ] Advanced balancing algorithms
- [ ] Human-scale testing

### Phase 3: COBRA-MAX (12 weeks)
- [ ] Life-size implementation
- [ ] 21700 batteries + solar cloak
- [ ] Full 48-servo system
- [ ] Commercial certification
- [ ] Production tooling

---

## SAFETY CONSIDERATIONS

### Battery Safety
- **Thermal runaway prevention:** BMS with temp cutoff at 60°C
- **Cell spacing:** 2mm minimum between cells for heat dissipation
- **Venting:** Each vertebra has pressure relief path
- **Fire containment:** Ceramic fiber barriers between cell groups

### Mechanical Safety
- **Range limiting:** Software + hard stops prevent over-rotation
- **Current sensing:** Detect stuck servos, limit torque
- **Emergency release:** Quick-disconnect for battery service
- **Fail-safe:** Loss of power = servos to neutral, spine collapses safely

---

**Document Version:** 1.0  
**Last Updated:** 2026-03-29 04:04 UTC  
**Status:** Ready for COBRA-MINI prototype
