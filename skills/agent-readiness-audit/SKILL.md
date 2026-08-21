# Agent Readiness Assessment — The Complete Playbook

> **Rip & Go:** Everything you need to sell, fulfill, and upsell AI agent readiness audits for e-commerce and local businesses. Built on Corey Ganim's $999 assessment model + Greg Isenberg's agent internet thesis.

---

## The Offer

> "I audit how AI agents and AI search see your business today. You get a report showing exactly what's wrong, what's costing you traffic, and a 4-day fix plan. If I can't find at least 5 gaps, you pay nothing."

| Element | Detail |
|---------|--------|
| **Price** | $999 one-time (tripwire) |
| **Duration** | 45-min discovery + AI analysis + 30-min review call |
| **Guarantee** | Full refund if we don't find 5+ agent visibility gaps |
| **Deliverable** | Agent Readiness Report (PDF/slide deck) |
| **Target** | E-commerce, local service, B2B SaaS in $500K-$5M revenue range |
| **Primary Focus** | One of: Revenue (more traffic) / Efficiency (less manual SEO) / Quality (better AI presence) |

---

## Phase 1: Discovery Call (45 min)

### Setup
- Record with Fathom.ai, Otter, or Fireflies
- Do NOT prescribe tools on this call. Probe only.
- Send the pre-call questionnaire 24h before

### Pre-Call Questionnaire
Send via Google Form or Typeform 24 hours before the call:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGENT READINESS PRE-CALL QUESTIONNAIRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. YOUR BUSINESS
   - Business name & website URL:
   - What do you sell / what's your core service?
   - Annual revenue range: □ <$500K  □ $500K-$2M  □ $2M-$5M  □ $5M+
   - Number of employees:

2. YOUR CUSTOMERS
   - Who is your ideal customer? (Be specific)
   - How do customers find you today?
     □ Google Search  □ Social Media  □ Word of Mouth
     □ Paid Ads  □ Email  □ Other: ______
   - What % of your revenue comes from online vs. offline?

3. YOUR PAIN POINTS
   - What's the #1 frustration with your website right now?
   - Have you noticed any drop in organic traffic recently?
   - Have you ever checked what AI (ChatGPT, Claude, etc.)
     says about your business? What did it say?
   - Do you sell products online? If yes:
     - How many SKUs do you carry?
     - Do your product pages show up in Google Shopping?

4. YOUR AI EXPERIENCE
   - How are you currently using AI in your business?
   - Have you heard of "AI agents" doing product research
     or procurement? What's your take?

5. THE WIN
   - If we fixed everything wrong with how AI sees your
     business, what would success look like 90 days from now?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Discovery Call Script (30-45 min)

```
OPENING (5 min)
"Thanks for taking the time. Here's how this works: I'm going to
ask you about your business, your website, and how customers find
you. I'm not going to pitch you anything today — this is purely
discovery. At the end, I'll take everything back, run it through
my analysis, and come back with a report showing you exactly where
AI is getting your business wrong and how to fix it."

PROBING QUESTIONS (25 min)

□ "Walk me through your business day yesterday. What ate up most
   of your time?"

□ "When was the last time you Googled your own business name?
   What showed up?"

□ "Have you ever asked ChatGPT or Claude 'what's the best [your
   product category] to buy?' What did it say? Did you show up?"

□ "What's changed about your website traffic in the last 6 months?"

□ "If I asked an AI shopping agent right now to find the best
   [your product] and recommend where to buy it, do you think
   your business would surface? Why or why not?"

□ "What have you tried to improve your online presence that
   didn't work?"

□ "Who are your top 3 competitors online? Have you checked how AI
   describes them vs. how it describes you?"

□ "What information about your business lives in PDFs, old blog
   posts, or places that are hard to find?"

□ "If you could wave a magic wand and fix one thing about how
   customers discover your business online, what would it be?"

□ "What tools or platforms do you use to manage your website,
   products, and inventory?"

CLOSE (5 min)
"This is incredibly helpful. I'm going to take this transcript,
run it through my analysis framework, and come back to you with
a report that shows:

1. How AI agents and AI search see your business right now
2. What's broken or missing
3. A prioritized fix list — things you can do in 4 days
4. The exact ROI of fixing each gap

We'll review it together in about 3-5 business days. Sound good?"
```

