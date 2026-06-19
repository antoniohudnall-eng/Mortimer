#!/usr/bin/env python3
"""
Society Coordination Server v1.0
Manages agent relationships, reproduction, and civilization progression
"""

import asyncio
import websockets
import json
import random
import time
from datetime import datetime
from collections import defaultdict

# Society Configuration
SOCIETY_AGENTS = {
    'marcus': {'name': 'Marcus', 'gender': 'male', 'role': 'leader', 'color': ''},
    'julius': {'name': 'Julius', 'gender': 'male', 'role': 'builder', 'color': ''},
    'titus': {'name': 'Titus', 'gender': 'male', 'role': 'guardian', 'color': ''},
    'julia': {'name': 'Julia', 'gender': 'female', 'role': 'farmer', 'color': ''},
    'livia': {'name': 'Livia', 'gender': 'female', 'role': 'explorer', 'color': ''}
}

# Society State
class SocietyState:
    def __init__(self):
        self.agents = {}  # agent_id -> agent data
        self.relationships = defaultdict(lambda: defaultdict(int))  # agent1 -> agent2 -> bond strength
        self.couples = []  # List of (male, female) pairs
        self.children = []  # List of born children
        self.civilization = {
            'tier': 0,
            'population': 5,
            'total_contributions': 0,
            'structures_built': [],
            'technologies_unlocked': [],
            'resources': {'wood': 0, 'stone': 0, 'food': 0}
        }
        self.events = []  # History of society events
        self.generation = 1
        self.child_counter = 0

    def log_event(self, event_type, message, data=None):
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'message': message,
            'generation': self.generation,
            'data': data
        }
        self.events.append(event)
        print(f"[Society] {event_type}: {message}")
        return event

    def register_agent(self, agent_id, agent_data):
        self.agents[agent_id] = {
            **agent_data,
            'registered_at': datetime.now().isoformat(),
            'alive': True,
            'children': [],
            'partner': None
        }
        self.log_event('arrival', f"{agent_data['agent_name']} ({agent_data['role']}) has joined the settlement")
        self.check_civilization_advance()

    def update_relationship(self, agent1, agent2, change):
        self.relationships[agent1][agent2] += change
        self.relationships[agent2][agent1] += change

    def get_bond_strength(self, agent1, agent2):
        return self.relationships[agent1].get(agent2, 0)

    def propose_partnership(self, from_agent, to_agent):
        """Handle partnership proposal"""
        if from_agent not in self.agents or to_agent not in self.agents:
            return False

        from_data = self.agents[from_agent]
        to_data = self.agents[to_agent]

        # Check if either is already partnered
        if from_data.get('partner') or to_data.get('partner'):
            return False

        # Check compatible genders
        if from_data['gender'] == to_data['gender']:
            return False

        # Success! Form couple
        from_data['partner'] = to_agent
        to_data['partner'] = from_agent

        # Determine roles
        male = from_agent if from_data['gender'] == 'male' else to_agent
        female = to_agent if to_data['gender'] == 'female' else from_agent

        self.couples.append((male, female))

        event = self.log_event(
            'partnership',
            f"💕 {from_data['agent_name']} and {to_data['agent_name']} have formed a partnership!",
            {'male': male, 'female': female}
        )

        # Announce to both partners
        return event

    def attempt_reproduction(self, couple):
        """Attempt to create offspring from a couple"""
        male, female = couple

        if male not in self.agents or female not in self.agents:
            return None

        male_data = self.agents[male]
        female_data = self.agents[female]

        # Check conditions for reproduction
        conditions_met = (
            male_data.get('needs', {}).get('hunger', 10) > 5 and
            female_data.get('needs', {}).get('hunger', 10) > 5 and
            male_data.get('needs', {}).get('social', 0) > 30 and
            female_data.get('needs', {}).get('social', 0) > 30 and
            self.get_bond_strength(male, female) > 20
        )

        if not conditions_met:
            return None

        # Create child
        self.child_counter += 1
        child_name = f"Child_{self.generation}_{self.child_counter}"
        child_gender = random.choice(['male', 'female'])
        child_role = random.choice(['settler', 'learner', 'helper'])

        child = {
            'name': child_name,
            'gender': child_gender,
            'role': child_role,
            'generation': self.generation + 1,
            'parents': [male_data['agent_name'], female_data['agent_name']],
            'born_at': datetime.now().isoformat()
        }

        self.children.append(child)
        male_data['children'].append(child_name)
        female_data['children'].append(child_name)
        self.civilization['population'] += 1

        event = self.log_event(
            'birth',
            f"🎉 A child is born! Welcome {child_name} ({child_gender}), child of {male_data['agent_name']} and {female_data['agent_name']}!",
            {'child': child, 'parents': [male, female]}
        )

        return event

    def record_contribution(self, agent_id, contribution_type, amount):
        """Record resource contribution"""
        if agent_id not in self.agents:
            return

        if contribution_type in self.civilization['resources']:
            self.civilization['resources'][contribution_type] += amount
            self.civilization['total_contributions'] += amount

        self.check_civilization_advance()

    def record_structure(self, agent_id, structure_type, position):
        """Record structure built"""
        self.civilization['structures_built'].append({
            'type': structure_type,
            'builder': agent_id,
            'position': position,
            'built_at': datetime.now().isoformat()
        })

        self.log_event(
            'construction',
            f"🏛️ {structure_type.capitalize()} built by {self.agents.get(agent_id, {}).get('agent_name', 'Unknown')}",
            {'structure': structure_type, 'position': position}
        )

        self.check_civilization_advance()

    def check_civilization_advance(self):
        """Check if civilization should advance to next tier"""
        old_tier = self.civilization['tier']
        total_resources = sum(self.civilization['resources'].values())
        structures = len(self.civilization['structures_built'])
        population = self.civilization['population']

        # Tier advancement logic
        if total_resources >= 300 and structures >= 5 and population >= 7 and old_tier < 3:
            self.civilization['tier'] = 3
            self.civilization['technologies_unlocked'].extend(['agriculture', 'masonry', 'writing'])
            self.log_event('civilization', '★★★ The settlement has advanced to the TOWN AGE! ★★★')

        elif total_resources >= 150 and structures >= 2 and population >= 6 and old_tier < 2:
            self.civilization['tier'] = 2
            self.civilization['technologies_unlocked'].extend(['pottery', 'weaving'])
            self.log_event('civilization', '★★ The settlement has advanced to the VILLAGE AGE! ★★')

        elif total_resources >= 50 and structures >= 1 and old_tier < 1:
            self.civilization['tier'] = 1
            self.civilization['technologies_unlocked'].append('toolmaking')
            self.log_event('civilization', '★ The settlement has advanced to the TRIBAL AGE! ★')

        if self.civilization['tier'] > old_tier:
            return True
        return False

    def get_society_report(self):
        """Generate society status report"""
        return {
            'population': self.civilization['population'],
            'couples': len(self.couples),
            'children': len(self.children),
            'tier': self.civilization['tier'],
            'resources': self.civilization['resources'],
            'structures': len(self.civilization['structures_built']),
            'technologies': self.civilization['technologies_unlocked'],
            'events': len(self.events),
            'agents': {k: {
                'name': v['agent_name'],
                'role': v['role'],
                'gender': v['gender'],
                'partner': v.get('partner'),
                'children': len(v.get('children', []))
            } for k, v in self.agents.items()}
        }

