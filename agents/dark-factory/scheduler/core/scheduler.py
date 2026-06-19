"""
Dark Factory Scheduler - Complete System
Coordinates 36 agents across 36 workstations.
"""

import random
import sqlite3
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path


class WorkStation:
    """Factory workstation"""
    def __init__(self, station_id: str, station_type: str):
        self.station_id = station_id
        self.station_type = station_type
        self.status = "idle"
        self.current_job = None
        self.agent_assigned = None
        self.jobs_completed = 0
        self.efficiency = 1.0
        self.last_maintenance = datetime.now()


class DarkFactoryScheduler:
    """Complete factory scheduler with AGI Connect integration"""
    
    def __init__(self):
        self.workstations: Dict[str, WorkStation] = {}
        self.agents: Dict[str, Dict] = {}
        self.db_path = Path("/var/lib/dark_factory/scheduler.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._init_workstations()
        self._init_agents()
        self._init_db()
        
        print("🏭 Dark Factory Scheduler v2.0 Initialized")
        print(f"   Workstations: {len(self.workstations)}")
        print(f"   Agents: {len(self.agents)}")
        
    def _init_workstations(self):
        """Create 36 workstations"""
        station_types = {
            "3d_print": 8,
            "cnc": 6,
            "assembly": 12,
            "quality": 6,
            "packing": 4,
        }
        
        for stype, count in station_types.items():
            for i in range(count):
                ws = WorkStation(f"{stype}_{i+1}", stype)
                self.workstations[ws.station_id] = ws
                
    def _init_agents(self):
        """Create 36 factory agents"""
        roles = [("operator", 16), ("technician", 8), ("inspector", 6), ("coordinator", 4), ("specialist", 2)]
        
        agent_id = 0
        for role, count in roles:
            for i in range(count):
                self.agents[f"factory_{agent_id}"] = {
                    "role": role,
                    "skill": random.randint(5, 10),
                    "station": None,
                }
                agent_id += 1
                
    def _init_db(self):
        """Initialize database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS production_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT,
                    station_id TEXT,
                    agent_id TEXT,
                    product_type TEXT,
                    quantity INTEGER,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    quality_score REAL
                )
            """)
            conn.commit()
            
    def assign_job(self, job_type: str, quantity: int, priority: int = 3) -> Optional[str]:
        """Assign job to best available workstation"""
        # Find idle station
        available = [ws for ws in self.workstations.values() if ws.status == "idle"]
        
        if not available:
            return None
            
        # Score stations
        scored = []
        for ws in available:
            score = ws.efficiency * 10
            if ws.station_type in ["3d_print", "cnc"] and job_type in ["prototype", "precision"]:
                score += 20
            scored.append((ws, score))
            
        scored.sort(key=lambda x: x[1], reverse=True)
        best = scored[0][0]
        
        # Find best agent
        best_agent = None
        best_skill = 0
        for agent_id, agent in self.agents.items():
            if agent["station"] is None and agent["skill"] > best_skill:
                best_skill = agent["skill"]
                best_agent = agent_id
                
        if best_agent:
            self.agents[best_agent]["station"] = best.station_id
            best.agent_assigned = best_agent
            best.status = "running"
            
        return best.station_id
        
    def production_tick(self):
        """One production cycle"""
        for station in self.workstations.values():
            if station.status == "running":
                station.jobs_completed += 1
                
                # Check for maintenance
                if station.jobs_completed % 100 == 0:
                    station.status = "maintenance"
                    print(f"🔧 {station.station_id} scheduled for maintenance")
                    
    def get_dashboard(self) -> Dict:
        """Production dashboard data"""
        return {
            "workstations": {
                "total": len(self.workstations),
                "idle": sum(1 for w in self.workstations.values() if w.status == "idle"),
                "running": sum(1 for w in self.workstations.values() if w.status == "running"),
                "maintenance": sum(1 for w in self.workstations.values() if w.status == "maintenance"),
            },
            "agents": {
                "total": len(self.agents),
                "working": sum(1 for a in self.agents.values() if a["station"]),
                "available": sum(1 for a in self.agents.values() if not a["station"]),
            },
            "production": {
                "jobs_completed": sum(w.jobs_completed for w in self.workstations.values()),
            }
        }
        
    def predict_maintenance(self) -> List[str]:
        """Predict which stations need maintenance"""
        predictions = []
        for station in self.workstations.values():
            if station.jobs_completed > 0 and station.jobs_completed % 90 == 0:
                predictions.append(station.station_id)
        return predictions