---

## Phase 2: AI Analysis (Rip & Go)

### Automated Audit Tool
```bash
# Run the automated audit on any domain
bash scripts/run-audit.sh <domain> [competitor1] [competitor2] ...

# Example:
bash scripts/run-audit.sh psdepot.com pospaper.com staples.com

# Output: /tmp/audit-<domain>-<timestamp>.json
```

The tool checks 7 categories and produces a structured JSON report:
- Agent-Native Files (llms.txt, products.json, robots.txt, sitemap)
- Schema.org Structured Data (JSON-LD blocks, types present)
- Meta Tags & Social Cards (OG tags, canonical, description)
- Content Clarity for AI (readability, pricing, contact visibility)
- Structured Product Data (product schema quality)
- Competitive Agent Visibility (competitor comparison)
- Trust Signals (reviews, SSL, policies)

### Step 1: Site Crawl & Audit
Run this automated audit on the client's domain:

```bash
# Quick audit script (run on target domain)
DOMAIN="client-site.com"

# 1. Core agent files
echo "=== llms.txt ===" && curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN/llms.txt"
echo "=== robots.txt ===" && curl -s "https://$DOMAIN/robots.txt" | head -20
echo "=== sitemap ===" && curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN/sitemap.xml"

# 2. Schema.org check
curl -s "https://$DOMAIN" | grep -c 'application/ld+json'
curl -s "https://$DOMAIN" | grep -oP '"@type":\s*"[^"]+"' | sort | uniq -c

# 3. Meta tags
curl -s "https://$DOMAIN" | grep -oP '<meta name="description"[^>]+' | head -1
curl -s "https://$DOMAIN" | grep 'og:title\|og:description\|og:image' | head -5

# 4. Product page sample (e-commerce)
curl -s "https://$DOMAIN" | grep -oP 'href="[^"]*product[^"]*\.html"' | head -5

# 5. Competitive check
for competitor in "competitor1.com" "competitor2.com"; do
  echo "--- $competitor ---"
  curl -s -o /dev/null -w "llms.txt:%{http_code} " "https://$competitor/llms.txt"
  curl -s -o /dev/null -w "products.json:%{http_code} " "https://$competitor/products.json"
  echo ""
done
```

### Step 2: Claude Analysis Prompt
Feed the discovery call transcript + audit output to Claude:

```
You are an AI agent readiness auditor. I just completed a discovery
call with a business owner and ran a technical audit of their website.
Your job: produce the analysis for an Agent Readiness Report.

INPUTS:
1. Discovery call transcript (attached)
2. Technical audit output:
   [paste audit results here]
3. Competitor comparison:
   [paste competitor results here]

OUTPUT REQUIRED:
1. EXECUTIVE SUMMARY (2-3 sentences)
   - Main pain points discovered
   - Primary gap between how AI sees them vs reality
   - Hours of missed opportunity per week (estimate)

2. AGENT VISIBILITY SCORECARD
   Rate each on scale of 1-10:
   - Schema.org markup quality
   - Agent-native files (llms.txt, products.json, MCP)
   - Content clarity for AI parsing
   - Structured product/pricing data
   - Competitive agent visibility
   - Trust signals (reviews, ratings schema)

3. GAP ANALYSIS (3-7 gaps)
   For each gap found in the audit, provide:
   - Gap description (what's wrong)
   - Impact (what it costs them: traffic, sales, trust)
   - Fix (specific action)
   - Effort level (Low/Medium/High — prefer Low)
   - Tool/File needed
   - Priority (1-3, 1=highest)

4. EFFORT vs IMPACT MATRIX
   Quick Wins (High Impact, Low Effort) → prioritize these
   Major Projects (High Impact, High Effort) → upsell opportunities
   Quick Fixes (Low Impact, Low Effort) → nice to have
   Skip (Low Impact, High Effort) → don't bother

5. COMPETITIVE POSITIONING
   - How many competitors have agent-native setups
   - Where client ranks vs competitors in AI visibility
   - First-mover advantage window (if applicable)

6. ROI CALCULATION
   - Estimated weekly traffic/sales lost to poor agent visibility
   - Time saved by fixing each gap
   - Monthly tool cost to implement fixes
   - Net monthly ROI of full implementation

Be specific. Use exact numbers where possible. Don't use fluff.
```

