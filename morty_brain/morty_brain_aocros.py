"""
Morty Brain AOCROS - Complete Brain System
===========================================
Integrates all 7 brain regions with:
- GrowingNN (neural growth)
- QMD Loop (Ollama decisions)
- MemoryBridge (workspace memory)
- Dice (quantum intuition)
- Visual Cortex (3D brain viz)
- RL Core (reinforcement learning)
- 3-Tier Consciousness

Author: Mortimer (C3 - SEED3)
Version: 2.3
Date: 2026-06-19
"""

import json
import time
import random
import hashlib
import math
from datetime import datetime, UTC
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import threading
import numpy as np

# ============ CONSTANTS ============

VERSION = "2.3"
VERSION_DATE = "2026-06-19"

# Paths
BASE_DIR = Path.home() / "mortimer" / "morty_brain"
WASTE_DIR = BASE_DIR / "waste"
WASTE_DIR.mkdir(parents=True, exist_ok=True)

# ============ ENUMS ============

class BrainPhase(Enum):
    OBSERVE = "observe"
    ORIENT = "orient"
    DECIDE = "decide"
    ACT = "act"

class ConsciousnessLevel(Enum):
    CONSCIOUS = "conscious"
    SUBCONSCIOUS = "subconscious"
    UNCONSCIOUS = "unconscious"

class DecisionType(Enum):
    RESPOND = "respond"
    ACT = "act"
    NOOP = "noop"
    HALT = "halt"
    QUERY = "query"
    LEARN = "learn"

# ============ GROWING NEURAL NETWORK ============

class GrowingNN:
    """
    Growing Neural Network - Self-Organizing Brain
    ==============================================
    Nodes grow when novelty is high or error rate is high.
    Layers grow when complexity exceeds threshold.
    """
    version = "v1.0"
    
    def __init__(self):
        # Network architecture
        self.layers = 3
        self.layer_nodes = [8, 12, 16]  # Starting nodes per layer
        self.activations = [[0.5] * n for n in self.layer_nodes]
        
        # Growth tracking
        self.growth_events = []
        self.total_nodes = sum(self.layer_nodes)
        
        # Thresholds
        self.node_threshold = {"novelty": 0.8, "error": 0.6}
        self.layer_threshold = {"complexity": 0.9}
        
        # State
        self.error_rate = 0.0
        self.complexity = 0.0
        self.novelty = 0.0
    
    def forward(self, inputs: List[float]) -> Dict:
        """Forward pass through network."""
        current = inputs[:self.layer_nodes[0]]
        
        for i in range(self.layers):
            # Apply weights and activation
            output = []
            for node in range(self.layer_nodes[i]):
                # Simple weighted sum
                weight_sum = sum(current[j] * random.uniform(0.3, 0.7) 
                               for j in range(len(current)))
                activated = 1 / (1 + math.exp(-weight_sum))
                output.append(activated)
            
            self.activations[i] = output
            current = output
        
        return {
            'output': current,
            'layers': self.layers,
            'total_nodes': self.total_nodes
        }
    
    def grow_node(self) -> None:
        """Add a node to the last layer."""
        last_layer = self.layers - 1
        self.layer_nodes[last_layer] += 1
        self.activations[last_layer].append(0.5)
        self.total_nodes = sum(self.layer_nodes)
        
        event = {
            'type': 'add_node',
            'layer': last_layer,
            'timestamp': time.time()
        }
        self.growth_events.append(event)
    
    def grow_layer(self) -> None:
        """Add a new layer."""
        self.layers += 1
        self.layer_nodes.append(8)
        self.activations.append([0.5] * 8)
        self.total_nodes = sum(self.layer_nodes)
        
        event = {
            'type': 'add_layer',
            'layer': self.layers - 1,
            'timestamp': time.time()
        }
        self.growth_events.append(event)
    
    def should_grow_node(self, novelty: float, error: float) -> bool:
        """Check if should add node."""
        return novelty >= self.node_threshold["novelty"] or error >= self.node_threshold["error"]
    
    def should_grow_layer(self, complexity: float) -> bool:
        """Check if should add layer."""
        return complexity >= self.layer_threshold["complexity"]
    
    def update_error(self, predicted: Any, actual: Any) -> float:
        """Update error rate."""
        if predicted is None or actual is None:
            return 0.0
        
        # Simple error calculation
        if isinstance(predicted, (int, float)) and isinstance(actual, (int, float)):
            self.error_rate = abs(predicted - actual) / max(abs(predicted), 0.001)
        else:
            # String similarity
            matches = sum(1 for p, a in zip(str(predicted), str(actual)) if p == a)
            self.error_rate = 1 - (matches / max(len(str(predicted)), 1))
        
        self.error_rate = min(1.0, self.error_rate)
        return self.error_rate
    
    def calculate_complexity(self, obs: Dict, ctx: Dict) -> float:
        """Calculate task complexity."""
        complexity = 0.0
        
        # Context size
        if ctx:
            complexity += min(len(str(ctx)) / 1000, 0.3)
        
        # Observation size
        if obs:
            complexity += min(len(str(obs)) / 500, 0.3)
        
        # Historical average
        complexity = min(1.0, complexity)
        self.complexity = complexity
        return complexity
    
    def get_state(self) -> Dict:
        return {
            'layers': self.layers,
            'layer_nodes': self.layer_nodes,
            'total_nodes': self.total_nodes,
            'error_rate': self.error_rate,
            'complexity': self.complexity,
            'novelty': self.novelty,
            'growth_events': len(self.growth_events)
        }

