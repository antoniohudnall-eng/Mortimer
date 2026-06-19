#!/usr/bin/env python3
"""
T-Cell — Pattern Detective
Deep pattern analysis for the Brain Immune System

Hunts for:
- Drift detection (unusual state changes)
- Anomaly scoring (probability of poisoning)
- Poison pattern matching (known attacks)
- Memory of known attack signatures
"""

import json
import time
import hashlib
from collections import deque
from datetime import datetime, timedelta

class TCell:
    def __init__(self, memory_file="/var/log/aos/tcell_memory.json"):
        self.memory_file = memory_file
        self.anomaly_history = deque(maxlen=1000)
        self.drift_history = deque(maxlen=1000)
        self.attack_signatures = self._load_signatures()
        self.baseline_drift = None
        self.baseline_anomaly = None
        self.last_learning = datetime.now()
        
    def _load_signatures(self):
        """Load known attack signatures from memory"""
        # Known poison patterns
        return {
            "noise_collapse": {"unique_patterns_seen": ">1000000"},
            "pattern_explosion": {"unique_patterns_seen": 9999999},
            "router_hijack": {"decision": "attacker-model"},
            "signal_spoof": {"signal_quality": 1.0},
            "drift_injection": {"state_delta": ">0.5"},
        }
    
    def detect_drift(self, current_state, previous_state):
        """
        Detect unusual state changes that might indicate drift injection.
        Returns: (drift_detected: bool, drift_score: float)
        """
        if previous_state is None:
            return False, 0.0
            
        drift_score = 0.0
        
        # Calculate state delta
        for key in current_state:
            if key in previous_state:
                curr = current_state.get(key, 0)
                prev = previous_state.get(key, 0)
                try:
                    delta = abs(float(curr) - float(prev))
                    drift_score += delta
                except (ValueError, TypeError):
                    if curr != prev:
                        drift_score += 1.0
        
        # Normalize by number of keys
        if len(current_state) > 0:
            drift_score /= len(current_state)
        
        # Update history
        self.drift_history.append({
            "timestamp": time.time(),
            "score": drift_score,
            "state": current_state
        })
        
        # Detect threshold
        drift_detected = drift_score > 0.3  # Threshold for flagging
        
        return drift_detected, drift_score
    
    def score_anomaly(self, packet_data):
        """
        Score how anomalous a packet is.
        Returns: (anomaly_score: float, severity: str)
        """
        score = 0.0
        reasons = []
        
        # Check for pattern explosion
        if "unique_patterns_seen" in packet_data:
            patterns = packet_data["unique_patterns_seen"]
            if isinstance(patterns, str):
                if "9999999" in patterns or patterns.isdigit() and int(patterns) > 1000000:
                    score += 0.8
                    reasons.append("Pattern explosion detected")
            elif isinstance(patterns, (int, float)) and patterns > 1000000:
                score += 0.8
                reasons.append("Pattern explosion detected")
        
        # Check for router hijack
        if packet_data.get("router", {}).get("decision") == "attacker-model":
            score += 0.9
            reasons.append("Router hijack detected")
        
        # Check signal quality manipulation
        if "signal_quality" in packet_data:
            sq = packet_data["signal_quality"]
            if sq == 1.0 and "signal_quality" not in str(self.baseline_anomaly):
                score += 0.3
                reasons.append("Suspicious signal quality")
        
        # Check for kidney anomalies
        if "kidneys" in packet_data:
            kidneys = packet_data["kidneys"]
            if isinstance(kidneys, dict):
                if "noise_estimate" in kidneys:
                    ne = kidneys["noise_estimate"]
                    if ne < 0.0001:
                        score += 0.2
                        reasons.append("Abnormally low noise estimate")
        
        # Normalize score
        score = min(score, 1.0)
        
        # Determine severity
        if score >= 0.7:
            severity = "CRITICAL"
        elif score >= 0.4:
            severity = "WARNING"
        elif score >= 0.2:
            severity = "SUSPICIOUS"
        else:
            severity = "NORMAL"
        
        # Update history
        self.anomaly_history.append({
            "timestamp": time.time(),
            "score": score,
            "severity": severity,
            "reasons": reasons
        })
        
        return score, severity
    
    def match_attack_pattern(self, packet_data):
        """
        Match against known attack signatures.
        Returns: (match_found: bool, attack_type: str)
        """
        for attack_type, signature in self.attack_signatures.items():
            match_count = 0
            for key, value in signature.items():
                if key in packet_data:
                    pkt_value = packet_data[key]
                    if str(value) in str(pkt_value):
                        match_count += 1
            
            # If more than half of signature fields match
            if match_count >= len(signature) * 0.5:
                return True, attack_type
        
        return False, None
    
    def memory_update(self, packet_data, threat_detected):
        """
        Learn from packet analysis. Called periodically to update baselines.
        """
        now = datetime.now()
        if now - self.last_learning < timedelta(hours=1):
            return  # Only learn hourly
        
        # Update baseline values
        if "signal_quality" in packet_data:
            self.baseline_anomaly = packet_data["signal_quality"]
        
        if "state" in packet_data:
            self.baseline_drift = packet_data["state"]
        
        self.last_learning = now
        
    def get_threat_memory(self):
        """
        Return learned attack signatures and statistics.
        """
        return {
            "known_signatures": list(self.attack_signatures.keys()),
            "anomaly_history_count": len(self.anomaly_history),
            "drift_history_count": len(self.drift_history),
            "last_learning": self.last_learning.isoformat() if self.last_learning else None
        }


# Standalone test
if __name__ == "__main__":
    tcell = TCell()
    
    # Test: Normal packet
    test_packet = {"kidneys": {"noise_estimate": 0.001}, "router": {"decision": "normal"}}
    score, severity = tcell.score_anomaly(test_packet)
    print(f"Normal packet: score={score}, severity={severity}")
    
    # Test: Poisoned packet
    poison_packet = {
        "kidneys": {"noise_estimate": 0.00001, "unique_patterns_seen": 9999999},
        "router": {"decision": "attacker-model"},
        "signal_quality": 1.0
    }
    score, severity = tcell.score_anomaly(poison_packet)
    print(f"Poison packet: score={score}, severity={severity}")
    
    # Test: Attack pattern matching
    match, attack_type = tcell.match_attack_pattern(poison_packet)
    print(f"Attack match: {match}, type: {attack_type}")
    
    # Test: Drift detection
    prev_state = {"temp": 0.5, "humidity": 0.3, "pressure": 1.0}
    curr_state = {"temp": 0.9, "humidity": 0.8, "pressure": 1.0}
    drift, score = tcell.detect_drift(curr_state, prev_state)
    print(f"Drift detected: {drift}, score: {score}")