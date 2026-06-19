#!/usr/bin/env python3
"""
🚀 AGENT SALES PIPELINE - The Complete System
Creates, voices, and schedules agent promo content for all platforms
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add pipelines to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.voice_pipeline import VoicePipeline
from core.video_pipeline import VideoPipeline
from content.content_templates import ContentGenerator, AGENT_SALES_TEMPLATES
from platforms.tiktok_uploader import TikTokUploader, MultiPlatformUploader

class AgentSalesPipeline:
    """
    Main orchestrator for selling AI agents via social content
    
    Flow:
    1. Select agent to feature
    2. Generate script/content
    3. Create voiceover
    4. Generate video slides
    5. Combine into final video
    6. Upload to platforms
    """
    
    def __init__(self, output_dir="/storage/emulated/0/Movies/AgentSales"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.voice = VoicePipeline()
        self.video = VideoPipeline(str(self.output_dir))
        self.content = ContentGenerator()
        self.uploader = MultiPlatformUploader()
        
        # State
        self.session_log = []
        
    def create_agent_promo(self, agent_type="sales", length="medium",
                          use_voice=True, platforms=["tiktok"]):
        """Create complete promotional video for an agent"""
        
        print(f"🎬 Creating {agent_type} agent promo ({length})...")
        
        # 1. Generate script
        script_data = self.content.generate_script(agent_type, length)
        script = script_data["script"]
        scenes = script_data["scenes"]
        agent = script_data["agent"]
        
        print(f"   📝 Script generated: {len(scenes)} scenes")
        self.session_log.append({
            "step": "script",
            "agent": agent_type,
            "scenes": len(scenes)
        })
        
        # 2. Generate voiceover for each scene
        audio_segments = []
        if use_voice:
            print("   🎙️ Generating voiceover...")
            for i, scene in enumerate(scenes):
                text = scene["text"]
                # Generate audio for this scene
                audio_path = self._temp_file(f"seg_{i}.mp3")
                
                # Use ElevenLabs if available, else skip (termux-tts doesn't save)
                if self.voice.elevenlabs_available:
                    self.voice.speak(text, audio_path)
                    audio_segments.append((scene["start"], audio_path))
        
        print("   ✨ Creating video slides...")
        # 3. Create video slides
        slides_data = []
        for i, scene in enumerate(scenes):
            # Calculate duration from scene timing
            duration = scene["end"] - scene["start"]
            
            slide = {
                "text": scene["text"],
                "bg_color": self._scene_color(i, len(scenes)),
                "duration": duration
            }
            slides_data.append(slide)
        
        # 4. Combine into video (without audio for now - ElevenLabs only)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_name = f"{agent_type}_agent_{timestamp}"
        
        # If we have audio, we'd use it here
        audio_path = None
        if audio_segments and self.voice.elevenlabs_available:
            # For simplicity, use first scene audio
            audio_path = audio_segments[0][1]
        
        video_path = self.video.create_video_from_slides(
            slides_data, 
            audio_path,
            video_name,
            fps=30
        )
        
        print(f"   ✅ Video created: {video_path}")
        self.session_log.append({
            "step": "video",
            "path": video_path,
            "agent": agent_type
        })
        
        # 5. Generate caption
        caption = self._generate_caption(agent, script_data["hashtags"])
        
        # 6. Schedule for upload
        if "tiktok" in platforms:
            self.uploader.uploaders["tiktok"].schedule_upload(
                video_path, agent_type
            )
        
        return {
            "status": "success",
            "video_path": video_path,
            "caption": caption,
            "script": script,
            "agent": agent
        }
    
    def _scene_color(self, index, total):
        """Gradient of colors for scenes"""
        colors = [
            (26, 26, 46),    # Dark blue
            (20, 40, 60),    # Navy
            (40, 20, 60),    # Purple
            (30, 30, 50),    # Slate
            (20, 60, 40),    # Green
            (60, 40, 20),    # Orange
            (40, 20, 40),    # Magenta
            (20, 30, 50),    # Steel blue
        ]
        return colors[index % len(colors)]
    
    def _generate_caption(self, agent, hashtags):
        """Create engaging caption"""
        ctas = AGENT_SALES_TEMPLATES["cta_phrases"]
        
        caption = f"""
