# VOICE SETTINGS — DO NOT LOSE

## Primary Voice (Android)
```bash
termux-tts-speak "text here"
```

## Premium Voice (ElevenLabs)
```bash
source /data/data/com.termux/files/home/mortimer/voice/config.sh
export ELEVENLABS_API_KEY=your_key
python3 /data/data/com.termux/files/home/mortimer/voice/speak.py "text here"
```

## Voice ID Options (ElevenLabs)
- Adam: `pNInz6obpgDQGcFmaJgB` (C3P0's voice)
- Antoni: `ErXwobYiHyaRYGkd4X9r`
- Rachel: `21m00Tcm4TlvDq8ikWAM`

## Services to Start
```bash
# PulseAudio
pulseaudio --start --exit-idle-time=-1

# Termux API (for termux-tts-speak)
termux-api-start
```

## Scripts
- `speak_free.py` — Android espeak + paplay
- `speak.py` — ElevenLabs premium
- `conversation_mode.sh` — Full voice chat mode
- `start_conversation.sh` — Activate voice chat

---

*Settings preserved: 2026-06-18*
*Morty speaks with the Android voice. Always.*
