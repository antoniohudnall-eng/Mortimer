
# Daily Email Check Procedure - Miles

**Created:** 2026-04-02 03:26 UTC
**Purpose:** Daily check of miles@myl0nr0s.cloud inbox for Captain's directives

## IMAP Configuration
```json
{
  "email": "miles@myl0nr0s.cloud",
  "password": "Myl0n.R0s",
  "imap_server": "imap.hostinger.com",
  "imap_port": 993,
  "ssl": true
}
```

## Daily Check Command
```bash
python3 /root/.openclaw/workspace/AGI_COMPANY/shared/tools/imap_checker.py
```

## Action Items from Captain (as of 2026-04-02)

### HIGH PRIORITY
1. **Dusty Wallet Implementation**
   - MongoDB API: al-M6dJ806p-wNoTc1ghNwjRIQogijaNMKxUEAx4zJJEKk
   - Infuria: 9614725115614e0c8b71d97b6db698f2
   - CoinGecko: CG-UXL41vSVxgCwWEp5YLH5soMH
   - Status: Ready to implement

2. **AI Agent Research**
   - Video: "How I'm Using AI Agents in 2026" (Tech With Tim)
   - Video: "Give Your AI Agent Unlimited Knowledge" (PMGPT + Vector Stores)
   - Video: "Make Your AI Agents 10x Smarter"

3. **OpenClaw Optimization**
   - System file audits to reduce token usage
   - 3-step prompt framework: Specific Objective → Clear KPIs → Force Questions

### MEDIUM PRIORITY
4. **County-Level Scraper**
   - Nationwide county-aware system design received
   - 3,143 counties in U.S.

5. **kRACKEN CLI**
   - Installed on VPS (Mar 30)
   - Command documented

## Email Routing Rules
- **From:** antonio.hudnall@gmail.com = ACTIONABLE
- **Subject keywords:** Research, API keys, Mission, Plan, Build
- **Auto-route to:** Appropriate team based on content

## Files to Check Daily
- `/root/.openclaw/workspace/data/email_action_items.json`
- IMAP inbox for new unread messages
- `/root/.openclaw/workspace/memory/pending_tasks.md` - Check for ACM API credentials

## Active Pending Tasks
1. **ACM Technologies API Credentials** - Awaiting secure note retrieval from Captain
   - Check for email with credentials
   - File location: `AGI_COMPANY/subsidiaries/ACM_TECH/`

## Last Updated
2026-05-02 17:51 UTC
