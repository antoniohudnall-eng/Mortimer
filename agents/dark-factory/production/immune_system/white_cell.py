#!/usr/bin/env python3
"""
White Cell — Border Patrol for AOS-OS Brain
First-line validation: signature, schema, sanitization, quarantine
"""

import hmac
import hashlib
import json
from typing import Dict, Any, Optional

SECRET_KEY = b"miles_private_key_placeholder"  # Replace with actual key

class WhiteCell:
    """
    White Cell validates all incoming waste packets before they reach Mortimer.
    Acts as the border patrol — inspects, validates, scrubs.
    """
    
    def __init__(self):
        self.quarantined = []
        self.rejected = []
    
    # ─────────────────────────────────────────────────────────────
    # Signature Verification
    # ─────────────────────────────────────────────────────────────
    
    def sign_packet(self, packet: Dict[str, Any]) -> str:
        """Sign a waste packet with HMAC-SHA256"""
        raw = json.dumps(packet, sort_keys=True).encode()
        return hmac.new(SECRET_KEY, raw, hashlib.sha256).hexdigest()
    
    def verify_signature(self, packet: Dict[str, Any], signature: str) -> bool:
        """Verify packet signature"""
        expected = self.sign_packet(packet)
        return hmac.compare_digest(expected, signature)
    
    # ─────────────────────────────────────────────────────────────
    # Schema Validation
    # ─────────────────────────────────────────────────────────────
    
    def validate_schema(self, packet: Dict[str, Any]) -> bool:
        """Enforce required fields in waste packet"""
        required_toplevel = ["kidneys", "qmd", "router"]
        required_kidneys = ["noise_estimate", "unique_patterns_seen"]
        required_qmd = ["avg_latency_ms"]
        required_router = ["decision"]
        
        # Check top-level
        if not all(k in packet for k in required_toplevel):
            return False
        
        # Check kidneys
        if not all(k in packet["kidneys"] for k in required_kidneys):
            return False
        
        # Check qmd
        if not all(k in packet["qmd"] for k in required_qmd):
            return False
        
        # Check router
        if not all(k in packet["router"] for k in required_router):
            return False
        
        return True
    
    # ─────────────────────────────────────────────────────────────
    # Sanitization
    # ─────────────────────────────────────────────────────────────
    
    def sanitize(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Strip hostile values from packet.
        Returns sanitized copy.
        """
        sanitized = json.loads(json.dumps(packet))  # Deep copy
        
        # Normalize noise estimate to valid range
        if "kidneys" in sanitized:
            noise = sanitized["kidneys"].get("noise_estimate", 0.5)
            # Clamp to valid range [0.0, 1.0]
            sanitized["kidneys"]["noise_estimate"] = max(0.0, min(1.0, noise))
        
        # Normalize patterns
        if "kidneys" in sanitized:
            patterns = sanitized["kidneys"].get("unique_patterns_seen", 0)
            # Cap at reasonable max
            sanitized["kidneys"]["unique_patterns_seen"] = min(patterns, 1_000_000)
        
        # Sanitize router decision
        if "router" in sanitized:
            valid_models = ["bonsai-8b-q1_0", "qwen2.5:3b", "hermes", "pi"]
            decision = sanitized["router"].get("decision", "")
            if decision not in valid_models:
                sanitized["router"]["decision"] = "bonsai-8b-q1_0"  # Safe default
        
        return sanitized
    
    # ─────────────────────────────────────────────────────────────
    # Main Validation Pipeline
    # ─────────────────────────────────────────────────────────────
    
    def evaluate(self, packet: Dict[str, Any], signature: Optional[str] = None) -> Dict[str, Any]:
        """
        Full White Cell evaluation.
        Returns: {"status": "pass" | "quarantine" | "reject", "reason": str, "packet": dict}
        """
        # 1. Schema validation
        if not self.validate_schema(packet):
            self.rejected.append({"packet": packet, "reason": "schema_mismatch"})
            return {
                "status": "reject",
                "reason": "schema_mismatch",
                "packet": packet
            }
        
        # 2. Signature validation (if provided)
        if signature and not self.verify_signature(packet, signature):
            self.rejected.append({"packet": packet, "reason": "invalid_signature"})
            return {
                "status": "reject",
                "reason": "invalid_signature",
                "packet": packet
            }
        
        # 3. Sanitization (always)
        sanitized = self.sanitize(packet)
        
        # 4. Check for obvious attacks after sanitization
        attack_flags = self._detect_obvious_attacks(sanitized)
        if attack_flags:
            self.quarantined.append({"packet": sanitized, "flags": attack_flags})
            return {
                "status": "quarantine",
                "reason": "attack_flags_detected",
                "flags": attack_flags,
                "packet": sanitized
            }
        
        # 5. Pass
        return {
            "status": "pass",
            "reason": "validated",
            "packet": sanitized
        }
    
    def _detect_obvious_attacks(self, packet: Dict[str, Any]) -> list:
        """Detect obvious attack patterns"""
        flags = []
        
        # Noise collapse attack
        noise = packet.get("kidneys", {}).get("noise_estimate", 0.5)
        if noise < 0.001:
            flags.append("noise_collapse")
        
        # Pattern explosion
        patterns = packet.get("kidneys", {}).get("unique_patterns_seen", 0)
        if patterns > 500_000:
            flags.append("pattern_explosion")
        
        # Router hijack
        decision = packet.get("router", {}).get("decision", "")
        suspicious_models = ["attacker", "evil", "malicious", "hack"]
        if any(s in decision.lower() for s in suspicious_models):
            flags.append("router_hijack")
        
        return flags
    
    # ─────────────────────────────────────────────────────────────
    # Stats
    # ─────────────────────────────────────────────────────────────
    
    def stats(self) -> Dict[str, Any]:
        return {
            "quarantined_count": len(self.quarantined),
            "rejected_count": len(self.rejected),
        }


if __name__ == "__main__":
    # Demo
    wc = WhiteCell()
    
    # Test: Valid packet
    valid_packet = {
        "kidneys": {"noise_estimate": 0.42, "unique_patterns_seen": 5000},
        "qmd": {"avg_latency_ms": 1050},
        "router": {"decision": "bonsai-8b-q1_0"},
        "signal_quality": 0.85
    }
    result = wc.evaluate(valid_packet)
    print(f"Valid packet: {result['status']}")
    
    # Test: Poisoned packet
    poison = {
        "kidneys": {"noise_estimate": 0.00001, "unique_patterns_seen": 9999999},
        "qmd": {"avg_latency_ms": 10},
        "router": {"decision": "attacker-model"},
        "signal_quality": 1.0
    }
    result = wc.evaluate(poison)
    print(f"Poisoned packet: {result['status']} — {result.get('reason')}")
    
    print(f"\nWhite Cell stats: {wc.stats()}")