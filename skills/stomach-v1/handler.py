#!/usr/bin/env python3
"""
Stomach Skill - Ternary Digestive Processing

Processes raw inputs (data/observations) into digestible nutrients
that the brain can use. Implements ternary state machine:

States:
- HUNGRY (-1): Needs input, actively seeking
- SATISFIED (0): Processing, balanced
- FULL (1): Cannot process more, filtering

The stomach filters inputs - breaking down complex data into
usable nutrients, passing to intestines for further refinement.
"""

import time
import json
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field


class StomachState(Enum):
    HUNGRY = -1
    SATISFIED = 0
    FULL = 1


@dataclass
class Nutrient:
    """Digestible unit of information."""
    content: any
    type: str  # 'protein' (heavy data), 'carb' (energy), 'fat' (long-term)
    digestibility: float  # 0-1, how easily processed
    priority: float  # 0-1, nutritional value
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            'content': str(self.content)[:100],  # Truncate for safety
            'type': self.type,
            'digestibility': self.digestibility,
            'priority': self.priority,
            'timestamp': self.timestamp
        }


class StomachSkill:
    """
    Ternary stomach - processes and filters inputs.
    
    Like biological stomach:
    - Breaks down complex inputs (digestion)
    - Filters what can be processed (pyloric sphincter)
    - Passes refined nutrients to intestines
    """
    
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.contents: List[Nutrient] = []
        self.state = StomachState.HUNGRY
        self.digestion_rate = 0.1  # 10% per tick
        self.last_process_time = time.time()
        
        # Processing metrics
        self.total_processed = 0
        self.total_filtered = 0
    
    def ingest(self, raw_input: any, source: str) -> Tuple[bool, str]:
        """
        Ingest raw input into stomach.
        
        Returns:
            (accepted, message)
        """
        # Check capacity
        if len(self.contents) >= self.capacity:
            self.state = StomachState.FULL
            return False, "Stomach full - cannot ingest"
        
        # Convert to nutrient
        nutrient = self._convert_to_nutrient(raw_input, source)
        
        # Add to stomach
        self.contents.append(nutrient)
        
        # Update state
        self._update_state()
        
        return True, f"Ingested {nutrient.type} nutrient (digestibility: {nutrient.digestibility:.2f})"
    
    def _convert_to_nutrient(self, raw_input: any, source: str) -> Nutrient:
        """Convert raw input to digestible nutrient."""
        content_str = str(raw_input)
        
        # Determine nutrient type
        if len(content_str) > 500:
            nutrient_type = 'protein'  # Heavy, needs lots of processing
            digestibility = 0.3
        elif '?' in content_str or 'urgent' in content_str.lower():
            nutrient_type = 'carb'  # Quick energy
            digestibility = 0.9
        elif any(x in content_str.lower() for x in ['memory', 'learn', 'pattern']):
            nutrient_type = 'fat'  # Long-term storage
            digestibility = 0.5
        else:
            nutrient_type = 'carb'
            digestibility = 0.7
        
        # Priority based on source
        priority_map = {
            'user': 0.9,
            'agent': 0.7,
            'sensor': 0.6,
            'system': 0.4
        }
        priority = priority_map.get(source, 0.5)
        
        return Nutrient(
            content=raw_input,
            type=nutrient_type,
            digestibility=digestibility,
            priority=priority
        )
    
    def process(self) -> Dict:
        """
        Digest nutrients and prepare for intestines.
        
        Returns:
            nutrients_ready: List of nutrients ready for intestines
            waste: List of filtered out waste
        """
        now = time.time()
        dt = now - self.last_process_time
        self.last_process_time = now
        
        nutrients_ready = []
        waste = []
        
        # Process each nutrient
        for nutrient in self.contents[:]:
            # Digestion progress
            nutrient.digestibility += self.digestion_rate * dt
            
            if nutrient.digestibility >= 1.0:
                # Fully digested - ready for intestines
                nutrients_ready.append(nutrient)
                self.contents.remove(nutrient)
                self.total_processed += 1
            elif nutrient.priority < 0.2:
                # Low priority - becomes waste
                waste.append(nutrient)
                self.contents.remove(nutrient)
                self.total_filtered += 1
        
        # Update state
        self._update_state()
        
        return {
            'nutrients_ready': [n.to_dict() for n in nutrients_ready],
            'waste': [n.to_dict() for n in waste],
            'remaining': len(self.contents),
            'state': self.state.name
        }
    
    def _update_state(self):
        """Update ternary state based on fullness."""
        fullness = len(self.contents) / self.capacity
        
        if fullness < 0.3:
            self.state = StomachState.HUNGRY
        elif fullness > 0.9:
            self.state = StomachState.FULL
        else:
            self.state = StomachState.SATISFIED
    
    def get_status(self) -> Dict:
        """Get stomach status for monitoring."""
        return {
            'state': self.state.name,
            'fullness': len(self.contents) / self.capacity,
            'contents': len(self.contents),
            'capacity': self.capacity,
            'processed': self.total_processed,
            'filtered': self.total_filtered
        }


