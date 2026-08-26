# Health and Damage System Blueprint

A comprehensive, component-based health and damage system with events, modifiers, and team support.

## Overview

This pattern uses an Actor Component for health management, allowing any actor to have health without complex inheritance hierarchies. Implements damage types, events, and team-based damage filtering.

## Files

- `BP_HealthComponent` (Actor Component)
- `BP_DamageTypeBase` (Blueprint)
- `BP_HealthInterface` (Blueprint Interface, optional)
- `BP_HealthBarWidget` (User Widget)
- `BP_ExampleCharacter` (Implementation)

---

## BP_HealthComponent

**Type:** Actor Component  
**Replication:** Replicated (Multiplayer support)

### Variables

#### Core Health

| Name | Type | Default | Flags |
|------|------|---------|-------|
| MaxHealth | Float | 100.0 | Replicated, EditAnywhere |
| CurrentHealth | Float | 100.0 | Replicated, EditAnywhere |
| bIsDead | Boolean | False | Replicated |
| bInvulnerable | Boolean | False | EditAnywhere |
| bCanRegenerate | Boolean | False | EditAnywhere |
| RegenRate | Float | 5.0 | EditAnywhere (HP/sec) |
| RegenDelay | Float | 3.0 | EditAnywhere (after damage) |
| RegenTimer | Timer Handle | - | Private |

#### Team System

| Name | Type | Default | Description |
|------|------|---------|-------------|
| TeamId | Integer | 0 | 0 = neutral, 1 = player, 2 = enemy, etc. |
| bIgnoreFriendlyFire | Boolean | False | Block same-team damage |

#### Events (Event Dispatchers)

| Name | Inputs | Description |
|------|--------|-------------|
| OnHealthChanged | CurrentHealth, MaxHealth, Delta | Fires on any health change |
| OnDamaged | DamageAmount, DamageType, Instigator, Causer | Fires when taking damage |
| OnHealed | HealAmount, Source | Fires when healing applied |
| OnDeath | DamageType, Instigator | Fires when health reaches 0 |
| OnRevive | - | Fires when revived |

---

## Event Graph

### Begin Play

```
[Event BeginPlay]
    │
    ├──► [IsServer]
    │       │
    │       └──► [True] ──► [InitializeHealth]
    │                         └── [CurrentHealth = MaxHealth]
    │                         └── [Broadcast OnHealthChanged]
    │
    └──► [Create Widget: HealthBar]
           └── [Attach to Owner] (if show health bar)
```

### Take Damage (BlueprintCallable)

```
[Event TakeDamage] (Inputs: DamageAmount, DamageType, Instigator, Causer, HitInfo)
    │
    ├──► [Branch: bIsDead] ──► [True] ──► [Return]
    │
    ├──► [Branch: bInvulnerable] ──► [True] ──► [Return]
    │
    ├──► [Check Team Damage]
    │       ├──► [Get TeamId of this component]
    │       ├──► [Get TeamId of Instigator]
    │       └──► [Branch: Same team AND bIgnoreFriendlyFire] ──► [Return]
    │
    ├──► [Modify Health]
    │       └──► [CurrentHealth = Clamp(CurrentHealth - DamageAmount, 0, MaxHealth)]
    │
    ├──► [Clear Timer: RegenTimer]
    │
    ├──► [Broadcast OnHealthChanged]
    │       └── [CurrentHealth, MaxHealth, -DamageAmount]
    │
    ├──► [Broadcast OnDamaged]
    │       └── [DamageAmount, DamageType, Instigator, Causer]
    │
    ├──► [Branch: CurrentHealth <= 0] ──► [True]
    │       │
    │       └──► [Die] (see below)
    │
    └──► [Branch: bCanRegenerate] ──► [True]
            │
            └──► [Set Timer by Function Name: StartRegeneration]
                     └── Delay: RegenDelay
```

### Heal (BlueprintCallable)

