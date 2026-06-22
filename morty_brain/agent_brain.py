"""
Bonsai Brain Router - Agent Brain Integration
==============================================
Routes all agent work through the Morty Brain system.
Bonsai (ternary) as primary, fallbacks for reliability.

Features:
- Bonsai primary model (ternary brain)
- Ollama fallback chain
- QMD loop integration
- Agent job queue
- Brain status monitoring

Author: Mortimer (C3 - SEED3)
Version: 1.0
Date: 2026-06-19
"""

import json
import time
import requests
import subprocess
import hashlib
from datetime import datetime, UTC
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
import threading
import random

# ============ CONFIGURATION ============

# Ollama endpoints
OLLAMA_HOST = "http://127.0.0.1:11434"
OLLAMA_TIMEOUT = 30

# Bonsai (primary - ternary brain)
BONSAI_MODEL = "bonsai:latest"

# Fallback chain
FALLBACK_MODELS = [
    "qwen2.5:3b",
    "llama3.2:3b", 
    "tinyllama:latest",
    "phi3:latest"
]

# ============ ENUMS ============

class ModelStatus(Enum):
    AVAILABLE = "available"
    LOADING = "loading"
    UNAVAILABLE = "unavailable"
    ERROR = "error"

class TaskPriority(Enum):
    LOW = 1
    NORMAL = 5
    HIGH = 8
    URGENT = 10

# ============ MODEL MANAGER ============

