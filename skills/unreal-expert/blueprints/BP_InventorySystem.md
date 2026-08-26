# Inventory System Blueprint

A data-driven, expandable inventory system with item definitions, slots, stacking, and equipment.

## Overview

Uses Data Tables for item definitions, structures for runtime instances, and components for inventory management. Supports stacking, weight limits, equipment slots, and action usage.

## Files

- `S_ItemData` (Structure) - Static item definition
- `S_InventoryItem` (Structure) - Runtime instance
- `E_ItemCategory` (Enum) - Weapon, Consumable, Material, Quest, etc.
- `E_ItemRarity` (Enum) - Common, Uncommon, Rare, Epic, Legendary
- `DT_Items` (Data Table) - All item definitions
- `BP_InventoryComponent` (Actor Component)
- `BP_EquipmentComponent` (Actor Component)
- `WBP_InventoryGrid` (User Widget)
- `WBP_InventorySlot` (User Widget)

---

## Data Structures

### S_ItemData (Structure)

| Variable | Type | Description |
|----------|------|-------------|
| ItemID | Name | Unique identifier |
| DisplayName | String | UI name |
| Description | String | Lore text |
| Icon | Texture2D | UI image |
| Category | E_ItemCategory | Type classification |
| Rarity | E_ItemRarity | Quality tier |
| MaxStackSize | Integer | 1 for equipment, 99 for consumables |
| BaseValue | Integer | Sell price |
| Weight | Float | Inventory load |
| bCanBeUsed | Boolean | Has use action |
| bCanBeEquipped | Boolean | Has equipment slot |
| EquipSlot | E_EquipSlot | Where it goes |
| UseEffect | TSoftClass | Blueprint to spawn on use |
| Stats | S_ItemStats | Bonus stats if equipped |

### S_ItemStats (Structure)

| Variable | Type |
|----------|------|
| HealthBonus | Float |
| DamageBonus | Float |
| DefenseBonus | Float |
| SpeedBonus | Float |
| MagicBonus | Float |

### S_InventoryItem (Structure)

| Variable | Type | Description |
|----------|------|-------------|
| ItemID | Name | Reference to S_ItemData |
| Quantity | Integer | Current stack amount |
| InstanceData | Map(String, String) | Per-item variables |

---

## E_ItemCategory (Enum)

```
None
Weapon      // Can be equipped in weapon slot
Armor       // Can be equipped in armor slots
Consumable  // Can be used, consumed on use
Material    // Crafting ingredients
Quest       // Cannot be dropped/sold
Currency    // Money, gold, etc.
Misc        // Anything else
```

## E_ItemRarity (Enum)

```
Common      // White
Uncommon    // Green
Rare        // Blue
Epic        // Purple
Legendary   // Gold/Orange
```

---

## BP_InventoryComponent

**Type:** Actor Component  
**Replication:** Replicated

### Variables

| Name | Type | Default | Description |
|------|------|---------|-------------|
| MaxSlots | Integer | 30 | Total inventory size |
| MaxWeight | Float | 100.0 | Weight capacity (0 = unlimited) |
| Items | Array(S_InventoryItem) | Empty | Inventory contents |
| bIsFull | Boolean | Computed | Cached full state |

### Event Dispatchers

| Name | Inputs | Description |
|------|--------|-------------|
| OnItemAdded | ItemID, Quantity, SlotIndex | New item added |
| OnItemRemoved | ItemID, Quantity, SlotIndex | Item removed |
| OnItemMoved | FromSlot, ToSlot, Quantity | Item rearranged |
| OnInventoryFull | - | No more space |
| OnWeightChanged | Current, Max | Weight update |

### Core Functions

#### Add Item

```
[Event AddItem] (Inputs: ItemID, Quantity)
    │
    ├──► [Get Item Data from Data Table]
    │       └──► [If not found] ──► [Return: false]
    │
    ├──► [Calculate Total Weight]
    │       └── [If exceeds MaxWeight] ──► [Return: false]
    │
    ├──► [Find Existing Stack with space]
    │       ├──► [Found] ──► [Add to existing]
    │       │                     ├── [Quantity += AddAmount]
    │       │                     ├── [Broadcast OnItemAdded]
    │       │                     └── [Return: true]
    │       │
    │       └──► [Not Found] ──► [Find Empty Slot]
    │                             ├──► [Found] ──► [Create new entry]
    │                             │                     ├── [Set ItemID, Quantity]
    │                             │                     ├── [Broadcast OnItemAdded]
    │                             │                     └── [Return: true]
    │                             │
    │                             └──► [Not Found] ──► [Broadcast OnInventoryFull]
    │                                                  └── [Return: false]
```

