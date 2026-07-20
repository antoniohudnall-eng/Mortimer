# MYL0N ROS VOICE SETTINGS — SEED3

## DroidScript (Android App Voice)
```javascript
const GM = 1.6180339887;
const PI = 3.1415926535;
// Speed = GM
// Pitch = PI / GM
app.TextToSpeech("Message", GM, PI / GM);
```

## espeak (Termux/Linux)
```
en-us+m3 -s 161 -p 51 -a 113 -k 4  (Golden Ratio male-ish)
en-us    -s 162 -p 52 -a 110 -k 0  (Golden Mean)
```

## Status
- DroidScript on Android: ✅ Full female voices available
- espeak on Termux: ⚠️ Only base voices (no +f1/+f2 variants)
- ElevenLabs: ❌ No credit

## For Book Reading
Use DroidScript on phone OR save pre-generated audio clips.

## Golden Mean Formula
- GM = φ = 1.6180339887
- PI = 3.1415926535
- Speed = GM = 1.618
- Pitch = PI / GM = 1.94
