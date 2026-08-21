---
name: tick-recovery
version: "1.0.0"
tier: diagnostic
description: "Recover brain from stalled or failed tick states by resetting regions and clearing blockages"
contracts:
  input:
    type: object
    required: [health_report]
    properties:
      health_report:
        type: object
      aggressive:
        type: boolean
        default: false
  output:
    type: object
    required: [status, actions_taken, regions_reset]
    properties:
      status: {type: string}
      actions_taken: {type: array}
      regions_reset: {type: array}
---

# Tick Recovery Skill

Emergency recovery for brain stalls, timeouts, or cascading failures.

## Recovery Actions

1. Identify stuck regions
2. Reset region state
3. Clear memory buffers if needed
4. Resume tick loop