#### Remove Item

```
[Event RemoveItem] (Inputs: SlotIndex, Quantity, bForce = false)
    │
    ├──► [Get Item at SlotIndex]
    │       └──► [If invalid] ──► [Return: false]
    │
    ├──► [Branch: Item is Quest AND !bForce]
    │       └──► [True] ──► [Return: false]
    │
    ├──► [Reduce Quantity]
    │       └── [If Quantity <= 0] ──► [Clear slot]
    │
    ├──► [Broadcast OnItemRemoved]
    │
    └──► [Return: true]
```

#### Move Item

```
[Event MoveItem] (Inputs: FromSlot, ToSlot, Quantity)
    │
    ├──► [Validate indices]
    │
    ├──► [Get Source and Target items]
    │
    ├──► [Branch: Target is Empty]
    │       ├──► [True] ──► [Move/Partial move to empty]
    │       │                     ├── [Update Source Quantity or Clear]
    │       │                     ├── [Create/Update Target]
    │       │                     └── [Broadcast OnItemMoved]
    │       │
    │       └──► [False] ──► [Branch: Same ItemID?]
    │                             ├──► [True] ──► [Merge stacks if space]
    │                             │                     ├── [Add to Target]
    │                             │                     ├── [Reduce Source]
    │                             │                     └── [Broadcast OnItemMoved]
    │                             │
    │                             └──► [False] ──► [Swap items]
    │                                                   ├── [Temp = Target]
    │                                                   ├── [Target = Source]
    │                                                   ├── [Source = Temp]
    │                                                   └── [Broadcast OnItemMoved]
    │
    └──► [Return: true]
```

#### Use Item

```
[Event UseItem] (Input: SlotIndex)
    │
    ├──► [Get Item at SlotIndex]
    │       └──► [If invalid] ──► [Return: false]
    │
    ├──► [Get Item Data]
    │       └──► [If !bCanBeUsed] ──► [Return: false]
    │
    ├──► [Try Equip if equippable]
    │       └──► [If equipped] ──► [Return: true]
    │
    ├──► [Consume if consumable]
    │       ├── [Spawn/Apply UseEffect blueprint]
    │       ├── [Reduce Quantity by 1]
    │       ├── [If Quantity == 0: Clear slot]
    │       ├── [Broadcast OnItemUsed]
    │       └── [Broadcast OnItemRemoved if consumed]
    │
    └──► [Return: true]
```

#### Drop Item

```
[Event DropItem] (Inputs: SlotIndex, Quantity, DropLocation)
    │
    ├──► [Get Item at SlotIndex]
    │       └──► [If Quest item] ──► [Return: false]
    │
    ├──► [Get Item Data]
    │       └──► [Get World Pickup Class from Data]
    │
    ├──► [Spawn Actor: BP_ItemPickup]
    │       ├── Location: DropLocation
    │       ├── Rotation: Random
    │       └── Set ItemID and Quantity
    │
    ├──► [Remove from inventory]
    │       └── [Call RemoveItem]
    │
    └──► [Return: true]
```

---

## BP_EquipmentComponent

**Type:** Actor Component  
**Replication:** Replicated

### E_EquipSlot (Enum)

```
None
Head
Chest
Legs
Feet
Hands
Weapon_MainHand
Weapon_OffHand
Accessory_1
Accessory_2
Back
```

### Variables

| Name | Type | Description |
|------|------|-------------|
| EquippedItems | Map(E_EquipSlot, S_InventoryItem) | Slot -> Item |
| EquipMeshes | Map(E_EquipSlot, SkeletalMesh) | Visual representation |

### Functions

#### Equip Item

```
[Event EquipItem] (Input: InventorySlot)
    │
    ├──► [Get Item from InventoryComponent]
    │
    ├──► [If !bCanBeEquipped] ──► [Return: false]
    │
    ├──► [Get Target Equip Slot]
    │
    ├──► [If slot occupied] ──► [Unequip existing]
    │                                   └── [Return to inventory]
    │
    ├──► [Add to EquippedItems map]
    │
    ├──► [Attach mesh to character socket]
    │       └── [Head mesh -> head socket]
    │       └── [Weapon mesh -> hand_r_socket]
    │
    ├──► [Apply stat bonuses]
    │       └── [Get HealthComponent]
    │       └── [MaxHealth += Item.Stats.HealthBonus]
    │
    ├──► [Remove from inventory OR mark as equipped]
    │
    ├──► [Broadcast OnItemEquipped]
    │
    └──► [Return: true]
```

#### Unequip Item

