#!/usr/bin/env python3
"""
📱 TIKTOK DELIVERY PIPELINE
Generate content → Package for mobile upload
Works without browser automation
"""

import os
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import random

class TikTokDelivery:
    """
    Hybrid workflow: Generate content on server, deliver to mobile
    
    Options:
    1. Save to accessible folder (Movies/)
    2. Send via Telegram bot
    3. Package for Later/Publer/Buffer
    4. Generate upload-ready package
    """
    
    def __init__(self):
        self.output_base = Path("/storage/emulated/0/Movies/AgentSales")
        self.ready_folder = Path("/storage/emulated/0/Movies/TikTokReady")
        self.ready_folder.mkdir(parents=True, exist_ok=True)
        
        self.telegram_ready = self._check_telegram()
        
    def _check_telegram(self):
        """Check if we can send via Telegram"""
        # Check for telegram bot config
        bot_config = Path("~/.telegram-bot/config.json").expanduser()
        return bot_config.exists()
    
    def prepare_for_upload(self, video_path, caption, hashtags=""):
        """Prepare a video + caption package"""
        video_path = Path(video_path)
        
        if not video_path.exists():
            return {"status": "error", "message": "Video not found"}
        
        # Copy to ready folder with descriptive name
        timestamp = datetime.now().strftime("%m%d_%H%M")
        new_name = f"tiktok_{timestamp}_{video_path.stem}.mp4"
        ready_path = self.ready_folder / new_name
        
        shutil.copy2(video_path, ready_path)
        
        # Save caption file
        caption_file = self.ready_folder / f"tiktok_{timestamp}_caption.txt"
        with open(caption_file, 'w') as f:
            f.write(f"VIDEO: {new_name}\n\n")
            f.write("CAPTION:\n")
            f.write(f"{caption}\n\n")
            f.write(f"{hashtags}")
        
        return {
            "status": "ready",
            "video": str(ready_path),
            "caption_file": str(caption_file),
            "caption": caption,
            "folder": str(self.ready_folder)
        }
    
    def create_upload_batch(self, videos_data):
        """Prepare multiple videos for batch upload
        
        videos_data: list of {video, agent_type, caption}
        """
        batch_dir = self.ready_folder / f"batch_{datetime.now().strftime('%m%d_%H%M')}"
        batch_dir.mkdir(exist_ok=True)
        
        packages = []
        
        for i, data in enumerate(videos_data):
            video_path = Path(data["video"])
            
            if not video_path.exists():
                continue
            
            # Create numbered package
            pkg_dir = batch_dir / f"post_{i+1:02d}"
            pkg_dir.mkdir(exist_ok=True)
            
            # Copy video
            shutil.copy2(video_path, pkg_dir / "video.mp4")
            
            # Save caption + hashtags
            with open(pkg_dir / "caption.txt", 'w') as f:
                f.write(data.get("caption", ""))
                f.write("\n\n")
                f.write(data.get("hashtags", "#AI #Agents #Automation"))
            
            # Save metadata
            with open(pkg_dir / "meta.json", 'w') as f:
                json.dump({
                    "agent_type": data.get("agent_type"),
                    "created": datetime.now().isoformat(),
                    "index": i + 1
                }, f, indent=2)
            
            packages.append(str(pkg_dir))
        
        return {
            "status": "success",
            "batch_dir": str(batch_dir),
            "packages": packages,
            "count": len(packages)
        }
    
    def generate_shareable_link(self, video_path):
        """Generate a share link (for cloud storage)"""
        # Future: Upload to cloud, generate shareable link
        return {
            "status": "pending",
            "message": "Configure cloud storage for shareable links"
        }
    
    def send_to_telegram(self, video_path, caption=""):
        """Send video directly via Telegram bot"""
        if not self.telegram_ready:
            return {
                "status": "error",
                "message": "Telegram bot not configured. Run: ~/mortimer/telegram/setup.sh"
            }
        
        # Read bot config
        bot_config = Path("~/.telegram-bot/config.json").expanduser()
        with open(bot_config) as f:
            config = json.load(f)
        
        import requests
        
        bot_token = config.get("bot_token", "")
        chat_id = config.get("chat_id", "")
        
        if not bot_token or not chat_id:
            return {"status": "error", "message": "Bot config incomplete"}
        
        video_path = Path(video_path)
        if not video_path.exists():
            return {"status": "error", "message": "Video not found"}
        
        # Send video via Telegram Bot API
        url = f"https://api.telegram.org/bot{bot_token}/sendVideo"
        
        with open(video_path, 'rb') as f:
            files = {'video': f}
            data = {
                'chat_id': chat_id,
                'caption': caption[:1024],  # Telegram caption limit
                'supports_streaming': True
            }
            
            try:
                response = requests.post(url, files=files, data=data, timeout=60)
                result = response.json()
                
                if result.get('ok'):
                    return {
                        "status": "sent",
                        "message": "Video sent to Telegram!",
                        "file_id": result['result']['video']['file_id']
                    }
                else:
                    return {
                        "status": "error",
                        "message": result.get('description', 'Unknown error')
                    }
            except Exception as e:
                return {"status": "error", "message": str(e)}
    
    def get_queue(self):
        """Get list of videos ready for upload"""
        videos = list(self.ready_folder.glob("tiktok_*.mp4"))
        captions = list(self.ready_folder.glob("tiktok_*_caption.txt"))
        
        queue = []
        for v in sorted(videos):
            timestamp = v.stem.replace("tiktok_", "")
            cap_file = self.ready_folder / f"tiktok_{timestamp}_caption.txt"
            
            caption = ""
            if cap_file.exists():
                caption = cap_file.read_text()
            
            queue.append({
                "video": str(v),
                "caption": caption,
                "size": v.stat().st_size,
                "created": datetime.fromtimestamp(v.stat().st_mtime).isoformat()
            })
        
        return queue


def main():
    import sys
    
    delivery = TikTokDelivery()
    
    print("📱 TIKTOK DELIVERY PIPELINE")
    print("=" * 50)
    
    print(f"\n📂 Ready Folder: {delivery.ready_folder}")
    print(f"📨 Telegram: {'✅ Ready' if delivery.telegram_ready else '❌ Not configured'}")
    
    print("\n📋 Queue:")
    queue = delivery.get_queue()
    
    if queue:
        for item in queue:
            size_mb = item['size'] / 1024 / 1024
            print(f"  • {Path(item['video']).name} ({size_mb:.1f}MB)")
    else:
        print("  No videos in queue")
    
    if "--send" in sys.argv:
        # Send first video to Telegram
        if queue:
            result = delivery.send_to_telegram(
                queue[0]['video'],
                queue[0]['caption']
            )
            print(f"\n{result}")
        else:
            print("\nNo videos to send")


if __name__ == "__main__":
    main()