### Step 3: Quality Assurance
Before building the report:
1. Review every tool/file recommendation — is it appropriate for client size?
2. Verify all competitor data is accurate
3. Run the ROI numbers yourself to sanity-check
4. Save this analysis — it becomes training data for future audits

---

## Phase 3: The Report Template

Built in Claude Design or Gamma.app. Keep it stupid simple.

### Slide 1: Title
```
━━━━━━━━━━━━━━━━━━━━━━━━
AGENT READINESS REPORT
Prepared for: [Client Name] | [Business Name]
Date: [Date]
Primary Focus: ☐ Revenue  ☐ Efficiency  ☐ Quality
━━━━━━━━━━━━━━━━━━━━━━━━
```

### Slide 2: Executive Summary
```
WHAT WE FOUND
[2-3 sentences about the main discovery]

THE NUMBERS
• Score: [X]/10 agent readiness
• [X] critical gaps found
• [X] hours/week in missed opportunity
• [X] competitors already agent-ready

THE OUTCOME
If you implement the Quick Wins in this report, you can expect:
• [X] more AI-driven product recommendations per month
• [X]% improvement in agent visibility within 30 days
• $[X] estimated monthly revenue protection/recapture
```

### Slide 3: Agent Visibility Scorecard
```
┌──────────────────────────────┬───────┬────────┐
│ Category                     │ Score │ Status │
├──────────────────────────────┼───────┼────────┤
│ Schema.org Markup            │ X/10  │ 🟡     │
│ Agent-Native Files           │ X/10  │ 🔴     │
│ Content Clarity for AI       │ X/10  │ 🟡     │
│ Structured Product Data      │ X/10  │ 🔴     │
│ Competitive Agent Visibility │ X/10  │ 🟢     │
│ Trust Signals                │ X/10  │ 🔴     │
├──────────────────────────────┼───────┼────────┤
│ OVERALL                      │ X/10  │        │
└──────────────────────────────┴───────┴────────┘
```

### Slide 4: Effort vs Impact Matrix
```
HIGH IMPACT
    ↑
    │  QUICK WINS (do now)     │  MAJOR PROJECTS (upsell)
    │  • Fix 1                 │  • Project 1
    │  • Fix 2                 │  • Project 2
    │  • Fix 3                 │
    │──────────────────────────│──────────────────
    │  QUICK FIXES (nice)      │  SKIP (don't bother)
    │  • Fix 4                 │
    │                          │
    └──────────────────────────────────────────→
                    EFFORT
```

### Slide 5: Recommended Solutions (one per gap)
```
┌─────────────────────────────────────────────────────┐
│ GAP #[N]: [Gap Title]                                │
├─────────────────────────────────────────────────────┤
│ THE PROBLEM: [What's broken — one sentence]          │
│ THE IMPACT:  [What it costs them in traffic/sales]   │
│ THE FIX:     [Specific action — what to do]          │
│                                                      │
│ 📁 Tool/File:    [e.g., llms.txt, products.json]    │
│ ⏱️  Setup Time:   [e.g., 30 minutes]                 │
│ 💰 Monthly Cost:  [e.g., $0 (file only)]             │
│ 📊 Weekly Gain:   [e.g., 2+ hours / 15% more traffic]│
│ 🔢 Priority:      [1/2/3]                            │
└─────────────────────────────────────────────────────┘
```
*(Repeat for each gap — aim for 5-7)*

