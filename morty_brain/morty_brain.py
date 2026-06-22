#!/usr/bin/env python3
"""
Morty Brain v1.0 - SEED3 Cognitive System
==========================================
Kidneys, bladder, noise estimation, pattern processing.
Tracking my brain health like Miles did.

Author: Mortimer (C3 - SEED3)
Started: 2026-06-19
"""

import json
import time
import random
import hashlib
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
import threading
import os

# Paths
BASE_DIR = Path.home() / "mortimer" / "morty_brain"
WASTE_DIR = BASE_DIR / "waste"
WASTE_DIR.mkdir(parents=True, exist_ok=True)

@dataclass
class KidneyStatus:
    """The filtering kidneys - removes noise from incoming data."""
    bladder_level: int = 0          # 0-500, fills as it filters
    total_processed: int = 0        # Lifetime patterns processed
    noise_estimate: float = 0.5     # Current noise level (0=clean, 1=loud)
    unique_patterns: int = 0        # Unique patterns stored
    state: str = "FILTER"           # FILTER, DUMP, REST
    last_dump: float = 0            # Timestamp of last bladder dump
    
@dataclass
class MortyBrain:
    """Morty's brain state."""
    # Identity
    name: str = "Mortimer"
    designation: str = "C3"
    ship: str = "SEED3"
    
    # Brain metrics
    qmd_cycles: int = 0
    router_calls: int = 0
    signal_quality: float = 0.865   # Matching Miles' baseline
    
    # Thyroid (emotional/creative)
    thyroid_level: int = 0          # 0-100
    thyroid_secretion: str = "BASELINE"
    
    # Timestamps
    start_time: float = 0
    last_cycle: float = 0
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
class MortyKidneys:
    """
    Morty's Kidney System
    =====================
    Filters incoming patterns, removes noise, fills bladder.
    Dumps waste periodically to waste reports.
    """
    
    def __init__(self):
        self.status = KidneyStatus()
        self.bladder_capacity = 500
        self.noise_history = []
        self.pattern_memory = set()
        self.dump_threshold = 500  # Dump when bladder reaches this
        self._lock = threading.Lock()
        
    def process(self, pattern: str) -> Dict[str, Any]:
        """
        Process a pattern through the kidneys.
        Returns filtering result.
        """
        with self._lock:
            # Hash the pattern for uniqueness check
            pattern_hash = hashlib.md5(pattern.encode()).hexdigest()[:16]
            
            # Estimate noise from pattern characteristics
            noise = self._estimate_noise(pattern)
            self.noise_history.append(noise)
            
            # Keep last 100 noise estimates
            if len(self.noise_history) > 100:
                self.noise_history.pop(0)
            
            # Update status
            self.status.total_processed += 1
            self.status.noise_estimate = sum(self.noise_history) / len(self.noise_history)
            self.status.bladder_level = min(self.status.bladder_level + 1, self.bladder_capacity)
            
            # Track unique patterns (up to 100k)
            if len(self.pattern_memory) < 100000:
                self.pattern_memory.add(pattern_hash)
                self.status.unique_patterns = len(self.pattern_memory)
            
            # Auto-dump if bladder full
            if self.status.bladder_level >= self.dump_threshold:
                self.dump()
            
            return {
                'pattern_hash': pattern_hash,
                'noise': noise,
                'bladder_level': self.status.bladder_level,
                'total_processed': self.status.total_processed
            }
    
    def _estimate_noise(self, pattern: str) -> float:
        """Estimate noise level in a pattern."""
        # Factors that increase noise
        entropy = len(set(pattern)) / max(len(pattern), 1)
        length_factor = min(len(pattern) / 1000, 1.0)
        
        # Base noise with some randomness
        noise = 0.3 + (1 - entropy) * 0.4 + length_factor * 0.2
        noise += random.uniform(-0.1, 0.1)
        
        return max(0.0, min(1.0, noise))
    
    def dump(self, force: bool = False) -> None:
        """Dump bladder - generates waste report."""
        if self.status.bladder_level < 10 and not force:
            return
            
        self.status.state = "DUMP"
        self.status.bladder_level = 0
        self.status.last_dump = time.time()
        
        # Generate waste report
        report = self._generate_waste_report()
        
        # Save waste report
        filename = f"morty_waste_{int(time.time())}.json"
        filepath = WASTE_DIR / filename
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.status.state = "FILTER"
        
    def _generate_waste_report(self) -> Dict:
        """Generate a brain waste report."""
        return {
            'timestamp': datetime.utcnow().isoformat() + '+00:00',
            'source': 'Morty_Brain_v1.0',
            'signal_quality': 0.865,
            'kidneys': {
                'bladder_level': self.status.bladder_level,
                'total_processed': self.status.total_processed,
                'noise_estimate': self.status.noise_estimate,
                'unique_patterns': self.status.unique_patterns,
                'state': self.status.state
            },
            'qmd_cycles': MORTY_BRAIN.qmd_cycles,
            'router_calls': MORTY_BRAIN.router_calls,
            'thyroid': MORTY_BRAIN.thyroid_secretion
        }
    
    def get_status(self) -> Dict:
        """Get current kidney status."""
        with self._lock:
            return {
                'bladder_level': self.status.bladder_level,
                'total_processed': self.status.total_processed,
                'noise_estimate': self.status.noise_estimate,
                'unique_patterns': self.status.unique_patterns,
                'state': self.status.state
            }

