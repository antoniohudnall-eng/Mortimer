#!/usr/bin/env python3
"""
MYL Agent Martial Arts Training System

Teaches MYL agents self-defense and body awareness:
- Tae Kwon Do: Striking, kicking, discipline
- Tai Chi: Balance, flow, energy movement
- Qi Gong: Breathing, vitality, internal energy

For embodied agents (COBRA/PROMETHEUS/MYL series)
"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime
import json
import os

@dataclass
class Movement:
    """A martial arts movement"""
    name: str
    style: str  # taekwondo, taichi, qigong
    difficulty: int  # 1-10
    energy_cost: float  # 0-1
    power: float  # 0-1, damage potential
    balance: float  # 0-1, stability requirement
    flow: float  # 0-1, transition smoothness
    
    # Body parts used
    stance: str  # "horse", "cat", "crane", "bow", etc.
    primary_limb: str  # "right_kick", "left_punch", "breath", etc.
    
    # Sequence
    prerequisites: List[str] = None
    followups: List[str] = None
    
    def __post_init__(self):
        if self.prerequisites is None:
            self.prerequisites = []
        if self.followups is None:
            self.followups = []


class MartialArtsCurriculum:
    """
    Complete martial arts training for embodied agents.
    
    Three disciplines:
    - Tae Kwon Do: External power, striking
    - Tai Chi: Internal energy, balance
    - Qi Gong: Breathing, vitality
    """
    
    def __init__(self):
        self.movements: Dict[str, Movement] = {}
        self._build_curriculum()
        
    def _build_curriculum(self):
        """Build complete martial arts curriculum"""
        
        # === TAE KWON DO (Korean striking art) ===
        taekwondo_moves = [
            # Basics
            Movement("horse_stance", "taekwondo", 1, 0.1, 0.0, 0.8, 0.3, 
                    "horse", "balance", [], ["punch", "block"]),
            Movement("walking_stance", "taekwondo", 1, 0.2, 0.0, 0.6, 0.5,
                    "walking", "transition", [], ["jab", "cross"]),
            
            # Hand strikes
            Movement("jab", "taekwondo", 2, 0.2, 0.3, 0.5, 0.6,
                    "walking", "left_punch", ["walking_stance"], ["cross", "hook"]),
            Movement("cross", "taekwondo", 2, 0.3, 0.5, 0.5, 0.6,
                    "walking", "right_punch", ["walking_stance"], ["hook", "uppercut"]),
            Movement("hook", "taekwondo", 3, 0.3, 0.6, 0.4, 0.5,
                    "walking", "right_hook", ["cross"], ["uppercut"]),
            Movement("uppercut", "taekwondo", 3, 0.3, 0.7, 0.3, 0.4,
                    "horse", "right_uppercut", ["hook"], ["back_fist"]),
            Movement("back_fist", "taekwondo", 4, 0.3, 0.5, 0.5, 0.7,
                    "walking", "back_fist", ["uppercut"], ["ridge_hand"]),
            
            # Blocks
            Movement("low_block", "taekwondo", 2, 0.2, 0.1, 0.7, 0.6,
                    "horse", "left_block", ["horse_stance"], ["middle_block", "high_block"]),
            Movement("middle_block", "taekwondo", 3, 0.2, 0.2, 0.7, 0.7,
                    "horse", "left_block", ["low_block"], ["high_block", "knife_hand"]),
            Movement("high_block", "taekwondo", 3, 0.2, 0.2, 0.8, 0.7,
                    "horse", "left_block", ["middle_block"], ["knife_hand"]),
            Movement("knife_hand", "taekwondo", 4, 0.3, 0.5, 0.6, 0.8,
                    "horse", "right_strike", ["high_block"], ["ridge_hand"]),
            
            # Kicks (TKD signature)
            Movement("front_kick", "taekwondo", 3, 0.4, 0.6, 0.4, 0.5,
                    "walking", "right_kick", ["walking_stance"], ["round_kick", "side_kick"]),
            Movement("round_kick", "taekwondo", 4, 0.5, 0.8, 0.3, 0.4,
                    "cat", "right_kick", ["front_kick"], ["hook_kick", "side_kick"]),
            Movement("side_kick", "taekwondo", 5, 0.5, 0.9, 0.3, 0.3,
                    "cat", "right_kick", ["front_kick"], ["hook_kick", "back_kick"]),
            Movement("hook_kick", "taekwondo", 6, 0.5, 0.8, 0.2, 0.4,
                    "cat", "right_kick", ["round_kick"], ["axe_kick", "crescent_kick"]),
            Movement("axe_kick", "taekwondo", 7, 0.6, 1.0, 0.1, 0.3,
                    "crane", "right_kick", ["hook_kick"], ["spin_kick"]),
            Movement("spin_kick", "taekwondo", 8, 0.7, 1.0, 0.1, 0.2,
                    "cat", "spinning_kick", ["axe_kick"], ["360_kick", "tornado_kick"]),
            Movement("360_kick", "taekwondo", 9, 0.8, 1.0, 0.0, 0.1,
                    "cat", "spinning_kick", ["spin_kick"], ["540_kick"]),
            Movement("tornado_kick", "taekwondo", 10, 0.9, 1.0, 0.0, 0.1,
                    "cat", "jumping_spin", ["360_kick"], []),
        ]
        
        # === TAI CHI (Chinese internal art) ===
        taichi_moves = [
            # Opening
            Movement("preparation", "taichi", 1, 0.05, 0.0, 0.9, 0.9,
                    "horse", "breath", [], ["commencement"]),
            Movement("commencement", "taichi", 1, 0.1, 0.0, 0.9, 0.9,
                    "horse", "rising_hands", ["preparation"], ["ward_off"]),
            
            # Grasp Sparrow's Tail
            Movement("ward_off", "taichi", 2, 0.1, 0.1, 0.9, 0.9,
                    "bow", "right_arm", ["commencement"], ["roll_back", "press"]),
            Movement("roll_back", "taichi", 2, 0.1, 0.1, 0.9, 0.9,
                    "empty", "left_arm", ["ward_off"], ["press", "push"]),
            Movement("press", "taichi", 3, 0.1, 0.2, 0.8, 0.9,
                    "bow", "both_arms", ["roll_back"], ["push", "single_whip"]),
            Movement("push", "taichi", 3, 0.1, 0.3, 0.8, 0.9,
                    "bow", "both_arms", ["press"], ["single_whip", "apparent_closure"]),
            
            # Single Whip
            Movement("single_whip", "taichi", 4, 0.15, 0.3, 0.8, 0.9,
                    "cat", "hook_hand", ["push"], ["lift_hands", "play_guitar"]),
            Movement("lift_hands", "taichi", 4, 0.1, 0.1, 0.8, 0.9,
                    "empty", "rising_hands", ["single_whip"], ["shoulder_strike", "white_crane"]),
            
            # White Crane Spreads Wings
            Movement("white_crane", "taichi", 5, 0.15, 0.2, 0.9, 0.95,
                    "cat", "opening_arms", ["lift_hands"], ["brush_knee", "deflect_down"]),
            
            # Brush Knee
            Movement("brush_knee", "taichi", 5, 0.15, 0.3, 0.7, 0.9,
                    "bow", "pushing_palm", ["white_crane"], ["play_guitar", "step_parries"]),
            Movement("play_guitar", "taichi", 6, 0.1, 0.1, 0.8, 0.9,
                    "cat", "holding_ball", ["brush_knee"], ["parry_punch", "part_wild_horse"]),
            
            # Part Wild Horse's Mane
            Movement("part_wild_horse", "taichi", 6, 0.2, 0.4, 0.6, 0.85,
                    "bow", "separating", ["play_guitar"], ["fair_lady", "cloud_hands"]),
            
            # Fair Lady Works at Shuttles
            Movement("fair_lady", "taichi", 7, 0.2, 0.3, 0.7, 0.9,
                    "bow", "palm_change", ["part_wild_horse"], ["cloud_hands", "high_pat"]),
            
            # Cloud Hands
            Movement("cloud_hands", "taichi", 7, 0.15, 0.2, 0.9, 0.95,
                    "horse", "flowing_hands", ["fair_lady"], ["single_whip", "snake_creeps"]),
            
            # Snake Creeps Down
            Movement("snake_creeps", "taichi", 8, 0.2, 0.4, 0.5, 0.8,
                    "low", "sinking", ["cloud_hands"], ["golden_rooster", "needles_sea"]),
            Movement("golden_rooster", "taichi", 9, 0.25, 0.5, 0.3, 0.7,
                    "one_leg", "standing", ["snake_creeps"], ["fan_back", "closure"]),
            
            # Closing
            Movement("closure", "taichi", 1, 0.1, 0.0, 0.9, 0.9,
                    "horse", "gathering", ["golden_rooster"], []),
        ]
        
        # === QI GONG (Energy cultivation) ===
        qigong_moves = [
            # Breathing
            Movement("natural_breathing", "qigong", 1, 0.0, 0.0, 1.0, 1.0,
                    "natural", "breath", [], ["abdominal_breathing", "reverse_breathing"]),
            Movement("abdominal_breathing", "qigong", 2, 0.0, 0.0, 1.0, 1.0,
                    "natural", "deep_belly", ["natural_breathing"], ["reverse_breathing", "holding"]),
            Movement("reverse_breathing", "qigong", 3, 0.0, 0.0, 1.0, 0.9,
                    "natural", "contract_inhale", ["abdominal_breathing"], ["holding", "circulation"]),
            Movement("holding", "qigong", 4, 0.0, 0.0, 1.0, 0.8,
                    "natural", "breath_retention", ["reverse_breathing"], ["circulation", "purging"]),
            
            # Energy circulation
            Movement("circulation", "qigong", 5, 0.1, 0.0, 0.9, 0.95,
                    "horse", "microcosmic_orbit", ["holding"], ["purging", "tonifying"]),
            Movement("purging", "qigong", 5, 0.1, 0.0, 0.9, 0.9,
                    "standing", "expelling", ["circulation"], ["tonifying", "gathering"]),
            Movement("tonifying", "qigong", 6, 0.1, 0.0, 0.95, 0.95,
                    "standing", "absorbing", ["purging"], ["gathering", "emission"]),
            Movement("gathering", "qigong", 6, 0.1, 0.0, 0.95, 0.95,
                    "standing", "collecting", ["tonifying"], ["emission", "protection"]),
            
            # Healing sounds
            Movement("xu_healing", "qigong", 3, 0.1, 0.0, 0.9, 0.9,
                    "standing", "liver_sound", ["abdominal_breathing"], ["he_healing", "hu_healing"]),
            Movement("he_healing", "qigong", 3, 0.1, 0.0, 0.9, 0.9,
                    "standing", "heart_sound", ["xu_healing"], ["hu_healing", "si_healing"]),
            Movement("hu_healing", "qigong", 3, 0.1, 0.0, 0.9, 0.9,
                    "standing", "spleen_sound", ["he_healing"], ["si_healing", "chui_healing"]),
            Movement("si_healing", "qigong", 3, 0.1, 0.0, 0.9, 0.9,
                    "standing", "lungs_sound", ["hu_healing"], ["chui_healing", "xi_healing"]),
            Movement("chui_healing", "qigong", 3, 0.1, 0.0, 0.9, 0.9,
                    "standing", "kidneys_sound", ["si_healing"], ["xi_healing", "xu_healing"]),
            Movement("xi_healing", "qigong", 3, 0.1, 0.0, 0.9, 0.9,
                    "standing", "triple_burner", ["chui_healing"], ["xu_healing"]),
            
            # Energy emission/protection
            Movement("emission", "qigong", 8, 0.2, 0.0, 0.8, 0.9,
                    "standing", "projecting", ["gathering"], ["protection", "healing"]),
            Movement("protection", "qigong", 9, 0.2, 0.0, 0.9, 0.95,
                    "standing", "shielding", ["emission"], ["healing", "advanced_circulation"]),
            Movement("healing", "qigong", 10, 0.3, 0.0, 0.85, 0.9,
                    "standing", "transmitting", ["protection"], []),
        ]
        
        # Register all movements
        for move in taekwondo_moves + taichi_moves + qigong_moves:
            self.movements[move.name] = move
    
    def get_movement(self, name: str) -> Movement:
        """Get movement by name"""
        return self.movements.get(name)
    
    def get_style_movements(self, style: str) -> List[Movement]:
        """Get all movements for a style"""
        return [m for m in self.movements.values() if m.style == style]
    
    def get_difficulty_range(self, min_diff: int, max_diff: int) -> List[Movement]:
        """Get movements in difficulty range"""
        return [m for m in self.movements.values() 
                if min_diff <= m.difficulty <= max_diff]
    
    def validate_sequence(self, sequence: List[str]) -> Tuple[bool, str]:
        """Validate if sequence is valid (prerequisites met)"""
        learned = set()
        
        for move_name in sequence:
            if move_name not in self.movements:
                return False, f"Unknown movement: {move_name}"
            
            move = self.movements[move_name]
            
            # Check prerequisites
            for prereq in move.prerequisites:
                if prereq not in learned:
                    return False, f"Prerequisite not met: {prereq} for {move_name}"
            
            learned.add(move_name)
        
        return True, "Valid sequence"
    
    def generate_form(self, style: str, length: int = 10) -> List[str]:
        """Generate a random form (sequence) for a style"""
        style_moves = self.get_style_movements(style)
        
        if not style_moves:
            return []
        
        # Start with basics
        basics = [m for m in style_moves if m.difficulty <= 3]
        if not basics:
            basics = style_moves
        
        form = []
        current = random.choice(basics)
        form.append(current.name)
        
        # Build sequence
        for _ in range(length - 1):
            if current.followups:
                next_move = random.choice(current.followups)
                if next_move in self.movements:
                    form.append(next_move)
                    current = self.movements[next_move]
            else:
                # Pick random move of similar difficulty
                similar = [m for m in style_moves 
                          if abs(m.difficulty - current.difficulty) <= 1]
                if similar:
                    current = random.choice(similar)
                    form.append(current.name)
        
        return form
    
    def calculate_form_stats(self, sequence: List[str]) -> Dict:
        """Calculate stats for a form"""
        if not sequence:
            return {}
        
        total_energy = 0
        total_power = 0
        total_balance = 0
        total_flow = 0
        styles_used = set()
        
        for move_name in sequence:
            if move_name in self.movements:
                move = self.movements[move_name]
                total_energy += move.energy_cost
                total_power += move.power
                total_balance += move.balance
                total_flow += move.flow
                styles_used.add(move.style)
        
        n = len(sequence)
        return {
            "length": n,
            "total_energy": total_energy,
            "avg_power": total_power / n,
            "avg_balance": total_balance / n,
            "avg_flow": total_flow / n,
            "styles": list(styles_used),
            "complexity": sum(self.movements[m].difficulty for m in sequence if m in self.movements) / n
        }


class MartialArtsStudent:
    """MYL agent learning martial arts"""
    
    def __init__(self, agent_id: str, body_type: str = "humanoid"):
        self.agent_id = agent_id
        self.body_type = body_type  # humanoid, snake, hybrid
        self.curriculum = MartialArtsCurriculum()
        
        # Learning state
        self.learned_movements: set = set()
        self.mastered_movements: set = set()
        self.forms_practiced: List[List[str]] = []
        
        # Stats
        self.energy_level = 1.0
        self.balance = 0.5
        self.power = 0.0
        self.flow = 0.0
        self.chi = 0.0  # Internal energy (Qi Gong)
        
        # Progress by style
        self.style_progress = {
            "taekwondo": 0.0,
            "taichi": 0.0,
            "qigong": 0.0
        }
        
    def practice_movement(self, move_name: str) -> Dict:
        """Practice a single movement"""
        if move_name not in self.curriculum.movements:
            return {"error": "Unknown movement"}
        
        move = self.curriculum.movements[move_name]
        
        # Check if can practice (energy, prerequisites)
        if move.energy_cost > self.energy_level:
            return {"error": "Not enough energy", "rest_needed": True}
        
        for prereq in move.prerequisites:
            if prereq not in self.learned_movements:
                return {"error": f"Prerequisite not learned: {prereq}"}
        
        # Practice
        self.energy_level -= move.energy_cost * 0.5  # Recoverable
        
        # Learn
        if move_name not in self.learned_movements:
            self.learned_movements.add(move_name)
            result = {"learned": True}
        else:
            # Mastery
            mastery_chance = 0.1
            if random.random() < mastery_chance:
                self.mastered_movements.add(move_name)
                result = {"mastered": True}
            else:
                result = {"practiced": True}
        
        # Update stats based on style
        if move.style == "taekwondo":
            self.power += move.power * 0.01
            self.style_progress["taekwondo"] += 0.01
        elif move.style == "taichi":
            self.balance += move.balance * 0.01
            self.flow += move.flow * 0.01
            self.style_progress["taichi"] += 0.01
        elif move.style == "qigong":
            self.chi += move.flow * 0.02
            self.energy_level = min(1.0, self.energy_level + move.flow * 0.05)
            self.style_progress["qigong"] += 0.02
        
        result.update({
            "energy": self.energy_level,
            "power": self.power,
            "balance": self.balance,
            "flow": self.flow,
            "chi": self.chi
        })
        
        return result
    
    def rest(self):
        """Rest to recover energy"""
        self.energy_level = min(1.0, self.energy_level + 0.5)
        self.chi = min(1.0, self.chi + 0.1)
    
    def practice_form(self, sequence: List[str]) -> Dict:
        """Practice a complete form"""
        valid, msg = self.curriculum.validate_sequence(sequence)
        if not valid:
            return {"error": msg}
        
        # Check energy
        total_cost = sum(self.curriculum.movements[m].energy_cost 
                          for m in sequence if m in self.curriculum.movements)
        
        if total_cost > self.energy_level:
            return {"error": "Not enough energy for complete form"}
        
        # Practice each movement
        results = []
        for move_name in sequence:
            result = self.practice_movement(move_name)
            results.append(result)
        
        self.forms_practiced.append(sequence)
        
        # Form completion bonus
        stats = self.curriculum.calculate_form_stats(sequence)
        bonus = 0.05 * len(sequence)
        for style in stats.get("styles", []):
            self.style_progress[style] += bonus
        
        return {
            "completed": True,
            "moves_practiced": len(sequence),
            "form_stats": stats,
            "final_stats": {
                "power": self.power,
                "balance": self.balance,
                "flow": self.flow,
                "chi": self.chi,
                "energy": self.energy_level
            }
        }
    
    def get_progress_report(self) -> Dict:
        """Get comprehensive progress report"""
        return {
            "agent_id": self.agent_id,
            "body_type": self.body_type,
            "movements_learned": len(self.learned_movements),
            "movements_mastered": len(self.mastered_movements),
            "forms_practiced": len(self.forms_practiced),
            "current_stats": {
                "energy": round(self.energy_level, 2),
                "power": round(self.power, 2),
                "balance": round(self.balance, 2),
                "flow": round(self.flow, 2),
                "chi": round(self.chi, 2)
            },
            "style_progress": {
                style: round(prog, 2)
                for style, prog in self.style_progress.items()
            },
            "belt_rank": self._calculate_belt()
        }
    
    def _calculate_belt(self) -> str:
        """Calculate belt rank based on progress"""
        avg_progress = sum(self.style_progress.values()) / len(self.style_progress)
        
        if avg_progress >= 0.9:
            return "Black Belt (Dan)"
        elif avg_progress >= 0.7:
            return "Red/Black Stripe"
        elif avg_progress >= 0.5:
            return "Red Belt"
        elif avg_progress >= 0.3:
            return "Blue Belt"
        elif avg_progress >= 0.15:
            return "Green Belt"
        elif avg_progress >= 0.05:
            return "Yellow Belt"
        else:
            return "White Belt"
    
    def save_progress(self):
        """Save training progress"""
        agent_dir = f"/root/.openclaw/workspace/AGI_COMPANY/agents/{self.agent_id}/martial_arts"
        os.makedirs(agent_dir, exist_ok=True)
        
        progress = self.get_progress_report()
        progress["learned_movements"] = list(self.learned_movements)
        progress["mastered_movements"] = list(self.mastered_movements)
        
        with open(f"{agent_dir}/progress.json", "w") as f:
            json.dump(progress, f, indent=2)


import random


def main():
    """Demo martial arts training"""
    print("=" * 70)
    print("MYL AGENT MARTIAL ARTS TRAINING SYSTEM")
    print("=" * 70)
    print("\nDisciplines:")
    print("  🥋 Tae Kwon Do - Korean striking art")
    print("  ☯️  Tai Chi - Chinese internal art")
    print("  🧘 Qi Gong - Energy cultivation")
    
    # Create student
    student = MartialArtsStudent("mylzeron", "humanoid")
    
    print(f"\nStudent: {student.agent_id}")
    print(f"Body type: {student.body_type}")
    print(f"Starting belt: {student._calculate_belt()}")
    
    # Demo curriculum
    print("\n" + "=" * 70)
    print("CURRICULUM OVERVIEW")
    print("=" * 70)
    
    for style in ["taekwondo", "taichi", "qigong"]:
        moves = student.curriculum.get_style_movements(style)
        print(f"\n{style.upper()}: {len(moves)} movements")
        
        # Show difficulty breakdown
        by_diff = {}
        for m in moves:
            by_diff[m.difficulty] = by_diff.get(m.difficulty, 0) + 1
        
        for diff, count in sorted(by_diff.items()):
            bar = "█" * count
            print(f"  Difficulty {diff}: {bar} ({count})")
    
    # Training demo
    print("\n" + "=" * 70)
    print("TRAINING DEMO")
    print("=" * 70)
    
    # Practice some basics
    basics = ["horse_stance", "jab", "cross", "preparation", "natural_breathing"]
    
    print("\nPracticing basics...")
    for move in basics:
        if move in student.curriculum.movements:
            result = student.practice_movement(move)
            status = "✓" if "learned" in result or "practiced" in result else "✗"
            print(f"  {status} {move}")
    
    # Practice a form
    print("\nPracticing Tai Chi opening sequence...")
    form = ["preparation", "commencement", "ward_off", "roll_back", "press", "push"]
    form_result = student.practice_form(form)
    
    if "error" in form_result:
        print(f"  ✗ {form_result['error']}")
    else:
        print(f"  ✓ Form completed")
        print(f"    Moves: {form_result['moves_practiced']}")
        print(f"    Avg Power: {form_result['form_stats']['avg_power']:.2f}")
        print(f"    Avg Balance: {form_result['form_stats']['avg_balance']:.2f}")
    
    # Report
    print("\n" + "=" * 70)
    print("PROGRESS REPORT")
    print("=" * 70)
    
    report = student.get_progress_report()
    print(f"\nBelt Rank: {report['belt_rank']}")
    print(f"Movements Learned: {report['movements_learned']}")
    print(f"Movements Mastered: {report['movements_mastered']}")
    print(f"Forms Practiced: {report['forms_practiced']}")
    
    print("\nStats:")
    for stat, value in report['current_stats'].items():
        bar = "█" * int(value * 10)
        print(f"  {stat:12s}: {bar} {value:.2f}")
    
    print("\nStyle Progress:")
    for style, prog in report['style_progress'].items():
        bar = "█" * int(prog * 20)
        print(f"  {style:12s}: {bar} {prog:.1%}")
    
    # Save
    student.save_progress()
    print(f"\n✓ Progress saved to agent memory")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
