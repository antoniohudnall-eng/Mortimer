#!/usr/bin/env python3
"""
MYL Agent Self-Defense Course
Combines martial arts training with physics room scenarios

Course Structure:
1. Foundation (White Belt) - Physics room basics
2. Technique (Yellow/Green) - Martial arts fundamentals  
3. Application (Blue/Red) - Combat scenarios
4. Mastery (Black) - Full self-defense readiness
"""

import numpy as np
import sys
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import os

sys.path.insert(0, '/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/simulation')
sys.path.insert(0, '/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/training')

from expanded_physics_room_v2 import ExpandedPhysicsRoom, TrainingScenario, ObjectType
from myl_martial_arts import MartialArtsCurriculum, MartialArtsStudent


@dataclass
class Threat:
    """A threat in the physics room"""
    threat_id: str
    threat_type: str  # "charging", "grabbing", "blocking", "ambush"
    position: np.ndarray
    velocity: np.ndarray
    aggression: float  # 0-1
    size: np.ndarray
    
    def distance_to(self, pos: np.ndarray) -> float:
        return np.linalg.norm(self.position - pos)


@dataclass
class DefenseScenario:
    """Self-defense training scenario"""
    name: str
    difficulty: int  # 1-10
    description: str
    threats: List[Threat]
    objectives: List[str]
    recommended_style: str  # taekwondo, taichi, qigong
    time_limit: int  # seconds