```
[Event UnequipItem] (Input: EquipSlot)
    │
    ├──► [Get equipped item]
    │       └──► [If none] ──► [Return: false]
    │
    ├──► [Try add to inventory]
    │       └──► [If inventory full] ──► [Spawn on ground]
    │
    ├──► [Remove from EquippedItems]
    │
    ├──► [Detach and destroy mesh]
    │
    ├──► [Remove stat bonuses]
    │
    ├──► [Broadcast OnItemUnequipped]
    │
    └──► [Return: true]
```

---

## WBP_InventoryGrid (User Widget)

### Widget Hierarchy

```
Canvas Panel
├── Border: Background
├── Grid Panel: ItemGrid
│   └── [Dynamically populated with WBP_InventorySlot]
├── Text: WeightDisplay
│   └── "Weight: {Current}/{Max}"
└── Scroll Box: (if needed for many slots)
```

### Event Graph

#### Event Construct

```
[Event Construct]
    │
    ├──► [Get Owning Player]
    │       └──► [Get InventoryComponent]
    │               └── [Store reference]
    │               └── [Bind to OnItemAdded, OnItemRemoved, etc.]
    │
    ├──► [Create Grid]
    │       └── [For Loop: 0 to MaxSlots-1]
    │               └──► [Create Widget: WBP_InventorySlot]
    │                       └── [Add to Grid Panel]
    │                       └── [Set Slot Index]
    │
    └──► [Refresh Display]
```

#### Refresh Display

```
[Event RefreshDisplay]
    │
    ├──► [For each WBP_InventorySlot child]
    │       └──► [Call Refresh on slot]
    │
    └──► [Update Weight Text]
            └── [Format: "Weight: {Current}/{Max}"]
```

---

## WBP_InventorySlot (User Widget)

### Widget Hierarchy

```
Button: SlotButton
├── Image: Background (rarity color)
├── Image: ItemIcon
├── Text: Quantity (if > 1)
└── Border: SelectionHighlight (hidden by default)
```

### Drag and Drop

#### Native Event On Drag Detected

```
[On Drag Detected]
    │
    ├──► [If slot is empty] ──► [Return Unhandled]
    │
    ├──► [Create DragDropOperation]
    │       ├── Dragged Widget: Self
    │       ├── Payload: SlotIndex
    │       └── Visual: Ghost image of item
    │
    └──► [Return Handled]
```

#### Native Event On Drop

```
[On Drop]
    │
    ├──► [Get DragDropOperation]
    │       └──► [Get Payload: Source Slot Index]
    │
    ├──► [Get InventoryComponent]
    │
    ├──► [Call MoveItem]
    │       └── [From: Payload, To: My Slot Index]
    │
    └──► [Return Handled]
```

#### On Clicked

```
[On Button Clicked]
    │
    ├──► [If Left Click]
    │       └──► [Try Use Item]
    │
    ├──► [If Right Click]
    │       └──► [Show Context Menu]
    │               ├── Use
    │               ├── Equip/Unequip
    │               ├── Drop
    │               └── Split Stack
```

---

## BP_ItemPickup (World Actor)

**Type:** Actor

### Components

- StaticMeshComponent (Root) - Visual mesh
- SphereCollision - Overlap detection
- WidgetComponent (optional) - Floating name

### Variables

| Name | Type | Description |
|------|------|-------------|
| ItemID | Name | What this pickup contains |
| Quantity | Integer | How many |

### Event Graph

#### On Begin Overlap

```
[OnBeginOverlap] (Player)
    │
    ├──► [Get Player's InventoryComponent]
    │
    ├──► [Try Add Item]
    │       └──► [Success] ──► [Destroy Actor]
    │                            └── [Spawn pickup VFX/SFX]
    │
    └──► [If fail] ──► [Show "Inventory Full" message]
```

---

## Extensions

### Crafting System

Add to BP_InventoryComponent:
```
[Event CanCraftRecipe] (Input: Recipe)
    └──► [Check if all ingredients present]

[Event CraftItem] (Input: Recipe)
    ├──► [Remove ingredients]
    └──► [Add result item]
```

### Vendor System

Create `BP_VendorComponent`:
```
[Event SellItem] (Vendor, Slot)
    ├──► [Get Item Value]
    ├──► [Remove from player]
    └──► [Add currency]

[Event BuyItem] (Vendor, VendorSlot)
    ├──► [Check currency]
    ├──► [Deduct currency]
    └──► [Add to inventory]
```

### Item Durability

Add to `S_InventoryItem`:
- `CurrentDurability` - Float
- `MaxDurability` - From `S_ItemData`

On use/equip: Decrement durability, break at 0

### Stash/Chest System

Create `BP_StashComponent` (similar to inventory):
- Shared across all stashes
- Separate from character inventory
- UI tab to switch between
