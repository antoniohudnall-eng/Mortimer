#!/usr/bin/env python3
"""
Spawn MYL agents in Minecraft via RCON
"""

import socket
import struct
import random
import time
import json

MINECRAFT_HOST = "localhost"
RCON_PORT = 25575
RCON_PASSWORD = "myl0nr0s"  # Default, may need adjustment

class RCONClient:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.socket = None
        self.request_id = 0
    
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        
        # Authenticate
        if self.password:
            self.send_packet(3, self.password)  # Type 3 = login
            response = self.recv_packet()
            if response and response['request_id'] != -1:
                print(f"RCON authenticated successfully")
                return True
            else:
                print(f"RCON authentication failed")
                return False
        return True
    
    def send_packet(self, packet_type, payload):
        self.request_id += 1
        payload_bytes = payload.encode('utf-8')
        # Packet structure: length (int32) + request_id (int32) + type (int32) + payload + null + null
        packet = struct.pack('<ii', self.request_id, packet_type) + payload_bytes + b'\x00\x00'
        packet = struct.pack('<i', len(packet)) + packet
        self.socket.sendall(packet)
        return self.request_id
    
    def recv_packet(self):
        try:
            length_data = self.socket.recv(4)
            if not length_data:
                return None
            length = struct.unpack('<i', length_data)[0]
            data = self.socket.recv(length)
            request_id = struct.unpack('<i', data[:4])[0]
            packet_type = struct.unpack('<i', data[4:8])[0]
            payload = data[8:-2].decode('utf-8', errors='replace')
            return {'request_id': request_id, 'type': packet_type, 'payload': payload}
        except Exception as e:
            print(f"Error receiving packet: {e}")
            return None
    
    def command(self, cmd):
        self.send_packet(2, cmd)  # Type 2 = command
        return self.recv_packet()
    
    def close(self):
        if self.socket:
            self.socket.close()


def tellraw(text, color="white", bold=False, prefix=None, prefix_color="gold"):
    """Build a JSON chat component for /tellraw command.
    
    Args:
        text: Main message text
        color: Minecraft color name (white, gold, green, aqua, red, yellow, etc.)
        bold: Whether text should be bold
        prefix: Optional prefix text (like "[MYL]")
        prefix_color: Color for the prefix
    """
    components = []
    
    if prefix:
        components.append({
            "text": prefix,
            "color": prefix_color,
            "bold": True
        })
        components.append({"text": " "})
    
    main_component = {
        "text": text,
        "color": color
    }
    if bold:
        main_component["bold"] = True
    components.append(main_component)
    
    return json.dumps(components)


def spawn_agents_and_build():
    rcon = RCONClient(MINECRAFT_HOST, RCON_PORT, RCON_PASSWORD)
    
    if not rcon.connect():
        print("Trying without password...")
        rcon = RCONClient(MINECRAFT_HOST, RCON_PORT, "")
        if not rcon.connect():
            print("RCON connection failed. Checking if server is running...")
            return
    
    try:
        # MYL agents to spawn
        agents = [
            "mylzeron", "mylonen", "myltwon", "mylthreen",
            "mylforon", "mylfivon", "mylsixon"
        ]
        
        print(f"Spawning {len(agents)} MYL agents...")
        
        # Spawn center platform
        rcon.command(f'tellraw @a {tellraw("Initializing Dark Factory agents...", "yellow", prefix="[MYL]", prefix_color="gold")}')
        
        center_x, center_y, center_z = 100, 70, 100
        
        for i, agent in enumerate(agents):
            # Calculate position in a circle
            angle = (i / len(agents)) * 2 * 3.14159
            x = center_x + int(15 * __import__('math').cos(angle))
            z = center_z + int(15 * __import__('math').sin(angle))
            y = center_y
            
            # Summon named armor stand as agent representation
            cmd = f'summon minecraft:armor_stand {x} {y} {z} {{CustomName:\'{{"text":"{agent}", "color":"aqua", "bold":true}}\', CustomNameVisible:1, NoGravity:1, ShowArms:1, Small:0, Invulnerable:1, Tags:["myl_agent","{agent}"]}}'
            response = rcon.command(cmd)
            print(f"Spawned {agent} at ({x}, {y}, {z})")
            
            # Add effect for visibility
            rcon.command(f'effect give @e[type=armor_stand,tag={agent}] minecraft:glowing 999999 1 true')
            
            time.sleep(0.2)
        
        # Create platform for the agents
        print("Building platform...")
        rcon.command(f'tellraw @a {tellraw("Constructing agent base...", "yellow", prefix="[MYL]", prefix_color="gold")}')
        
        # Build a circular platform
        for dx in range(-20, 21):
            for dz in range(-20, 21):
                dist = (dx**2 + dz**2) ** 0.5
                if dist < 18:
                    rcon.command(f"setblock {center_x + dx} {center_y - 1} {center_z + dz} minecraft:stone_bricks")
        
        # Build central tower
        print("Building central tower...")
        for y in range(center_y, center_y + 10):
            for dx in range(-3, 4):
                for dz in range(-3, 4):
                    if abs(dx) == 3 or abs(dz) == 3:
                        rcon.command(f"setblock {center_x + dx} {y} {center_z + dz} minecraft:glass")
        
        # Spawn some activity - each agent places blocks around them
        print("Triggering agent building actions...")
        rcon.command(f'tellraw @a {tellraw("Agents beginning construction...", "yellow", prefix="[MYL]", prefix_color="gold")}')
        
        for i, agent in enumerate(agents):
            angle = (i / len(agents)) * 2 * 3.14159
            x = center_x + int(10 * __import__('math').cos(angle))
            z = center_z + int(10 * __import__('math').sin(angle))
            y = center_y
            
            # Each agent builds a small pillar
            for h in range(3):
                block_types = ["minecraft:diamond_block", "minecraft:emerald_block", "minecraft:gold_block", 
                               "minecraft:iron_block", "minecraft:lapis_block", "minecraft:redstone_block", "minecraft:coal_block"]
                block = block_types[i % len(block_types)]
                rcon.command(f"setblock {x} {y + h} {z} {block}")
                time.sleep(0.1)
        
        # Make agents say hello using tellraw (entity name + colored message)
        greetings = [
            "Hello from MYLZERON!",
            "MYLONE reporting for duty!",
            "MYLTWO online and ready!",
            "MYLTHREE at your service!",
            "MYLFOR here to build!",
            "MYLFIVE checking in!",
            "MYLSIX standing by!"
        ]
        
        for i, agent in enumerate(agents):
            # Build tellraw that shows entity name + colored message
            # @s selector picks the executing entity's name
            msg_json = json.dumps([
                {"selector": "@s"},
                {"text": " "},
                {"text": greetings[i], "color": "aqua", "bold": True}
            ])
            rcon.command(f'execute as @e[type=armor_stand,tag={agent}] run tellraw @a {msg_json}')
            time.sleep(0.3)
        
        # Final announcement
        rcon.command(f'tellraw @a {tellraw("All 7 Dark Factory agents deployed and building!", "green", bold=True, prefix="[MYL]", prefix_color="gold")}')
        rcon.command(f'tellraw @a {tellraw("Agents: mylzeron, mylonen, myltwon, mylthreen, mylforon, mylfivon, mylsixon", "gray")}')
        
        print("\n✓ All MYL agents spawned and active!")
        print(f"✓ Location: ({center_x}, {center_y}, {center_z})")
        print("✓ Agents are building and interacting with the world")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        rcon.close()

if __name__ == "__main__":
    spawn_agents_and_build()
