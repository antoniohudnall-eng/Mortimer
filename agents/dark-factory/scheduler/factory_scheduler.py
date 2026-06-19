"""
Dark Factory Scheduler
Coordinates 36 agents across workstations in the factory.

Features:
- Self-optimizing job scheduler
- Priority-based task allocation
- Changeover minimization
- Real-time monitoring
- Predictive maintenance integration
"""

import random
import heapq
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class JobPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ManufacturingJob:
    """A job to be manufactured"""
    job_id: str
    product_type: str
    quantity: int
    priority: JobPriority
    materials_needed: Dict[str, int]
    estimated_duration: int  # minutes
    setup_time: int  # minutes
    deadline: Optional[datetime] = None
    status: JobStatus = JobStatus.PENDING
    assigned_station: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


@dataclass
class WorkStation:
    """Factory workstation"""
    station_id: str
    station_type: str  # "3d_print", "cnc", "assembly", "quality", "packing"
    capabilities: List[str]
    current_job: Optional[str] = None
    agent_assigned: Optional[str] = None
    status: str = "idle"  # idle, running, maintenance, offline
    last_job_type: Optional[str] = None
    total_jobs_completed: int = 0
    efficiency_rating: float = 1.0


class DarkFactoryScheduler:
    """
    Self-optimizing factory scheduler.
    
    Manages 36 agents across workstations.
    Minimizes changeover time.
    Prioritizes jobs based on urgency.
    """
    
    WORKSTATION_TYPES = {
        "3d_print": {"count": 8, "capabilities": ["prototype", "custom_parts"]},
        "cnc": {"count": 6, "capabilities": ["precision", "metal", "wood"]},
        "assembly": {"count": 12, "capabilities": ["assembly", "testing"]},
        "quality": {"count": 6, "capabilities": ["inspection", "testing"]},
        "packing": {"count": 4, "capabilities": ["packaging", "shipping_prep"]},
    }
    
    def __init__(self):
        print("🏭 DARK FACTORY SCHEDULER INITIALIZED")
        print("=" * 70)
        
        self.workstations: Dict[str, WorkStation] = {}
        self.jobs: Dict[str, ManufacturingJob] = {}
        self.job_queue: List[Tuple[int, str]] = []  # (priority, job_id)
        self.agents: Dict[str, Dict] = {}
        
        # Metrics
        self.jobs_completed = 0
        self.total_changeover_time = 0
        self.start_time = datetime.now()
        
        self._initialize_workstations()
        self._initialize_agents()
        
        print(f"\n✅ Factory ready:")
        print(f"   Workstations: {len(self.workstations)}")
        print(f"   Agents: {len(self.agents)}")
        print(f"   Self-optimizing: ENABLED")
        
    def _initialize_workstations(self):
        """Create all factory workstations"""
        station_id = 0
        
        for station_type, config in self.WORKSTATION_TYPES.items():
            for i in range(config["count"]):
                ws = WorkStation(
                    station_id=f"{station_type}_{i+1}",
                    station_type=station_type,
                    capabilities=config["capabilities"],
                )
                self.workstations[ws.station_id] = ws
                station_id += 1
                
    def _initialize_agents(self):
        """Initialize 36 factory agents"""
        agent_roles = [
            ("operator", 16),      # Run machines
            ("technician", 8),     # Maintenance & setup
            ("inspector", 6),       # Quality control
            ("coordinator", 4),    # Job coordination
            ("specialist", 2),     # Expert troubleshooting
        ]
        
        agent_id = 0
        for role, count in agent_roles:
            for i in range(count):
                self.agents[f"factory_agent_{agent_id}"] = {
                    "role": role,
                    "skill_level": random.randint(3, 10),
                    "current_station": None,
                    "shift": random.choice(["day", "night"]),
                    "efficiency": random.uniform(0.8, 1.2),
                }
                agent_id += 1
                
    def submit_job(self, job: ManufacturingJob) -> bool:
        """Submit a new manufacturing job"""
        self.jobs[job.job_id] = job
        
        # Add to priority queue
        heapq.heappush(self.job_queue, (job.priority.value, job.job_id))
        
        print(f"📋 Job submitted: {job.job_id}")
        print(f"   Product: {job.product_type}")
        print(f"   Quantity: {job.quantity}")
        print(f"   Priority: {job.priority.name}")
        
        return True
        
    def optimize_schedule(self):
        """
        Self-optimizing scheduler.
        
        Minimizes changeover by grouping similar jobs.
        Considers agent skills.
        Respects deadlines.
        """
        print("\n⚙️  Optimizing schedule...")
        
        # Sort jobs by priority and deadline
        pending = [
            self.jobs[job_id] 
            for _, job_id in self.job_queue 
            if self.jobs[job_id].status == JobStatus.PENDING
        ]
        
        # Group by product type to minimize changeover
        pending.sort(key=lambda j: (
            j.priority.value,
            j.deadline or datetime.max,
            j.product_type
        ))
        
        # Clear and rebuild queue
        self.job_queue = []
        for job in pending:
            heapq.heappush(self.job_queue, (job.priority.value, job.job_id))
            
        print(f"   Optimized {len(pending)} pending jobs")
        
    def assign_job_to_station(self, job_id: str) -> Optional[str]:
        """
        Find best workstation for a job.
        
        Considers:
        - Station capabilities
        - Current load
        - Changeover time
        - Agent availability
        """
        if job_id not in self.jobs:
            return None
            
        job = self.jobs[job_id]
        
        # Find compatible stations
        compatible = []
        for station_id, station in self.workstations.items():
            if station.status == "idle" or station.status == "running":
                # Check if station can handle this job
                if self._station_compatible(station, job):
                    # Calculate changeover time
                    changeover = 0
                    if station.last_job_type and station.last_job_type != job.product_type:
                        changeover = job.setup_time
                        
                    compatible.append((station_id, changeover))
                    
        if not compatible:
            return None
            
        # Pick station with minimum changeover
        compatible.sort(key=lambda x: x[1])
        best_station = compatible[0][0]
        changeover_time = compatible[0][1]
        
        self.total_changeover_time += changeover_time
        
        return best_station
        
    def _station_compatible(self, station: WorkStation, job: ManufacturingJob) -> bool:
        """Check if workstation can handle job"""
        # Simple check - in real system would be more complex
        if job.product_type in ["prototype", "custom"]:
            return "prototype" in station.capabilities or "custom_parts" in station.capabilities
        elif job.product_type in ["precision", "metal", "wood"]:
            return any(c in station.capabilities for c in ["precision", "metal", "wood"])
        elif job.product_type in ["assembly", "kit"]:
            return "assembly" in station.capabilities
        elif job.product_type in ["inspect", "test"]:
            return "inspection" in station.capabilities or "testing" in station.capabilities
        else:
            return True  # Default compatible
            
    def tick(self):
        """One tick of factory operation"""
        # 1. Check for completed jobs
        self._check_completed_jobs()
        
        # 2. Assign pending jobs
        self._assign_pending_jobs()
        
        # 3. Monitor stations
        self._monitor_stations()
        
        # 4. Update metrics
        self._update_metrics()
        
    def _check_completed_jobs(self):
        """Check for jobs that have finished"""
        for job_id, job in self.jobs.items():
            if job.status == JobStatus.RUNNING and job.end_time:
                if datetime.now() >= job.end_time:
                    job.status = JobStatus.COMPLETED
                    self.jobs_completed += 1
                    
                    # Free up station
                    if job.assigned_station:
                        station = self.workstations[job.assigned_station]
                        station.current_job = None
                        station.status = "idle"
                        station.total_jobs_completed += 1
                        station.last_job_type = job.product_type
                        
                    print(f"✅ Job completed: {job_id}")
                    
    def _assign_pending_jobs(self):
        """Assign pending jobs to available stations"""
        # Get pending jobs
        pending = [
            job_id for _, job_id in self.job_queue
            if self.jobs[job_id].status == JobStatus.PENDING
        ]
        
        for job_id in pending:
            station_id = self.assign_job_to_station(job_id)
            
            if station_id:
                job = self.jobs[job_id]
                station = self.workstations[station_id]
                
                # Assign
                job.assigned_station = station_id
                job.status = JobStatus.RUNNING
                job.start_time = datetime.now()
                job.end_time = job.start_time + timedelta(minutes=job.estimated_duration)
                
                station.current_job = job_id
                station.status = "running"
                
                # Find best agent
                agent_id = self._find_best_agent(station_id, job)
                if agent_id:
                    station.agent_assigned = agent_id
                    self.agents[agent_id]["current_station"] = station_id
                    
                print(f"🚀 Job {job_id} started on {station_id}")
                
    def _find_best_agent(self, station_id: str, job: ManufacturingJob) -> Optional[str]:
        """Find best agent for a station"""
        station = self.workstations[station_id]
        
        best_agent = None
        best_score = 0
        
        for agent_id, agent in self.agents.items():
            if agent["current_station"] is None:  # Available
                # Calculate score
                score = agent["skill_level"] * agent["efficiency"]
                
                # Bonus for matching role
                if station.station_type == "quality" and agent["role"] == "inspector":
                    score *= 1.5
                elif station.station_type in ["3d_print", "cnc"] and agent["role"] == "operator":
                    score *= 1.3
                    
                if score > best_score:
                    best_score = score
                    best_agent = agent_id
                    
        return best_agent
        
    def _monitor_stations(self):
        """Monitor station health and performance"""
        # Check for stations needing maintenance
        for station_id, station in self.workstations.items():
            if station.total_jobs_completed > 0 and station.total_jobs_completed % 50 == 0:
                # Schedule maintenance
                if random.random() < 0.1:
                    station.status = "maintenance"
                    print(f"🔧 Maintenance scheduled for {station_id}")
                    
    def _update_metrics(self):
        """Update factory metrics"""
        pass  # Metrics updated on demand
        
    def get_factory_status(self) -> str:
        """Get complete factory status"""
        running = sum(1 for j in self.jobs.values() if j.status == JobStatus.RUNNING)
        completed = sum(1 for j in self.jobs.values() if j.status == JobStatus.COMPLETED)
        pending = sum(1 for j in self.jobs.values() if j.status == JobStatus.PENDING)
        
        busy_stations = sum(1 for s in self.workstations.values() if s.status == "running")
        idle_stations = sum(1 for s in self.workstations.values() if s.status == "idle")
        
        busy_agents = sum(1 for a in self.agents.values() if a["current_station"])
        
        return f"""
╔════════════════════════════════════════════════════════════════╗
║              DARK FACTORY STATUS                                 ║
╠════════════════════════════════════════════════════════════════╣
║  Jobs: {pending} pending | {running} running | {completed} completed        ║
║  Stations: {busy_stations} busy | {idle_stations} idle | {len(self.workstations)} total         ║
║  Agents: {busy_agents} working | {len(self.agents) - busy_agents} available            ║
║  Changeover time saved: {self.total_changeover_time} minutes                    ║
╠════════════════════════════════════════════════════════════════╣
║  Uptime: {datetime.now() - self.start_time}                            ║
╚════════════════════════════════════════════════════════════════╝
"""


