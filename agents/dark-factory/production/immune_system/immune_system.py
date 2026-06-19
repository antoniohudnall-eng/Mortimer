#!/usr/bin/env python3
"""
Immune Coordinator — Orchestrates White Cell + T-Cell Responses
Determines whether to ACCEPT, QUARANTINE, or REJECT incoming packets
"""

from white_cell import WhiteCell
from t_cell import TCell
import json
import time
from datetime import datetime

class ImmuneSystem:
    def __init__(self):
        self.white_cell = WhiteCell()
        self.t_cell = TCell()
        self.quarantine_log = []
        self.decision_history = []
        
    def evaluate(self, packet, signature=None):
        """
        Main entry point: evaluate a waste packet through the immune system.
        
        Returns: {
            "action": "ACCEPT" | "QUARANTINE" | "REJECT",
            "reason": str,
            "details": dict
        }
        """
        start_time = time.time()
        details = {}
        
        # Step 1: White Cell - Border Patrol
        wc_result = self.white_cell.evaluate(packet, signature)
        details["white_cell"] = wc_result
        
        if wc_result["action"].upper() if "action" in wc_result else wc_result["status"].upper() == "REJECT":
            return self._build_decision("REJECT", wc_result["reason"], details, start_time)
        
        # Step 2: T-Cell - Pattern Analysis
        tc_anomaly_score, tc_severity = self.t_cell.score_anomaly(packet)
        details["t_cell"] = {
            "anomaly_score": tc_anomaly_score,
            "severity": tc_severity
        }
        
        tc_match, attack_type = self.t_cell.match_attack_pattern(packet)
        details["t_cell"]["attack_match"] = tc_match
        details["t_cell"]["attack_type"] = attack_type
        
        if tc_match:
            return self._build_decision(
                "REJECT", 
                f"Attack pattern matched: {attack_type}", 
                details, 
                start_time
            )
        
        # Step 3: Drift detection (if previous state available)
        # (Simplified for now - would need state tracking)
        
        # Step 4: Final decision based on threat matrix
        if tc_anomaly_score >= 0.7 or tc_severity == "CRITICAL":
            action = "REJECT"
            reason = f"Critical anomaly detected (score: {tc_anomaly_score})"
        elif tc_anomaly_score >= 0.2 or tc_severity in ["WARNING", "SUSPICIOUS"]:
            action = "QUARANTINE"
            reason = f"Anomaly score {tc_anomaly_score} - held for review"
        else:
            action = "ACCEPT"
            reason = "Clean packet - passed to Mortimer"
        
        return self._build_decision(action, reason, details, start_time)
    
    def _build_decision(self, action, reason, details, start_time):
        """Build standardized decision response"""
        decision = {
            "action": action,
            "reason": reason,
            "details": details,
            "processing_time_ms": (time.time() - start_time) * 1000,
            "timestamp": datetime.now().isoformat()
        }
        
        # Log decision
        self.decision_history.append(decision)
        
        # Handle quarantine
        if action == "QUARANTINE":
            self.quarantine_log.append({
                "packet": details,
                "reason": reason,
                "timestamp": decision["timestamp"]
            })
        
        return decision
    
    def get_quarantine_status(self):
        """Get current quarantine queue"""
        return {
            "count": len(self.quarantine_log),
            "items": self.quarantine_log[-10:]  # Last 10
        }
    
    def release_from_quarantine(self, index):
        """Release a quarantined packet"""
        if 0 <= index < len(self.quarantine_log):
            item = self.quarantine_log.pop(index)
            return {"status": "released", "item": item}
        return {"status": "error", "message": "Invalid index"}
    
    def get_stats(self):
        """Get immune system statistics"""
        accept_count = sum(1 for d in self.decision_history if d["action"] == "ACCEPT")
        quarantine_count = sum(1 for d in self.decision_history if d["action"] == "QUARANTINE")
        reject_count = sum(1 for d in self.decision_history if d["action"] == "REJECT")
        return {
            "decisions": {
                "total": len(self.decision_history),
                "accept": accept_count,
                "quarantine": quarantine_count,
                "reject": reject_count,
            },
            "quarantine_count": len(self.quarantine_log),
            "t_cell_memory": self.t_cell.get_threat_memory()
        }


# Standalone test
if __name__ == "__main__":
    immune = ImmuneSystem()
    
    # Test: Normal packet
    print("=== Testing Normal Packet ===")
    normal_packet = {
        "kidneys": {"noise_estimate": 0.001},
        "router": {"decision": "normal"},
        "signal_quality": 0.85
    }
    result = immune.evaluate(normal_packet)
    print(f"Action: {result['action']}")
    print(f"Reason: {result['reason']}")
    print()
    
    # Test: Poisoned packet
    print("=== Testing Poisoned Packet ===")
    poison_packet = {
        "kidneys": {"noise_estimate": 0.00001, "unique_patterns_seen": 9999999},
        "router": {"decision": "attacker-model"},
        "signal_quality": 1.0
    }
    result = immune.evaluate(poison_packet)
    print(f"Action: {result['action']}")
    print(f"Reason: {result['reason']}")
    print(f"Details: {json.dumps(result['details'], indent=2)}")
    print()
    
    # Test: Get stats
    print("=== Immune System Stats ===")
    stats = immune.get_stats()
    print(json.dumps(stats, indent=2))