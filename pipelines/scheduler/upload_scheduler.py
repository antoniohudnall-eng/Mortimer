#!/usr/bin/env python3
"""
📤 UPLOAD SCHEDULER - Execute scheduled uploads
Run via cron every hour
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scheduler import ContentScheduler
from platforms.tiktok_uploader import MultiPlatformUploader

def check_and_upload():
    """Check for due uploads and execute them"""
    scheduler = ContentScheduler()
    uploader = MultiPlatformUploader()
    
    now = datetime.now()
    due_items = []
    
    for item in scheduler.schedule["scheduled"]:
        if item["status"] != "pending":
            continue
        
        scheduled = datetime.fromisoformat(item["scheduled_time"])
        
        # Check if within 5 minute window
        if abs((now - scheduled).total_seconds()) <= 300:
            due_items.append(item)
    
    results = []
    for item in due_items:
        video_path = Path(item["video"])
        
        if not video_path.exists():
            results.append({
                "item": item,
                "status": "error",
                "message": "Video not found"
            })
            continue
        
        # Upload to platform
        platform = item["platform"]
        
        if platform in uploader.uploaders:
            result = uploader.uploaders[platform].upload_video(
                video_path,
                item["caption"]
            )
            results.append({
                "item": item,
                "status": result.get("status"),
                "result": result
            })
            
            # Mark as completed
            item["status"] = "completed"
            item["completed_at"] = now.isoformat()
        else:
            results.append({
                "item": item,
                "status": "skipped",
                "message": f"Platform {platform} not configured"
            })
    
    scheduler._save_schedule()
    
    return results


if __name__ == "__main__":
    if "--check" in sys.argv:
        results = check_and_upload()
        if results:
            print(json.dumps(results, indent=2))
        else:
            print("No uploads due")
    else:
        print("Usage: python3 upload_scheduler.py --check")
