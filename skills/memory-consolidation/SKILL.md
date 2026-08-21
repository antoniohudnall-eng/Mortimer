---
name: memory-consolidation
version: "1.0.0"
tier: methodology
description: "Transfer important short-term memories to mid-term and long-term storage based on importance and access patterns"
contracts:
  input:
    type: object
    properties:
      force: {type: boolean, default: false}
      max_items: {type: integer, default: 100}
  output:
    type: object
    required: [consolidated_count, freed_bytes, errors]
    properties:
      consolidated_count: {type: integer}
      freed_bytes: {type: integer}
      errors: {type: array}
---

# Memory Consolidation Skill

Moves memories between tiers:
- Short-term → Mid-term (frequently accessed)
- Mid-term → Long-term (patterns, semantic meaning)
