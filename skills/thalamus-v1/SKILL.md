---
name: thalamus
version: "1.0.0"
tier: standard
description: "Normalize and route sensory input to appropriate brain regions based on priority and content type"
contracts:
  input:
    type: object
    required: [source, data, timestamp]
    properties:
      source:
        type: string
        enum: [sensor, agent, system, user]
      data:
        type: any
      timestamp:
        type: number
      priority:
        type: number
        minimum: 0
        maximum: 1
        default: 0.5
  output:
    type: object
    required: [normalized, priority, routing, signature]
    properties:
      normalized:
        type: object
      priority:
        type: number
      routing:
        type: array
        items: {type: string}
      signature:
        type: object
---

# Thalamus Skill

Sensory relay and routing skill. Normalizes incoming data and determines which brain regions should process it.

## Routing Logic

- **sensor** data → hippocampus, pfc
- **agent** data → pfc, limbic
- **system** data → brainstem, pfc
- **user** data → pfc, limbic

## Signature

Produces a ternary signature: [novelty, value, action, risk, growth]
