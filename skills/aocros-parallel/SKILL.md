---
name: aocros-parallel
description: Parallel execution skill - use sub-agents for parallel tasks. Stop being the bottleneck by coordinating multiple agents.
metadata:
  clawdbot:
    emoji: 🚀
    triggers:
      - /goal
      - parallel
      - sub-agents
      - coordinate
---

# AOCROS Parallel Execution Skill

Use sub-agents to run tasks in parallel. Stop being the bottleneck.

## The Problem

You're the bottleneck. Single-threaded execution is slow. Anthropic research: teams of sub-agents outperform single agents by 90%.

## Concepts

### Sub-Agent
A separate agent instance with:
- Own clean context window
- Individual task assignment
- Independent execution
- Reports back when complete

### /goal Command
Set a finish line. Agent works until completion criteria met.
- Separate evaluator grades progress
- Agent can't "fake" completion
- Keeps working until done

## Usage Patterns

### Pattern 1: Parallel Research

```
Task: Research [TOPIC]
Sub-agents:
- Agent A: Competitor analysis
- Agent B: Market size data
- Agent C: Customer interviews
- Agent D: Technical feasibility

Results synthesized by main agent.
```

### Pattern 2: Build + Verify

```
Main Agent: Orchestrates
Sub-agent 1: Build feature
Sub-agent 2: Test feature
Sub-agent 3: Security audit

Parallel execution, then merge.
```

### Pattern 3: /goal with Sub-agents

```
/goal Build complete landing page

Sub-agents (parallel):
- Hero section builder
- Features section builder
- Pricing section builder
- Contact form builder

Each has own context. No context rot.
Main agent verifies and merges.
```

## /goal Syntax

```
/goal [COMPLETION_CRITERIA]

Example:
/goal Create 5 blog posts on topic X, each 1000 words, save to /content/
Done when: 5 files exist in /content/, none empty, each >800 words
```

## Best Practices

1. **Identify Independent Parts** - What can run simultaneously?
2. **Clear Boundaries** - Each sub-agent has one job
3. **Objective Criteria** - How do we know it's done?
4. **Verify Results** - Main agent reviews all outputs
5. **No Overlap** - Sub-agents shouldn't need each other's output

## Sub-Agent Coordination

```
Main Agent: "Orchestrator"
├── Sub-agent 1: Research (parallel)
├── Sub-agent 2: Research (parallel)
├── Sub-agent 3: Build
└── Sub-agent 4: Test

All sub-agents have:
- Own context window
- Clear inputs
- Measurable outputs
- Deadlines if needed
```

## When to Use

✅ Good for parallel:
- Multiple research topics
- Independent features
- Content generation
- Data processing

❌ Not good for:
- Sequential dependencies
- Single quick tasks (overhead not worth it)
- Tasks requiring shared state

## Notes

- Sub-agents = team members
- More agents ≠ better if tasks are sequential
- Use goal to set objective completion criteria
- Separate "worker" from "judge" for honest completion assessment
