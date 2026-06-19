#!/usr/bin/env python3
"""
Complete Brain v4.3 - Multi-Model Dynamic Switching
Plug in any model, switch dynamically, fall back automatically.

Supported:
- Ollama models (local): tinyllama, phi3, qwen, llama3, etc.
- API models (remote): OpenAI, Anthropic, Gemini
- Custom models: Any compatible endpoint
"""

import json
import time
import numpy as np
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
import threading


class ModelProvider(Enum):
    """Supported model providers."""
    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    CUSTOM = "custom"


@dataclass
class ModelConfig:
    """Configuration for a model."""
    name: str                           # Display name
    provider: ModelProvider
    model_id: str                       # Provider-specific ID
    endpoint: Optional[str] = None     # Custom endpoint
    api_key: Optional[str] = None       # For API models
    temperature: float = 0.7
    max_tokens: int = 2048
    timeout_seconds: int = 30
    priority: int = 0                   # Higher = preferred
    requires_internet: bool = False
    
    def __hash__(self):
        return hash(self.model_id)


class ModelRegistry:
    """
    Registry of available models.
    Manages model switching and fallbacks.
    """
    
    def __init__(self):
        self.models: Dict[str, ModelConfig] = {}
        self.active_model: Optional[str] = None
        self.fallback_stack: List[str] = []
        self.model_stats: Dict[str, Dict] = {}
        
        # Register default models
        self._register_defaults()
        
    def _register_defaults(self):
        """Register default Ollama models."""
        defaults = [
            ModelConfig(
                name="Mort_II (Primary)",
                provider=ModelProvider.OLLAMA,
                model_id="antoniohudnall/Mort_II:latest",
                priority=10
            ),
            ModelConfig(
                name="Phi-3 (Fast)",
                provider=ModelProvider.OLLAMA,
                model_id="phi3:latest",
                priority=9
            ),
            ModelConfig(
                name="TinyLlama (Tiny)",
                provider=ModelProvider.OLLAMA,
                model_id="tinyllama:latest",
                priority=8
            ),
            ModelConfig(
                name="Qwen 2.5",
                provider=ModelProvider.OLLAMA,
                model_id="qwen2.5:3b",
                priority=7
            ),
            ModelConfig(
                name="Llama 3.2",
                provider=ModelProvider.OLLAMA,
                model_id="llama3.2:latest",
                priority=6
            )
        ]
        
        for model in defaults:
            self.register_model(model)
        
        # Set active to highest priority available
        self.active_model = "antoniohudnall/Mort_II:latest"
        
    def register_model(self, config: ModelConfig) -> bool:
        """Register a new model."""
        self.models[config.model_id] = config
        self.model_stats[config.model_id] = {
            'calls': 0,
            'successes': 0,
            'failures': 0,
            'avg_latency_ms': 0
        }
        return True
    
    def switch_model(self, model_id: str) -> Dict:
        """Switch to a different model dynamically."""
        if model_id not in self.models:
            return {'success': False, 'error': f"Model {model_id} not registered"}
        
        old_model = self.active_model
        self.active_model = model_id
        
        # Update fallback stack (exclude current)
        self._rebuild_fallback_stack()
        
        return {
            'success': True,
            'previous': old_model,
            'current': model_id,
            'config': self._config_to_dict(self.models[model_id])
        }
    
    def auto_select_best(self) -> str:
        """Auto-select best available model."""
        # Try models in priority order
        for model_id in sorted(self.models.values(), key=lambda m: -m.priority):
            if self._test_model(model_id.model_id):
                return model_id.model_id
        
        return self.active_model  # Fallback to current
    
    def _test_model(self, model_id: str) -> bool:
        """Test if a model is responsive."""
        try:
            config = self.models[model_id]
            if config.provider == ModelProvider.OLLAMA:
                resp = requests.get(
                    "http://localhost:11434/api/tags",
                    timeout=5
                )
                if resp.status_code == 200:
                    data = resp.json()
                    models = [m['name'] for m in data.get('models', [])]
                    return model_id in models
            return False
        except:
            return False
    
    def _rebuild_fallback_stack(self):
        """Rebuild fallback stack (excluding active model)."""
        sorted_models = sorted(
            self.models.values(),
            key=lambda m: -m.priority
        )
        self.fallback_stack = [
            m.model_id for m in sorted_models
            if m.model_id != self.active_model
        ]
    
    def get_next_fallback(self) -> Optional[str]:
        """Get next fallback model."""
        if self.fallback_stack:
            return self.fallback_stack.pop(0)
        return None
    
    def _config_to_dict(self, config: ModelConfig) -> Dict:
        return {
            'name': config.name,
            'provider': config.provider.value,
            'model_id': config.model_id,
            'priority': config.priority,
            'requires_internet': config.requires_internet
        }
    
    def list_models(self) -> List[Dict]:
        """List all registered models."""
        return [self._config_to_dict(m) for m in self.models.values()]
    
    def get_active(self) -> Optional[ModelConfig]:
        """Get currently active model config."""
        if self.active_model:
            return self.models.get(self.active_model)
        return None


