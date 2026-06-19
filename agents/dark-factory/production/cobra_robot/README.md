# 🐍 COBRA Robot

**COordinated Biomimetic Robotic Architecture**

A complete snake-spine humanoid robot with integrated power systems and tendon-driven hands.

![COBRA Concept](docs/images/cobra_concept.png)

---

## Features

- **25-Vertebra Snake Spine:** Mimics human spinal column with 2-DOF per joint
- **Distributed Batteries:** 17 Li-ion cells housed within vertebrae
- **Solar Charging:** Integrated panels on thoracic vertebrae
- **Tendon Hands:** Dyneema fishing line actuation, 60% lighter than servo hands
- **Three Sizes:** MINI (30cm), MIDI (90cm), MAX (175cm)

---

## Quick Start

```bash
# Generate STL files
cd src
python3 stl_generator.py

# Run simulation demo
python3 cobra_robot.py
```

---

## Repository Structure

```
cobra_robot/
├── src/
│   ├── cobra_robot.py      # Main control software
│   ├── stl_generator.py     # OpenSCAD file generator
│   └── firmware/            # STM32 vertebra firmware
├── stls/
│   ├── mini/               # 61 files for mini model
│   ├── midi/               # 61 files for midi model
│   └── max/                # 61 files for max model
├── bom/
│   ├── BOM_MINI.md
│   ├── BOM_MIDI.md
│   └── BOM_MAX.md
├── docs/
│   ├── assembly_guide.md
│   ├── wiring_diagram.md
│   └── calibration.md
└── README.md
```

---

## Specifications

### COBRA-MIDI (1:2 Scale)

| Parameter | Value |
|-----------|-------|
| **Height** | 90cm |
| **Weight** | ~8kg |
| **Vertebrae** | 25 |
| **DOF** | 50 (spine) + 10 (hands) |
| **Battery** | 34× 18650 cells, 188.7Wh |
| **Solar** | 12 panels, 8W peak |
| **Runtime** | 16-24 hours active |
| **Materials** | PETG CF, Dyneema, aluminum |
| **Est. Cost** | $800 |

---

## Assembly

### Phase 1: Spine (Weeks 1-2)
1. Print all 25 vertebrae (40 hours)
2. Install batteries and BMS in T1-L5
3. Mount servos and gimbals
4. Wire CAN bus between vertebrae

### Phase 2: Hands (Week 3)
1. Print finger segments in TPU
2. Thread Dyneema through guides
3. Mount micro servos in palms
4. Calibrate tendon tension

### Phase 3: Integration (Week 4)
1. Mount brain (RPi5) in sacrum
2. Install solar panels on T5-T9
3. Connect power distribution
4. Flash firmware and calibrate

See [docs/assembly_guide.md](docs/assembly_guide.md) for detailed steps.

---

## Software

### Python Control
```python
from cobra_robot import CobraRobot

robot = CobraRobot(model_size="midi", name="COBRA-1")
robot.calibrate()

# Natural standing posture
robot.spine.natural_standing()

# Forward bend
robot.spine.forward_bend(30)

# Hand gestures
robot.right_hand.set_grip("fist")
robot.left_hand.set_grip("point")
```

### Firmware
Each vertebra runs an STM32F103 with:
- 2× servo control (PWM)
- CAN bus communication
- BMS monitoring
- IMU data collection

See `firmware/vertebra_node/` for source.

---

## Power Management

```
Solar Panels → MPPT → Vertebra Batteries → DC-DC → 5V/12V Rails
                    ↓
               BMS Monitoring (CAN bus)
```

- **Charging:** 8W solar @ full sun = 25h for full charge
- **Runtime:** 16-24h depending on activity
- **Emergency:** Sleep mode extends to 1 week

---

## Bill of Materials

See [bom/BOM_MIDI.md](bom/BOM_MIDI.md) for complete parts list.

**Quick Shopping:**
- 34× 18650 Li-ion cells ($170)
- 34× servos ($216)
- 25× STM32 nodes ($165)
- RPi5 + AI HAT ($150)
- 800g PETG CF filament ($36)

**Total: ~$800 USD**

---

## Design Philosophy

1. **Biomimicry:** Human-like spine enables natural movement
2. **Integration:** Batteries and solar are structural, not added
3. **Tendon Drive:** Motors at proximal end, light distal segments
4. **Modularity:** Print individual parts, replace as needed

---

## Roadmap

- [x] Design specification
- [x] STL file generation
- [x] Python control software
- [ ] STM32 firmware
- [ ] Assembly documentation
- [ ] Video build guide
- [ ] Community beta builds

---

## License

MIT License - See [LICENSE](LICENSE)

## Credits

- Design: Performance Supply Depot LLC
- Inspiration: Human anatomy, Shadow Robot Company
- Materials: DSM Dyneema, eSun PETG CF

---

**Status:** 🟢 Ready for prototyping

**Questions?** Open an issue or see [docs/](docs/)
