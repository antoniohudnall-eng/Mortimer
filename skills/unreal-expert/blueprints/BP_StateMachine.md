# State Machine Blueprint

A robust, enum-based finite state machine (FSM) for character AI, player states, game flow, and any sequential logic.

## Overview

Uses Enums to define states, with enter/exit/update hooks for each state. Supports transitions, state history, and event handling. Can be extended for AI behaviors, player movement modes, UI flows, or game state management.

## Files

- `E_ExampleState` (Enum) - Define your states
- `BP_StateMachineComponent` (Actor Component) - Reusable FSM engine
- `BP_StateMachineInterface` (Blueprint Interface) - Optional callbacks
- `BP_ExampleAIController` (Implementation)

---

## E_ExampleState (Enum)

**Use Case: AI Enemy States**

```
Idle            // Waiting for player
Patrol          // Following waypoint path
Alert           // Heard something, investigating
Chase           // Spotted player, pursuing
Attack          // In range, attacking
Stunned         // Hit by player, temporarily disabled
Dead            // Defeated
```

**Use Case: Player Movement States**

```
Idle
Walking
Sprinting
Crouching
Jumping
Falling
Landed
Swimming
Flying
Dead
```

---

## BP_StateMachineComponent

**Type:** Actor Component  
**Replication:** Replicated

### Variables

| Name | Type | Default | Description |
|------|------|---------|-------------|
| CurrentState | Enum | First value | Active state |
| PreviousState | Enum | None | For state revert |
| bCanChangeState | Boolean | true | Lock during transitions |
| bLogStateChanges | Boolean | false | Debug logging |
| StateData | Map(Enum, Struct) | Empty | Per-state config |

### Event Dispatchers

| Name | Inputs | Description |
|------|--------|-------------|
| OnStateEntered | NewState, OldState | Fires after entering state |
| OnStateExited | OldState, NewState | Fires before leaving state |
| OnStateUpdate | CurrentState, DeltaTime | Fires every tick |
| OnStateChanged | NewState, OldState | Wrapper for enter/exit |

### Core Functions

#### Initialize State Machine

```
[Event Initialize] (Input: StartingState)
    │
    ├──► [Set CurrentState = StartingState]
    │
    ├──► [Call State Enter]
    │       └── [State_Enter: StartingState]
    │
    └──► [Start Update Loop]
             └── [Event Tick] ──► [State_Update: CurrentState]
```

#### Change State

```
[Event ChangeState] (Input: NewState)
    │
    ├──► [Branch: NewState == CurrentState] ──► [True] ──► [Return: false]
    │
    ├──► [Branch: !bCanChangeState] ──► [True] ──► [Return: false]
    │
    ├──► [CanTransitionFrom: CurrentState → NewState?]
    │       └──► [False] ──► [Return: false]
    │
    ├──► [Store PreviousState]
    │       └── [PreviousState = CurrentState]
    │
    ├──► [Call State Exit]
    │       ├── [Broadcast OnStateExited]
    │       └── [State_Exit: CurrentState]
    │
    ├──► [Set CurrentState = NewState]
    │
    ├──► [Call State Enter]
    │       ├── [State_Enter: NewState]
    │       └── [Broadcast OnStateEntered]
    │
    ├──► [Broadcast OnStateChanged]
    │
    ├──► [If bLogStateChanges] ──► [Print: "State: {Old} → {New}"]
    │
    └──► [Return: true]
```

#### Revert to Previous State

```
[Event RevertState]
    │
    └──► [ChangeState: PreviousState]
```

#### State Enter (Dynamic)

```
[Event State_Enter] (Input: State)
    │
    └──► [Switch on Enum: State]
            ├──► [Idle] ──► [Start Idle Animation]
            │               [Reset Detection Timer]
            │
            ├──► [Patrol] ──► [Get Next Waypoint]
            │                 [Move To Actor]
            │
            ├──► [Alert] ──► [Stop Movement]
            │                [Play Alert Animation]
            │                [Set Timer: CheckForThreat]
            │
            ├──► [Chase] ──► [Set Movement Speed: Sprint]
            │                [Set Focus: Player]
            │                [Start Chase Music]
            │
            ├──► [Attack] ──► [Stop Movement]
            │                 [Start Attack Cooldown]
            │                 [Begin Attack Sequence]
            │
            ├──► [Stunned] ──► [Stop All Actions]
            │                  [Play Hit Reaction]
            │                  [Set Timer: Recover]
            │
            └──► [Dead] ──► [Ragdoll Physics]
                            [Drop Loot]
                            [Disable Collision]
                            [Destroy: 10 seconds]
```

