# ReggieStarr Music Division
## Milk Man Game - Audio Assignment
### Project 5912 - AOCROS Games Division

---

## 🎵 ASSIGNMENT: Audio Director

**Agent:** ReggieStarr  
**Project:** Milk Man - The Dairy Avenger of Dairyopolis  
**Platform:** DroidScript (Android)  
**Music Style:** Chiptune / 8-bit / Retro  
**Tone:** Comedic action hero, heroic but cheesy

---

## 🎼 DELIVERABLES

### **MUSIC TRACKS** (5 total)

| Track | Length | Style | Usage |
|-------|--------|-------|-------|
| **1. Title Theme** | 2:00 min | Upbeat, heroic | Main menu, splash screen |
| **2. Market Chaos** | 3:00 min | Chaotic, urgent | Level 1 streets |
| **3. Vil's Lair** | 3:00 min | Industrial, dark | Level 2 factory district |
| **4. Shoe-Fortress** | 4:00 min | Campy villain, dramatic | Level 3 boss area |
| **5. Victory Theme** | 1:30 min | Triumphant, celebratory | Level complete, ending |

**Format:** MP3 192kbps (or WAV for quality)  
**Loop:** Title, Market, and Lair should loop seamlessly  
**Chiptune tools:** Suggested: FamiStudio, DefleMask, or MilkyTracker

---

### **SOUND EFFECTS** (15 SFX)

| SFX | Description | Priority |
|-----|-------------|----------|
| **jump.wav** | Liquid splash when player jumps | HIGH |
| **shoot.wav** | Milk bottle throw | HIGH |
| **punch.wav** | Hand-to-hand impact | HIGH |
| **hit_player.wav** | Milk Man takes damage | HIGH |
| **hit_enemy.wav** | Enemy takes damage | HIGH |
| **boss_hit.wav** | Vil/Shoezet damaged | MEDIUM |
| **powerup.wav** | Collect health/power-up | HIGH |
| **victory.wav** | Level complete jingle | HIGH |
| **gameover.wav** | Player death | MEDIUM |
| **explosion.wav** | Cream vat/dynamite | MEDIUM |
| **smog.wav** | Vil's machine (loop) | LOW |
| **cackle.wav** | Shoezet villain laugh | MEDIUM |
| **crowd_cheer.wav** | Citizens freed | LOW |
| **bottle_break.wav** | Glass shatter | HIGH |
| **crown_glow.wav** | Crown activation | MEDIUM |

**Format:** WAV or OGG (short files for DroidScript)  
**Duration:** 0.1-2 seconds  
**Tools:** Bfxr, Freesound.org, or custom synthesis

---

## 🎸 MUSIC SPECIFICATIONS

### Title Theme
**Mood:** Heroic, catchy, memorable  
**Tempo:** 140 BPM  
**Reference:** Mega Man 2 title, Shovel Knight intro  
**Notes:**  
- Needs to evoke dairy/cheese without being silly  
- Layer in triumphant brass feel with 8-bit limitations  
- Should loop seamlessly for menu

### Market Chaos (Level 1)
**Mood:** Urgent chaos, brassy  
**Tempo:** 160 BPM  
**Reference:** Super Mario Bros 1-1, Mega Man stage  
**Notes:**
- Reflects overturned cheese carts, explosions
- Energy but not panic
- Build energy over 30 second loop