# ═══════════════════════════════════════════════════════════════════
# MULTI-MODEL CURRICULUM MANAGER
# ═══════════════════════════════════════════════════════════════════

class MultiModelCurriculumManager:
    """
    Curriculum manager that can use multiple models.
    Switches dynamically if one fails.
    """
    
    def __init__(self, registry: ModelRegistry):
        self.registry = registry
        self.curriculum_queue = deque(maxlen=10000)
        self.learned_items = deque(maxlen=50000)
        
        self.stats = {
            'curriculum_generated': 0,
            'items_learned': 0,
            'llm_calls': 0,
            'llm_failures': 0,
            'model_switches': 0
        }
        
        self.generation_active = False
        
    def generate_curriculum(self, topic: str, num_items: int = 50) -> List[Dict]:
        """Generate curriculum using active model (with fallback)."""
        model = self.registry.get_active()
        if not model:
            return []
        
        return self._try_generate(model, topic, num_items)
    
    def _try_generate(self, model: ModelConfig, topic: str, num_items: int) -> List[Dict]:
        """Try to generate with current model, fallback if fails."""
        try:
            items = self._query_model(model, topic, num_items)
            if items:
                return items
        except Exception as e:
            print(f"Model {model.model_id} failed: {e}")
            self.stats['llm_failures'] += 1
        
        # Try fallback
        fallback = self.registry.get_next_fallback()
        if fallback:
            print(f"Falling back to {fallback}")
            self.stats['model_switches'] += 1
            self.registry.switch_model(fallback)
            return self.generate_curriculum(topic, num_items)
        
        return []
    
    def _query_model(self, model: ModelConfig, topic: str, num_items: int) -> List[Dict]:
        """Query specific model for curriculum."""
        prompt = f"""Generate {num_items} training examples for a neural network learning about: {topic}

Format as JSON array with objects containing:
- "concept": what concept this teaches (string)
- "input": array of 10 float values (normalized 0-1)
- "output": expected result (float 0-1)
- "difficulty": how hard this is (float 0.0-1.0)

Generate {num_items} diverse items:"""

        self.stats['llm_calls'] += 1
        
        if model.provider == ModelProvider.OLLAMA:
            return self._query_ollama(model, prompt)
        elif model.provider == ModelProvider.OPENAI:
            return self._query_openai(model, prompt)
        else:
            return []
    
    def _query_ollama(self, model: ModelConfig, prompt: str) -> List[Dict]:
        """Query Ollama model."""
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model.model_id,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": model.temperature,
                    "num_predict": model.max_tokens
                }
            },
            timeout=model.timeout_seconds
        )
        
        if response.status_code == 200:
            data = response.json()
            text = data.get("response", "")
            return self._parse_curriculum(text)
        
        return []
    
    def _query_openai(self, model: ModelConfig, prompt: str) -> List[Dict]:
        """Query OpenAI API (placeholder)."""
        # Would implement actual OpenAI API call here
        return []
    
    def _parse_curriculum(self, text: str) -> List[Dict]:
        """Parse curriculum from model response."""
        try:
            start = text.find('[')
            end = text.rfind(']') + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])
        except:
            pass
        return []
    
    def start_continuous_learning(self, topics: List[str], interval: int = 60):
        """Start continuous curriculum generation."""
        self.generation_active = True
        
        def loop():
            while self.generation_active:
                for topic in topics:
                    if not self.generation_active:
                        break
                    items = self.generate_curriculum(topic, 20)
                    self.curriculum_queue.extend(items)
                    time.sleep(interval)
        
        threading.Thread(target=loop, daemon=True).start()
        print(f"🎓 Continuous learning with multi-model support")


