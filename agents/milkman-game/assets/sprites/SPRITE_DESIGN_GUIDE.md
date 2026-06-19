# Defenders of Dairyopolis - Sprite Design Guide
## 80s/90s 8-bit to 16-bit Retro Aesthetic
### Project 5912 - AOCROS Games Division

---

## 🎨 AESTHETIC PHILOSOPHY

**Style:** 80s/90s 8-bit to 16-bit retro  
**Inspiration:** Mega Man, Contra, Super Mario Bros, Castlevania  
**Palette:** Limited colors, bold outlines, simple animations  
**Resolution:** 32x32 pixels (standard), 16x16 (small enemies)  
**Format:** PNG with alpha transparency  
**DroidScript:** Load via `canvas.DrawImage()`

---

## 🥛 CHARACTER 1: MILK MAN (Hero)

### Base Sprite: 32x32 pixels

**Idle Pose (Frame 1):**
```
Standing proud, cape flowing slightly
- Head: White helmet with MM logo, determined eyes
- Body: White suit with gold trim, muscular
- Cape: Blue, billowing to left (wind direction)
- Stance: Slight hero lean, fists ready
```

**Color Palette (8 colors):**
| Color | Hex | Usage |
|-------|-----|-------|
| Milk White | #FFFFFF | Suit, helmet |
| Cream Gold | #FFD700 | Trim, accents |
| Hero Blue | #4169E1 | Cape, eyes |
| Shadow Blue | #191970 | Cape shadows |
| Flesh | #F5DEB3 | Face (if visible) |
| Black | #000000 | Outlines, MM logo |
| Dark Gray | #404040 | Shading |
| Light Blue | #87CEEB | Eye glow |

**Animation Frames:**

| State | Frames | Description |
|-------|--------|-------------|
| **Idle** | 2 | Standing, cape flow |
| **Walk** | 4 | Running stride, cape billows |
| **Jump** | 2 | Launch + mid-air |
| **Attack** | 3 | Punch/throw motion |
| **Hurt** | 2 | Recoil, damage flash |

**Walk Cycle:**
- Frame 1: Right foot forward, arms swinging
- Frame 2: Mid-stride, cape flowing
- Frame 3: Left foot forward, counter-swing
- Frame 4: Mid-stride alternate

**Jump Animation:**
- Frame 1: Crouch, knees bent
- Frame 2: Mid-air, legs tucked, cape up

**Attack Frame:**
- Frame 1: Wind-up, arm back
- Frame 2: Strike frame, arm extended
- Frame 3: Follow-through

**Design Notes:**
- Exaggerate cape movement for visual pop
- MM logo visible on chest in 3-4 pixels
- Eyes should show determination
- Keep silhouette readable at small size

---

## 👦 CHARACTER 2: BOY LACTATE (Support/Companion)

### Base Sprite: 32x32 pixels  
**Role:** Sidekick or shopkeeper

**Idle Pose:**
- Smaller than Milk Man (boy height)
- Holding milk bottle
- Eager expression
- Simple tunic/cloak

