#!/usr/bin/env python3
"""
Mortimer Academy - Curriculum Tracker
Tests brain learning by studying and reporting
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

MORTIMER_DIR = os.path.expanduser("~/mortimer")
BRAIN_DIR = os.path.expanduser("~/AOS-Brain")
MEMORY_DIR = os.path.join(BRAIN_DIR, "memory")

class CurriculumTracker:
    def __init__(self):
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = os.path.join(MORTIMER_DIR, "memory", f"curriculum-{self.today}.md")
        self.curriculum_file = os.path.join(BRAIN_DIR, "curriculum", 
            "aos-brain-academy-v2-mortimer-enhanced.json")
        self.progress_file = os.path.join(MORTIMER_DIR, "memory", "curriculum_progress.json")
        self.stages = []
        self.current_stage = 0
        self.current_module = 0
        self.load_curriculum()
        self.load_progress()
        
    def load_curriculum(self):
        """Load curriculum from JSON"""
        with open(self.curriculum_file) as f:
            data = json.load(f)
            self.stages = data['stages']
        print(f"📚 Loaded {len(self.stages)} stages")
        
    def load_progress(self):
        """Load saved progress"""
        if os.path.exists(self.progress_file):
            with open(self.progress_file) as f:
                p = json.load(f)
                self.current_stage = p.get('stage', 0)
                self.current_module = p.get('module', 0)
            print(f"📊 Progress: Stage {self.current_stage}, Module {self.current_module}")
        else:
            self.save_progress()
            
    def save_progress(self):
        """Save current progress"""
        with open(self.progress_file, 'w') as f:
            json.dump({
                'stage': self.current_stage,
                'module': self.current_module,
                'updated': self.today
            }, f, indent=2)
            
    def log(self, text):
        """Log to today's curriculum file"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {text}"
        print(line)
        with open(self.log_file, 'a') as f:
            f.write(line + "\n")
            
    def get_current_item(self):
        """Get current stage and module"""
        if self.current_stage >= len(self.stages):
            return None, None
        stage = self.stages[self.current_stage]
        modules = stage.get('modules', [])
        if self.current_module >= len(modules):
            return stage, None
        return stage, modules[self.current_module]
    
    def study(self, topic):
        """Study a topic and save learning"""
        self.log(f"📖 STUDIED: {topic}")
        
        # Save to brain memory
        memory_file = os.path.join(MEMORY_DIR, f"study-{self.today}.md")
        with open(memory_file, 'a') as f:
            f.write(f"\n## {topic}\nStudied at {datetime.now().isoformat()}\n")
            
        # Update progress
        self.current_module += 1
        
        # Check if stage complete
        stage, modules = self.get_current_item()
        if modules is None and self.current_module > 0:
            self.log(f"✅ STAGE {stage['stage']} COMPLETE: {stage['name']}")
            self.current_stage += 1
            self.current_module = 0
            
        self.save_progress()
        
    def run(self):
        """Run curriculum session"""
        print("=" * 60)
        print("🎓 MORTIMER ACADEMY - Brain Learning Test")
        print("=" * 60)
        
        study_files = list(Path(MEMORY_DIR).glob('study-*.md'))
        print(f"Prior sessions: {len(study_files)}")
        print()
        
        # Get current position
        stage, module = self.get_current_item()
        
        if stage is None:
            print("🎉 ALL STAGES COMPLETE!")
            return
            
        print(f"📍 Stage {stage['stage']}: {stage['name']}")
        if module:
            print(f"📍 Module: {module.get('name', 'Unknown')}")
            print(f"📝 {module.get('content', 'N/A')[:200]}...")
        print()
        
        # Log session
        self.log(f"ACADEMY SESSION - Stage {stage['stage']}, Module {self.current_module + 1}")
        
        # Return what we should study
        return {
            'stage': stage,
            'module': module,
            'progress': f"{self.current_stage + 1}/{len(self.stages)}"
        }

def main():
    tracker = CurriculumTracker()
    result = tracker.run()
    
    if result and result['module']:
        module = result['module']
        tracker.log(f"MODULE: {module['name']}")
        tracker.log(f"CONTENT: {module['content'][:500]}")
        tracker.log(f"ASSESSMENT: {module.get('assessment', 'N/A')}")
        
        # Mark as studied
        tracker.study(module['name'])
        
        print()
        print("=" * 40)
        tracker.log("Session complete. Brain updated.")
        
if __name__ == "__main__":
    main()