class SelfDefenseCourse:
    """
    Complete self-defense curriculum in physics room.
    
    Combines:
    - Physics room navigation
    - Martial arts techniques
    - Situational awareness
    - Combat scenarios
    """
    
    def __init__(self):
        self.room = ExpandedPhysicsRoom()
        self.martial_arts = MartialArtsCurriculum()
        self.scenarios: Dict[str, DefenseScenario] = {}
        self._build_scenarios()
        
    def _build_scenarios(self):
        """Build self-defense training scenarios"""
        
        # LEVEL 1: FOUNDATION (White Belt)
        self.scenarios["evasion_basics"] = DefenseScenario(
            name="Evasion Basics",
            difficulty=1,
            description="Learn to move away from threats using physics room",
            threats=[
                Threat("threat_1", "charging", np.array([22, 2, 0.5]), 
                      np.array([0.1, 0, 0]), 0.3, np.array([0.5, 0.5, 1.8]))
            ],
            objectives=["evade", "reach_safety", "maintain_distance"],
            recommended_style="taichi",
            time_limit=30
        )
        
        self.scenarios["doorway_defense"] = DefenseScenario(
            name="Doorway Defense",
            difficulty=2,
            description="Defend doorway position, use hallways",
            threats=[
                Threat("threat_1", "blocking", np.array([20.5, 4, 0.5]),
                      np.array([0, 0, 0]), 0.4, np.array([0.6, 0.6, 1.8]))
            ],
            objectives=["maintain_position", "use_doorway", "escape_if_needed"],
            recommended_style="taichi",
            time_limit=45
        )
        
        # LEVEL 2: TECHNIQUE (Yellow/Green Belt)
        self.scenarios["stair_defense"] = DefenseScenario(
            name="Stair Defense",
            difficulty=3,
            description="Defend high ground on stairs",
            threats=[
                Threat("threat_1", "charging", np.array([26, 5, 0.5]),
                      np.array([0.05, 0, 0.02]), 0.5, np.array([0.5, 0.5, 1.8]))
            ],
            objectives=["maintain_high_ground", "front_kick_defense", "retreat_upward"],
            recommended_style="taekwondo",
            time_limit=60
        )
        
        self.scenarios["precision_counter"] = DefenseScenario(
            name="Precision Counter",
            difficulty=4,
            description="Use small objects for distraction/counter",
            threats=[
                Threat("threat_1", "grabbing", np.array([3, 15, 0.5]),
                      np.array([0.02, 0.02, 0]), 0.6, np.array([0.5, 0.5, 1.8]))
            ],
            objectives=["grab_object", "throw_distraction", "create_escape"],
            recommended_style="taekwondo",
            time_limit=45
        )
        
        self.scenarios["multiple_threats_basic"] = DefenseScenario(
            name="Multiple Threats - Basic",
            difficulty=5,
            description="Handle two attackers",
            threats=[
                Threat("threat_1", "charging", np.array([5, 5, 0.5]),
                      np.array([0.08, 0, 0]), 0.5, np.array([0.5, 0.5, 1.8])),
                Threat("threat_2", "flanking", np.array([7, 7, 0.5]),
                      np.array([0, 0.08, 0]), 0.4, np.array([0.5, 0.5, 1.8]))
            ],
            objectives=["positioning", "line_up_threats", "escape_corridor"],
            recommended_style="taichi",
            time_limit=90
        )
        
        # LEVEL 3: APPLICATION (Blue/Red Belt)
        self.scenarios["corridor_ambush"] = DefenseScenario(
            name="Corridor Ambush",
            difficulty=6,
            description="Surprise attack in narrow space",
            threats=[
                Threat("threat_1", "ambush", np.array([25, 3, 0.5]),
                      np.array([0.1, 0, 0]), 0.7, np.array([0.5, 0.5, 1.8])),
                Threat("threat_2", "ambush", np.array([25, 7, 0.5]),
                      np.array([0.1, 0, 0]), 0.7, np.array([0.5, 0.5, 1.8]))
            ],
            objectives=["surprise_recovery", "knife_hand_strike", "escape_through_door"],
            recommended_style="taekwondo",
            time_limit=60
        )
        
        self.scenarios["high_ground_siege"] = DefenseScenario(
            name="High Ground Siege",
            difficulty=7,
            description="Defend platform from multiple angles",
            threats=[
                Threat("threat_1", "charging", np.array([28, 3, 1.0]),
                      np.array([0.05, 0, 0]), 0.6, np.array([0.5, 0.5, 1.8])),
                Threat("threat_2", "flanking", np.array([28, 7, 1.0]),
                      np.array([0, -0.05, 0]), 0.6, np.array([0.5, 0.5, 1.8])),
                Threat("threat_3", "blocking", np.array([27, 5, 0.8]),
                      np.array([0, 0, 0]), 0.5, np.array([0.5, 0.5, 1.8]))
            ],
            objectives=["maintain_platform", "round_kick_defense", "side_kick_repulsion"],
            recommended_style="taekwondo",
            time_limit=120
        )
        
        self.scenarios["furniture_defense"] = DefenseScenario(
            name="Furniture Defense",
            difficulty=7,
            description="Use tables/chairs as barriers",
            threats=[
                Threat("threat_1", "charging", np.array([5, 3, 0.5]),
                      np.array([0.1, 0, 0]), 0.8, np.array([0.5, 0.5, 1.8])),
                Threat("threat_2", "charging", np.array([5, 7, 0.5]),
                      np.array([0.1, 0, 0]), 0.8, np.array([0.5, 0.5, 1.8]))
            ],
            objectives=["flip_table", "create_barrier", "escape_while_blocked"],
            recommended_style="taichi",
            time_limit=90
        )
        
        # LEVEL 4: MASTERY (Black Belt)
        self.scenarios["room_clear"] = DefenseScenario(
            name="Room Clear",
            difficulty=8,
            description="Clear multiple hostiles from room",
            threats=[
                Threat("threat_1", "charging", np.array([2, 2, 0.5]),
                      np.array([0.1, 0.1, 0]), 0.8, np.array([0.5, 0.5, 1.8])),
                Threat("threat_2", "flanking", np.array([8, 2, 0.5]),
                      np.array([-0.1, 0.1, 0]), 0.8, np.array([0.5, 0.5, 1.8])),
                Threat("threat_3", "ambush", np.array([5, 8, 0.5]),
                      np.array([0, -0.1, 0]), 0.9, np.array([0.5, 0.5, 1.8]))
            ],
            objectives=["360_awareness", "spin_kick", "continuous_movement", "neutralize_all"],
            recommended_style="taekwondo",
            time_limit=180
        )
        
        self.scenarios["full_house_defense"] = DefenseScenario(
            name="Full House Defense",
            difficulty=10,
            description="Ultimate test: defend entire physics room",
            threats=[
                Threat("t1", "charging", np.array([5, 5, 0.5]), np.array([0.1, 0, 0]), 0.9, np.array([0.5, 0.5, 1.8])),
                Threat("t2", "flanking", np.array([15, 5, 0.5]), np.array([0, 0.1, 0]), 0.8, np.array([0.5, 0.5, 1.8])),
                Threat("t3", "ambush", np.array([25, 5, 0.5]), np.array([0, 0, 0]), 1.0, np.array([0.5, 0.5, 1.8])),
                Threat("t4", "blocking", np.array([5, 15, 0.5]), np.array([0.05, 0.05, 0]), 0.7, np.array([0.5, 0.5, 1.8])),
                Threat("t5", "charging", np.array([15, 15, 0.5]), np.array([-0.1, 0, 0]), 0.9, np.array([0.5, 0.5, 1.8])),
            ],
            objectives=["zone_control", "weaponize_environment", "tornado_kick_finale", "complete_victory"],
            recommended_style="taekwondo",
            time_limit=300
        )
    
    def run_scenario(self, agent_id: str, scenario_name: str, 
                     martial_student: MartialArtsStudent) -> Dict:
        """Run a self-defense scenario"""
        if scenario_name not in self.scenarios:
            return {"error": f"Unknown scenario: {scenario_name}"}
        
        scenario = self.scenarios[scenario_name]
        print(f"\n{'='*70}")
        print(f"SCENARIO: {scenario.name}")
        print(f"Difficulty: {'★'*scenario.difficulty}{'☆'*(10-scenario.difficulty)}")
        print(f"Description: {scenario.description}")
        print(f"Style: {scenario.recommended_style}")
        print(f"Time Limit: {scenario.time_limit}s")
        print(f"{'='*70}")
        
        # Initialize agent in room
        agent_pos = np.array([5.0, 5.0, 0.5])  # Start in play area
        
        # Run simulation
        steps = 0
        max_steps = scenario.time_limit * 20  # 50ms per step
        
        results = {
            "agent_id": agent_id,
            "scenario": scenario_name,
            "difficulty": scenario.difficulty,
            "threats_neutralized": 0,
            "objectives_completed": [],
            "techniques_used": [],
            "belt_achieved": "White",
            "survived": False
        }
        
        while steps < max_steps:
            # Update threat positions
            for threat in scenario.threats:
                threat.position += threat.velocity
                # Keep in bounds
                threat.position = np.clip(threat.position, [0, 0, 0], [30, 30, 5])
            
            # Agent decision
            action = self._defense_decision(agent_pos, scenario.threats, 
                                           martial_student, scenario)
            
            # Execute action
            if action.get("type") == "movement":
                agent_pos += np.array(action.get("delta", [0, 0, 0]))
            elif action.get("type") == "technique":
                tech = action.get("technique")
                results["techniques_used"].append(tech)
                
                # Check if technique neutralizes threat
                for threat in scenario.threats:
                    if threat.distance_to(agent_pos) < 1.5:
                        results["threats_neutralized"] += 1
                        scenario.threats.remove(threat)
                        break
            
            # Check win condition
            if len(scenario.threats) == 0:
                results["survived"] = True
                results["objectives_completed"] = scenario.objectives
                break
            
            # Check fail condition (caught by threat)
            for threat in scenario.threats:
                if threat.distance_to(agent_pos) < 0.5:
                    results["survived"] = False
                    break
            
            if not results.get("survived", True) and len(scenario.threats) > 0:
                break
            
            steps += 1
        
        # Calculate belt based on performance
        if results["survived"]:
            success_rate = results["threats_neutralized"] / max(1, len(scenario.threats) + results["threats_neutralized"])
            
            if scenario.difficulty >= 8 and success_rate > 0.8:
                results["belt_achieved"] = "Black"
            elif scenario.difficulty >= 6 and success_rate > 0.7:
                results["belt_achieved"] = "Red"
            elif scenario.difficulty >= 4 and success_rate > 0.6:
                results["belt_achieved"] = "Blue"
            elif scenario.difficulty >= 2 and success_rate > 0.5:
                results["belt_achieved"] = "Green"
            else:
                results["belt_achieved"] = "Yellow"
        
        # Award martial arts progress
        if results["survived"]:
            moves_to_learn = self._get_scenario_moves(scenario)
            for move in moves_to_learn:
                if move not in martial_student.learned_movements:
                    martial_student.practice_movement(move)
        
        return results
    
    def _defense_decision(self, agent_pos: np.ndarray, threats: List[Threat],
                          student: MartialArtsStudent, scenario: DefenseScenario) -> Dict:
        """Agent makes defense decision"""
        
        # Find closest threat
        if not threats:
            return {"type": "movement", "delta": [0.05, 0, 0]}
        
        closest = min(threats, key=lambda t: t.distance_to(agent_pos))
        dist = closest.distance_to(agent_pos)
        
        # If very close, attempt technique
        if dist < 1.5:
            # Basic strikes always available
            basic_strikes = ["jab", "cross", "front_kick", "low_block"]
            return {"type": "technique", "technique": random.choice(basic_strikes)}
        
        # Move away from threat
        away_dir = agent_pos - closest.position
        if np.linalg.norm(away_dir) > 0.01:
            away_dir = away_dir / np.linalg.norm(away_dir) * 0.15
        else:
            away_dir = np.array([0.1, 0.1, 0])
        
        return {"type": "movement", "delta": away_dir.tolist()}
    
    def _get_scenario_moves(self, scenario: DefenseScenario) -> List[str]:
        """Get moves learned from completing scenario"""
        moves = []
        
        if scenario.difficulty == 1:
            moves = ["natural_breathing", "preparation", "walking_stance"]
        elif scenario.difficulty == 2:
            moves = ["horse_stance", "jab", "low_block"]
        elif scenario.difficulty == 3:
            moves = ["front_kick", "middle_block", "walking_stance"]
        elif scenario.difficulty == 4:
            moves = ["cross", "hook", "high_block"]
        elif scenario.difficulty == 5:
            moves = ["round_kick", "knife_hand", "ward_off"]
        elif scenario.difficulty == 6:
            moves = ["side_kick", "uppercut", "roll_back"]
        elif scenario.difficulty == 7:
            moves = ["hook_kick", "back_fist", "press"]
        elif scenario.difficulty == 8:
            moves = ["axe_kick", "spin_kick", "push"]
        elif scenario.difficulty == 10:
            moves = ["360_kick", "tornado_kick", "closure"]
        
        return moves
    
    def run_full_course(self, agent_id: str) -> Dict:
        """Run complete self-defense course for an agent"""
        print(f"\n{'='*70}")
        print(f"SELF-DEFENSE COURSE FOR: {agent_id}")
        print(f"{'='*70}")
        
        student = MartialArtsStudent(agent_id, "humanoid")
        
        # Run scenarios in difficulty order
        scenario_order = [
            "evasion_basics",      # White
            "doorway_defense",      # White
            "stair_defense",        # Yellow
            "precision_counter",    # Yellow
            "multiple_threats_basic", # Green
            "corridor_ambush",      # Blue
            "high_ground_siege",    # Red
            "furniture_defense",    # Red
            "room_clear",           # Black
            "full_house_defense"    # Black
        ]
        
        results = []
        highest_belt = "White"
        
        for scenario_name in scenario_order:
            result = self.run_scenario(agent_id, scenario_name, student)
            results.append(result)
            
            if result.get("survived", False):
                belt = result.get("belt_achieved", "White")
                if self._belt_rank(belt) > self._belt_rank(highest_belt):
                    highest_belt = belt
                print(f"  ✅ PASSED - Achieved {belt} Belt")
            else:
                print(f"  ❌ FAILED - Retry required")
        
        # Final report
        passed = sum(1 for r in results if r.get("survived", False))
        
        print(f"\n{'='*70}")
        print(f"COURSE COMPLETE")
        print(f"{'='*70}")
        print(f"Scenarios Passed: {passed}/{len(scenario_order)}")
        print(f"Final Belt: {highest_belt}")
        print(f"Movements Learned: {len(student.learned_movements)}")
        print(f"Martial Arts Stats:")
        print(f"  Power: {student.power:.2f}")
        print(f"  Balance: {student.balance:.2f}")
        print(f"  Flow: {student.flow:.2f}")
        print(f"  Chi: {student.chi:.2f}")
        
        # Save progress
        student.save_progress()
        
        return {
            "agent_id": agent_id,
            "scenarios_completed": passed,
            "total_scenarios": len(scenario_order),
            "final_belt": highest_belt,
            "movements_learned": len(student.learned_movements),
            "stats": {
                "power": student.power,
                "balance": student.balance,
                "flow": student.flow,
                "chi": student.chi
            }
        }
    
    def _belt_rank(self, belt: str) -> int:
        """Get numeric rank for belt"""
        ranks = {
            "White": 0,
            "Yellow": 1,
            "Green": 2,
            "Blue": 3,
            "Red": 4,
            "Black": 5
        }
        return ranks.get(belt, 0)