```
[Event Heal] (Inputs: HealAmount, HealSource)
    │
    ├──► [Branch: bIsDead] ──► [True] ──► [Return: false]
    │
    ├──► [Branch: CurrentHealth >= MaxHealth] ──► [True] ──► [Return: false]
    │
    ├──► [Modify Health]
    │       └──► [CurrentHealth = Min(CurrentHealth + HealAmount, MaxHealth)]
    │
    ├──► [Broadcast OnHealthChanged]
    │       └── [CurrentHealth, MaxHealth, +HealAmount]
    │
    ├──► [Broadcast OnHealed]
    │       └── [HealAmount, HealSource]
    │
    └──► [Return: true]
```

### Die (Private)

```
[Event Die] (Inputs: DamageType, Instigator)
    │
    ├──► [Set bIsDead = true]
    │
    ├──► [Broadcast OnDeath]
    │       └── [DamageType, Instigator]
    │
    └──► [BlueprintImplementableEvent: OnDeath_BP]
            └── [Override in child for visual effects, ragdoll, etc.]
```

### Revive (BlueprintCallable)

```
[Event Revive] (Inputs: ReviveHealthPercent = 0.5)
    │
    ├──► [Branch: !bIsDead] ──► [True] ──► [Return: false]
    │
    ├──► [Set CurrentHealth = MaxHealth * ReviveHealthPercent]
    │
    ├──► [Set bIsDead = false]
    │
    ├──► [Broadcast OnHealthChanged]
    │
    ├──► [Broadcast OnRevive]
    │
    └──► [Return: true]
```

### Regeneration

```
[Event StartRegeneration] (Timer callback)
    │
    └──► [Set Timer: RegenLoop]
             ├── Function: "RegenTick"
             ├── Time: 0.25 (or 1.0)
             └── Looping: true

[Event RegenTick]
    │
    ├──► [Branch: bIsDead OR CurrentHealth >= MaxHealth]
    │       └──► [True] ──► [Clear Timer: RegenTimer]
    │                       └── [Return]
    │
    └──► [Heal]
             └── [HealAmount: RegenRate * TickInterval]
```

---

## BP_DamageTypeBase

**Type:** Blueprint (Parent class: None, data-only)

### Variables

| Name | Type | Default | Description |
|------|------|---------|-------------|
| DamageMultiplier | Float | 1.0 | Global damage modifier |
| bCanCrit | Boolean | false | Allows critical hits |
| CritMultiplier | Float | 2.0 | Critical damage bonus |
| CritChance | Float | 0.05 | 0-1 probability |
| DamageColor | Color | Red | UI color for this damage type |
| HitReaction | AnimNotify | None | Animation to play |

### Child Types

- **BP_DamageType_Fire** - Damage over time, orange color
- **BP_DamageType_Ice** - Slow effect, blue color
- **BP_DamageType_Poison** - DOT, green color
- **BP_DamageType_Explosive** - Area damage, knockback
- **BP_DamageType_Fall** - No instigator, environmental

---

## BP_HealthBarWidget

**Type:** User Widget

### Widget Hierarchy

```
Canvas Panel
├── Progress Bar: HealthBar
│   ├── Fill Color: Green (or dynamic based on %)
│   └── Percent: Bound to HealthPercent
├── Text: HealthText
│   └── Text: "{Current}/{Max}" Bound
└── Border: DamageFlash
    └── Color: Red, Opacity: 0 (flashes on damage)
```

### Widget Blueprint

#### Event Construct

```
[Event Construct]
    │
    └──► [Get Owning Actor]
           └──► [Get Component by Class: HealthComponent]
                   └──► [Store as variable: TargetHealthComp]
                           └──► [Bind to OnHealthChanged]
                           └──► [Bind to OnDamaged]
```

#### Update Health Bar

```
[Event UpdateHealthBar] (Inputs: Current, Max)
    │
    ├──► [Set HealthBar Percent] = Current / Max
    │
    ├──► [Set HealthText] = "{Round(Current)}/{Round(Max)}"
    │
    └──► [Set Color]
             ├── [If Percent > 0.6] Green
             ├── [If Percent > 0.3] Yellow
             └── [Else] Red
```

#### On Damaged (Flash Effect)

