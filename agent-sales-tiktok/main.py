#!/usr/bin/env python3
"""
🎬 AGENT SALES TIKTOK PIPELINE
Selling AI agents with voice on TikTok
"""

import os
import sys
import subprocess
import random
import requests
from pathlib import Path
from datetime import datetime

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
VOICE_ID = "pNInz6obpgDQGcFmaJgB"

AGENTS = {
    "clerk": {"price": 97, "name": "CLERK", "tagline": "Handles emails 24/7"},
    "greet": {"price": 147, "name": "GREET", "tagline": "Professional receptionist"},
    "personal": {"price": 197, "name": "PERSONAL", "tagline": "Your AI life manager"},
    "velvet": {"price": 247, "name": "VELVET", "tagline": "Premium assistant"},
    "concierge": {"price": 297, "name": "CONCIERGE", "tagline": "24/7 VIP support"},
    "executive": {"price": 497, "name": "EXECUTIVE", "tagline": "C-suite coordination"},
}

HOOKS = [
    "I built an AI team that works 24/7... never going back.",
    "What if you could delegate EVERYTHING to an AI?",
    "Meet the agents that run my business while I sleep.",
    "This is what the future of work looks like.",
    "The best employee I ever hired doesn't need coffee breaks.",
]

class Pipeline:
    def __init__(self):
        self.out = Path("/storage/emulated/0/Movies/AgentSales")
        self.out.mkdir(parents=True, exist_ok=True)
        self.temp = Path("/data/data/com.termux/files/usr/tmp/ast")
        self.temp.mkdir(exist_ok=True)
        
    def script(self, agent=None):
        if not agent:
            agent = random.choice(list(AGENTS.keys()))
        a = AGENTS[agent]
        hook = random.choice(HOOKS)
        return {
            "id": f"AST_{datetime.now().strftime('%m%d_%H%M%S')}_{agent[:3]}",
            "agent": agent,
            "name": a["name"],
            "price": a["price"],
            "hook": hook,
            "tagline": a["tagline"],
            "narration": f"{hook} {a['name']} - {a['tagline']}.",
        }
    
    def voice(self, s):
        if not ELEVENLABS_API_KEY:
            return None
        try:
            r = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
                json={"text": s["narration"], "voice_settings": {"stability": 0.5}},
                headers={"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"},
                timeout=30
            )
            if r.status_code == 200:
                p = self.temp / f"{s['id']}.mp3"
                p.write_bytes(r.content)
                return str(p)
        except:
            pass
        return None
    
    def video(self, s, audio=None):
        # Create video with FFmpeg text
        out = self.out / f"{s['id']}.mp4"
        txt = f"{s['name']}\n${s['price']}/month\n{s['hook']}"
        
        # Replace newlines for FFmpeg
        txt_ff = txt.replace("\n", "\\n")
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c=0x1a1a2e:s=1080x1920:d=12",
            "-vf", f"drawtext=text='{txt_ff}':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:borderw=2:bordercolor=black",
            "-t", "12", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        ]
        
        if audio and Path(audio).exists():
            cmd.extend(["-i", audio, "-c:a", "aac"])
        
        cmd.append(str(out))
        
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode == 0:
            return str(out)
        return None
    
    def create(self, agent=None):
        s = self.script(agent)
        print(f"📹 {s['name']} | {s['hook'][:45]}...")
        
        audio = self.voice(s)
        video = self.video(s, audio)
        
        if video:
            size = Path(video).stat().st_size / 1024
            print(f"   ✅ {Path(video).name} ({size:.0f}KB)")
        else:
            print("   ❌ Failed")
        
        return s


def main():
    p = Pipeline()
    print("🎬 AGENT SALES TIKTOK")
    print("=" * 50)
    
    count = 5
    if "--batch" in sys.argv:
        for a in sys.argv:
            if a.startswith("--count="):
                count = int(a.split("=")[1])
    
    for _ in range(count):
        p.create()
    
    print(f"\n📁 {p.out}")


if __name__ == "__main__":
    main()
