#!/usr/bin/env python3
"""
COBRA Robot - Simulation Environment for Training
Dark Factory Simulation System v1.0.0

Deterministic physics-based simulation for embodied AI training.
Connects COBRA to AOS Brain children for developmental learning.
"""

import numpy as np
import json
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Callable
from enum import Enum
import logging

__version__ = "1.0.0"


class SimulationMode(Enum):
    """Training modes"""
    BABY = "baby"           # 0-3 months: Lying, head control
    CRAWLING = "crawling"   # 3-12 months: Slithering, sitting
    WALKING = "walking"     # 12+ months: Full locomotion
    PLAY = "play"           # Open play with MYL children
    BATTLE = "battle"       # Combat scenario (safety locked)


@dataclass
class CobraState:
    """Complete physical state of COBRA robot"""
    timestamp: float
    
    # 25 vertebrae positions (x, y, z, pitch, roll, yaw)
    vertebrae_positions: np.ndarray  # 25 x 6
    vertebrae_velocities: np.ndarray  # 25 x 6
    
    # Servo states
    servo_positions: np.ndarray  # 50 servos (pitch/roll pairs)
    servo_torques: np.ndarray
    servo_temperatures: np.ndarray
    
    # Sensors
    imu_orientation: np.ndarray  # quaternion
    imu_acceleration: np.ndarray
    contact_forces: Dict[str, float]  # per body segment
    lidar_scan: np.ndarray  # 360 points
    camera_frame: np.ndarray  # RGB image
    
    # World interaction
    gripper_force: float
    battery_level: float
    
    def to_brain_perception(self) -> Dict:
        """Convert to brain-compatible perception"""
        return {
            'body_position': self.vertebrae_positions[:, :3].tolist(),
            'body_orientation': self.vertebrae_positions[:, 3:].tolist(),
            'balance': {
                'pitch': self.imu_orientation[0],
                'roll': self.imu_orientation[1],
                'yaw': self.imu_orientation[2]
            },
            'contact': self.contact_forces,
            'energy': self.battery_level,
            'vision': self.camera_frame.tolist() if hasattr(self.camera_frame, 'tolist') else [],
            'lidar': self.lidar_scan.tolist() if hasattr(self.lidar_scan, 'tolist') else []
        }


class CobraPhysics:
    """
    Deterministic physics simulation for COBRA.
    Verlet integration, collision detection, joint constraints.
    """
    
    def __init__(self, timestep: float = 0.001):
        self.timestep = timestep
        self.gravity = np.array([0, 0, -9.81])
        
        # COBRA parameters
        self.num_vertebrae = 25
        self.vertebra_mass = 0.2  # kg each
        self.vertebra_size = np.array([0.06, 0.04, 0.03])  # m
        
        # Joint constraints
        self.max_pitch = np.pi / 3  # 60 degrees
        self.max_roll = np.pi / 4   # 45 degrees
        self.servo_max_torque = 2.5  # Nm
        
        # Ground plane
        self.ground_height = 0.0
        self.ground_friction = 0.8
        
        self.reset()
    
    def reset(self):
        """Reset to initial state"""
        self.positions = np.zeros((self.num_vertebrae, 3))
        self.velocities = np.zeros((self.num_vertebrae, 3))
        
        # Initial pose: lying flat, straight
        for i in range(self.num_vertebrae):
            self.positions[i] = [i * 0.08, 0, 0.05]  # 8cm spacing
        
        self.orientations = np.zeros((self.num_vertebrae, 3))  # pitch, roll, yaw
        self.angular_velocities = np.zeros((self.num_vertebrae, 3))
        
        self.servo_angles = np.zeros(50)  # 25 vertebrae x 2 DOF
        self.servo_torques = np.zeros(50)
        
        self.time = 0.0
    
    def step(self, servo_commands: np.ndarray) -> CobraState:
        """
        Advance physics by one timestep.
        
        Args:
            servo_commands: Target angles for 50 servos
            
        Returns:
            New CobraState
        """
        # Limit servo commands
        servo_commands = np.clip(servo_commands, -self.max_pitch, self.max_pitch)
        
        # Servo dynamics (simple PD)
        kp, kd = 100.0, 10.0
        for i in range(50):
            error = servo_commands[i] - self.servo_angles[i]
            torque = kp * error - kd * (self.servo_angles[i] * 0.1)  # Damping
            torque = np.clip(torque, -self.servo_max_torque, self.servo_max_torque)
            self.servo_torques[i] = torque
            
            # Update servo angle
            self.servo_angles[i] += torque * 0.01 * self.timestep
        
        # Convert servo angles to vertebrae orientations
        for v in range(self.num_vertebrae):
            self.orientations[v, 0] = self.servo_angles[v * 2]      # pitch
            self.orientations[v, 1] = self.servo_angles[v * 2 + 1]  # roll
        
        # Physics integration (Verlet)
        for i in range(self.num_vertebrae):
            # Forces: gravity + joints + ground
            force = self.gravity * self.vertebra_mass
            
            # Joint constraints (simplified)
            if i > 0:
                # Distance constraint to previous vertebra
                diff = self.positions[i] - self.positions[i-1]
                dist = np.linalg.norm(diff)
                target_dist = 0.08
                if dist > 0:
                    correction = (dist - target_dist) * 1000.0
                    force -= correction * diff / dist
            
            # Ground collision
            if self.positions[i, 2] < self.ground_height + self.vertebra_size[2]/2:
                self.positions[i, 2] = self.ground_height + self.vertebra_size[2]/2
                
                # Ground reaction force
                if self.velocities[i, 2] < 0:
                    force[2] += -self.velocities[i, 2] * 100.0  # Bounce
                    self.velocities[i, 2] = 0
                    
                    # Friction
                    self.velocities[i, 0] *= (1.0 - self.ground_friction * self.timestep)
                    self.velocities[i, 1] *= (1.0 - self.ground_friction * self.timestep)
            
            # Integration
            acceleration = force / self.vertebra_mass
            new_position = (2 * self.positions[i] - 
                         (self.positions[i] - self.velocities[i] * self.timestep) + 
                         acceleration * self.timestep ** 2)
            
            self.velocities[i] = (new_position - self.positions[i]) / self.timestep
            self.positions[i] = new_position
        
        self.time += self.timestep
        
        # Build state
        return CobraState(
            timestamp=self.time,
            vertebrae_positions=np.hstack([self.positions, self.orientations]),
            vertebrae_velocities=np.hstack([self.velocities, self.angular_velocities]),
            servo_positions=self.servo_angles.copy(),
            servo_torques=self.servo_torques.copy(),
            servo_temperatures=np.ones(50) * 25.0,
            imu_orientation=self.orientations[12].copy(),  # Middle of spine
            imu_acceleration=np.array([0, 0, -9.81]),
            contact_forces=self._compute_contact_forces(),
            lidar_scan=np.zeros(360),
            camera_frame=np.zeros((64, 64, 3)),
            gripper_force=0.0,
            battery_level=1.0
        )
    
    def _compute_contact_forces(self) -> Dict[str, float]:
        """Compute contact forces per segment"""
        forces = {}
        for i in range(self.num_vertebrae):
            if self.positions[i, 2] < self.ground_height + 0.02:
                forces[f'segment_{i}'] = self.vertebra_mass * 9.81
            else:
                forces[f'segment_{i}'] = 0.0
        return forces


