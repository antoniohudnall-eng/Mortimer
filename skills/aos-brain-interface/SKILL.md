---
name: aos-brain-interface
description: Interface with AOS Brain (Python) via WebSocket. Allows OpenClaw to query the three-tier consciousness system, check GrowingNN status, and interact with Miles/Mortimer/Jordan agents.
---

# AOS Brain Interface

Connects OpenClaw to the Python-based AOS Brain via WebSocket API.

## Architecture

```
User → OpenClaw Gateway → aos-brain-interface skill → WebSocket → AOS Brain (Python)
                                                              ↓
                                                        Three-Tier Consciousness
                                                        - Conscious (PFC)
                                                        - Subconscious (Hippo)
                                                        - Unconscious (Basal)
```

## Why This Separation?

- **AOS Brain (Python)**: Core consciousness, GrowingNN, real-time OODA
- **OpenClaw**: User interface, tool ecosystem, scheduling
- **This Skill**: Bridge between them

## Configuration

```yaml
# In OpenClaw config
plugins:
  entries:
    aos-brain-interface:
      config:
        brainHost: "localhost"
        brainPort: 8765
        timeoutMs: 5000
```

## Tools

### brain-query
Send a query to AOS Brain and get response.

**Input:**
```json
{
  "query": "What is the current status?",
  "context": "user asking about system health"
}
```

**Output:**
```json
{
  "response": "System operational. Tick: 1412, Nodes: 1412, Memory: 2824 clusters",
  "source": "AOS Brain v2.2.0",
  "personality": "Miles"
}
```

### brain-status
Get full GrowingNN status.

**Output:**
```json
{
  "tick": 1412,
  "nodes": 1412,
  "memory_clusters": 2824,
  "novelty": 1.0,
  "phase": "Act",
  "personality": "Miles"
}
```

### brain-memory
Query the three-tier memory system.

**Input:**
```json
{
  "query": "What do we know about Stripe integration?",
  "tier": "subconscious"  // or "all"
}
```

## Usage Examples

**Check brain status:**
```
What's the status of the AOS Brain?
```

**Query consciousness:**
```
Ask Miles about the GrowingNN growth rate.
```

**Check memory:**
```
What does the brain remember about our Stripe research?
```

## Requirements

- AOS Brain must be running (WebSocket on ws://localhost:8765)
- Network connectivity to brain host

## Error Handling

If brain is unreachable:
- Returns error: "AOS Brain not responding"
- Suggests: "Check if brain is running: tmux list-sessions"

## Security

- Only queries, no modifications
- Read-only interface
- No access to vault/credentials