🚀 MEET YOUR NEW {agent['name'].upper()}

{agent['tagline']}

💰 ${agent['price']}/month

{chr(10).join(f'• {f}' for f in agent['features'][:3])}

{random.choice(ctas)}

{hashtags}
"""
        return caption.strip()
    
    def _temp_file(self, name):
        """Get temp file path"""
        import tempfile
        temp = Path(tempfile.gettempdir()) / "mortimer_pipeline"
        temp.mkdir(exist_ok=True)
        return temp / name
    
    def batch_create(self, count=10, agents=None, platforms=["tiktok"]):
        """Create multiple promo videos"""
        if agents is None:
            agents = list(AGENT_SALES_TEMPLATES["agent_types"].keys())
        
        results = []
        
        for i in range(count):
            agent = random.choice(agents)
            length = random.choice(["short", "medium", "long"])
            
            result = self.create_agent_promo(
                agent_type=agent,
                length=length,
                platforms=platforms
            )
            results.append(result)
        
        return results
    
    def create_voiceover_only(self, agent_type="sales"):
        """Create just the voiceover audio (no video)"""
        script_data = self.content.generate_script(agent_type, "medium")
        
        audio_files = []
        for i, scene in enumerate(script_data["scenes"]):
            text = scene["text"]
            audio_path = self._temp_file(f"vo_{agent_type}_{i}.mp3")
            
            if self.voice.elevenlabs_available:
                self.voice.speak(text, audio_path)
                audio_files.append(audio_path)
        
        return {
            "script": script_data["script"],
            "audio_files": audio_files,
            "agent": script_data["agent"]
        }
    
    def get_status(self):
        """Get pipeline status"""
        return {
            "output_dir": str(self.output_dir),
            "voice_available": self.voice.elevenlabs_available,
            "elevenlabs_key_set": bool(os.environ.get("ELEVENLABS_API_KEY")),
            "session_log": self.session_log,
            "videos_created": len([l for l in self.session_log if l.get("step") == "video"])
        }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Sales Pipeline")
    parser.add_argument("command", choices=["create", "batch", "voice", "status", "list"])
    parser.add_argument("--agent", default="sales", help="Agent type")
    parser.add_argument("--length", default="medium", choices=["short", "medium", "long"])
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--platforms", nargs="+", default=["tiktok"])
    
    args = parser.parse_args()
    
    pipeline = AgentSalesPipeline()
    
    if args.command == "status":
        status = pipeline.get_status()
        print(json.dumps(status, indent=2))
    
    elif args.command == "list":
        print("Available agents:")
        for key, agent in AGENT_SALES_TEMPLATES["agent_types"].items():
            print(f"  • {key}: {agent['name']} (${agent['price']}/mo)")
    
    elif args.command == "create":
        result = pipeline.create_agent_promo(
            agent_type=args.agent,
            length=args.length,
            platforms=args.platforms
        )
        print("\n✅ PROMO CREATED!")
        print(f"Video: {result['video_path']}")
        print(f"\n📝 Caption:\n{result['caption']}")
    
    elif args.command == "batch":
        results = pipeline.batch_create(
            count=args.count,
            platforms=args.platforms
        )
        print(f"\n✅ Created {len(results)} promo videos!")
        for r in results:
            print(f"  • {r['agent']['name']}: {r['video_path']}")
    
    elif args.command == "voice":
        result = pipeline.create_voiceover_only(args.agent)
        print(f"Voiceover for {args.agent} agent:")
        print(result["script"])
        print(f"\nAudio files: {len(result['audio_files'])}")


if __name__ == "__main__":
    main()
