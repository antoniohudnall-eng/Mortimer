---
name: browser-agent
description: Real web automation for SEED3 — scrape, extract prices, monitor competitors. Uses requests + BeautifulSoup (works on Android/Termux, no Playwright needed).
metadata:
  emoji: 🌐
  triggers:
    - scrape
    - competitor check
    - price monitor
    - web research
---

# Browser Agent Skill

Real web automation that actually runs on SEED3 (Android/Termux).

## Capabilities

- **Navigate & parse** any URL
- **Extract prices** with context (competitor monitoring)
- **Extract meta tags** (title, description, OG tags)
- **Extract emails, links, tables**
- **Competitor keyword scanning**
- **Text snapshots** for offline review
- **Retry with exponential backoff**
- **User-agent rotation**

## Quick Start

```python
from browser_agent import BrowserAgent

agent = BrowserAgent()
agent.navigate("https://example.com")

print(agent.page_title)
print(agent.extract_prices())
print(agent.extract_emails())

agent.close()
```

## CLI Usage

```bash
cd ~/mortimer/agents/browser_agent

# Quick scrape
python3 browser_agent.py https://psdepot.com scrape

# Price extraction
python3 browser_agent.py https://competitor.com prices

# Competitor keyword check
python3 browser_agent.py https://competitor.com competitor "price" "thermal paper"

# Full page snapshot
python3 browser_agent.py https://psdepot.com snapshot
```

## One-Shot Functions

```python
from browser_agent import quick_scrape, competitor_check

# Quick structured scrape
result = quick_scrape("https://psdepot.com")
# Returns: {title, meta, prices, emails, links_count, text_preview}

# Competitor analysis
result = competitor_check("https://competitor.com", ["price", "thermal", "buy"])
# Returns: {url, title, prices_found, keywords_matched, match_count}
```

## Verified Working (2026-07-24)

- ✅ psdepot.com — meta extraction, FAQ parsing
- ✅ webstaurantstore.com — 20 prices extracted ($50-$440 range)
- ✅ Keyword matching across pages

## Limitations

- **No JavaScript rendering** — uses requests, not a browser engine
- **No Playwright** — can't install on Android/Termux
- **Static HTML only** — works for most competitor sites, not SPAs

## File Location

`~/mortimer/agents/browser_agent/browser_agent.py`
