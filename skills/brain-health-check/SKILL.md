---
name: brain-health-check
version: "1.0.0"
tier: diagnostic
description: "Check brain health metrics including tick latency, memory pressure, Ollama connectivity, and skill registry status"
contracts:
  input:
    type: object
    properties:
      detailed:
        type: boolean
        default: false
  output:
    type: object
    required: [status, metrics, recommendations, timestamp]
    properties:
      status:
        type: string
        enum: [healthy, warning, critical]
      metrics:
        type: object
        required: [tick_latency_ms, memory_usage, ollama_status, skills_registered]
        properties:
          tick_latency_ms: {type: number}
          memory_usage: {type: number}
          ollama_status: {type: string}
          skills_registered: {type: integer}
      recommendations:
        type: array
        items: {type: string}
      timestamp:
        type: number
---

# Brain Health Check

Comprehensive diagnostic skill that analyzes brain state and returns actionable health metrics.

## Metrics

1. **Tick Latency** - Time between OODA cycles (target: <200ms)
2. **Memory Usage** - Short/mid/long-term memory pressure
3. **Ollama Connectivity** - Model API responsiveness
4. **Skill Registry** - All registered skills responding
5. **GrowingNN Status** - Node growth and error rates

## Output Contract

- `status`: healthy | warning | critical
- `metrics`: Detailed measurements
- `recommendations`: List of suggested actions
- `timestamp`: Unix timestamp of check

## Recommendations

The skill returns specific recommendations based on findings:
- High latency: "Consider memory consolidation"
- Ollama timeout: "Check Ollama service status"
- Low skills: "Verify skill registry initialization"