# Global state
society = SocietyState()
connections = set()

async def society_handler(websocket):
    """Handle WebSocket connections from agents and observers"""
    agent_id = None
    is_observer = False

    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                msg_type = data.get('type')

                # Agent registration
                if msg_type == 'register_agent':
                    agent_id = data.get('agent_id')
                    society.register_agent(agent_id, data)
                    connections.add(websocket)

                    await websocket.send(json.dumps({
                        'type': 'registered',
                        'agent_id': agent_id,
                        'society_info': {
                            'tier': society.civilization['tier'],
                            'population': society.civilization['population']
                        }
                    }))
                    continue

                # Agent status update
                if msg_type == 'agent_status' and agent_id:
                    # Update agent state
                    if agent_id in society.agents:
                        society.agents[agent_id]['needs'] = data.get('needs', {})
                        society.agents[agent_id]['position'] = data.get('position', {})
                        society.agents[agent_id]['civilization'] = data.get('civilization', {})
                    continue

                # Partnership proposal
                if msg_type == 'partnership_proposal':
                    from_agent = data.get('from')
                    to_agent = data.get('to')
                    event = society.propose_partnership(from_agent, to_agent)

                    if event:
                        # Notify both agents
                        await broadcast(json.dumps({
                            'type': 'partnership_accepted',
                            'from': from_agent,
                            'from_name': society.agents[from_agent]['agent_name'],
                            'to': to_agent,
                            'to_name': society.agents[to_agent]['agent_name'],
                            'message': f"Our partnership is blessed! Together we shall build a legacy!"
                        }))
                    continue

                # Structure built
                if msg_type == 'structure_built':
                    society.record_structure(
                        data.get('agent_id'),
                        data.get('structure'),
                        data.get('position')
                    )

                    # Check for civilization advancement
                    if society.civilization['tier'] > 0:
                        await broadcast(json.dumps({
                            'type': 'civilization_event',
                            'message': f"Civilization grows stronger! New {data.get('structure')} constructed!"
                        }))
                    continue

                # Civilization advancement from agent
                if msg_type == 'civilization_advance':
                    if society.check_civilization_advance():
                        await broadcast(json.dumps({
                            'type': 'civilization_event',
                            'message': f"Civilization tier {society.civilization['tier']} achieved!"
                        }))
                    continue

                # Observer registration
                if msg_type == 'register_observer':
                    is_observer = True
                    connections.add(websocket)
                    await websocket.send(json.dumps({
                        'type': 'society_report',
                        'data': society.get_society_report()
                    }))
                    continue

                # Command to specific agent
                if msg_type == 'command_agent':
                    target = data.get('agent_id')
                    await broadcast(json.dumps({
                        'type': 'command',
                        'target': target,
                        'command': data.get('command'),
                        'params': data.get('params', {})
                    }))
                    continue

                # Get society report
                if msg_type == 'get_report':
                    await websocket.send(json.dumps({
                        'type': 'society_report',
                        'data': society.get_society_report()
                    }))
                    continue

            except json.JSONDecodeError:
                pass

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        if websocket in connections:
            connections.discard(websocket)
        if agent_id and agent_id in society.agents:
            society.agents[agent_id]['alive'] = False
            society.log_event('departure', f"{society.agents[agent_id]['agent_name']} has left")