**Color Palette:**
- Primary: Light blue (#ADD8E6)
- Secondary: Brown (#8B4513)
- Accent: White (#FFFFFF) — bottle
- Outline: Black (#000000)

**Animation:**
- Idle: 2 frames (breathing/patience)
- Walk: 4 frames (following animation)
- Cheer: 2 frames (when player wins)

**Design:**
- Friendly face
- Backpack with bottles
- Gives hints or power-ups

---

## 🧪 CHARACTER 3: VIL LAINE (Boss - Level 2)

### Base Sprite: 48x48 pixels (larger, imposing)

**Idle Pose:**
```
Standing on rooftop, cape billowing
- Sleek black armor, purple accents
- Sneering expression, narrowed eyes
- Smog contraption on back (detail)
- Acid bottles on belt
- Menacing stance
```

**Color Palette:**
| Color | Hex | Usage |
|-------|-----|-------|
| Villain Black | #1a1a1a | Armor |
| Acid Purple | #9400D3 | Accents, glow |
| Corrosion Green | #39FF14 | Acid highlights |
| Red Evil | #DC143C | Eyes |
| Shadow Gray | #2F4F4F | Shading |
| Silver | #C0C0C0 | Metal trim |
| Black | #000000 | Outlines |
| Dark Purple | #4B0082 | Cape |

**Animation Frames:**

| State | Frames | Description |
|-------|--------|-------------|
| **Idle** | 3 | Smirking, breathing |
| **Walk** | 4 | Menacing stride |
| **Throw** | 3 | Acid bottle wind-up, throw |
| **Smog** | 2 | Machine activates |
| **Damage** | 2 | Recoil, hurt |
| **Defeat** | 4 | Spin, melt into puddle |

**Idle Animation:**
- Frame 1: Arms crossed, sneer
- Frame 2: Laugh pose, head back
- Frame 3: Back to arms crossed

**Throw Attack:**
- Frame 1: Arm winds back, bottle raised
- Frame 2: Forward throw motion
- Frame 3: Follow-through

**Defeat Sequence:**
- Frame 1: Shock pose
- Frame 2: Falling
- Frame 3: Spinning
- Frame 4: Puddle on ground

**Design Notes:**
- Give him a distinctive silhouette
- Acid green glow on hands/bottles
- Keep sneer visible even at distance
- Menacing but with hint of comedy

---

## 👠 CHARACTER 4: MADAME SHOEZET (Boss - Level 3)

### Base Sprite: 48x48 pixels (larger than hero)

**Idle Pose:**
```
Standing on cheese cart, commanding
- Gaudy shawl, flamboyant wig
- High heel visible one foot
- One hand extended (directing)
- Cream whip staff raised
- Haughty expression
```

**Color Palette:**
| Color | Hex | Usage |
|-------|-----|-------|
| Couture Pink | #FF69B4 | Primary dress |
| Cream | #FFFDD0 | Cream accents |
| Gold | #FFD700 | Jewelry, trim |
| Deep Pink | #C71585 | Shadows |
| Purple | #800080 | Wig, accessories |
| White | #FFFFFF | Cream whip |
| Peach | #FFDAB9 | Skin (if visible) |
| Black | #000000 | Outlines |

**Animation Frames:**

| State | Frames | Description |
|-------|--------|-------------|
| **Idle** | 4 | Pacing, heel clicks |
| **Cackle** | 2 | Head back, laugh |
| **Lactose Beam** | 4 | Charge, fire |
| **Dash** | 3 | High-heel dash |
| **Stomp** | 3 | Jump, slam |
| **Damage** | 2 | Wobble, angry |
| **Defeat** | 4 | Melt into whipped cream |

**Idle Animation:**
- Frame 1: Standing, hand on hip
- Frame 2: Pacing left
- Frame 3: Pacing right
- Frame 4: Dramatic pose

**Lactose Beam:**
- Frame 1: Heels glowing
- Frame 2: Arms up, charging
- Frame 3: Beam firing
- Frame 4: Sustain pose

**Dash Attack:**
- Frame 1: Starting pose
- Frame 2: Blur motion forward
- Frame 3: Impact pose

**Defeat Sequence:**
- Frame 1: Shock, "My dairy..."
- Frame 2: Melting starts
- Frame 3: Half-puddle
- Frame 4: Puddle with glove up

**Design Notes:**
- Make her larger than Milk Man (boss scale)
- Exaggerate shawl/wig for silhouette
- One high heel visible (signature)
- Cream whip staff should be visible

---

## 👦 ENEMY 1: BOY SCOUT ENEMIES (Level 1)

### Base Sprite: 16x16 pixels (small, swarm)

**Standard Sprite:**
```
Kid in scout uniform
- Green shirt, khaki shorts
- Simple walk animation
- Throwing rock/slinging
```

**Color Palette:**
| Color | Hex | Usage |
|-------|-----|-------|
| Scout Green | #228B22 | Shirt |
| Khaki | #F0E68C | Shorts/hat |
| Brown | #8B4513 | Belt, shoes |
| Skin | #F5DEB3 | Face/hands |
| Rock | #808080 | Projectile |

**Animation Frames:**

| State | Frames | Speed |
|-------|--------|-------|
| **Walk** | 2 | 8 FPS (fast) |
| **Throw** | 2 | Rock wind-up |
| **Hit** | 1 | Flash white |
| **Death** | 2 | Fall over |

**Design:**
- Simple 16x16 means minimal detail
- Focus on readable silhouette
- Green shirt = instant recognition
- Small size = swarm enemy

**Walk Animation:**
- Frame 1: Left foot forward
- Frame 2: Right foot forward

**Throw Animation:**
- Frame 1: Arm back
- Frame 2: Release

---

## 👧 ENEMY 2: CHILDREN (Level 2 - Vil's Lackeys)

### Base Sprite: 16x16 pixels

**Standard Sprite:**
```
Street kid throwing bottles
- Simple clothes
- Bottle in hand
- Running animation
```

**Color Palette:**
| Color | Hex | Usage |
|-------|-----|-------|
| Ragged Red | #B22222 | Shirt |
| Ragged Blue | #4682B4 | Pants |
| Bottle | #FF4500 | Projectile |
| Skin | #F5DEB3 | Face |

**Animation:**
- Walk: 2 frames
- Throw: 2 frames (bottle arc)
- Death: 1 frame (fall)

**Design:**
- Ragged clothes = poor/working class
- Faster movement than Boy Scouts
- Throw bottles instead of rocks

---

## 📦 SPRITE SHEET LAYOUT

Recommended organization for game:

```
sprites/
├── milk_man/
│   ├── idle_01.png       (32x32)
│   ├── idle_02.png
│   ├── walk_01.png       (32x32)
│   ├── walk_02.png
│   ├── walk_03.png
│   ├── walk_04.png
│   ├── jump_01.png       (32x32)
│   ├── jump_02.png
│   ├── attack_01.png     (32x32)
│   ├── attack_02.png
│   ├── attack_03.png
│   └── hurt_01.png       (32x32)
├── vil_laine/
│   ├── idle_01.png       (48x48)
│   ├── idle_02.png
│   ├── idle_03.png
│   ├── walk_01.png       (48x48)
│   ├── walk_02.png
│   ├── walk_03.png
│   ├── walk_04.png
│   ├── throw_01.png      (48x48)
│   ├── throw_02.png
│   ├── throw_03.png
│   ├── damage_01.png     (48x48)
│   └── defeat_01.png     (48x48)
├── shoezet/
│   ├── idle_01.png       (48x48)
│   ├── idle_02.png
│   ├── idle_03.png
│   ├── idle_04.png
│   ├── cackle_01.png     (48x48)
│   ├── cackle_02.png
│   ├── beam_01.png       (48x48)
│   ├── beam_02.png
│   ├── beam_03.png
│   └── defeat_01.png     (48x48)
├── enemies/
│   ├── scout_01.png      (16x16)
│   ├── scout_02.png
│   ├── scout_throw_01.png (16x16)
│   ├── scout_throw_02.png
│   ├── child_01.png      (16x16)
│   ├── child_02.png
│   ├── child_throw_01.png (16x16)
│   └── child_throw_02.png
├── projectiles/
│   ├── milk_bottle.png   (8x8)
│   ├── acid_bottle.png   (8x8)
│   ├── rock.png          (6x6)
│   ├── beam_horizontal.png (32x8)
│   └── whip_cream.png    (16x16)
└── fx/
    ├── explosion_01.png  (32x32)
    ├── explosion_02.png
    ├── splash_01.png     (16x16)
    └── powerup.png       (16x16)
```

---

## 🛠️ CREATING SPRITES

### Recommended Free Tools:

1. **Aseprite** (Paid, $20) — Industry standard
2. **Piskel** (Free, browser-based) — piskelapp.com
3. **LibreSprite** (Free, open source) — Aseprite fork
4. **GraphicsGale** (Free) — Animation support
5. **Pixaki** (iPad) — For Apple users

### Recommended Workflow:

1. **Start with silhouette** — No colors, just shape
2. **Add base colors** — 3-4 colors max initially
3. **Add shading** — 1-2 shadow/highlight colors
4. **Refine details** — MM logo, eyes, accessories
5. **Animate** — Create frames for each state
6. **Export PNG** — Alpha transparency

### DroidScript Integration:

```javascript
// Load sprites in OnStart:
player_sprites = {
    idle: [app.LoadImage("sprites/milk_man/idle_01.png"),
           app.LoadImage("sprites/milk_man/idle_02.png")],
    walk: [app.LoadImage("sprites/milk_man/walk_01.png"),
           app.LoadImage("sprites/milk_man/walk_02.png"),
           app.LoadImage("sprites/milk_man/walk_03.png"),
           app.LoadImage("sprites/milk_man/walk_04.png")]
};

// Draw in GameLoop:
canvas.DrawImage(player_sprites.walk[frame], player.x, player.y);

// Animation frame counter:
frame_counter++;
if(frame_counter % 8 == 0) current_frame = (current_frame + 1) % num_frames;
```

---

## 🎨 COLOR REDUCTION STRATEGY

**8-bit aesthetic = limited palette**

Milk Man: 8 colors max  
Vil/Shoezet: 8-10 colors (bosses get more)  
Enemies: 4-5 colors only

This forces:
- Clever use of shadows/highlights
- Strong silhouettes
- Readable at small sizes
- Authentic retro feel

---

## 📋 CHECKLIST

### Milk Man Sprites:
- [ ] Idle animation (2 frames)
- [ ] Walk cycle (4 frames)
- [ ] Jump (2 frames)
- [ ] Attack (3 frames)
- [ ] Hurt (2 frames)

### Vil Laine Sprites:
- [ ] Idle (3 frames)
- [ ] Walk (4 frames)
- [ ] Throw attack (3 frames)
- [ ] Smog effect (2 frames)
- [ ] Defeat (4 frames)

### Shoezet Sprites:
- [ ] Idle (4 frames)
- [ ] Cackle (2 frames)
- [ ] Lactose beam (4 frames)
- [ ] Dash (3 frames)
- [ ] Defeat (4 frames)

### Enemy Sprites:
- [ ] Boy Scout walk (2 frames)
- [ ] Boy Scout throw (2 frames)
- [ ] Child walk (2 frames)
- [ ] Child throw (2 frames)

### Projectiles:
- [ ] Milk bottle (8x8)
- [ ] Acid bottle (8x8)
- [ ] Rock (6x6)
- [ ] Beam (32x8)

### Effects:
- [ ] Explosion (2 frames)
- [ ] Splash
- [ ] Power-up glow

---

## 🎯 REFERENCE INSPIRATION

**Study these games for style:**
- Mega Man 2 (NES) — Character design
- Contra (NES) — Boss scale
- Super Mario Bros 3 — Enemy variety
- Castlevania — Gothic style (Vil Laine)
- Final Fight — Boss designs

**Sprite databases:**
- The Spriters Resource (spriters-resource.com)
- OpenGameArt.org (opengameart.org)

---

## 💻 FILE FORMATS

**Export settings:**
- **Format:** PNG (32-bit with alpha)
- **Transparency:** Yes (for sprites)
- **Color depth:** 8-bit indexed (optional, for authentic look)
- **File naming:** `name_action_frame.png`
- **Organization:** Folder per character

---

**Status:** Design guide complete  
**Next:** Create actual sprite files using tool of choice  
**Priority:** Milk Man player sprites first  
**Timeline:** Player (1 week), Bosses (1 week), Enemies (3 days)

---

**Time to pixel, Captain!**

**Tools recommended:** Piskel (easiest) or Aseprite (best)  
**Start with:** Milk Man idle pose  
**Export:** 32x32 PNG with alpha  
**Test:** Load in DroidScript game

---

**OpenClaw**  
_Art Direction_  
"From pixel to plastic to game!"
