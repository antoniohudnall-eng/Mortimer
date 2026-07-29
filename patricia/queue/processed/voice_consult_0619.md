# PATRICIA CONSULTATION - Voice Implementation

## Request
Update Agent Sales TikTok pipeline with:
- **Native voice PRIMARY** (termux-tts, espeak-ng)
- **ElevenLabs OPTIONAL** (premium backup)

## Questions for Patricia

1. **Voice Priority Logic**
   - If ElevenLabs key set → use ElevenLabs
   - If no key → fall back to native TTS
   - Correct?

2. **Native Voice Quality**
   - termux-tts-speak: Android native, natural
   - espeak-ng: Fast, robotic but consistent
   - Recommendation?

3. **Voice Settings**
   - Speed: 161 (φ ratio from wiki)
   - Pitch: 51
   - Any Patricia recommendations?

4. **Script Adaptation**
   - Native TTS reads differently than human
   - Should scripts be shorter/more direct?
   - Punctuation optimization?

5. **Performance**
   - termux-tts is async (non-blocking)
   - How to handle in Temporal workflow?
   - Background task vs sync?

## Files to Update
- temporal_workflows.py
- main.py

## Target
All 6 agent types should have working voice.
Captain notified via Telegram when complete.