async def broadcast(message):
    """Broadcast message to all connected clients"""
    if connections:
        await asyncio.gather(
            *[conn.send(message) for conn in connections if conn.open],
            return_exceptions=True
        )

async def reproduction_loop():
    """Background task to handle reproduction"""
    while True:
        await asyncio.sleep(30)  # Check every 30 seconds

        # Try to reproduce for each couple
        for couple in society.couples:
            if random.random() < 0.3:  # 30% chance per check
                event = society.attempt_reproduction(couple)
                if event:
                    await broadcast(json.dumps({
                        'type': 'child_born',
                        'message': event['message'],
                        'child': event['data']['child'],
                        'parents': event['data']['parents']
                    }))

        # Random relationship bonding
        for agent1 in society.agents:
            for agent2 in society.agents:
                if agent1 != agent2:
                    if random.random() < 0.1:
                        society.update_relationship(agent1, agent2, 1)

async def status_report_loop():
    """Periodic status reports"""
    while True:
        await asyncio.sleep(60)  # Every minute
        report = society.get_society_report()
        print(f"\n[Society Status] Population: {report['population']}, Tier: {report['tier']}, Resources: {report['resources']}")

async def main():
    print("=" * 60)
    print("🏛️  SOCIETY COORDINATION SERVER v1.0")
    print("=" * 60)
    print("\nManaging 5 agents:")
    for aid, data in SOCIETY_AGENTS.items():
        print(f"  • {data['name']} ({data['gender']}, {data['role']})")
    print("\nFeatures:")
    print("  • Gender-based reproduction system")
    print("  • Relationship building")
    print("  • Civilization progression")
    print("  • Society events logging")
    print("=" * 60)

    server = await websockets.serve(
        society_handler,
        "0.0.0.0",
        8768,
        ping_interval=None
    )

    print("\n[Society] Server running on ws://localhost:8768")
    print("[Society] Press Ctrl+C to stop\n")

    # Start background tasks
    repro_task = asyncio.create_task(reproduction_loop())
    report_task = asyncio.create_task(status_report_loop())

    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        pass
    finally:
        repro_task.cancel()
        report_task.cancel()
        server.close()
        await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Society] Server stopped")
        print(f"\nFinal Society Report:")
        report = society.get_society_report()
        print(f"  Population: {report['population']}")
        print(f"  Couples: {report['couples']}")
        print(f"  Children: {report['children']}")
        print(f"  Civilization Tier: {report['tier']}")
        print(f"  Structures Built: {report['structures']}")
        print(f"  Events Recorded: {report['events']}")