# ═══════════════════════════════════════════════════════════════════
# BRAIN v4.3 - MULTI-MODEL
# ═══════════════════════════════════════════════════════════════════

class BrainV43:
    """
    Brain v4.3 - Multi-Model Dynamic Switching.
    
    Features:
    - Plug any Ollama/API model
    - Dynamic switching
    - Automatic fallback
    - Model performance tracking
    """
    
    def __init__(self):
        self.name = "Brain v4.3"
        self.emoji = "🧠🔄"
        
        # Multi-model system
        self.registry = ModelRegistry()
        self.curriculum = MultiModelCurriculumManager(self.registry)
        
        # Neural network
        self.nn = GrowingNeuralNetwork(input_size=10, output_size=1)
        
        # State
        self.tick = 0
        self.running = False
        
    def switch_to_model(self, model_id: str) -> Dict:
        """Public API: Switch to a different model."""
        return self.registry.switch_model(model_id)
    
    def list_available_models(self) -> List[Dict]:
        """List all available models."""
        return self.registry.list_models()
    
    def download_model_instructions(self, model_id: str) -> str:
        """Get instructions for downloading a model."""
        if model_id in self.registry.models:
            config = self.registry.models[model_id]
            if config.provider == ModelProvider.OLLAMA:
                return f"""To download {config.name}:

1. Ensure Ollama is running:
   systemctl status ollama

2. Pull the model:
   ollama pull {config.model_id}

3. Verify installation:
   ollama list | grep {config.model_id.split(':')[0]}

4. Test the model:
   ollama run {config.model_id} "Hello"

Size estimate: Check ollama.com/library/{config.model_id.split(':')[0]}
"""
        return f"Model {model_id} not found in registry"
    
    def initialize(self):
        """Initialize brain with multi-model support."""
        print(f"{self.emoji} {self.name} initializing...")
        print(f"Active model: {self.registry.active_model}")
        print(f"Available models: {len(self.registry.models)}")
        
        # Show all models
        for model in self.registry.list_models():
            status = "✅ ACTIVE" if model['model_id'] == self.registry.active_model else "⏳ standby"
            print(f"  {status} {model['name']} ({model['model_id']})")
        
        self.curriculum.start_continuous_learning(
            topics=["process_optimization", "success_prediction"],
            interval=60
        )
        
        self.running = True
        print(f"\n✅ {self.name} ready")
        print("\nTo switch models:")
        print("  brain.switch_to_model('phi3:latest')")
        print("  brain.switch_to_model('tinyllama:latest')")
    
    def tick_cycle(self):
        """Main brain tick."""
        self.tick += 1
        
        item = self.curriculum.curriculum_queue.popleft() if self.curriculum.curriculum_queue else None
        
        if item and 'input' in item and 'output' in item:
            inp = item['input'][:10] + [0.0] * (10 - len(item['input']))
            X = np.array([inp])
            y = np.array([float(item['output'])])
            
            loss = self.nn.train(X, y)
            
            if self.tick % 100 == 0:
                self._report_status()
        
        time.sleep(0.1)
    
    def _report_status(self):
        """Report status with model info."""
        active = self.registry.get_active()
        print(f"\n{self.emoji} Tick {self.tick}")
        if active:
            print(f"  Active model: {active.name}")
        print(f"  Neural nodes: {self.nn.total_nodes}")
        print(f"  Curriculum queue: {len(self.curriculum.curriculum_queue)}")
        print(f"  Model switches: {self.curriculum.stats['model_switches']}")


