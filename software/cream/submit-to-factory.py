#!/usr/bin/env python3
"""
Submit CREAM Standalone build job to Dark Factory
"""
import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

# Database path
DB_PATH = "/var/lib/dark_factory/jobs.db"

# Job data
job = {
    "id": None,  # Auto-generated
    "product_type": "multi_platform_build",
    "name": "CREAM-Standalone-Build",
    "description": "Build CREAM PIM - Time & Chaos Clone for Desktop (.exe) and Mobile (.apk)",
    "priority": 1,  # HIGH
    "status": "pending",
    "data": {
        "desktop": {
            "type": "desktop_app",
            "platform": "windows",
            "format": ".exe",
            "source": "/root/.openclaw/workspace/cream-standalone/desktop",
            "build_tool": "tauri",
            "features": [
                "Contacts Management",
                "Calendar (Day/Week/Month views)",
                "Task Management",
                "Project Management",
                "Import/Export CSV/JSON",
                "Duplicate Finder",
                "Data Backup/Restore"
            ]
        },
        "mobile": {
            "type": "mobile_app",
            "platform": "android",
            "format": ".apk",
            "source": "/root/.openclaw/workspace/cream-standalone/mobile",
            "build_tool": "react_native",
            "features": [
                "Contacts Management",
                "Calendar View",
                "Task Management",
                "Project Management",
                "Offline Data Storage",
                "Quick Search"
            ]
        }
    },
    "created_at": datetime.now().isoformat(),
    "started_at": None,
    "completed_at": None,
    "assigned_to": None,
    "result": None
}

# Ensure database exists
def ensure_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_type TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            priority INTEGER DEFAULT 3,
            status TEXT DEFAULT 'pending',
            data TEXT,
            created_at TEXT,
            started_at TEXT,
            completed_at TEXT,
            assigned_to TEXT,
            result TEXT
        )
    """)
    conn.commit()
    conn.close()

def submit_job():
    ensure_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO jobs (product_type, name, description, priority, status, data, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        job["product_type"],
        job["name"],
        job["description"],
        job["priority"],
        job["status"],
        json.dumps(job["data"]),
        job["created_at"]
    ))
    
    job_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return job_id

if __name__ == "__main__":
    print("🍦 Submitting CREAM Standalone build to Dark Factory...")
    print()
    
    try:
        job_id = submit_job()
        print(f"✅ Job submitted successfully!")
        print(f"   Job ID: {job_id}")
        print(f"   Name: CREAM-Standalone-Build")
        print(f"   Priority: HIGH (1)")
        print(f"   Status: PENDING")
        print()
        print("📦 Build Targets:")
        print("   - Desktop: Windows .exe (Tauri)")
        print("   - Mobile: Android .apk (React Native)")
        print()
        print("📁 Source Locations:")
        print(f"   - Desktop: /root/.openclaw/workspace/cream-standalone/desktop")
        print(f"   - Mobile: /root/.openclaw/workspace/cream-standalone/mobile")
        print(f"   - Shared: /root/.openclaw/workspace/cream-standalone/shared")
        print()
        print("⏱️  The Dark Factory will process this job in the next tick cycle.")
        
    except Exception as e:
        print(f"❌ Error submitting job: {e}")
        exit(1)