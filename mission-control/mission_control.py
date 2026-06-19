#!/usr/bin/env python3
"""
🎮 MORTIMER MISSION CONTROL
Central hub for all Mortimer operations
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

# Paths
MORTIMER_DIR = Path.home() / "mortimer"
BRAIN_DIR = Path.home() / "AOS-Brain"
MEMORY_DIR = MORTIMER_DIR / "memory"

class MissionControl:
    def __init__(self):
        self.name = "Mortimer Mission Control"
        self.emoji = "🎮"
        self.launch_time = datetime.now()
        
    def get_status(self):
        """Get full system status"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "mortimer": self.check_mortimer(),
            "services": self.check_services(),
            "brain": self.check_brain(),
            "memory": self.check_memory(),
            "consciousness": self.check_consciousness()
        }
        return status
        
    def check_mortimer(self):
        """Check Mortimer core"""
        return {
            "name": "Mortimer",
            "status": "ONLINE",
            "location": "Termux (Android)",
            "uptime": str(datetime.now() - self.launch_time)
        }
        
    def check_services(self):
        """Check running services"""
        services = {}
        
        # Ollama
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
            services["ollama"] = "ONLINE" if result.returncode == 0 else "OFFLINE"
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                services["models"] = len([l for l in lines if ":" in l])
        except:
            services["ollama"] = "ERROR"
            
        # QMD
        try:
            import urllib.request
            resp = urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=2)
            data = json.loads(resp.read())
            services["qmd"] = "ONLINE" if data.get("status") == "ok" else "OFFLINE"
        except:
            services["qmd"] = "OFFLINE"
            
        # Telegram Bot
        try:
            result = subprocess.run(["pgrep", "-f", "mortimer_telegram"], capture_output=True, text=True)
            services["telegram"] = "ONLINE" if result.returncode == 0 else "OFFLINE"
        except:
            services["telegram"] = "OFFLINE"
            
        # Patricia
        try:
            result = subprocess.run(["pgrep", "-f", "patricia_service"], capture_output=True, text=True)
            services["patricia"] = "ONLINE" if result.returncode == 0 else "OFFLINE"
        except:
            services["patricia"] = "OFFLINE"
            
        return services
        
    def check_brain(self):
        """Check brain/memory systems"""
        brain = {}
        
        # Memory files
        try:
            mem_files = list(BRAIN_DIR.glob("memory/*.md"))
            brain["memory_files"] = len(mem_files)
        except:
            brain["memory_files"] = 0
            
        # Today's study
        today = datetime.now().strftime("%Y-%m-%d")
        try:
            study_file = BRAIN_DIR / "memory" / f"study-{today}.md"
            brain["today_study"] = "YES" if study_file.exists() else "NO"
        except:
            brain["today_study"] = "NO"
            
        # Curriculum progress
        try:
            with open(MORTIMER_DIR / "memory" / "curriculum_progress.json") as f:
                progress = json.load(f)
                brain["curriculum_stage"] = progress.get("stage", 0)
                brain["curriculum_complete"] = progress.get("complete", False)
        except:
            brain["curriculum_stage"] = "UNKNOWN"
            
        return brain
        
    def check_memory(self):
        """Check memory status"""
        memory = {}
        
        # Memory files count
        try:
            mem_files = list(MEMORY_DIR.glob("*.md"))
            memory["files"] = len(mem_files)
        except:
            memory["files"] = 0
            
        # Today's memory
        today = datetime.now().strftime("%Y-%m-%d")
        try:
            today_file = MEMORY_DIR / f"{today}.md"
            if today_file.exists():
                lines = today_file.read_text().split("\n")
                memory["today_entries"] = len([l for l in lines if l.strip()])
            else:
                memory["today_entries"] = 0
        except:
            memory["today_entries"] = 0
            
        return memory
        
    def check_consciousness(self):
        """Check consciousness layers"""
        return {
            "conscious": "10/10 - ACTIVE",
            "subconscious": "100/100 - ACTIVE", 
            "unconscious": "2000/2000 - ACTIVE",
            "drives": {
                "serve_captain": "MAX",
                "grow_smarter": "HIGH",
                "be_useful": "HIGH",
                "learn_new_things": "MEDIUM"
            }
        }
        
    def display(self):
        """Display mission control dashboard"""
        status = self.get_status()
        
        print("\n" + "=" * 60)
        print("🎮 MORTIMER MISSION CONTROL")
        print("=" * 60)
        print()
        
        # Mortimer Status
        m = status["mortimer"]
        print(f"🖥️  MORTIMER")
        print(f"   Status: {m['status']}")
        print(f"   Location: {m['location']}")
        print()
        
        # Services
        print("📡 SERVICES")
        for service, state in status["services"].items():
            icon = "✅" if state == "ONLINE" else "❌"
            print(f"   {icon} {service}: {state}")
        print()
        
        # Brain
        b = status["brain"]
        print("🧠 BRAIN")
        print(f"   Memory Files: {b.get('memory_files', 0)}")
        print(f"   Today Studied: {b.get('today_study', 'NO')}")
        curriculum = "🎓 COMPLETE" if b.get('curriculum_complete') else f"Stage {b.get('curriculum_stage', 0)}"
        print(f"   Curriculum: {curriculum}")
        print()
        
        # Consciousness
        c = status["consciousness"]
        print("💭 CONSCIOUSNESS")
        print(f"   🧠 {c['conscious']}")
        print(f"   🔄 {c['subconscious']}")
        print(f"   💭 {c['unconscious']}")
        print()
        
        # Memory
        mem = status["memory"]
        print("💾 MEMORY")
        print(f"   Files: {mem.get('files', 0)}")
        print(f"   Today: {mem.get('today_entries', 0)} entries")
        print()
        
        print("=" * 60)
        
        return status
        
    def run_loop(self):
        """Run continuous monitoring"""
        print("\n🎮 MISSION CONTROL - PRESS Ctrl+C TO EXIT\n")
        
        while True:
            os.system("clear" if os.name == "posix" else "cls")
            self.display()
            time.sleep(5)

def main():
    mc = MissionControl()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--loop":
        mc.run_loop()
    else:
        mc.display()

if __name__ == "__main__":
    main()