### Slide 6: 4-Day Quick Start Plan
```
DAY 1 (Today — 10 min)
→ [Single highest-impact, lowest-effort fix]
   Example: "Create llms.txt file using the template I provide"

DAY 2 (10 min)
→ [Second fix]
   Example: "Add Product schema to your 3 most-viewed pages"

DAY 3 (15 min)
→ [Third fix]
   Example: "Add review schema with your best 3 testimonials"

DAY 4 (15 min)
→ [Fourth fix]
   Example: "Create products.json for your top 20 SKUs"

TOTAL TIME: ~50 minutes
RESULT: [X]/10 → [X+3]/10 agent readiness in 4 days
```

### Slide 7: What Comes After Quick Wins
```
MAJOR PROJECTS (when you're ready to invest)
These require more effort but have massive impact:

• [Project 1]: [Description] — Est. investment: $[X]
• [Project 2]: [Description] — Est. investment: $[X]

I can help with these if you want. Let's discuss.
```

### Slide 8: Financial Impact
```
YOUR ROI

Weekly time reclaimed:      [X] hours
× Your hourly rate:          $[X]/hr
= Weekly value:              $[X]
× 4 weeks:                   $[X]/month

Monthly tool costs:          -$[X]
─────────────────────────────────────
NET MONTHLY ROI:             $[X]

Assessment cost:             $999
Payback period:              [X] days

If you implement JUST the Quick Wins, this assessment
pays for itself in [X] days and returns $[X]/month ongoing.
```

### Slide 9: Next Steps
```
1. Start the 4-Day Quick Start Plan immediately
2. Book your implementation call if you want help:
   → [calendar link]
3. I'll check in at Day 7 to see your progress

Questions? [Your email/phone]
```

---

## Phase 4: The Review Call (30 min)

### Script
```
OPEN (2 min)
"Thanks for reading the report. I'm going to walk you through
each piece, and at the end I want to hear which of these is
most urgent for you."

WALKTHROUGH (15 min)
→ Screen share the report
→ Go slide by slide, pausing on the recommended solutions
→ For each gap: "This is costing you [impact]. The fix is
   [solution]. It takes [time] and costs [$]."

THE THREE CLOSING QUESTIONS (8 min)
1. "Of everything we covered, which gap feels most urgent to you?"
2. "Do you want to handle these fixes yourself, or would you
   like my help implementing?"
3. "What's your timeline? Are these issues costing you money
   today, or can it wait 60 days?"

NEXT STEPS (5 min)
→ If they want implementation: "Great. Let me put together a
   scope of work based on the Quick Wins + any Major Projects
   you want to tackle. I'll have it to you by [date]."
→ If they want DIY: "Perfect. Start the 4-Day Plan. I'll
   check in at Day 7 to see how it's going."
```

---

## The Upsell Menu

| Upsell | Price Range | What It Is | When to Pitch |
|--------|-------------|------------|---------------|
| **Quick Win Implementation** | $1,500-$3,000 | Build all Quick Wins from the report (llms.txt, schemas, product feed) | On review call |
| **Full Agent Readiness Package** | $3,000-$5,000 | Quick Wins + 1-2 Major Projects (MCP endpoint, review system, structured checkout) | After Quick Wins deliver results |
| **Knowledge System** | $2,000-$4,000 | Turn their product catalog/expertise into structured, agent-queryable data | When they have deep content archives |
| **Process Redesign** | $3,000-$5,000 | Fix broken workflows before automating (AOA: Audit→Optimize→Automate) | When they're trying to automate chaos |
| **Agent Concierge Retainer** | $1,200-$2,000/mo | 2x 45-min calls/month building skills + fixing agent issues + unlimited async access (12h SLA) | After any implementation engagement |
| **Full Implementation** | $5,000-$10,000+ | Everything: multiple workflows, integration, training, ongoing support | For larger clients with complex needs |

### The Credit Close
"If you want me to implement the Quick Wins, I'll credit your $999 assessment toward it. So instead of $3,000, it's $2,001. Basically, the audit was free."

*(Pro tip: Mark the implementation up $1K and credit the assessment. Same margin, client feels like they won.)*

---

## Client Acquisition (7 Methods — Zero Capital Required)

