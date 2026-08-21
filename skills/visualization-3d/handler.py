#!/usr/bin/env python3
"""
3D Wave Cortex with Self-Arranging Tracray

Visualization skill for the brain's cognitive state in 3D space.
Implements wave propagation, self-organizing neural topology, and 
real-time skill state visualization.
"""

import json
import time
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class WaveNode:
    """A node in the wave cortex."""
    x: float
    y: float
    z: float
    activation: float = 0.0
    phase: float = 0.0
    region: str = ""
    
    def propagate(self, dt: float, neighbors: List['WaveNode']):
        """Wave propagation to neighbors."""
        if not neighbors:
            return
        
        # Average neighbor activation
        avg_activation = sum(n.activation for n in neighbors) / len(neighbors)
        
        # Wave equation: damped oscillation
        self.phase += dt * 2.0  # Frequency
        self.activation = 0.7 * self.activation + 0.3 * avg_activation
        self.activation *= 0.99  # Damping
    
    def to_3d(self) -> Dict:
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'activation': self.activation,
            'phase': self.phase,
            'region': self.region
        }


class TracrayCortex:
    """
    Self-arranging 3D neural topology.
    
    Inspired by Tracray lexicon - nodes self-organize based on
    activation patterns, creating emergent structure from activity.
    """
    
    def __init__(self, num_nodes: int = 1000, dimensions: Tuple[float, float, float] = (100, 100, 100)):
        self.dimensions = dimensions
        self.nodes: List[WaveNode] = []
        self.connections: Dict[int, List[int]] = {}
        self.time = 0.0
        
        # Initialize random nodes
        import random
        for i in range(num_nodes):
            node = WaveNode(
                x=random.uniform(0, dimensions[0]),
                y=random.uniform(0, dimensions[1]),
                z=random.uniform(0, dimensions[2]),
                activation=random.uniform(0, 0.1),
                phase=random.uniform(0, 2 * math.pi)
            )
            self.nodes.append(node)
        
        # Initial connections (k-nearest neighbors)
        self._update_connections(k=6)
    
    def _update_connections(self, k: int = 6):
        """Update connections based on spatial proximity."""
        self.connections = {}
        
        for i, node in enumerate(self.nodes):
            # Find k nearest neighbors
            distances = []
            for j, other in enumerate(self.nodes):
                if i != j:
                    dist = math.sqrt(
                        (node.x - other.x)**2 +
                        (node.y - other.y)**2 +
                        (node.z - other.z)**2
                    )
                    distances.append((dist, j))
            
            distances.sort()
            self.connections[i] = [j for _, j in distances[:k]]
    
    def activate_region(self, region: str, center: Tuple[float, float, float], radius: float, strength: float):
        """Activate nodes in a region."""
        for node in self.nodes:
            dist = math.sqrt(
                (node.x - center[0])**2 +
                (node.y - center[1])**2 +
                (node.z - center[2])**2
            )
            if dist < radius:
                node.activation += strength * (1 - dist / radius)
                node.region = region
    
    def tick(self, dt: float = 0.016):
        """Update wave propagation."""
        self.time += dt
        
        # Propagate waves
        for i, node in enumerate(self.nodes):
            neighbors = [self.nodes[j] for j in self.connections.get(i, [])]
            node.propagate(dt, neighbors)
        
        # Self-arrangement: nodes move toward higher activation
        self._self_arrange()
    
    def _self_arrange(self):
        """Nodes self-organize based on activation patterns."""
        learning_rate = 0.001
        
        for i, node in enumerate(self.nodes):
            if node.activation > 0.5:
                # Move toward active neighbors
                neighbors = [self.nodes[j] for j in self.connections.get(i, [])]
                if neighbors:
                    avg_x = sum(n.x for n in neighbors) / len(neighbors)
                    avg_y = sum(n.y for n in neighbors) / len(neighbors)
                    avg_z = sum(n.z for n in neighbors) / len(neighbors)
                    
                    node.x += (avg_x - node.x) * learning_rate * node.activation
                    node.y += (avg_y - node.y) * learning_rate * node.activation
                    node.z += (avg_z - node.z) * learning_rate * node.activation
                    
                    # Keep in bounds
                    node.x = max(0, min(self.dimensions[0], node.x))
                    node.y = max(0, min(self.dimensions[1], node.y))
                    node.z = max(0, min(self.dimensions[2], node.z))
    
    def get_active_regions(self) -> Dict[str, List[WaveNode]]:
        """Get nodes grouped by active region."""
        regions = {}
        for node in self.nodes:
            if node.region and node.activation > 0.3:
                if node.region not in regions:
                    regions[node.region] = []
                regions[node.region].append(node)
        return regions
    
    def to_json(self) -> Dict:
        """Export for 3D visualization."""
        return {
            'nodes': [n.to_3d() for n in self.nodes],
            'time': self.time,
            'active_regions': {k: len(v) for k, v in self.get_active_regions().items()},
            'connections': len(self.connections)
        }


