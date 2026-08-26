#!/usr/bin/env python3
"""
Thalamus Skill - Sensory normalization and routing.
"""

import time
from typing import Dict, List

def thalamus_handler(input_data: Dict) -> Dict:
    """Process sensory input."""
    source = input_data['source']
    data = input_data['data']
    priority = input_data.get('priority', 0.5)
    
    # Normalize data based on source
    normalized = _normalize(data, source)
    
    # Determine routing
    routing = _route(source, normalized)
    
    # Generate ternary signature
    signature = _generate_signature(normalized, priority)
    
    return {
        "normalized": normalized,
        "priority": priority,
        "routing": routing,
        "signature": signature
    }

def _normalize(data: any, source: str) -> Dict:
    """Normalize data based on source."""
    return {
        "content": data,
        "source": source,
        "processed": True,
        "type": _detect_type(data)
    }

def _route(source: str, normalized: Dict) -> List[str]:
    """Determine which regions should process this."""
    routes = {
        "sensor": ["hippocampus", "pfc"],
        "agent": ["pfc", "limbic"],
        "system": ["brainstem", "pfc"],
        "user": ["pfc", "limbic"]
    }
    return routes.get(source, ["pfc"])

def _generate_signature(normalized: Dict, priority: float) -> Dict:
    """Generate ternary signature [novelty, value, action, risk, growth]."""
    content = str(normalized.get("content", ""))
    
    return {
        "novelty": 1 if "?" in content else 0,
        "value": 1 if len(content) > 20 else 0,
        "action": 1 if priority > 0.5 else 0,
        "risk": -1 if "error" in content.lower() else 0,
        "growth": 1 if priority > 0.7 else 0
    }

def _detect_type(data: any) -> str:
    """Detect data type."""
    if isinstance(data, str):
        return "text"
    elif isinstance(data, dict):
        return "structured"
    elif isinstance(data, list):
        return "array"
    return "unknown"
