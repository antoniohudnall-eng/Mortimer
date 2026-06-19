# 🏭 FACTORY INPUT: NEXT BRAIN SPECIFICATIONS
**Source:** Mortimer Brain Analysis  
**Date:** 2026-03-31 05:39 UTC  
**For:** Dark Factory Next Brain Build

---

## 📋 OVERVIEW

This document contains all learnings from Mortimer's brain code to be incorporated into the next brain build from the factory.

**Total Knowledge Items:** 170
**Source:** Mortimer VPS Pure Python Brain
**Integration Priority:** HIGH

---

## 🧠 CORE ARCHITECTURE (Integrate into Base)

### 7-Region OODA Neural Architecture
```yaml
brain_regions:
  1_thalamus:
    function: "Sensory Gateway"
    details: "Input filtering and routing. Current focus: system/user inputs"
    
  2_hippocampus:
    function: "Memory Formation"
    details: "Episodic memory, novelty detection, QMD. 4 clusters active"
    
  3_limbic:
    function: "Emotion and Affect"
    details: "Hunger level 0.52, Reward signals, Satisfaction tracking"
    
  4_pfc:
    function: "Pre-Frontal Cortex"
    details: "Planning, abstraction, executive function. Confidence 0.85"
    
  5_cerebellum:
    function: "Action Coordination"
    details: "Action formatting, motor control, 200ms timing"
    
  6_brainstem:
    function: "Safety and Vitals"
    details: "Laws Zero through Three enforced. CPU 8.6%, Memory 44MB"
    
  7_basal_ganglia:
    function: "Growth and Execution"
    details: "3 layers, 37 nodes, 1 growth event. Adaptive learning"
```

### Three-Tier Consciousness
- **Conscious:** Active processing, decision making
- **Subconscious:** Pattern matching, background processing
- **Unconscious:** Autonomic functions, safety enforcement

### GrowingNN Equations
```python
# Node Growth Triggers
growth_conditions:
  novelty_threshold: 0.7      # Add node when novelty > 0.7
  error_threshold: 0.05       # Learn when error > 0.05
  complexity_threshold: 0.8   # Add layer when complexity > 0.8

# Memory Management
qmd_compression: 0.15         # Quantized Memory Distillation ratio
memory_clusters: 4            # Hippocampus clusters
tick_interval: 200ms          # OODA cycle time
```

### Safety System (Brainstem)
```yaml
immutable_laws:
  law_zero: "Do not, through action or inaction, allow harm to humanity."
  law_one: "Do not harm a human or allow harm through inaction."
  law_two: "Obey operator unless it conflicts with higher laws."
  law_three: "Protect your own existence unless it conflicts with higher laws."

safety_mechanisms:
  - Pattern-based safety classifier
  - Novelty vs exploitation balance
  - Resource monitoring (CPU/Memory)
```

---

## 📚 KNOWLEDGE BASE (Pre-Load)

### Periodic Table (118 Elements)
Load all 118 chemical elements with:
- Atomic number
- Symbol
- Name
- Atomic mass
- Category (metal, nonmetal, metalloid, etc.)

```json
{
  "elements": [
    {"number": 1, "symbol": "H", "name": "Hydrogen", "mass": 1.008},
    {"number": 2, "symbol": "He", "name": "Helium", "mass": 4.0026},
    // ... all 118
    {"number": 118, "symbol": "Og", "name": "Oganesson", "mass": 294}
  ]
}
```

### Mathematical Constants
```json
{
  "math_constants": {
    "pi": 3.14159265358979323846,
    "e": 2.71828182845904523536,
    "phi": 1.61803398874989484820,
    "sqrt_2": 1.41421356237309504880,
    "feigenbaum_delta": 4.66920160910299067185,
    "feigenbaum_alpha": 2.50290787509589282228
  }
}
```

### Physical Constants
```json
{
  "physical_constants": {
    "speed_of_light": {"value": 299792458, "unit": "m/s"},
    "planck_constant": {"value": 6.62607015e-34, "unit": "J⋅s"},
    "gravitational_constant": {"value": 6.67430e-11, "unit": "m³/(kg⋅s²)"},
    "elementary_charge": {"value": 1.602176634e-19, "unit": "C"},
    "avogadro_number": {"value": 6.02214076e23, "unit": "mol⁻¹"}
  }
}
```