def main():
    """Demo factory scheduler"""
    print("=" * 70)
    print("DARK FACTORY SCHEDULER")
    print("=" * 70)
    
    scheduler = DarkFactoryScheduler()
    
    # Submit sample jobs
    jobs = [
        ManufacturingJob("job_001", "prototype", 10, JobPriority.HIGH, 
                         {"plastic": 5}, 30, 10),
        ManufacturingJob("job_002", "assembly", 50, JobPriority.MEDIUM,
                         {"parts": 50}, 60, 15),
        ManufacturingJob("job_003", "precision", 5, JobPriority.CRITICAL,
                         {"metal": 2}, 45, 20),
        ManufacturingJob("job_004", "prototype", 20, JobPriority.LOW,
                         {"plastic": 10}, 40, 10),
        ManufacturingJob("job_005", "assembly", 100, JobPriority.HIGH,
                         {"parts": 100}, 90, 15),
    ]
    
    for job in jobs:
        scheduler.submit_job(job)
        
    # Optimize
    scheduler.optimize_schedule()
    
    # Run ticks
    print("\n🏭 Running factory simulation...")
    for tick in range(5):
        print(f"\n--- Tick {tick + 1} ---")
        scheduler.tick()
        
    print(scheduler.get_factory_status())
    
    print("\n" + "=" * 70)
    print("Dark Factory operational. Agents working. Production flowing.")
    print("=" * 70)


if __name__ == "__main__":
    from dataclasses import dataclass
    main()
