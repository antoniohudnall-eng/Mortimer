---
name: visualization-3d
version: "1.0.0"
tier: methodology
description: "3D wave cortex visualization with self-arranging Tracray topology. Agents can inspect brain state in 3D space, see wave propagation, and observe self-organization patterns."
contracts:
  input:
    type: object
    properties:
      brain_state:
        type: object
      highlight_regions:
        type: array
        items: {type: string}
      format:
        type: string
        enum: [json, three.js]
        default: json
  output:
    type: object
    required: [scene, active_regions, node_count]
    properties:
      scene:
        type: object
        description: "3D scene data for rendering"
      active_regions:
        type: array
      node_count:
        type: integer
---

# Visualization-3D Skill

Real-time 3D visualization of the brain's cognitive state using wave propagation and self-organizing Tracray topology.

## Tracray Cortex

- **Wave Propagation**: Activation flows through network like neural waves
- **Self-Arrangement**: Nodes move toward active neighbors, creating emergent structure
- **Region Mapping**: Thalamus, PFC, Hippocampus, etc. mapped to 3D space

## Visualization Modes

- **Real-time**: Watch brain think in 3D
- **Region Highlight**: Focus on specific cognitive areas
- **Wave Propagation**: See activation spread through network

## Three.js Integration

Output compatible with Three.js for web-based visualization. Can render in browser, VR, or as applet.
