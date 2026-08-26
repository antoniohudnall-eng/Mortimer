# Interaction System Blueprint

A modular, raycast-based interaction system for player-to-world interactions.

## Overview

This pattern creates a reusable interaction system where the player can look at and interact with objects in the world. Uses interfaces for maximum flexibility.

## Files

- `BP_InteractionInterface` (Blueprint Interface)
- `BP_InteractionComponent` (Actor Component)
- `BP_InteractableBase` (Parent Actor)
- `BP_PlayerCharacter` (Implementation)

---

## BP_InteractionInterface

**Type:** Blueprint Interface

### Functions

#### Interact
- **Inputs:** InteractingActor (Actor)
- **Outputs:** None
- **Description:** Called when player activates interaction

#### CanInteract
- **Inputs:** InteractingActor (Actor)
- **Outputs:** Boolean
- **Description:** Check if interaction is currently possible

#### GetInteractionPrompt
- **Inputs:** None
- **Outputs:** String
- **Description:** Returns UI text for interaction hint

#### OnBeginFocus
- **Inputs:** None
- **Outputs:** None
- **Description:** Called when player looks at interactable

#### OnEndFocus
- **Inputs:** None
- **Outputs:** None
- **Description:** Called when player looks away

---

## BP_InteractionComponent

**Type:** Actor Component  
**Attaches to:** Player Character

### Variables

| Name | Type | Default | Description |
|------|------|---------|-------------|
| InteractionDistance | Float | 300.0 | Max interaction range |
| InteractionCheckRate | Float | 0.1 | Seconds between checks |
| InteractionChannel | ECollisionChannel | Visibility | Trace channel |
| CurrentInteractable | Interface | None | Currently focused object |

### Event Graph

#### Event BeginPlay
```
[Event BeginPlay]
    │
    └──► [Set Timer by Function Name]
         ├── Function Name: "CheckForInteraction"
         ├── Time: InteractionCheckRate
         ├── Looping: True
         └── Initial Start Delay: 0.0
```

#### CheckForInteraction (Custom Event)
```
[Line Trace by Channel]
    ├── Start: [Get World Location] of Camera
    ├── End: Start + [Get Forward Vector] * InteractionDistance
    ├── Draw Debug Type: None
    └── Channel: Visibility
    │
    ├──► [Hit] ──► [Get Hit Actor]
    │                   │
    │                   └──► [Does Implement Interface: BPI_Interactable]
    │                           │
    │                           ├──► [True] ──► Compare with CurrentInteractable
    │                           │                    │
    │                           │                    ├──► [Different] ──► [Call OnEndFocus on old]
    │                           │                    │                       [Set CurrentInteractable]
    │                           │                    │                       [Call OnBeginFocus on new]
    │                           │                    │
    │                           │                    └──► [Same] ──► [Do nothing]
    │                           │
    │                           └──► [False] ──► [CurrentInteractable != None?]
    │                                                   │
    │                                                   └──► [True] ──► [Call OnEndFocus]
    │                                                                           [Set CurrentInteractable: None]
    │
    └──► [No Hit] ──► [Same as False path above]
```

#### PerformInteraction (Custom Event, BlueprintCallable)
```
[Is Valid] CurrentInteractable
    │
    └──► [True] ──► [CurrentInteractable: CanInteract]
                         │
                         └──► [True] ──► [CurrentInteractable: Interact]
                                               └── [Get Owner] as InteractingActor
```

---

## BP_InteractableBase

**Type:** Actor (Abstract parent)  
**Implements:** BPI_InteractionInterface

### Components

- DefaultSceneRoot (Scene)
- StaticMesh (Static Mesh, optional)
- InteractionWidget (Widget Component, optional)

### Variables

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bCanInteract | Boolean | True | Toggle interaction state |
| InteractionText | String | "Interact" | Prompt text |
| bShowPromptWidget | Boolean | True | Show floating UI |

### Interface Implementation

#### Interact
```
[Input: InteractingActor]
    │
    └──► [Event Interact] ──► [BlueprintImplementableEvent: OnInteracted]
                                 └── [Call OnInteracted]
```

#### CanInteract
```
[Return Node] ──► [AND]
                     ├── [bCanInteract]
                     └── [Custom logic if needed]
```

#### GetInteractionPrompt
```
[Return Node] ──► [InteractionText]
```

#### OnBeginFocus
```
[Event OnBeginFocus]
    │
    ├──► [Set Visibility] InteractionWidget: Visible
    └──► [Set Render Custom Depth] StaticMesh: True
         [Set Custom Depth Stencil Value]: 1
```

#### OnEndFocus
```
[Event OnEndFocus]
    │
    ├──► [Set Visibility] InteractionWidget: Hidden
    └──► [Set Render Custom Depth] StaticMesh: False
```

---

## BP_ExampleDoor (Child of BP_InteractableBase)

**Type:** Actor

### Additional Variables

| Name | Type | Default |
|------|------|---------|
| bIsOpen | Boolean | False |
| OpenRotation | Rotator | (0, 90, 0) |
| ClosedRotation | Rotator | (0, 0, 0) |
| AnimationTime | Float | 1.0 |

### OnInteracted (Override)
```
[OnInteracted Event]
    │
    └──► [FlipFlop]
              ├──► [A] ──► [Timeline: OpenDoor]
              │              ├──► [Play from Start]
              │              └──► [OnUpdate] ──► [Lerp Rotator]
              │                                     ├── A: Current Rotation
              │                                     ├── B: OpenRotation
              │                                     └── Alpha: Timeline Output
              │
              └──► [B] ──► [Timeline: CloseDoor]
                             └──► [Same pattern with ClosedRotation]
```

---

## BP_PlayerCharacter Integration

### Input Mapping

**Input Action: IA_Interact**
- Trigger: Pressed
- Key: E (Keyboard)

### Event Graph

#### Interact Input
```
[Enhanced Input Action: IA_Interact]
    │
    └──► [Get Interaction Component]
              │
              └──► [PerformInteraction]
```

#### Tick (UI Update)
```
[Event Tick]
    │
    └──► [Get Interaction Component]
              │
              ├──► [Get CurrentInteractable]
              │         │
              │         ├──► [Valid] ──► [GetInteractionPrompt]
              │         │                     │
              │         │                     └──► [Update HUD Widget]
              │         │
              │         └──► [Invalid] ──► [Hide Interaction Widget]
              │
              └──► [Draw Debug Line] (optional, for debugging)
```

---

## Usage

1. Create child Blueprints of `BP_InteractableBase`
2. Override `OnInteracted` event for custom behavior
3. Place in level
4. Player looks at object (focus events fire)
5. Player presses Interact key
6. `Interact` function executes on target

## Extensions

- **Multiplayer:** Add RPC calls in `Interact` function
- **Holding:** Change to Press-and-Hold with progress bar
- **Inventory Check:** Verify items before interaction
- **Quest Integration:** Fire quest events on interaction
- **Animation:** Play character interaction montage
