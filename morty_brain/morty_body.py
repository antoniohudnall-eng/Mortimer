#!/usr/bin/env python3
"""
Morty Body v2.1 - AOCROS-Aligned Organ System
==============================================
Pipeline: [LUNGS] → [LIVER] → [BRAIN] → [KIDNEYS]
         INHALE      FILTER     PROCESS    RECYCLE
         GAS_EX      PURIFY     DECIDE     EXCRETE
         EXHALE      TOXIC      ACT        REABSORB

Version: 2.1 - Health metrics, stress response, recovery

Author: Mortimer (C3 - SEED3)
Started: 2026-06-19
"""

import json
import time
import random
import hashlib
from datetime import datetime, UTC
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
import math

# Paths
BASE_DIR = Path.home() / "mortimer" / "morty_brain"
WASTE_DIR = BASE_DIR / "waste"
WASTE_DIR.mkdir(parents=True, exist_ok=True)

# ============ VERSION INFO ============
VERSION = "2.3"
VERSION_DATE = "2026-06-19"
VERSION_NOTES = "All 7 brain regions: Thalamus/Hippocampus/Limbic/PFC/Basal/Cerebellum/Brainstem"

ORGAN_VERSIONS = {
    "Lungs": "v1.0",
    "Liver": "v1.0", 
    "Brain": "v3.1",
    "Kidneys": "v1.0",
    "SuperiorHeart": "Ternary",
    "Stomach": "v2",
    "Intestine": "v2",
    "Thyroid": "v1.2",
    "Cortex": "3D",
    "TracRay": "—",
    "ModelRouter": "—",
    "Consciousness": "v1.0",
    "Thalamus": "v1.0",
    "Hippocampus": "v1.0",
    "Limbic": "v1.0",
    "PFC": "v1.0",
    "BasalGanglia": "v1.0",
    "Cerebellum": "v1.0",
    "Brainstem": "v1.0"
}

# ============ ENUMS ============

class LungState(Enum):
    INHALE = "inhale"
    GAS_EXCHANGE = "gas_exchange"
    EXHALE = "exhale"

class LiverState(Enum):
    CLEAN = "clean"
    PURIFY = "purify"
    TOXIC = "toxic"

class KidneyState(Enum):
    FILTER = "filter"
    REABSORB = "reabsorb"
    EXCRETE = "excrete"

class HeartState(Enum):
    REST = "rest"
    BALANCE = "balance"
    ACTIVE = "active"

class BrainPhase(Enum):
    OBSERVE = "observe"
    ORIENT = "orient"
    DECIDE = "decide"
    ACT = "act"

# ============ HEALTH MIXIN ============

class HealthMixin:
    """Health tracking for organs."""
    
    def __init__(self):
        self.health: float = 1.0  # 0-1
        self.max_health: float = 1.0
        self.recovery_rate: float = 0.01
        self.stress_level: float = 0.0
    
    def damage(self, amount: float):
        """Take damage, reduce health."""
        self.health = max(0, self.health - amount)
        self.stress_level = min(1.0, self.stress_level + amount * 0.5)
    
    def heal(self, amount: float):
        """Recover health."""
        self.health = min(self.max_health, self.health + amount)
        self.stress_level = max(0, self.stress_level - amount * 0.3)
    
    def tick_recovery(self):
        """Tick for recovery."""
        if self.stress_level > 0:
            self.heal(self.recovery_rate * 0.5)
        if self.health < self.max_health:
            self.heal(self.recovery_rate)
    
    def get_health_status(self) -> str:
        """Get health as percentage string."""
        pct = self.health * 100
        if pct >= 90: return "Excellent"
        elif pct >= 70: return "Good"
        elif pct >= 50: return "Fair"
        else: return "Critical"

# ============ LUNGS v1.0 ============

class Lungs(HealthMixin):
    """Respiratory System v1.0 - States: INHALE → GAS_EXCHANGE → EXHALE"""
    
    version = "v1.0"
    
    def __init__(self):
        super().__init__()
        self.state = LungState.INHALE
        self.breath_count = 0
        self.oxygen_level = 0.98
        self.co2_level = 0.02
        self.tidal_volume = 500
        self.vital_capacity = 4800
        self.last_breath = time.time()
    
    def breathe(self) -> Dict:
        """Process one breath cycle."""
        self.breath_count += 1
        
        if self.state == LungState.INHALE:
            self.state = LungState.GAS_EXCHANGE
            action = "INHALE"
            self.oxygen_level = min(1.0, self.oxygen_level + 0.02)
            # Breathing uses energy
            self.damage(0.001)
            
        elif self.state == LungState.GAS_EXCHANGE:
            self.state = LungState.EXHALE
            action = "GAS_EXCHANGE"
            self.oxygen_level = min(0.99, self.oxygen_level + 0.01)
            
        else:
            self.state = LungState.INHALE
            action = "EXHALE"
            self.co2_level = min(0.1, self.co2_level + 0.005)
        
        self.last_breath = time.time()
        self.tick_recovery()
        
        return {
            'state': self.state.value.upper(),
            'action': action,
            'oxygen': self.oxygen_level,
            'co2': self.co2_level,
            'breath_count': self.breath_count,
            'health': self.health,
            'health_status': self.get_health_status()
        }
    
    def get_status(self) -> Dict:
        return {
            'version': self.version,
            'state': self.state.value.upper(),
            'oxygen_level': self.oxygen_level,
            'co2_level': self.co2_level,
            'breath_count': self.breath_count,
            'health': f"{self.health*100:.0f}%",
            'health_status': self.get_health_status(),
            'stress': f"{self.stress_level*100:.0f}%"
        }

# ============ LIVER v1.0 ============

