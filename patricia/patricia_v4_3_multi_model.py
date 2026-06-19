#!/usr/bin/env python3
"""
Patricia v4.3 - Multi-Model Agent
Brain learns from ANY model you plug in.
"""

import sys
import os
sys.path.insert(0, '/root/.openclaw/workspace/aocros/brain')

from complete_brain_v4_3_multi_model import BrainV43, ModelRegistry, ModelConfig, ModelProvider
import json


class PatriciaV43:
    """
    Patricia with multi-model brain v4.3.
    Switch between models dynamically.
    """
    
    def __init__(self):
        self.name = "Patricia v4.3"
        self.emoji = "📊🧠🔄"
        self.role = "Multi-Model Process Excellence Officer"
        
        # Multi-model brain
        self.brain = BrainV43()
        
        # State
        self.projects = []
        
    def activate(self):
        """Activate with multi-model support."""
        print(f"{self.emoji} {self.name}")
        print(f"Role: {self.role}")
        self.brain.initialize()
        
    def use_model(self, model_id: str):
        """Switch to a specific model."""
        result = self.brain.switch_to_model(model_id)
        if result['success']:
            print(f"✅ Now using: {result['current']}")
        else:
            print(f"❌ Failed: {result['error']}")
        return result
    
    def list_models(self):
        """Show all available models."""
        models = self.brain.list_available_models()
        print("\n📋 Available Models:")
        for m in models:
            status = "🟢" if m['model_id'] == self.brain.registry.active_model else "⚪"
            print(f"  {status} {m['name']} ({m['model_id']})")
        return models
    
    def get_download_instructions(self, model_id: str = None):
        """Get instructions for downloading a model."""
        if model_id:
            instructions = self.brain.download_model_instructions(model_id)
            print(instructions)
            return instructions
        else:
            print("""
To download a model:

1. Check available models:
   ollama list

2. Download a model:
   ollama pull phi3:latest
   ollama pull tinyllama:latest
   ollama pull qwen2.5:3b

3. Verify download:
   ollama list

4. Test the model:
   ollama run phi3:latest "Hello world"
""")
    
    def run_standalone_test(self, model_id: str, prompt: str = "Explain process optimization in 2 sentences"):
        """Test a model standalone."""
        import subprocess
        
        print(f"\n🧪 Testing {model_id} standalone...")
        print(f"Prompt: '{prompt}'")
        print("-" * 50)
        
        try:
            result = subprocess.run(
                ['ollama', 'run', model_id, prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            print(result.stdout)
            if result.stderr:
                print(f"Stderr: {result.stderr}")
        except Exception as e:
            print(f"Test failed: {e}")
            print("\nMake sure the model is downloaded:")
            print(f"  ollama pull {model_id}")


# ═══════════════════════════════════════════════════════════════════
# AURORA AGENT WITH v4.3 BRAIN
# ═══════════════════════════════════════════════════════════════════

class AuroraV43:
    """
    Aurora - New agent with v4.3 multi-model brain.
    Flexible, adaptive, multi-model capable.
    """
    
    def __init__(self):
        self.name = "Aurora"
        self.emoji = "🌅🧠"
        self.role = "Adaptive Multi-Model Agent"
        
        # Multi-model brain
        self.brain = BrainV43()
        
        # Capabilities
        self.capabilities = [
            "multi_model_learning",
            "dynamic_switching",
            "offline_operation",
            "edge_deployment"
        ]
        
    def activate(self):
        """Activate Aurora."""
        print(f"{self.emoji} {self.name}")
        print(f"Role: {self.role}")
        print(f"Capabilities: {', '.join(self.capabilities)}")
        self.brain.initialize()
        
    def switch_model(self, model_id: str):
        """Switch Aurora's brain to a different model."""
        return self.brain.switch_to_model(model_id)
    
    def learn_with_model(self, model_id: str, topic: str):
        """Learn using a specific model."""
        # Switch to requested model
        self.brain.switch_to_model(model_id)
        
        # Generate curriculum with that model
        items = self.brain.curriculum.generate_curriculum(topic, 10)
        
        print(f"\n🎓 Generated {len(items)} curriculum items using {model_id}")
        return items


# ═══════════════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("PATRICIA v4.3 + AURORA v4.3 - Multi-Model Agents")
    print("=" * 70)
    
    # Demo Patricia
    print("\n📊 Activating Patricia v4.3...")
    patricia = PatriciaV43()
    patricia.activate()
    
    print("\n" + "-" * 70)
    print("MODEL SWITCHING DEMO")
    print("-" * 70)
    
    # Show models
    patricia.list_models()
    
    print("\n" + "=" * 70)
    print("DOWNLOAD INSTRUCTIONS")
    print("=" * 70)
    patricia.get_download_instructions()
    
    print("\n" + "=" * 70)
    print("STANDALONE TEST")
    print("=" * 70)
    print("\nTo test phi3 standalone:")
    print("  python patricia_v4_3_multi_model.py test phi3")
    print("\nTo test tinyllama standalone:")
    print("  python patricia_v4_3_multi_model.py test tinyllama")
    
    # Check for command line args
    if len(sys.argv) > 1:
        if sys.argv[1] == "test" and len(sys.argv) > 2:
            model = sys.argv[2]
            if ":" not in model:
                model = f"{model}:latest"
            patricia.run_standalone_test(model)
