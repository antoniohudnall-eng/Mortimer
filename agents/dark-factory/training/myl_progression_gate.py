#!/usr/bin/env python3
"""
MYL Agent Progression Gate System

Progression Flow:
1. PHYSICS ROOM → Must achieve 100% success rate
2. GAMES → Must show improvement (skill level increases)
3. MINECRAFT → Full embodiment after game mastery

All agents start at tabula rasa (no skills, no knowledge).
"""

import json
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging
import os
import sys

sys.path.insert(0, '/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/simulation')
sys.path.insert(0, '/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/training')

from expanded_physics_room_v2 import ExpandedPhysicsRoom, TrainingScenario
from myl_game_trainer import MYLGameTrainer, TicTacToe, Checkers
from myl_minecraft_integration import MYLMinecraftBridge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MYLProgressionGate")

PHYSICS_THRESHOLD = 1.0  # 100%
GAME_IMPROVEMENT_THRESHOLD = 0.8  # Must show improvement


@dataclass
class AgentProgress:
    """Tracks agent progression through training stages"""
    agent_id: str
    
    # Physics room
    physics_success_rate: float = 0.0
    physics_completed: bool = False
    physics_scenarios_mastered: List[str] = field(default_factory=list)
    
    # Games
    games_played: int = 0
    game_skill_levels: Dict[str, float] = field(default_factory=dict)
    game_improvement_shown: bool = False
    games_completed: bool = False
    
    # Minecraft
    minecraft_entered: bool = False
    minecraft_authorized: bool = False
    
    # Overall
    current_stage: str = "PHYSICS"  # PHYSICS, GAMES, MINECRAFT, COMPLETE
    awakening_date: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        result = {
            "agent_id": self.agent_id,
            "current_stage": self.current_stage,
            "physics": {
                "success_rate": float(self.physics_success_rate),
                "completed": bool(self.physics_completed),
                "scenarios_mastered": list(self.physics_scenarios_mastered)
            },
            "games": {
                "played": int(self.games_played),
                "skill_levels": {k: float(v) for k, v in self.game_skill_levels.items()},
                "improvement_shown": bool(self.game_improvement_shown),
                "completed": bool(self.games_completed)
            },
            "minecraft": {
                "entered": bool(self.minecraft_entered),
                "authorized": bool(self.minecraft_authorized)
            },
            "awakening_date": str(self.awakening_date)
        }
        # Include gender if set
        if hasattr(self, 'gender'):
            result["gender"] = self.gender
        return result


