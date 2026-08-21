---
name: agent-orchestrator
description: Spawn and manage sub-agents for parallel task execution. Use when breaking down complex tasks into smaller sub-tasks that can run concurrently, monitoring sub-agent progress, collecting results, and handling failures. Ideal for multi-component builds, testing suites, and distributed workflows.
---

# Agent Orchestrator Skill

Manage sub-agents for parallel task execution.

## Quick Start

Spawn a sub-agent:
```bash
scripts/spawn-agent.sh "Build component X" component-builder
```

Check all sub-agents:
```bash
openclaw subagents list
```

## Common Patterns

### Parallel Component Build
Spawn multiple agents to build different components simultaneously:
1. Spawn agent for core-api
2. Spawn agent for frontend
3. Spawn agent for database
4. Wait for all to complete
5. Collect results

### Test Suite Distribution
Distribute tests across agents:
1. Split test files into batches
2. Spawn agent per batch
3. Collect pass/fail results
4. Generate combined report

## Best Practices

- Keep sub-agent tasks focused and independent
- Set appropriate timeouts (default: 300s)
- Use descriptive labels for tracking
- Always check results before proceeding

## Reference

See [references/patterns.md](references/patterns.md) for workflow patterns.
