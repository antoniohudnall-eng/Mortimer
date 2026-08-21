#!/usr/bin/env python3
"""
Tick Recovery Skill - Emergency brain reset.
"""

def tick_recovery_handler(input_data: dict) -> dict:
    """Recover from stalled state."""
    health_report = input_data.get('health_report', {})
    aggressive = input_data.get('aggressive', False)
    
    actions = []
    regions_reset = []
    
    # Check metrics
    metrics = health_report.get('metrics', {})
    
    # Reset if high latency
    if metrics.get('tick_latency_ms', 0) > 500:
        actions.append("Reset tick loop")
        regions_reset.append('tick_coordinator')
    
    # Reset if Ollama issues
    if metrics.get('ollama_status') != 'connected':
        actions.append("Clear Ollama queue")
        regions_reset.append('pfc')
    
    # Aggressive reset
    if aggressive:
        actions.append("Full region reset")
        regions_reset.extend(['thalamus', 'hippocampus', 'pfc', 'limbic'])
    
    return {
        "status": "recovered" if actions else "no_action_needed",
        "actions_taken": actions,
        "regions_reset": regions_reset
    }
