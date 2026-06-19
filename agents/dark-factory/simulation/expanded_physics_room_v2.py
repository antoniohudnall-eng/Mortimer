#!/usr/bin/env python3
"""
MYL Children Expanded Physics Training Room v2.0
Comprehensive environment with diverse objects and scenarios

Features:
- Diverse objects: blocks, balls, ramps, stairs, containers, doors, hallways
- Multiple rooms: Play area, obstacle course, precision zone, hallway
- Interactive scenarios: sorting, stacking, navigation, doorways, turns
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

__version__ = "2.1.0"


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
    DOORWAY = "doorway"


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
    size: Tuple[float, float, float] = (30.0, 30.0, 6.0)  # Extended room
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
    - Hallway: Doorway with left/right turn, steps up
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
        
        # Hallway: 20-30x, 0-10y
        self.zones['hallway'] = (np.array([20, 0, 0]), np.array([30, 10, 3]))
    
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
        
        # === HALLWAY WITH DOORWAY AND TURN ===
        self._build_hallway()
    
    def _build_structure(self):
        """Build floor and walls"""
        # Main floor
        self.add_object(PhysicsObject(
            id="floor",
            obj_type=ObjectType.WALL,
            position=np.array([15, 15, -0.5]),
            velocity=np.zeros(3),
            size=np.array([30, 30, 1]),
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
                color="gray",
                movable=False
            ))
        
        # Items to sort
        sort_items = [
            ("red_small", [13, 13.5], [0.1, 0.1, 0.1], "red", "color_small"),
            ("blue_medium", [15.2, 13.3], [0.2, 0.2, 0.2], "blue", "color_medium"),
            ("green_large", [16.8, 13.1], [0.3, 0.3, 0.3], "green", "color_large"),
            ("circle_small", [13.5, 14.8], [0.15, 0.15, 0.05], "yellow", "shape_circle"),
            ("square_medium", [15, 14.5], [0.25, 0.25, 0.05], "orange", "shape_square"),
            ("triangle_large", [17, 14.7], [0.35, 0.35, 0.05], "purple", "shape_triangle"),
        ]
        
        for name, pos, size, color, category in sort_items:
            self.add_object(PhysicsObject(
                id=f"sort_{name}",
                obj_type=ObjectType.BLOCK,
                position=np.array([pos[0], pos[1], 0.05 + size[2]/2]),
                velocity=np.zeros(3),
                size=np.array(size),
                mass=size[0] * size[1] * size[2] * 2,
                color=color,
                movable=True
            ))
    
    def _build_hallway(self):
        """Build hallway with doorway, left/right turn, and steps up"""
        
        # === DOORWAY ===
        # Door frame
        self.add_object(PhysicsObject(
            id="door_frame_left",
            obj_type=ObjectType.WALL,
            position=np.array([20.0, 2.0, 1.0]),
            velocity=np.zeros(3),
            size=np.array([0.2, 1.5, 2.0]),
            mass=500,
            color="white",
            movable=False
        ))
        
        self.add_object(PhysicsObject(
            id="door_frame_right",
            obj_type=ObjectType.WALL,
            position=np.array([20.0, 6.0, 1.0]),
            velocity=np.zeros(3),
            size=np.array([0.2, 1.5, 2.0]),
            mass=500,
            color="white",
            movable=False
        ))
        
        self.add_object(PhysicsObject(
            id="door_frame_top",
            obj_type=ObjectType.WALL,
            position=np.array([20.0, 4.0, 2.3]),
            velocity=np.zeros(3),
            size=np.array([0.2, 4.0, 0.4]),
            mass=300,
            color="white",
            movable=False
        ))
        
        # Actual door (swingable)
        self.add_object(PhysicsObject(
            id="door_main",
            obj_type=ObjectType.DOOR,
            position=np.array([20.0, 4.0, 1.0]),
            velocity=np.zeros(3),
            size=np.array([0.1, 1.8, 2.0]),
            mass=50,
            color="brown",
            movable=True
        ))
        
        # Door sensor/button
        self.add_object(PhysicsObject(
            id="door_button",
            obj_type=ObjectType.BUTTON,
            position=np.array([19.5, 4.0, 1.0]),
            velocity=np.zeros(3),
            size=np.array([0.1, 0.2, 0.2]),
            mass=1,
            color="red",
            movable=False
        ))
        
        # === HALLWAY WALLS ===
        # Left wall (outer)
        for y in [0, 5, 10]:
            self.add_object(PhysicsObject(
                id=f"hallway_wall_left_{y}",
                obj_type=ObjectType.WALL,
                position=np.array([25.0, y + 2.5, 1.0]),
                velocity=np.zeros(3),
                size=np.array([10.0, 0.2, 2.0]),
                mass=1000,
                color="white",
                movable=False
            ))
        
        # Right wall (inner)
        for y in [0, 5, 10]:
            self.add_object(PhysicsObject(
                id=f"hallway_wall_right_{y}",
                obj_type=ObjectType.WALL,
                position=np.array([25.0, y - 2.5, 1.0]),
                velocity=np.zeros(3),
                size=np.array([10.0, 0.2, 2.0]),
                mass=1000,
                color="white",
                movable=False
            ))
        
        # === LEFT TURN AREA ===
        # Wall blocking straight path
        self.add_object(PhysicsObject(
            id="turn_block_left",
            obj_type=ObjectType.WALL,
            position=np.array([28.0, 1.5, 1.0]),
            velocity=np.zeros(3),
            size=np.array([0.2, 3.0, 2.0]),
            mass=800,
            color="gray",
            movable=False
        ))
        
        # Indicator for left turn
        self.add_object(PhysicsObject(
            id="turn_indicator_left",
            obj_type=ObjectType.SENSOR,
            position=np.array([26.0, 3.0, 0.1]),
            velocity=np.zeros(3),
            size=np.array([0.5, 0.5, 0.1]),
            mass=0.5,
            color="green",
            movable=False
        ))
        
        # === RIGHT TURN AREA ===
        # Wall blocking straight path
        self.add_object(PhysicsObject(
            id="turn_block_right",
            obj_type=ObjectType.WALL,
            position=np.array([28.0, 8.5, 1.0]),
            velocity=np.zeros(3),
            size=np.array([0.2, 3.0, 2.0]),
            mass=800,
            color="gray",
            movable=False
        ))
        
        # Indicator for right turn
        self.add_object(PhysicsObject(
            id="turn_indicator_right",
            obj_type=ObjectType.SENSOR,
            position=np.array([26.0, 7.0, 0.1]),
            velocity=np.zeros(3),
            size=np.array([0.5, 0.5, 0.1]),
            mass=0.5,
            color="blue",
            movable=False
        ))
        
        # === STEPS UP ===
        # Platform at end of hallway
        self.add_object(PhysicsObject(
            id="platform_base",
            obj_type=ObjectType.WALL,
            position=np.array([28.0, 5.0, 0.5]),
            velocity=np.zeros(3),
            size=np.array([4.0, 6.0, 1.0]),
            mass=2000,
            color="concrete",
            movable=False
        ))
        
        # Steps up (4 steps)
        for i in range(4):
            step_height = 0.2 * (i + 1)
            self.add_object(PhysicsObject(
                id=f"step_up_{i}",
                obj_type=ObjectType.STAIRS,
                position=np.array([26.0 + i*0.5, 5.0, step_height/2]),
                velocity=np.zeros(3),
                size=np.array([0.6, 4.0, step_height]),
                mass=500,
                color="gray",
                movable=False
            ))
        
        # === END OF HALLWAY FEATURES ===
        # Final platform
        self.add_object(PhysicsObject(
            id="platform_final",
            obj_type=ObjectType.TABLE,
            position=np.array([29.0, 5.0, 1.0]),
            velocity=np.zeros(3),
            size=np.array([2.0, 4.0, 0.1]),
            mass=100,
            color="blue",
            movable=False
        ))
        
        # Reward/target object on platform
        self.add_object(PhysicsObject(
            id="hallway_target_trophy",
            obj_type=ObjectType.BLOCK,
            position=np.array([29.0, 5.0, 1.2]),
            velocity=np.zeros(3),
            size=np.array([0.3, 0.3, 0.4]),
            mass=1,
            color="gold",
            movable=True
        ))
    
    def add_object(self, obj: PhysicsObject):
        """Add an object to the room"""
        self.objects[obj.id] = obj
    
    def add_agent(self, agent_id: str, position: np.ndarray):
        """Add an agent to the room"""
        self.agents[agent_id] = AgentObservation(agent_id, position)
        self.logger.info(f"Agent {agent_id} entered at {position}")
    
    def get_objects_in_zone(self, zone_name: str) -> List[str]:
        """Get all objects in a specific zone"""
        if zone_name not in self.zones:
            return []
        
        min_c, max_c = self.zones[zone_name]
        result = []
        for obj_id, obj in self.objects.items():
            if np.all(obj.position >= min_c) and np.all(obj.position <= max_c):
                result.append(obj_id)
        return result
    
    def step(self, dt: Optional[float] = None) -> Dict:
        """Step physics simulation forward"""
        dt = dt or self.config.dt
        
        # Update positions (simple Euler integration for now)
        for obj in self.objects.values():
            if obj.movable and obj.parent is None:
                obj.position += obj.velocity * dt
                obj.velocity += self.config.gravity * dt
                
                # Floor collision
                min_b, max_b = obj.get_bounds()
                if min_b[2] < 0:
                    obj.position[2] = obj.size[2] / 2
                    obj.velocity[2] = -obj.velocity[2] * self.config.bounce_damping
                    obj.velocity[0] *= self.config.friction
                    obj.velocity[1] *= self.config.friction
        
        self.time += dt
        return {"time": self.time, "objects": len(self.objects)}
    
    def get_state(self) -> Dict:
        """Get current room state"""
        return {
            "time": self.time,
            "objects": {k: {
                "position": v.position.tolist(),
                "velocity": v.velocity.tolist(),
                "type": v.obj_type.value,
                "movable": v.movable
            } for k, v in self.objects.items()},
            "agents": {k: {
                "position": v.position.tolist(),
                "visible": v.visible_objects
            } for k, v in self.agents.items()},
            "zones": {k: {"min": v[0].tolist(), "max": v[1].tolist()} 
                     for k, v in self.zones.items()}
        }
    
    def save_state(self, filename: str):
        """Save room state to file"""
        with open(filename, 'w') as f:
            json.dump(self.get_state(), f, indent=2)


class TrainingScenario:
    """
    Training scenarios for MYL children in the expanded physics room.
    
    Scenarios:
    - stack_tower: Stack blocks to build tower
    - sort_colors: Sort colored items into bins
    - navigate_course: Navigate ramps, stairs, obstacles
    - precision_place: Place small objects precisely
    - multi_task: Combined challenges
    - navigate_hallway: New - door, turn, steps
    """
    
    def __init__(self, room: ExpandedPhysicsRoom):
        self.room = room
        self.logger = logging.getLogger("TrainingScenario")
        
        # Agent action memory
        self.agent_actions: Dict[str, List[Dict]] = {}
    
    def run(self, scenario_name: str, agent_id: str, max_steps: int = 500) -> Dict:
        """Run a training scenario"""
        scenario_methods = {
            'stack_tower': self._stack_tower,
            'sort_colors': self._sort_colors,
            'navigate_course': self._navigate_course,
            'precision_place': self._precision_place,
            'multi_task': self._multi_task,
            'navigate_hallway': self._navigate_hallway,  # NEW
        }
        
        if scenario_name not in scenario_methods:
            return {"error": f"Unknown scenario: {scenario_name}"}
        
        self.logger.info(f"Running {scenario_name} for {agent_id}")
        
        # Initialize agent at starting position
        if scenario_name == 'navigate_hallway':
            start_pos = np.array([19.0, 4.0, 0.5])  # Before doorway
        else:
            start_pos = np.array([5.0, 5.0, 0.5])
        
        self.room.add_agent(agent_id, start_pos)
        self.agent_actions[agent_id] = []
        
        return scenario_methods[scenario_name](agent_id, max_steps)
    
    def _navigate_hallway(self, agent_id: str, max_steps: int) -> Dict:
        """Navigate through doorway, turn, and up steps"""
        agent = self.room.agents[agent_id]
        steps = 0
        success = False
        checkpoints = {
            'doorway_passed': False,
            'turn_made': False,
            'steps_climbed': False,
            'platform_reached': False
        }
        
        while steps < max_steps and not success:
            # Simple navigation logic
            pos = agent.position
            
            # Check checkpoints
            if pos[0] > 20.5 and not checkpoints['doorway_passed']:
                checkpoints['doorway_passed'] = True
                self.logger.info(f"{agent_id}: Passed doorway")
            
            if pos[0] > 26.0 and pos[1] != 5.0 and not checkpoints['turn_made']:
                checkpoints['turn_made'] = True
                self.logger.info(f"{agent_id}: Made turn")
            
            if pos[0] > 27.0 and pos[2] > 0.5 and not checkpoints['steps_climbed']:
                checkpoints['steps_climbed'] = True
                self.logger.info(f"{agent_id}: Climbed steps")
            
            if pos[0] > 28.5 and checkpoints['doorway_passed'] and checkpoints['turn_made'] and checkpoints['steps_climbed']:
                checkpoints['platform_reached'] = True
                success = True
                self.logger.info(f"{agent_id}: Reached platform!")
            
            # Simple movement towards goal
            action = self._decide_action(agent_id, checkpoints)
            self._execute_action(agent_id, action)
            
            self.room.step()
            steps += 1
        
        return {
            'success': success,
            'steps': steps,
            'checkpoints': checkpoints
        }
    
    def _decide_action(self, agent_id: str, checkpoints: Dict) -> Dict:
        """Decide next action based on current state"""
        agent = self.room.agents[agent_id]
        pos = agent.position
        
        if not checkpoints['doorway_passed']:
            # Move towards doorway
            return {'action': 'move', 'delta': [0.1, 0.0, 0.0]}
        elif not checkpoints['turn_made']:
            # Randomly turn left or right
            turn = random.choice(['left', 'right'])
            if turn == 'left':
                return {'action': 'move', 'delta': [0.05, -0.1, 0.0]}
            else:
                return {'action': 'move', 'delta': [0.05, 0.1, 0.0]}
        elif not checkpoints['steps_climbed']:
            # Move up steps
            return {'action': 'move', 'delta': [0.1, 0.0, 0.05]}
        else:
            # Move to platform
            return {'action': 'move', 'delta': [0.1, 0.0, 0.0]}
    
    def _execute_action(self, agent_id: str, action: Dict):
        """Execute agent action"""
        agent = self.room.agents[agent_id]
        
        if action['action'] == 'move':
            agent.position += np.array(action['delta'])
        elif action['action'] == 'grip':
            # Find closest object
            pass
        elif action['action'] == 'release':
            pass
        
        self.agent_actions[agent_id].append(action)
    
    def _stack_tower(self, agent_id: str, max_steps: int) -> Dict:
        """Stack blocks to build a tower"""
        agent = self.room.agents[agent_id]
        steps = 0
        success = False
        
        # Find blocks
        blocks = [obj_id for obj_id, obj in self.room.objects.items() 
                 if obj.obj_type == ObjectType.BLOCK and 'block_' in obj_id]
        
        tower_height = 0
        
        while steps < max_steps and tower_height < 5:
            # Simulate stacking
            if random.random() < 0.3:  # 30% success rate per attempt
                tower_height += 1
            steps += 1
            self.room.step()
        
        success = tower_height >= 3
        return {'success': success, 'steps': steps, 'tower_height': tower_height}
    
    def _sort_colors(self, agent_id: str, max_steps: int) -> Dict:
        """Sort colored items into bins"""
        agent = self.room.agents[agent_id]
        steps = 0
        items_sorted = 0
        
        sort_items = [obj_id for obj_id in self.room.objects.keys() if 'sort_' in obj_id]
        
        for item in sort_items:
            if steps >= max_steps:
                break
            
            # Simulate sorting attempt
            if random.random() < 0.4:
                items_sorted += 1
            
            steps += 10  # Each sort takes time
            self.room.step()
        
        success = items_sorted >= len(sort_items) * 0.5
        return {'success': success, 'steps': steps, 'items_sorted': items_sorted}
    
    def _navigate_course(self, agent_id: str, max_steps: int) -> Dict:
        """Navigate obstacle course"""
        agent = self.room.agents[agent_id]
        steps = 0
        obstacles_cleared = 0
        
        # Obstacles: ramp, stairs, narrow passage
        obstacles = ['ramp_main', 'stair_0', 'passage_wall_1']
        
        for obstacle in obstacles:
            if steps >= max_steps:
                break
            
            # Simulate navigation
            if random.random() < 0.5:
                obstacles_cleared += 1
            
            steps += 20
            self.room.step()
        
        success = obstacles_cleared >= 2
        return {'success': success, 'steps': steps, 'obstacles_cleared': obstacles_cleared}
    
    def _precision_place(self, agent_id: str, max_steps: int) -> Dict:
        """Place small objects precisely"""
        agent = self.room.agents[agent_id]
        steps = 0
        objects_placed = 0
        
        precision_objects = ['small_cube', 'small_sphere']
        
        for obj in precision_objects:
            if steps >= max_steps:
                break
            
            # Precision is harder
            if random.random() < 0.2:
                objects_placed += 1
            
            steps += 15
            self.room.step()
        
        success = objects_placed >= 1
        return {'success': success, 'steps': steps, 'objects_placed': objects_placed}
    
    def _multi_task(self, agent_id: str, max_steps: int) -> Dict:
        """Combined multi-task scenario"""
        # Run sub-scenarios
        results = []
        successes = []
        
        # Stack some blocks
        result = self._stack_tower(agent_id, max_steps // 3)
        results.append(result)
        successes.append(result['success'])
        
        # Sort some items
        result = self._sort_colors(agent_id, max_steps // 3)
        results.append(result)
        successes.append(result['success'])
        
        # Navigate
        result = self._navigate_course(agent_id, max_steps // 3)
        results.append(result)
        successes.append(result['success'])
        
        success = sum(successes) >= 2
        return {'success': success, 'steps': sum([r['steps'] for r in results]), 'sub_tasks': successes}


def main():
    """Demo the expanded physics room"""
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("EXPANDED PHYSICS TRAINING ROOM v2.1")
    print("=" * 70)
    
    # Create room
    room = ExpandedPhysicsRoom()
    scenarios = TrainingScenario(room)
    
    print(f"\nRoom Size: {room.config.size}")
    print(f"Total Objects: {len(room.objects)}")
    print(f"Total Zones: {len(room.zones)}")
    
    print("\nZones:")
    for name, (min_c, max_c) in room.zones.items():
        size = max_c - min_c
        print(f"  {name:12s}: {size[0]:.1f}m x {size[1]:.1f}m x {size[2]:.1f}m")
    
    print("\nObject Counts by Type:")
    type_counts = {}
    for obj in room.objects.values():
        t = obj.obj_type.value
        type_counts[t] = type_counts.get(t, 0) + 1
    for t, count in sorted(type_counts.items()):
        print(f"  {t:12s}: {count}")
    
    print("\n" + "=" * 70)
    print("Running sample training scenarios...")
    print("=" * 70)
    
    # Run sample scenarios
    test_agent = "demo_agent"
    scenario_list = ['stack_tower', 'sort_colors', 'navigate_course', 
                     'precision_place', 'multi_task', 'navigate_hallway']
    
    for scenario in scenario_list:
        print(f"\n{scenario}...")
        result = scenarios.run(scenario, test_agent, max_steps=100)
        status = "✅" if result['success'] else "❌"
        print(f"  {status} Success: {result['success']}, Steps: {result.get('steps', 'N/A')}")
    
    # Save state
    room.save_state("expanded_physics_room_state.json")
    print("\n✅ State saved to expanded_physics_room_state.json")


if __name__ == "__main__":
    main()