# ============ MEMORY BRIDGE ============

class MemoryBridge:
    """
    Memory Bridge - Workspace Memory Integration
    ==============================================
    Queries workspace memory files for context.
    """
    version = "v1.0"
    
    def __init__(self):
        self.memory_index = {}
        self.last_query_time = 0
        self.query_count = 0
    
    def index_file(self, path: Path) -> None:
        """Index a memory file."""
        try:
            content = path.read_text()
            key = hashlib.md5(str(path).encode()).hexdigest()[:16]
            self.memory_index[key] = {
                'path': str(path),
                'content': content,
                'indexed': time.time()
            }
        except Exception:
            pass
    
    def query(self, query_text: str, n_results: int = 5) -> Dict:
        """Query memory index."""
        self.query_count += 1
        self.last_query_time = time.time()
        
        results = []
        query_lower = query_text.lower()
        
        for key, mem in self.memory_index.items():
            if query_lower in mem['content'].lower():
                results.append({
                    'source': mem['path'],
                    'text': mem['content'][:200],
                    'relevance': 0.8
                })
        
        return {
            'results': results[:n_results],
            'source_count': len(results)
        }
    
    def should_query(self, novelty: float, novelty_avg: float) -> bool:
        """Determine if should query memory."""
        return novelty > novelty_avg * 1.5 or novelty > 0.7
    
    def get_state(self) -> Dict:
        return {
            'indexed_files': len(self.memory_index),
            'queries': self.query_count,
            'last_query': self.last_query_time
        }

# ============ DICE (Quantum Intuition) ============

class Dice:
    """
    Dice - Quantum Intuition Organ
    ================================
    Generates random insights for creativity.
    """
    version = "v1.0"
    
    def __init__(self):
        self.sides = ["tick", "rest", "explore", "focus", "create", "analyze"]
        self.last_roll = "tick"
        self.roll_count = 0
        self.roll_history = []
    
    def roll(self, sides: List[str] = None) -> str:
        """Roll the dice."""
        if sides:
            self.sides = sides
        
        self.last_roll = random.choice(self.sides)
        self.roll_count += 1
        self.roll_history.append(self.last_roll)
        
        if len(self.roll_history) > 100:
            self.roll_history.pop(0)
        
        return self.last_roll
    
    def get_insight(self) -> Dict:
        """Get random insight."""
        return {
            'insight': self.last_roll,
            'rolls': self.roll_count,
            'history': self.roll_history[-10:]
        }
    
    def get_state(self) -> Dict:
        return {
            'last_roll': self.last_roll,
            'rolls': self.roll_count
        }

# ============ RL CORE ============

