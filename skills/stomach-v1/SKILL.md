---
name: stomach
version: "1.0.0"
tier: standard
description: "Ternary digestive processing - filters and breaks down raw inputs into digestible nutrients for the brain. States: HUNGRY(-1), SATISFIED(0), FULL(1)"
contracts:
  input:
    type: object
    properties:
      action:
        type: string
        enum: [ingest, process, status]
      data:
        type: any
      source:
        type: string
        enum: [user, agent, sensor, system]
  output:
    type: object
    required: [status]
    properties:
      status:
        type: object
        properties:
          state: {type: string, enum: [HUNGRY, SATISFIED, FULL]}
          fullness: {type: number}
          contents: {type: integer}
      nutrients_ready:
        type: array
      waste:
        type: array
---

# Stomach Skill

Ternary digestive system that processes raw inputs before they reach the brain.

## Nutrient Types

- **Protein**: Heavy data requiring extensive processing (>500 chars)
- **Carb**: Quick energy, easily digestible (urgent queries)
- **Fat**: Long-term storage candidates (patterns, memories)

## Ternary States

- **HUNGRY (-1)**: Actively seeking input
- **SATISFIED (0)**: Processing, balanced
- **FULL (1)**: Filtering, cannot accept more

## Filtering

Low priority (<0.2) inputs become **waste** (fertilizer). High quality nutrients pass to **intestines** for further refinement.
