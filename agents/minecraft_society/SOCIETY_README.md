# Minecraft Society Simulation v1.0

A civilization-building multi-agent system for Minecraft featuring 5 autonomous agents (3 male, 2 female) with reproduction, society building, and civilization progression.

## 🏛️ Society Members

| Name | Gender | Role | Personality | Color |
|------|--------|------|-------------|-------|
| **Marcus** | ♂ Male | Leader | Charismatic | Gold §6 |
| **Julius** | ♂ Male | Builder | Diligent | Dark Green §2 |
| **Titus** | ♂ Male | Guardian | Brave | Red §4 |
| **Julia** | ♀ Female | Farmer | Nurturing | Green §a |
| **Livia** | ♀ Female | Explorer | Curious | Aqua §b |

## 🌟 Features

### Gender & Reproduction
- **3 Male agents** (Marcus, Julius, Titus)
- **2 Female agents** (Julia, Livia)
- Partnership formation when compatible agents meet
- Child birth when partnerships form and needs are met
- Children inherit traits and can form new partnerships

### Needs System
Each agent tracks:
- **Hunger** - Requires food (hunting/farming)
- **Energy** - Rest required to recover
- **Social** - Interactions with other agents
- **Shelter** - Home building when resources allow

### Role-Based Behaviors

**Leader (Marcus)**
- Gathers other agents for coordination
- Announces civilization milestones
- Monitors settlement health

**Builder (Julius)**
- Collects wood and stone resources
- Constructs dwellings and structures
- Advances civilization through building

**Guardian (Titus)**
- Patrols settlement perimeter
- Engages hostile mobs
- Defends other agents

**Farmer (Julia)**
- Cultivates crops
- Hunts animals for food
- Feeds the settlement

**Explorer (Livia)**
- Maps surrounding territory
- Discovers resources
- Brings knowledge back

### Civilization Progression

| Tier | Name | Requirements | Unlocks |
|------|------|--------------|---------|
| 0 | Nomadic | Starting state | - |
| 1 | Tribal | 50 resources, 1 structure | Toolmaking |
| 2 | Village | 150 resources, 2 structures | Pottery, Weaving |
| 3 | Town | 300 resources, 5 structures, 7+ population | Agriculture, Masonry, Writing |

## 📁 Files

```
minecraft_agents/
├── society_agent.js         # Main agent code (each agent runs this)
├── society_server.py        # Society coordination server
├── society_rotation.py      # Agent launcher
├── SOCIETY_README.md        # This file
├── simple_agent.js          # Original simple agent (backup)
├── simple_brain_server.py   # Original brain server (backup)
└── spawn_three_agents.sh    # Original launcher (backup)
```

## 🚀 Quick Start

### Prerequisites
- Minecraft server running on localhost:25566
- Node.js with mineflayer installed
- Python 3 with websockets

### Start the Society

```bash
cd /root/.openclaw/workspace/scripts/minecraft_agents

# Start all 5 society agents
python3 society_rotation.py
```

This will:
1. Start the Society Coordination Server (port 8768)
2. Start the Brain Server for compatibility (port 8767)
3. Launch all 5 agents with staggered timing
4. Begin the civilization simulation

### Check Status

```bash
python3 society_rotation.py status
```

### Stop All Agents

```bash
python3 society_rotation.py stop

# Or force kill:
pkill -f society_agent.js
pkill -f society_server.py
```

## 🎮 In-Game Commands

Agents respond to chat messages:

```
say society status  - Agents announce civilization progress
say Marcus come     - Marcus moves to your position
say Julia follow    - Julia follows you
```

## 📊 Logs

| Log File | Contents |
|----------|----------|
| `society_rotation.log` | Rotation system events |
| `society_server.log` | Society coordination events |
| `marcus.log` | Agent Marcus activities |
| `julius.log` | Agent Julius activities |
| `titus.log` | Agent Titus activities |
| `julia.log` | Agent Julia activities |
| `livia.log` | Agent Livia activities |

Location: `/root/.openclaw/workspace/logs/`

## 🔧 Architecture

```
┌─────────────────────────────────────────────┐
│           Society Coordination Server        │
│                 (port 8768)                  │
│  • Partnership management                    │
│  • Reproduction logic                        │
│  • Civilization progression                  │
│  • Event logging                             │
└─────────────────┬─────────────────────────────┘
                  │ WebSocket
        ┌─────────┼─────────┐
        │         │         │
   ┌────▼────┐ ┌──▼───┐ ┌──▼───┐
   │ Marcus  │ │Julius│ │Titus │  (Male agents)
   │ ♂ Leader│ │♂Build│ │♂Guard│
   └────┬────┘ └──────┘ └──────┘
        │
   ┌────▼────┐ ┌──────┐
   │ Julia   │ │Livia │  (Female agents)
   │♀ Farmer │ │♀Explr│
   └────┬────┘ └──────┘
        │
        ▼
   ┌─────────────────┐
   │ Minecraft World │
   │ (localhost:25566)│
   └─────────────────┘
```

## 🔬 How It Works

### Relationship Building
- Agents gain bond strength when near each other
- Partnerships form when male+female agents meet with sufficient social need
- Partners are tracked and children can be born

### Reproduction Conditions
1. Male + Female partnership formed
2. Both agents have hunger > 5
3. Both agents have social need > 30
4. Bond strength > 20
5. 30% chance every 30 seconds

### Civilization Advancement
- Resources collected by agents count toward progression
- Structures built unlock new technologies
- Population growth through reproduction
- All agents notified of tier advancements

## 🛠️ Customization

### Change Agent Names/Roles
Edit the `SOCIETY_AGENTS` dictionary in both:
- `society_agent.js` (line ~35)
- `society_server.py` (line ~15)

### Modify Reproduction Rate
Edit `REPRODUCTION_CHANCE` in `society_server.py` (line ~15)

### Adjust Needs Decay
Edit `updateNeeds()` in `society_agent.js` (line ~105)

## 🐛 Troubleshooting

**Agents not connecting**
- Check Minecraft server is running on port 25566
- Verify Node.js and mineflayer are installed
- Check logs in `/root/.openclaw/workspace/logs/`

**Society server not starting**
- Ensure Python websockets module: `pip install websockets`
- Check port 8768 is not in use: `ss -tlnp | grep 8768`

**Agents not interacting**
- Verify they're in the same area (check positions in logs)
- Social needs must be high enough for partnership
- Different genders required for reproduction

## 📜 License

Part of the AOS (Autonomous Operations System) project.

## 🙏 Credits

Built on:
- [Mineflayer](https://github.com/PrismarineJS/mineflayer) - Minecraft bot framework
- [OpenClaw](https://github.com/openclaw/openclaw) - Agent orchestration system
