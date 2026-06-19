# 🖥️ AGENT SALES TIKTOK - TEMPORAL COMPLETION STEPS

**Captain's Directive:** These are the steps I follow to completion using Temporal.

---

## THE PLAN

### Step 1: Set ElevenLabs API Key
- [ ] Captain provides ElevenLabs API key
- [ ] I verify connection
- [ ] Voice generation enabled

### Step 2: Temporal Server Deployment (Miles)
- [ ] Miles deploys `temporal-server` on 31.97.6.40
- [ ] PostgreSQL + Elasticsearch configured
- [ ] Worker connects to SEED3

### Step 3: Define Temporal Workflows
```python
# Workflows to implement:
1. GenerateAgentContent  → script → voice → video
2. BatchAgentContent    → fan-out GenerateAgentContent
3. PublishToTikTok      → human approval → upload
4. DailyContentCalendar  → 7-day schedule
```

### Step 4: Activity Functions
```python
# Activities:
- generate_script(agent_type)     → viral hook + value prop
- create_voiceover(text)          → ElevenLabs API
- render_video(slides, audio)     → FFmpeg
- generate_caption(agent)        → hashtags + CTA
- upload_to_tiktok(video, cap)   → TikAPI/Manual
- send_notification(msg)         → Telegram to Captain
```

### Step 5: Retry Policies
```python
generate_script:    retry 3x, backoff 1s
create_voiceover:   retry 5x, backoff 2s (API dependent)
render_video:       retry 3x, backoff 1s
upload_to_tiktok:   retry 3x, backoff 5s
```

### Step 6: Signals (Human-in-Loop)
```python
Signal: HumanApproval    → pause before upload
Signal: ContentRevision   → regenerate script
Signal: ImmediatePost     → bypass approval
```

### Step 7: Queries
```python
Query: status            → current workflow state
Query: progress          → % complete
Query: video_urls        → list of generated videos
Query: scheduled_posts   → calendar view
```

### Step 8: Daily Automation
```bash
# Cron: Every 6 hours
temporal workflow execute GenerateDailyBatch
  - 5 videos per batch
  - Rotate through 6 agent types
  - Send to Captain via Telegram
```

---

## TEMPORAL WORKFLOW DEFINITIONS

### Workflow 1: GenerateAgentContent
```
Input:  agent_type, length, voice_enabled
Output: video_path, caption, script

Activities:
  1. generate_script(agent_type)     → script
  2. create_voiceover(script)        → audio (if enabled)
  3. render_video(script, audio)     → video
  4. generate_caption(script)        → caption
  5. send_notification("Video ready") → Telegram

Signals:
  - ContentRevision: regenerate script
```

### Workflow 2: BatchAgentContent
```
Input:  count, agent_types[], voice_enabled
Output: videos[], report

Pattern: Fan-out/Fan-in
  - Spawn count child workflows
  - Each child: GenerateAgentContent
  - Aggregate results
  - Generate batch report
```

### Workflow 3: DailyContentCalendar
```
Input:  days, posts_per_day
Output: schedule[]

Activities:
  1. create_content_calendar(days, posts_per_day)
  2. For each slot: schedule_post(video, time, platforms)
  3. send_calendar_to_telegram(schedule)
```

### Workflow 4: PublishToTikTok
```
Input:  video_path, caption, require_approval
Output: post_url, status

Signals:
  - HumanApproval → proceed with post
  - Reject        → mark failed, notify

Activities:
  1. validate_video(video_path)
  2. upload_to_tiktok(video, caption) [retry 3x]
  3. send_notification(f"Posted: {url}")
```

---

## EXECUTION STEPS

### Hour 0: Setup
- [ ] Deploy Temporal server (Miles)
- [ ] Set ELEVENLABS_API_KEY (Captain)
- [ ] Verify all connections

### Hour 1: Worker Registration
- [ ] Register activities on SEED3
- [ ] Connect worker to Temporal
- [ ] Test single workflow

### Hour 2: Batch Test
- [ ] Run BatchAgentContent(10)
- [ ] Verify 10 videos created
- [ ] Check voiceovers

### Hour 3: Approval Flow
- [ ] Test PublishToTikTok with approval
- [ ] Send to Captain for sign-off
- [ ] Captain sends approval signal

### Hour 4: Daily Automation
- [ ] Setup cron: every 6 hours
- [ ] Create 7-day calendar
- [ ] First automated batch

### Ongoing: Monitor & Optimize
- [ ] Daily batch at 06:00, 12:00, 18:00 UTC
- [ ] Captain reviews queue
- [ ] Signal approval for posting
- [ ] Track metrics

---

## TEMPORAL CLI COMMANDS

```bash
# Start worker
temporal workflow run \
  --task-queue agent-sales \
  --type GenerateAgentContent

# Execute workflow
temporal workflow execute \
  --task-queue agent-sales \
  --type BatchAgentContent \
  --input '{"count": 5}'

# Query status
temporal workflow query \
  --workflow-id ID \
  --query-type progress

# Send signal
temporal workflow signal \
  --workflow-id ID \
  --signal-name HumanApproval \
  --input '{}'
```

---

## SUCCESS METRICS

| Metric | Target |
|--------|--------|
| Videos per day | 15-20 |
| Voice覆盖率 | 100% |
| Post rate | 5-7/day |
| Manual effort | < 5 min/day |
| Engagement | Track via TikTok |

---

*Morty follows these steps to completion. Captain approves. Miles deploys. We ship.*