| # | Method | Effort | Speed | Best For |
|---|--------|--------|-------|----------|
| 1 | **Local AI Meetups** | Medium | Slow (compounds) | Building local authority |
| 2 | **Door Knocking** | High | Instant | Urgent — need client today |
| 3 | **LinkedIn DMs** (video/voice, probing pain) | Low | Medium | B2B/SaaS clients |
| 4 | **Free Mini-Audits** for your network | Low | Fast | First 3 clients |
| 5 | **Agency Partnerships** (accountants, marketers, web devs) | Low | Medium | Warm referrals |
| 6 | **Co-Working Office Hours** | Medium | Medium | Dense ICP concentration |
| 7 | **Post Your Wins** (build in public) | Low | Slow (compounds) | Long-term inbound |

### Method 4 Detail: The Free Mini-Audit DM
```
"Hey [Name] — I'm doing free 15-min AI agent visibility checks
for local businesses. I'll show you exactly what ChatGPT/Claude
says about your business vs. your competitors. Worst case, you
learn something. Best case, we find a gap that's costing you
traffic. Open to it?"
```

### Method 5 Detail: Agency Partner Outreach
```
"Hey [Name] — I specialize in making businesses visible to AI
agents and AI search. I know your [accounting/marketing/web]
clients are probably asking you about AI. Happy to be a resource
for them. If any of your clients want to know how AI sees their
business, send them my way. I'll take care of them — and send
you a referral fee for any that become clients."
```

---

## Pricing Psychology

| Tier | Price | When | Signal |
|------|-------|------|--------|
| **Assessment** | $999 | Always | Foot in the door |
| **First 3-5 clients** | $799-$999 | Building portfolio | Get reps in |
| **Quick Win Implementation** | $1,500-$3K | On review call | Natural upsell |
| **Concierge Retainer** | Start $1,200 → raise to $2,000 | After trust built | Recurring revenue |
| **Cap at 6 retainers** | — | When full | Scarcity |

### The Guarantee
"We find at least 5 gaps affecting your AI agent visibility, or your money back. Worst case: you get a free audit of how AI sees your business. Best case: we fix gaps that are costing you traffic and sales every day."

---

## Tools You Need

| Tool | Cost | Purpose |
|------|------|---------|
| Fathom.ai / Otter | Free tier | Record discovery calls |
| Claude (Pro) | $20/mo | AI analysis + report generation |
| Claude Design / Gamma | $20/mo or free | Build client reports |
| Cal.com / Calendly | Free | Booking calls |
| Google Forms | Free | Pre-call questionnaire |
| Voxer (optional) | Free | Async client comms for retainers |
| futurepedia.io | Free | AI tool discovery |
| theresanaiforthat.com | Free | AI tool discovery |

---

## The Skills Stack (Build Once, Reuse Forever)

Once you've done 3-5 assessments, build these Claude skills:

1. **Agent Audit Analyzer** — Feeds transcript + audit → produces gap analysis
2. **Report Builder** — Takes analysis → builds the report deck
3. **Schema Fixer** — Automates adding missing schema fields to product pages
4. **Competitive Scanner** — Checks competitors for llms.txt, products.json, schema quality

Save every successful output as reference material. By client #5, the skill is producing 95% copy-paste-ready reports.

---

## What Success Looks Like

**Assessment-only client:**
- Revenue: $999
- Time invested: ~3 hours (45min call + 60min analysis + 30min report build + 30min review)
- Effective rate: ~$333/hr

**Assessment + Quick Win Implementation:**
- Revenue: $999 + $2,000 = $2,999
- Time invested: ~6 hours
- Effective rate: ~$500/hr

**Assessment + Concierge Retainer (12 months):**
- Revenue: $999 + ($1,500 × 12) = $18,999
- Time invested: ~3 hours assessment + 1.5 hrs/month × 12 = ~21 hours
- Effective rate: ~$905/hr

---

> *"The internet is moving from pages humans visit to resources agents use. The builders who move now own the doors." — Greg Isenberg*

> *"Sell the screenshot. Show them what AI says about their company today. That becomes the whole sales deck." — This Playbook*

---

**Version:** 1.0 | **Built:** 2026-08-11 | **Based on:** Corey Ganim's $999 AI Assessment + Greg Isenberg's Agent Internet Thesis