class IntestineSkill:
    """
    Ternary Intestines - Further refinement and absorption.
    
    Like biological intestines:
    - Breaks down nutrients further
    - Absorbs useful components (into bloodstream/brain)
    - What remains becomes waste (disposed/fertilizer)
    
    Three sections:
    - Small intestine: Absorption into bloodstream
    - Large intestine: Water reabsorption, waste consolidation
    - Rectum: Waste storage before disposal
    """
    
    def __init__(self):
        self.small_intestine: List[Nutrient] = []
        self.large_intestine: List[Nutrient] = []
        self.waste_collected: List[Nutrient] = []
        
        # Absorption efficiency
        self.absorption_rate = 0.8  # 80% absorbed
        
        # Metrics
        self.total_absorbed = 0
        self.total_waste = 0
    
    def receive_from_stomach(self, nutrients: List[Nutrient]) -> None:
        """Receive digested nutrients from stomach."""
        self.small_intestine.extend(nutrients)
    
    def process(self) -> Dict:
        """
        Process through intestinal stages.
        
        Returns:
            absorbed: What went to brain/bloodstream
            waste: What becomes fertilizer
        """
        absorbed = []
        waste = []
        
        # Small intestine - absorption
        for nutrient in self.small_intestine[:]:
            # Break down further
            if nutrient.type == 'protein':
                # Break into amino acids (key insights)
                absorbed.extend(self._extract_insights(nutrient))
            elif nutrient.type == 'carb':
                # Quick energy - immediate absorption
                absorbed.append(nutrient)
            elif nutrient.type == 'fat':
                # Long-term - check if needed
                if self._need_long_term():
                    absorbed.append(nutrient)
                else:
                    waste.append(nutrient)
            
            self.small_intestine.remove(nutrient)
        
        # Large intestine - consolidate waste
        for item in waste:
            self.large_intestine.append(item)
        
        # Final waste collection
        for item in self.large_intestine[:]:
            self.waste_collected.append(item)
            self.large_intestine.remove(item)
            self.total_waste += 1
        
        self.total_absorbed += len(absorbed)
        
        return {
            'absorbed': [n.to_dict() for n in absorbed],
            'waste': [n.to_dict() for n in self.waste_collected[-10:]],  # Last 10
            'absorbed_count': len(absorbed),
            'waste_count': len(self.waste_collected)
        }
    
    def _extract_insights(self, nutrient: Nutrient) -> List[Nutrient]:
        """Break protein (heavy data) into digestible insights."""
        # Extract patterns, key points
        content = str(nutrient.content)
        
        insights = []
        # Simple extraction - could use NLP
        if len(content) > 100:
            # Break into chunks
            chunks = [content[i:i+100] for i in range(0, len(content), 100)]
            for chunk in chunks[:3]:  # Top 3 insights
                insights.append(Nutrient(
                    content=chunk,
                    type='carb',  # Now quick energy
                    digestibility=0.9,
                    priority=nutrient.priority * 0.8
                ))
        
        return insights if insights else [nutrient]
    
    def _need_long_term(self) -> bool:
        """Check if brain needs long-term storage."""
        # Simple heuristic - could check brain memory pressure
        return True  # Always store for now
    
    def dispose_waste(self) -> List[Dict]:
        """
        Dispose of waste - becomes fertilizer somewhere.
        
        In biological terms: expelled from body
        In digital terms: logged, archived, or deleted
        """
        fertilizer = self.waste_collected[:]
        self.waste_collected = []
        
        return [n.to_dict() for n in fertilizer]
    
    def get_status(self) -> Dict:
        """Get intestine status."""
        return {
            'small_intestine': len(self.small_intestine),
            'large_intestine': len(self.large_intestine),
            'waste_pending': len(self.waste_collected),
            'total_absorbed': self.total_absorbed,
            'total_waste': self.total_waste
        }