#### State Exit (Dynamic)

```
[Event State_Exit] (Input: State)
    │
    └──► [Switch on Enum: State]
            ├──► [Idle] ──► [Clear Timer: IdleChecks]
            │
            ├──► [Patrol] ──► [Clear Waypoint Target]
            │
            ├──► [Alert] ──► [Clear Search Timer]
            │
            ├──► [Chase] ──► [Clear Focus]
            │                [Reset Speed]
            │
            ├──► [Attack] ──► [Stop Attack Montage]
            │                 [Clear Combo Counter]
            │
            └──► [Stunned] ──► [Clear Recovery Timer]
```

#### State Update (Dynamic, Event Tick)

```
[Event State_Update] (Inputs: State, DeltaTime)
    │
    └──► [Switch on Enum: State]
            ├──► [Idle] ──► [CheckForPlayerInRange]
            │               [If detected] ──► [ChangeState: Alert]
            │
            ├──► [Patrol] ──► [If Reached Waypoint]
            │                   [Get Next Waypoint]
            │                   [If Player Detected]
            │                   [ChangeState: Chase]
            │
            ├──► [Alert] ──► [Move Towards Sound Source]
            │                [If Player Visible]
            │                [ChangeState: Chase]
            │                [If Timer Expired]
            │                [ChangeState: Patrol]
            │
            ├──► [Chase] ──► [Update Path to Player]
            │                [If Lost Line of Sight]
            │                [Set Timer: AlertBeforeGiveUp]
            │                [If In Attack Range]
            │                [ChangeState: Attack]
            │
            ├──► [Attack] ──► [Face Player]
            │                 [If Player Moved Out of Range]
            │                 [ChangeState: Chase]
            │
            ├──► [Stunned] ──► [Stun Timer Countdown]
            │
            └──► [Dead] ──► [Do Nothing]
```

---

## State Configuration Structure

### S_StateConfig (Structure)

| Variable | Type | Description |
|----------|------|-------------|
| bCanBeInterrupted | Boolean | Can force change out of this state |
| MaxDuration | Float | 0 = infinite, auto-exit after time |
| NextAutoState | Enum | Transition to this when duration expires |
| AnimationState | EAnimState | Animation graph parameter |
| MovementSpeed | Float | Override character speed |
| AllowedTransitions | Array(Enum) | Which states can we enter from here |

---

## BP_ExampleAIController Implementation

### Components

- AIController (Base)
- StateMachineComponent
- AIPerception (Sight, Hearing)
- PawnSensing (Optional backup)
- HealthComponent

### Variables

| Name | Type | Description |
|------|------|-------------|
| CurrentWaypoint | Actor | Patrol target |
| WaypointList | Array(Actor) | All patrol points |
| DetectionRange | Float | Distance to spot player |
| AttackRange | Float | Distance to start attacking |
| PlayerPawn | Actor | Cached player reference |

### AI Perception Setup

```
[On Perception Updated]
    │
    ├──► [Get Perceived Actors: By Sense: Sight]
    │       └──► [For Each]
    │               └──► [If Is Player]
    │                       └──► [Update PlayerPawn reference]
    │                       └──► [StateMachine: Can See Player = true]
    │
    └──► [On Lost Sight]
            └──► [StateMachine: Can See Player = false]
```

### State-Specific Logic

#### CheckForPlayerInRange (Custom)

```
[CheckForPlayerInRange]
    │
    ├──► [Get All Actors of Class: PlayerCharacter]
    │       └──► [For Each]
    │               └──► [Get Distance To]
    │                       └──► [If < DetectionRange]
    │                               └──► [Line of Sight Check]
    │                                       └──► [If Clear]
    │                                               └──► [Return: true]
    │
    └──► [Return: false]
```

#### UpdatePathToPlayer (Custom)

```
[UpdatePathToPlayer]
    │
    ├──► [Get Player Location]
    │
    ├──► [AI Move To]
    │       ├── Goal: Player Location
    │       ├── Acceptance Radius: AttackRange - 50
    │       └── Should Stop on Overlap: false
    │
    └──► [If Failed] ──► [ChangeState: Alert]
```

#### Begin Attack Sequence (Custom)

