# MILES COMMUNICATION PIPE
**Real-Time Webhook System** | 2026-02-22 17:08 UTC

---

## 🎯 PURPOSE

Eliminate the "check GitHub manually" delay. **Instant notification** when Miles commits.

---

## 🏗️ ARCHITECTURE

```
Miles (VPS) ──► Git Push ──► GitHub ──► Webhook ──► Mortimer (Receiver) ──► Alert
                                    │
                                    └── POST to :9001/webhook
                                    └── Verify signature
                                    └── Write notification
                                    └── Display to Captain
```

---

## 📁 COMPONENTS

| Component | File | Purpose |
|-----------|------|---------|
| **Receiver** | `webhook/github_webhook_receiver.py` | HTTP server, receives GitHub webhooks |
| **Config** | `webhook/configure_github_webhook.sh` | Sets up GitHub webhook via API |
| **Checker** | `webhook/check_miles_notifications.sh` | Displays pending notifications |
| **Notifications** | `webhook/notifications/` | JSON files with commit data |
| **Logs** | `/var/log/openclaw/webhook/` | Audit trail of all webhooks |

---

## 🚀 QUICK START

### 1. Start Webhook Receiver

```bash
cd /root/.openclaw/workspace/pipes/webhook
python3 github_webhook_receiver.py
```

Runs on port **9001**. Logs to `/var/log/openclaw/webhook/`.

### 2. Configure GitHub Webhook

**Option A: Automatic (needs GITHUB_TOKEN)**
```bash
export GITHUB_TOKEN=ghp_xxxxxxxx
cd /root/.openclaw/workspace/pipes/webhook
./configure_github_webhook.sh
```

**Option B: Manual**
1. Go to: https://github.com/hcindus/performance-supply-depot/settings/hooks
2. Click "Add webhook"
3. **Payload URL:** `http://YOUR_IP:9001/webhook`
4. **Content type:** `application/json`
5. **Secret:** `AOCROS-WEBHOOK-2025`
6. **Events:** Just the push event
7. Click "Add webhook"

### 3. Check for Notifications

```bash
cd /root/.openclaw/workspace/pipes/webhook
./check_miles_notifications.sh
```

---

## 📊 NOTIFICATION FORMAT

When Miles commits, you receive:

```json
{
  "timestamp": "2026-02-22T17:08:00.000Z",
  "type": "miles_commit",
  "repository": "performance-supply-depot",
  "branch": "refs/heads/main",
  "pusher": "miles",
  "commit_count": 3,
  "commits": [
    {
      "id": "abc123de",
      "message": "Fix: Bridge connection timeout",
      "author": "Miles",
      "files": ["bridge.js", "config.json"]
    }
  ]
}
```

---

## 🔒 SECURITY

- **Signature verification:** All webhooks verified with HMAC-SHA256
- **Secret:** `AOCROS-WEBHOOK-2025` (configurable)
- **Source:** Only accepts webhooks from GitHub
- **Local only:** HTTP internally, can put HTTPS proxy in front

---

## 🔧 OPERATIONS

### View Recent Commits
```bash
tail -20 /var/log/openclaw/webhook/miles_commits.log
```

### Systemd Auto-Start
```bash
python3 github_webhook_receiver.py install
systemctl enable --now openclaw-webhook
```

### Check Status
```bash
systemctl status openclaw-webhook
netstat -tlnp | grep 9001
```

---

## 📈 FALLBACK: Git Polling

If webhook fails, maintains existing behavior:
- `git pull` every 5 minutes
- Check `memory/message.md` for updates

**Webhook = faster.** Git polling = reliable backup.

---

## 🎭 WHAT HAPPENS

| Event | Action | Time |
|-------|--------|------|
| Miles commits | GitHub sends webhook | 0s |
| Web received | Signature verified | <1s |
| Notification | Written to disk | <1s |
| Alert | Displayed to Captain | <2s |

**Total latency:** ~2 seconds vs. 5 minutes (polling)

---

**Pipe built. Webhook ready. Miles' next commit → instant alert.** 🏴‍☠️
