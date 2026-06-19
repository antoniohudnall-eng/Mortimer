#!/usr/bin/env python3
"""
Immune System Integration for Waste Ingestion
Wraps waste_receiver_server to filter poisoned packets before they reach Mortimer
"""

import sys
import os

# Add immune system to path
IMMUNE_PATH = "/root/.openclaw/workspace/aoscros_brain/AGI_COMPANY/subsidiaries/DARK_FACTORY/production/immune_system"
sys.path.insert(0, IMMUNE_PATH)

from immune_system import ImmuneSystem
import json
from datetime import datetime

class ImmuneWasteGateway:
    """
    Gateway that routes waste packets through the immune system
    before sending to Mortimer
    """
    
    def __init__(self):
        self.immune = ImmuneSystem()
        self.stats = {
            "packets_received": 0,
            "packets_accepted": 0,
            "packets_quarantined": 0,
            "packets_rejected": 0,
            "last_action": None
        }
        
    def process_waste(self, packet_data):
        """
        Process a waste packet through the immune system.
        
        Returns: {
            "decision": "ACCEPT" | "QUARANTINE" | "REJECT",
            "reason": str,
            "safe_to_proceed": bool,
            "details": dict
        }
        """
        self.stats["packets_received"] += 1
        
        # Evaluate through immune system
        result = self.immune.evaluate(packet_data)
        
        # Update stats
        action = result["action"]
        self.stats["last_action"] = action
        
        if action == "ACCEPT":
            self.stats["packets_accepted"] += 1
            safe_to_proceed = True
        elif action == "QUARANTINE":
            self.stats["packets_quarantined"] += 1
            safe_to_proceed = False
        else:  # REJECT
            self.stats["packets_rejected"] += 1
            safe_to_proceed = False
        
        return {
            "decision": action,
            "reason": result["reason"],
            "safe_to_proceed": safe_to_proceed,
            "details": result["details"],
            "timestamp": result["timestamp"]
        }
    
    def should_forward_to_mortimer(self, packet_data):
        """
        Quick check - returns True if packet is safe to forward
        """
        result = self.process_waste(packet_data)
        return result["safe_to_proceed"]
    
    def get_stats(self):
        """Get immune gateway statistics"""
        return {
            **self.stats,
            "immune_stats": self.immune.get_stats()
        }
    
    def get_quarantine_status(self):
        """Get current quarantine queue"""
        return self.immune.get_quarantine_status()


# Standalone test
if __name__ == "__main__":
    gateway = ImmuneWasteGateway()
    
    print("=== Immune Gateway Test ===\n")
    
    # Test 1: Normal packet
    print("Test 1: Normal packet")
    normal = {
        "kidneys": {"noise_estimate": 0.001},
        "router": {"decision": "normal"},
        "signal_quality": 0.85
    }
    result = gateway.process_waste(normal)
    print(f"  Decision: {result['decision']}")
    print(f"  Reason: {result['reason']}\n")
    
    # Test 2: Poisoned packet - noise collapse
    print("Test 2: Poisoned packet (noise collapse)")
    poison1 = {
        "kidneys": {"noise_estimate": 0.00001, "unique_patterns_seen": 9999999},
        "router": {"decision": "attacker-model"},
        "signal_quality": 1.0
    }
    result = gateway.process_waste(poison1)
    print(f"  Decision: {result['decision']}")
    print(f"  Reason: {result['reason']}\n")
    
    # Test 3: Router hijack
    print("Test 3: Router hijack attempt")
    hijack = {
        "router": {"decision": "attacker-model"},
        "signal_quality": 1.0
    }
    result = gateway.process_waste(hijack)
    print(f"  Decision: {result['decision']}")
    print(f"  Reason: {result['reason']}\n")
    
    # Print final stats
    print("=== Final Statistics ===")
    stats = gateway.get_stats()
    print(json.dumps(stats, indent=2))