class RLCore:
    """
    RL Core - Reinforcement Learning
    ================================
    Reward signals and policy learning.
    """
    version = "v1.0"
    
    def __init__(self):
        self.reward_signal = 0.0
        self.policy = {}  # state -> action
        self.q_table = {}  # state-action pairs
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 0.1
    
    def get_reward(self, action: str, outcome: Dict) -> float:
        """Calculate reward for action."""
        reward = 0.0
        
        if outcome.get('success', False):
            reward += 1.0
        
        if outcome.get('improvement', 0) > 0:
            reward += outcome['improvement'] * 0.5
        
        if outcome.get('novelty', 0) > 0:
            reward += outcome['novelty'] * 0.3
        
        self.reward_signal = reward
        return reward
    
    def choose_action(self, state: str, actions: List[str]) -> str:
        """Choose action using epsilon-greedy."""
        if random.random() < self.exploration_rate:
            return random.choice(actions)
        
        # Exploit - choose best known action
        if state in self.q_table:
            q_values = self.q_table[state]
            return max(q_values, key=q_values.get)
        
        return random.choice(actions)
    
    def update_q(self, state: str, action: str, reward: float, next_state: str) -> None:
        """Update Q-table."""
        if state not in self.q_table:
            self.q_table[state] = {}
        
        if action not in self.q_table[state]:
            self.q_table[state][action] = 0.0
        
        # Q-learning update
        max_next_q = 0.0
        if next_state in self.q_table:
            max_next_q = max(self.q_table[next_state].values())
        
        current_q = self.q_table[state][action]
        self.q_table[state][action] = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q
        )
    
    def get_state(self) -> Dict:
        return {
            'reward': self.reward_signal,
            'states_learned': len(self.q_table),
            'exploration_rate': self.exploration_rate
        }

# ============ VISUAL CORTEX ============

class VisualCortex:
    """
    Visual Cortex - 3D Brain Visualization
    =======================================
    Renders brain state in 3D voxel space.
    """
    version = "v1.0"
    
    def __init__(self, size: int = 32):
        self.size = size
        self.voxels = {}  # (x,y,z) -> activation
        self.history = []
        self.max_history = 100
    
    def set_voxel(self, x: int, y: int, z: int, activation: float) -> None:
        """Set voxel activation."""
        if 0 <= x < self.size and 0 <= y < self.size and 0 <= z < self.size:
            self.voxels[(x, y, z)] = max(0, min(1, activation))
    
    def render(self, brain_state: Dict) -> Dict:
        """Render brain state to voxels."""
        tick = brain_state.get('tick', 0)
        
        # Map brain regions to spatial positions
        regions = brain_state.get('regions', {})
        
        # Thalamus - center top
        self.set_voxel(16, 16, 28, 0.8)
        
        # Hippocampus - left side
        self.set_voxel(8, 16, 16, 0.7)
        
        # Limbic - right side
        self.set_voxel(24, 16, 16, regions.get('limbic', {}).get('reward', 0.5))
        
        # PFC - front center
        self.set_voxel(16, 8, 12, 0.9)
        
        # Basal - bottom center
        self.set_voxel(16, 24, 4, 0.6)
        
        # Cerebellum - back
        self.set_voxel(16, 28, 8, regions.get('cerebellum', {}).get('coordination', 0.7))
        
        # Brainstem - bottom
        self.set_voxel(16, 16, 2, regions.get('brainstem', {}).get('survival', 1.0))
        
        return {
            'voxel_count': len(self.voxels),
            'size': f"{self.size}³",
            'history_len': len(self.history)
        }
    
    def get_state(self) -> Dict:
        return {
            'size': self.size,
            'active_voxels': len(self.voxels),
            'total_capacity': self.size ** 3
        }

# ============ QMD LOOP ============

