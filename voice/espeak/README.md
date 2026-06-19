# 🤖 ESPEAK VOICE MODULATION SYSTEM

**Location:** `~/mortimer/voice/espeak/`  
**Status:** ✅ OPERATIONAL  
**Platform:** Android/Termux (offline capable!)

---

## Voice Profiles

| Agent | Speed | Pitch | Variant | Description |
|-------|-------|-------|---------|-------------|
| **CLERK** | 130 | 85 | m1 | Professional, efficient |
| **GREET** | 110 | 110 | f3 | Friendly, welcoming |
| **PERSONAL** | 105 | 100 | f2 | Caring, thoughtful |
| **VELVET** | 115 | 90 | f1 | Smooth, premium |
| **CONCIERGE** | 100 | 95 | f4 | Attentive, 24/7 |
| **EXECUTIVE** | 125 | 75 | m2 | Deep, authoritative |

### Special Voices
| Voice | Description |
|-------|-------------|
| **robot** | Beep boop, robotic assistant |
| **whisper** | Intimate, whispered delivery |

---

## Usage

```bash
# Test a voice
python3 espeak_voices.py speak "Hello world" clerk

# Generate all samples
python3 espeak_voices.py generate

# List available voices
python3 espeak_voices.py list

# Test specific agent
python3 espeak_voices.py generate clerk
```

---

## Integration with TikTok Campaign

```bash
cd ~/mortimer/secretarial_pool/tiktok

# Generate espeak voiceovers
python3 espeak_tiktok.py campaigns/campaign_20260618.json

# Output: campaigns/audio_espeak/
```

---

## Generated Voice Files

```
output/
├── clerk_voice.wav
├── greet_voice.wav
├── personal_voice.wav
├── velvet_voice.wav
├── concierge_voice.wav
├── executive_voice.wav
├── robot_voice.wav
└── whisper_voice.wav
```

---

## API Usage

```python
from espeak_voices import espeak_speak, AGENT_VOICES

# Simple speak
espeak_speak("Hello world", output_file="hello.wav")

# With profile
profile = AGENT_VOICES["executive"]
espeak_speak("Ready for business", profile, "exec.wav")
```

---

## espeak Parameters

| Parameter | Range | Default | Effect |
|-----------|-------|---------|--------|
| `-s` speed | 80-200 | 130 | Words per minute |
| `-p` pitch | 0-200 | 100 | Voice pitch |
| `-a` amplitude | 0-200 | 100 | Volume |
| `-v` variant | m1-f4 | - | Voice variant |

---

*Built: 2026-06-18*
