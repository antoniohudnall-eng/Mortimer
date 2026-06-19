#!/usr/bin/env python3
"""
MYL Children Expanded Physics Training Room
Comprehensive environment with diverse objects and scenarios

Features:
- Diverse objects: blocks, balls, ramps, stairs, containers, doors
- Multiple rooms: Play area, obstacle course, precision zone
- Interactive scenarios: sorting, stacking, navigation
- Agent observation and learning
"""

import numpy as np
import json
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Set
from enum import Enum
import time
import logging
import random

__version__ = "2.0.0"


class ObjectType(Enum):
    """Types of objects in the room"""
    BLOCK = "block"
    BALL = "ball"
    TABLE = "table"
    CHAIR = "chair"
    RAMP = "ramp"
    STAIRS = "stairs"
    CONTAINER = "container"
    DOOR = "door"
    WALL = "wall"
    SENSOR = "sensor"
    BUTTON = "button"


@dataclass
class PhysicsObject:
    """Physical object in the training room"""
    id: str
    obj_type: ObjectType
    position: np.ndarray  # [x, y, z]
    velocity: np.ndarray
    size: np.ndarray      # dimensions
    mass: float
    color: str
    movable: bool
    gripped: bool = False
    activated: bool = False  # For buttons/sensors
    parent: Optional[str] = None  # For hierarchical objects
    
    def get_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get AABB bounds (min, max)"""
        half_size = self.size / 2
        return self.position - half_size, self.position + half_size
    
    def contains_point(self, point: np.ndarray) -> bool:
        """Check if point is inside object"""
        min_b, max_b = self.get_bounds()
        return np.all(point >= min_b) and np.all(point <= max_b)


@dataclass
class RoomConfig:
    """Room configuration"""
    size: Tuple[float, float, float] = (20.0, 20.0, 5.0)  # Larger room
    gravity: np.ndarray = field(default_factory=lambda: np.array([0, 0, -9.81]))
    dt: float = 0.01
    friction: float = 0.9
    bounce_damping: float = 0.3


class AgentObservation:
    """What an agent can observe"""
    def __init__(self, agent_id: str, position: np.ndarray):
        self.agent_id = agent_id
        self.position = position
        self.visible_objects: List[str] = []
        self.touching: Optional[str] = None
        self.gripping: Optional[str] = None
        self.hearing: List[str] = []  # Sound events
        self.memory: Dict = {}  # What agent remembers


class ExpandedPhysicsRoom:
    """
    Expanded physics training room with multiple zones and objects.
    
    Zones:
    - Play Area: Open space with blocks, balls, basic furniture
    - Obstacle Course: Ramps, stairs, narrow passages
    - Precision Zone: Small objects, delicate manipulation
    - Sorting Area: Multiple containers, categorization tasks
    """
    
    def __init__(self, config: Optional[RoomConfig] = None):
        self.config = config or RoomConfig()
        self.logger = logging.getLogger("ExpandedPhysicsRoom")
        
        self.objects: Dict[str, PhysicsObject] = {}
        self.agents: Dict[str, AgentObservation] = {}
        self.zones: Dict[str, Tuple[np.ndarray, np.ndarray]] = {}
        
        self.time = 0.0
        self.events: List[Dict] = []  # Event log for learning
        
        self._build_zones()
        self._build_room()
        
        self.logger.info(f"Expanded physics room initialized: {self.config.size}")
    
    def _build_zones(self):
        """Define different training zones"""
        # Play Area: 0-10x, 0-10y
        self.zones['play'] = (np.array([0, 0, 0]), np.array([10, 10, 3]))
        
        # Obstacle Course: 10-20x, 0-10y
        self.zones['obstacle'] = (np.array([10, 0, 0]), np.array([20, 10, 3]))
        
        # Precision Zone: 0-10x, 10-20y
        self.zones['precision'] = (np.array([0, 10, 0]), np.array([10, 20, 3]))
        
        # Sorting Area: 10-20x, 10-20y
        self.zones['sorting'] = (np.array([10, 10, 0]), np.array([20, 20, 3]))
    
    def _build_room(self):
        """Build the expanded training room"""
        
        # === FLOOR AND WALLS ===
        self._build_structure()
        
        # === PLAY AREA ===
        self._build_play_area()
        
        # === OBSTACLE COURSE ===
        self._build_obstacle_course()
        
        # === PRECISION ZONE ===
        self._build_precision_zone()
        
        # === SORTING AREA ===
        self._build_sorting_area()
    
    def _build_structure(self):
        """Build floor and walls"""
        # Main floor
        self.add_object(PhysicsObject(
            id="floor",
            obj_type=ObjectType.WALL,
            position=np.array([10, 10, -0.5]),
            velocity=np.zeros(3),
            size=np.array([20, 20, 1]),
            mass=10000,
            color="gray",
            movable=False
        ))
        
        # Zone dividers (low walls)
        for i, (name, (min_c, max_c)) in enumerate(self.zones.items()):
            if name != 'play':  # Don't divide play area
                # Add subtle markers
                center = (min_c + max_c) / 2
                self.add_object(PhysicsObject(
                    id=f"zone_marker_{name}",
                    obj_type=ObjectType.SENSOR,
                    position=center,
                    velocity=np.zeros(3),
                    size=np.array([0.1, 0.1, 0.1]),
                    mass=0.1,
                    color="white",
                    movable=False
                ))
    
    def _build_play_area(self):
        """Build play area with basic furniture and toys"""
        
        # Large play table
        self.add_object(PhysicsObject(
            id="play_table",
            obj_type=ObjectType.TABLE,
            position=np.array([5, 5, 0.6]),
            velocity=np.zeros(3),
            size=np.array([3, 2, 0.1]),
            mass=50,
            color="lightbrown",
            movable=False
        ))
        
        # Building blocks (various sizes and colors)
        block_configs = [
            # (id_suffix, position, size, color)
            ("red_large", [2, 2, 0.3], [0.6, 0.6, 0.6], "red"),
            ("blue_large", [3, 2, 0.3], [0.6, 0.6, 0.6], "blue"),
            ("green_medium", [2, 3, 0.2], [0.4, 0.4, 0.4], "green"),
            ("yellow_medium", [3, 3, 0.2], [0.4, 0.4, 0.4], "yellow"),
            ("purple_small", [4, 2, 0.15], [0.3, 0.3, 0.3], "purple"),
            ("orange_small", [4, 3, 0.15], [0.3, 0.3, 0.3], "orange"),
            ("cyan_tiny", [2, 4, 0.1], [0.2, 0.2, 0.2], "cyan"),
            ("pink_tiny", [3, 4, 0.1], [0.2, 0.2, 0.2], "pink"),
        ]
        
        for suffix, pos, size, color in block_configs:
            self.add_object(PhysicsObject(
                id=f"block_{suffix}",
                obj_type=ObjectType.BLOCK,
                position=np.array(pos),
                velocity=np.zeros(3),
                size=np.array(size),
                mass=size[0] * size[1] * size[2] * 2,  # Density ~2
                color=color,
                movable=True
            ))
        
        # Balls (different sizes)
        ball_configs = [
            ("basketball", [6, 2, 0.25], 0.25, "orange", 0.6),
            ("tennis", [7, 2, 0.04], 0.04, "yellow", 0.06),
            ("marble", [6, 3, 0.015], 0.015, "blue", 0.01),
            ("beach", [7, 3, 0.2], 0.2, "redwhite", 0.5),
        ]
        
        for name, pos, radius, color, mass in ball_configs:
            self.add_object(PhysicsObject(
                id=f"ball_{name}",
                obj_type=ObjectType.BALL,
                position=np.array(pos),
                velocity=np.zeros(3),
                size=np.array([radius*2, radius*2, radius*2]),
                mass=mass,
                color=color,
                movable=True
            ))
        
        # Child-sized chair
        self.add_object(PhysicsObject(
            id="play_chair",
            obj_type=ObjectType.CHAIR,
            position=np.array([7, 5, 0.4]),
            velocity=np.zeros(3),
            size=np.array([0.8, 0.8, 0.8]),
            mass=15,
            color="blue",
            movable=True
        ))
    
    def _build_obstacle_course(self):
        """Build obstacle course with ramps and stairs"""
        
        # Ramp (inclined platform)
        self.add_object(PhysicsObject(
            id="ramp_main",
            obj_type=ObjectType.RAMP,
            position=np.array([12, 2, 0.5]),
            velocity=np.zeros(3),
            size=np.array([3, 1.5, 0.1]),
            mass=100,
            color="brown",
            movable=False
        ))
        
        # Stairs (3 steps)
        for i in range(3):
            self.add_object(PhysicsObject(
                id=f"stair_{i}",
                obj_type=ObjectType.STAIRS,
                position=np.array([14, 4 + i*0.8, 0.15 + i*0.15]),
                velocity=np.zeros(3),
                size=np.array([1.5, 0.6, 0.3]),
                mass=50,
                color="gray",
                movable=False
            ))
        
        # Narrow passage walls
        self.add_object(PhysicsObject(
            id="passage_wall_1",
            obj_type=ObjectType.WALL,
            position=np.array([12, 7, 0.5]),
            velocity=np.zeros(3),
            size=np.array([0.2, 3, 1]),
            mass=200,
            color="white",
            movable=False
        ))
        
        self.add_object(PhysicsObject(
            id="passage_wall_2",
            obj_type=ObjectType.WALL,
            position=np.array([14, 7, 0.5]),
            velocity=np.zeros(3),
            size=np.array([0.2, 3, 1]),
            mass=200,
            color="white",
            movable=False
        ))
        
        # Rolling test cylinders
        self.add_object(PhysicsObject(
            id="cylinder_wood",
            obj_type=ObjectType.BALL,  # Treat as rolling
            position=np.array([13, 2, 0.2]),
            velocity=np.zeros(3),
            size=np.array([0.3, 0.3, 0.4]),  # Non-sphere
            mass=0.8,
            color="wood",
            movable=True
        ))
    
    def _build_precision_zone(self):
        """Build precision zone with delicate objects"""
        
        # Small peg board (for peg insertion tasks)
        self.add_object(PhysicsObject(
            id="peg_board",
            obj_type=ObjectType.TABLE,
            position=np.array([3, 13, 0.5]),
            velocity=np.zeros(3),
            size=np.array([2, 2, 0.05]),
            mass=30,
            color="white",
            movable=False
        ))
        
        # Pegs to insert
        for i in range(4):
            for j in range(4):
                self.add_object(PhysicsObject(
                    id=f"peg_{i}_{j}",
                    obj_type=ObjectType.BLOCK,
                    position=np.array([2.2 + i*0.4, 12.2 + j*0.4, 0.15]),
                    velocity=np.zeros(3),
                    size=np.array([0.05, 0.05, 0.3]),
                    mass=0.05,
                    color="red",
                    movable=True
                ))
        
        # Stacking rings
        ring_sizes = [0.3, 0.25, 0.2, 0.15, 0.1]
        for i, size in enumerate(ring_sizes):
            self.add_object(PhysicsObject(
                id=f"ring_{i}",
                obj_type=ObjectType.BLOCK,
                position=np.array([6, 13, 0.05 + i*0.05]),
                velocity=np.zeros(3),
                size=np.array([size*2, size*2, 0.05]),
                mass=0.1,
                color=f"ring_{i}",
                movable=True
            ))
        
        # Precision grip objects (small)
        self.add_object(PhysicsObject(
            id="small_cube",
            obj_type=ObjectType.BLOCK,
            position=np.array([5, 15, 0.03]),
            velocity=np.zeros(3),
            size=np.array([0.05, 0.05, 0.05]),
            mass=0.01,
            color="gold",
            movable=True
        ))
        
        self.add_object(PhysicsObject(
            id="small_sphere",
            obj_type=ObjectType.BALL,
            position=np.array([7, 15, 0.03]),
            velocity=np.zeros(3),
            size=np.array([0.06, 0.06, 0.06]),
            mass=0.015,
            color="silver",
            movable=True
        ))
    
    def _build_sorting_area(self):
        """Build sorting area with containers"""
        
        # Sorting containers (bins)
        container_positions = [
            ([13, 13], "red", "color"),
            ([15, 13], "blue", "color"),
            ([17, 13], "green", "color"),
            ([13, 15], "small", "size"),
            ([15, 15], "medium", "size"),
            ([17, 15], "large", "size"),
        ]
        
        for pos, name, sort_type in container_positions:
            self.add_object(PhysicsObject(
                id=f"bin_{name}",
                obj_type=ObjectType.CONTAINER,
                position=np.array([pos[0], pos[1], 0.25]),
                velocity=np.zeros(3),
                size=np.array([1.5, 1.5, 0.5]),
                mass=20,
                color=name if sort_type == "color" else "gray",
                movable=False
            ))
            
            # Mark as container
            obj = self.objects[f"bin_{name}"]
            obj.activated = True  # Container is "active"
            obj.parent = sort_type  # What it sorts by
        
        # Sorting items (scattered)
        sort_items = [
            ("red_small", [12, 17], "red", 0.2),
            ("red_medium", [13, 17], "red", 0.3),
            ("red_large", [14, 17], "red", 0.4),
            ("blue_small", [15, 17], "blue", 0.2),
            ("blue_medium", [16, 17], "blue", 0.3),
            ("blue_large", [17, 17], "blue", 0.4),
            ("green_small", [18, 17], "green", 0.2),
            ("green_medium", [18, 16], "green", 0.3),
            ("green_large", [18, 15], "green", 0.4),
        ]
        
        for name, pos, color, size in sort_items:
            self.add_object(PhysicsObject(
                id=f"sort_item_{name}",
                obj_type=ObjectType.BLOCK,
                position=np.array([pos[0], pos[1], size/2]),
                velocity=np.zeros(3),
                size=np.array([size, size, size]),
                mass=size**3 * 2,
                color=color,
                movable=True
            ))
    
    def add_object(self, obj: PhysicsObject):
        """Add object to room"""
        self.objects[obj.id] = obj
    
    def spawn_agent(self, agent_id: str, position: np.ndarray = None):
        """Spawn agent in room"""
        if position is None:
            position = np.array([1, 1, 0])
        
        self.agents[agent_id] = AgentObservation(agent_id, position.copy())
        self.logger.info(f"Agent {agent_id} spawned at {position}")
    
    def step(self, actions: Dict[str, List[Dict]] = None):
        """Advance physics simulation"""
        actions = actions or {}
        
        # Process agent actions
        for agent_id, action_list in actions.items():
            for action in action_list:
                self._process_action(agent_id, action)
        
        # Update physics
        for obj in self.objects.values():
            if obj.movable and not obj.gripped:
                self._update_physics(obj)
        
        # Detect collisions and events
        self._detect_events()
        
        self.time += self.config.dt
    
    def _process_action(self, agent_id: str, action: Dict):
        """Process single agent action"""
        action_type = action.get('type')
        
        if action_type == 'move':
            if agent_id in self.agents:
                delta = np.array(action.get('delta', [0, 0, 0]))
                self.agents[agent_id].position += delta
                
        elif action_type == 'grip':
            target_id = action.get('target_id')
            if target_id and target_id in self.objects:
                obj = self.objects[target_id]
                if obj.movable:
                    obj.gripped = True
                    obj.velocity = np.zeros(3)
                    if agent_id in self.agents:
                        self.agents[agent_id].gripping = target_id
                    
        elif action_type == 'release':
            if agent_id in self.agents:
                gripping = self.agents[agent_id].gripping
                if gripping and gripping in self.objects:
                    self.objects[gripping].gripped = False
                    self.agents[agent_id].gripping = None
                    
        elif action_type == 'push':
            target_id = action.get('target_id')
            force = np.array(action.get('force', [0, 0, 0]))
            if target_id and target_id in self.objects:
                obj = self.objects[target_id]
                if obj.movable:
                    obj.velocity += force / obj.mass * self.config.dt
    
    def _update_physics(self, obj: PhysicsObject):
        """Update object physics"""
        # Gravity
        obj.velocity += self.config.gravity * self.config.dt
        
        # Position update
        obj.position += obj.velocity * self.config.dt
        
        # Floor collision
        half_height = obj.size[2] / 2
        if obj.position[2] < half_height:
            obj.position[2] = half_height
            if obj.velocity[2] < 0:
                obj.velocity[2] *= -self.config.bounce_damping
            obj.velocity[0:2] *= self.config.friction
    
    def _detect_events(self):
        """Detect and log events"""
        # Check agent-object interactions
        for agent_id, agent in self.agents.items():
            agent.visible_objects = []
            agent.touching = None
            
            for obj_id, obj in self.objects.items():
                if obj.obj_type in [ObjectType.WALL, ObjectType.SENSOR]:
                    continue
                    
                # Visibility check (within 5m)
                dist = np.linalg.norm(agent.position - obj.position)
                if dist < 5.0:
                    agent.visible_objects.append(obj_id)
                
                # Touching check (within 0.5m)
                if dist < 0.5:
                    agent.touching = obj_id
    
    # === TASK VERIFICATION ===
    
    def task_stack_blocks(self, agent_id: str, num_blocks: int = 3, 
                          tolerance: float = 0.1) -> bool:
        """Check if blocks are stacked"""
        blocks = [obj for obj in self.objects.values() 
                 if obj.obj_type == ObjectType.BLOCK and obj.movable]
        
        if len(blocks) < num_blocks:
            return False
        
        # Find stacks (blocks aligned vertically)
        for i, block1 in enumerate(blocks):
            stack_count = 1
            for block2 in blocks:
                if block1.id != block2.id:
                    dx = abs(block1.position[0] - block2.position[0])
                    dy = abs(block1.position[1] - block2.position[1])
                    dz = abs(block1.position[2] - block2.position[2] - 
                             (block1.size[2] + block2.size[2])/2)
                    
                    if dx < tolerance and dy < tolerance and dz < tolerance:
                        stack_count += 1
            
            if stack_count >= num_blocks:
                return True
        
        return False
    
    def task_sort_by_color(self, agent_id: str) -> Tuple[int, int]:
        """Check sorting progress. Returns (correct, total)"""
        correct = 0
        total = 0
        
        # Find items in containers
        for obj_id, obj in self.objects.items():
            if obj_id.startswith("sort_item_"):
                total += 1
                item_color = obj.color
                
                # Check if in matching container
                for container_id, container in self.objects.items():
                    if container_id.startswith("bin_") and container.obj_type == ObjectType.CONTAINER:
                        container_color = container.color
                        if container.contains_point(obj.position) and item_color == container_color:
                            correct += 1
                            break
        
        return correct, total
    
    def task_navigate_obstacle(self, agent_id: str) -> bool:
        """Check if agent navigated obstacle course"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        
        # Check if agent reached end of obstacle zone
        obstacle_end = np.array([19, 9, 0])  # End of obstacle course
        dist = np.linalg.norm(agent.position - obstacle_end)
        
        return dist < 1.0
    
    def task_place_in_container(self, agent_id: str, item_id: str, 
                                 container_id: str) -> bool:
        """Check if item is in container"""
        if item_id not in self.objects or container_id not in self.objects:
            return False
        
        item = self.objects[item_id]
        container = self.objects[container_id]
        
        return container.contains_point(item.position)
    
    def get_room_state(self) -> Dict:
        """Get complete room state"""
        return {
            'time': self.time,
            'objects': {
                obj_id: {
                    'type': obj.obj_type.value,
                    'position': obj.position.tolist(),
                    'velocity': obj.velocity.tolist(),
                    'size': obj.size.tolist(),
                    'color': obj.color,
                    'movable': obj.movable,
                    'gripped': obj.gripped
                }
                for obj_id, obj in self.objects.items()
            },
            'agents': {
                agent_id: {
                    'position': agent.position.tolist(),
                    'visible': agent.visible_objects,
                    'touching': agent.touching,
                    'gripping': agent.gripping
                }
                for agent_id, agent in self.agents.items()
            },
            'zones': {
                name: {
                    'min': zone[0].tolist(),
                    'max': zone[1].tolist()
                }
                for name, zone in self.zones.items()
            }
        }
    
    def print_room_summary(self):
        """Print room summary"""
        print("\n" + "=" * 70)
        print("EXPANDED PHYSICS ROOM SUMMARY")
        print("=" * 70)
        print(f"Room Size: {self.config.size}")
        print(f"Total Objects: {len(self.objects)}")
        print(f"Agents: {len(self.agents)}")
        
        print("\nObject Counts by Type:")
        type_counts = {}
        for obj in self.objects.values():
            type_counts[obj.obj_type.value] = type_counts.get(obj.obj_type.value, 0) + 1
        for obj_type, count in sorted(type_counts.items()):
            print(f"  {obj_type}: {count}")
        
        print("\nZones:")
        for name, (min_c, max_c) in self.zones.items():
            print(f"  {name}: {min_c} to {max_c}")
        
        print("=" * 70)


