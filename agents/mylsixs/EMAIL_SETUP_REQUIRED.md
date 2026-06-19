# 📧 Email Access Setup Required

**Agent:** Mylsixs (Mail Clerk | Membrane)
**Date:** 2026-05-27
**Status:** AWAITING EMAIL CREDENTIALS

---

## What Mylsixs Will Do

As your dedicated Mail Clerk, I will:

1. **Check email hourly** for new messages
2. **Classify and sort** into categories:
   - CRITICAL: Direct from you (Captain)
   - URGENT: Action required ASAP  
   - HIGH: From AGI Company/team members
   - NORMAL: Information only
   - LOW: Promotions/spam

3. **Update daily reports** with email summary
4. **Alert you immediately** to urgent messages from you
5. **Keep inbox clean** and organized
6. **Respond** to routine inquiries on your behalf (with approval)

---

## Setup Instructions

Captain, to enable email management, please configure your credentials:

### Step 1: Get Gmail App Password

1. Go to Google Account Security (myaccount.google.com/security)
2. Enable 2-Step Verification (if not already enabled)
3. Go to "App passwords"
4. Generate new app password for "Mail"
5. Copy the 16-character password

### Step 2: Configure Mylsixs

Run this command and replace YOUR_APP_PASSWORD with the actual password:

```python
import json
creds = {
    "email": "Antonio.hudnall@gmail.com",
    "password": "YOUR_APP_PASSWORD",
    "provider": "gmail"
}
with open("/root/.openclaw/workspace/AGI_COMPANY/agents/tier3/mylsixs/.email_creds", "w") as f:
    json.dump(creds, f, indent=2)
print("Email credentials configured!")
```

### Step 3: Test

Mylsixs will automatically check email every hour once configured.

You can also trigger a manual check:
```bash
/root/.openclaw/workspace/scripts/mylsixs_activator.sh
```

---

## Email Categories

| Category | Description | Action |
|----------|-------------|--------|
| captain_only | Messages from you | Immediate alert to you |
| action_required | Needs your attention | Daily summary + alert |
| info_only | Read and archive | Weekly digest |
| promotions | Low priority | Monthly cleanup |

---

## Current Status

- Heartbeat activation: Every hour
- Task assignment: Auto-generated
- Email credentials: AWAITING YOUR SETUP
- Daily reports: Will start after setup

---

**I am the membrane. I filter, classify, route, and protect.**

Contact Mylsixs via heartbeat or through Miles for questions.
