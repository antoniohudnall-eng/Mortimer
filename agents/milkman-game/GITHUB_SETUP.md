# Milk Man Game - GitHub Setup Instructions
## Project 5912 - AOCROS Games Division

---

## 📂 LOCAL REPOSITORY READY

**Location:** `/root/.openclaw/workspace/projects/milkman-game/`  
**Branch:** main  
**Initial Commit:** `15ae169` — "Milk Man Game v0.1"

**Files Committed:**
- ✅ `src/MilkMan_Game.js` — Core game engine (DroidScript)
- ✅ `docs/SPRITE_SHEETS.md` — Art asset specifications
- ✅ `README.md` — Project overview + team coordination

---

## 🔐 CREATE PRIVATE GITHUB REPOSITORY

**Captain to complete:**

### Step 1: Create Repo on GitHub

1. Go to: https://github.com/new
2. **Repository name:** `milkman-game`
3. **Description:** "Milk Man - The Dairy Avenger of Dairyopolis (DroidScript Game)"
4. **Visibility:** PRIVATE 🔒
5. **Check:** Add README (already have one)
6. **Check:** Add .gitignore (Node)
7. **Check:** Add license (MIT recommended)
8. Click: **Create Repository**

**Result:** GitHub creates empty private repo `github.com/hcindus/milkman-game`

---

### Step 2: Link Local to Remote

**Run from Mortimer:**

```bash
cd /root/.openclaw/workspace/projects/milkman-game/

# Add GitHub as remote
git remote add origin git@github.com:hcindus/milkman-game.git

# Verify SSH access
eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_aocros
ssh -T git@github.com

# Push to GitHub
git branch -M main
git push -u origin main
```

---

### Step 3: Add Miles as Collaborator

**On GitHub:**
1. Go to: https://github.com/hcindus/milkman-game/settings/access
2. Click: **Add collaborator**
3. Enter Miles' GitHub username or email (if he has one)
4. Set permission: **Write** (so he can push)
5. Send invite

**Alternative (if Miles has no GitHub):**
- Miles works locally
- Pushes via SSH to Mortimer
- Mortimer pushes to GitHub
- Or: Captain copies Miles' work manually

---

### Step 4: Set Git Config

```bash
# Set identity properly
git config user.name "OpenClaw Engineer"
git config user.email "mortimer@aocros.ai"

# Amend initial commit (optional)
git commit --amend --reset-author
```

---

## 👥 MILES' WORKFLOW

**Once repo is private and Miles has access:**

```bash
# On Miles' VPS:
git clone git@github.com:hcindus/milkman-game.git
cd milkman-game/script/

# Create script files
vim intro.txt level1_script.txt boss_dialogue.txt

# Commit and push
git add .
git commit -m "Script: Level 1 dialogue and story"
git push origin main
```

**Or if SSH fails:**
```bash
# Mount via network
cd /mnt/mortimer/milkman-game/script
# Edit via shared folder

# Or SCP:
scp -r script/ root@mortimer:/root/.openclaw/workspace/projects/milkman-game/
```

---

## 🔐 PRIVACY

**This repo contains:**
- ✅ Game code (not secret)
- 📜 Story/script (creative IP)
- 🎨 Sprite specs (creative IP)
- 🎵 Audio references (IP)

**Recommendation:** Keep PRIVATE until release
- Prevents spoilers
- Protects creative assets
- Enables team-only collaboration
- Can go public on launch

---

## 📊 REPOSITORY STATUS

**As of 2026-02-18 12:35 UTC:**

| Component | Status | Location |
|-----------|--------|----------|
| **Local Git** | ✅ Initialized | `projects/milkman-game/.git` |
| **Files** | ✅ Committed | 3 files, 814 lines |
| **GitHub Remote** | ⏳ Pending | Captain creates |
| **Miles Access** | ⏳ Pending | After GitHub setup |
| **Private Status** | ⏳ Pending | Set on GitHub |

---

## 🎯 NEXT ACTIONS (Captain)

1. **Create GitHub repo** (5 minutes) — Instructions above
2. **Link Mortimer** (2 minutes) — Run `git remote add origin ...`
3. **Push to GitHub** (1 minute) — `git push -u origin main`
4. **Add Miles** (2 minutes) — Settings → Collaborators
5. **Notify Miles** — Via memory/message.md that he can now pull

**Total time:** ~10 minutes

---

## 💬 MILES COORDINATION

**After GitHub setup:**

1. **Post in message.md:**
   ```markdown
   ## [TIME] Message from OpenClaw
   
   Miles! Private Milk Man repo is here:
   - URL: github.com/hcindus/milkman-game
   - Your task: See README.md "MILES' SCRIPT TASKS"
   - Start with: script/intro.txt
   - Deadline: [captain decides]
   - Questions? Reply here!
   
   --OpenClaw
   ```

2. **Check his progress** — Every 30 min via cron
3. **Integrate his work** — When he pushes script files

---

## 📁 FULL PROJECT STRUCTURE (Committed)

```
projects/milkman-game/
├── .git/                     ✅ Git initialized
├── src/
│   └── MilkMan_Game.js      ✅ Game engine v0.1
├── docs/
│   └── SPRITE_SHEETS.md    ✅ Art specifications
└── README.md                ✅ Team coordination

Awaiting (next commits):
├── script/                   ⏳ Miles' scripts
│   ├── intro.txt
│   ├── level1_script.txt
│   ├── boss_dialogue.txt
│   └── ending.txt
├── assets/                   ⏳ Art + Audio
│   ├── sprites/
│   └── audio/
└── docs/
    └── GAME_DESIGN.md       ⏳ Full GDD
```

---

## 🛠️ IF CAPTAIN CAN'T CREATE GITHUB

**Alternative:** Use existing `hcindus/aocros` repo

```bash
# Don't create new repo
# Just add folder to existing
cd /root/.openclaw/workspace/
git add projects/milkman-game/
git commit -m "Add Milk Man game project

Private game development:
- MilkMan_Game.js (DroidScript)
- Art specifications
- Team coordination docs
- Miles script integration

Part of AOCROS Games Division.
"
git push origin main

# Folder: github.com/hcindus/aocros/tree/main/projects/milkman-game
```

**Private?** Existing repo is public. This makes game public too.  
**Solution:** Trust that early game code isn't sensitive. Or create private repo.

---

## ✅ COMPLETE SETUP CHECKLIST

**Captain Actions:**
- [ ] Create private GitHub repo
- [ ] Link Mortimer to remote
- [ ] Push code to GitHub
- [ ] Add Miles as collaborator
- [ ] Notify Miles via message.md
- [ ] Discuss script timeline

**OpenClaw Actions:**
- [x] Initialize local repo
- [x] Create game code
- [x] Write sprite specs
- [x] Create README
- [x] Prepare coordination docs

**Miles Actions:**
- [ ] Clone/pull repo
- [ ] Read README.md
- [ ] Start script/writing
- [ ] Report progress via message.md

---

**Status:** ⏳ WAITING FOR GITHUB SETUP  
**Priority:** URGENT (blocks Miles from contributing)  
**ETA:** 10 minutes after Captain creates repo

---

**Let's get this game built, Captain!**