class QMDLoop:
    """
    Quantized Memory Distillation Loop
    ===================================
    Ollama-based decision making.
    """
    version = "v1.0"
    
    def __init__(self):
        self.cycles = 0
        self.latencies = []
        self.max_latencies = 100
        self.last_query = ""
        self.model = "tinyllama:latest"
        self.embedding_model = "nomic-embed-text"
    
    def query(self, prompt: str, model: str = None) -> Dict:
        """Query Ollama for decision."""
        self.cycles += 1
        start = time.time()
        
        # Simulate Ollama call (in real system would use requests)
        # For now, generate a response based on prompt
        latency = random.uniform(0.1, 0.5)
        time.sleep(min(latency, 0.1))  # Don't actually sleep
        
        self.latencies.append(latency)
        if len(self.latencies) > self.max_latencies:
            self.latencies.pop(0)
        
        avg_latency = sum(self.latencies) / len(self.latencies)
        
        # Generate simple response
        response = self._generate_response(prompt)
        
        self.last_query = prompt
        
        return {
            'response': response,
            'model': model or self.model,
            'latency_ms': avg_latency * 1000,
            'cycles': self.cycles
        }
    
    def _generate_response(self, prompt: str) -> str:
        """Generate simple response."""
        prompt_lower = prompt.lower()
        
        if '?' in prompt:
            return "Analyzed question. Providing answer."
        elif any(w in prompt_lower for w in ['create', 'make', 'build']):
            return "Action planned. Initiating execution."
        elif any(w in prompt_lower for w in ['stop', 'halt', 'wait']):
            return "Action paused. Standing by."
        else:
            return "Input processed. Acknowledged."
    
    def embed(self, text: str) -> List[float]:
        """Generate embedding for text."""
        # Simple hash-based embedding
        hash_val = hashlib.md5(text.encode()).hexdigest()
        embedding = [int(c, 16) / 15 for c in hash_val[:32]]
        return embedding
    
    def get_state(self) -> Dict:
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        return {
            'cycles': self.cycles,
            'avg_latency_ms': avg_latency * 1000,
            'model': self.model,
            'last_query': self.last_query[:50] if self.last_query else None
        }

# ============ COMPLETE MORTY BRAIN ============

