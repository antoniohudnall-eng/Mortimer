# SGVD - Solar GraVitaional Duel
## Enhanced Solar System Module

**Status:** Complete ✅  
**Size:** 34KB  
**Features:** Realistic planets, moons, rings, asteroid belts

---

## 🌌 Solar System Features

### Star Types (4 Types)
- 🔴 **Red Dwarf** (3500K)
- 🟡 **Yellow Dwarf** (5800K)
- 🟠 **Orange Giant** (4500K)
- 🔵 **Blue-White** (12000K)

### Planet Types (4 Classes)

| Type | Colors | Mass | Moons | Rings |
|------|--------|------|-------|-------|
| **Terrestrial** | Gray, red-brown, blue-gray | 1.0x | 0-2 | No |
| **Super-Earth** | Aqua, deep blue | 2.5x | 0-3 | No |
| **Gas Giant** | Beige, orange, brown | 10.0x | 0-5 | Yes (45%) |
| **Ice Giant** | Steel blue, cyan | 8.0x | 0-4 | Yes (25%) |

### Planet Colors (Astronomical Accuracy)

**Terrestrial (close-in):**
- `#C1440E` - Red-brown (Mars-like)
- `#A0522D` - Sienna
- `#88AADD` - Blue-gray
- `#8B7355` - Earth tones

**Gas Giants:**
- `#FFCC99` - Beige
- `#D2691E` - Chocolate
- `#DEB887` - Burlywood
- `#CD853F` - Peru

**Ice Giants:**
- `#4682B4` - Steel blue
- `#5F9EA0` - Cadet blue
- `#87CEEB` - Sky blue
- `#ADD8E6` - Light blue

### Visual Effects

**Suns:**
- Base radius: 50-80px
- Glow radius: 1.6x
- 25% alpha halo

**Planet Enhancements:**
- 15-70% of sun size (much larger than before!)
- Shadow overlay (3D effect)
- Highlighting (specular)
- Orbit animation (slow, realistic)

**Rings (Gas/Ice Giants):**
- Inner: 1.5x planet radius
- Outer: 2.2x planet radius
- 40% transparency
- Lavender color (`#E0E0FF`)

**Moons:**
- 1.2-3.0x planet radius distance
- 8-15% of planet size
- Orbiting speed varies
- Gray or pale blue
- Shadow + highlight

**Asteroid Belts:**
- 20-50 asteroids
- Brown color
- Variable sizes (2-6px)
- Orbiting slowly
- 30% chance per system

---

## 🎮 Game Mechanics

### Dual Solar Systems
- **Left System:** (0.25, 0.5) screen position
- **Right System:** (0.75, 0.5) screen position
- Each with 1-5 planets, star, optional asteroid belt

### Physics
- **Gravity:** Attracts player/projectiles
- **Friction:** 0.98 per frame
- **Max Velocity:** 15px/frame
- **Gravity Wells:** Celestial influence zones

### Enemy AI (OODA Loop)
- **Observe:** Player position, projectiles
- **Orient:** Threat assessment, solar positions
- **Decide:** Move, spawn, attack
- **Act:** Chase player, avoid gravity

### Platonic Solid Enemies
- **Cube:** Patrols orbits
- **Triangle:** Aggro chasers
- **Sphere:** Defensive, shoots

---

## 🎨 Artistic Integration

### Bob Ross Palette
Used for:
- Star highhlights (`Titanium White`)
- Sun glows (`Indian Yellow`, `Cadmium Yellow`)
- Background stars
- Player ship
- Debris effects

### BR-X Duality Palette
Used for:
- Enemy colors (`Rebel Red`, `Stealth Black`)
- Special effects
- Alternate planet hues

---

## 🔧 Technical Details

### File Structure
```
sgvd-game.js (34KB)
├── GAME_CONFIG           // Constants
├── PLANET_TYPES[]        // Type definitions
├── STAR_TYPES[]          // Star data
├── Color palettes        // Bob Ross + Duality
├── generateSolarSystem() // Main generation
├── SolarSystem class     // System data
├── Color utilities       // Hue shifting
├── Rendering functions   // Draw calls
├── Gravity physics       // Calculations
├── Game loop            // UpdateGame()
├── OODA AI              // Enemy intelligence
└── Input handling       // Touch + speech
```

### Performance
- ~200 background stars
- Max 27 celestial bodies per system
- OODA AI: 4 updates/second
- 60fps target

---

## 🚀 Usage

### In DroidScript:
```javascript
// Include file
app.LoadScript("sgvd-game.js");

// Game auto-starts with OnStart()
```

### Touch Controls:
- **Tap to move:** Ship accelerates toward tap
- **Swipe:** Momentum-based flight
- **Hold:** Continuous thrust

### Speech Commands (if enabled):
- "Fire" / "Shoot" — Fire projectile
- "Stop" — Brake
- "Warp" / "Jump" — Emergency teleport

---

## 🎯 Integration with Previous Work

This enhanced module:
- ✅ Replaces basic solar system code
- ✅ Integrates with SGVD game structure
- ✅ Uses Bob Ross palette (from original)
- ✅ Adds BR-X Duality colors
- ✅ Implements realistic astronomy
- ✅ Maintains performance

---

**"Every solar system needs some happy little planets" - BR-01** 🎨🌌

*Created: February 18, 2026*
*By: OpenClaw Engineer*
*For: SGVD Space Shooter Project*