```
[Event OnDamaged] (Inputs: DamageAmount, ...)
    │
    └──► [Play Animation: DamageFlash]
             └── [Opacity 0 -> 0.5 -> 0 over 0.2s]
```

---

## BP_ExampleCharacter Integration

### Components

- CapsuleComponent (Root)
- Mesh (Skeletal Mesh)
- Camera (SpringArm + Camera)
- **HealthComponent** (Added component)

### Event Graph

#### Event BeginPlay

```
[Event BeginPlay]
    │
    ├──► [Parent: BeginPlay]
    │
    └──► [Get HealthComponent]
           ├──► [Bind Event: OnHealthChanged] ──► [Update UI]
           ├──► [Bind Event: OnDamaged] ──► [Play Hit Reaction]
           └──► [Bind Event: OnDeath] ──► [HandleDeath]
```

#### Handle Death

```
[Event HandleDeath]
    │
    ├──► [Get Mesh]
    │       └──► [Set Simulate Physics] = true
    │       └──► [Set Collision Profile] = Ragdoll
    │
    ├──► [Get Capsule]
    │       └──► [Set Collision Enabled] = No Collision
    │
    ├──► [Disable Movement Input]
    │
    ├──► [Play Sound: Death]
    │
    └──► [Set Timer: DestroyActor] (5.0 seconds delay)
```

#### Apply Damage (Called from weapon/projectile)

```
[Event ApplyDamageToSelf] (Input: Damage)
    │
    └──► [Get HealthComponent]
              └──► [TakeDamage]
```

---

## Damage Application Patterns

### From Projectile

```
[On Hit]
    │
    └──► [Get Hit Actor]
           └──► [Get Component by Class: HealthComponent]
                    ├──► [Valid] ──► [TakeDamage]
                    │                  ├── DamageAmount: 25.0
                    │                  ├── DamageType: ProjectileDamage
                    │                  ├── Instigator: GetOwner
                    │                  └── Causer: Self
                    │
                    └──► [Invalid] ──► [Spawn Impact FX on environment]
```

### From Melee Weapon

```
[On Weapon Swing]
    │
    └──► [Sphere Trace]
            └──► [ForEach Hit]
                       └──► [If Has HealthComponent]
                                  └──► [TakeDamage]
```

### From Environment

```
[On Overlap Damage Volume]
    │
    └──► [Get Overlapping Actor]
           └──► [Get HealthComponent]
                    └──► [TakeDamage]
                             ├── DamageType: Environmental
                             └── Instigator: None
```

---

## Multiplayer Considerations

### Replication Setup

```cpp
// In C++ header (for reference, BP uses Details Panel)
UPROPERTY(ReplicatedUsing = OnRep_CurrentHealth)
float CurrentHealth;

UFUNCTION()
void OnRep_CurrentHealth();
```

In Blueprint:
1. Set Variable → Replication → RepNotify
2. Create OnRep function to update UI
3. Ensure TakeDamage runs on Server (Authority check)

### Server Authority

```
[TakeDamage Event]
    │
    ├──► [Switch Has Authority]
    │       │
    │       ├──► [Authority] ──► [Process damage logic]
    │       │                       └── [Client: Update UI via RepNotify]
    │       │
    │       └──► [Remote] ──► [Run on Server: TakeDamage]
    │                           └── [Return]
```

---

## Extensions

### Armor System

Add to HealthComponent:
- `ArmorValue` - Flat damage reduction
- `ArmorPercent` - Percentage reduction
- `DamageType_ArmorPiercing` - Ignores armor

### Status Effects

Create component `BP_StatusEffectComponent`:
- DOT (Damage Over Time)
- Stun (bCanTakeDamage = false)
- Heal Over Time
- Speed modifiers

### Kill Feed

Game State tracks:
```
[OnDeath Event]
    └──► [Get GameState]
              └──► [Add Kill Feed Entry]
                       └── [Killer, Victim, Weapon/DamageType]
```

### Damage Numbers

Spawn widget component on hit:
```
[OnDamaged]
    └──► [Spawn Actor: DamageNumberWidget]
              └── Location: Hit location + offset
              └── Value: DamageAmount
              └── Color: From DamageType
```