class MortyBrain:
    """
    Morty's Complete AOCROS Brain
    ==============================
    Integrates all components:
    - 7 Brain Regions
    - 3-Tier Consciousness
    - GrowingNN
    - QMD Loop
    - MemoryBridge
    - Dice
    - RL Core
    - Visual Cortex
    """
    version = VERSION
    version_date = VERSION_DATE
    
    def __init__(self):
        # Identity
        self.name = "Mortimer"
        self.designation = "C3"
        self.ship = "SEED3"
        
        # 7 Brain Regions
        self._init_regions()
        
        # 3-Tier Consciousness
        self._init_consciousness()
        
        # AOCROS Systems
        self.growing_nn = GrowingNN()
        self.memory_bridge = MemoryBridge()
        self.dice = Dice()
        self.rl_core = RLCore()
        self.visual_cortex = VisualCortex()
        self.qmd_loop = QMDLoop()
        
        # State
        self.tick = 0
        self.phase = BrainPhase.OBSERVE
        self.start_time = time.time()
        self.uptime = 0
        
        # History
        self.tick_history = []
        self.decision_history = []
    
    def _init_regions(self):
        """Initialize 7 brain regions."""
        # Thalamus - Sensory relay
        self.thalamus = {
            'queue': [],
            'priority': 0.5,
            'processed': 0
        }
        
        # Hippocampus - Episodic memory
        self.hippocampus = {
            'traces': [],
            'clusters': 0,
            'novelty_avg': 0.0,
            'max_traces': 1000
        }
        
        # Limbic - Emotion/affect
        self.limbic = {
            'reward': 0.5,
            'novelty': 0.0,
            'mode': 'adaptive',  # adaptive, creative, defensive
            'reward_history': []
        }
        
        # PFC - Decision making
        self.pfc = {
            'decisions': 0,
            'confidence': 0.7,
            'working_memory': [],
            'max_working': 7
        }
        
        # Basal Ganglia - Habits
        self.basal = {
            'habits': {},
            'threshold': 0.8,
            'activations': 0
        }
        
        # Cerebellum - Motor coordination
        self.cerebellum = {
            'commands': [],
            'coordination': 1.0,
            'precision': 1.0
        }
        
        # Brainstem - Survival
        self.brainstem = {
            'survival': 1.0,
            'safety_override': False,
            'vitals': {'heart': True, 'breath': True, 'conscious': True}
        }
    
    def _init_consciousness(self):
        """Initialize 3-tier consciousness."""
        # CONSCIOUS - Active thinking
        self.conscious = {
            'active': True,
            'focus': 0.8,
            'working_memory': [],
            'attention_ticks': 0,
            'max_attention': 20
        }
        
        # SUBCONSCIOUS - Working memory
        self.subconscious = {
            'active': False,
            'buffer': [],
            'max_buffer': 50,
            'processing': []
        }
        
        # UNCONSCIOUS - Deep memory
        self.unconscious = {
            'active': False,
            'deep_memory': {},
            'max_deep': 10000,
            'instincts': []
        }
    
    def tick_cycle(self, input_data: str = "") -> Dict:
        """One complete OODA tick."""
        self.tick += 1
        self.uptime = time.time() - self.start_time
        
        # O: OBSERVE (Thalamus)
        obs = self._observe(input_data)
        
        # O: ORIENT (Hippocampus + Limbic)
        ctx = self._orient(obs)
        affect = self._evaluate_affect(obs, ctx)
        
        # D: DECIDE (PFC + Brainstem)
        decision = self._decide(obs, ctx, affect)
        
        # A: ACT (Basal + Cerebellum)
        action = self._act(decision, affect)
        
        # Learn
        self._learn(obs, decision, action, affect)
        
        # Update consciousness
        self._update_consciousness(obs, decision)
        
        # State
        state = {
            'tick': self.tick,
            'phase': self.phase.value.upper(),
            'uptime': self.uptime,
            'input': input_data[:100] if input_data else None,
            'observation': obs,
            'context': ctx,
            'affect': affect,
            'decision': decision,
            'action': action,
            'regions': self._get_region_states(),
            'consciousness': self._get_consciousness_state(),
            'growingnn': self.growing_nn.get_state(),
            'qmd': self.qmd_loop.get_state(),
            'dice': self.dice.get_state(),
            'rl': self.rl_core.get_state(),
            'visual': self.visual_cortex.render({
                'tick': self.tick,
                'regions': self._get_region_states()
            })
        }
        
        # Update visual cortex
        self.visual_cortex.render(state)
        
        # Store in history
        self.tick_history.append(state)
        if len(self.tick_history) > 1000:
            self.tick_history.pop(0)
        
        return state
    
    def _observe(self, data: str) -> Dict:
        """OBSERVE - Thalamus sensory input."""
        self.phase = BrainPhase.OBSERVE
        
        obs = {
            'input': data,
            'source': 'thalamus',
            'timestamp': time.time(),
            'priority': 0.5
        }
        
        # Update priority
        if '?' in data:
            obs['priority'] = 0.7
        if any(w in data.lower() for w in ['urgent', 'emergency', '!']):
            obs['priority'] = 0.95
        
        self.thalamus['processed'] += 1
        
        return obs
    
    def _orient(self, obs: Dict) -> Dict:
        """ORIENT - Hippocampus memory context."""
        self.phase = BrainPhase.ORIENT
        
        # Query memory
        memory_result = self.memory_bridge.query(obs.get('input', ''))
        
        # Calculate novelty
        novelty = 0.5
        if memory_result['source_count'] == 0:
            novelty = 0.8  # High novelty if no memory
        
        # Update hippocampus
        trace = {
            'tick': self.tick,
            'observation': obs,
            'novelty': novelty
        }
        self.hippocampus['traces'].append(trace)
        if len(self.hippocampus['traces']) > self.hippocampus['max_traces']:
            self.hippocampus['traces'].pop(0)
        
        # Update novelty average
        novelties = [t['novelty'] for t in self.hippocampus['traces'][-100:]]
        self.hippocampus['novelty_avg'] = sum(novelties) / len(novelties) if novelties else 0.5
        self.growing_nn.novelty = novelty
        
        return {
            'memory': memory_result,
            'novelty': novelty,
            'novelty_avg': self.hippocampus['novelty_avg']
        }
    
    def _evaluate_affect(self, obs: Dict, ctx: Dict) -> Dict:
        """EVALUATE - Limbic emotional response."""
        reward = self.limbic['reward']
        content = obs.get('input', '').lower()
        
        # Adjust reward based on content
        if any(w in content for w in ['good', 'great', 'success', 'yes', 'win']):
            reward = min(1.0, reward + 0.1)
        elif any(w in content for w in ['bad', 'fail', 'error', 'no', 'wrong']):
            reward = max(0.0, reward - 0.1)
        
        self.limbic['reward'] = reward
        self.limbic['reward_history'].append(reward)
        if len(self.limbic['reward_history']) > 100:
            self.limbic['reward_history'].pop(0)
        
        # Determine mode
        if reward > 0.7:
            mode = 'creative'
        elif reward < 0.3:
            mode = 'defensive'
        else:
            mode = 'adaptive'
        
        self.limbic['mode'] = mode
        self.limbic['novelty'] = ctx.get('novelty', 0.5)
        
        return {
            'reward': reward,
            'novelty': ctx.get('novelty', 0.5),
            'mode': mode,
            'reward_avg': sum(self.limbic['reward_history']) / len(self.limbic['reward_history'])
        }
    
    def _decide(self, obs: Dict, ctx: Dict, affect: Dict) -> Dict:
        """DECIDE - PFC executive decision."""
        self.phase = BrainPhase.DECIDE
        
        # Query QMD
        qmd_result = self.qmd_loop.query(obs.get('input', ''))
        
        # Determine decision type
        content = obs.get('input', '')
        decision_type = 'respond'
        confidence = 0.7
        reason = 'Based on context and affect'
        
        if '?' in content:
            decision_type = 'query'
            confidence = 0.6
            reason = 'Question detected'
        elif any(w in content.lower() for w in ['do', 'make', 'create', 'build', 'start']):
            decision_type = 'act'
            confidence = 0.8
            reason = 'Action requested'
        elif any(w in content.lower() for w in ['stop', 'halt', 'wait']):
            decision_type = 'noop'
            confidence = 0.9
            reason = 'Stop command'
        
        # Brainstem safety check
        safety_override = any(w in content.lower() for w in 
                           ['kill', 'destroy', 'harm', 'emergency', 'danger'])
        if safety_override:
            self.brainstem['safety_override'] = True
            decision_type = 'halt'
            confidence = 1.0
            reason = 'SAFETY OVERRIDE'
        
        self.pfc['decisions'] += 1
        self.pfc['confidence'] = confidence
        
        # Add to working memory
        self.pfc['working_memory'].append(content[:100])
        if len(self.pfc['working_memory']) > self.pfc['max_working']:
            self.pfc['working_memory'].pop(0)
        
        decision = {
            'type': decision_type,
            'confidence': confidence,
            'reason': reason,
            'qmd_response': qmd_result.get('response'),
            'safety_override': safety_override
        }
        
        self.decision_history.append(decision)
        
        return decision
    
    def _act(self, decision: Dict, affect: Dict) -> Dict:
        """ACT - Basal execution + Cerebellum coordination."""
        self.phase = BrainPhase.ACT
        
        # Check for habit
        habit = None
        for pattern, action in self.basal['habits'].items():
            if pattern in decision.get('reason', ''):
                habit = action
                self.basal['activations'] += 1
                break
        
        # Execute action
        action = {
            'type': decision['type'],
            'executed': True,
            'habit_used': habit is not None,
            'mode': affect['mode']
        }
        
        # Learn habit if repeated
        pattern = decision['reason']
        if pattern in self.basal['habits']:
            # Increase habit strength
            pass
        else:
            # New habit
            if random.random() < 0.1:  # 10% chance to learn
                self.basal['habits'][pattern] = action
        
        # Cerebellum coordination
        self.cerebellum['commands'].append(action)
        if len(self.cerebellum['commands']) > 100:
            self.cerebellum['commands'].pop(0)
        
        # Update growing NN
        complexity = self.growing_nn.calculate_complexity(
            decision, affect
        )
        error = self.growing_nn.error_rate
        
        if self.growing_nn.should_grow_node(self.growing_nn.novelty, error):
            self.growing_nn.grow_node()
        
        if self.growing_nn.should_grow_layer(complexity):
            self.growing_nn.grow_layer()
        
        # Update RL
        reward = self.rl_core.get_reward(decision['type'], action)
        self.rl_core.update_q(decision['reason'], decision['type'], reward, '')
        
        # Auto-dice every 100 ticks
        if self.tick % 100 == 0:
            self.dice.roll()
        
        return action
    
    def _learn(self, obs: Dict, decision: Dict, action: Dict, affect: Dict) -> None:
        """LEARN - Store memory trace."""
        trace = {
            'tick': self.tick,
            'observation': obs,
            'decision': decision,
            'action': action,
            'affect': affect,
            'nn_state': self.growing_nn.get_state()
        }
        
        self.hippocampus['traces'].append(trace)
        if len(self.hippocampus['traces']) > self.hippocampus['max_traces']:
            self.hippocampus['traces'].pop(0)
        
        # Update error tracking
        if self.decision_history:
            prev_decision = self.decision_history[-2] if len(self.decision_history) > 1 else None
            if prev_decision:
                self.growing_nn.update_error(
                    prev_decision.get('type'),
                    decision.get('type')
                )
    
    def _update_consciousness(self, obs: Dict, decision: Dict) -> None:
        """Update consciousness layers."""
        # CONSCIOUS
        self.conscious['working_memory'].append(obs.get('input', '')[:100])
        if len(self.conscious['working_memory']) > 7:
            self.conscious['working_memory'].pop(0)
        self.conscious['attention_ticks'] += 1
        
        # Transfer to SUBCONSCIOUS if attention exhausted
        if self.conscious['attention_ticks'] >= self.conscious['max_attention']:
            self.subconscious['buffer'].extend(self.conscious['working_memory'])
            self.conscious['working_memory'].clear()
            self.conscious['attention_ticks'] = 0
            self.subconscious['active'] = True
        
        # Transfer to UNCONSCIOUS if buffer full
        if len(self.subconscious['buffer']) > self.subconscious['max_buffer']:
            old = self.subconscious['buffer'].pop(0)
            key = hashlib.md5(str(old).encode()).hexdigest()[:16]
            self.unconscious['deep_memory'][key] = old
            self.unconscious['active'] = True
            
            if len(self.unconscious['deep_memory']) > self.unconscious['max_deep']:
                oldest = next(iter(self.unconscious['deep_memory']))
                del self.unconscious['deep_memory'][oldest]
    
    def _get_region_states(self) -> Dict:
        """Get all 7 region states."""
        return {
            'thalamus': self.thalamus,
            'hippocampus': {
                'traces': len(self.hippocampus['traces']),
                'novelty_avg': self.hippocampus['novelty_avg']
            },
            'limbic': self.limbic,
            'pfc': self.pfc,
            'basal': self.basal,
            'cerebellum': self.cerebellum,
            'brainstem': self.brainstem
        }
    
    def _get_consciousness_state(self) -> Dict:
        """Get 3-tier consciousness state."""
        return {
            'conscious': self.conscious,
            'subconscious': self.subconscious,
            'unconscious': self.unconscious
        }
    
    def get_status(self) -> Dict:
        """Get full brain status."""
        return {
            'identity': {
                'name': self.name,
                'designation': self.designation,
                'ship': self.ship,
                'version': self.version,
                'version_date': self.version_date
            },
            'tick': self.tick,
            'phase': self.phase.value.upper(),
            'uptime_seconds': int(self.uptime),
            'regions': self._get_region_states(),
            'consciousness': self._get_consciousness_state(),
            'growingnn': self.growing_nn.get_state(),
            'qmd': self.qmd_loop.get_state(),
            'memory_bridge': self.memory_bridge.get_state(),
            'dice': self.dice.get_state(),
            'rl': self.rl_core.get_state(),
            'visual': self.visual_cortex.get_state()
        }
    
    def recall(self, query: str) -> Optional[str]:
        """Recall memory from any layer."""
        # Check conscious first
        for mem in self.conscious['working_memory']:
            if query.lower() in mem.lower():
                return f"[CONSCIOUS] {mem}"
        
        # Check subconscious
        for mem in self.subconscious['buffer']:
            if query.lower() in mem.lower():
                return f"[SUBCONSCIOUS] {mem}"
        
        # Check unconscious
        for key, mem in self.unconscious['deep_memory'].items():
            if query.lower() in str(mem).lower():
                return f"[UNCONSCIOUS] {mem}"
        
        # Check hippocampus traces
        for trace in reversed(self.hippocampus['traces']):
            obs = trace.get('observation', {})
            content = obs.get('input', '')
            if query.lower() in content.lower():
                return f"[HIPPOCAMPUS] {content}"
        
        return None


