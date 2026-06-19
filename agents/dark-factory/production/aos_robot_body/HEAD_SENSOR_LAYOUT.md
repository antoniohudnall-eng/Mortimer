# Robot Head - Sensor Layout Specification
## Hardware Integration Guide

**Updated:** March 29, 2026  
**Applies to:** Cylon, C-3PO, R2-D2, Nomad (humanoid heads)

---

## SENSOR CONFIGURATION

### Audio System

#### Microphones (2x)
**Purpose:** Stereo audio input, sound localization, voice commands

**Placement:**
- **Left Ear:** 1x MEMS microphone (SPH0645LM4H or similar)
- **Right Ear:** 1x MEMS microphone
- **Spacing:** 160mm (human ear spacing for stereo localization)

**Wiring:**
```
Left Mic  → GPIO 18 (I2S CLK)
          → GPIO 19 (I2S WS)
          → GPIO 20 (I2S DATA)

Right Mic → GPIO 21 (I2S CLK)
          → GPIO 26 (I2S WS)
          → GPIO 16 (I2S DATA)
```

**Specifications:**
- Sample rate: 16kHz (voice) or 48kHz (full audio)
- Bit depth: 16-bit
- Sensitivity: -26 dBFS
- SNR: 64 dB

**Use Cases:**
- Voice command recognition
- Sound source localization (left/right)
- Audio recording
- Noise cancellation (with phone mic)

---

#### Speaker (1x)
**Purpose:** Audio output, TTS, sound effects

**Placement:**
- **Mouth Position:** Center of face, behind speaker grille
- **Size:** 3W 4Ω mini speaker (28mm diameter)
- **Alternative:** Use phone speaker if docked

**Wiring:**
```
Speaker → Amplifier (PAM8403) → GPIO 40 (PWM0) → Pi Zero
        → 5V Power
        → GND
```

**Amplifier:**
- PAM8403 3W stereo amplifier (use single channel)
- Volume control via PWM
- Power: 5V from Pi

**Specifications:**
- Power: 3W max
- Impedance: 4Ω
- Frequency: 200Hz - 20kHz
- Grille: 3D printed with acoustic holes

**Mounting:**
```
[Face Panel]
    |
[Speaker Grille - 3D Printed]
    |
[Speaker (28mm)]
    |
[Amplifier Board]
    |
[Pi Zero Audio Out]
```

---

### Vision System

#### Cameras (3x)
**Purpose:** Stereoscopic vision, depth perception, panoramic view

**Placement:**

**Camera 1 - Center (Primary)**
- **Position:** Forehead/upper face, center
- **Angle:** Straight ahead (0°)
- **FOV:** 120° wide angle
- **Resolution:** 1080p (Pi Camera Module 3 Wide)
- **Purpose:** Main vision, facial recognition, object detection

**Camera 2 - Left**
- **Position:** Left temple/side of head
- **Angle:** 45° outward
- **FOV:** 90° standard
- **Resolution:** 720p (Pi Camera Module 3)
- **Purpose:** Peripheral vision, side obstacle detection

**Camera 3 - Right**
- **Position:** Right temple/side of head
- **Angle:** 45° outward
- **FOV:** 90° standard
- **Resolution:** 720p (Pi Camera Module 3)
- **Purpose:** Peripheral vision, side obstacle detection

**Wiring (CSI):**
```
Camera 1 (Center) → CSI Port 0 (primary)
Camera 2 (Left)   → CSI Port 1 (via multiplexer)
Camera 3 (Right)  → CSI Port 1 (via multiplexer)

Multiplexer: Adafruit CSI/DSI HUB
```

**Specifications:**
| Camera | Position | FOV | Resolution | FPS |
|--------|----------|-----|------------|-----|
| Center | Forehead | 120° | 1920x1080 | 30 |
| Left   | Temple   | 90°  | 1280x720  | 30 |
| Right  | Temple   | 90°  | 1280x720  | 30 |

**Stereoscopic Configuration:**
- Baseline (Camera 2-3): 160mm (human eye spacing)
- Depth calculation: Triangulation between left/right cameras
- Minimum depth: 30cm
- Maximum depth: 10m

