# 🎙️ Agent Sales Pipeline

Multi-channel content pipeline for selling AI agents on social media.

## Structure

```
pipelines/
├── core/                   # Core modules
│   ├── voice_pipeline.py  # Voice generation (ElevenLabs/termux-tts)
│   └── video_pipeline.py  # Video creation with FFmpeg
├── content/               # Content templates
│   └── content_templates.py
├── platforms/             # Platform-specific uploaders
│   └── tiktok_uploader.py
├── scheduler/             # Scheduling system
│   ├── scheduler.py
│   └── upload_scheduler.py
├── agent_sales_pipeline.py # Main orchestrator
└── run_pipeline.py        # Quick start
```

## Quick Start

```bash
cd ~/mortimer/pipelines

# See what's available
python3 agent_sales_pipeline.py list

# Create a promo video
python3 agent_sales_pipeline.py create --agent sales

# Create 5 promos
python3 agent_sales_pipeline.py batch --count 5

# Voice only
python3 agent_sales_pipeline.py voice --agent support
```

## Available Agents

| Type | Name | Price | Tagline |
|------|------|-------|---------|
| sales | Sales Agent | $297/mo | Closes deals while you rest |
| support | Support Agent | $397/mo | Your 24/7 customer service team |
| marketing | Marketing Agent | $347/mo | Your content machine never stops |
| operations | Operations Agent | $427/mo | Runs your business like clockwork |
| research | Research Agent | $277/mo | Knows everything about your market |

## Platforms

- ✅ TikTok
- 🔄 YouTube Shorts
- 🔄 Instagram Reels
- 🔄 Twitter
- 🔄 LinkedIn
- 🔄 Facebook

## Requirements

- FFmpeg
- Python 3.8+
- Pillow
- ElevenLabs API key (optional, for premium voice)

## Environment

```bash
export ELEVENLABS_API_KEY=your_key_here
```

## Output

Videos saved to: `/storage/emulated/0/Movies/AgentSales/`
