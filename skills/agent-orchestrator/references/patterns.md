# Agent Orchestration Patterns

## Pattern 1: Fan-Out / Fan-In

Spawn multiple agents in parallel, wait for all to complete.

```
Phase 1: Fan-Out
├── Spawn Agent A (task 1)
├── Spawn Agent B (task 2)
└── Spawn Agent C (task 3)

Phase 2: Fan-In
└── Collect all results
```

## Pattern 2: Pipeline

Chain agents where output of one feeds into next.

```
Agent 1 (Data Fetch) → Agent 2 (Transform) → Agent 3 (Store)
```

## Pattern 3: Map-Reduce

Distribute data processing, then aggregate results.

```
Map Phase:
├── Agent 1 processes chunk 1
├── Agent 2 processes chunk 2
└── Agent 3 processes chunk 3

Reduce Phase:
└── Agent 4 aggregates all results
```

## Pattern 4: Failover

Primary agent with backup on failure.

```
Try Agent A
└── If fails, spawn Agent B
```
