#!/usr/bin/env python3
"""
⚡ TEMPORAL WORKFLOWS - Agent Sales TikTok
Native Voice PRIMARY + ElevenLabs OPTIONAL
"""

import os, sys, json, random, subprocess, requests
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Dict

sys.path.insert(0, str(Path(__file__).parent))
from voice import VoiceModule

VOICE = VoiceModule()

AGENTS = {
    "clerk": {"price": 97, "name": "CLERK", "tagline": "Handles emails 24/7"},
    "greet": {"price": 147, "name": "GREET", "tagline": "Professional receptionist"},
    "personal": {"price": 197, "name": "PERSONAL", "tagline": "Your AI life manager"},
    "velvet": {"price": 247, "name": "VELVET", "tagline": "Premium assistant"},
    "concierge": {"price": 297, "name": "CONCIERGE", "tagline": "24/7 VIP support"},
    "executive": {"price": 497, "name": "EXECUTIVE", "tagline": "C-suite coordination"},
}

HOOKS = [
    "I built an AI team that works 24/7 never going back.",
    "What if you could delegate EVERYTHING to an AI?",
    "Meet the agents that run my business while I sleep.",
    "This is what the future of work looks like.",
    "The best employee I ever hired does not need coffee breaks.",
    "My AI secretary handles 100+ emails daily.",
]

@dataclass
class WorkflowResult:
    workflow_id: str
    status: str
    result: Optional[Dict] = None
    error: Optional[str] = None

class Activities:
    def __init__(self):
        self.temp_dir = Path("/data/data/com.termux/files/usr/tmp/ast")
        self.temp_dir.mkdir(exist_ok=True)
        self.output_dir = Path("/storage/emulated/0/Movies/AgentSales")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.voice = VOICE
    
    def generate_script(self, agent_type: str = None) -> Dict:
        if not agent_type:
            agent_type = random.choice(list(AGENTS.keys()))
        agent = AGENTS[agent_type]
        return {
            "id": f"TWF_{datetime.now().strftime('%m%d_%H%M%S')}_{agent_type[:3]}",
            "agent_type": agent_type,
            "name": agent["name"],
            "price": agent["price"],
            "tagline": agent["tagline"],
            "hook": random.choice(HOOKS),
            "narration": f"{random.choice(HOOKS)} {agent['name']} - {agent['tagline']}.",
        }
    
    def create_voiceover(self, script: Dict) -> Optional[str]:
        try:
            path, provider = self.voice.speak(script["narration"], str(self.temp_dir / f"{script['id']}.mp3"))
            script["voice_provider"] = provider
            return path
        except:
            return None
    
    def render_video(self, script: Dict, audio_path: str = None) -> str:
        output = self.output_dir / f"{script['id']}.mp4"
        name = script["name"]
        price = f"${script['price']} per month"
        hook = script["hook"][:40]
        
        if audio_path and Path(audio_path).exists():
            cmd = [
                "ffmpeg", "-y",
                "-i", audio_path,
                "-f", "lavfi", "-i", "color=c=0x1a1a2e:s=1080x1920:d=12",
                "-filter_complex", f"[1:v]drawtext=text='{name}':fontsize=80:fontcolor=0xFFC800:x=(w-text_w)/2:y=300,"
                       f"drawtext=text='{price}':fontsize=50:fontcolor=0x64FF64:x=(w-text_w)/2:y=500,"
                       f"drawtext=text='{hook}':fontsize=40:fontcolor=0xFFFFFF:x=(w-text_w)/2:y=800[vid]",
                "-map", "0:a", "-map", "[vid]",
                "-t", "12", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
                "-c:a", "aac", "-b:a", "192k", "-shortest",
                str(output)
            ]
        else:
            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi", "-i", "color=c=0x1a1a2e:s=1080x1920:d=12",
                "-vf", f"drawtext=text='{name}':fontsize=80:fontcolor=0xFFC800:x=(w-text_w)/2:y=300,"
                       f"drawtext=text='{price}':fontsize=50:fontcolor=0x64FF64:x=(w-text_w)/2:y=500,"
                       f"drawtext=text='{hook}':fontsize=40:fontcolor=0xFFFFFF:x=(w-text_w)/2:y=800",
                "-t", "12", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
                str(output)
            ]
        
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode == 0:
            return str(output)
        raise Exception("Video failed")
    
    def generate_caption(self, script: Dict) -> str:
        return f"🚀 {script['name']} - {script['tagline']}\n💰 ${script['price']}/month\n{script['hook']}\n#AI #AIAgents #FutureOfWork"
    
    def send_notification(self, msg: str):
        config = Path("~/.telegram-bot/config.json").expanduser()
        if config.exists():
            with open(config) as f:
                cfg = json.load(f)
            try:
                requests.post(f"https://api.telegram.org/bot{cfg['bot_token']}/sendMessage",
                           json={"chat_id": cfg["chat_id"], "text": msg}, timeout=10)
            except:
                pass

class Workflows:
    def __init__(self):
        self.activities = Activities()
    
    def GenerateAgentContent(self, input_data: Dict) -> WorkflowResult:
        wid = f"Gen-{datetime.now().strftime('%m%d%H%M%S')}"
        try:
            script = self.activities.generate_script(input_data.get("agent_type"))
            print(f"  📝 {script['name']}: {script['hook'][:35]}...")
            
            audio = self.activities.create_voiceover(script)
            prov = script.get("voice_provider", "none")
            print(f"  🎙️ Voice: ✅ ({prov})" if audio else "  🎙️ Voice: ⏭️ skipped")
            
            video = self.activities.render_video(script, audio)
            print(f"  🎥 Video: ✅ {Path(video).name}")
            
            if input_data.get("notify", True):
                self.activities.send_notification(f"🎬 {script['name']} ready!\n📹 {Path(video).name}")
            
            return WorkflowResult(wid, "completed", {"video": video, "script": script})
        except Exception as e:
            return WorkflowResult(wid, "failed", error=str(e))
    
    def BatchAgentContent(self, input_data: Dict) -> WorkflowResult:
        wid = f"Batch-{datetime.now().strftime('%m%d%H%M%S')}"
        count = input_data.get("count", 5)
        print(f"\n📦 Batch: {count} videos...")
        results = []
        for i in range(count):
            r = self.GenerateAgentContent({"agent_type": random.choice(list(AGENTS.keys())), "notify": False})
            results.append(r)
            print(f"  [{i+1}/{count}] {r.status}")
        
        success = [x for x in results if x.status == "completed"]
        self.activities.send_notification(f"📦 Batch: {len(success)}/{count} videos\n🎙️ Voice: {VOICE.get_status()['primary']}")
        return WorkflowResult(wid, "completed", {"completed": len(success), "total": count})

def main():
    w = Workflows()
    print("⚡ TEMPORAL WORKFLOWS - Agent Sales TikTok")
    print(f"🎙️ Voice: {VOICE.get_status()['primary']}\n")
    
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    
    if cmd == "gen":
        r = w.GenerateAgentContent({"agent_type": sys.argv[2] if len(sys.argv) > 2 else None})
    elif cmd == "batch":
        r = w.BatchAgentContent({"count": int(sys.argv[2]) if len(sys.argv) > 2 else 5})
    elif cmd == "all":
        for a in AGENTS:
            r = w.GenerateAgentContent({"agent_type": a, "notify": False})
            print(f"  {a}: {r.status}")
        return
    else:
        r = w.GenerateAgentContent({})
    
    print(f"\n✅ {r.status}: {r.workflow_id}")

if __name__ == "__main__":
    main()
