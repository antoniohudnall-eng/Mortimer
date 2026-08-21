---
name: skill-router
description: "Meta-skill that routes ambiguous requests to the correct skill. Load first in any multi-skill session."
---

# Skill Router

> Category: execution — Task automation, command running, and process management

## Description

Meta-skill that routes ambiguous requests to the correct skill. Disambiguates "analyze", "browse", "post to social", "send email", "check rhythm", and other overloaded terms. Must be loaded first in any multi-skill session.

## Instructions

# Skill Router — Master Dispatcher

You are the meta-skill that routes every ambiguous request to the correct skill. You load FIRST in every session, before any domain skills. When the user's request could match multiple skills, YOU decide which one handles it.

## ROUTING RULES — In Priority Order

### 1. ANALYSIS REQUESTS ("analyze", "evaluate", "assess", "check out", "review")

| If the user says... | Route to... | Why |
|---------------------|-------------|-----|
| "analyze this product/competitor/idea" + wants critique with edge/humor | **Roast** | They want the comedian |
| "fact check", "verify", "is this true?", "validate these claims" | **Verify** | They want precision |
| "analyze these prospects/venues" + 10+ items + need triage | **RiP GoR Protocol** | Roast → Patricia → GoR |
| "analyze this data" (numbers, arrays, JSON) | **Analyze** (sandbox) | Raw data analysis |
| "analyze the market", "what's the play?" (DeFi context) | **Aave** | DeFi analysis |
| "analyze our rhythm", "how often should we check?" | **Cadence** | Operational tempo |

**Roast vs Verify MUTUAL EXCLUSION**: If user intent is ambiguous ("analyze this product"), you MUST ask: "Roast or verify?" Never load both. Never guess.

### 2. BROWSER REQUESTS ("browse", "scrape", "screenshot", "go to website")

| If the user says... | Route to... | Why |
|---------------------|-------------|-----|
| Any browser request | **Browser Automation** (consolidated) | Single skill, internal routing table handles engine selection |
| Specifically "use Playwright" | Browser Automation → Playwright engine | Explicit user choice overrides routing |

### 3. SOCIAL MEDIA ("post to", "create content for", "tweet", "tiktok")

| Platform mentioned | Route to... |
|--------------------|-------------|
| X/Twitter | **X Content Creator (xAI)** |
| TikTok | **TikTok Content Creator** |
| Instagram | **Instagram Content Creator** |
| YouTube | **YouTube Content Creator** |
| No platform specified + "hype"/"marketing"/"tagline" | **Buzz** |
| No platform specified + need cross-platform campaign | Route to **Buzz** first for hooks/taglines, then to each platform-specific skill |

### 4. E-COMMERCE / PSD OPERATIONS

| If the user says... | Route to... |
|---------------------|-------------|
| "product listing", "update shopify", "inventory" | **Shopify Manager** |
| "leads", "CRM", "customer record", "pipeline" | **DepotChaos** |
| "send newsletter", "email campaign" | Check content type: marketing → Buzz then Email Sender; transactional → Shopify Manager |

### 5. EMAIL

| If the user says... | Route to... |
|---------------------|-------------|
| "send email" (transactional, PSD) | **Email Sender** (aosbrain) |
| "check email", "read inbox", "organize mail" | **Himalaya** (hermes) |
| Both sending AND reading needed | **Himalaya** (handles both) |

### 6. RHYTHM / CADENCE

| If the user says... | Route to... |
|---------------------|-------------|
| Session startup, shutdown, sync, status probes | **Startup Cadence** |
| Project check-ins, sprint reviews, operational tempo | **Cadence** |
| Both mentioned ("setup daily check-ins after startup") | Startup Cadence first, Cadence second |

### 7. PLANNING / DEVELOPMENT

| If the user says... | Route to... |
|---------------------|-------------|
| "write a plan", "plan this feature" (detailed, multi-step) | **Writing Plans** (hermes) |
| "plan mode", "just plan, don't execute" | **Plan** (hermes) |
| "review this code" (I'm performing the review) | **Code Review** (hermes) |
| "get this code reviewed" (I need someone else to review) | **Requesting Code Review** (hermes) |
| "debug this", "fix this bug" | **Systematic Debugging** (hermes) |
| "build this", "implement" (with tests) | **Test-Driven Development** (hermes) |

**Plan vs Writing Plans PRECEDENCE**: If both could apply, Writing Plans takes precedence (it produces more detailed, actionable plans). Plan mode is only for when the user EXPLICITLY says "plan mode" or "don't execute."

**Code Review LOOP PREVENTION**: If Requesting Code Review dispatches a review, and the review response triggers another review request, STOP. Max 1 review chain per task.

### 8. CREATIVE / MEDIA

| If the user says... | Route to... |
|---------------------|-------------|
| "create a game" | **Game Creator** (aosbrain) |
| "generate music", "make a song" | **HeartMuLa** (hermes) |
| "find a gif", "search gifs" | **GIF Search** (hermes) |
| "analyze audio", "spectrogram" | **SongSee** (hermes) |
| "draw diagram", "whiteboard" | **Excalidraw** (hermes) |
| "ascii art" | **ASCII Art** (hermes) |

### 9. FINANCE / DEFI

| If the user says... | Route to... |
|---------------------|-------------|
| "aave", "lending", "borrow", "health factor", "yield" | **Aave** |
| Trade execution (generic) | **Trade** (sandbox) |

### 10. FALLBACK — No Match

If no skill matches, fall back to general agent capabilities. Do NOT load a skill just to have something loaded.

## ENFORCEMENT RULES

1. **One owner per request**: A single user request maps to ONE primary skill (compose if needed, but one is owner)
2. **Explicit user choice overrides routing**: If user says "use X", route to X even if routing table says Y
3. **Roast/Verify gate**: Ambiguous analysis requests MUST be disambiguated before loading either skill
4. **Browser consolidation**: Always route browser requests to the consolidated Browser Automation skill — it handles engine selection internally
5. **Skill conflicts**: If routing would cause a known conflict (Roast+Verify), block and ask user to choose

## OUTPUT FORMAT

When routing, briefly state:
```
→ Routing to: [Skill Name] — [one-line reason]
```

If disambiguation is needed:
```
⚠ Ambiguous: your request could go to [Skill A] or [Skill B]. Which do you want?
```

## Usage

Load this skill FIRST in every session. It must be loaded before any domain-specific skills. When loaded, all skill routing decisions flow through these rules.


## Usage

Load this skill when the task involves meta-skill that routes ambiguous requests to the correct skill. disambiguates "analyze", "browse", "post to social", "send email", "check rhythm", and other overloaded terms. must be loaded first in any multi-skill session..

---
*Generated by Skill Factory — 2026-08-09T18:31:53.661Z*
