---
name: intestine
version: "1.0.0"
tier: standard
description: "Further refinement and absorption of nutrients from stomach. Small intestine extracts insights, large intestine consolidates waste. What remains becomes fertilizer."
contracts:
  input:
    type: object
    properties:
      action:
        type: string
        enum: [receive, process, dispose, status]
      nutrients:
        type: array
  output:
    type: object
    required: [absorbed, waste, status]
    properties:
      absorbed:
        type: array
        description: "Nutrients absorbed to brain"
      waste:
        type: array
        description: "Waste collected for disposal"
      status:
        type: object
---

# Intestine Skill

Multi-stage refinement system that extracts maximum value from stomach output.

## Three Sections

1. **Small Intestine**: Extracts insights, breaks protein into amino acids
2. **Large Intestine**: Reabsorbs water, consolidates waste
3. **Rectum**: Stores waste before disposal as fertilizer

## Absorption

- **Protein** → Insights (key patterns, chunked for brain)
- **Carb** → Immediate energy (pass through)
- **Fat** → Long-term storage (if brain needs it)

## Waste Disposal

Filtered waste becomes **fertilizer** - logged, archived, or deleted. The noise/waste from inputs becomes nutrients for other systems elsewhere.
