---
name: pfc
version: "2.0.0"
tier: methodology
description: "Prefrontal cortex decision-making: evaluate options, apply ternary logic, select optimal action with reasoning"
contracts:
  input:
    type: object
    required: [context, options, signature]
    properties:
      context:
        type: object
      options:
        type: array
        items: {type: object}
      signature:
        type: object
      ollama_available:
        type: boolean
        default: false
  output:
    type: object
    required: [decision, confidence, reasoning, action]
    properties:
      decision:
        type: string
      confidence:
        type: number
        minimum: 0
        maximum: 1
      reasoning:
        type: string
      action:
        type: object
---

# PFC Skill

Prefrontal cortex decision-making. Evaluates options, applies reasoning, and selects the best course of action.

## Decision Modes

1. **Analytical** - High novelty, requires evaluation
2. **Reactive** - Urgent action required
3. **Exploratory** - Novel situation, seek information
4. **Cautious** - Risk detected, proceed carefully

## Ollama Integration

If `ollama_available=True`, the skill may use external LLM for complex reasoning.
Otherwise uses local ternary logic (faster, deterministic).