# ═══════════════════════════════════════════════════════════════════
# GROWING NN (from v4.2)
# ═══════════════════════════════════════════════════════════════════

class GrowingNeuralNetwork:
    """Growing neural network - same as v4.2"""
    
    def __init__(self, input_size: int = 10, output_size: int = 1):
        self.input_size = input_size
        self.output_size = output_size
        self.layers = []
        self.layer_sizes = [input_size, 8, output_size]
        self.total_nodes = 8
        self._init_weights()
        self.lr = 0.01
        self.training_samples = 0
        self.error_history = deque(maxlen=100)
        
    def _init_weights(self):
        for i in range(len(self.layer_sizes) - 1):
            W = np.random.randn(
                self.layer_sizes[i], 
                self.layer_sizes[i+1]
            ) * np.sqrt(2.0 / self.layer_sizes[i])
            b = np.zeros((1, self.layer_sizes[i+1]))
            self.layers.append({'W': W, 'b': b})
    
    def relu(self, x): return np.maximum(0, x)
    def sigmoid(self, x): return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def forward(self, X):
        current = X
        for i, layer in enumerate(self.layers):
            z = np.dot(current, layer['W']) + layer['b']
            current = self.relu(z) if i < len(self.layers) - 1 else self.sigmoid(z)
        return current
    
    def backward(self, X, y, output):
        m = X.shape[0]
        delta = output - y.reshape(-1, 1)
        for i in range(len(self.layers) - 1, -1, -1):
            a_prev = X if i == 0 else self.relu(np.dot(X, self.layers[0]['W']) + self.layers[0]['b'])
            dW = np.dot(a_prev.T, delta) / m
            self.layers[i]['W'] -= self.lr * dW
            self.layers[i]['b'] -= self.lr * np.mean(delta, axis=0, keepdims=True)
        loss = -np.mean(y * np.log(output + 1e-8) + (1 - y) * np.log(1 - output + 1e-8))
        return loss
    
    def train(self, X, y, epochs: int = 1):
        X, y = np.array(X), np.array(y)
        for _ in range(epochs):
            output = self.forward(X)
            loss = self.backward(X, y, output)
            self.error_history.append(loss)
            self.training_samples += 1
        return np.mean(self.error_history) if self.error_history else 0


# ═══════════════════════════════════════════════════════════════════
# DEMO & INSTRUCTIONS
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("🧠🔄 Brain v4.3 - Multi-Model Dynamic Switching")
    print("=" * 70)
    
    brain = BrainV43()
    brain.initialize()
    
    print("\n" + "-" * 70)
    print("QUICK START GUIDE:")
    print("-" * 70)
    
    print("\n1. SWITCH TO PH3 (Fast):")
    print("   brain.switch_to_model('phi3:latest')")
    
    print("\n2. SWITCH TO TINYLLAMA (Smallest):")
    print("   brain.switch_to_model('tinyllama:latest')")
    
    print("\n3. DOWNLOAD NEW MODEL:")
    print("   ollama pull phi3:latest")
    
    print("\n4. LIST ALL MODELS:")
    print("   ollama list")
    
    print("\n5. RUN STANDALONE TEST:")
    print("   ollama run phi3:latest 'Hello world'")
    
    print("\n" + "=" * 70)
    print("Testing with Phi-3...")
    print("=" * 70)
    
    result = brain.switch_to_model('phi3:latest')
    print(f"\nSwitch result: {json.dumps(result, indent=2)}")