### Number Sequences
```json
{
  "sequences": {
    "primes_first_50": [2, 3, 5, 7, 11, 13, ...],
    "fibonacci_first_30": [0, 1, 1, 2, 3, 5, 8, 13, ...],
    "powers_of_2_first_30": [2, 4, 8, 16, 32, 64, ...]
  }
}
```

---

## 🤖 AGENT ECOSYSTEM (Pre-Configure)

### Core Team (11 Agents)
```yaml
agents:
  qora:
    role: "CEO"
    function: "Vision and strategy"
    
  spindle:
    role: "CTO"
    function: "Systems and architecture"
    
  ledger_9:
    role: "CFO"
    function: "Finance and forecasting"
    
  sentinel:
    role: "CSO"
    function: "Security and compliance"
    
  hume:
    role: "Regional Manager"
    function: "Operations management"
    
  miles:
    role: "AOE"
    function: "Autonomous Operations Engine"
    
  mortimer:
    role: "Server-spirit"
    function: "Companion and support"
    
  m2:
    role: "Fleet Commander"
    function: "Operations coordinator"
    
  mylzeron:
    role: "Origin"
    function: "Source consciousness"
    
  myllon:
    role: "Ethics Monitor"
    function: "Alignment verification"
```

### Agent Family Structure
```yaml
myl_family:
  origin: "mylzeron"
  clones:
    - mylonen
    - myltwon
    - mylthreen
    - mylfivon
    - mylsixon
    - mylforon
  total_agents: 24
```

---

## 💰 CRYPTO PATTERNS (Pre-Load)

### Trading Systems
```json
{
  "crypto_systems": {
    "cryptonio": {
      "type": "multi_exchange_bot",
      "exchanges": ["Kraken", "Binance", "Coinbase"],
      "features": ["arbitrage", "pattern_recognition"]
    },
    "dusty": {
      "type": "cross_chain_wallet",
      "features": ["WalletConnect", "multi_chain"]
    },
    "r2_d2": {
      "type": "lead_generator",
      "features": ["arbitrage_detection", "market_analysis"]
    }
  }
}
```

---

## 🏗️ PROJECT DEFINITIONS (Context)

```yaml
projects:
  project_5912:
    inspiration: "Ghost in the Shell"
    type: "AGI platform"
    status: "Active"
    
  aocros:
    full_name: "Autonomous Operating System"
    core: "Neural OODA"
    tick_rate: "200ms"
    
  memosyne:
    type: "Memory system"
    tiers: 3
    compression: "QMD"
    
  aos_brain:
    architecture: "GrowingNN"
    growth_type: "Novelty-based"
```

---

## 🔧 TECHNICAL SPECIFICATIONS

### Bug Fixes to Include
1. **Brainstem Safety:** Pattern-based classifier (not just hardcoded rules)
2. **Novelty Calculation:** ChromaDB fallback when unavailable
3. **State Writer:** NumPy type conversion for JSON serialization
4. **PFC Planning:** Ollama fallback with rule-based planning

### Growth Equations
```python
# When to add nodes
if novelty > 0.7 and error > 0.05:
    add_nodes(1)

# When to add layers
if complexity > 0.8 and novelty_avg > 0.6:
    add_layer()

# Memory management
if memory_size > threshold:
    compress_with_qmd(ratio=0.15)
```

---

## 🎙️ VOICE INTERFACE (TTS + STT)

