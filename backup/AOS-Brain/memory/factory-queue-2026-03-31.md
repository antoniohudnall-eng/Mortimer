# Dark Factory Production Queue
## Queued: 2026-03-31 06:28 UTC

---

## ORDER: DF-20260331-CREAM-001
**Product:** Cream Mobile App  
**Quantity:** 1 production build  
**Source:** `/root/.openclaw/workspace/Cream/`  
**Type:** Android APK + iOS IPA  
**Priority:** HIGH  
**Estimated Timeline:** 48-72 hours  

### Build Requirements
- Android SDK 34
- Gradle 8.x
- Flutter/Dart (if Flutter app)
- Or React Native toolchain
- Keystore for signing

### Components Found
- `/mobile-android/` - Android source
- `/mobile-ios/` - iOS source  
- `/src/` - Shared components
- `/tests/` - Test suite

### Status: ⏳ QUEUED (System load managed)

---

## ORDER: DF-20260331-REGGIE-001
**Product:** ReggieStarr Android App  
**Quantity:** 1 production build  
**Source:** `/root/.openclaw/workspace/aocros/projects/ReggieStarr/`  
**Type:** Android APK (Bitgert wallet integration)  
**Priority:** HIGH  
**Estimated Timeline:** 36-48 hours  

### Build Requirements
- Android SDK 34
- Bitgert API integration
- Wallet functionality
- Gradle 8.x
- Keystore for signing

### Components Found
- `/android/app/src/main/java/com/performancesupply/reggiestarr/` - Main source
- Bitgert API endpoints configured
- Wallet integration layer

### Status: ⏳ QUEUED (System load managed)

---

## ORDER: DF-20260408-NOGNOG-001
**Product:** N'og nog v3 - Universal Explorer  
**Quantity:** 1 production build  
**Source:** `/root/.openclaw/workspace/nognog/v3/`  
**Type:** Web Game (HTML5/Three.js) → Mobile APK + Desktop PWA  
**Priority:** HIGH  
**Estimated Timeline:** 24-36 hours  
**Issue:** Stars not rendering (black screen on load)  

### Build Requirements
- Three.js r128 bundled
- WebGL 2.0 support detection
- Mobile touch optimization
- APK wrapper (Cordova/Capacitor)
- PWA manifest for desktop

### Components Found
- `/v3/index.html` - Main game entry
- `/v3/js/core/` - Platform detection, Game loop
- `/v3/js/universe/` - Galaxy generation, Star field
- `/v3/js/player/` - Player controller
- `/game/` - Legacy v1 (reference)

### Status: ⏳ QUEUED (Pending star rendering fix)

### Notes from Captain
- Stars not visible on load (black screen)
- Taking photos to diagnose
- Likely BufferGeometry/PointsMaterial sizing issue
- Camera positioning or sizeAttenuation problem

---

## System Load Management
**Current Status:**  
- Brain: 548,925 nodes, growing  
- CPU: Moderate  
- Ollama: 6 models loaded  
- Minecraft: Active  
- Roblox Bridge: Active  

**Factory Strategy:** Stagger builds to prevent resource contention  
1. ReggieStarr first (smaller, 36h)  
2. Cream second (larger, 72h)  

---

## Next Actions
- [ ] Validate source code completeness
- [ ] Configure signing keystores
- [ ] Initiate build pipeline (ReggieStarr)
- [ ] Post-build: APK/IPA distribution setup

**Queued By:** Captain  
**Factory Manager:** Miles-Brain  
