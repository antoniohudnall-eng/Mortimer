---
name: browser-automation
description: "Unified browser automation using the best engine per task — agent-browser, Playwright, or Stagehand. Use for web scraping, form filling, screenshots, and browser interaction."
---

# Browser Automation (Consolidated)

> Category: execution — Browser interaction, web scraping, screenshots, form automation
> **CONSOLIDATED**: This skill replaces browser-agent, browser-automation (Stagehand), and agent-browser (clawdbot).
> **Version**: 2.0.0 — Three engines, one interface, zero confusion.

## Description

Unified browser automation using the best engine for each task. Three engines available: agent-browser (fast, ref-based), Playwright (visual, PDF, Python), Stagehand (NL-driven, CAPTCHA-resistant).

---

## 🧭 ROUTING TABLE — Which Engine To Use

This table is **mandatory**. When a browser task is requested, match against these rules IN ORDER. First match wins.

| If the task involves... | Use Engine | Because... |
|--------------------------|------------|------------|
| Multi-step form filling, complex SPA workflows, deterministic clicks | **agent-browser** (Vercel CLI) | Ref-based selection is reliable; no flaky CSS selectors |
| Text/data extraction from known sites | **agent-browser** | Fast snapshots, JSON output, session isolation |
| Need screenshots with visual analysis, PDF generation | **Playwright** (Python) | Full rendering, full-page screenshots, PDF generation |
| Visual diff/comparison of pages | **Playwright** | `.compare_screenshots()` built in |
| CAPTCHA-heavy sites, production scraping behind bot detection | **Stagehand** (Browserbase) | Stealth mode, proxy support, CAPTCHA handling |
| Natural language browsing ("go to site and find the pricing") | **Stagehand** | `browser act` takes NL instructions directly |
| Need both visual rendering AND fast text extraction | **Playwright** → screenshot first, then switch to agent-browser if just text |
| Local dev/testing, no CAPTCHA concerns | **agent-browser** | Fastest, lightest, no API keys needed |
| Session isolation (admin + user simultaneously) | **agent-browser** | `--session` flag built in |
| Mobile viewport testing | **Playwright** | `set_viewport()` for mobile dimensions |

### Decision Flowchart

```
Browser task requested
│
├─ Need screenshots/PDFs/visuals? ──→ Playwright
├─ Need CAPTCHA bypass / production stealth? ──→ Stagehand
├─ Natural language browsing? ──→ Stagehand
├─ Multi-step automation / data extraction? ──→ agent-browser
├─ Form testing / SPA interaction? ──→ agent-browser
└─ Unsure? ──→ Start with agent-browser (lightest), escalate if needed
```

### Engine Switching

You MAY switch engines mid-task if needed:
- Start with **agent-browser** for navigation + data extraction
- Switch to **Playwright** only if screenshots/PDFs are requested
- Switch to **Stagehand** only if CAPTCHA or bot detection is encountered

**Never run two engines simultaneously against the same site** — this triggers rate limiting and bot detection.

---

## ⚙️ Engine 1: agent-browser (Vercel CLI)

**Best for:** Fast, deterministic automation. Multi-step workflows. Data extraction.

### Installation
```bash
npm install -g agent-browser
agent-browser install                     # Download Chromium
agent-browser install --with-deps         # Linux: + system deps
```

### Core Workflow
```bash
agent-browser open https://example.com
agent-browser snapshot -i --json          # Get refs for all interactive elements
agent-browser click @e2                   # Click element by ref
agent-browser fill @e3 "text"             # Fill by ref
agent-browser snapshot -i --json          # Re-snapshot after changes
```

### Commands Reference

**Navigation:** `open`, `back`, `forward`, `reload`, `close`

**Snapshot:** `snapshot -i --json` (always use `-i` for interactive, `--json` for parseable output)

**Interactions (all ref-based with @eN):**
```bash
agent-browser click @e2
agent-browser fill @e3 "text"
agent-browser type @e3 "text"
agent-browser hover @e4
agent-browser check @e5 | uncheck @e5
agent-browser select @e6 "value"
agent-browser press "Enter"
agent-browser scroll down 500
agent-browser drag @e7 @e8
```

**Information:**
```bash
agent-browser get text @e1 --json
agent-browser get html @e2 --json
agent-browser get value @e3 --json
agent-browser get attr @e4 "href" --json
agent-browser get title --json
agent-browser get url --json
agent-browser get count ".item" --json
```

**State checks:** `is visible @e2 --json`, `is enabled @e3 --json`, `is checked @e4 --json`

**Waiting:**
```bash
agent-browser wait @e2                    # Wait for element
agent-browser wait --load networkidle     # Wait for network
agent-browser wait --text "Welcome"       # Wait for text
agent-browser wait --url "**/dashboard"   # Wait for URL
```

**Sessions (isolated):**
```bash
agent-browser --session admin open site.com
agent-browser --session user open site.com
agent-browser session list
```

**State persistence:**
```bash
agent-browser state save auth.json        # Save cookies/storage
agent-browser state load auth.json        # Restore session
```