**Mounting:**
```
     [Camera 1 - Center]
            |
    [Face Panel - Forehead]
            |
    [Camera 2]    [Camera 3]
    [Left]        [Right]
    [Temple]      [Temple]
```

**3D Print Considerations:**
- Camera windows: Clear PETG or acrylic inserts
- Sunshade: Overhang above each camera to reduce glare
- Alignment pins: Ensure cameras point in correct directions
- Cable channels: Internal routing to Pi Zero

---

### Distance Sensing

#### Distance Sensor (1x) - NOSE POSITION
**Purpose:** Front obstacle detection, collision avoidance, depth measurement

**Placement:**
- **Position:** Center of face, nose area
- **Height:** 50mm below eyes (natural nose position)
- **Sensor Type:** VL53L5CX Time-of-Flight (8x8 zones) or HC-SR04

**Recommended Sensor Options:**

**Option A: VL53L5CX (Advanced)**
- Type: Time-of-Flight laser
- Range: 4cm - 400cm
- Accuracy: ±5cm
- Zones: 8x8 multizone (64 measurement points)
- Interface: I2C
- Price: $15

**Option B: HC-SR04 (Basic)**
- Type: Ultrasonic
- Range: 2cm - 400cm
- Accuracy: ±3cm
- Beam angle: 15°
- Interface: GPIO trigger/echo
- Price: $3

**Wiring:**

**VL53L5CX (I2C):**
```
VCC  → 3.3V
GND  → GND
SDA  → GPIO 2 (SDA)
SCL  → GPIO 3 (SCL)
INT  → GPIO 17 (optional interrupt)
```

**HC-SR04 (GPIO):**
```
VCC  → 5V
GND  → GND
TRIG → GPIO 23
ECHO → GPIO 24 (with voltage divider)
```

**Specifications:**
| Feature | VL53L5CX | HC-SR04 |
|---------|----------|---------|
| Range | 4-400cm | 2-400cm |
| Accuracy | ±5cm | ±3cm |
| Speed | Fast | Slower (sound) |
| Zones | 8x8 | Single |
| Price | $15 | $3 |
| Best For | Advanced | Budget |

**Mounting:**
```
[Face Panel]
    |
[Sensor Housing - 3D Printed]
    |
[VL53L5CX Sensor]
    |
[Acrylic Window (if using ToF)]
```

**Visual Design:**
- Sensor positioned where nose would be
- Can be styled as:
  - Cylon: Red glowing "eye" nose
  - C-3PO: Gold vent-like grille
  - R2-D2: Blue sensor dome
  - Nomad: Antenna base

**Software Integration:**
```python
# Distance reading in brain_heart_stomach.py
if sensor.distance < 20:  # 20cm threshold
    action = "avoid_obstacle"
    motor.backward(10)  # 10cm
    motor.turn(45)      # 45 degrees
```

---

## COMPLETE HEAD WIRING DIAGRAM

```
┌─────────────────────────────────────────┐
│            ROBOT HEAD                   │
│                                         │
│   ┌─────────┐                           │
│   │ CAM 2   │    ┌─────────┐          │
│   │ (Left)  │    │ CAM 1   │          │
│   └────┬────┘    │ (Center)│          │
│        │          └────┬────┘          │
│        │               │                │
│        └───────┬───────┘                │
│                │                        │
│         ┌──────┴──────┐                 │
│         │ DISTANCE    │                 │
│         │ SENSOR      │                 │
│         │ (Nose)      │                 │
│         └──────┬──────┘                 │
│                │                        │
│   ┌─────────┐  │  ┌─────────┐           │
│   │ MIC L   │  │  │ MIC R   │           │
│   │ (Left)  │  │  │ (Right) │           │
│   └────┬────┘  │  └────┬────┘           │
│        │       │       │                │
│   ┌────┴───────┴───────┴────┐           │
│   │      SPEAKER            │           │
│   │      (Mouth)            │           │
│   └───────────┬─────────────┘            │
│               │                         │
└───────────────┼─────────────────────────┘
                │
                │ (Cable Bundle)
                │
    ┌───────────┴───────────┐
    │     PI ZERO 2W        │
    │  ┌─────────────────┐  │
    │  │ GPIO 2-3: I2C   │  │ ← Distance sensor, mics
    │  │ GPIO 18-21: I2S │  │ ← Microphones
    │  │ GPIO 23-24: GPIO│  │ ← HC-SR04 (if used)
    │  │ GPIO 40: PWM    │  │ ← Speaker
    │  │ CSI: Cameras    │  │ ← 3x Cameras
    │  └─────────────────┘  │
    └───────────────────────┘
```

