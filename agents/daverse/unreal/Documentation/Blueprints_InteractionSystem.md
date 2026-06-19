# Interaction System Blueprint Documentation

## BPI_Interactable (Interface)

### Interface Functions
```
Function: GetInteractionText
    ├── Inputs: Actor InteractingActor
    └── Outputs: Text InteractionText

Function: CanInteract
    ├── Inputs: Actor InteractingActor
    └── Outputs: bool bCanInteract

Function: Interact
    ├── Inputs: Actor InteractingActor
    └── Outputs: None

Function: OnHoverStart
    ├── Inputs: Actor InteractingActor
    └── Outputs: None

Function: OnHoverEnd
    ├── Inputs: Actor InteractingActor
    └── Outputs: None
```

## BP_InteractableBase (Actor)

### Components
```
Static Mesh Component (Root)
└── InteractableMesh

Box Component
└── InteractionZone
    ├── Extent: (100, 100, 100)
    └── Collision: Overlap All Dynamic

Widget Component
└── InteractionPrompt
    ├── Widget Class: W_InteractionPrompt
    ├── Draw Size: (200, 100)
    └── Space: Screen
```

### Variables
```
| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| InteractionText | Text | "Interact" | Display text |
| bRequireLineOfSight | bool | true | Must see to interact |
| InteractionDistance | float | 200.0 | Max distance |
| InteractionTime | float | 0.0 | Hold time (0 = instant) |
| bOneTimeUse | bool | false | Destroy after use |
| CooldownTime | float | 0.0 | Seconds before re-use |
| bIsOnCooldown | bool | false | Current state |
```

### Event Graph

```
BeginPlay
    ├── Set Widget Component Visible: False
    ├── Set Widget Text to InteractionText
    └── Bind to Interaction Zone Events

Event OnBeginOverlap (InteractionZone)
    ├── Other Actor = Player
    ├── Cast to BP_PlayerCharacter
    ├── Register Interactable (add to player's list)
    └── If bRequireLineOfSight: Start Line Trace

Event OnEndOverlap (InteractionZone)
    ├── Cast to BP_PlayerCharacter
    ├── Unregister Interactable
    └── Call OnHoverEnd

Interface Implementation: CanInteract
    ├── If bIsOnCooldown: Return False
    ├── If bRequireLineOfSight: Check Trace
    └── Return True

Interface Implementation: Interact
    ├── If NOT CanInteract: Return
    ├── If InteractionTime > 0:
    │   └── Start Hold Interaction
    ├── Else:
    │   ├── Call PerformInteraction
    │   ├── If bOneTimeUse: Destroy Self
    │   └── If CooldownTime > 0: Start Cooldown

Custom Event: PerformInteraction
    ├── Override in child classes
    ├── Default: Print "Interacted!"
    └── Play Sound/Animation

Function: StartCooldown
    ├── Set bIsOnCooldown = True
    ├── Delay: CooldownTime
    └── Set bIsOnCooldown = False
```

## BP_Door_Interactable (Child)

### Additional Variables
```
| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| DoorState | EDoorState | Closed | Current state |
| OpenRotation | Rotator | (0, 90, 0) | Target open rotation |
| ClosedRotation | Rotator | (0, 0, 0) | Target closed rotation |
| OpenSpeed | float | 2.0 | Interp speed |
| bIsLocked | bool | false | Requires key |
| RequiredKeyItem | TSubclassOf | None | Key class needed |
```

### Event Graph

```
Interface: Interact
    ├── If bIsLocked:
    │   └── Call AttemptUnlock
    ├── Else:
    │   └── Call ToggleDoor

Function: AttemptUnlock
    ├── Get Player Inventory
    ├── Check for RequiredKeyItem
    ├── If Has Key:
    │   ├── Consume Key (optional)
    │   ├── Set bIsLocked = False
    │   ├── Play Unlock Sound/Animation
    │   └── Call ToggleDoor
    └── Else:
        └── Show "Locked" message

Function: ToggleDoor
    ├── Switch on DoorState
    │   ├── Closed → Open
    │   │   ├── Set Target Rotation = OpenRotation
    │   │   ├── Set DoorState = Opening
    │   │   └── Start Door Timeline
    │   ├── Open → Close
    │   │   ├── Set Target Rotation = ClosedRotation
    │   │   ├── Set DoorState = Closing
    │   │   └── Start Door Timeline
    └── Play Door Sound (Open/Close)

Timeline: DoorMovement
    ├── Float Track: 0-1 (1 sec)
    ├── Update:
    │   ├── Get Current Rotation
    │   ├── Interp to Target Rotation
    │   └── Set Actor Rotation
    └── Finished:
        ├── Set DoorState = Open/Closed
        └── Stop Timeline
```

