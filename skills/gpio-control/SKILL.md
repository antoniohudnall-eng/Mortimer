---
name: gpio-control
version: "1.0.0"
tier: standard
description: "General Purpose Input/Output control for sensors, LEDs, and switches. Complements BCSA V4 actuator control. Manages digital pins, PWM outputs, and analog sensors for complete hardware interface."
contracts:
  input:
    type: object
    properties:
      action:
        type: string
        enum: [write, read, set_expression, read_temp, check_stops, map, stats]
      pin:
        type: integer
      value:
        type: number
      mode:
        type: string
        enum: [digital, analog, pwm]
      expression:
        type: string
        enum: [neutral, happy, sad, surprised, alert]
      location:
        type: string
        enum: [core, right_arm, left_arm]
  output:
    type: object
    required: [success]
    properties:
      success:
        type: boolean
      value:
        type: number
      pin_map:
        type: object
      emergency_stops:
        type: object
---

# GPIO Control Skill

## Different from BCSA V4

While **BCSA V4** controls high-torque actuators (motors, joints), **GPIO** handles low-level digital/analog signals:

| System | Controls | Protocol | Use Case |
|--------|----------|----------|----------|
| **BCSA V4** | Motors, joints | Binary packets | Movement |
| **GPIO** | Sensors, LEDs | Digital/PWM/Analog | Sensing, expression |

## Pin Configuration (AOS-H1)

### Digital Outputs (0-3)
- Status LEDs on head, torso, arms

### Digital Inputs (4-7)
- Emergency stop switches (distributed)

### PWM Outputs (16-19)
- Eye brightness (left/right)
- Expression LEDs (eyebrows)

### Analog Inputs (24-29)
- Temperature sensors (core, arms)
- Pressure sensors (hands)
- Proximity sensor (head)

## Usage

```python
# Set facial expression
registry.call('gpio-control', {
    'action': 'set_expression',
    'expression': 'happy',
    'intensity': 0.8
})

# Read temperature
result = registry.call('gpio-control', {
    'action': 'read_temp',
    'location': 'core'
})
# Returns: {'temperature': 45.2, 'success': True}

# Check emergency stops
result = registry.call('gpio-control', {
    'action': 'check_stops'
})
# Returns: {'emergency_stops': {...}, 'any_pressed': False}
```

## Integration with BHSI

Agents control BOTH:
- **BCSA V4** → Body movement (via Body Hardware System Interface)
- **GPIO** → Sensing and expression (via this skill)

Complete embodiment requires both systems.
