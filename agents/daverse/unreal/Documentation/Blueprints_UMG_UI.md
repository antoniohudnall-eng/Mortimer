# UMG (Unreal Motion Graphics) UI System

## UI Architecture

### Widget Hierarchy
```
Game UI Layer
├── W_MainHUD (Persistent)
│   ├── W_HealthBar
│   ├── W_StaminaBar
│   ├── W_Crosshair
│   ├── W_InteractionPrompt
│   └── W_Minimap
├── W_PauseMenu (Modal)
│   ├── W_SettingsPanel
│   ├── W_SaveLoadPanel
│   └── W_QuitConfirm
├── W_Inventory (Modal)
│   ├── W_InventoryGrid
│   ├── W_ItemTooltip
│   └── W_EquipmentSlots
└── W_Dialogue (Modal)
    ├── W_DialogueText
    └── W_ResponseOptions
```

## W_MainHUD (Heads-Up Display)

### Widget Layout
```
Canvas Panel (Root)
├── Safe Zone (Mobile-safe margins)
│   ├── Health Container (Bottom Left)
│   │   ├── Progress Bar (Health)
│   │   ├── Text Block (HP: 100/100)
│   │   └── Image (Icon)
│   ├── Stamina Container (Bottom Left, under Health)
│   │   ├── Progress Bar (Stamina)
│   │   └── Image (Icon)
│   ├── Crosshair (Center)
│   │   ├── Size Box (64x64)
│   │   └── Image (Crosshair texture)
│   ├── Interaction Prompt (Center, below Crosshair)
│   │   ├── Horizontal Box
│   │   │   ├── Image (Key icon)
│   │   │   └── Text Block ("[F] Interact")
│   │   └── Visibility: Hidden (default)
│   ├── Minimap (Top Right)
│   │   ├── Size Box (200x200)
│   │   ├── Image (Minimap render target)
│   │   └── Image (Player indicator)
│   └── Notifications (Top Center)
│       └── Vertical Box (for queued messages)
```

### Event Graph: Health Update

```
Event Construct
    └── Bind to Player Health Changed

Custom Event: UpdateHealth
    ├── Input: NewHealth (float), MaxHealth (float)
    ├── Calculate Percent = NewHealth / MaxHealth
    ├── Set Progress Bar Value = Percent
    ├── Set Text = "HP: " + Floor(NewHealth) + "/" + MaxHealth
    └── Play Animation: HealthFlash (if damage taken)
```

### Event Graph: Interaction Prompt

```
Custom Event: ShowInteractionPrompt
    ├── Input: ActionText (String)
    ├── Set Text Block: "[" + KeyName + "] " + ActionText
    ├── Set Visibility: Visible
    └── Play Animation: PromptFadeIn

Custom Event: HideInteractionPrompt
    ├── Play Animation: PromptFadeOut
    └── Set Visibility: Hidden
```

## W_PauseMenu

### Widget Layout
```
Canvas Panel (Root)
├── Background Blur (Full screen)
│   └── Blur Strength: 10
├── Main Panel (Center)
│   ├── Border (Rounded corners)
│   │   ├── Vertical Box
│   │   │   ├── Text Block: "PAUSED"
│   │   │   ├── Spacer
│   │   │   ├── Button: Resume
│   │   │   ├── Button: Settings
│   │   │   ├── Button: Save Game
│   │   │   ├── Button: Load Game
│   │   │   └── Button: Quit to Menu
│   │   └── Close Button (Top Right)
└── Safe Zone (for content)
```

### Button Styling

```
Button Style: MenuButton
├── Normal
│   ├── Background: Semi-transparent dark
│   └── Text: White
├── Hovered
│   ├── Background: Accent color (cyan)
│   └── Text: Black
├── Pressed
│   ├── Background: Darker accent
│   └── Text: Light gray
└── Font: Roboto Bold, 24pt
```

## W_Inventory

### Widget Layout
```
Canvas Panel (Root)
├── Background Dim (70% opacity black)
├── Main Panel (80% screen)
│   ├── Horizontal Box
│   │   ├── Left Panel (70%)
│   │   │   ├── Tabs (All, Weapons, Consumables, Quest)
│   │   │   ├── Uniform Grid Panel (Item Grid)
│   │   │   │   └── W_InventorySlot (repeated)
│   │   │   └── Weight Display (Bottom)
│   │   └── Right Panel (30%)
│   │       ├── Character Preview
│   │       ├── Equipment Slots
│   │       └── Item Details (W_ItemDetails)
└── Close Button (ESC handler)
```

### W_InventorySlot (Individual Slot)

```
Size Box (64x64)
└── Button
    ├── Image (Item Icon)
    ├── Text Block (Quantity, if >1)
    ├── Border (Rarity color)
    └── Tool Tip Widget: W_ItemTooltip
```

### Drag and Drop Setup

```
Inventory Slot: Detect Drag
    ├── If Has Item
    │   └── Create Drag Drop Operation
    │       ├── Drag Visual: W_ItemDragVisual
    │       ├── Payload: Item Data
    │       └── Default Drag Visual: true
    └── Return Drag Operation

Inventory Slot: On Drop
    ├── Get Drag Operation Payload
    ├── Source Slot = Payload.Source
    ├── Target Slot = Self
    ├── Swap Items (Source ↔ Target)
    └── Refresh Both Slots
```

## W_ItemTooltip

```
Border (Tooltip background)
└── Vertical Box
    ├── Text Block: Item Name (Gold, Bold)
    ├── Text Block: Item Type (Gray, Italic)
    ├── Separator
    ├── Text Block: Description
    ├── Spacer
    └── Text Block: Stats (Green if positive, Red if negative)
```

## UI Animations

### Health Bar Flash (UMG Animation)
```
Timeline: 0.0s - 0.5s
├── 0.0s: Color = White
├── 0.1s: Color = Red
├── 0.25s: Color = Red
└── 0.5s: Color = White
```

### Menu Fade In
```
Timeline: 0.0s - 0.3s
├── Render Opacity: 0 → 1 (Ease Out)
└── Transform Scale: 0.9 → 1 (Ease Out)
```

### Notification Slide
```
Timeline: 0.0s - 3.0s
├── 0.0s: Translation Y = -50, Opacity = 0
├── 0.2s: Translation Y = 0, Opacity = 1
├── 2.8s: Translation Y = 0, Opacity = 1
└── 3.0s: Translation Y = -50, Opacity = 0
```

## Responsive Design

### Breakpoints
```
Mobile: < 720px width
├── Scale UI: 1.5x
├── Touch targets: 80x80 min
└── Simplified layout

Tablet: 720px - 1080px
├── Scale UI: 1.2x
├── Hybrid touch/controller
└── Standard layout

Desktop: > 1080px
├── Scale UI: 1.0x
├── Full feature set
└── Advanced layout
```

## Blueprint Communication

### PlayerController → Widget
```
Player Controller
    └── Function: UpdateHUD
        ├── Get HUD Widget
        ├── Cast to W_MainHUD
        └── Call UpdateHealth Event
```

### Widget → GameMode
```
Pause Menu Button: Quit
    ├── Get Game Mode
    ├── Cast to BP_GameMode_DaVerse
    ├── Call: ReturnToMainMenu
    └── Remove from Parent
```

### Event Dispatcher Pattern
```
BP_PlayerCharacter
    └── Event Dispatcher: OnHealthChanged
        └── Broadcast (NewHealth, MaxHealth)

W_MainHUD
    └── Event Construct
        └── Bind to OnHealthChanged
            └── Call UpdateHealth
```