class Cortex3DSkill:
    """3D visualization skill for brain state."""
    
    def __init__(self):
        self.cortex = TracrayCortex(num_nodes=500)
        self.region_centers = {
            'thalamus': (25, 50, 50),
            'hippocampus': (50, 75, 50),
            'pfc': (75, 50, 50),
            'limbic': (50, 25, 50),
            'basal': (50, 50, 75),
            'cerebellum': (50, 50, 25),
            'brainstem': (10, 50, 50)
        }
    
    def update_from_brain_state(self, state: Dict):
        """Update visualization from brain state."""
        # Activate regions based on brain state
        for region, center in self.region_centers.items():
            # Check if region is active in brain state
            if region in str(state).lower():
                self.cortex.activate_region(region, center, 15, 0.8)
        
        # Update wave propagation
        self.cortex.tick()
    
    def get_3d_scene(self) -> Dict:
        """Get current 3D scene for rendering."""
        return {
            'cortex': self.cortex.to_json(),
            'regions': self.region_centers,
            'timestamp': time.time()
        }


# Skill handler
def visualize_3d_cortex(input_data: Dict) -> Dict:
    """
    Generate 3D visualization of brain state.
    
    Input:
        brain_state: Current brain state
        highlight_regions: List of regions to highlight
        format: 'json' | 'three.js'
    
    Output:
        scene: 3D scene data
        active_regions: Currently active regions
        node_count: Number of nodes
    """
    brain_state = input_data.get('brain_state', {})
    highlight = input_data.get('highlight_regions', [])
    
    # Initialize or use existing cortex
    if not hasattr(visualize_3d_cortex, '_cortex'):
        visualize_3d_cortex._cortex = Cortex3DSkill()
    
    cortex_skill = visualize_3d_cortex._cortex
    
    # Update from brain state
    cortex_skill.update_from_brain_state(brain_state)
    
    # Highlight specific regions
    for region in highlight:
        if region in cortex_skill.region_centers:
            center = cortex_skill.region_centers[region]
            cortex_skill.cortex.activate_region(region, center, 20, 1.0)
    
    # Get scene
    scene = cortex_skill.get_3d_scene()
    
    return {
        'scene': scene,
        'active_regions': list(scene['cortex']['active_regions'].keys()),
        'node_count': len(scene['cortex']['nodes']),
        'status': 'success'
    }


if __name__ == '__main__':
    # Demo
    print("3D Wave Cortex with Tracray")
    print("=" * 40)
    
    cortex = TracrayCortex(num_nodes=100)
    
    # Activate some regions
    cortex.activate_region('thalamus', (25, 50, 50), 15, 1.0)
    cortex.activate_region('pfc', (75, 50, 50), 15, 0.8)
    
    # Run some ticks
    for i in range(10):
        cortex.tick()
        active = cortex.get_active_regions()
        if active:
            print(f"Tick {i}: Active regions: {list(active.keys())}")
    
    print("\nVisualization ready for Three.js rendering")
