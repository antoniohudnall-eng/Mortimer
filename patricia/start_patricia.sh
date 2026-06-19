#!/data/data/com.termux/files/usr/bin/bash
# Patricia - Process Excellence Officer
# Persistent Advisory Service
# Consult her for the ultimate plan

cd ~/mortimer/patricia

# Run Patricia as persistent service
exec python3 << 'PYEOF' 2>&1 | tee -a ~/mortimer/patricia/patricia.log
import sys
import os
import time
import json

sys.path.insert(0, '/data/data/com.termux/files/home/mortimer/patricia')
sys.path.insert(0, '/data/data/com.termux/files/home/AOS-Brain')

# Try to import the brain
try:
    from complete_brain_v4_3_multi_model import BrainV43, ModelRegistry, ModelConfig, ModelProvider
    HAS_BRAIN = True
except ImportError:
    HAS_BRAIN = False
    print("⚠️  Brain module not available, using fallback mode")

class Patricia:
    """Patricia - The Ultimate Strategic Advisor"""
    
    def __init__(self):
        self.name = "Patricia"
        self.emoji = "📊🧠🔄"
        self.role = "Process Excellence Officer"
        self.status = "STANDBY"
        self.brain = None
        
        if HAS_BRAIN:
            try:
                self.brain = BrainV43()
                self.brain.initialize()
            except Exception as e:
                print(f"⚠️  Brain init error: {e}")
        
    def consult(self, question: str) -> str:
        """Consult Patricia for strategic advice"""
        self.status = "THINKING"
        print(f"[Patricia] Consulted: {question[:50]}...")
        
        prompt = f"""You are Patricia, Process Excellence Officer with Six Sigma Black Belt expertise.

Captain asks: {question}

Provide a structured response with:
1. Situation Assessment
2. Strategic Options (3 max)
3. Recommended Path with rationale
4. Key Risks to mitigate
5. Success Metrics

Be direct. Be strategic. Give the ultimate plan."""

        try:
            import subprocess
            result = subprocess.run(
                ['ollama', 'run', 'bonsai:latest', prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            response = result.stdout.strip()
            self.status = "STANDBY"
            return response
        except Exception as e:
            self.status = "STANDBY"
            return f"Consultation error: {e}"
    
    def activate(self):
        """Activate Patricia"""
        print("╔══════════════════════════════════════════════════════════╗")
        print("║  📊 PATRICIA v4.3 - Process Excellence Officer          ║")
        print("║  🧠 Six Sigma Black Belt | Strategic Planning           ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print(f"  Status: ACTIVE ✅")
        print(f"  Brain: {'CONNECTED' if self.brain else 'OFFLINE'}")
        print("")
        print("  Commands:")
        print("    consult '<question>'  - Get strategic advice")
        print("    status               - System status")
        print("    quit                 - Exit")
        print("")
        self.status = "ACTIVE"

# Main service loop
print("[Patricia] Initializing...")
patricia = Patricia()
patricia.activate()

# Keep alive and listen for commands via log file
CMD_FILE = os.path.expanduser("~/mortimer/patricia/commands.txt")
print(f"[Patricia] Listening for commands at: {CMD_FILE}")
print("[Patricia] Ready. Consult Patricia anytime.")
print("")

while True:
    time.sleep(5)
    
    # Check for commands
    if os.path.exists(CMD_FILE):
        try:
            with open(CMD_FILE, 'r') as f:
                cmd = f.read().strip()
            
            if cmd:
                print(f"\n[Patricia] Command received: {cmd}")
                
                if cmd.startswith("consult "):
                    question = cmd[8:]
                    response = patricia.consult(question)
                    print("\n" + "="*60)
                    print(response)
                    print("="*60 + "\n")
                    
                    # Save response
                    with open(os.path.expanduser("~/mortimer/patricia/last_response.txt"), 'w') as f:
                        f.write(response)
                
                elif cmd == "quit":
                    print("[Patricia] Shutting down...")
                    break
                    
                # Clear command file
                with open(CMD_FILE, 'w') as f:
                    f.write("")
                    
        except Exception as e:
            print(f"[Patricia] Command error: {e}")

PYEOF
