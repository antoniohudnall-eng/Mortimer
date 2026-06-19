# Milk Man — Sprite Sheet Specifications

## Characters

### 🥛 Milk Man (Hero)

**Animation States & Frame Counts:**

| State | Description | Frames | Notes |
|-------|-------------|--------|-------|
| **Idle** | Standing proud, cape fluttering | 3 | Slight cape movement |
| **Walk** | Smooth stride, splashing footsteps | 6 | Alternate leg/arm motion |
| **Jump** | Launch pose, mid-air leg tuck | 4 | Cape billow, vy effect |
| **Attack (Fist)** | Classic punch with splash impact | 5 | Hand-to-hand combat |
| **Projectile** | Throws milk bottle in arc | 4 | Overhand throw motion |
| **Damage** | Recoil with goofy wince | 2 | Frames should show impact |
| **Power-Up** | Glowing outline, milk sparkles | 3 | Absorbs power-up animation |
| **Victory** | One arm raised, bottle held aloft | 2 | Level clear pose |
| **Slide** | Slide across hood (variant) | 3 | Action hero moment |

**Sprite Size:** 32x32 pixels per frame  
**Format:** PNG with alpha channel  
**Color Palette:** White hero, cape, milk splashes, golden accents

---

### 🧪 Vil Laine (Boss 1)

**Animation States & Frame Counts:**

| State | Description | Frames | Notes |
|-------|-------------|--------|-------|
| **Idle** | Arms crossed, evil smirk | 3 | Eyes darting |
| **Bottle Throw Prep** | Wind-up stance | 2 | Acidic milk bottle |
| **Bottle Throw** | Overhand launch | 4 | Trail blur effect |
| **Walk (Menace)** | Hunched strut | 6 | Cape dragging |
| **Lair Laugh** | Head back, evil cackle | 3 | Animated villain laugh |
| **Hit Reaction** | Twitch with splash | 2 | Bubbling face |
| **Defeat** | Spin, splash, disappear | 4 | Melts into sour puddle |

**Sprite Size:** 40x40 pixels  
**Colors:** Purple (#800080), dark tones, acidic green accents

---

### 👠 Madame Shoezete (Boss 2)

**Animation States & Frame Counts:**

| State | Description | Frames | Notes |
|-------|-------------|--------|-------|
| **Idle** | Pacing with heel clicks | 4 | Cape swishes |
| **Lactose Beam Prep** | Energy in heels glowing | 3 | Toes glow effect |
| **Lactose Beam Fire** | Horizontal beam | 6 | Pulse animation, splash decals |
| **Dash Attack** | Heel-power dash | 4 | Yogurt blur trail |
| **Stomp Slam** | Jump, slam, ricotta shockwave | 5 | Cheese pits created |
| **Hit Reaction** | Wobble, curdled face | 2 | Disgust expression |
| **Defeat** | Melts into whipped cream | 3 | Dramatic glove up |

**Sprite Size:** 48x48 pixels  
**Colors:** Pink (#FF69B4), whip cream white, gold accents  
**Effects:** Glitch overlays, "milk couture" sparkles

---

## Enemy: Boy Scouts

**Animation:** Walk cycle only (simplified)
**Frames:** 4 frames
**Size:** 20x20 pixels
**Colors:** Green (#228B22), khaki

---

## Enemy: Bottle Throwers

**Animation:** Stand + throw
**Frames:** 4 frames
**Size:** 15x25 pixels  
**Colors:** Orange (#FF4500) projectiles

---

## Projectiles

**Milk Spray/Bottle:**
- **Size:** 10x10 pixels
- **Shape:** Circle or ovular
- **Effect:** White (#FFFFFF) with motion blur

**Lactose Beam:**
- **Size:** Full screen width, 20px height
- **Colors:** Gradient from yellow to white
- **Pulse:** 2-frame animation

---

## Backgrounds

**Level 1 — Dairyopolis Streets:**
- Sky: #87CEEB (sky blue)
- Ground: #FFD700 (golden/yellow)
- Buildings: Simple rectangles
- Parallax: 2 layers (buildings, clouds)

**Level 2 — Vil Laine's Lair:**
- Dark purple/blue sky
- Industrial pipes
- Lactose-free warning signs
- Conveyor belts (hazard)

**Level 3 — Madame Shoezete's Fortress:**
- Pink/purple gradient
- High fashion elements (runway, curtains)
- Cheese vats (hazard)
- Spotlight effects

---

## UI Elements

**Health Bar:**
- **Size:** 100x10 pixels
- **Color:** Red (#FF0000) filled, gray background
- **Position:** Top-left corner

**Level Indicator:**
- **Size:** Text-based
- **Position:** Top-left, below health

**Score:**
- **Calculation:** (level × 100) + enemies_defeated × 10
- **Position:** Top-right

---

## Animation Timing

**Game FPS:** 30  
**Frame Duration:** 33ms per frame

**Animation Speeds:**
- **Idle:** 8 FPS (slow, idle feel)
- **Walk:** 12 FPS (smooth motion)
- **Attack:** 20 FPS (fast impact)
- **Damage:** 15 FPS (quick reaction)

---

## Sprite Sheet Layout

Recommended format:** Single sheet per character
- **Width:** (frame_width × num_frames)
- **Height:** (animation_rows × frame_height)
- **Example:** Milk Man = (32 × 29 frames) × 32px height

OR** Separate files per animation state (easier for DroidScript)

---

## Deliverables

**For Each Character:**
- [ ] Idle animation PNG
- [ ] Walk animation PNG
- [ ] Jump animation PNG
- [ ] Attack animation PNG (2 variants)
- [ ] Damage animation PNG
- [ ] Victory/Defeat animation PNG

**For Levels:**
- [ ] Level 1 background (3 layers)
- [ ] Level 2 background (3 layers)
- [ ] Level 3 background (3 layers)

**UI:**
- [ ] Health bar sprites
- [ ] Font assets (pixel/chiptune style)
- [ ] Menu backgrounds

**Status:** ⏳ Awaiting art team coordination  
**Assigned:** Miles + OpenClaw collaboration  
**GitHub:** Private repo creation pending