class TrainingScenario:
    """Pre-defined training scenarios"""
    
    def __init__(self, room: ExpandedPhysicsRoom):
        self.room = room
        self.scenarios = {
            'stack_tower': self._scenario_stack_tower,
            'sort_colors': self._scenario_sort_colors,
            'navigate_course': self._scenario_navigate,
            'precision_place': self._scenario_precision,
            'multi_task': self._scenario_multi,
        }
    
    def run(self, scenario_name: str, agent_id: str) -> Dict:
        """Run a training scenario"""
        if scenario_name not in self.scenarios:
            return {'error': f'Unknown scenario: {scenario_name}'}
        
        return self.scenarios[scenario_name](agent_id)
    
    def _scenario_stack_tower(self, agent_id: str) -> Dict:
        """Stack 5 blocks in a tower"""
        self.room.spawn_agent(agent_id, np.array([2, 2, 0]))
        
        steps = 0
        max_steps = 500
        
        while steps < max_steps:
            self.room.step()
            
            if self.room.task_stack_blocks(agent_id, 5):
                return {
                    'success': True,
                    'steps': steps,
                    'task': 'stack_tower'
                }
            
            steps += 1
        
        return {
            'success': False,
            'steps': steps,
            'task': 'stack_tower'
        }
    
    def _scenario_sort_colors(self, agent_id: str) -> Dict:
        """Sort items by color into containers"""
        self.room.spawn_agent(agent_id, np.array([16, 16, 0]))
        
        steps = 0
        max_steps = 1000
        
        while steps < max_steps:
            self.room.step()
            
            correct, total = self.room.task_sort_by_color(agent_id)
            if correct == total and total > 0:
                return {
                    'success': True,
                    'steps': steps,
                    'task': 'sort_colors',
                    'correct': correct,
                    'total': total
                }
            
            steps += 1
        
        correct, total = self.room.task_sort_by_color(agent_id)
        return {
            'success': False,
            'steps': steps,
            'task': 'sort_colors',
            'correct': correct,
            'total': total
        }
    
    def _scenario_navigate(self, agent_id: str) -> Dict:
        """Navigate obstacle course"""
        self.room.spawn_agent(agent_id, np.array([11.0, 2.0, 0.0]))
        
        steps = 0
        max_steps = 1000
        
        while steps < max_steps:
            self.room.step({
                agent_id: [{'type': 'move', 'delta': [0.05, 0.0, 0.0]}]
            })
            
            if self.room.task_navigate_obstacle(agent_id):
                return {
                    'success': True,
                    'steps': steps,
                    'task': 'navigate'
                }
            
            steps += 1
        
        return {
            'success': False,
            'steps': steps,
            'task': 'navigate'
        }
    
    def _scenario_precision(self, agent_id: str) -> Dict:
        """Place small objects precisely"""
        self.room.spawn_agent(agent_id, np.array([3, 12, 0]))
        
        steps = 0
        max_steps = 500
        
        while steps < max_steps:
            self.room.step()
            
            # Check if small cube is on peg board
            if self.room.task_place_in_container(agent_id, 'small_cube', 'peg_board'):
                return {
                    'success': True,
                    'steps': steps,
                    'task': 'precision_place'
                }
            
            steps += 1
        
        return {
            'success': False,
            'steps': steps,
            'task': 'precision_place'
        }
    
    def _scenario_multi(self, agent_id: str) -> Dict:
        """Multi-task scenario: sort, then stack, then navigate"""
        self.room.spawn_agent(agent_id, np.array([10, 10, 0]))
        
        results = []
        
        # Task 1: Sort one item
        steps = 0
        while steps < 300:
            self.room.step()
            correct, _ = self.room.task_sort_by_color(agent_id)
            if correct >= 1:
                results.append({'task': 'sort_1', 'success': True, 'steps': steps})
                break
            steps += 1
        else:
            results.append({'task': 'sort_1', 'success': False, 'steps': steps})
        
        # Task 2: Stack 2 blocks
        steps = 0
        while steps < 300:
            self.room.step()
            if self.room.task_stack_blocks(agent_id, 2):
                results.append({'task': 'stack_2', 'success': True, 'steps': steps})
                break
            steps += 1
        else:
            results.append({'task': 'stack_2', 'success': False, 'steps': steps})
        
        return {
            'success': all(r['success'] for r in results),
            'results': results,
            'task': 'multi'
        }


def main():
    """Demo expanded physics room"""
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("EXPANDED PHYSICS ROOM FOR MYL CHILDREN")
    print("=" * 70)
    
    # Create room
    room = ExpandedPhysicsRoom()
    room.print_room_summary()
    
    # Create scenario runner
    scenarios = TrainingScenario(room)
    
    # Run scenarios
    print("\n" + "=" * 70)
    print("TRAINING SCENARIOS")
    print("=" * 70)
    
    scenario_list = ['stack_tower', 'sort_colors', 'navigate_course', 'precision_place']
    
    for scenario_name in scenario_list:
        print(f"\nRunning: {scenario_name}")
        result = scenarios.run(scenario_name, f"myl_{scenario_name}")
        print(f"  Result: {'SUCCESS' if result['success'] else 'FAILED'}")
        print(f"  Steps: {result.get('steps', 'N/A')}")
    
    print("\n" + "=" * 70)
    print("EXPANDED PHYSICS ROOM READY FOR MYL CHILDREN")
    print("=" * 70)


if __name__ == "__main__":
    main()
