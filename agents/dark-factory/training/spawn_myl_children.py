#!/usr/bin/env python3
"""
Spawn MYL Children for Physics Room Training
Train mylzeron through mylsixes in expanded physics room
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/simulation')
sys.path.insert(0, '/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/training')

from expanded_physics_room import ExpandedPhysicsRoom, TrainingScenario
from myl_training_system import MYLChild, TrainingStage
import logging
import random
from datetime import datetime
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SpawnMYL")

# MYL children names
MYL_CHILDREN = [
    "mylzeron",    # 001
    "mylonen",     # 002  
    "myltwon",     # 003
    "mylthreen",   # 004
    "mylforon",    # 005
    "mylfivon",    # 006
    "mylsixon",    # 007
]

def create_myl_agent(child_id: str) -> dict:
    """Create MYL child agent configuration"""
    return {
        "id": child_id,
        "type": "myl",
        "created": datetime.now().isoformat(),
        "specialization": random.choice([
            "manipulation", "navigation", "sorting", 
            "precision", "cooperation", "exploration"
        ]),
        "stats": {
            "strength": random.uniform(0.5, 1.0),
            "dexterity": random.uniform(0.5, 1.0),
            "intelligence": random.uniform(0.5, 1.0),
            "curiosity": random.uniform(0.7, 1.0),
        }
    }

def train_child_in_physics_room(child_id: str, room: ExpandedPhysicsRoom, 
                                 scenarios: TrainingScenario) -> dict:
    """Train a single MYL child"""
    logger.info(f"Training {child_id}...")
    
    results = {
        "child_id": child_id,
        "scenarios_completed": [],
        "total_steps": 0,
        "success_rate": 0.0,
        "skills_learned": []
    }
    
    # Run each scenario
    scenario_list = ['stack_tower', 'sort_colors', 'navigate_course', 
                     'precision_place', 'multi_task']
    
    successes = 0
    for scenario_name in scenario_list:
        logger.info(f"  Running {scenario_name}...")
        result = scenarios.run(scenario_name, child_id)
        
        results["scenarios_completed"].append({
            "name": scenario_name,
            "success": result.get('success', False),
            "steps": result.get('steps', 0)
        })
        
        if result.get('success'):
            successes += 1
            results["skills_learned"].append(scenario_name)
        
        results["total_steps"] += result.get('steps', 0)
    
    results["success_rate"] = successes / len(scenario_list)
    
    # Determine specialization based on performance
    best_scenario = max(results["scenarios_completed"], 
                       key=lambda x: x["success"])
    results["best_skill"] = best_scenario["name"]
    
    return results

def save_myl_memory(child_id: str, results: dict, memory_path: str):
    """Save MYL child training memory"""
    agent_dir = os.path.join(memory_path, child_id)
    os.makedirs(agent_dir, exist_ok=True)
    os.makedirs(os.path.join(agent_dir, "memory"), exist_ok=True)
    
    # Create MEMORY.md
    memory_content = f"""# {child_id} Memory

## Training Session - {datetime.now().strftime('%Y-%m-%d')}

### Results
- **Success Rate**: {results['success_rate']:.1%}
- **Total Steps**: {results['total_steps']}
- **Scenarios Completed**: {len(results['scenarios_completed'])}
- **Skills Learned**: {', '.join(results['skills_learned'])}
- **Best Skill**: {results['best_skill']}

### Scenario Performance
"""
    
    for scenario in results['scenarios_completed']:
        status = "✅" if scenario['success'] else "❌"
        memory_content += f"\n{status} **{scenario['name']}**: {scenario['steps']} steps\n"
    
    memory_content += f"""
### Specialization
{results.get('specialization', 'General')}

### Physical Room Training
Trained in Expanded Physics Room with:
- 64 interactive objects
- 4 training zones
- Physics-based manipulation

---

*Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    with open(os.path.join(agent_dir, "MEMORY.md"), 'w') as f:
        f.write(memory_content)
    
    # Save JSON results
    with open(os.path.join(agent_dir, "training_results.json"), 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Saved memory for {child_id}")

def main():
    """Main training orchestration"""
    print("=" * 70)
    print("SPAWNING MYL CHILDREN FOR PHYSICS ROOM TRAINING")
    print("=" * 70)
    
    # Create physics room
    logger.info("Creating Expanded Physics Room...")
    room = ExpandedPhysicsRoom()
    scenarios = TrainingScenario(room)
    
    print(f"\nRoom ready: {len(room.objects)} objects, {len(room.zones)} zones")
    
    # Train all MYL children
    all_results = []
    memory_base = "/root/.openclaw/workspace/AGI_COMPANY/agents"
    
    for child_id in MYL_CHILDREN:
        print(f"\n{'='*70}")
        print(f"Training: {child_id}")
        print('='*70)
        
        # Create agent
        agent_config = create_myl_agent(child_id)
        
        # Train in physics room
        results = train_child_in_physics_room(child_id, room, scenarios)
        results['config'] = agent_config
        
        all_results.append(results)
        
        # Save memory
        save_myl_memory(child_id, results, memory_base)
        
        print(f"✅ {child_id} complete - Success rate: {results['success_rate']:.1%}")
        print(f"   Best skill: {results['best_skill']}")
        print(f"   Skills: {', '.join(results['skills_learned'])}")
    
    # Summary
    print("\n" + "=" * 70)
    print("TRAINING COMPLETE - SUMMARY")
    print("=" * 70)
    
    total_success = sum(r['success_rate'] for r in all_results) / len(all_results)
    print(f"\nOverall Success Rate: {total_success:.1%}")
    print(f"Total Children Trained: {len(all_results)}")
    
    print("\nIndividual Results:")
    for result in all_results:
        print(f"  {result['child_id']:12s}: {result['success_rate']:>6.1%} "
              f"({len(result['skills_learned'])}/5 skills) - "
              f"Best: {result['best_skill']}")
    
    print("\n" + "=" * 70)
    print("Memories saved to:", memory_base)
    print("=" * 70)

if __name__ == "__main__":
    main()
