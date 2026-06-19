"""Model Router Integration for Agent - Auto-generated v3.1"""
import sys
sys.path.insert(0, '/root/.openclaw/workspace/agents/shared')

try:
    from agent_model_router import get_model_router, check_router_status
    
    # Initialize router on import
    model_router = get_model_router()
    
    # Helper functions
    def decide(context):
        """Make decision using Bonsai/tinyllama"""
        return model_router.decide(context)
    
    def speak(message, context=None):
        """Generate voice response using Mort_II"""
        return model_router.speak(message, context)
    
    def reason(prompt, max_tokens=500):
        """Complex reasoning using qwen2.5:14b"""
        return model_router.reason(prompt, max_tokens)
    
    def code(prompt, language="python", max_tokens=300):
        """Code generation using phi3:medium"""
        return model_router.code(prompt, language, max_tokens)
    
    def ask(question, max_tokens=200):
        """General questions using llama3.1:latest"""
        return model_router.ask(question, max_tokens)
    
    def analyze(text, task="summarize", max_tokens=300):
        """Analysis using mistral:latest MoE"""
        return model_router.analyze(text, task, max_tokens)
    
    def get_router_status():
        """Get Model Router status"""
        return check_router_status()
    
    MODEL_ROUTER_READY = True
    
except ImportError as e:
    MODEL_ROUTER_READY = False
    print(f"⚠️ Model Router not available: {e}")
    
    # Dummy functions
    def decide(c): return "CONTINUE", 0.5
    def speak(m, c=None): return "[Model Router offline]"
    def reason(p, mt=500): return "[Model Router offline]"
    def code(p, l="python", mt=300): return "[Model Router offline]"
    def ask(q, mt=200): return "[Model Router offline]"
    def analyze(t, task="summarize", mt=300): return "[Model Router offline]"
    def get_router_status(): return {"status": "offline"}
