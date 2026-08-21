---
name: brain-integration
version: "1.0.0"
tier: methodology
description: "Unified interface for agents to discover and call brain skills, check health, and submit sensory data"
contracts:
  input:
    type: object
    oneOf:
      - $ref: "#/definitions/sensory_input"
      - $ref: "#/definitions/decision_request"
      - $ref: "#/definitions/health_check"
  output:
    type: object
    required: [status, result]
definitions:
  sensory_input:
    type: object
    required: [type, source, data]
    properties:
      type: {const: "sensory"}
      source: {type: string}
      data: {type: any}
      priority: {type: number}
  decision_request:
    type: object
    required: [type, context, options]
    properties:
      type: {const: "decision"}
      context: {type: object}
      options: {type: array}
  health_check:
    type: object
    required: [type]
    properties:
      type: {const: "health"}
      detailed: {type: boolean}
---

# Brain Integration Skill

Provides agents with unified access to brain capabilities.

## Capabilities Exposed

1. **Sensory Processing** - Submit observations to brain
2. **Decision Making** - Request PFC evaluation
3. **Health Monitoring** - Check brain status
4. **Recovery** - Trigger self-healing (privileged)

## Usage

```python
client = BrainClient()

# Submit observation
result = client.process_sensory('agent', data, priority=0.8)

# Get decision
decision = client.request_decision(context, options)
```
