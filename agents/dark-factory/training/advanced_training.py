#!/usr/bin/env python3
"""
Advanced MYL Children Training
Complex locomotion, manipulation, and cooperation
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/training')

from myl_training_system import MYLChild, TrainingOrchestrator, TrainingStage, Experience
import random
import time
import logging
from typing import Dict, List, Tuple
import numpy as np

__version__ = "1.1.0"


class AdvancedTrainingOrchestrator(TrainingOrchestrator):
    """Extended training with advanced tasks"""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("AdvancedTraining")
        
        # Extended curriculum
        self.curriculum.update({
            TrainingStage.WALKER: [
                # Locomotion
                "sprint_running",
                "obstacle_avoidance_simple",
                "obstacle_avoidance_complex",
                "narrow_passage_navigation",
                "climb_over_object",
                "duck_under_barrier",
                
                # Manipulation
                "pick_up_small_object",
                "pick_up_large_object",
                "rotate_object",
                "stack_objects",
                "place_object_precise",
                "grip_force_control",
                
                # Transport
                "carry_object_1m",
                "carry_object_5m",
                "carry_object_10m",
                "transport_fragile",
                "transport_heavy",
            ],
            TrainingStage.EXPERT: [
                # Complex locomotion
                "sprint_with_direction_change",
                "obstacle_course",
                "dynamic_balance",
                "recovery_from_fall",
                "stair_climbing",
                "ramp_traversal",
                "uneven_terrain",
                
                # Complex manipulation
                "tool_use_wrench",
                "tool_use_screwdriver",
                "assembly_task_simple",
                "assembly_task_complex",
                "disassembly",
                "sorting_objects_by_size",
                "sorting_objects_by_weight",
                
                # A-to-B transport
                "move_object_A_to_B_1m",
                "move_object_A_to_B_5m",
                "move_object_A_to_B_10m",
                "move_object_A_to_B_complex_path",
                "move_multiple_objects_sequence",
                
                # Cooperation
                "cooperative_lift_2_agents",
                "cooperative_carry_2_agents",
                "cooperative_assembly",
                "follow_leader",
                "synchronized_movement",
                "division_of_labor_task",
                "rescue_maneuver",
            ]
        })
        
        # Obstacle configurations
        self.obstacles = [
            {'type': 'box', 'size': (0.5, 0.5, 0.5), 'position': (2, 0, 0)},
            {'type': 'wall', 'size': (0.1, 2, 1), 'position': (5, 0, 0)},
            {'type': 'barrier', 'height': 0.3, 'position': (3, 1, 0)},
            {'type': 'gap', 'width': 0.5, 'position': (4, 0, 0)},
        ]
        
        # Transport locations
        self.locations = {
            'A': (0, 0, 0),
            'B': (5, 0, 0),
            'C': (10, 2, 0),
            'D': (7, -3, 0),
        }
    
    def simulate_advanced_task(self, task: str, child: MYLChild) -> Tuple[bool, str]:
        """
        Simulate advanced task execution.
        Returns (success, details)
        """
        success_prob = self._calculate_task_difficulty(task, child)
        success = random.random() < success_prob
        
        details = self._generate_task_details(task, success)
        
        return success, details
    
    def _calculate_task_difficulty(self, task: str, child: MYLChild) -> float:
        """Calculate success probability based on task and child state"""
        base_prob = 0.3
        
        # Stage bonus
        if child.stage == TrainingStage.WALKER:
            base_prob += 0.2
        elif child.stage == TrainingStage.EXPERT:
            base_prob += 0.4
        
        # Confidence bonus
        base_prob += child.confidence * 0.3
        
        # Task-specific modifiers
        if "cooperative" in task:
            # Cooperation tasks need coordination
            if len(self.children) < 2:
                base_prob *= 0.5  # Harder alone
            else:
                base_prob += 0.2  # Easier with partners
        
        if "obstacle" in task or "complex" in task:
            base_prob -= 0.1  # Harder tasks
        
        if "sprint" in task or "running" in task:
            if child.embodiment == "cobra":
                base_prob += 0.15  # COBRA good at running
            elif child.embodiment == "prometheus":
                base_prob -= 0.05  # PROMETHEUS needs more balance
        
        if "manipulation" in task or "tool" in task:
            if child.embodiment == "prometheus":
                base_prob += 0.2  # PROMETHEUS good at manipulation
            elif child.embodiment == "cobra":
                base_prob -= 0.1  # COBRA needs tail skills
        
        return max(0.05, min(0.95, base_prob))
    
    def _generate_task_details(self, task: str, success: bool) -> str:
        """Generate task execution details"""
        if "obstacle" in task:
            if "simple" in task:
                return "Navigated around single obstacle" if success else "Hit obstacle, need better path planning"
            elif "complex" in task:
                return "Successfully threaded through multiple obstacles" if success else "Got stuck in obstacle field"
        
        elif "move_object" in task or "A_to_B" in task:
            distance = task.split('_')[-1].replace('m', '') if 'm' in task else 'unknown'
            return f"Successfully transported object {distance}m" if success else f"Dropped object after {random.randint(1, int(distance))}m"
        
        elif "cooperative" in task:
            if success:
                return "Perfect synchronization with partner"
            else:
                return "Timing mismatch with partner"
        
        elif "sprint" in task or "running" in task:
            return "Reached target velocity" if success else "Lost balance during acceleration"
        
        elif "manipulation" in task or "tool" in task:
            return "Precise grip and placement" if success else "Object slipped from grip"
        
        return "Task executed" if success else "Task failed"
    
    def run_advanced_training_episode(self, child_id: str, task_type: str = "mixed") -> Experience:
        """Run advanced training episode"""
        if child_id not in self.children:
            raise ValueError(f"Child {child_id} not found")
        
        child = self.children[child_id]
        child.total_episodes += 1
        
        # Select task based on type
        if task_type == "locomotion":
            possible_tasks = [t for t in self.curriculum[TrainingStage.WALKER] 
                            if any(k in t for k in ['sprint', 'obstacle', 'climb', 'duck'])]
        elif task_type == "manipulation":
            possible_tasks = [t for t in self.curriculum[TrainingStage.WALKER] 
                            if any(k in t for k in ['pick', 'rotate', 'stack', 'place', 'grip'])]
        elif task_type == "transport":
            possible_tasks = [t for t in self.curriculum[TrainingStage.WALKER] + self.curriculum[TrainingStage.EXPERT]
                            if 'move_object' in t or 'carry' in t or 'transport' in t]
        elif task_type == "cooperation":
            possible_tasks = [t for t in self.curriculum[TrainingStage.EXPERT] 
                            if 'cooperative' in t]
        else:
            # Mixed - appropriate for stage
            if child.stage == TrainingStage.WALKER:
                possible_tasks = self.curriculum[TrainingStage.WALKER]
            else:
                possible_tasks = self.curriculum[TrainingStage.WALKER] + self.curriculum[TrainingStage.EXPERT]
        
        if not possible_tasks:
            possible_tasks = ["free_exploration"]
        
        task = random.choice(possible_tasks)
        
        # Execute task
        success, details = self.simulate_advanced_task(task, child)
        
        # Calculate reward
        if success:
            reward = 0.5 + (child.confidence * 0.3)
            child.successful_episodes += 1
            child.confidence = min(1.0, child.confidence + 0.08)
            child.frustration = max(0.0, child.frustration - 0.15)
        else:
            reward = -0.1
            child.frustration = min(1.0, child.frustration + 0.15)
            child.confidence = max(0.0, child.confidence - 0.03)
        
        # Learn skills
        skills_learned = []
        if success:
            skill_name = f"{child.embodiment}_{task}"
            if skill_name not in child.skills:
                child.skills[skill_name] = type('Skill', (), {
                    'name': skill_name,
                    'embodiment': child.embodiment,
                    'proficiency': 0.25,
                    'learned_at': time.time(),
                    'last_practiced': time.time(),
                    'practice_count': 1
                })()
                skills_learned.append(skill_name)
            else:
                skill = child.skills[skill_name]
                skill.proficiency = min(1.0, skill.proficiency + 0.08)
                skill.practice_count += 1
                skill.last_practiced = time.time()
        
        # Check stage advancement
        if child.successful_episodes >= 20 and child.stage == TrainingStage.CRAWLER:
            child.stage = TrainingStage.WALKER
            self.logger.info(f"🎉 {child_id} advanced to WALKER stage!")
        elif child.successful_episodes >= 50 and len(child.skills) >= 5 and child.stage == TrainingStage.WALKER:
            child.stage = TrainingStage.EXPERT
            self.logger.info(f"🏆 {child_id} advanced to EXPERT stage!")
        
        experience = Experience(
            timestamp=time.time(),
            child_id=child_id,
            embodiment=child.embodiment,
            task=task,
            success=success,
            reward=reward,
            notes=details,
            skills_learned=skills_learned
        )
        
        child.experiences.append(experience)
        
        return experience
    
    def run_cooperative_training(self, task: str, child_ids: List[str]) -> List[Experience]:
        """
        Train multiple children on cooperative task.
        Requires synchronization.
        """
        experiences = []
        
        self.logger.info(f"Cooperative training: {task} with {child_ids}")
        
        # Check all children ready
        for cid in child_ids:
            if cid not in self.children:
                self.logger.error(f"Child {cid} not found")
                return experiences
        
        # Cooperative task execution
        success = True
        base_prob = 0.5
        
        # Each child contributes
        for cid in child_ids:
            child = self.children[cid]
            contribution = child.confidence * 0.3
            base_prob += contribution
        
        # Coordination penalty if not enough practice
        if any(self.children[cid].stage.value == "crawler" for cid in child_ids):
            base_prob *= 0.7  # Harder for crawlers
        
        success = random.random() < min(0.9, base_prob)
        
        # Generate experiences for all
        for cid in child_ids:
            child = self.children[cid]
            child.total_episodes += 1
            
            if success:
                child.successful_episodes += 1
                reward = 0.6  # Higher reward for cooperation
                child.confidence = min(1.0, child.confidence + 0.1)
                notes = f"Successful cooperation on {task}"
            else:
                reward = -0.05  # Lower penalty (shared struggle)
                notes = f"Cooperation difficult on {task}, needs more practice"
            
            exp = Experience(
                timestamp=time.time(),
                child_id=cid,
                embodiment=child.embodiment,
                task=f"cooperative_{task}",
                success=success,
                reward=reward,
                notes=notes,
                skills_learned=[f"{child.embodiment}_cooperative_{task}"] if success else []
            )
            
            child.experiences.append(exp)
            experiences.append(exp)
        
        return experiences
    
    def run_advanced_training_cycle(self, episodes_per_child: int = 20):
        """Run complete advanced training cycle"""
        self.logger.info(f"Starting advanced training: {episodes_per_child} episodes per child")
        
        # Individual training
        for child_id, child in self.children.items():
            self.logger.info(f"Training {child_id} (Stage: {child.stage.value})...")
            
            # Mix of task types based on stage
            task_types = ["locomotion", "manipulation"]
            if child.stage.value in ["walker", "expert"]:
                task_types.append("transport")
            if child.stage.value == "expert":
                task_types.append("cooperation")
            
            for i in range(episodes_per_child):
                task_type = random.choice(task_types)
                exp = self.run_advanced_training_episode(child_id, task_type)
                
                # Log progress
                if (i + 1) % 5 == 0:
                    status = child.get_status()
                    self.logger.info(f"  Progress: {i+1}/{episodes_per_child} | "
                                     f"Stage: {status['stage']} | "
                                     f"Success: {status['success_rate']:.0%} | "
                                     f"Skills: {status['skills']}")
        
        # Cooperative training (if enough expert children)
        expert_children = [cid for cid, c in self.children.items() 
                         if c.stage >= TrainingStage.WALKER]
        
        if len(expert_children) >= 2:
            self.logger.info("Running cooperative training...")
            
            cooperative_tasks = [
                "cooperative_lift",
                "cooperative_carry",
                "division_of_labor",
            ]
            
            for task in cooperative_tasks:
                # Pair up children
                pairs = [(expert_children[i], expert_children[i+1]) 
                        for i in range(0, len(expert_children)-1, 2)]
                
                for pair in pairs:
                    self.run_cooperative_training(task, list(pair))
        
        self.logger.info("Advanced training complete")


def main():
    """Run advanced training"""
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("ADVANCED MYL CHILDREN TRAINING")
    print("Locomotion | Manipulation | Transport | Cooperation")
    print("=" * 70)
    
    # Create orchestrator
    orchestrator = AdvancedTrainingOrchestrator()
    
    # Load existing children if available
    import os
    agents_path = "/root/.openclaw/workspace/AGI_COMPANY/agents"
    existing_children = []
    
    for item in os.listdir(agents_path):
        if item.startswith("myl_") and os.path.isdir(os.path.join(agents_path, item)):
            existing_children.append(item)
    
    if existing_children:
        print(f"\nLoading {len(existing_children)} existing children...")
        for child_id in existing_children:
            # Determine embodiment from ID
            if "cobra" in child_id:
                embodiment = "cobra"
            elif "prometheus" in child_id:
                embodiment = "prometheus"
            else:
                embodiment = "cobra"
            
            orchestrator.spawn_child(child_id, embodiment)
            
            # Advance them to WALKER for advanced training
            child = orchestrator.children[child_id]
            if child.stage == TrainingStage.CRAWLER:
                child.stage = TrainingStage.WALKER
                print(f"  {child_id} advanced to WALKER stage")
    else:
        print("\nSpawning new MYL children...")
        children_config = [
            ("myl_cobra_runner", "cobra"),
            ("myl_cobra_manipulator", "cobra"),
            ("myl_prometheus_transporter", "prometheus"),
            ("myl_prometheus_cooperator", "prometheus"),
            ("myl_dual_expert", "cobra"),
        ]
        
        for child_id, embodiment in children_config:
            orchestrator.spawn_child(child_id, embodiment)
            # Start at WALKER for advanced training
            orchestrator.children[child_id].stage = TrainingStage.WALKER
    
    # Run advanced training
    print("\nStarting advanced training...")
    orchestrator.run_advanced_training_cycle(episodes_per_child=15)
    
    # Save memories
    print("\nSaving memories...")
    import sys
    sys.path.insert(0, '/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/training')
    from myl_training_system import MYLChild
    
    memory_path = "/root/.openclaw/workspace/AGI_COMPANY/agents"
    for child_id, child in orchestrator.children.items():
        child.save_memory(memory_path)
        child.save_daily_log(os.path.join(memory_path, child_id, "memory"))
    
    # Generate report
    print("\n" + "=" * 70)
    print("ADVANCED TRAINING REPORT")
    print("=" * 70)
    report = orchestrator.get_training_report()
    print(report)
    
    # Add skill summary
    print("\n## Skill Summary")
    for child_id, child in orchestrator.children.items():
        print(f"\n### {child_id}")
        print(f"  Stage: {child.stage.value}")
        print(f"  Skills: {len(child.skills)}")
        if child.skills:
            top_skills = sorted(child.skills.values(), 
                              key=lambda s: s.proficiency, reverse=True)[:3]
            for skill in top_skills:
                print(f"    - {skill.name}: {skill.proficiency:.0%}")
    
    print("\n✅ ADVANCED TRAINING COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
