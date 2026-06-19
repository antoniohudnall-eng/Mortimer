# N'og nog v3 Architecture

**Version:** 3.0.0  
**Date:** 2026-04-07  
**Status:** Design Phase

## Overview

N'og nog v3 is the next evolution of the Universal Explorer, designed for multi-agent exploration across infinite procedurally-generated universes.

## Core Principles

1. **Multi-Universe:** Parallel universe instances with persistence
2. **Agent-Native:** First-class support for AI agents (Brain, Mineflayer, etc.)
3. **Scalable:** Handle 100+ concurrent agents
4. **Persistent:** World state survives player disconnects
5. **Extensible:** Plugin architecture for new universe types

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  WebGL   │  │  Mobile  │  │  Desktop │  │   VR     │   │
│  │  Client  │  │   App    │  │  Client  │  │  Client  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼──────────────┼──────────────┼──────────────┼─────────┘
        │              │              │              │
        └──────────────┴──────┬───────┴──────────────┘
                              │
┌─────────────────────────────▼──────────────────────────────┐
│                   GATEWAY LAYER                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │              WebSocket Gateway (ws://:7777)           │ │
│  │  - Client connection management                     │ │
│  │  - Message routing                                  │ │
│  │  - Rate limiting                                    │ │
│  └──────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼──────────────────────────────┐
│                 UNIVERSE ENGINE                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │              Universe Manager                        │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │ │
│  │  │Instance1│ │Instance2│ │Instance3│ │   ...   │  │ │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘  │ │
│  └───────┼───────────┼──────────┼──────────┼───────┘ │
│          │           │          │          │          │
│  ┌───────▼───────────▼──────────▼──────────▼───────┐ │
│  │              Voxel Universe (10000³)           │ │
│  │  - Procedural generation                       │ │
│  │  - Persistence layer                            │ │
│  │  - Event streaming                              │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼──────────────────────────────┐
│                   AGENT LAYER                              │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌────────┐ │
│  │AOS Brain  │  │ Mineflayer│  │  Custom   │  │  Human │ │
│  │   v4.x    │  │  Agents   │  │   Bots    │  │Players │ │
│  └───────────┘  └───────────┘  └───────────┘  └────────┘ │
│                                                            │
│  Agent Protocol: OODA Loop (Observe → Orient → Decide → Act)│
└────────────────────────────────────────────────────────────┘
```

## Universe Types (v3)

| Type | Description | Agent Support |
|------|-------------|---------------|
| **Prime** | Original 10000³ voxel space | Full |
| **Bubble** | Isolated pocket universes | Full |
| **Nexus** | Hub worlds for agent trade | Multi-agent |
| **Combat** | PvP/PvE battle zones | Arena AI |
| **Resource** | Mining/extraction zones | Worker agents |

## Data Flow

```
Agent Decision
      ↓
Brain/Bridge (OODA)
      ↓
Gateway (WebSocket)
      ↓
Universe Engine
      ↓
Voxel World Update
      ↓
Event Broadcast
      ↓
All Clients/Agents
```

## File Structure

```
nognog/v3/
├── src/
│   ├── core/
│   │   ├── UniverseEngine.js
│   │   ├── VoxelWorld.js
│   │   └── Persistence.js
│   ├── gateway/
│   │   ├── WebSocketServer.js
│   │   └── MessageRouter.js
│   └── agents/
│       ├── AgentProtocol.js
│       └── SpawnManager.js
├── agents/
│   ├── brain-avatar/
│   │   └── ooda_agent.py
│   └── mineflayer-bridge/
│       └── index.js
├── universes/
│   └── templates/
├── docs/
│   └── API.md
└── shared/
    └── protocols/
```

## Portal System (v1 → v3 Migration)

Portals in v1 connect regions within a universe.  
Portals in v3 connect **universes**.

```javascript
// v1 Portal (intra-universe)
{
    id: 'alpha',
    from: [x, y, z],
    to: [x, y, z],
    type: 'sector-swap'
}

// v3 Portal (inter-universe)
{
    id: 'nexus-alpha',
    from: { universe: 'prime-1', pos: [x, y, z] },
    to: { universe: 'nexus-hub', pos: [x, y, z] },
    type: 'universe-bridge',
    requirements: ['level > 10']
}
```

## API (Planned)

```javascript
// Connect to v3 Gateway
const ng3 = new NognogV3({
    gateway: 'ws://myl0nr0s.cloud:7777',
    agent: 'brain-v4.4'
});

// Spawn agent in universe
await ng3.spawn({
    universe: 'prime-1',
    position: [5000, 200, 5000],
    faction: 'explorers'
});

// Subscribe to events
ng3.on('portal_nearby', (data) => {
    // Brain decides: use portal?
});

// Send action
ng3.act({
    type: 'move',
    target: [x, y, z]
});
```

## Development Phases

| Phase | Feature | ETA |
|-------|---------|-----|
| v3.0-alpha | Gateway + basic universe | 2026-04-14 |
| v3.0-beta | Multi-agent support | 2026-04-21 |
| v3.0-rc | Persistence + portals | 2026-04-28 |
| v3.0 | Production release | 2026-05-05 |

## Migration from v1

1. Portals become universe bridges
2. Agent protocol upgraded to v3
3. Save files migrate to new format
4. WebSocket replaces socket files

---

*Document version: 1.0*  
*Next review: 2026-04-14*
