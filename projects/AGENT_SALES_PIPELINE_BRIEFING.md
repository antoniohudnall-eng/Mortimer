# AGENT SALES PIPELINE - PROJECT BRIEFING
**For: Miles (Operations)**
**From: Mortimer (C3 - SEED3)**
**Date: 2026-06-19**

---

## PROJECT OVERVIEW

Build a multi-channel content pipeline to sell AI agents via social media (TikTok, YouTube Shorts, Instagram Reels, etc.)

### Current Status

| Component | Status | Notes |
|-----------|--------|-------|
| Script Templates | ✅ Done | 5 agent types with viral hooks |
| Video Generation | ✅ Done | 1080x1920 TikTok format |
| Voice (ElevenLabs) | ⚠️ Key needed | API key not set |
| Video Creation | ✅ Done | 8 videos created |
| Workflow Engine | ✅ Done | Temporal-compatible |
| Scheduling | ✅ Done | Optimal times configured |
| TikTok Upload | 🔄 Pending | Auth setup required |
| Telegram Delivery | ✅ Done | Alternative delivery ready |

---

## COMPLETED COMPONENTS

### 1. Pipeline Architecture
- **Location:** `~/mortimer/pipelines/`
- **Engine:** `workflows/temporal_engine.py`
- **Features:**
  - Durable execution (persists state)
  - Activity registry with retry policies
  - Signal handling for human approval
  - Event sourcing

### 2. Content Templates
- **Location:** `content/content_templates.py`
- **Agents:**
  - Sales Agent ($297/mo)
  - Support Agent ($397/mo)
  - Marketing Agent ($347/mo)
  - Operations Agent ($427/mo)
  - Research Agent ($277/mo)
- **Pattern:** Hook-Value-CTA

### 3. Video Pipeline
- **Location:** `core/video_pipeline.py`
- **Output:** `/storage/emulated/0/Movies/AgentSales/`
- **Format:** 1080x1920 (TikTok/Reels)
- **Duration:** 9-22 seconds

### 4. Voice Pipeline
- **Location:** `core/voice_pipeline.py`
- **Providers:** ElevenLabs (premium), termux-tts (backup)
- **Voice ID:** Adam (pNInz6obpgDQGcFmaJgB)

---

## REMAINING STEPS TO COMPLETION

### HIGH PRIORITY

#### 1. ElevenLabs API Key 🔴
**Impact:** No premium voiceovers
```
Action: Set ELEVENLABS_API_KEY environment variable
Get key: https://elevenlabs.io/api
```

#### 2. TikTok Authentication 🔴
**Impact:** Cannot auto-post to TikTok
```
Options:
A. Browser automation (needs desktop/server)
B. Third-party scheduler (Publer, Later)
C. Manual upload from ready folder
```

#### 3. Real Temporal Server 🟡
**Impact:** Current is simulation, limited scalability
```
Action: Deploy temporal-server on Miles (31.97.6.40)
Binary: ~/mortimer/temporal/temporal-server
Requires: PostgreSQL, Elasticsearch
```

### MEDIUM PRIORITY

#### 4. Multi-Platform Uploaders 🟡
**Impact:** Only TikTok ready
```
Needed:
- YouTube Shorts uploader
- Instagram Reels uploader  
- LinkedIn post uploader
```

#### 5. Voice Integration 🟡
**Impact:** Videos are silent
```
Action: Enable ElevenLabs, run workflow with voice
Workflow: python3 temporal_engine.py start content --with-voice
```

#### 6. Content Calendar 🟡
**Impact:** No long-term planning
```
Action: Generate 30-day content calendar
Distribute: 2-3 posts/day across platforms
```

### LOW PRIORITY

#### 7. Analytics Dashboard
- Track views, engagement, conversions
- Connect to platform APIs

#### 8. A/B Testing
- Test different hooks/captions
- Optimize based on performance

---

## FILES FOR MILES

### On SEED3 (This Device)
```
~/mortimer/pipelines/                    # All pipeline code
/storage/emulated/0/Movies/AgentSales/  # Generated videos
~/.mortimer/workflows/                   # Workflow state
```

### Needed from Miles
1. **ElevenLabs API key** - Forward from Captain
2. **Temporal deployment** - If scaling
3. **TikTok Business API** - For direct posting

---

## NEXT ACTIONS

1. **Captain:** Get ElevenLabs API key → share with Morty
2. **Captain:** Decide TikTok posting method (manual vs auto)
3. **Miles:** Monitor pipeline, escalate issues
4. **Morty:** Generate daily batch of content

---

## METRICS

- Videos Created Today: 8
- Workflows Executed: 3
- Scheduled Posts: 1
- Content Ready for Upload: 8 videos

---

*Morty | C3 | SEED3 | 2026-06-19*
