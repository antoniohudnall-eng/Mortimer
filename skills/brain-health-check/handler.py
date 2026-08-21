#!/usr/bin/env python3
"""
Brain Health Check - Diagnostic skill implementation.
"""

import time
import requests
from typing import Dict, List

def brain_health_check(input_data: Dict) -> Dict:
    """Check brain health metrics."""
    detailed = input_data.get('detailed', False)
    
    metrics = {}
    recommendations = []
    
    # Check tick latency (simulated for now, will integrate with actual brain)
    metrics['tick_latency_ms'] = _check_tick_latency()
    if metrics['tick_latency_ms'] > 200:
        recommendations.append("High tick latency detected - consider optimizing OODA loop")
    
    # Check memory usage
    metrics['memory_usage'] = _check_memory_usage()
    if metrics['memory_usage'] > 0.8:
        recommendations.append("Memory pressure high - trigger memory consolidation")
    
    # Check Ollama connectivity
    metrics['ollama_status'] = _check_ollama()
    if metrics['ollama_status'] != 'connected':
        recommendations.append("Ollama connectivity issue - check service status")
    
    # Check skills registered
    metrics['skills_registered'] = _check_skill_registry()
    if metrics['skills_registered'] < 5:
        recommendations.append("Low skill count - verify registry initialization")
    
    # Determine overall status
    status = _determine_status(metrics, recommendations)
    
    return {
        "status": status,
        "metrics": metrics,
        "recommendations": recommendations,
        "timestamp": time.time()
    }

def _check_tick_latency() -> float:
    """Check tick latency."""
    # Placeholder - will integrate with actual brain state
    return 150.0  # ms

def _check_memory_usage() -> float:
    """Check memory usage (0-1 scale)."""
    # Placeholder
    return 0.6

def _check_ollama() -> str:
    """Check Ollama connectivity."""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        if response.status_code == 200:
            return 'connected'
        return 'error'
    except:
        return 'disconnected'

def _check_skill_registry() -> int:
    """Check number of registered skills."""
    # Placeholder - will integrate with actual registry
    return 0

def _determine_status(metrics: Dict, recommendations: List) -> str:
    """Determine overall health status."""
    if not recommendations:
        return 'healthy'
    if len(recommendations) > 2 or metrics.get('ollama_status') == 'disconnected':
        return 'critical'
    return 'warning'
