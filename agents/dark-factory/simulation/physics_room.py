#!/usr/bin/env python3
"""
MYL Children Physics Training Room
Interactive environment with tables, chairs, blocks, and balls for manipulation learning.

Features:
- Physics engine (Verlet integration)
- Interactive objects: blocks (different sizes), balls, table, chair
- Collision detection
- Object manipulation tasks
- Visual feedback
"""

import numpy as np
import json
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import time
import logging

__version__ = "1.0.0"


@dataclass
class PhysicsObject:
    """Physical object in the training room"""
    id: str
    obj_type: str  # 'block', 'ball', 'table', 'chair', 'wall'
    position: np.ndarray  # [x, y, z]
    velocity: np.ndarray
    size: np.ndarray      # dimensions
    mass: float
    color: str
    movable: bool
    gripped: bool = False
    
    def get_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get AABB bounds (min, max)"""
        half_size = self.size / 2
        return self.position - half_size, self.position + half_size


@dataclass
class RoomConfig:
    """Room configuration"""
    size: Tuple[float, float, float] = (10.0, 10.0, 3.0)  # meters
    gravity: np.ndarray = field(default_factory=lambda: np.array([0, 0, -9.81]))
    dt: float = 0.01  # timestep
    

class PhysicsRoom:
    """
    Physics-based training room for embodied agents.
    Objects: blocks (S/M/L), balls, table, chair
    """
    
    def __init__(self, config: Optional[RoomConfig] = None):
        self.config = config or RoomConfig()
        self.logger = logging.getLogger("PhysicsRoom")
        
        # Objects in room
        self.objects: Dict[str, PhysicsObject] = {}
        
        # Agent positions
        self.agent_positions: Dict[str, np.ndarray] = {}
        
        # Physics state
        self.time = 0.0
        self.collisions = []
        
        # Initialize room
        self._build_room()
        
        self.logger.info(f"Physics room initialized: {self.config.size}")
    
    def _build_room(self):
        """Build the training room with furniture and objects"""
        
        # Floor
        self.add_object(PhysicsObject(
            id="floor",
            obj_type="wall",
            position=np.array([5.0, 5.0, -0.5]),
            velocity=np.zeros(3),
            size=np.array([10.0, 10.0, 1.0]),
            mass=1000.0,
            color="gray",
            movable=False
        ))
        
        # Table (center of room)
        self.add_object(PhysicsObject(
            id="table",
            obj_type="table",
            position=np.array([5.0, 5.0, 0.75]),
            velocity=np.zeros(3),
            size=np.array([1.5, 1.0, 0.05]),  # tabletop
            mass=20.0,
            color="brown",
            movable=False
        ))
        
        # Table legs
        for i, leg_pos in enumerate([
            [4.3, 4.5], [5.7, 4.5], [4.3, 5.5], [5.7, 5.5]
        ]):
            self.add_object(PhysicsObject(
                id=f"table_leg_{i}",
                obj_type="wall",
                position=np.array([leg_pos[0], leg_pos[1], 0.375]),
                velocity=np.zeros(3),
                size=np.array([0.1, 0.1, 0.75]),
                mass=5.0,
                color="brown",
                movable=False
            ))
        
        # Chair (near table)
        self.add_object(PhysicsObject(
            id="chair",
            obj_type="chair",
            position=np.array([5.0, 3.5, 0.5]),
            velocity=np.zeros(3),
            size=np.array([0.6, 0.6, 1.0]),
            mass=10.0,
            color="blue",
            movable=True
        ))
        
        # Small blocks (stackable)
        for i in range(3):
            self.add_object(PhysicsObject(
                id=f"block_small_{i}",
                obj_type="block",
                position=np.array([3.0 + i*0.3, 2.0, 0.1]),
                velocity=np.zeros(3),
                size=np.array([0.2, 0.2, 0.2]),
                mass=0.5,
                color="red",
                movable=True
            ))
        
        # Medium blocks
        for i in range(2):
            self.add_object(PhysicsObject(
                id=f"block_medium_{i}",
                obj_type="block",
                position=np.array([6.0 + i*0.4, 2.0, 0.15]),
                velocity=np.zeros(3),
                size=np.array([0.3, 0.3, 0.3]),
                mass=1.0,
                color="green",
                movable=True
            ))
        
        # Large block
        self.add_object(PhysicsObject(
            id="block_large",
            obj_type="block",
            position=np.array([8.0, 2.0, 0.2]),
            velocity=np.zeros(3),
            size=np.array([0.4, 0.4, 0.4]),
            mass=2.0,
            color="blue",
            movable=True
        ))
        
        # Balls (will roll)
        for i in range(3):
            self.add_object(PhysicsObject(
                id=f"ball_{i}",
                obj_type="ball",
                position=np.array([2.0 + i*0.5, 7.0, 0.15]),
                velocity=np.zeros(3),
                size=np.array([0.3, 0.3, 0.3]),  # diameter
                mass=0.8,
                color=["yellow", "orange", "purple"][i],
                movable=True
            ))
    
    def add_object(self, obj: PhysicsObject):
        """Add object to room"""
        self.objects[obj.id] = obj
    
    def spawn_agent(self, agent_id: str, position: np.ndarray):
        """Spawn agent in room"""
        self.agent_positions[agent_id] = position.copy()
        self.logger.info(f"Agent {agent_id} spawned at {position}")
    
    def step(self, actions: Dict[str, Dict] = None):
        """
        Advance physics simulation one timestep.
        
        Args:
            actions: Dict of agent_id -> action (move, grip, etc.)
        """
        actions = actions or {}
        
        # Process agent actions
        for agent_id, action in actions.items():
            self._process_action(agent_id, action)
        
        # Update all objects
        for obj in self.objects.values():
            if obj.movable and not obj.gripped:
                self._update_object(obj)
        
        # Check collisions
        self._check_collisions()
        
        self.time += self.config.dt
    
    def _process_action(self, agent_id: str, action: Dict):
        """Process agent action"""
        action_type = action.get('type')
        
        if action_type == 'move':
            # Move agent
            if agent_id in self.agent_positions:
                delta = np.array(action.get('delta', [0, 0, 0]))
                self.agent_positions[agent_id] += delta
        
        elif action_type == 'grip':
            # Grip nearest object
            target_id = action.get('target_id')
            if target_id and target_id in self.objects:
                obj = self.objects[target_id]
                if obj.movable:
                    obj.gripped = True
                    obj.velocity = np.zeros(3)
        
        elif action_type == 'release':
            # Release gripped object
            target_id = action.get('target_id')
            if target_id and target_id in self.objects:
                self.objects[target_id].gripped = False
        
        elif action_type == 'push':
            # Push object
            target_id = action.get('target_id')
            force = np.array(action.get('force', [0, 0, 0]))
            if target_id and target_id in self.objects:
                obj = self.objects[target_id]
                if obj.movable:
                    obj.velocity += force / obj.mass * self.config.dt
    
    def _update_object(self, obj: PhysicsObject):
        """Update object physics"""
        # Apply gravity
        obj.velocity += self.config.gravity * self.config.dt
        
        # Update position
        obj.position += obj.velocity * self.config.dt
        
        # Floor collision
        if obj.position[2] < obj.size[2] / 2:
            obj.position[2] = obj.size[2] / 2
            if obj.velocity[2] < 0:
                obj.velocity[2] *= -0.3  # Bounce with damping
            obj.velocity[0:2] *= 0.9  # Friction
    
    def _check_collisions(self):
        """Check and resolve collisions"""
        self.collisions = []
        
        obj_list = list(self.objects.values())
        for i, obj_a in enumerate(obj_list):
            for obj_b in obj_list[i+1:]:
                if self._objects_collide(obj_a, obj_b):
                    self.collisions.append((obj_a.id, obj_b.id))
                    self._resolve_collision(obj_a, obj_b)
    
    def _objects_collide(self, a: PhysicsObject, b: PhysicsObject) -> bool:
        """Check if two objects collide (AABB)"""
        min_a, max_a = a.get_bounds()
        min_b, max_b = b.get_bounds()
        
        return (min_a[0] < max_b[0] and max_a[0] > min_b[0] and
                min_a[1] < max_b[1] and max_a[1] > min_b[1] and
                min_a[2] < max_b[2] and max_a[2] > min_b[2])
    
    def _resolve_collision(self, a: PhysicsObject, b: PhysicsObject):
        """Simple collision response"""
        if not (a.movable or b.movable):
            return
        
        # Push apart
        direction = a.position - b.position
        distance = np.linalg.norm(direction)
        if distance > 0:
            direction /= distance
            
            if a.movable:
                a.position += direction * 0.01
                a.velocity += direction * 0.1
            if b.movable:
                b.position -= direction * 0.01
                b.velocity -= direction * 0.1
    
    def get_state(self) -> Dict:
        """Get current room state"""
        return {
            'time': self.time,
            'objects': {
                obj_id: {
                    'type': obj.obj_type,
                    'position': obj.position.tolist(),
                    'velocity': obj.velocity.tolist(),
                    'size': obj.size.tolist(),
                    'color': obj.color,
                    'gripped': obj.gripped
                }
                for obj_id, obj in self.objects.items()
            },
            'agents': {
                agent_id: pos.tolist()
                for agent_id, pos in self.agent_positions.items()
            },
            'collisions': self.collisions
        }
    
    def task_stack_blocks(self, agent_id: str, num_blocks: int = 3) -> bool:
        """
        Task: Stack blocks vertically.
        Returns success.
        """
        # Check if blocks are stacked
        blocks = [obj for obj in self.objects.values() 
                 if obj.obj_type == 'block' and obj.movable]
        
        if len(blocks) < num_blocks:
            return False
        
        # Sort by height
        blocks_sorted = sorted(blocks, key=lambda b: b.position[2])
        
        # Check if stacked (same x, y, increasing z)
        for i in range(len(blocks_sorted) - 1):
            dx = abs(blocks_sorted[i].position[0] - blocks_sorted[i+1].position[0])
            dy = abs(blocks_sorted[i].position[1] - blocks_sorted[i+1].position[1])
            dz = blocks_sorted[i+1].position[2] - blocks_sorted[i].position[2]
            
            if dx > 0.1 or dy > 0.1 or dz < 0.1 or dz > 0.5:
                return False
        
        return True
    
    def task_push_ball_to_target(self, agent_id: str, ball_id: str, 
                                  target: np.ndarray, tolerance: float = 0.5) -> bool:
        """
        Task: Push ball to target location.
        Returns success.
        """
        if ball_id not in self.objects:
            return False
        
        ball = self.objects[ball_id]
        distance = np.linalg.norm(ball.position - target)
        
        return distance < tolerance
    
    def task_move_object_to_table(self, agent_id: str, obj_id: str) -> bool:
        """
        Task: Move object onto table.
        Returns success.
        """
        if obj_id not in self.objects:
            return False
        
        obj = self.objects[obj_id]
        table = self.objects.get('table')
        
        if table is None:
            return False
        
        # Check if on table
        dx = abs(obj.position[0] - table.position[0])
        dy = abs(obj.position[1] - table.position[1])
        dz = obj.position[2] - table.position[2]
        
        table_bounds_x = table.size[0] / 2 + obj.size[0] / 2
        table_bounds_y = table.size[1] / 2 + obj.size[1] / 2
        
        return (dx < table_bounds_x and 
                dy < table_bounds_y and 
                0.04 < dz < 0.15)  # On top of table
    
    def print_room_layout(self):
        """Print ASCII room layout"""
        print("\n" + "=" * 60)
        print("PHYSICS ROOM LAYOUT")
        print("=" * 60)
        print(f"Room size: {self.config.size}")
        print("\nObjects:")
        
        for obj_id, obj in self.objects.items():
            print(f"  {obj_id:20s} | {obj.obj_type:10s} | "
                  f"pos={obj.position.round(2)} | "
                  f"movable={obj.movable}")
        
        if self.agent_positions:
            print("\nAgents:")
            for agent_id, pos in self.agent_positions.items():
                print(f"  {agent_id}: {pos.round(2)}")
        
        print("=" * 60)


# Training scenarios
class TrainingScenarios:
    """Pre-defined training scenarios for MYL children"""
    
    @staticmethod
    def scenario_stack_blocks(room: PhysicsRoom, agent_id: str):
        """Train stacking blocks"""
        room.spawn_agent(agent_id, np.array([2.0, 2.0, 0.0]))
        
        print(f"\nScenario: Stack 3 blocks")
        print(f"Agent {agent_id} must stack small blocks vertically")
        
        for step in range(100):
            # Agent would take actions here
            room.step()
            
            if room.task_stack_blocks(agent_id, 3):
                print(f"SUCCESS at step {step}!")
                return True
        
        return False
    
    @staticmethod
    def scenario_push_ball(room: PhysicsRoom, agent_id: str):
        """Train pushing ball to target"""
        room.spawn_agent(agent_id, np.array([2.0, 7.0, 0.0]))
        target = np.array([8.0, 7.0, 0.0])
        
        print(f"\nScenario: Push ball to target")
        print(f"Target: {target}")
        
        for step in range(100):
            # Agent pushes ball
            room.step({
                agent_id: {'type': 'push', 'target_id': 'ball_0', 
                          'force': [0.1, 0, 0]}
            })
            
            if room.task_push_ball_to_target(agent_id, 'ball_0', target):
                print(f"SUCCESS at step {step}!")
                return True
        
        return False
    
    @staticmethod
    def scenario_place_on_table(room: PhysicsRoom, agent_id: str):
        """Train placing object on table"""
        room.spawn_agent(agent_id, np.array([8.0, 2.0, 0.0]))
        
        print(f"\nScenario: Place block on table")
        
        # Pick up block and move to table
        block_id = 'block_small_0'
        
        for step in range(100):
            actions = {}
            
            # Grip, move, release
            if step < 10:
                actions[agent_id] = {'type': 'grip', 'target_id': block_id}
            elif step < 50:
                actions[agent_id] = {'type': 'move', 'delta': [0.05, 0.03, 0]}
            elif step == 50:
                actions[agent_id] = {'type': 'release', 'target_id': block_id}
            
            room.step(actions)
            
            if room.task_move_object_to_table(agent_id, block_id):
                print(f"SUCCESS at step {step}!")
                return True
        
        return False


def main():
    """Demo physics room"""
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("PHYSICS TRAINING ROOM FOR MYL CHILDREN")
    print("=" * 70)
    
    # Create room
    room = PhysicsRoom()
    room.print_room_layout()
    
    # Run training scenarios
    scenarios = TrainingScenarios()
    
    print("\n" + "=" * 70)
    print("TRAINING SCENARIOS")
    print("=" * 70)
    
    # Scenario 1: Stack blocks
    room1 = PhysicsRoom()
    success1 = scenarios.scenario_stack_blocks(room1, "myl_001")
    
    # Scenario 2: Push ball
    room2 = PhysicsRoom()
    success2 = scenarios.scenario_push_ball(room2, "myl_002")
    
    # Scenario 3: Place on table
    room3 = PhysicsRoom()
    success3 = scenarios.scenario_place_on_table(room3, "myl_003")
    
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Stack blocks: {'PASS' if success1 else 'FAIL'}")
    print(f"Push ball: {'PASS' if success2 else 'FAIL'}")
    print(f"Place on table: {'PASS' if success3 else 'FAIL'}")
    
    print("\n" + "=" * 70)
    print("PHYSICS ROOM READY FOR MYL CHILDREN")
    print("=" * 70)


if __name__ == "__main__":
    main()
