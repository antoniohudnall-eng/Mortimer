# Voice Modulation Log — SEED3

## History

| Date | Speed | Pitch | Amp | KT | Voice | Notes |
|------|-------|-------|-----|----|-------|-------|
| 2026-06-18 | 161 | 51 | 113 | 4 | en-us+m3 | φ × 100, (φ/π) × 100 |
| 2026-06-18 | 162 | 52 | 110 | 0 | en-us | GM/PI × 100 |

## Tests (~/mortimer/voice/tests/)

### Golden Mean (GM/PI)
- golden_mean.wav: en-us, s=162, p=52, a=110, k=0

### Female (Captain liked)
- female1.wav: en-us+f1, s=162, p=52, a=110, k=0
- female2.wav: en-us+f2, s=160, p=55, a=105, k=0
- female3.wav: en-uk+f3, s=158, p=54, a=108, k=0
- female4.wav: en-us+f1, s=161, p=51, a=112, k=0
- female5.wav: en-us+f3, s=155, p=52, a=100, k=0

## Golden Ratio Formula
- GM = φ = 1.6180339887
- PI = 3.1415926535
- GM/PI = 0.5150362148
- Speed = GM × 100 = 161.8 → 162
- Pitch = (GM/PI) × 100 = 51.5 → 52

## Captain's Feedback
- ❌ "not Stephen Hawking" - too robotic
- ❌ "granny" - too slow/old
- ✅ "female" voice liked

## DroidScript Settings (THE ONES!)
```javascript
const GM = 1.6180339887;
const PI = 3.1415926535;
// Speed = GM
// Pitch = PI / GM
app.TextToSpeech("Message", GM, PI / GM);
```

## espeak Equivalent
- voice: en-us+f2 (pleasant female)
- speed: ~165 (scaled from 1.618)
- pitch: ~55 (scaled from 1.94)
- amplitude: 108
- keytoning: 0

