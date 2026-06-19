"""
Persistent Job Queue for Dark Factory
Ensures jobs survive restarts and are processed reliably.
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import asdict


class PersistentJobQueue:
    """SQLite-backed job queue for durability."""
    
    def __init__(self, db_path: str = "/var/lib/dark_factory/jobs.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        
    def _init_db(self):
        """Initialize SQLite tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    product_type TEXT,
                    quantity INTEGER,
                    priority INTEGER,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    assigned_station TEXT,
                    data JSON
                )
            """)
            conn.commit()
            
    def enqueue(self, job) -> bool:
        """Add job to queue."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """INSERT INTO jobs 
                       (job_id, product_type, quantity, priority, status, data)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (job.job_id, job.product_type, job.quantity, 
                     job.priority.value, "pending", json.dumps(asdict(job)))
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Queue error: {e}")
            return False
            
    def dequeue(self) -> Optional[Dict]:
        """Get next pending job."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """SELECT job_id, data FROM jobs 
                   WHERE status = 'pending'
                   ORDER BY priority ASC, created_at ASC
                   LIMIT 1"""
            )
            row = cursor.fetchone()
            if row:
                job_id, data = row
                conn.execute(
                    "UPDATE jobs SET status = 'running', started_at = CURRENT_TIMESTAMP WHERE job_id = ?",
                    (job_id,)
                )
                conn.commit()
                return json.loads(data)
            return None
            
    def complete(self, job_id: str) -> bool:
        """Mark job as completed."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """UPDATE jobs 
                       SET status = 'completed', completed_at = CURRENT_TIMESTAMP 
                       WHERE job_id = ?""",
                    (job_id,)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Complete error: {e}")
            return False
            
    def get_stats(self) -> Dict:
        """Get queue statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """SELECT status, COUNT(*) FROM jobs GROUP BY status"""
            )
            stats = dict(cursor.fetchall())
            return {
                "pending": stats.get("pending", 0),
                "running": stats.get("running", 0),
                "completed": stats.get("completed", 0),
                "failed": stats.get("failed", 0),
            }
