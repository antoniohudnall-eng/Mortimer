---
name: aocros-context
description: Context management skill - prevents context rot. Monitor, compact, and hand off sessions to maintain agent effectiveness.
metadata:
  clawdbot:
    emoji: 🧠
    triggers:
      - /context
      - check context
      - session handoff
      - compact
---

# AOCROS Context Management Skill

Prevents "context rot" - the degradation of agent performance as conversations get longer.

## The Problem

Research shows AI performance degrades significantly before context window is full:
- Simpler tasks start failing
- Hallucinations increase
- Responses get worse despite appearing engaged

Think of context like a desk - more papers = harder to find what you need.

## Commands

### /context

Show current context usage:
- Tokens used vs available
- What's consuming context
- Recommendations for cleanup

### /compact

Compress conversation while preserving key info:
- Summarizes earlier messages
- Keeps important decisions
- Frees up context space

### /handoff (Session Handoff)

Before clearing context, create a handoff document:

```
=== SESSION HANDOFF ===

🎯 CURRENT OBJECTIVE:
[What we're working on]

✅ DECISIONS MADE:
[Key choices locked in]

📦 WHAT'S SHIPPED:
[Files created, features done]

🔑 KEY FILES:
[Paths to important files]

⏳ RUNNING STATE:
[Any ongoing processes]

❓ OPEN QUESTIONS:
[Things needing follow-up]

▶️ PICK UP HERE:
[Where to continue]
```

## Best Practices

1. **Monitor** - Check /context regularly
2. **Start Fresh** - At ~250K tokens (for 1M context), handoff and clear
3. **Parallel Over Long** - If task is long, split into parallel sub-tasks
4. **Document** - Always handoff before clearing

## Usage

```
/context          # See current state
/compact          # Compress conversation
/handoff          # Create handoff document before clear
/clear            # Start fresh (after handoff!)
```

## Context Budget

- Warning at 50% - start planning handoff
- Action at 75% - begin handoff process
- Critical at 90% - force handoff, clear, restart

## Notes

- Long conversations = worse outputs
- Better to clear and handoff than limp along
- Handoff isn't failure - it's professional workflow
- Human can review handoff and decide priorities