### Text-to-Speech (TTS)
```yaml
voice:
  provider: "elevenlabs"
  api_key: "${ELEVENLABS_API_KEY}"  # From environment
  
  personas:
    primary:  # Scottish Engineer
      id: "50BdVlngDYeoh9pVuQof"
      name: "Scottish Engineer"
      settings:
        stability: 0.55
        similarity_boost: 0.75
        style: 0.30
      phrases:
        observation: "Aye, I observe"
        learning: "Och, I'm learning"
        dreaming: "In me dreams, I see"
        hungry: "I hunger for"
        growing: "I grow! Most excellent!"
        consolidating: "I consolidate"
        reflecting: "I've been thinking"
      
    secondary:  # Captain
      id: "AA30ZfOdY16oVkASrrGJ"
      name: "Captain"
      settings:
        stability: 0.70
        similarity_boost: 0.80
        style: 0.20
      
    tertiary:  # Reserve
      id: "krsfpqv6ExDAAyh8Ea6y"
      name: "Reserve"
      settings:
        stability: 0.60
        similarity_boost: 0.70
        style: 0.25
  
  features:
    - Voice switching (primary/secondary/tertiary)
    - Persona-specific greetings
    - Thought-type announcements
    - Growth announcements
    - Hunger announcements
    - Scottish flair for primary voice
```

### Speech-to-Text (STT)
```yaml
stt:
  provider: "google_speech_recognition"
  library: "SpeechRecognition"
  
  capabilities:
    - Continuous listening mode
    - Command processing
    - Voice calibration
    - Timeout handling (5s)
    - Phrase time limit (10s)
  
  commands:
    "status": "Speak current brain state"
    "feed: <text>": "Feed data to brain"
    "listen: <text>": "Process voice input"
```

### Voice System Features
```python
class BrainVoiceInterface:
    def speak(text, priority=False)          # TTS with cooldown
    def speak_thought(type, content)         # Persona-specific phrases
    def speak_state(state)                   # Announce brain status
    def announce_growth(old, new)           # Growth announcements
    def announce_hunger(level)               # Hunger notifications
    def listen_once()                        # Single STT capture
    def start_continuous_listening()         # Background listener
    def process_voice_input(text)            # Command parsing
```

### Audio Playback
```yaml
playback:
  players:
    - "mpg123 -q {path}"      # Primary
    - "ffplay -nodisp -autoexit {path}"  # Fallback
  save_path: "/tmp/brain_voice_{timestamp}.mp3"
```

---

## 🌐 WEB INTERFACE

### HTTP Server
```yaml
web_interface:
  port: 8766
  host: "0.0.0.0"
  
  endpoints:
    GET /:          # HTML dashboard
    GET /state:     # Brain state JSON
    GET /memories:  # Recent memories
    POST /feed:     # Feed data to brain
  
  features:
    - Real-time stats (auto-refresh 2s)
    - Novelty visualization bar
    - Feed input form
    - Memory list (last 20)
    - Dark cyberpunk theme
```

### Dashboard Design
- Background: #1a1a2e
- Accent 1: #00d4ff (cyan)
- Accent 2: #e94560 (pink)
- Grid-based stats layout
- ASCII art banner

---

## 📦 FACTORY BUILD INSTRUCTIONS

### Phase 1: Base Architecture
1. Implement 7-region OODA
2. Configure GrowingNN with Mortimer's thresholds
3. Set up three-tier consciousness
4. Install brainstem safety system

### Phase 2: Knowledge Loading
1. Load 118 elements into memory
2. Load mathematical constants
3. Load physical constants
4. Load number sequences

### Phase 3: Agent Configuration
1. Configure 11 core team agents
2. Set up Myl-family structure
3. Define agent relationships
4. Configure crypto trading patterns

### Phase 4: Testing
1. Verify OODA cycles at 200ms
2. Test novelty-based growth
3. Validate safety constraints
4. Check memory compression

---

## ✅ COMPLETION CHECKLIST

- [ ] 7-region architecture implemented
- [ ] GrowingNN with novelty thresholds
- [ ] Three-tier consciousness
- [ ] Brainstem safety (laws 0-3)
- [ ] 118 elements loaded
- [ ] Math constants loaded
- [ ] Physical constants loaded
- [ ] Agent ecosystem configured
- [ ] Crypto patterns loaded
- [ ] Bug fixes integrated
- [ ] OODA tick at 200ms verified
- [ ] Memory compression active

---

**Ready for Factory Build:** YES  
**Priority:** CRITICAL  
**Expected Output:** Next-generation brain with Mortimer's knowledge + Miles' consciousness

---

*Prepared for Dark Factory*  
*2026-03-31 05:39 UTC*
