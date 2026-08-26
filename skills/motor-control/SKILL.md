---
name: motor-control
version: "1.0.0"
tier: methodology
description: "Brain-to-body interface for AOS-H1 robot using BCSA V4 actuators. Translates cerebellum motor commands to physical joint control with inverse kinematics."
contracts:
  input:
    type: object
    properties:
      action:
        type: string
        enum: [set_pose, set_joint, update, status]
      end_effector:
        type: string
        enum: [right_hand, left_hand, right_foot, left_foot]
      position:
        type: array
        items: {type: number}
        minItems: 3
        maxItems: 3
      joint:
        type: string
      joint_position:
        type: number
  output:
    type: object
    required: [success, body_state]
    properties:
      success:
        type: boolean
      commands:
        type: array
        description: "BCSA V4 actuator commands"
      body_state:
        type: object
        description: "Current joint states"
---

# Motor Control Skill

## Brain-to-Body Bridge

Translates high-level cognitive motor commands into precise actuator control for the AOS-H1 humanoid robot using BCSA V4 cycloidal drives.

## Capabilities

- **Inverse Kinematics**: Calculate joint angles for end-effector positions
- **Forward Kinematics**: Compute body position from joint angles
- **PD Control**: Smooth joint trajectory following
- **Safety Limits**: Enforce joint range limits
- **BCSA V4 Integration**: Native protocol support

## Joint Configuration (AOS-H1)

### Head (2 DOF)
- neck_pitch: ±30°
- neck_yaw: ±60°

### Arms (4 DOF each)
- shoulder_pitch: ±90°
- shoulder_roll: -30° to +120°
- elbow_pitch: 0° to -150°
- wrist_yaw: ±60°

### Legs (5 DOF each)
- hip_pitch: ±90°
- hip_roll: ±30°
- knee_pitch: 0° to -150°
- ankle_pitch: ±45°
- ankle_roll: ±30°

## Usage

```python
# Set hand position
result = registry.call('motor-control', {
    'action': 'set_pose',
    'end_effector': 'right_hand',
    'position': [0.3, -0.2, 0.1]  # x, y, z in meters
})

# Update and generate commands
result = registry.call('motor-control', {
    'action': 'update',
    'dt': 0.016
})

# BCSA V4 commands ready to send
commands = result['commands']
```

## Integration

Connects to BCSA V4 actuators via CAN bus:
- Baud rate: 1 Mbps
- Protocol: BCSA native
- Update rate: 60 Hz
- Torque control mode

## Safety

- Joint limits enforced in software
- Velocity limits prevent damage
- Emergency stop via brain command
- Position feedback for closed-loop control