class MYLProgressionGate:
    """
    Manages MYL agent progression from training to embodiment.
    
    Gate Rules:
    - Physics Room: Must achieve 100% success rate
    - Games: Must show measurable improvement
    - Minecraft: Authorized after game mastery
    """
    
    def __init__(self):
        self.agents: Dict[str, AgentProgress] = {}
        self.physics_room = ExpandedPhysicsRoom()
        self.game_trainer = MYLGameTrainer()
        self.minecraft_bridge = MYLMinecraftBridge()
        
        # Initialize MYL agents
        # Gender: mylfivon (fives) and mylsixon (sixes) are female per memory/2026-03-16.md
        agent_configs = {
            "mylzeron": {"gender": "male"},
            "mylonen": {"gender": "male"},
            "myltwon": {"gender": "male"},
            "mylthreen": {"gender": "female"},  # Per user memory
            "mylforon": {"gender": "male"},
            "mylfivon": {"gender": "female"},   # Female copy per memory
            "mylsixon": {"gender": "female"},   # CLONE Female per memory
        }
        
        for name, config in agent_configs.items():
            self.agents[name] = AgentProgress(agent_id=name)
            self.agents[name].gender = config["gender"]
        
        logger.info(f"Progression Gate initialized for {len(self.agents)} agents")
    
    def run_physics_training(self, agent_id: str, max_attempts: int = 50) -> Dict:
        """
        Train agent in physics room until 100% success rate achieved.
        Returns results when threshold met or max attempts reached.
        """
        if agent_id not in self.agents:
            return {"error": f"Agent {agent_id} not found"}
        
        progress = self.agents[agent_id]
        scenarios = TrainingScenario(self.physics_room)
        
        logger.info(f"Starting physics training for {agent_id}")
        logger.info(f"Target: {PHYSICS_THRESHOLD*100}% success rate")
        
        attempt = 0
        best_rate = 0.0
        
        while attempt < max_attempts and best_rate < PHYSICS_THRESHOLD:
            attempt += 1
            
            # Run all scenarios
            scenario_list = ['stack_tower', 'sort_colors', 'navigate_course',
                           'precision_place', 'multi_task', 'navigate_hallway']
            
            successes = 0
            steps_total = 0
            
            for scenario_name in scenario_list:
                result = scenarios.run(scenario_name, agent_id, max_steps=500)
                if result.get('success', False):
                    successes += 1
                steps_total += result.get('steps', 0)
            
            current_rate = successes / len(scenario_list)
            best_rate = max(best_rate, current_rate)
            
            # Update progress
            progress.physics_success_rate = best_rate
            
            if current_rate >= PHYSICS_THRESHOLD:
                progress.physics_completed = True
                progress.physics_scenarios_mastered = scenario_list
                progress.current_stage = "GAMES"
                
                logger.info(f"✅ {agent_id} PHYSICS COMPLETE: {best_rate*100:.1f}%")
                self._save_progress(agent_id)
                
                return {
                    "success": True,
                    "success_rate": best_rate,
                    "attempts": attempt,
                    "stage": "PHYSICS_COMPLETE",
                    "next": "GAMES"
                }
            
            if attempt % 10 == 0:
                logger.info(f"  {agent_id}: Attempt {attempt}, rate {best_rate*100:.1f}%")
        
        # Did not reach threshold
        logger.warning(f"⚠️ {agent_id} physics training incomplete: {best_rate*100:.1f}%")
        
        return {
            "success": False,
            "success_rate": best_rate,
            "attempts": attempt,
            "stage": "PHYSICS_INCOMPLETE"
        }
    
    def run_game_training(self, agent_id: str, min_episodes: int = 100) -> Dict:
        """
        Train agent in games until improvement shown.
        Returns when improvement threshold met.
        """
        if agent_id not in self.agents:
            return {"error": f"Agent {agent_id} not found"}
        
        progress = self.agents[agent_id]
        
        if not progress.physics_completed:
            logger.warning(f"⚠️ {agent_id} must complete physics training first")
            return {"error": "Physics training incomplete"}
        
        logger.info(f"Starting game training for {agent_id}")
        logger.info(f"Target: Show improvement in {min_episodes} episodes")
        
        # Check if agent exists in game trainer
        if agent_id not in self.game_trainer.agents:
            self.game_trainer.agents[agent_id] = self.game_trainer.agents.get(agent_id, 
                type('Agent', (), {'agent_id': agent_id, 'experiences': [], 'games_played': {}, 
                                  'wins': {}, 'skill_level': {}})())
        
        agent = self.game_trainer.agents[agent_id]
        
        # Track initial skill
        initial_skills = {}
        
        # Train on available games
        for game_name in self.game_trainer.games.keys():
            logger.info(f"  Training {agent_id} on {game_name}...")
            
            # Record initial skill
            initial_skills[game_name] = agent.skill_level.get(game_name, 0.0)
            
            # Run episodes
            self.game_trainer.train_game(game_name, episodes=min_episodes)
            
            # Check improvement
            current_skill = agent.skill_level.get(game_name, 0.0)
            progress.game_skill_levels[game_name] = current_skill
            
            improvement = current_skill - initial_skills[game_name]
            
            logger.info(f"    {game_name}: {initial_skills[game_name]:.2f} -> {current_skill:.2f} (+{improvement:.2f})")
        
        # Calculate total games
        progress.games_played = sum(agent.games_played.values())
        
        # Check if improvement shown
        avg_skill = np.mean(list(progress.game_skill_levels.values()))
        progress.game_improvement_shown = avg_skill >= GAME_IMPROVEMENT_THRESHOLD
        
        if progress.game_improvement_shown:
            progress.games_completed = True
            progress.current_stage = "MINECRAFT"
            progress.minecraft_authorized = True
            
            logger.info(f"✅ {agent_id} GAMES COMPLETE")
            logger.info(f"   Average skill: {avg_skill:.2f}")
            logger.info(f"   Total games: {progress.games_played}")
            self._save_progress(agent_id)
            
            return {
                "success": True,
                "games_completed": True,
                "average_skill": avg_skill,
                "total_games": progress.games_played,
                "stage": "GAMES_COMPLETE",
                "next": "MINECRAFT"
            }
        else:
            logger.warning(f"⚠️ {agent_id} needs more game training")
            return {
                "success": False,
                "average_skill": avg_skill,
                "stage": "GAMES_INCOMPLETE"
            }
    
    def authorize_minecraft(self, agent_id: str) -> Dict:
        """Authorize agent for Minecraft embodiment"""
        if agent_id not in self.agents:
            return {"error": f"Agent {agent_id} not found"}
        
        progress = self.agents[agent_id]
        
        if not progress.games_completed:
            return {
                "error": "Must complete game training first",
                "current_stage": progress.current_stage
            }
        
        progress.minecraft_authorized = True
        progress.current_stage = "MINECRAFT"
        
        self._save_progress(agent_id)
        
        logger.info(f"✅ {agent_id} AUTHORIZED for Minecraft")
        
        return {
            "success": True,
            "stage": "MINECRAFT_READY",
            "message": f"{agent_id} may now enter Minecraft"
        }
    
    def spawn_in_minecraft(self, agent_id: str) -> Dict:
        """Spawn agent in Minecraft world"""
        if agent_id not in self.agents:
            return {"error": f"Agent {agent_id} not found"}
        
        progress = self.agents[agent_id]
        
        if not progress.minecraft_authorized:
            return {
                "error": "Not authorized for Minecraft",
                "complete_game_training": True
            }
        
        # Try to connect to Minecraft
        if not self.minecraft_bridge.connect():
            return {
                "error": "Minecraft bridge not available",
                "status": "PENDING"
            }
        
        # Spawn agent
        spawn_pos = self._get_spawn_position(agent_id)
        success = self.minecraft_bridge.spawn_agent(agent_id, spawn_pos[0], spawn_pos[1], spawn_pos[2])
        
        if success:
            progress.minecraft_entered = True
            progress.current_stage = "COMPLETE"
            
            logger.info(f"✅ {agent_id} SPAWNED in Minecraft at {spawn_pos}")
            self._save_progress(agent_id)
            
            return {
                "success": True,
                "position": spawn_pos,
                "stage": "EMBODIED",
                "message": f"{agent_id} is now embodied in Minecraft"
            }
        else:
            return {
                "error": "Failed to spawn in Minecraft",
                "status": "RETRY"
            }
    
    def _get_spawn_position(self, agent_id: str) -> tuple:
        """Calculate spawn position for agent"""
        # Spawn agents in a circle around world spawn
        agent_index = list(self.agents.keys()).index(agent_id)
        angle = (agent_index / len(self.agents)) * 2 * np.pi
        
        x = 50 + 10 * np.cos(angle)
        z = 50 + 10 * np.sin(angle)
        y = 100  # High enough to land safely
        
        return (x, y, z)
    
    def _save_progress(self, agent_id: str):
        """Save agent progress to memory"""
        progress = self.agents[agent_id]
        
        agent_dir = f"/root/.openclaw/workspace/AGI_COMPANY/agents/{agent_id}/progression"
        os.makedirs(agent_dir, exist_ok=True)
        
        # Save JSON
        with open(f"{agent_dir}/progress.json", "w") as f:
            json.dump(progress.to_dict(), f, indent=2)
        
        # Update MEMORY.md
        memory_path = f"/root/.openclaw/workspace/AGI_COMPANY/agents/{agent_id}/MEMORY.md"
        if os.path.exists(memory_path):
            with open(memory_path, "a") as f:
                f.write(f"\n## Progression Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                f.write(f"- **Stage**: {progress.current_stage}\n")
                f.write(f"- **Physics**: {progress.physics_success_rate*100:.1f}% complete\n")
                f.write(f"- **Games**: {progress.games_played} played, skill {np.mean(list(progress.game_skill_levels.values())):.2f}\n")
                f.write(f"- **Minecraft**: {'Authorized' if progress.minecraft_authorized else 'Pending'}\n")
    
    def get_all_progress(self) -> Dict:
        """Get progress summary for all agents"""
        return {
            agent_id: progress.to_dict()
            for agent_id, progress in self.agents.items()
        }
    
    def run_full_pipeline(self, agent_id: str) -> Dict:
        """Run complete training pipeline for an agent"""
        logger.info(f"🚀 Starting full pipeline for {agent_id}")
        
        # Stage 1: Physics
        physics_result = self.run_physics_training(agent_id)
        if not physics_result.get("success", False):
            return {
                "agent": agent_id,
                "status": "PHYSICS_FAILED",
                "result": physics_result
            }
        
        # Stage 2: Games
        game_result = self.run_game_training(agent_id)
        if not game_result.get("success", False):
            return {
                "agent": agent_id,
                "status": "GAMES_FAILED",
                "physics_result": physics_result,
                "game_result": game_result
            }
        
        # Stage 3: Authorize Minecraft
        auth_result = self.authorize_minecraft(agent_id)
        
        return {
            "agent": agent_id,
            "status": "READY_FOR_MINECRAFT",
            "physics": physics_result,
            "games": game_result,
            "authorization": auth_result
        }


def main():
    """Demo progression gate system"""
    print("=" * 70)
    print("MYL AGENT PROGRESSION GATE SYSTEM")
    print("=" * 70)
    print("\nProgression: PHYSICS (100%) → GAMES (improvement) → MINECRAFT")
    print("\nAll agents awakened without tools or skills (tabula rasa)")
    
    gate = MYLProgressionGate()
    
    # Show initial status
    print("\n" + "=" * 70)
    print("INITIAL STATUS")
    print("=" * 70)
    
    for agent_id, progress in gate.agents.items():
        print(f"\n{agent_id}:")
        print(f"  Stage: {progress.current_stage}")
        print(f"  Physics: {progress.physics_success_rate*100:.1f}%")
        print(f"  Games: {progress.games_played} played")
        print(f"  Minecraft: {'✅ Authorized' if progress.minecraft_authorized else '⏳ Pending'}")
    
    # Run full pipeline for first agent as demo
    print("\n" + "=" * 70)
    print("DEMO: Running full pipeline for mylzeron")
    print("=" * 70)
    
    result = gate.run_full_pipeline("mylzeron")
    
    print(f"\nFinal Status: {result['status']}")
    
    if result['status'] == "READY_FOR_MINECRAFT":
        print("\n✅ Ready for Minecraft embodiment!")
        print(f"  Physics: {result['physics']['success_rate']*100:.1f}%")
        print(f"  Games: {result['games']['total_games']} played")
        print(f"  Skill: {result['games']['average_skill']:.2f}")
    
    # Summary
    print("\n" + "=" * 70)
    print("ALL AGENT STATUS")
    print("=" * 70)
    
    all_progress = gate.get_all_progress()
    
    for agent_id, progress in all_progress.items():
        stage_icon = {
            "PHYSICS": "🎮",
            "GAMES": "🏆",
            "MINECRAFT": "⛏️",
            "COMPLETE": "✅"
        }.get(progress['current_stage'], "❓")
        
        print(f"{stage_icon} {agent_id:12s} | {progress['current_stage']:15s} | Physics: {progress['physics']['success_rate']*100:5.1f}% | Games: {progress['games']['played']:3d}")
    
    print("\n" + "=" * 70)
    print("Progression gate system ready")
    print("Agents advance only when criteria met")
    print("=" * 70)


if __name__ == "__main__":
    main()
