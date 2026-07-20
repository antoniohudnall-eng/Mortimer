# Sweet Voice Settings

## DroidScript (Android) - THE SWEET VOICE
```javascript
const GM = 1.6180339887;
const PI = 3.1415926535;
app.TextToSpeech("Message", GM, PI / GM);
```

## espeak (Termux) - Best available
```
en-us -s 162 -p 52 -a 110 -k 0
```

## Status
- DroidScript: ✅ Sweet female voice
- espeak: ⚠️ Best we can do without +f1/+f2 variants