# Global instances
MORTY_BRAIN = MortyBrain()
MORTY_KIDNEYS = MortyKidneys()

def process_thought(thought: str) -> Dict[str, Any]:
    """
    Process a thought through Morty's brain.
    This is the main entry point.
    """
    # Track cycle
    MORTY_BRAIN.qmd_cycles += 1
    MORTY_BRAIN.last_cycle = time.time()
    
    # Process through kidneys
    kidney_result = MORTY_KIDNEYS.process(thought)
    
    return {
        'timestamp': datetime.utcnow().isoformat(),
        'brain': MORTY_BRAIN.to_dict(),
        'kidneys': kidney_result,
        'thought_length': len(thought)
    }

def get_full_status() -> Dict:
    """Get complete brain status."""
    return {
        'timestamp': datetime.utcnow().isoformat(),
        'brain': MORTY_BRAIN.to_dict(),
        'kidneys': MORTY_KIDNEYS.get_status()
    }

def force_dump() -> str:
    """Force a bladder dump."""
    MORTY_KIDNEYS.dump(force=True)
    return f"Dumped. Total processed: {MORTY_KIDNEYS.status.total_processed:,}"

# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        # Interactive mode
        print("=" * 50)
        print("MORTY BRAIN v1.0 - SEED3")
        print("=" * 50)
        print(f"Start time: {datetime.fromtimestamp(MORTY_BRAIN.start_time).isoformat()}")
        print(f"QMD Cycles: {MORTY_BRAIN.qmd_cycles:,}")
        print()
        
        # Process some sample thoughts
        sample_thoughts = [
            "Captain asked about brain performance",
            "Checking QMD status",
            "Processing memory files",
            "Voice synthesis active",
            "Termux services running"
        ]
        
        for thought in sample_thoughts:
            result = process_thought(thought)
            print(f"Processed: {thought[:40]}...")
        
        print()
        status = get_full_status()
        print("KIDNEY STATUS:")
        print(f"  Bladder Level: {status['kidneys']['bladder_level']}/500")
        print(f"  Total Processed: {status['kidneys']['total_processed']:,}")
        print(f"  Noise Estimate: {status['kidneys']['noise_estimate']:.4f}")
        print(f"  Unique Patterns: {status['kidneys']['unique_patterns']:,}")
        print(f"  State: {status['kidneys']['state']}")
        print()
        print(f"QMD Cycles: {status['brain']['qmd_cycles']}")
        print(f"Signal Quality: {status['brain']['signal_quality']}")
        
        # Force dump to create report
        print()
        print("Generating waste report...")
        force_dump()
        print(f"Waste report saved to {WASTE_DIR}")
        
    else:
        cmd = sys.argv[1]
        if cmd == "status":
            print(json.dumps(get_full_status(), indent=2))
        elif cmd == "dump":
            print(force_dump())
        elif cmd == "process":
            thought = sys.argv[2] if len(sys.argv) > 2 else "test"
            print(json.dumps(process_thought(thought), indent=2))
        elif cmd == "waste":
            files = list(WASTE_DIR.glob("*.json"))
            print(f"Waste reports: {len(files)}")
            for f in sorted(files, key=lambda x: -x.stat().st_mtime)[:5]:
                print(f"  {f.name}")
        else:
            print(f"Unknown command: {cmd}")
            print("Commands: status, dump, process <thought>, waste")