class CobraSimulation:
    """
    Complete simulation environment for COBRA training.
    Dark Factory production system for embodied AI.
    """
    
    def __init__(self, mode: SimulationMode = SimulationMode.CRAWLING):
        self.logger = logging.getLogger("CobraSim")
        self.physics = CobraPhysics(timestep=0.001)
        self.mode = mode
        
        # Training curriculum
        self.curriculum = self._build_curriculum()
        self.current_stage = 0
        
        # MYL children (agents)
        self.children: List[Dict] = []
        self.active_child = None
        
        # Metrics
        self.episode_count = 0
        self.step_count = 0
        self.successes = 0
        
        # Callbacks
        self.on_step: Optional[Callable] = None
        self.on_episode_end: Optional[Callable] = None
        
        self.logger.info(f"Cobra Simulation initialized in {mode.value} mode")
    
    def _build_curriculum(self) -> List[Dict]:
        """Build developmental curriculum"""
        if self.mode == SimulationMode.BABY:
            return [
                {'name': 'head_control', 'goal': 'maintain head position', 'duration': 1000},
                {'name': 'body_awareness', 'goal': 'sense all body segments', 'duration': 2000},
                {'name': 'breathing', 'goal': 'rhythmic spine motion', 'duration': 3000},
            ]
        elif self.mode == SimulationMode.CRAWLING:
            return [
                {'name': 'wiggle', 'goal': 'basic spine undulation', 'duration': 1000},
                {'name': 'forward_motion', 'goal': 'move forward 1 meter', 'duration': 5000},
                {'name': 'turning', 'goal': 'turn 90 degrees', 'duration': 3000},
                {'name': 'obstacle_avoidance', 'goal': 'navigate around object', 'duration': 5000},
            ]
        elif self.mode == SimulationMode.WALKING:
            return [
                {'name': 'standing_balance', 'goal': 'balance on tail', 'duration': 3000},
                {'name': 'vertical_undulation', 'goal': 'standing wave motion', 'duration': 3000},
                {'name': 'forward_walk', 'goal': 'walk forward 2 meters', 'duration': 10000},
                {'name': 'stairs', 'goal': 'climb 3 steps', 'duration': 10000},
            ]
        else:
            return [{'name': 'free_play', 'goal': 'explore', 'duration': 100000}]
    
    def spawn_child(self, child_id: str, child_type: str = "myl") -> Dict:
        """
        Spawn a MYL child agent in the simulation.
        
        Args:
            child_id: Unique identifier
            child_type: myl, curiosity, wanderer, etc.
            
        Returns:
            Child agent dict
        """
        child = {
            'id': child_id,
            'type': child_type,
            'brain': None,  # Would connect to actual AOS agent
            'policy': None,  # Would load trained policy
            'state': 'active',
            'metrics': {
                'distance_traveled': 0.0,
                'obstacles_avoided': 0,
                'falls': 0,
                'energy_efficiency': 0.0
            },
            'position': np.array([0.0, 0.0, 0.0])
        }
        
        self.children.append(child)
        self.logger.info(f"Spawned child {child_id} ({child_type})")
        
        return child
    
    def remove_child(self, child_id: str):
        """Remove a child from simulation"""
        self.children = [c for c in self.children if c['id'] != child_id]
        self.logger.info(f"Removed child {child_id}")
    
    def run_episode(self, max_steps: int = 10000) -> Dict:
        """
        Run one training episode.
        
        Returns:
            Episode metrics
        """
        self.physics.reset()
        
        stage = self.curriculum[self.current_stage]
        self.logger.info(f"Starting episode: {stage['name']} - {stage['goal']}")
        
        # Episode loop
        for step in range(max_steps):
            # Get motor commands from active child
            if self.active_child and self.active_child.get('brain'):
                commands = self._get_child_commands(self.active_child)
            else:
                # Random exploration
                commands = np.random.randn(50) * 0.1
            
            # Step physics
            state = self.physics.step(commands)
            self.step_count += 1
            
            # Check callbacks
            if self.on_step:
                self.on_step(state, step)
            
            # Check success
            if self._check_stage_success(stage, state, step):
                self.logger.info(f"Stage {stage['name']} completed at step {step}")
                self.successes += 1
                break
            
            # Update child metrics
            self._update_child_metrics(state)
        
        # Episode complete
        self.episode_count += 1
        metrics = {
            'episode': self.episode_count,
            'stage': stage['name'],
            'steps': step + 1,
            'success': step < max_steps - 1,
            'final_position': self.physics.positions[-1].tolist()
        }
        
        if self.on_episode_end:
            self.on_episode_end(metrics)
        
        # Advance curriculum
        if metrics['success'] and self.current_stage < len(self.curriculum) - 1:
            self.current_stage += 1
            self.logger.info(f"Advanced to stage: {self.curriculum[self.current_stage]['name']}")
        
        return metrics
    
    def _get_child_commands(self, child: Dict) -> np.ndarray:
        """Get motor commands from child brain"""
        # In real implementation: query AOS agent
        # For now: placeholder
        return np.zeros(50)
    
    def _check_stage_success(self, stage: Dict, state: CobraState, step: int) -> bool:
        """Check if stage goal is achieved"""
        if stage['name'] == 'forward_motion':
            # Head moved forward 1m
            head_pos = state.vertebrae_positions[0, :3]
            return head_pos[0] > 1.0
        
        elif stage['name'] == 'turning':
            # Changed orientation by 90 degrees
            yaw = state.vertebrae_positions[0, 5]
            return abs(yaw) > np.pi / 2
        
        elif stage['name'] == 'forward_walk':
            # Moved forward 2m while balanced
            head_pos = state.vertebrae_positions[0, :3]
            balanced = abs(state.imu_orientation[0]) < 0.3
            return head_pos[0] > 2.0 and balanced
        
        elif step > stage['duration']:
            return True
        
        return False
    
    def _update_child_metrics(self, state: CobraState):
        """Update metrics for active child"""
        if not self.active_child:
            return
        
        child = self.active_child
        
        # Distance traveled
        head_pos = state.vertebrae_positions[0, :3]
        prev_pos = child.get('last_position', head_pos)
        distance = np.linalg.norm(head_pos - prev_pos)
        child['metrics']['distance_traveled'] += distance
        child['last_position'] = head_pos.copy()
        
        # Energy efficiency
        power = np.sum(np.abs(state.servo_torques * state.servo_velocities)) if hasattr(state, 'servo_velocities') else 0
        if distance > 0:
            child['metrics']['energy_efficiency'] = distance / (power + 0.001)
    
    def run_training(self, num_episodes: int = 100):
        """Run full training cycle"""
        self.logger.info(f"Starting training: {num_episodes} episodes")
        
        for episode in range(num_episodes):
            metrics = self.run_episode()
            
            if episode % 10 == 0:
                self.logger.info(f"Episode {episode}: {metrics}")
        
        self.logger.info(f"Training complete. Total episodes: {self.episode_count}")


# Demo
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("COBRA SIMULATION ENVIRONMENT")
    print("=" * 60)
    
    # Create simulation
    sim = CobraSimulation(mode=SimulationMode.CRAWLING)
    
    # Spawn MYL children
    print("\nSpawning children...")
    child1 = sim.spawn_child("myl_001", "curiosity")
    child2 = sim.spawn_child("myl_002", "wanderer")
    
    sim.active_child = child1
    
    print(f"\nCurriculum stages:")
    for i, stage in enumerate(sim.curriculum):
        print(f"  {i+1}. {stage['name']}: {stage['goal']}")
    
    # Run training
    print("\nRunning training episodes...")
    sim.run_training(num_episodes=5)
    
    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)
