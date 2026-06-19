#!/usr/bin/env python3
"""
📦 MORTIMER LOGISTICS BOT
Handles: Transcriptions, Pickups, Deliveries
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

TOKEN = "8467857363:AAGofPQ6RtppzI8EwsA5GrC5ZAnLaGztvlY"
CAPTAIN_ID = 1611228942

# Data files
DATA_DIR = Path.home() / "mortimer" / "logistics"
DATA_DIR.mkdir(exist_ok=True)

PICKUP_FILE = DATA_DIR / "pickups.json"
DELIVERY_FILE = DATA_DIR / "deliveries.json"
TASKS_FILE = DATA_DIR / "tasks.json"

def load_json(filepath, default):
    if filepath.exists():
        with open(filepath) as f:
            return json.load(f)
    return default

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def transcribe_audio(file_id):
    """Download and transcribe voice message"""
    # Download voice file
    result = subprocess.run([
        "curl", "-s", 
        f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}"
    ], capture_output=True, text=True)
    
    try:
        data = json.loads(result.stdout)
        if not data.get('ok'):
            return "Could not get file"
        
        file_path = data['result']['file_path']
        
        # Download the actual file
        dl_result = subprocess.run([
            "curl", "-s",
            f"https://api.telegram.org/file/bot{TOKEN}/{file_path}",
            "-o", "/tmp/voice_msg.ogg"
        ], capture_output=True)
        
        # Use speech recognition
        # For now, return placeholder - Android speech recognition would need different approach
        return "[Voice message received - will transcribe]"
    except:
        return "[Transcription failed]"

def add_pickup(item):
    """Add item to pickup list"""
    pickups = load_json(PICKUP_FILE, [])
    pickups.append({
        "item": item,
        "added": datetime.now().isoformat(),
        "status": "pending"
    })
    save_json(PICKUP_FILE, pickups)
    return f"✅ Added to pickups: {item}"

def add_delivery(item, address):
    """Add delivery"""
    deliveries = load_json(DELIVERY_FILE, [])
    deliveries.append({
        "item": item,
        "address": address,
        "added": datetime.now().isoformat(),
        "status": "pending"
    })
    save_json(DELIVERY_FILE, deliveries)
    return f"🚚 Added delivery: {item} → {address}"

def list_pickups():
    pickups = load_json(PICKUP_FILE, [])
    if not pickups:
        return "📦 No pickups pending"
    
    msg = "📦 **PICKUPS:**\n"
    for i, p in enumerate(pickups, 1):
        status = "⏳" if p['status'] == 'pending' else "✅"
        msg += f"{status} {i}. {p['item']}\n"
    return msg

def list_deliveries():
    deliveries = load_json(DELIVERY_FILE, [])
    if not deliveries:
        return "🚚 No deliveries pending"
    
    msg = "🚚 **DELIVERIES:**\n"
    for i, d in enumerate(deliveries, 1):
        status = "⏳" if d['status'] == 'pending' else "✅"
        msg += f"{status} {i}. {d['item']} → {d['address']}\n"
    return msg

def complete_pickup(index):
    pickups = load_json(PICKUP_FILE, [])
    if 0 < index <= len(pickups):
        pickups[index-1]['status'] = 'done'
        pickups[index-1]['completed'] = datetime.now().isoformat()
        save_json(PICKUP_FILE, pickups)
        return f"✅ Pickup {index} completed!"
    return "❌ Invalid pickup number"

def complete_delivery(index):
    deliveries = load_json(DELIVERY_FILE, [])
    if 0 < index <= len(deliveries):
        deliveries[index-1]['status'] = 'done'
        deliveries[index-1]['completed'] = datetime.now().isoformat()
        save_json(DELIVERY_FILE, deliveries)
        return f"✅ Delivery {index} completed!"
    return "❌ Invalid delivery number"

print("📦 MORTIMER LOGISTICS BOT READY")
print(f"Data directory: {DATA_DIR}")

# Initialize files
if not PICKUP_FILE.exists():
    save_json(PICKUP_FILE, [])
if not DELIVERY_FILE.exists():
    save_json(DELIVERY_FILE, [])

print("✅ Pickup list initialized")
print("✅ Delivery list initialized")