```
[BeginAttackSequence]
    │
    ├──► [Set Timer: PerformAttack]
    │       ├── Time: 0.3 (windup)
    │       └── Looping: false
    │
    └──► [Play Animation Montage: Attack]
```

#### Perform Attack (Custom)

```
[PerformAttack]
    │
    ├──► [Sphere Trace]
    │       ├── Location: Weapon Socket
    │       ├── Radius: Attack Hitbox
    │       └── [For Each Hit]
    │               └──► [Apply Damage]
    │
    ├──► [Set Timer: AttackCooldown]
    │       ├── Time: 1.5 seconds
    │       └── On Complete: ChangeState: Chase (if still in Attack)
    │
    └──► [Spawn VFX: Attack Swing]
```

---

## Player State Machine Example

**Use: Movement State Management**

### E_PlayerMovementState

```
Idle
Walking
Sprinting
Crouching
Jumping
Falling
Landing
Prone
Climbing
Mantling
```

### State Transitions

```
Transitions:

Idle → Walking:     [Input Axis > 0]
Idle → Sprinting:   [Shift + Input > 0]
Idle → Crouching:   [C Key]
Idle → Jumping:     [Space]
Idle → Prone:       [Ctrl + C]

Walking → Idle:     [Input Axis == 0]
Walking → Sprinting:[Shift Pressed]
Walking → Crouching:[C Key]
Walking → Jumping:  [Space]

Sprinting → Walking:[Shift Released]
Sprinting → Idle:   [Input Axis == 0]

Crouching → Idle:   [C Key AND Can Stand?]
Crouching → Walking:[C + Input > 0]
Crouching → Prone:  [Ctrl]

Jumping → Falling:  [Velocity Z < 0]

Falling → Landing:  [IsOnGround]

Landing → Idle:     [Landing Animation Complete]
```

### Implementation

```
[Player Input: Jump]
    │
    ├──► [Get Movement State Machine]
    │
    └──► [CanEnterState: Jumping?]
            ├──► [Check: Is On Ground?]
            ├──► [Check: Not Crouching?]
            ├──► [Check: Not Prone?]
            │
            └──► [True] ──► [ChangeState: Jumping]
                                   └── [Launch Character: JumpVelocity]
```

---

## Nested State Machines

For complex AI, use multiple state machines:

```
MovementStateMachine:
    Idle, Walk, Run, Crouch, Prone

CombatStateMachine:
    Passive, Aggressive, Defensive, Fleeing

BehaviorStateMachine:
    Patrol, Investigate, Combat, Search, Flee

// Movement is subordinate to Behavior
[Behavior: Patrol] ──► [Movement: Walk]
[Behavior: Combat] ──► [Movement: Run/Crouch]
```

---

## Hierarchical State Machine (HSM)

Parent states with child states:

```
Combat (Parent)
├── Melee
│   ├── Windup
│   ├── Active
│   └── Recovery
└── Ranged
    ├── Aiming
    └── Firing

Transitions:
Combat → Flee: Health < 20%
Melee → Ranged: Distance > MeleeRange
```

---

## Debug Visualization

```
[Event Draw Debug]
    │
    ├──► [If bDebugStateMachine]
    │       └──► [Draw Debug String Above Actor]
    │               └── Text: "State: {CurrentState}"
    │               └── Color: Based on state
    │
    └──► [For AI]
            └──► [Draw Debug Sphere: Detection Range]
            └──► [Draw Debug Sphere: Attack Range]
            └──► [Draw Debug Line To: Target]
```

---

## Best Practices

1. **Keep states atomic** - Each state does one thing well
2. **Validate transitions** - Not all states can go to all others
3. **Use events, not polling** - React to changes, don't constantly check
4. **Clean up on exit** - Timers, animations, effects
5. **Initialize on enter** - Set up everything fresh
6. **Handle interruption** - States can be force-changed
7. **Use state history** - For debugging and "undo" features

---

## Extensions

### State History Stack

```
[PushState] - Save current to stack, enter new
[PopState]  - Exit current, restore from stack
[SwapState] - Pop then push (atomic)
```

### State Blackboard

Data shared across states:
```
Blackboard:
    TargetActor
    LastKnownPosition
    AlertLevel
    TimeInState
    CustomData
```

### Visual State Editor

Create editor utility widget:
```
- Drag states as boxes
- Draw arrows for transitions
- Edit conditions on arrows
- Generate enum + switch code
```
