#!/usr/bin/env python3
"""
📱 TIKTOK UPLOADER - Automated posting to TikTok
Uses TikTok APIs or browser automation
"""

import os
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import random

class TikTokUploader:
    def __init__(self, config_path="~/.mortimer/tiktok_config.json"):
        self.config_path = Path(config_path).expanduser()
        self.config = self._load_config()
        self.upload_log = Path("~/.mortimer/tiktok_log.json").expanduser()
        
    def _load_config(self):
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return {
            "cookies": "",
            "csrf_token": "",
            "upload_times": ["09:00", "12:00", "18:00", "21:00"],
            "max_daily": 5
        }
    
    def _save_config(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _log_upload(self, video_path, status, message=""):
        """Log upload attempt"""
        log = []
        if self.upload_log.exists():
            with open(self.upload_log) as f:
                log = json.load(f)
        
        log.append({
            "timestamp": datetime.now().isoformat(),
            "video": str(video_path),
            "status": status,
            "message": message
        })
        
        # Ensure directory exists
        self.upload_log.parent.mkdir(parents=True, exist_ok=True)
        with open(self.upload_log, 'w') as f:
            json.dump(log, f, indent=2)
    
    def generate_caption(self, agent_type, hashtag_set=1):
        """Generate engaging TikTok caption"""
        captions = [
            f"Meet your new {agent_type} agent 🤖 #AI #AgentLife #WorkSmarter",
            f"This {agent_type} agent works 24/7 for you 💪 #FutureOfWork #Automation",
            f"Stop hiring. Start deploying AI agents 🛑 #Entrepreneur #SideHustle",
            f"My AI workforce just expanded 🚀 #AIAgents #BusinessGrowth",
            f"Who needs employees when you have agents? 👀 #ChatGPT #Productivity"
        ]
        
        hashtags = [
            "#AI #Agents #Automation #Business #Entrepreneur",
            "#FutureOfWork #WorkSmarter #AIAgents #Startup",
            "#ChatGPT #ProductivityHacks #SideHustle #BusinessGrowth"
        ]
        
        return random.choice(captions) + "\n\n" + random.choice(hashtags)
    
    def schedule_upload(self, video_path, agent_type, target_times=None):
        """Schedule video for upload"""
        if target_times is None:
            target_times = self.config.get("upload_times", ["09:00", "18:00"])
        
        # For now, just log it - actual scheduling would need TikTok API
        self._log_upload(video_path, "scheduled", f"Agent: {agent_type}")
        
        return {
            "status": "scheduled",
            "video": str(video_path),
            "agent_type": agent_type,
            "scheduled_times": target_times
        }
    
    def upload_video(self, video_path, caption, privacy="public"):
        """Upload video to TikTok
        
        NOTE: TikTok requires browser-based auth. This is a template
        for automated posting via Selenium or TikTok's Creator API.
        """
        video_path = Path(video_path)
        
        if not video_path.exists():
            return {"status": "error", "message": "Video not found"}
        
        # Check if we have TikTok session cookies
        if not self.config.get("cookies"):
            return {
                "status": "needs_auth",
                "message": "TikTok session required. See AUTH_SETUP.md"
            }
        
        # This would use TikTok's API or Selenium automation
        # For now, return upload info
        return {
            "status": "ready",
            "video": str(video_path),
            "caption": caption,
            "privacy": privacy,
            "note": "Automated upload ready - configure TikTok API credentials"
        }
    
    def upload_batch(self, videos, stagger_minutes=30):
        """Upload multiple videos with time staggering"""
        results = []
        base_time = datetime.now()
        
        for i, (video_path, agent_type) in enumerate(videos):
            scheduled_time = base_time + timedelta(minutes=i * stagger_minutes)
            
            caption = self.generate_caption(agent_type)
            result = self.schedule_upload(video_path, agent_type)
            result["scheduled_datetime"] = scheduled_time.isoformat()
            
            results.append(result)
        
        return results


class MultiPlatformUploader:
    """Unified uploader for all social platforms"""
    
    PLATFORMS = ["tiktok", "youtube_shorts", "instagram_reels", "twitter", "linkedin", "facebook"]
    
    def __init__(self):
        self.uploaders = {
            "tiktok": TikTokUploader()
        }
        # Other platform uploaders would be initialized here
    
    def upload_all(self, video_path, agent_type, platforms=None):
        """Upload to multiple platforms"""
        if platforms is None:
            platforms = self.PLATFORMS
        
        results = {}
        for platform in platforms:
            if platform in self.uploaders:
                uploader = self.uploaders[platform]
                caption = self.generate_caption(agent_type, platform)
                results[platform] = uploader.upload_video(video_path, caption)
            else:
                results[platform] = {"status": "not_configured"}
        
        return results
    
    def generate_caption(self, agent_type, platform):
        """Platform-specific caption"""
        base = f"Your AI {agent_type} agent is ready 🤖"
        
        platform_captions = {
            "tiktok": base + " #AI #Agents #WorkSmarter",
            "youtube_shorts": base + " | Full demo in description",
            "instagram_reels": base + " 🚀",
            "twitter": base + " Thread 🧵👇",
            "linkedin": base + " Let's discuss the future of work.",
            "facebook": base + " What do you think?"
        }
        
        return platform_captions.get(platform, base)


if __name__ == "__main__":
    uploader = TikTokUploader()
    
    # Test caption generation
    print("Caption Preview:")
    print(uploader.generate_caption("sales"))
    
    print("\nUpload Status: Ready (needs TikTok auth)")