## BP_LootChest (Child)

### Variables
```
| Variable | Type | Description |
|----------|------|-------------|
| LootTable | DataTable | Possible items |
| MinItems | int | Minimum drops |
| MaxItems | int | Maximum drops |
| bIsOpen | bool | State tracking |
| SpawnedItems | Array | References to spawned loot |
```

### Event Graph

```
Interface: Interact
    ├── If bIsOpen: Return (already open)
    ├── Play Open Animation
    ├── Set bIsOpen = True
    ├── Call GenerateLoot
    └── Call SpawnLoot

Function: GenerateLoot
    ├── Clear SpawnedItems array
    ├── Random int: ItemCount = Random Range(MinItems, MaxItems)
    ├── Loop ItemCount times:
    │   ├── Random Row from LootTable
    │   ├── Add to SpawnedItems
    └── Return SpawnedItems

Function: SpawnLoot
    ├── For Each Item in SpawnedItems:
    │   ├── Spawn Actor: Item Class
    │   ├── Set Location: ChestLocation + Offset
    │   ├── Set Physics: Simulate
    │   ├── Apply Impulse (up/out)
    │   └── Delay: 0.1s (stagger spawns)
    └── Play Loot Spawn Sound
```

## BP_InteractionComponent (Actor Component)

### Purpose
Attach to player character for detection logic

### Variables
```
| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| InteractionRange | float | 300.0 | Trace distance |
| InteractionRadius | float | 50.0 | Sphere trace size |
| CurrentInteractable | Actor | None | Focus target |
| CachedInteractables | Array | Empty | In-range actors |
```

### Event Graph

```
Event Tick
    ├── Call UpdateInteraction

Function: UpdateInteraction
    ├── Sphere Trace from Camera
    ├── Filter by Interface (BPI_Interactable)
    ├── Sort by Distance
    ├── If New Target ≠ CurrentInteractable:
    │   ├── Call OnHoverEnd on Current
    │   ├── Set CurrentInteractable = New Target
    │   └── Call OnHoverStart on New
    └── Update UI Prompt

Event OnInput_Interact
    ├── If CurrentInteractable is Valid:
    │   └── Call Interface: Interact
    └── Play Interaction Attempt Sound (if fail)
```

## BP_DialogueNPC (Child)

### Variables
```
| Variable | Type | Description |
|----------|------|-------------|
| DialogueTree | UDialogueTreeAsset | Conversation data |
| NPCName | String | Display name |
| Portrait | Texture2D | UI image |
| bHasQuest | bool | Offers quest |
| QuestID | String | Quest identifier |
```

### Event Graph

```
Interface: Interact
    ├── Stop Player Movement
    ├── Open Dialogue UI
    │   ├── Create Widget: W_Dialogue
    │   ├── Set NPC Name/Portrait
    │   ├── Load Dialogue Tree
    │   └── Show First Node
    └── Lock Input to UI Mode

Custom Event: OnDialogueEnd
    ├── Close Dialogue Widget
    ├── Resume Player Movement
    ├── Return Input to Game
    └── If Quest Accepted: Add to Quest Log
```

## Data Structures

### FInteractionData (Struct)
```
USTRUCT()
struct FInteractionData {
    UPROPERTY()
    FText DisplayText;
    
    UPROPERTY()
    UTexture2D* Icon;
    
    UPROPERTY()
    FLinearColor IconColor;
    
    UPROPERTY()
    float HoldDuration;
    
    UPROPERTY()
    bool bShowProgressBar;
};
```

### EInteractionType (Enum)
```
UENUM()
enum class EInteractionType {
    Instant,      // Press button
    Hold,         // Hold button
    Charge,       // Hold with progress
    Toggle,       // On/Off state
    Sequence,     // Multiple steps
    Combo         // Button combination
};
```
