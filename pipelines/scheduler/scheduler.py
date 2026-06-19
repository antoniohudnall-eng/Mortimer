#!/usr/bin/env python3
"""
⏰ SCHEDULER - Automated posting schedule for all platforms
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import random

class ContentScheduler:
    """
    Schedule content across all platforms
    Best posting times based on platform analytics
    """
    
    # Best posting times (PST) by platform
    POSTING_SCHEDULE = {
        "tiktok": {
            "best_times": ["07:00", "11:00", "18:00", "21:00"],
            "posts_per_day": 3,
            "min_gap_hours": 3
        },
        "youtube_shorts": {
            "best_times": ["12:00", "15:00", "18:00"],
            "posts_per_day": 2,
            "min_gap_hours": 4
        },
        "instagram_reels": {
            "best_times": ["09:00", "12:00", "17:00"],
            "posts_per_day": 2,
            "min_gap_hours": 4
        },
        "twitter": {
            "best_times": ["08:00", "12:00", "17:00", "20:00"],
            "posts_per_day": 5,
            "min_gap_hours": 2
        },
        "linkedin": {
            "best_times": ["08:00", "12:00", "17:00"],
            "posts_per_day": 2,
            "min_gap_hours": 4
        },
        "facebook": {
            "best_times": ["09:00", "13:00", "18:00"],
            "posts_per_day": 2,
            "min_gap_hours": 4
        }
    }
    
    def __init__(self, schedule_file="~/.mortimer/content_schedule.json"):
        self.schedule_file = Path(schedule_file).expanduser()
        self.schedule_file.parent.mkdir(parents=True, exist_ok=True)
        self.schedule = self._load_schedule()
    
    def _load_schedule(self):
        if self.schedule_file.exists():
            with open(self.schedule_file) as f:
                return json.load(f)
        return {
            "scheduled": [],
            "completed": [],
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_schedule(self):
        self.schedule["last_updated"] = datetime.now().isoformat()
        with open(self.schedule_file, 'w') as f:
            json.dump(self.schedule, f, indent=2)
    
    def add_to_schedule(self, video_path, platforms, agent_type, caption=""):
        """Add content to schedule"""
        scheduled_items = []
        
        for platform in platforms:
            if platform in self.POSTING_SCHEDULE:
                times = self.POSTING_SCHEDULE[platform]["best_times"]
                # Get next available time slot
                next_time = self._get_next_slot(platform)
                
                scheduled_items.append({
                    "platform": platform,
                    "video": str(video_path),
                    "agent_type": agent_type,
                    "caption": caption,
                    "scheduled_time": next_time.isoformat(),
                    "status": "pending"
                })
        
        self.schedule["scheduled"].extend(scheduled_items)
        self._save_schedule()
        
        return scheduled_items
    
    def _get_next_slot(self, platform):
        """Find next available posting slot"""
        config = self.POSTING_SCHEDULE.get(platform, {})
        best_times = config.get("best_times", ["09:00", "18:00"])
        
        # Get existing scheduled posts for this platform
        existing = [p for p in self.schedule["scheduled"] 
                   if p["platform"] == platform and p["status"] == "pending"]
        
        now = datetime.now()
        
        for time_str in best_times:
            candidate = datetime.strptime(time_str, "%H:%M")
            candidate = now.replace(hour=candidate.hour, minute=candidate.minute)
            
            if candidate <= now:
                candidate += timedelta(days=1)
            
            # Check gap
            min_gap = timedelta(hours=config.get("min_gap_hours", 3))
            
            too_close = False
            for post in existing:
                post_time = datetime.fromisoformat(post["scheduled_time"])
                if abs(candidate - post_time) < min_gap:
                    too_close = True
                    break
            
            if not too_close:
                return candidate
        
        # Default to tomorrow at first slot
        tomorrow = now + timedelta(days=1)
        first_time = datetime.strptime(best_times[0], "%H:%M")
        return tomorrow.replace(hour=first_time.hour, minute=first_time.minute)
    
    def get_schedule(self, days=7):
        """Get upcoming schedule"""
        now = datetime.now()
        cutoff = now + timedelta(days=days)
        
        upcoming = []
        for item in self.schedule["scheduled"]:
            if item["status"] == "pending":
                scheduled = datetime.fromisoformat(item["scheduled_time"])
                if scheduled <= cutoff:
                    upcoming.append(item)
        
        return sorted(upcoming, key=lambda x: x["scheduled_time"])
    
    def mark_completed(self, scheduled_id):
        """Mark scheduled post as completed"""
        for item in self.schedule["scheduled"]:
            if item.get("id") == scheduled_id:
                item["status"] = "completed"
                item["completed_at"] = datetime.now().isoformat()
        
        self._save_schedule()
    
    def get_daily_plan(self):
        """Get today's posting plan"""
        today = datetime.now().date()
        today_posts = []
        
        for item in self.schedule["scheduled"]:
            scheduled = datetime.fromisoformat(item["scheduled_time"])
            if scheduled.date() == today and item["status"] == "pending":
                today_posts.append(item)
        
        return sorted(today_posts, key=lambda x: x["scheduled_time"])


class CronManager:
    """Manage cron jobs for automated pipeline execution"""
    
    def __init__(self):
        self.cron_file = Path("~/.mortimer/mortimer_crons").expanduser()
    
    def install_crons(self):
        """Install pipeline cron jobs"""
        crons = [
            # Generate new content every 6 hours
            "0 */6 * * * cd ~/mortimer/pipelines && python3 agent_sales_pipeline.py batch --count 2 >> ~/mortimer/logs/pipeline.log 2>&1",
            
            # Check and upload scheduled content every hour
            "0 * * * * cd ~/mortimer/pipelines && python3 scheduler/upload_scheduler.py --check >> ~/mortimer/logs/scheduler.log 2>&1",
            
            # Voice check every morning
            "0 7 * * * cd ~/mortimer/pipelines && python3 agent_sales_pipeline.py voice --agent sales >> ~/mortimer/logs/voice.log 2>&1"
        ]
        
        self.cron_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cron_file, 'w') as f:
            f.write("\n".join(crons))
        
        # Install to crontab
        subprocess.run(f"crontab {self.cron_file}", shell=True)
        
        return crons
    
    def list_crons(self):
        """List current cron jobs"""
        result = subprocess.run("crontab -l", shell=True, capture_output=True, text=True)
        return result.stdout or "No crontab installed"


if __name__ == "__main__":
    scheduler = ContentScheduler()
    
    print("📅 CONTENT SCHEDULER")
    print("=" * 40)
    
    print("\n📆 Today's Plan:")
    today = scheduler.get_daily_plan()
    if today:
        for item in today:
            time = datetime.fromisoformat(item["scheduled_time"]).strftime("%H:%M")
            print(f"  {time} | {item['platform']} | {item['agent_type']}")
    else:
        print("  No posts scheduled today")
    
    print("\n📆 This Week:")
    week = scheduler.get_schedule(7)
    print(f"  {len(week)} posts scheduled")
    
    print("\n⏰ Best Posting Times:")
    for platform, config in ContentScheduler.POSTING_SCHEDULE.items():
        times = ", ".join(config["best_times"])
        print(f"  {platform}: {times}")