**Network control:**
```bash
agent-browser network route "**/ads/*" --abort           # Block
agent-browser network route "**/api/*" --body '{"x":1}'  # Mock
```

**Tabs & Frames:** `tab new URL`, `tab N`, `frame @e5`, `frame main`

### Best Practices
1. Always use `-i` (interactive elements only) + `--json` (parseable)
2. Wait for stability: `agent-browser wait --load networkidle`
3. Save auth state to skip login flows
4. Use sessions to isolate different browser contexts
5. Use `--headed` for debugging

---

## ⚙️ Engine 2: Playwright (Python)

**Best for:** Screenshots, PDFs, visual comparisons, mobile viewport testing.

### Installation
```bash
npm install -g playwright
playwright install chromium
```

### Quick Start
```python
from browser_agent import BrowserAgent

agent = BrowserAgent(headless=True)
agent.navigate("https://psdepot.com")
agent.screenshot_full_page("homepage.png")
agent.close()
```

### Key Capabilities

**Screenshots:**
```python
agent.screenshot("page.png")                    # Viewport only
agent.screenshot_full_page("full.png")          # Full scroll
agent.screenshot_element(".product", "el.png") # Single element
agent.set_viewport({"width": 375, "height": 812}) # Mobile
```

**PDF Generation:**
```python
agent.save_pdf("output.pdf", {"format": "A4", "printBackground": True})
```

**Form Filling:**
```python
agent.fill_form({"name": "Miles", "email": "miles@psdepot.com"})
agent.click_submit()
agent.wait_for_success_message()
```

**Data Extraction:**
```python
agent.get_text(".price")                        # Single element text
agent.extract_table("table.results")            # Table → list of dicts
agent.extract_links()                           # All links on page
agent.extract_images()                          # All image URLs
```

**Visual Diff:**
```python
agent.compare_screenshots("before.png", "after.png")  # Returns diff
```

### Advanced
```python
# Stealth
agent = BrowserAgent(
    headless=True,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
)

# Proxy
agent = BrowserAgent(proxy={"server": "http://proxy:8080"})

# Auth
agent.authenticate("user", "pass")              # HTTP Basic
agent.set_cookie("session", "abc123", domain=".example.com")
```

---

## ⚙️ Engine 3: Stagehand (Browserbase)

**Best for:** CAPTCHA-heavy sites, production scraping, NL-driven browsing.

### Prerequisites
- `BROWSERBASE_API_KEY` and `BROWSERBASE_PROJECT_ID` in `.env`
- Falls back to local Chrome if no Browserbase keys

### Installation
```bash
npm install          # In skill directory
npm link             # Creates global 'browser' command
```

### Commands
```bash
browser navigate <url>                    # Go to URL
browser act "<action>"                    # Natural language: "click sign in"
browser extract "<instruction>" ['{}']    # Extract data (optional JSON schema)
browser observe "<query>"                 # Discover elements on page
browser screenshot                        # Take screenshot
browser close                             # Close browser
```

### Example
```bash
browser navigate https://example.com
browser act "click the Sign In button"
browser extract "get the page title"
browser close
```

### When to Use Stagehand
- Site has Cloudflare, DataDome, or similar bot protection
- Need CAPTCHA solving
- Scraping at scale (Browserbase handles IP rotation)
- User describes the task in natural language ("find the cheapest plan")

---

## 🔒 Engine Conflict Prevention

### Rules
1. **One engine per task** unless escalation is justified (see Engine Switching above)
2. **Default to agent-browser** when uncertain — it's the lightest and fastest
3. **Playwright only** when screenshots or PDFs are explicitly requested
4. **Stagehand only** when CAPTCHA/stealth is needed
5. **If a task description matches multiple engines**, use the Routing Table in order — first match wins

### Anti-Patterns
- ❌ Opening the same URL in two engines simultaneously
- ❌ Using Playwright for simple text extraction (use agent-browser)
- ❌ Using Stagehand when there's no CAPTCHA concern (unnecessary cost)
- ❌ Using agent-browser when screenshots are needed (it can do basic screenshots but Playwright is better)

---

## 📁 File Structure

```
skills/browser-automation/
├── SKILL.md                    # This consolidated file (replaces all three)
├── engines/
│   ├── agent-browser.md        # Full agent-browser reference (archived)
│   ├── playwright.md           # Full Playwright reference (archived)
│   └── stagehand.md            # Full Stagehand reference (archived)
├── examples/
│   ├── competitor-monitor.py   # Playwright example
│   ├── form-tester.sh          # agent-browser example
│   └── scrape-protected.sh     # Stagehand example
└── outputs/                    # Generated screenshots/PDFs
```

---

## 🏷️ Aliases

```
browser  → This consolidated skill
browse   → Same
scrape   → Routes to agent-browser or Stagehand based on site
screenshot → Routes to Playwright
```

---

**Status:** CONSOLIDATED v2.0.0
**Supersedes:** browser-agent, browser-automation (Stagehand), agent-browser (clawdbot)
**Maintainer:** Miles (Performance Supply Depot)