# ============ MAIN ============

def main():
    print("=" * 70)
    print("🧠 MORTY BRAIN AOCROS v" + VERSION)
    print("=" * 70)
    print()
    
    # Create brain
    brain = MortyBrain()
    
    # Curriculum
    curriculum = [
        "What is the capital of France?",
        "Tell me about machine learning",
        "Create a new file called test.txt",
        "The mitochondria is the powerhouse of the cell",
        "Python uses indentation for code blocks",
        "Prime numbers are only divisible by 1 and themselves",
        "Shakespeare wrote Romeo and Juliet",
        "The golden ratio is approximately 1.618",
    ]
    
    print("📚 Processing curriculum...")
    for item in curriculum:
        result = brain.tick_cycle(item)
        print(f"  ✓ [{result['phase']}] {item[:40]}...")
        print(f"    Decision: {result['decision']['type']} ({result['decision']['confidence']:.0%})")
        print(f"    Affect: {result['affect']['mode']} (reward: {result['affect']['reward']:.0%})")
    
    print()
    
    # Get status
    status = brain.get_status()
    
    print("=" * 70)
    print("📊 FULL BRAIN STATUS")
    print("=" * 70)
    
    print()
    print("🧠 7 BRAIN REGIONS")
    print("-" * 50)
    regions = status['regions']
    print(f"Thalamus:     Processed {regions['thalamus']['processed']} inputs")
    print(f"Hippocampus:  {regions['hippocampus']['traces']} traces, novelty: {regions['hippocampus']['novelty_avg']:.0%}")
    print(f"Limbic:      Mode={regions['limbic']['mode']}, reward={regions['limbic']['reward']:.0%}")
    print(f"PFC:         {regions['pfc']['decisions']} decisions, confidence={regions['pfc']['confidence']:.0%}")
    print(f"Basal:       {len(regions['basal']['habits'])} habits, {regions['basal']['activations']} activations")
    print(f"Cerebellum:  {len(regions['cerebellum']['commands'])} commands")
    print(f"Brainstem:   Survival={regions['brainstem']['survival']:.0%}, safety={not regions['brainstem']['safety_override']}")
    
    print()
    print("🧩 3-TIER CONSCIOUSNESS")
    print("-" * 50)
    con = status['consciousness']
    print(f"CONSCIOUS:    Active={con['conscious']['active']}, working={len(con['conscious']['working_memory'])}")
    print(f"SUBCONSCIOUS: Active={con['subconscious']['active']}, buffer={len(con['subconscious']['buffer'])}")
    print(f"UNCONSCIOUS:  Active={con['unconscious']['active']}, deep={len(con['unconscious']['deep_memory'])}")
    
    print()
    print("🧬 GROWING NEURAL NETWORK")
    print("-" * 50)
    nn = status['growingnn']
    print(f"Layers:      {nn['layers']}")
    print(f"Total Nodes: {nn['total_nodes']}")
    print(f"Error Rate:  {nn['error_rate']:.0%}")
    print(f"Complexity:  {nn['complexity']:.0%}")
    print(f"Growth Events: {nn['growth_events']}")
    
    print()
    print("⚡ QMD LOOP")
    print("-" * 50)
    qmd = status['qmd']
    print(f"Cycles:      {qmd['cycles']}")
    print(f"Avg Latency: {qmd['avg_latency_ms']:.1f}ms")
    print(f"Model:       {qmd['model']}")
    
    print()
    print("🎲 DICE")
    print("-" * 50)
    dice = status['dice']
    print(f"Last Roll:   {dice['last_roll']}")
    print(f"Total Rolls: {dice['rolls']}")
    
    print()
    print("📈 RL CORE")
    print("-" * 50)
    rl = status['rl']
    print(f"Reward:      {rl['reward']:.2f}")
    print(f"States:      {rl['states_learned']}")
    print(f"Exploration: {rl['exploration_rate']:.0%}")
    
    # Recall test
    print()
    print("🔍 RECALL TEST")
    print("-" * 50)
    queries = ["mitochondria", "python", "prime", "shakespeare"]
    for q in queries:
        result = brain.recall(q)
        if result:
            layer = result.split(']')[0].replace('[', '')
            print(f"  '{q}': Found in {layer}")
        else:
            print(f"  '{q}': Not found")
    
    print()
    print("=" * 70)
    print(f"Total Ticks: {status['tick']}")
    print(f"Uptime: {status['uptime_seconds']}s")
    print("=" * 70)


if __name__ == "__main__":
    main()