def main():
    """Run self-defense course"""
    print("=" * 70)
    print("MYL AGENT SELF-DEFENSE COURSE")
    print("Physics Room + Martial Arts Integration")
    print("=" * 70)
    
    course = SelfDefenseCourse()
    
    # Show curriculum
    print("\nCOURSE CURRICULUM:")
    print("=" * 70)
    
    scenarios_by_level = {
        "Level 1 (White Belt)": ["evasion_basics", "doorway_defense"],
        "Level 2 (Yellow Belt)": ["stair_defense", "precision_counter"],
        "Level 3 (Green Belt)": ["multiple_threats_basic"],
        "Level 4 (Blue Belt)": ["corridor_ambush"],
        "Level 5 (Red Belt)": ["high_ground_siege", "furniture_defense"],
        "Level 6 (Black Belt)": ["room_clear", "full_house_defense"]
    }
    
    for level, scenarios in scenarios_by_level.items():
        print(f"\n{level}:")
        for s_name in scenarios:
            s = course.scenarios[s_name]
            print(f"  • {s.name} (★{'★' * (s.difficulty-1)})")
    
    # Run demo with one agent
    print("\n" + "=" * 70)
    print("RUNNING DEMO: mylzeron")
    print("=" * 70)
    
    result = course.run_full_course("mylzeron")
    
    print("\n" + "=" * 70)
    print("SELF-DEFENSE COURSE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