---

## POWER BUDGET (Head Only)

| Component | Current | Voltage | Power |
|-----------|---------|---------|-------|
| 2x Microphones | 2x 1mA | 3.3V | 6.6mW |
| Speaker + Amp | 500mA | 5V | 2.5W (peak) |
| 3x Cameras | 3x 250mA | 5V | 3.75W |
| Distance Sensor | 20mA | 3.3V | 66mW |
| **TOTAL** | **~1A** | **5V** | **~6.3W** |

**Note:** Peak when all cameras active + speaker at max volume.
Normal operation: ~4W

---

## 3D PRINT SPECIFICATIONS

### Head Shell Design

**Material:** PETG (durable, heat resistant)
**Infill:** 20% (structural), 100% (mounting points)
**Walls:** 3 perimeters

**Sections:**
1. **Front Face** - Removable for access
2. **Side Panels** - Temples with camera windows
3. **Top Dome** - Brain cavity
4. **Neck Joint** - Rotation mechanism

**Features:**
- Snap-fit mounting for all sensors
- Cable management channels (15mm diameter)
- Ventilation holes (brain cooling)
- Water-resistant sealing (outdoor use)
- Quick-release latches (maintenance)

---

## SOFTWARE INTEGRATION

### Sensor Fusion

```python
class HeadSensors:
    def __init__(self):
        self.mics = StereoMics()
        self.speaker = Speaker()
        self.cameras = MultiCamera()
        self.distance = DistanceSensor()
    
    def perceive(self):
        return {
            "audio": self.mics.listen(),
            "vision": self.cameras.capture(),
            "depth": self.distance.read(),
            "direction": self.mics.localization(),
        }
```

### Audio Processing

```python
# Voice Activity Detection
if mic_level > threshold:
    command = speech_to_text(audio)
    brain.process(command)

# Sound Localization
angle = calculate_angle(left_mic, right_mic)
head.turn_to(angle)
```

### Visual Processing

```python
# Stereoscopic depth
depth_map = stereo_depth(left_cam, right_cam)
obstacles = detect_obstacles(depth_map)

# Panoramic stitching
panorama = stitch(cam_center, cam_left, cam_right)
```

---

## TESTING CHECKLIST

### Audio Tests
- [ ] Both microphones record
- [ ] Stereo separation works
- [ ] Speaker plays TTS
- [ ] Volume control responsive
- [ ] Sound localization accurate

### Vision Tests
- [ ] All 3 cameras capture
- [ ] Stereoscopic depth works
- [ ] Object detection runs
- [ ] Panoramic stitching works
- [ ] Low-light performance

### Distance Tests
- [ ] Sensor reads accurately
- [ ] Range 5cm - 3m tested
- [ ] Response time < 50ms
- [ ] False positive rate low

---

## COST BREAKDOWN (Head Sensors)

| Component | Cost | Source |
|-----------|------|--------|
| 2x MEMS Mics | $10 | Adafruit |
| Speaker + Amp | $8 | Amazon |
| 3x Pi Cameras | $105 | Raspberry Pi |
| CSI Hub | $15 | Adafruit |
| VL53L5CX | $15 | SparkFun |
| Cables/etc | $10 | Various |
| **TOTAL** | **$163** | |

**Alternative (Budget):**
| Component | Cost |
|-----------|------|
| 2x Basic Mics | $6 |
| Speaker | $5 |
| 1x Pi Camera | $35 |
| HC-SR04 | $3 |
| **TOTAL** | **$49** |

---

**Document Version:** 1.0  
**Last Updated:** 2026-03-29 03:43 UTC  
**Next Review:** After prototype testing
