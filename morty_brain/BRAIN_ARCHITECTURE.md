# Morty Brain - 7-Region Architecture

## The 7 Brain Regions (AOCROS)

| Region | Function | In Body |
|--------|----------|---------|
| 1. **Thalamus** | Sensory Relay | Routes input |
| 2. **Hippocampus** | Episodic Memory | Stores experiences |
| 3. **Limbic** | Affect/Emotion | Reward/novelty |
| 4. **PFC** | Prefrontal Cortex | Decision making |
| 5. **Basal Ganglia** | Habits/Auto | Pattern automation |
| 6. **Cerebellum** | Motor Control | Coordination |
| 7. **Brainstem** | Survival/Instinct | Safety, life support |

---

## Three-Tier Consciousness Layers

| Layer | Brain Regions | Function |
|-------|--------------|----------|
| **CONSCIOUS** | PFC, Cerebellum | Active thinking, decisions |
| **SUBCONSCIOUS** | Hippocampus, Thalamus | Working memory, relay |
| **UNCONSCIOUS** | Limbic, Basal, Brainstem | Emotions, habits, survival |

---

## Current Implementation Status

### Already Implemented
- ✅ Consciousness Layers (CONSCIOUS/SUBCONSCIOUS/UNCONSCIOUS)
- ✅ TracRay (trajectory recording)
- ✅ Cortex 3D (spatial consciousness)

### Need to Add
- ❌ Thalamus Region
- ❌ Hippocampus Region  
- ❌ Limbic Region
- ❌ PFC Region
- ❌ Basal Ganglia Region
- ❌ Cerebellum Region
- ❌ Brainstem Region

---

## Data Structures

### Observation
```python
{
    'input': str,
    'source': str,
    'timestamp': float,
    'metadata': {}
}
```

### Decision
```python
{
    'type': str,  # respond, act, noop, halt, query, learn
    'reason': str,
    'confidence': float,
    'action': {},
    'safety_override': bool
}
```

### Affect
```python
{
    'reward': float,
    'novelty': float,
    'mode': str,  # adaptive, creative, defensive
    'novelty_avg': float,
    'reward_avg': float
}
```

### MemoryTrace
```python
{
    'tick': int,
    'observation': {},
    'affect': {},
    'decision': {},
    'result': {}
}
```

---

## Brain State Output

```python
{
    'tick': int,
    'timestamp': float,
    'phase': str,  # observe, orient, decide, act
    'mode': str,   # adaptive, creative, defensive
    
    'regions': {
        'thalamus': {},
        'hippocampus': {},
        'limbic': {},
        'pfc': {},
        'basal': {},
        'cerebellum': {},
        'brainstem': {}
    },
    
    'decision': {},
    'result': {}
}
```

---

## Pipeline Integration

```
INPUT → [THALAMUS] → [HIPPOCAMPUS] → [LIMBIC] → [PFC] → [BASAL] → [CEREBELLUM] → [BRAINSTEM] → OUTPUT
        Relay      Memory       Emotion   Decision  Habits   Motor      Survival
```

---

*Last Updated: 2026-06-19*
*Morty Brain v2.2 - 7-Region AOCROS Architecture*