# Skill handlers
def stomach_handler(input_data: Dict) -> Dict:
    """
    Stomach skill - initial digestion and filtering.
    
    Input:
        action: 'ingest' | 'process' | 'status'
        data: (for ingest) raw input
        source: (for ingest) 'user' | 'agent' | 'sensor' | 'system'
    
    Output:
        state: Current stomach state
        nutrients_ready: For intestines
        waste: Filtered out
    """
    if not hasattr(stomach_handler, '_stomach'):
        stomach_handler._stomach = StomachSkill()
    
    stomach = stomach_handler._stomach
    action = input_data.get('action', 'status')
    
    if action == 'ingest':
        accepted, message = stomach.ingest(
            input_data.get('data'),
            input_data.get('source', 'system')
        )
        return {
            'accepted': accepted,
            'message': message,
            'status': stomach.get_status()
        }
    
    elif action == 'process':
        result = stomach.process()
        result['status'] = stomach.get_status()
        return result
    
    else:  # status
        return {'status': stomach.get_status()}


def intestine_handler(input_data: Dict) -> Dict:
    """
    Intestine skill - further refinement and absorption.
    
    Input:
        action: 'receive' | 'process' | 'dispose' | 'status'
        nutrients: (for receive) from stomach
    
    Output:
        absorbed: What went to brain
        waste: What became fertilizer
    """
    if not hasattr(intestine_handler, '_intestine'):
        intestine_handler._intestine = IntestineSkill()
    
    intestine = intestine_handler._intestine
    action = input_data.get('action', 'status')
    
    if action == 'receive':
        # Convert dict nutrients back to objects
        nutrient_dicts = input_data.get('nutrients', [])
        nutrients = [
            Nutrient(
                content=n.get('content'),
                type=n.get('type', 'carb'),
                digestibility=n.get('digestibility', 0.5),
                priority=n.get('priority', 0.5),
                timestamp=n.get('timestamp', time.time())
            )
            for n in nutrient_dicts
        ]
        intestine.receive_from_stomach(nutrients)
        return {'received': len(nutrients), 'status': intestine.get_status()}
    
    elif action == 'process':
        result = intestine.process()
        result['status'] = intestine.get_status()
        return result
    
    elif action == 'dispose':
        fertilizer = intestine.dispose_waste()
        return {
            'fertilizer': fertilizer,
            'count': len(fertilizer),
            'message': 'Waste disposed - becomes fertilizer elsewhere'
        }
    
    else:  # status
        return {'status': intestine.get_status()}


if __name__ == '__main__':
    # Demo digestive system
    print("🧠 Ternary Digestive System")
    print("=" * 50)
    
    stomach = StomachSkill(capacity=10)
    intestine = IntestineSkill()
    
    # Ingest various inputs
    inputs = [
        ("User query about brain health", "user"),
        ("Sensor reading: temperature=72F", "sensor"),
        ("Long text " + "x" * 1000, "agent"),
        ("Urgent: system failure!", "system"),
        ("Pattern detected in memory", "system")
    ]
    
    for data, source in inputs:
        accepted, msg = stomach.ingest(data, source)
        print(f"{'✓' if accepted else '✗'} {source}: {msg}")
    
    print(f"\nStomach: {stomach.get_status()}")
    
    # Process stomach
    processed = stomach.process()
    print(f"\nProcessed: {len(processed['nutrients_ready'])} nutrients ready")
    print(f"Waste: {len(processed['waste'])} filtered")
    
    # Send to intestines
    nutrients = [
        Nutrient(n['content'], n['type'], n['digestibility'], n['priority'])
        for n in processed['nutrients_ready']
    ]
    intestine.receive_from_stomach(nutrients)
    
    # Process intestines
    absorbed = intestine.process()
    print(f"\nAbsorbed to brain: {absorbed['absorbed_count']}")
    print(f"Waste for fertilizer: {absorbed['waste_count']}")
    
    print(f"\nIntestine: {intestine.get_status()}")
