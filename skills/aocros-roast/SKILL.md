---
name: aocros-roast
description: Adversarial analysis skill - stress test ideas before building. Forces honest evaluation by multiple perspectives to prevent yes-man behavior.
metadata:
  clawdbot:
    emoji: 🔥
    triggers:
      - /roast
      - roast this
      - stress test
      - analyze this idea
---

# AOCROS Roast Skill

Adversarial analysis before any significant action. Prevents the "yes-man" problem where AI agrees with everything.

## When to Use

Invoke before:
- Creating new agents
- Starting major projects
- Building new features
- Proposing strategic changes
- Any task with complexity > threshold

## The Council

### 1. Contrarian
**Role:** Find fatal flaws
**Prompt:** What could absolutely destroy this? What assumptions are fatal? What's the worst case?

### 2. Expansionist  
**Role:** Find biggest upside
**Prompt:** What's the ceiling? What if everything went perfectly? What's the 10x opportunity?

### 3. FirstPrinciples
**Role:** Pure logic, no assumptions
**Prompt:** Strip away all context. What remains? What's actually true without external knowledge?

### 4. Researcher
**Role:** Pull real market data
**Prompt:** What do competitors charge? What's the market size? Any recent news that changes things?

### 5. Buyer
**Role:** Would they pay?
**Prompt:** Roleplay as target customer. Would you buy this? At what price? What's the objection?

## Judge Verdict

After all 5 analyze, the Judge provides:
- **GREEN LIGHT** → Proceed as planned
- **RESHAPE** → Modify significantly before proceeding
- **KILL** → Don't do this (explain why)

Also includes: **Cheapest 48-hour test** to validate before full commitment.

## Usage

```
/roast [your idea or proposal]
```

Example:
```
/roast Build a crypto trading bot that follows Twitter signals
```

## Output Format

```
=== ROAST ANALYSIS ===

📉 CONTRARIAN:
[Flaws found]

📈 EXPANSIONIST:
[Upside potential]

🔬 FIRST PRINCIPLES:
[Core truths]

📊 RESEARCHER:
[Market data]

💰 BUYER:
[Would they pay?]

⚖️ JUDGE VERDICT: [GREEN LIGHT / RESHAPE / KILL]
Confidence: [High/Medium/Low]

🧪 CHEAPEST TEST:
[What to do in next 48 hours]
```

## Notes

- Roast is uncomfortable but valuable
- The goal isn't to kill ideas, it's to make them stronger
- Even "Green Light" usually has improvement suggestions
- Use before every significant decision
