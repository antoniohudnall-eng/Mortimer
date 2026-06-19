# 🎬 Agent Sales TikTok Pipeline

## Voice Configuration

| Provider | Status | Role |
|----------|--------|------|
| **espeak-ng** | ✅ ACTIVE | PRIMARY (native) |
| **ElevenLabs** | ⏸️ STANDBY | No credits |

ElevenLabs key is stored but has no credits. Using native espeak-ng only.

## Usage

```bash
cd ~/mortimer/agent-sales-tiktok

# Generate single video
python3 temporal_workflows.py gen clerk

# Generate all 6 agents
python3 temporal_workflows.py all

# Batch generate
python3 temporal_workflows.py batch 10
```

## Agents

| Agent | Price | Tagline |
|-------|-------|---------|
| CLERK | $97/mo | Handles emails 24/7 |
| GREET | $147/mo | Professional receptionist |
| PERSONAL | $197/mo | Your AI life manager |
| VELVET | $247/mo | Premium assistant |
| CONCIERGE | $297/mo | 24/7 VIP support |
| EXECUTIVE | $497/mo | C-suite coordination |

## Videos

Output: `/storage/emulated/0/Movies/AgentSales/`

Format: 1080x1920 (TikTok/Reels)
Voice: espeak-ng (native)

## Temporal Steps

See `TEMPORAL_STEPS.md` for completion roadmap.
