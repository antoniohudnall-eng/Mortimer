# Golden Mean Voice Settings

## DroidScript (Original)
```
Speed = GM = 1.618
Pitch = PI / GM = 1.94
app.TextToSpeech("text", 1.618, 1.94)
```

## espeak (Applied)
```
-v en-us -s 161 -p 52 -a 100 -k 0
```

## Command
```bash
espeak -v en-us -s 161 -p 52 -a 100 -k 0 "text"
```
