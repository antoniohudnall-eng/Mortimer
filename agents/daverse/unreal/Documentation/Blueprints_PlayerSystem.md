# Blueprint Player System Documentation

## BP_PlayerCharacter (Main Character)

### Components Hierarchy
```
BP_PlayerCharacter (Character)
├── CapsuleComponent (Root)
├── Mesh (SkeletalMeshComponent)
│   └── WeaponAttachPoint (SceneComponent)
├── SpringArmComponent (Camera boom)
│   └── Camera (CameraComponent)
├── InteractionComponent (SphereComponent)
└── PlayerDataComponent (ActorComponent)
```

### Variables

#### Movement Variables
| Name | Type | Default | Description |
|------|------|---------|-------------|
| WalkSpeed | float | 450.0 | Base walking speed |
| SprintSpeed | float | 750.0 | Sprint speed multiplier |
| CrouchSpeed | float | 250.0 | Crouch movement speed |
| TurnRate | float | 45.0 | Mouse/gamepad turn rate |
| JumpHeight | float | 600.0 | Z velocity on jump |
| AirControl | float | 0.5 | Air control multiplier |

#### Camera Variables
| Name | Type | Default | Description |
|------|------|---------|-------------|
| BaseFOV | float | 90.0 | Field of view |
| AimFOV | float | 70.0 | ADS field of view |
| CameraLagSpeed | float | 10.0 | Spring arm lag |
| CameraBoomLength | float | 300.0 | Third-person distance |
| CameraOffset | FVector | (0,0,50) | Height offset |

#### Input Actions (Enhanced Input)
```
IA_Move (Vector2D)          - WASD/Left Stick
IA_Look (Vector2D)            - Mouse/Right Stick
IA_Jump (Action)              - Space/A
IA_Sprint (Action)            - Shift/L3
IA_Crouch (Action)            - C/B
IA_Interact (Action)          - F/X
IA_Attack (Action)            - LMB/RT
IA_Aim (Action)               - RMB/LT
IA_Pause (Action)             - Esc/Menu
```

### Event Graph: Movement System

```
Event Tick
    └── UpdateCamera
        ├── Get Movement Direction
        ├── Calculate Camera Lag
        └── Apply to SpringArm

Event OnMovementModeChanged
    ├── If Falling: Set AirControl
    ├── If Walking: Reset AirControl
    └── If Swimming: Enable Swimming State

Custom Event: Sprint
    ├── InputAction Sprint (Pressed)
    │   └── Set MaxWalkSpeed = SprintSpeed
    └── InputAction Sprint (Released)
        └── Set MaxWalkSpeed = WalkSpeed

Custom Event: Crouch
    ├── InputAction Crouch (Pressed)
    │   ├── Crouch()
    │   └── Set MaxWalkSpeed = CrouchSpeed
    └── InputAction Crouch (Released)
        ├── UnCrouch()
        └── Set MaxWalkSpeed = WalkSpeed
```

### Event Graph: Camera System

```
Custom Event: UpdateCamera
    ├── Get Control Rotation
    ├── Calculate Desired Rotation
    ├── Interp to Target Rotation
    └── Apply to SpringArm

Custom Event: Aim
    ├── InputAction Aim (Pressed)
    │   ├── Set Camera FOV = AimFOV
    │   ├── Set SpringArm Length = AimBoomLength
    │   └── Enable ADS State
    └── InputAction Aim (Released)
        ├── Set Camera FOV = BaseFOV
        ├── Set SpringArm Length = CameraBoomLength
        └── Disable ADS State
```

### Event Graph: Interaction System

```
BeginPlay
    └── Create Interaction Widget
        ├── Set Visibility: Hidden
        └── Store Reference

Event Tick (Interaction Check)
    ├── Sphere Trace from Camera
    ├── If Hit: Check for Interface (BPI_Interactable)
    ├── If Valid: Show Interaction Widget
    └── Update Widget with Interaction Text

Custom Event: Interact
    ├── InputAction Interact (Pressed)
    ├── Get Hit Actor from Trace
    ├── Call Interface Function: Interact
    └── Play Interaction Animation
```

## BP_PlayerController

### Purpose
- Handles player input
- Manages UI states
- Coordinates game mode transitions

### Key Functions

```
Function: ShowPauseMenu
    ├── Create Widget (W_PauseMenu)
    ├── Add to Viewport
    ├── Set Input Mode: UI Only
    └── Set Game Paused: True

Function: HidePauseMenu
    ├── Remove from Parent
    ├── Set Input Mode: Game Only
    └── Set Game Paused: False

Function: ChangeMap
    ├── Input: MapName (String)
    ├── Open Level (MapName)
    └── Delay (travel time)
```

## BP_GameMode_DaVerse

### Class Settings
```
Default Pawn Class: BP_PlayerCharacter
Player Controller Class: BP_PlayerController
HUD Class: BP_HUD_DaVerse
Game State: BP_GameState_DaVerse
Player State: BP_PlayerState_DaVerse
```

### Game Flow

```
Event OnPostLogin
    ├── Spawn Player
    ├── Initialize Player Data
    └── Broadcast: Player Joined

Event OnLogout
    ├── Save Player Data
    ├── Broadcast: Player Left
    └── Handle Spectator

Function: StartGame
    ├── Set Game State: InProgress
    ├── Enable Player Input
    └── Start Game Timer

Function: EndGame
    ├── Set Game State: Finished
    ├── Disable Player Input
    ├── Show Results Screen
    └── Delay (10s) → Return to Lobby
```

## Animation Blueprint: ABP_PlayerCharacter

### State Machine

```
[Entry]
    └── Locomotion
        ├── Idle/Walk/Run Blendspace (Speed, Direction)
        ├── Jump Start (Notify: Play Sound)
        ├── Jump Loop
        ├── Jump End
        ├── Crouch Idle/Walk Blendspace
        └── Swim

[Interaction Layer]
    └── Interact States
        ├── Interact
        ├── Pickup
        └── Open

[Combat Layer]
    └── Combat States
        ├── Idle Combat
        ├── Aim
        ├── Fire
        └── Reload
```

### Animation Blueprint Variables

| Name | Type | Description |
|------|------|-------------|
| Speed | float | Movement speed magnitude |
| Direction | float | Movement direction (-180 to 180) |
| IsInAir | bool | Is character jumping/falling |
| IsCrouching | bool | Is character crouched |
| IsAiming | bool | Is ADS active |
| IsInteracting | bool | Is interaction playing |

### Blendspace Setup

#### BS_IdleWalkRun
```
Horizontal Axis: Direction (-180 to 180)
Vertical Axis: Speed (0 to 750)

Points:
- (0, 0): Idle
- (0, 450): Walk_Fwd
- (0, 750): Run_Fwd
- (-90, 450): Walk_Left
- (90, 450): Walk_Right
- (180, 450): Walk_Back
```