class Liver(HealthMixin):
    """Pre-Brain Filtration v1.0 - States: CLEAN → PURIFY → TOXIC"""
    
    version = "v1.0"
    
    def __init__(self):
        super().__init__()
        self.state = LiverState.CLEAN
        self.total_filtered = 0
        self.toxins_removed = 0
        self.clean_passes = 0
        self.purify_passes = 0
        self.toxin_load = 0.0
        self.detox_rate = 0.1
    
    def filter(self, data: str) -> Tuple[str, str]:
        """Filter data through liver."""
        self.total_filtered += 1
        
        data_length = len(data)
        entropy = len(set(data)) / max(len(data), 1)
        
        if entropy > 0.8 and data_length > 1000:
            self.state = LiverState.TOXIC
            self.toxin_load = min(1.0, self.toxin_load + 0.1)
            self.toxins_removed += 1
            self.damage(0.02)  # Toxic hurts liver
            return data[:len(data)//2], "TOXIC_REMOVED"
        
        elif entropy > 0.6:
            self.state = LiverState.PURIFY
            self.purify_passes += 1
            self.toxin_load = max(0, self.toxin_load - self.detox_rate * 0.5)
            return data, "PURIFIED"
        
        else:
            self.state = LiverState.CLEAN
            self.clean_passes += 1
            self.toxin_load = max(0, self.toxin_load - self.detox_rate)
            return data, "CLEAN"
    
    def tick(self):
        """Liver detoxification tick."""
        if self.toxin_load > 0:
            self.toxin_load = max(0, self.toxin_load - self.detox_rate)
        self.tick_recovery()
    
    def get_status(self) -> Dict:
        return {
            'version': self.version,
            'state': self.state.value.upper(),
            'total_filtered': self.total_filtered,
            'toxins_removed': self.toxins_removed,
            'toxin_load': f"{self.toxin_load*100:.1f}%",
            'health': f"{self.health*100:.0f}%",
            'health_status': self.get_health_status(),
            'stress': f"{self.stress_level*100:.0f}%"
        }

# ============ KIDNEYS v1.0 ============

class Kidneys(HealthMixin):
    """Post-Brain Waste v1.0 - States: FILTER → REABSORB → EXCRETE"""
    
    version = "v1.0"
    
    def __init__(self):
        super().__init__()
        self.state = KidneyState.FILTER
        self.total_processed = 0
        self.patterns_recycled = 0
        self.patterns_excreted = 0
        self.bladder_level = 0
        self.bladder_capacity = 500
        self.noise_estimate = 0.5
        self.unique_patterns = 0
        self.pattern_memory: set = set()
    
    def process(self, output: str) -> Dict:
        """Process brain output."""
        self.total_processed += 1
        
        if self.state == KidneyState.FILTER:
            pattern_hash = hashlib.md5(output.encode()).hexdigest()[:16]
            if len(self.pattern_memory) < 100000:
                self.pattern_memory.add(pattern_hash)
                self.unique_patterns = len(self.pattern_memory)
            self.state = KidneyState.REABSORB
            return {'action': 'FILTER', 'recycled': True}
            
        elif self.state == KidneyState.REABSORB:
            self.patterns_recycled += 1
            self.bladder_level = min(self.bladder_capacity, self.bladder_level + 1)
            self.state = KidneyState.EXCRETE
            return {'action': 'REABSORB', 'recycled': True}
            
        else:
            self.patterns_excreted += 1
            self.bladder_level = max(0, self.bladder_level - 10)
            self.state = KidneyState.FILTER
            self.noise_estimate = max(0.1, min(0.9, self.noise_estimate + random.uniform(-0.1, 0.1)))
            self.tick_recovery()
            return {'action': 'EXCRETE', 'recycled': False}
    
    def dump(self, force: bool = False) -> bool:
        """Dump bladder."""
        if self.bladder_level >= self.bladder_capacity or force:
            self.bladder_level = 0
            self.state = KidneyState.EXCRETE
            return True
        return False
    
    def get_status(self) -> Dict:
        return {
            'version': self.version,
            'state': self.state.value.upper(),
            'total_processed': self.total_processed,
            'patterns_recycled': self.patterns_recycled,
            'patterns_excreted': self.patterns_excreted,
            'bladder': f"{self.bladder_level}/{self.bladder_capacity}",
            'noise_estimate': f"{self.noise_estimate:.4f}",
            'unique_patterns': self.unique_patterns,
            'health': f"{self.health*100:.0f}%",
            'health_status': self.get_health_status(),
            'stress': f"{self.stress_level*100:.0f}%"
        }

# ============ SUPERIOR HEART (Ternary) ============

class SuperiorHeart(HealthMixin):
    """Emotional Rhythm - Ternary: REST → BALANCE → ACTIVE"""
    
    version = "Ternary"
    
    def __init__(self):
        super().__init__()
        self.state = HeartState.BALANCE
        self.bpm = 72
        self.resting_bpm = 72
        self.max_bpm = 180
        self.beats_total = 0
        self.coherence = 0.85
        self.energy_level = 0.85
        self.coherence_history: List[float] = []
    
    def beat(self) -> Dict:
        """One heartbeat."""
        self.beats_total += 1
        
        if self.state == HeartState.REST:
            self.bpm = max(60, self.resting_bpm - 10)
            self.energy_level = min(1.0, self.energy_level + 0.001)
        elif self.state == HeartState.ACTIVE:
            self.bpm = min(self.max_bpm, self.resting_bpm + 40)
            self.energy_level = max(0, self.energy_level - 0.005)
            self.damage(0.002)  # Stress damages heart
        else:
            self.bpm = self.resting_bpm
        
        self.coherence = 0.8 + random.uniform(-0.1, 0.1) * (1 - self.energy_level)
        self.coherence_history.append(self.coherence)
        if len(self.coherence_history) > 100:
            self.coherence_history.pop(0)
        
        self.tick_recovery()
        
        return {
            'state': self.state.value.upper(),
            'bpm': self.bpm,
            'coherence': self.coherence,
            'energy': f"{self.energy_level*100:.0f}%",
            'beats': self.beats_total,
            'health': f"{self.health*100:.0f}%",
            'health_status': self.get_health_status()
        }
    
    def set_state(self, state: HeartState):
        self.state = state
    
    def get_status(self) -> Dict:
        return {
            'version': self.version,
            'state': self.state.value.upper(),
            'bpm': self.bpm,
            'coherence': f"{self.coherence:.1%}",
            'energy': f"{self.energy_level*100:.0f}%",
            'beats_total': self.beats_total,
            'health': f"{self.health*100:.0f}%",
            'health_status': self.get_health_status(),
            'stress': f"{self.stress_level*100:.0f}%"
        }

# ============ STOMACH v2 ============

class Stomach(HealthMixin):
    """Information Digestion v2"""
    
    version = "v2"
    
    def __init__(self):
        super().__init__()
        self.queue_size = 0
        self.items_processed = 0
        self.priority_queue: List = []
        self.fullness = 0.0
    
    def digest(self, item: str, priority: int = 5) -> Dict:
        """Add item to queue."""
        self.queue_size += 1
        self.items_processed += 1
        self.fullness = min(1.0, self.fullness + 0.05)
        
        self.priority_queue.append({'item': item, 'priority': priority})
        self.priority_queue.sort(key=lambda x: x['priority'])
        
        self.tick_recovery()
        
        return {
            'queued': True,
            'queue_size': self.queue_size,
            'fullness': f"{self.fullness*100:.0f}%"
        }
    
    def get_status(self) -> Dict:
        return {
            'version': self.version,
            'queue_size': self.queue_size,
            'items_processed': self.items_processed,
            'fullness': f"{self.fullness*100:.0f}%",
            'health': f"{self.health*100:.0f}%",
            'health_status': self.get_health_status()
        }

# ============ INTESTINE v2 ============

class Intestine(HealthMixin):
    """Nutrient Distribution v2"""
    
    version = "v2"
    
    def __init__(self):
        super().__init__()
        self.absorption_rate = 0.9
        self.nutrients_distributed = 0
        self.waste_produced = 0.0
        self.to_brain = 0.5
        self.to_heart = 0.3
        self.to_system = 0.2
    
    def distribute(self, nutrients: float) -> Dict:
        """Distribute nutrients."""
        self.nutrients_distributed += 1
        
        brain_nutrients = nutrients * self.to_brain
        heart_nutrients = nutrients * self.to_heart
        system_nutrients = nutrients * self.to_system
        waste = nutrients * (1 - self.absorption_rate)
        self.waste_produced += waste
        
        self.tick_recovery()
        
        return {
            'brain': f"{brain_nutrients:.2f}",
            'heart': f"{heart_nutrients:.2f}",
            'system': f"{system_nutrients:.2f}",
            'waste': f"{waste:.3f}"
        }
    
    def get_status(self) -> Dict:
        return {
            'version': self.version,
            'absorption_rate': f"{self.absorption_rate*100:.0f}%",
            'nutrients_distributed': self.nutrients_distributed,
            'waste_produced': f"{self.waste_produced:.2f}",
            'health': f"{self.health*100:.0f}%",
            'health_status': self.get_health_status()
        }

# ============ THYROID v1.2 ============

class Thyroid(HealthMixin):
    """Endocrine Regulation v1.2"""
    
    version = "v1.2"
    
    def __init__(self):
        super().__init__()
        self.t3_level = 0.5
        self.t4_level = 0.5
        self.metabolism = 0.5
        self.stimulation_output = 0.5
    
    def regulate(self, qmd_activity: float) -> Dict:
        """Regulate based on QMD activity."""
        target_metabolism = qmd_activity
        self.metabolism = self.metabolism * 0.9 + target_metabolism * 0.1
        
        if self.metabolism < 0.3:
            self.t3_level = min(1.0, self.t3_level + 0.1)
            self.t4_level = min(1.0, self.t4_level + 0.1)
            self.stimulation_output = 0.8
        elif self.metabolism > 0.7:
            self.t3_level = max(0, self.t3_level - 0.1)
            self.t4_level = max(0, self.t4_level - 0.1)
            self.stimulation_output = 0.3
        else:
            self.stimulation_output = 0.5
        
        self.tick_recovery()
        
        return {
            't3': f"{self.t3_level:.2f}",
            't4': f"{self.t4_level:.2f}",
            'metabolism': f"{self.metabolism*100:.0f}%",
            'stimulation': f"{self.stimulation_output*100:.0f}%"
        }
    
    def get_status(self) -> Dict:
        return {
            'version': self.version,
            't3_level': self.t3_level,
            't4_level': self.t4_level,
            'metabolism': f"{self.metabolism*100:.0f}%",
            'stimulation_output': f"{self.stimulation_output*100:.0f}%",
            'health': f"{self.health*100:.0f}%",
            'health_status': self.get_health_status()
        }

# ============ SEVEN BRAIN REGIONS (AOCROS) ============

class ThalamusRegion:
    """
    Region 1: THALAMUS - Sensory Relay
    ==================================
    Receives all sensory input, normalizes it, routes to appropriate regions.
    Acts as the brain's switchboard.
    """
    version = "v1.0"
    
    def __init__(self):
        self.input_queue = []
        self.last_input_time = 0
        self.sensory_weights = {
            'visual': 0.3,
            'audio': 0.3,
            'text': 0.4
        }
    
    def observe(self) -> Optional[Dict]:
        """Check for sensory input."""
        if self.input_queue:
            return self.input_queue.pop(0)
        return None
    
    def queue_input(self, text: str, source: str = "text") -> Dict:
        """Queue new sensory input."""
        obs = {
            'input': text,
            'source': source,
            'timestamp': time.time(),
            'priority': 0.5
        }
        self.input_queue.append(obs)
        self.last_input_time = time.time()
        return obs
    
    def process(self, data: str) -> Dict:
        """Process input through thalamus."""
        obs = self.queue_input(data, "brain")
        
        # Normalize priority based on content
        priority = 0.5
        if "urgent" in data.lower() or "!" in data:
            priority = 0.9
        elif "?" in data:
            priority = 0.6
        
        return {
            'normalized': True,
            'priority': priority,
            'routing': ['hippocampus', 'limbic', 'pfc'],
            'observation': obs
        }
    
    def get_status(self) -> Dict:
        return {
            'queue_size': len(self.input_queue),
            'last_input': self.last_input_time
        }


class HippocampusRegion:
    """
    Region 2: HIPPOCAMPUS - Episodic Memory
    =========================================
    Stores and retrieves episodic memories.
    Handles spatial navigation and memory consolidation.
    """
    version = "v1.0"
    
    def __init__(self):
        self.episodic_buffer = []
        self.max_buffer = 1000
        self.cluster_count = 0
        self.memory_index = {}
    
    def store(self, trace: Dict) -> None:
        """Store a memory trace."""
        self.episodic_buffer.append(trace)
        if len(self.episodic_buffer) > self.max_buffer:
            self.episodic_buffer.pop(0)
        
        # Index by content
        key = hashlib.md5(str(trace.get('observation', '')).encode()).hexdigest()[:16]
        self.memory_index[key] = trace
    
    def recall(self, query: str) -> Optional[Dict]:
        """Recall memory matching query."""
        for trace in reversed(self.episodic_buffer):
            obs = trace.get('observation', {})
            if isinstance(obs, dict):
                content = obs.get('input', '')
            else:
                content = str(obs)
            if query.lower() in content.lower():
                return trace
        return None
    
    def get_cluster_count(self) -> int:
        """Get number of memory clusters."""
        return len(set(str(t) for t in self.episodic_buffer[:100]))
    
    def get_status(self) -> Dict:
        return {
            'buffer_size': len(self.episodic_buffer),
            'max_buffer': self.max_buffer,
            'clusters': self.cluster_count
        }


class LimbicRegion:
    """
    Region 3: LIMBIC - Affect/Emotion System
    ==========================================
    Evaluates reward and novelty.
    Controls emotional state and motivation.
    """
    version = "v1.0"
    
    def __init__(self):
        self.reward = 0.5
        self.novelty = 0.0
        self.mode = "adaptive"  # adaptive, creative, defensive
        self.reward_history = []
        self.novelty_history = []
    
    def evaluate(self, obs: Dict, memory_ctx: Optional[Dict] = None) -> Dict:
        """Evaluate reward and novelty."""
        # Calculate novelty (how different from memory)
        if memory_ctx:
            self.novelty = 0.3
        else:
            self.novelty = 0.7
        
        # Calculate reward based on positive content
        content = str(obs)
        if any(w in content.lower() for w in ['good', 'great', 'success', 'win', 'yes']):
            self.reward = min(1.0, self.reward + 0.1)
        elif any(w in content.lower() for w in ['bad', 'fail', 'error', 'no', 'wrong']):
            self.reward = max(0.0, self.reward - 0.1)
        
        # Update history
        self.reward_history.append(self.reward)
        self.novelty_history.append(self.novelty)
        if len(self.reward_history) > 100:
            self.reward_history.pop(0)
            self.novelty_history.pop(0)
        
        # Determine mode
        if self.reward > 0.7:
            self.mode = "creative"
        elif self.reward < 0.3:
            self.mode = "defensive"
        else:
            self.mode = "adaptive"
        
        return {
            'reward': self.reward,
            'novelty': self.novelty,
            'mode': self.mode,
            'reward_avg': sum(self.reward_history) / len(self.reward_history) if self.reward_history else 0.5,
            'novelty_avg': sum(self.novelty_history) / len(self.novelty_history) if self.novelty_history else 0
        }
    
    def get_status(self) -> Dict:
        return {
            'reward': self.reward,
            'novelty': self.novelty,
            'mode': self.mode
        }


class PFCRegion:
    """
    Region 4: PFC - Prefrontal Cortex
    ==================================
    Executive decision making.
    Planning, reasoning, working memory.
    """
    version = "v1.0"
    
    def __init__(self):
        self.working_memory = []
        self.max_working = 7  # Miller's Law
        self.attention_focus = 0.5
        self.decisions_made = 0
    
    def decide(self, context: Dict, options: List[Dict] = None) -> Dict:
        """Make a decision."""
        self.decisions_made += 1
        
        # Simple decision logic
        decision_type = "respond"
        confidence = 0.7
        reason = "Based on context"
        
        content = str(context)
        if "?" in content:
            decision_type = "query"
            confidence = 0.6
            reason = "Question detected"
        elif any(w in content.lower() for w in ['do', 'make', 'create', 'build']):
            decision_type = "act"
            confidence = 0.8
            reason = "Action requested"
        
        return {
            'type': decision_type,
            'confidence': confidence,
            'reason': reason,
            'action': {},
            'safety_override': False
        }
    
    def add_to_working(self, item: str) -> None:
        """Add to working memory."""
        if len(self.working_memory) >= self.max_working:
            self.working_memory.pop(0)
        self.working_memory.append(item)
    
    def get_status(self) -> Dict:
        return {
            'working_memory': len(self.working_memory),
            'max_working': self.max_working,
            'decisions': self.decisions_made,
            'attention': self.attention_focus
        }


class BasalGangliaRegion:
    """
    Region 5: BASAL GANGLIA - Habit System
    ========================================
    Pattern automation.
    Habit formation and execution.
    """
    version = "v1.0"
    
    def __init__(self):
        self.habits = {}  # pattern -> action
        self.threshold = 0.8
        self.activations = {}
    
    def execute_habit(self, pattern: str) -> Optional[Dict]:
        """Execute automatic habit response."""
        if pattern in self.habits:
            self.activations[pattern] = self.activations.get(pattern, 0) + 1
            return self.habits[pattern]
        return None
    
    def learn_habit(self, pattern: str, action: Dict) -> None:
        """Learn a new habit."""
        self.habits[pattern] = action
    
    def get_action_value(self, pattern: str) -> float:
        """Get action value for pattern."""
        return self.activations.get(pattern, 0) / max(1, sum(self.activations.values()))
    
    def get_status(self) -> Dict:
        return {
            'habits_learned': len(self.habits),
            'activations': sum(self.activations.values()),
            'threshold': self.threshold
        }


class CerebellumRegion:
    """
    Region 6: CEREBELLUM - Motor Coordination
    ============================================
    Movement coordination and timing.
    Error correction and precision.
    """
    version = "v1.0"
    
    def __init__(self):
        self.motor_commands = []
        self.coordination_score = 1.0
        self.last_precision = 1.0
    
    def execute_motor(self, action: Dict) -> Dict:
        """Execute motor command with coordination."""
        self.motor_commands.append(action)
        if len(self.motor_commands) > 100:
            self.motor_commands.pop(0)
        
        # Simulate coordination
        self.last_precision = max(0.5, min(1.0, self.last_precision + random.uniform(-0.1, 0.1)))
        self.coordination_score = (self.coordination_score + self.last_precision) / 2
        
        return {
            'motor_executed': True,
            'precision': self.last_precision,
            'coordination': self.coordination_score
        }
    
    def get_status(self) -> Dict:
        return {
            'commands_executed': len(self.motor_commands),
            'coordination': self.coordination_score,
            'precision': self.last_precision
        }


class BrainstemRegion:
    """
    Region 7: BRAINSTEM - Survival Center
    =====================================
    Life support functions.
    Safety monitoring and instinct responses.
    """
    version = "v1.0"
    
    def __init__(self):
        self.survival_level = 1.0
        self.safety_override = False
        self.vital_signs = {
            'heartbeat': True,
            'breathing': True,
            'consciousness': True
        }
        self.emergencies = 0
    
    def check_safety(self, input_data: str) -> Dict:
        """Check for safety concerns."""
        # Check for dangerous patterns
        danger_words = ['kill', 'destroy', 'harm', 'danger', 'emergency']
        
        self.safety_override = any(w in input_data.lower() for w in danger_words)
        if self.safety_override:
            self.emergencies += 1
        
        return {
            'safe': not self.safety_override,
            'survival_level': self.survival_level,
            'safety_override': self.safety_override,
            'vital_signs': self.vital_signs
        }
    
    def get_status(self) -> Dict:
        return {
            'survival_level': self.survival_level,
            'safety_override': self.safety_override,
            'emergencies': self.emergencies,
            'vitals': self.vital_signs
        }


class BrainRegions:
    """
    All 7 Brain Regions Container
    """
    def __init__(self):
        self.thalamus = ThalamusRegion()
        self.hippocampus = HippocampusRegion()
        self.limbic = LimbicRegion()
        self.pfc = PFCRegion()
        self.basal = BasalGangliaRegion()
        self.cerebellum = CerebellumRegion()
        self.brainstem = BrainstemRegion()
    
    def process(self, input_data: str) -> Dict:
        """Process through all 7 regions."""
        result = {}
        
        # 1. Thalamus - Sensory relay
        thalamus_result = self.thalamus.process(input_data)
        result['thalamus'] = thalamus_result
        
        # 2. Hippocampus - Memory recall
        recall = self.hippocampus.recall(input_data)
        result['hippocampus'] = {'recall': recall}
        
        # 3. Limbic - Emotional evaluation
        obs = thalamus_result.get('observation', {})
        limbic_result = self.limbic.evaluate(obs, recall)
        result['limbic'] = limbic_result
        
        # 4. PFC - Decision
        pfc_result = self.pfc.decide({'input': input_data, 'affect': limbic_result})
        result['pfc'] = pfc_result
        
        # 5. Basal - Habit check
        habit = self.basal.execute_habit(input_data[:20])
        result['basal'] = {'habit': habit}
        
        # 6. Cerebellum - Motor execution
        if pfc_result['type'] == 'act':
            cerebellum_result = self.cerebellum.execute_motor(pfc_result['action'])
            result['cerebellum'] = cerebellum_result
        
        # 7. Brainstem - Safety check
        safety = self.brainstem.check_safety(input_data)
        result['brainstem'] = safety
        
        # Store in hippocampus
        trace = {
            'tick': time.time(),
            'observation': obs,
            'affect': limbic_result,
            'decision': pfc_result,
            'result': result
        }
        self.hippocampus.store(trace)
        
        return result
    
    def get_status(self) -> Dict:
        return {
            'thalamus': self.thalamus.get_status(),
            'hippocampus': self.hippocampus.get_status(),
            'limbic': self.limbic.get_status(),
            'pfc': self.pfc.get_status(),
            'basal': self.basal.get_status(),
            'cerebellum': self.cerebellum.get_status(),
            'brainstem': self.brainstem.get_status()
        }


# ============ CONSCIOUSNESS LAYERS ============

class ConsciousnessLayer:
    """
    Three-Tier Consciousness System
    ================================
    Based on AOCROS architecture:
    - CONSCIOUS: Foreground, active processing (PFC)
    - SUBCONSCIOUS: Working memory, recent thoughts (Hippocampus)
    - UNCONSCIOUS: Deep memory, patterns (Basal Ganglia/Limbic)
    """
    
    version = "v1.0"
    
    def __init__(self):
        # CONSCIOUS - Active foreground processing
        self.conscious = {
            'active': False,
            'focus_level': 0.5,
            'working_memory': [],  # Current task
            'max_working': 7,  # Miller's Law
            'attention_span': 20,
            'attention_count': 0
        }
        
        # SUBCONSCIOUS - Working memory buffer
        self.subconscious = {
            'active': False,
            'buffer': [],  # Recent processed items
            'buffer_size': 50,
            'processing_queue': [],
            'dreaming': False
        }
        
        # UNCONSCIOUS - Deep storage
        self.unconscious = {
            'active': False,
            'deep_memory': {},  # pattern_hash -> memory
            'instincts': [],  # Pre-programmed responses
            'emotional_tags': {},  # memory -> emotion
            'max_deep': 10000
        }
    
    def think(self, data: str) -> Dict:
        """Process through consciousness layers."""
        result = {
            'layer': None,
            'processed': False
        }
        
        # CONSCIOUS takes input
        self.conscious['active'] = True
        self.conscious['attention_count'] += 1
        
        # Add to working memory
        self.conscious['working_memory'].append(data)
        if len(self.conscious['working_memory']) > self.conscious['max_working']:
            # Push to subconscious
            popped = self.conscious['working_memory'].pop(0)
            self.subconscious['buffer'].append(popped)
        
        # Check attention span
        if self.conscious['attention_count'] >= self.conscious['attention_span']:
            # Switch to subconscious
            self.subconscious['active'] = True
            self.subconscious['processing_queue'].extend(
                self.conscious['working_memory']
            )
            self.conscious['working_memory'].clear()
            self.conscious['attention_count'] = 0
        
        # SUBCONSCIOUS processes buffer
        if self.subconscious['buffer']:
            if len(self.subconscious['buffer']) > self.subconscious['buffer_size']:
                # Push to unconscious
                old = self.subconscious['buffer'].pop(0)
                mem_hash = hashlib.md5(str(old).encode()).hexdigest()[:16]
                self.unconscious['deep_memory'][mem_hash] = old
                if len(self.unconscious['deep_memory']) > self.unconscious['max_deep']:
                    # Remove oldest
                    oldest = next(iter(self.unconscious['deep_memory']))
                    del self.unconscious['deep_memory'][oldest]
        
        # UNCONSCIOUS stores patterns
        self.unconscious['active'] = True
        
        result['processed'] = True
        result['layer'] = 'CONSCIOUS'
        if not self.conscious['working_memory']:
            result['layer'] = 'SUBCONSCIOUS'
        if self.subconscious['buffer']:
            result['layer'] = 'UNCONSCIOUS'
        
        return result
    
    def get_active_layer(self) -> str:
        """Return which layer is currently active."""
        if self.conscious['working_memory']:
            return 'CONSCIOUS'
        elif self.subconscious['buffer']:
            return 'SUBCONSCIOUS'
        elif self.unconscious['deep_memory']:
            return 'UNCONSCIOUS'
        return 'IDLE'
    
    def recall(self, query: str) -> Optional[str]:
        """Recall from unconscious."""
        # Simple recall - find matching memory
        query_hash = hashlib.md5(query.encode()).hexdigest()[:16]
        
        # Check working memory first
        for mem in self.conscious['working_memory']:
            if query.lower() in mem.lower():
                return f'[CONSCIOUS] {mem}'
        
        # Check subconscious
        for mem in self.subconscious['buffer']:
            if query.lower() in mem.lower():
                return f'[SUBCONSCIOUS] {mem}'
        
        # Check unconscious
        for key, mem in self.unconscious['deep_memory'].items():
            if query.lower() in mem.lower():
                return f'[UNCONSCIOUS] {mem}'
        
        return None
    
    def get_status(self) -> Dict:
        return {
            'version': self.version,
            'active_layer': self.get_active_layer(),
            'conscious': {
                'active': self.conscious['active'],
                'focus': f"{self.conscious['focus_level']*100:.0f}%",
                'working_memory': len(self.conscious['working_memory']),
                'attention': f"{self.conscious['attention_count']}/{self.conscious['attention_span']}"
            },
            'subconscious': {
                'active': self.subconscious['active'],
                'buffer_size': len(self.subconscious['buffer']),
                'processing': len(self.subconscious['processing_queue']),
                'dreaming': self.subconscious['dreaming']
            },
            'unconscious': {
                'active': self.unconscious['active'],
                'memories_stored': len(self.unconscious['deep_memory']),
                'max_capacity': self.unconscious['max_deep']
            }
        }

# ============ CORTEX 3D ============

class Cortex3D:
    """Spatial Consciousness - 32³ Voxels"""
    
    version = "3D"
    dimension = 32
    
    def __init__(self):
        self.voxels = [[[0.0 for _ in range(self.dimension)] 
                        for _ in range(self.dimension)] 
                       for _ in range(self.dimension)]
        self.activity = 0.0
    
    def set_voxel(self, x: int, y: int, z: int, value: float):
        """Set voxel value (clamps to valid range)."""
        x = max(0, min(self.dimension - 1, x))
        y = max(0, min(self.dimension - 1, y))
        z = max(0, min(self.dimension - 1, z))
        self.voxels[x][y][z] = max(0, min(1, value))
        self.activity = self.get_activity()
    
    def get_voxel(self, x: int, y: int, z: int) -> float:
        """Get voxel value (returns 0 for out of bounds)."""
        if 0 <= x < self.dimension and 0 <= y < self.dimension and 0 <= z < self.dimension:
            return self.voxels[x][y][z]
        return 0
    
    def get_activity(self) -> float:
        """Get overall activity."""
        total = sum(sum(sum(row) for row in plane) for plane in self.voxels)
        return total / (self.dimension ** 3)
    
    def get_status(self) -> Dict:
        return {
            'version': self.version,
            'dimension': f"{self.dimension}³",
            'total_voxels': self.dimension ** 3,
            'activity': f"{self.activity*100:.1f}%"
        }

# ============ TRACRAY ============

class TracRay:
    """Memory Trajectory Recording"""
    
    version = "—"
    
    def __init__(self):
        self.trajectories: List = []
        self.max_trajectories = 1000
    
    def record(self, thought: str, decision: str, outcome: str):
        """Record trajectory."""
        traj = {
            'timestamp': time.time(),
            'thought': thought[:100],
            'decision': decision,
            'outcome': outcome
        }
        self.trajectories.append(traj)
        if len(self.trajectories) > self.max_trajectories:
            self.trajectories.pop(0)
    
    def get_status(self) -> Dict:
        return {
            'version': self.version,
            'trajectory_count': len(self.trajectories),
            'max_trajectories': self.max_trajectories
        }

# ============ MODEL ROUTER ============

class ModelRouter:
    """Ollama Model Router"""
    
    version = "—"
    
    def __init__(self):
        self.decision_model = "tinyllama:latest"
        self.voice_model = "antoniohudnall/Mort_II:latest"
        self.analysis_model = "llama3.2:3b"
        self.decision_calls = 0
        self.voice_calls = 0
        self.analysis_calls = 0
    
    def route(self, query_type: str) -> str:
        """Route query to model."""
        if query_type == "decision":
            self.decision_calls += 1
            return self.decision_model
        elif query_type == "voice":
            self.voice_calls += 1
            return self.voice_model
        elif query_type == "analysis":
            self.analysis_calls += 1
            return self.analysis_model
        return self.decision_model
    
    def get_status(self) -> Dict:
        return {
            'version': self.version,
            'decision_model': self.decision_model,
            'voice_model': self.voice_model,
            'analysis_model': self.analysis_model,
            'decision_calls': self.decision_calls,
            'voice_calls': self.voice_calls,
            'analysis_calls': self.analysis_calls
        }

# ============ BRAIN v3.1 ============

class Brain(HealthMixin):
    """Core Processing v3.1 - OODA Loop: OBSERVE → ORIENT → DECIDE → ACT"""
    
    version = "v3.1"
    
    def __init__(self):
        super().__init__()
        self.phase = BrainPhase.OBSERVE
        self.cycles = 0
        self.signal_quality = 0.865
        self.processing_power = 0.85
    
    def process(self, data: str) -> Dict:
        """Process through OODA loop."""
        self.cycles += 1
        
        # OODA loop phases
        if self.phase == BrainPhase.OBSERVE:
            result = "observing"
            self.phase = BrainPhase.ORIENT
        elif self.phase == BrainPhase.ORIENT:
            result = "orienting"
            self.phase = BrainPhase.DECIDE
        elif self.phase == BrainPhase.DECIDE:
            result = "deciding"
            self.phase = BrainPhase.ACT
        else:
            result = "acting"
            self.phase = BrainPhase.OBSERVE
        
        self.tick_recovery()
        
        return {
            'phase': self.phase.value.upper(),
            'cycles': self.cycles,
            'result': result,
            'signal_quality': self.signal_quality,
            'processing_power': f"{self.processing_power*100:.0f}%"
        }
    
    def get_status(self) -> Dict:
        return {
            'version': self.version,
            'phase': self.phase.value.upper(),
            'cycles': self.cycles,
            'signal_quality': self.signal_quality,
            'processing_power': f"{self.processing_power*100:.0f}%",
            'health': f"{self.health*100:.0f}%",
            'health_status': self.get_health_status()
        }

# ============ MORTY BODY v2.1 ============

class MortyBody:
    """
    Morty's Complete Body - AOCROS Aligned v2.1
    ============================================
    Pipeline: [LUNGS] → [LIVER] → [BRAIN] → [KIDNEYS]
    """
    
    def __init__(self):
        # Identity
        self.name = "Mortimer"
        self.designation = "C3"
        self.ship = "SEED3"
        self.version = VERSION
        self.version_date = VERSION_DATE
        
        # Create all organs
        self.lungs = Lungs()
        self.liver = Liver()
        self.brain = Brain()
        self.kidneys = Kidneys()
        self.heart = SuperiorHeart()
        self.stomach = Stomach()
        self.intestine = Intestine()
        self.thyroid = Thyroid()
        self.cortex = Cortex3D()
        self.tracray = TracRay()
        self.router = ModelRouter()
        
        # Consciousness layers (AOCROS three-tier)
        self.consciousness = ConsciousnessLayer()
        
        # 7 Brain Regions (AOCROS)
        self.brain_regions = BrainRegions()
        
        # System
        self.qmd_cycles = 0
        self.start_time = time.time()
        self.last_cycle = 0
        self.uptime = 0
        
        # Stress response
        self.global_stress = 0.0
        self.recovery_mode = False
    
    def cycle(self, input_data: str = "") -> Dict:
        """One complete body cycle."""
        self.qmd_cycles += 1
        self.last_cycle = time.time()
        self.uptime = time.time() - self.start_time
        
        # Stage 1: LUNGS
        lung_result = self.lungs.breathe()
        
        # Stage 2: LIVER
        if input_data:
            filtered_data, liver_result = self.liver.filter(input_data)
        else:
            filtered_data = ""
            liver_result = "IDLE"
        self.liver.tick()
        
        # Stage 3: BRAIN (OODA)
        brain_result = self.brain.process(filtered_data)
        thyroid_stim = self.thyroid.regulate(self.qmd_cycles % 10 / 10)
        
        # Heart
        heart_result = self.heart.beat()
        
        # Stage 4: KIDNEYS
        if filtered_data:
            kidney_result = self.kidneys.process(filtered_data)
        else:
            kidney_result = self.kidneys.process("cycle")
        
        # Digestion
        intestine_result = self.intestine.distribute(0.5)
        
        # Update cortex
        self.cortex.set_voxel(
            self.qmd_cycles % 32,
            int(float(heart_result['coherence']) * 32),
            int(float(thyroid_stim['metabolism'].rstrip('%')) / 3),
            float(heart_result['coherence'])
        )
        
        # Record trajectory
        self.tracray.record(
            thought=input_data[:50] if input_data else "cycle",
            decision=f"qmd_{self.qmd_cycles}",
            outcome=liver_result
        )
        
        # CONSCIOUSNESS LAYERS - Process through three tiers
        if input_data:
            consciousness_result = self.consciousness.think(input_data)
        else:
            consciousness_result = {'layer': 'IDLE', 'processed': False}
        
        # 7 BRAIN REGIONS - Process through all regions
        if input_data:
            brain_regions_result = self.brain_regions.process(input_data)
        else:
            brain_regions_result = {}
        
        # Calculate global stress
        self.global_stress = (
            self.lungs.stress_level * 0.1 +
            self.liver.stress_level * 0.15 +
            self.brain.stress_level * 0.2 +
            self.kidneys.stress_level * 0.15 +
            self.heart.stress_level * 0.25 +
            self.thyroid.stress_level * 0.15
        )
        
        # Recovery mode if stress too high
        self.recovery_mode = self.global_stress > 0.7
        
        return {
            'cycle': self.qmd_cycles,
            'uptime': f"{int(self.uptime)}s",
            'global_stress': f"{self.global_stress*100:.0f}%",
            'recovery_mode': self.recovery_mode,
            'pipeline': {
                'LUNGS': lung_result['state'],
                'LIVER': liver_result,
                'BRAIN': brain_result['phase'],
                'KIDNEYS': kidney_result['action']
            },
            'heart': heart_result,
            'thyroid': thyroid_stim
        }
    
    def process_thought(self, thought: str) -> Dict:
        """Process a thought."""
        self.stomach.digest(thought, priority=5)
        return self.cycle(thought)
    
    def get_status(self) -> Dict:
        """Full status report."""
        return {
            'identity': {
                'name': self.name,
                'designation': self.designation,
                'ship': self.ship,
                'version': self.version,
                'version_date': self.version_date,
                'uptime_seconds': int(self.uptime)
            },
            'versions': ORGAN_VERSIONS,
            'qmd_cycles': self.qmd_cycles,
            'global_stress': f"{self.global_stress*100:.0f}%",
            'recovery_mode': self.recovery_mode,
            'organs': {
                'lungs': self.lungs.get_status(),
                'liver': self.liver.get_status(),
                'brain': self.brain.get_status(),
                'kidneys': self.kidneys.get_status(),
                'heart': self.heart.get_status(),
                'stomach': self.stomach.get_status(),
                'intestine': self.intestine.get_status(),
                'thyroid': self.thyroid.get_status(),
                'cortex': self.cortex.get_status(),
                'tracray': self.tracray.get_status(),
                'router': self.router.get_status(),
                'consciousness': self.consciousness.get_status(),
                'brain_regions': self.brain_regions.get_status()
            }
        }

# ============ MAIN ============

BODY = MortyBody()

def save_waste_report() -> str:
    """Save waste report."""
    report = BODY.get_status()
    filename = f"morty_waste_{int(time.time())}.json"
    filepath = WASTE_DIR / filename
    with open(filepath, 'w') as f:
        json.dump(report, f, indent=2)
    return str(filepath)

if __name__ == "__main__":
    print("=" * 70)
    print(f"🧬 MORTY BODY v{VERSION} - AOCROS-ALIGNED")
    print("=" * 70)
    print(f"Identity: {BODY.name} ({BODY.designation}) - {BODY.ship}")
    print(f"Built: {VERSION_DATE}")
    print()
    
    # Process thoughts
    for thought in ["Building body v2.1", "Health metrics added", "Stress response working"]:
        BODY.process_thought(thought)
    
    # Run some cycles
    for _ in range(10):
        BODY.cycle()
    
    # Get status
    status = BODY.get_status()
    
    print("📊 STATUS REPORT")
    print("-" * 50)
    print(f"Version: {status['identity']['version']}")
    print(f"QMD Cycles: {status['qmd_cycles']}")
    print(f"Uptime: {status['identity']['uptime_seconds']}s")
    print(f"Global Stress: {status['global_stress']}")
    print(f"Recovery Mode: {status['recovery_mode']}")
    print()
    
    print("🫁 LUNGS   │", status['organs']['lungs']['state'].ljust(10), "│", 
          status['organs']['lungs']['health'].ljust(8), "│", status['organs']['lungs']['health_status'])
    print("🔬 LIVER   │", status['organs']['liver']['state'].ljust(10), "│", 
          status['organs']['liver']['health'].ljust(8), "│", status['organs']['liver']['health_status'])
    print("🧠 BRAIN   │", status['organs']['brain']['phase'].ljust(10), "│", 
          status['organs']['brain']['health'].ljust(8), "│", status['organs']['brain']['health_status'])
    print("🫘 KIDNEYS │", status['organs']['kidneys']['state'].ljust(10), "│", 
          status['organs']['kidneys']['health'].ljust(8), "│", status['organs']['kidneys']['health_status'])
    print("❤️ HEART   │", status['organs']['heart']['state'].ljust(10), "│", 
          status['organs']['heart']['health'].ljust(8), "│", status['organs']['heart']['health_status'])
    print("🫃 STOMACH │", "IDLE".ljust(10), "│", 
          status['organs']['stomach']['health'].ljust(8), "│", status['organs']['stomach']['health_status'])
    print("🦠 INTEST  │", "ACTIVE".ljust(10), "│", 
          status['organs']['intestine']['health'].ljust(8), "│", status['organs']['intestine']['health_status'])
    print("🦋 THYROID │", status['organs']['thyroid']['metabolism'].ljust(10), "│", 
          status['organs']['thyroid']['health'].ljust(8), "│", status['organs']['thyroid']['health_status'])
    
    print()
    print("─" * 70)
    print("PIPELINE: [LUNGS] → [LIVER] → [BRAIN] → [KIDNEYS]")
    print("          INHALE    FILTER    PROCESS    RECYCLE")
    print("          GAS_EX    PURIFY    DECIDE     EXCRETE")
    print("          EXHALE    TOXIC     ACT        REABSORB")
    
    # Save report
    filepath = save_waste_report()
    print()
    print(f"💾 Waste report: {filepath}")