#!/usr/bin/env python3
"""
Continuous Data Feeder
Feeds workspace files to stomach for chunking and digestion
Brain absorbs chunked data
"""

import sys
import os
import time
import glob
sys.path.insert(0, '/root/.openclaw/workspace/aos_brain_py/stomach')
sys.path.insert(0, '/root/.openclaw/workspace/AOS/brain')

from ternary_stomach import TernaryStomach, StomachState

class DataFeeder:
    """Feeds actual workspace data to stomach for brain absorption"""
    
    def __init__(self):
        self.stomach = TernaryStomach()
        self.workspace = "/root/.openclaw/workspace"
        self.chunks_fed = 0
        self.files_fed = 0
        print("[DataFeeder] Initialized")
        
    def scan_workspace(self):
        """Find all files in workspace"""
        files = []
        
        # Code files
        files.extend(glob.glob(f"{self.workspace}/**/*.py", recursive=True))
        files.extend(glob.glob(f"{self.workspace}/**/*.md", recursive=True))
        files.extend(glob.glob(f"{self.workspace}/**/*.json", recursive=True))
        files.extend(glob.glob(f"{self.workspace}/**/*.txt", recursive=True))
        
        # Config files
        files.extend(glob.glob(f"{self.workspace}/**/*.yaml", recursive=True))
        files.extend(glob.glob(f"{self.workspace}/**/*.yml", recursive=True))
        
        return files[:1000]  # Limit to first 1000
    
    def feed_file(self, filepath):
        """Feed a single file to stomach"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if len(content) < 100:
                return 0
            
            # Calculate nutrition based on content type
            nutrition = 0.5
            if '.py' in filepath:
                nutrition = 0.8  # Code is high nutrition
            elif '.md' in filepath:
                nutrition = 0.6  # Docs are medium
            elif '.json' in filepath:
                nutrition = 0.7  # Data is good
            
            # Feed to stomach
            self.stomach.consume(content, complexity=0.3, nutrition=nutrition)
            self.files_fed += 1
            
            # Digest and get chunks for brain
            self.stomach.digest()
            
            # Get chunks ready for brain
            brain_chunks = self.stomach.get_chunks_for_brain(count=5)
            
            for chunk in brain_chunks:
                self.chunks_fed += 1
                print(f"  [Chunk {self.chunks_fed}] {chunk['content'][:60]}... (nutrition: {chunk['nutrition']:.2f})")
            
            return len(brain_chunks)
            
        except Exception as e:
            print(f"  Error feeding {filepath}: {e}")
            return 0
    
    def feed_workspace(self):
        """Feed entire workspace to stomach"""
        print("\n[DataFeeder] Scanning workspace...")
        files = self.scan_workspace()
        print(f"Found {len(files)} files")
        
        print("\n[DataFeeder] Feeding files to stomach...")
        for i, filepath in enumerate(files[:50]):  # Feed first 50
            if i % 10 == 0:
                print(f"  Progress: {i}/{len(files[:50])} files")
            
            chunks = self.feed_file(filepath)
            
            # Check stomach status
            if self.stomach.state == StomachState.FULL:
                print("  Stomach FULL - processing before continuing")
                for _ in range(3):
                    self.stomach.digest()
                time.sleep(1)
            
            time.sleep(0.1)
        
        print(f"\n[DataFeeder] Summary:")
        print(f"  Files fed: {self.files_fed}")
        print(f"  Chunks created: {self.chunks_fed}")
        print(f"  Stomach state: {self.stomach.state.name}")
        
        # Final digestion
        print("\n[DataFeeder] Final digestion...")
        for _ in range(10):
            self.stomach.digest()
        
        # Get energy outputs
        outputs = self.stomach.get_outputs()
        print(f"\n  Energy available: {outputs['energy_available']:.2f}")
        print(f"  → Heart: {outputs['heart_energy']:.2f}")
        print(f"  → Brain: {outputs['brain_energy']:.2f}")
        print(f"  → System: {outputs['system_energy']:.2f}")
        
        return self.chunks_fed
    
    def continuous_feed(self):
        """Keep feeding data continuously"""
        print("\n[DataFeeder] Starting continuous feed...")
        files = self.scan_workspace()
        
        idx = 0
        while True:
            if idx >= len(files):
                idx = 0  # Loop back
            
            filepath = files[idx]
            self.feed_file(filepath)
            idx += 1
            
            # Periodic digestion
            if idx % 5 == 0:
                self.stomach.digest()
                time.sleep(0.5)
            
            time.sleep(0.2)

def main():
    """Run data feeder"""
    print("=" * 70)
    print("DATA FEEDER - Stomach > Brain Pipeline")
    print("=" * 70)
    print("\nThis feeder:")
    print("  • Scans workspace for files")
    print("  • Feeds files to stomach")
    print("  • Stomach chunks data")
    print("  • Brain absorbs chunks")
    print("  • Energy distributed to heart/brain/system")
    
    feeder = DataFeeder()
    total_chunks = feeder.feed_workspace()
    
    print("\n" + "=" * 70)
    print("FEED COMPLETE")
    print("=" * 70)
    print(f"\nTotal chunks ready for brain: {total_chunks}")
    print("\nStarting continuous feed...")
    print("(Press Ctrl+C to stop)")
    
    try:
        feeder.continuous_feed()
    except KeyboardInterrupt:
        print("\n\nData feeder stopped")

if __name__ == "__main__":
    main()