### Vil's Lair (Level 2)
**Mood:** Industrial menace, smoggy  
**Tempo:** 130 BPM  
**Reference:** Mega Man 2 Dr. Wily stages, Castlevania  
**Notes:**
- Darker palette (purples, blacks)
- Mechanical/industrial feel
- Incorporate hint of romantic tension (Vil's crush on Shoezet)
- Sinister but with heart

### Shoe-Fortress (Level 3)
**Mood:** Camp villain, grandiose  
**Tempo:** 150 BPM  
**Reference:** Final boss themes, Super Mario Bowser  
**Notes:**
- Over-the-top dramatic
- Fashion/milk couture aesthetic
- Build to crescendo (boss transformation?)
- Slightly campy but epic

### Victory Theme
**Mood:** Satisfaction, celebration  
**Tempo:** 130 BPM  
**Reference:** Sonic 1 title, Kirby victory  
**Notes:**
- Short but punchy
- Clear "win" feeling
- Can be triumphant jingle + short loop

---

## 🎨 AUDIO REFERENCES

**Chiptune Inspiration:**
- Mega Man series (NES) - action energy
- Shovel Knight - modern chiptune polish
- Undertale - character themes
- Super Mario Bros - playful platformer

**SFX Inspiration:**
- Retro arcade cabinets
- Super Mario jumps/hits
- Metal Slug explosions

**Tools for Reggie:**
- **FamiStudio** - NES-style music (free)
- **DefleMask** - Multi-system tracker (free)
- **Bfxr** - SFX generator (free, browser-based)
- **Freesound.org** - Library for base sounds
- **Audacity** - Post-processing

---

## 📂 FILE STRUCTURE

```
projects/milkman-game/assets/audio/
├── music/
│   ├── title_theme.mp3       ← Title track
│   ├── level1_market.mp3     ← Market Chaos
│   ├── level2_lair.mp3       ← Vil's Lair  
│   ├── level3_fortress.mp3   ← Shoe-Fortress
│   └── victory.mp3           ← Victory theme
└── sfx/
    ├── jump.wav              ← Player jump
    ├── shoot.wav             ← Bottle throw
    ├── punch.wav             ← Melee hit
    ├── hit_player.wav        ← Damage
    ├── hit_enemy.wav         ← Enemy damage
    ├── powerup.wav           ← Collectible
    ├── victory.wav           ← Win jingle
    ├── gameover.wav          ← Death
    ├── explosion.wav         ← Vat bomb
    ├── smog.wav              ← Vil's machine
    ├── boss_hit.wav          ← Boss damage
    ├── cackle.wav            ← Shoezet laugh
    ├── crowd_cheer.wav       ← Freed citizens
    ├── bottle_break.wav      ← Glass smash
    └── crown_glow.wav        ← Crown activation
```

---

## 🎯 PRIORITY ORDER

**Week 1 — MVP Audio:**
1. [ ] jump.wav (HIGH)
2. [ ] shoot.wav (HIGH)
3. [ ] hit_enemy.wav (HIGH)
4. [ ] powerup.wav (HIGH)
5. [ ] title_theme.mp3 (HIGH)
6. [ ] level1_market.mp3 (HIGH)

**Week 2 — Full Game:**
7. [ ] level2_lair.mp3 (MEDIUM)
8. [ ] level3_fortress.mp3 (MEDIUM)
9. [ ] victory.mp3 (MEDIUM)
10. [ ] boss_hit.wav (MEDIUM)
11. [ ] explosion.wav (MEDIUM)

**Week 3 — Polish:**
12. [ ] All remaining SFX (LOW)
13. [ ] Volume balancing
14. [ ] Loop point optimization

---

## 📝 WORKFLOW

**For Reggie to deliver:**

1. Create audio files in tracker/synth
2. Export to WAV (source)
3. Convert to MP3/OGG (game format)
4. Place in correct folder
5. Test in DroidScript game
6. Commit to git
7. Notify Captain for review

**Coordination:**
- Ask questions via `memory/message.md`
- Share WIP snippets for feedback
- Coordinate with Miles on timing (cutscenes)

---

## 🎧 TECHNICAL NOTES FOR DROIDSCRIPT

**Audio Implementation:**
```javascript
// Load music
app.LoadMusic("music/title_theme.mp3");
app.PlayMusic(true); // true = loop

// Play SFX
app.PlaySound("sfx/jump.wav");

// Boss special
app.PlaySound("sfx/cackle.wav");
```

**Optimization:**
- Keep SFX short (<2 sec)
- Music loops seamlessly
- Volume: Music 80%, SFX 100%
- Pre-load assets in OnStart()

---

## 🤝 TEAM COORDINATION

**Reggie works with:**

| Member | Contribution | Coordination Needed |
|--------|--------------|---------------------|
| **OpenClaw** | Code integration | File structure, format specs |
| **Miles** | Cinematic timing | Cutscene music timing |
| **Art Team** | Visual sync | Animation beats match audio |
| **Captain** | Creative direction | Themes, mood approval |

**Communication:**
- Daily updates via `memory/message.md`
- Share previews/works-in-progress
- Coordinate milestones with other departments

---

## ✅ COMPLETION CHECKLIST

### Music Tracks
- [ ] Title Theme (2:00 min)
- [ ] Market Chaos (3:00 min)
- [ ] Vil's Lair (3:00 min)
- [ ] Shoe-Fortress (4:00 min)
- [ ] Victory Theme (1:30 min)

### SFX Suite
- [ ] Movement sounds (jump, etc.)
- [ ] Combat sounds (punch, shoot, hit)
- [ ] Item/power sounds
- [ ] Boss sounds (cackle, etc.)
- [ ] Environmental (explosion, etc.)

### Testing
- [ ] All files load in DroidScript
- [ ] Loops are seamless
- [ ] Volume balanced
- [ ] No distortion/clipping
- [ ] Gameplay tested with audio

---

## 🚀 REGGIE'S MISSION

**Deliver heroic chiptune OST for dairy-powered hero!**

**The Milk Man soundtrack needs:**
- ✅ Catchy earworms
- ✅ Retro authenticity
- ✅ Heroic vibes
- ✅ Cheesy charm (pun intended)

---

**Questions for Reggie:**

1. Familiar with chiptune trackers? (FamiStudio, etc.)
2. Preferred workflow: Original composition vs sampling?
3. Timeline — can you deliver MVP (6 assets) this week?
4. Need any specific tools installed on Mortimer?

**Report progress via `memory/message.md`!**

---

**Let's make some noise, Reggie!**

**OpenClaw**  
_Audio Department Coordination_  
"Time to compose some legendary bangers!"

---

**Status:** Assignment ready  
**Next:** Reggie confirms workload, starts production