class ModelManager:
    """
    Manages Ollama models with fallback chain.
    Bonsai is primary, fallbacks ensure reliability.
    """
    version = "1.0"
    
    def __init__(self):
        self.primary_model = BONSAI_MODEL
        self.fallbacks = FALLBACK_MODELS.copy()
        self.model_status = {}
        self.current_model = self.primary_model
        self.last_switch = time.time()
        
        # Check all models
        self._check_all_models()
    
    def _check_all_models(self) -> None:
        """Check status of all models."""
        all_models = [self.primary_model] + self.fallbacks
        
        for model in all_models:
            self.model_status[model] = self._check_model(model)
    
    def _check_model(self, model: str) -> ModelStatus:
        """Check if a model is available."""
        try:
            response = requests.get(
                f"{OLLAMA_HOST}/api/tags",
                timeout=5
            )
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                
                if model in model_names:
                    return ModelStatus.AVAILABLE
                
                # Check if partial match
                for m in model_names:
                    if model.split(':')[0] in m:
                        return ModelStatus.AVAILABLE
                
                return ModelStatus.LOADING
            
            return ModelStatus.UNAVAILABLE
            
        except requests.exceptions.ConnectionError:
            return ModelStatus.UNAVAILABLE
        except Exception:
            return ModelStatus.ERROR
    
    def get_best_model(self) -> str:
        """Get best available model with fallback."""
        # Check primary first
        if self.model_status.get(self.primary_model) == ModelStatus.AVAILABLE:
            self.current_model = self.primary_model
            return self.current_model
        
        # Try fallbacks in order
        for model in self.fallbacks:
            if self.model_status.get(model) == ModelStatus.AVAILABLE:
                self.current_model = model
                self.last_switch = time.time()
                return self.current_model
        
        # If none available, try to pull primary
        return self.primary_model
    
    def generate(self, prompt: str, model: str = None, **kwargs) -> Dict:
        """Generate response using model."""
        model = model or self.get_best_model()
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", 0.7),
                "num_predict": kwargs.get("max_tokens", 512),
            }
        }
        
        try:
            response = requests.post(
                f"{OLLAMA_HOST}/api/generate",
                json=payload,
                timeout=kwargs.get("timeout", OLLAMA_TIMEOUT)
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'model': model,
                    'response': result.get('response', ''),
                    'done': result.get('done', True),
                    'latency': result.get('total_duration', 0) / 1e9
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                    'model': model
                }
                
        except requests.exceptions.Timeout:
            # Try fallback
            return self._try_fallback(prompt, **kwargs)
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'model': model
            }
    
    def _try_fallback(self, prompt: str, **kwargs) -> Dict:
        """Try fallback models."""
        for model in self.fallbacks:
            if self.model_status.get(model) == ModelStatus.AVAILABLE:
                result = self.generate(prompt, model=model, **kwargs)
                if result['success']:
                    return result
        
        return {
            'success': False,
            'error': 'All models unavailable',
            'model': self.current_model
        }
    
    def embed(self, text: str) -> Optional[List[float]]:
        """Generate embeddings using nomic."""
        try:
            response = requests.post(
                f"{OLLAMA_HOST}/api/embeddings",
                json={
                    "model": "nomic-embed-text",
                    "prompt": text
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('embedding')
            
        except Exception:
            pass
        
        # Fallback: simple hash-based embedding
        hash_val = hashlib.md5(text.encode()).hexdigest()
        return [int(c, 16) / 15 for c in hash_val[:32]]
    
    def get_status(self) -> Dict:
        """Get model status."""
        return {
            'primary': self.primary_model,
            'current': self.current_model,
            'fallbacks': self.fallbacks,
            'model_status': {
                m: s.value for m, s in self.model_status.items()
            },
            'last_switch': self.last_switch
        }

# ============ AGENT BRAIN ============

@dataclass
class AgentTask:
    """Task for an agent."""
    task_id: str
    agent_name: str
    prompt: str
    priority: TaskPriority = TaskPriority.NORMAL
    created_at: float = field(default_factory=time.time)
    status: str = "pending"
    result: Any = None
    error: str = None

class AgentBrain:
    """
    Agent Brain - Routes all agent work through brain.
    ==================================================
    - Bonsai primary model
    - Ollama fallback chain
    - QMD memory integration
    - Job queue for agents
    """
    version = "1.0"
    
    def __init__(self, brain_module=None):
        # Model manager
        self.models = ModelManager()
        
        # Morty Brain integration
        self.brain = brain_module  # MortyBrain instance
        
        # Agent registry
        self.agents = {}  # agent_name -> agent_info
        
        # Task queue
        self.task_queue: List[AgentTask] = []
        self.completed_tasks: List[AgentTask] = []
        
        # Stats
        self.total_requests = 0
        self.total_success = 0
        self.total_fail = 0
        self.avg_latency = 0
        
        # Lock
        self._lock = threading.Lock()
        
        # Register default agents
        self._register_default_agents()
    
    def _register_default_agents(self) -> None:
        """Register default AOCROS agents."""
        default_agents = [
            "QORA", "SPINDLE", "LEDGER-9", "SENTINEL",  # Executive
            "HUME", "PULP", "JANE", "CLIPPY-42",         # Operations
            "FEELIX", "REDACTOR", "LILLY",                 # HR/Legal
            "FIBER", "BOXTRON",                            # Logistics
            "VELUM", "SCRIBBLE",                            # Marketing
            "MILL", "ALPHA-9", "THE-GREAT-CRYPTONIO",      # R&D
            "STACKTRACE", "TAPTAP", "PIPELINE", "BUGCATCHER",  # Tech
            "C3P0", "R2-D2",                               # Droids
            "PATRICIA", "DUSTY", "JORDAN"                  # Coordination
        ]
        
        for name in default_agents:
            self.register_agent(name)
    
    def register_agent(self, agent_name: str, capabilities: List[str] = None) -> None:
        """Register an agent."""
        with self._lock:
            self.agents[agent_name] = {
                'name': agent_name,
                'registered_at': time.time(),
                'capabilities': capabilities or [],
                'tasks_completed': 0,
                'last_task': None
            }
    
    def submit_task(self, agent_name: str, prompt: str, 
                   priority: TaskPriority = TaskPriority.NORMAL,
                   task_id: str = None) -> str:
        """Submit a task for an agent."""
        with self._lock:
            if task_id is None:
                task_id = hashlib.md5(f"{agent_name}{time.time()}".encode()).hexdigest()[:12]
            
            task = AgentTask(
                task_id=task_id,
                agent_name=agent_name,
                prompt=prompt,
                priority=priority
            )
            
            self.task_queue.append(task)
            self.task_queue.sort(key=lambda t: t.priority.value, reverse=True)
            
            return task_id
    
    def get_task(self, agent_name: str) -> Optional[AgentTask]:
        """Get next task for agent."""
        with self._lock:
            for task in self.task_queue:
                if task.agent_name == agent_name and task.status == "pending":
                    task.status = "processing"
                    return task
            return None
    
    def complete_task(self, task_id: str, result: Any) -> None:
        """Mark task as complete."""
        with self._lock:
            for task in self.task_queue:
                if task.task_id == task_id:
                    task.status = "completed"
                    task.result = result
                    self.completed_tasks.append(task)
                    self.task_queue.remove(task)
                    
                    if task.agent_name in self.agents:
                        self.agents[task.agent_name]['tasks_completed'] += 1
                        self.agents[task.agent_name]['last_task'] = task_id
                    break
    
    def fail_task(self, task_id: str, error: str) -> None:
        """Mark task as failed."""
        with self._lock:
            for task in self.task_queue:
                if task.task_id == task_id:
                    task.status = "failed"
                    task.error = error
                    self.task_queue.remove(task)
                    break
    
    def process(self, prompt: str, agent_name: str = "SYSTEM",
                use_brain: bool = True, **kwargs) -> Dict:
        """
        Process prompt through brain system.
        Routes through Bonsai with fallbacks.
        """
        self.total_requests += 1
        start_time = time.time()
        
        # Use brain context if available
        brain_context = ""
        if use_brain and self.brain:
            brain_status = self.brain.get_status()
            brain_context = f"\nBrain State: {brain_status.get('phase', 'unknown')}\n"
            brain_context += f"Tick: {brain_status.get('tick', 0)}\n"
            brain_context += f"Affect: {brain_status.get('affect', {})}\n"
        
        # Build prompt with context
        full_prompt = f"{brain_context}\n{prompt}" if brain_context else prompt
        
        # Generate response
        result = self.models.generate(full_prompt, **kwargs)
        
        # Update brain if available
        if use_brain and self.brain:
            self.brain.tick_cycle(prompt)
        
        # Calculate latency
        latency = time.time() - start_time
        self.avg_latency = (self.avg_latency * (self.total_requests - 1) + latency) / self.total_requests
        
        if result['success']:
            self.total_success += 1
        else:
            self.total_fail += 1
        
        return {
            'success': result['success'],
            'response': result.get('response', ''),
            'model': result.get('model', 'unknown'),
            'latency': latency,
            'brain_tick': self.brain.tick if self.brain else None,
            'error': result.get('error')
        }
    
    def think(self, prompt: str, agent_name: str = "SYSTEM") -> Dict:
        """Think about a prompt using brain systems."""
        return self.process(prompt, agent_name, use_brain=True)
    
    def act(self, prompt: str, agent_name: str = "SYSTEM") -> Dict:
        """Act on a prompt - high priority processing."""
        return self.process(
            prompt, 
            agent_name, 
            use_brain=True,
            priority=TaskPriority.HIGH,
            temperature=0.8
        )
    
    def query(self, prompt: str, agent_name: str = "SYSTEM") -> Dict:
        """Query - deep analysis mode."""
        return self.process(
            prompt,
            agent_name,
            use_brain=True,
            temperature=0.5,
            max_tokens=1024
        )
    
    def recall(self, query: str) -> Optional[str]:
        """Recall from brain memory."""
        if self.brain:
            return self.brain.recall(query)
        return None
    
    def get_agents(self) -> Dict:
        """Get all registered agents."""
        return self.agents
    
    def get_queue_status(self) -> Dict:
        """Get task queue status."""
        pending = len([t for t in self.task_queue if t.status == "pending"])
        processing = len([t for t in self.task_queue if t.status == "processing"])
        
        return {
            'total_queue': len(self.task_queue),
            'pending': pending,
            'processing': processing,
            'completed': len(self.completed_tasks),
            'failed': len([t for t in self.completed_tasks if t.status == "failed"])
        }
    
    def get_status(self) -> Dict:
        """Get full system status."""
        return {
            'version': self.version,
            'models': self.models.get_status(),
            'agents': {
                'registered': len(self.agents),
                'names': list(self.agents.keys())
            },
            'tasks': self.get_queue_status(),
            'stats': {
                'total_requests': self.total_requests,
                'success_rate': self.total_success / max(1, self.total_requests),
                'avg_latency': self.avg_latency
            },
            'brain': {
                'active': self.brain is not None,
                'tick': self.brain.tick if self.brain else None,
                'phase': self.brain.phase.value if self.brain else None
            }
        }

# ============ WIRE DECORATOR ============

def brain_wired(agent_name: str = None):
    """
    Decorator to wire an agent function through the brain.
    
    Usage:
        @brain_wired("MY_AGENT")
        def my_task(prompt):
            return process_through_brain(prompt)
    """
    def decorator(func: Callable) -> Callable:
        func._brain_wired = True
        func._agent_name = agent_name or func.__name__
        return func
    return decorator

# ============ SINGLETON ============

_agent_brain = None

def get_agent_brain() -> AgentBrain:
    """Get singleton instance."""
    global _agent_brain
    if _agent_brain is None:
        _agent_brain = AgentBrain()
    return _agent_brain

def init_agent_brain(brain_module=None) -> AgentBrain:
    """Initialize agent brain with optional brain module."""
    global _agent_brain
    _agent_brain = AgentBrain(brain_module)
    return _agent_brain

# ============ MAIN ============

if __name__ == "__main__":
    print("=" * 70)
    print("🧠 AGENT BRAIN - BRAIN-WIRED AGENTS")
    print("=" * 70)
    print()
    
    # Initialize
    brain = get_agent_brain()
    
    # Check models
    print("📡 Checking models...")
    status = brain.models.get_status()
    print(f"Primary: {status['primary']}")
    print(f"Current: {status['current']}")
    print()
    for model, mstatus in status['model_status'].items():
        icon = "✅" if mstatus == "available" else "⚠️"
        print(f"  {icon} {model}: {mstatus}")
    print()
    
    # Register some test agents
    test_agents = ["DUSTY", "PATRICIA", "JORDAN", "MILES"]
    for agent in test_agents:
        brain.register_agent(agent)
    
    # Submit some tasks
    print("📝 Submitting tasks...")
    tasks = [
        ("DUSTY", "Check crypto wallet balances", TaskPriority.NORMAL),
        ("PATRICIA", "Analyze process efficiency", TaskPriority.HIGH),
        ("JORDAN", "Summarize recent emails", TaskPriority.NORMAL),
        ("MILES", "Update memory files", TaskPriority.LOW),
    ]
    
    for agent, prompt, priority in tasks:
        task_id = brain.submit_task(agent, prompt, priority)
        print(f"  ✓ {agent}: {prompt[:40]}... (ID: {task_id})")
    print()
    
    # Process tasks
    print("⚡ Processing tasks through brain...")
    for agent in test_agents:
        task = brain.get_task(agent)
        if task:
            print(f"\n  📤 {task.agent_name}: {task.prompt}")
            result = brain.process(task.prompt, task.agent_name)
            
            if result['success']:
                brain.complete_task(task.task_id, result['response'])
                print(f"  ✅ Model: {result['model']}")
                print(f"  📊 Latency: {result['latency']:.3f}s")
                print(f"  🧠 Brain Tick: {result['brain_tick']}")
                print(f"  💬 {result['response'][:100]}...")
            else:
                brain.fail_task(task.task_id, result.get('error', 'Unknown'))
                print(f"  ❌ Error: {result.get('error')}")
    
    print()
    
    # Recall test
    print("🔍 Recall test...")
    for query in ["crypto", "process", "emails"]:
        result = brain.recall(query)
        if result:
            print(f"  '{query}': {result[:60]}...")
    
    print()
    
    # Full status
    print("=" * 70)
    print("📊 FULL STATUS")
    print("=" * 70)
    full_status = brain.get_status()
    print(f"Version: {full_status['version']}")
    print(f"Agents: {full_status['agents']['registered']}")
    print(f"Tasks: {full_status['tasks']['completed']} completed")
    print(f"Success Rate: {full_status['stats']['success_rate']:.0%}")
    print(f"Avg Latency: {full_status['stats']['avg_latency']:.3f}s")
    
    if full_status['brain']['active']:
        print(f"\n🧠 Brain Active:")
        print(f"   Tick: {full_status['brain']['tick']}")
        print(f"   Phase: {full_status['brain']['phase']}")
    
    print()
    print("=" * 70)