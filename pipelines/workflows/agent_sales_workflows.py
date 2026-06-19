#!/usr/bin/env python3
"""
⚡ AGENT SALES WORKFLOWS - Temporal-style Durable Execution
Handles content pipeline with retry, persistence, and async operations
"""

import os
import sys
import json
import time
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import uuid

class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"

@dataclass
class WorkflowExecution:
    id: str
    name: str
    status: WorkflowStatus
    input_data: Dict
    result: Optional[Dict] = None
    error: Optional[str] = None
    attempts: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    scheduled_at: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

class SimpleWorkflowEngine:
    """
    Lightweight workflow engine with Temporal-like features:
    - Durable execution (persists to disk)
    - Retry with backoff
    - Activity functions
    - Scheduled execution
    - Event history
    """
    
    def __init__(self, state_dir="~/.mortimer/workflows"):
        self.state_dir = Path(state_dir).expanduser()
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.executions_file = self.state_dir / "executions.json"
        self.activity_log = self.state_dir / "activity.log"
        
        self.executions = self._load_executions()
    
    def _load_executions(self) -> Dict:
        if self.executions_file.exists():
            with open(self.executions_file) as f:
                return json.load(f)
        return {}
    
    def _save_executions(self):
        with open(self.executions_file, 'w') as f:
            json.dump(self.executions, f, indent=2)
    
    def _log_activity(self, workflow_id: str, activity: str, details: Dict = None):
        """Log activity to file"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "workflow_id": workflow_id,
            "activity": activity,
            "details": details or {}
        }
        with open(self.activity_log, 'a') as f:
            f.write(json.dumps(entry) + "\n")
    
    # ========== Workflow Management ==========
    
    def start_workflow(self, name: str, input_data: Dict) -> str:
        """Start a new workflow execution"""
        workflow_id = str(uuid.uuid4())[:8]
        
        execution = WorkflowExecution(
            id=workflow_id,
            name=name,
            status=WorkflowStatus.PENDING,
            input_data=input_data
        )
        
        self.executions[workflow_id] = {
            "id": execution.id,
            "name": execution.name,
            "status": execution.status.value,
            "input": execution.input_data,
            "attempts": execution.attempts,
            "created_at": execution.created_at
        }
        
        self._save_executions()
        self._log_activity(workflow_id, "workflow_started", {"name": name})
        
        return workflow_id
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict]:
        return self.executions.get(workflow_id)
    
    def list_workflows(self, status: str = None, limit: int = 50) -> List[Dict]:
        """List workflow executions"""
        workflows = list(self.executions.values())
        
        if status:
            workflows = [w for w in workflows if w["status"] == status]
        
        return sorted(workflows, key=lambda x: x["created_at"], reverse=True)[:limit]
    
    # ========== Activity Execution ==========
    
    def execute_activity(self, workflow_id: str, activity_name: str, 
                        activity_func, *args, **kwargs) -> Any:
        """Execute an activity within a workflow context"""
        self._log_activity(workflow_id, f"activity_start:{activity_name}")
        
        try:
            result = activity_func(*args, **kwargs)
            self._log_activity(workflow_id, f"activity_complete:{activity_name}", 
                             {"result": str(result)[:100]})
            return result
        except Exception as e:
            self._log_activity(workflow_id, f"activity_failed:{activity_name}", 
                             {"error": str(e)})
            raise
    
    def complete_workflow(self, workflow_id: str, result: Dict):
        """Mark workflow as completed"""
        if workflow_id in self.executions:
            self.executions[workflow_id]["status"] = WorkflowStatus.COMPLETED.value
            self.executions[workflow_id]["result"] = result
            self.executions[workflow_id]["completed_at"] = datetime.now().isoformat()
            self._save_executions()
            self._log_activity(workflow_id, "workflow_completed", result)
    
    def fail_workflow(self, workflow_id: str, error: str):
        """Mark workflow as failed"""
        if workflow_id in self.executions:
            self.executions[workflow_id]["status"] = WorkflowStatus.FAILED.value
            self.executions[workflow_id]["error"] = error
            self.executions[workflow_id]["completed_at"] = datetime.now().isoformat()
            self._save_executions()
            self._log_activity(workflow_id, "workflow_failed", {"error": error})
    
    def retry_workflow(self, workflow_id: str, max_attempts: int = 3) -> bool:
        """Retry a failed workflow"""
        exec_data = self.executions.get(workflow_id)
        if not exec_data:
            return False
        
        if exec_data["attempts"] >= max_attempts:
            return False
        
        exec_data["attempts"] += 1
        exec_data["status"] = WorkflowStatus.RETRYING.value
        exec_data["updated_at"] = datetime.now().isoformat()
        self._save_executions()
        
        self._log_activity(workflow_id, "workflow_retry", 
                          {"attempt": exec_data["attempts"]})
        return True


# ========== Pre-built Workflows ==========

class AgentSalesWorkflows:
    """
    Pre-built workflows for agent sales content pipeline
    """
    
    def __init__(self):
        self.engine = SimpleWorkflowEngine()
    
    # -------- Content Generation --------
    
    def create_agent_promo_workflow(self, agent_type: str, length: str = "medium") -> str:
        """Workflow: Generate agent promo video"""
        workflow_id = self.engine.start_workflow(
            "create_agent_promo",
            {"agent_type": agent_type, "length": length}
        )
        
        try:
            # Activity 1: Generate script
            self.engine._log_activity(workflow_id, "generating_script", 
                                     {"agent": agent_type})
            
            sys.path.insert(0, str(Path(__file__).parent))
            from content.content_templates import ContentGenerator
            
            gen = ContentGenerator()
            script = gen.generate_script(agent_type, length)
            
            # Activity 2: Create slides
            self.engine._log_activity(workflow_id, "creating_slides")
            
            from core.video_pipeline import VideoPipeline
            
            video_dir = Path("/storage/emulated/0/Movies/AgentSales")
            video_dir.mkdir(parents=True, exist_ok=True)
            
            pipeline = VideoPipeline(str(video_dir))
            
            slides = []
            colors = [(26, 26, 46), (20, 40, 60), (40, 20, 60), (30, 30, 50), (20, 60, 40)]
            
            for i, scene in enumerate(script["scenes"]):
                duration = scene["end"] - scene["start"]
                slides.append({
                    "text": scene["text"],
                    "bg_color": colors[i % len(colors)],
                    "duration": duration
                })
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_name = f"{agent_type}_agent_{timestamp}"
            video_path = pipeline.create_video_from_slides(slides, None, video_name)
            
            # Activity 3: Generate caption
            from content.content_templates import AGENT_SALES_TEMPLATES
            agent = script["agent"]
            import random
            
            caption = f"""
🚀 MEET YOUR NEW {agent['name'].upper()}

{agent['tagline']}

💰 ${agent['price']}/month

{chr(10).join(f'• {f}' for f in agent['features'][:3])}

{random.choice(AGENT_SALES_TEMPLATES['cta_phrases'])}

{script['hashtags']}
""".strip()
            
            # Complete
            result = {
                "video_path": video_path,
                "caption": caption,
                "agent": agent['name'],
                "scenes": len(slides)
            }
            
            self.engine.complete_workflow(workflow_id, result)
            return workflow_id
            
        except Exception as e:
            self.engine.fail_workflow(workflow_id, str(e))
            return workflow_id
    
    def batch_content_workflow(self, count: int, agents: List[str] = None) -> str:
        """Workflow: Generate batch of agent promos"""
        if agents is None:
            agents = ["sales", "support", "marketing", "operations", "research"]
        
        workflow_id = self.engine.start_workflow(
            "batch_content",
            {"count": count, "agents": agents}
        )
        
        import random
        
        try:
            created = []
            for i in range(count):
                agent = random.choice(agents)
                length = random.choice(["short", "medium", "long"])
                
                self.engine._log_activity(workflow_id, f"creating_promo_{i+1}", 
                                        {"agent": agent, "length": length})
                
                # Create single promo
                sub_workflow_id = self.create_agent_promo_workflow(agent, length)
                sub_result = self.engine.get_workflow(sub_workflow_id)
                
                if sub_result and sub_result.get("result"):
                    created.append(sub_result["result"])
            
            self.engine.complete_workflow(workflow_id, {
                "created_count": len(created),
                "videos": [c["video_path"] for c in created]
            })
            
        except Exception as e:
            self.engine.fail_workflow(workflow_id, str(e))
        
        return workflow_id
    
    # -------- Delivery --------
    
    def deliver_to_telegram_workflow(self, video_path: str, caption: str) -> str:
        """Workflow: Deliver video to Telegram"""
        workflow_id = self.engine.start_workflow(
            "deliver_telegram",
            {"video": video_path, "caption": caption[:100]}
        )
        
        try:
            # Check if Telegram is configured
            bot_config = Path("~/.telegram-bot/config.json").expanduser()
            
            if not bot_config.exists():
                raise Exception("Telegram bot not configured")
            
            with open(bot_config) as f:
                config = json.load(f)
            
            import requests
            
            # Send video
            url = f"https://api.telegram.org/bot{config['bot_token']}/sendVideo"
            
            with open(video_path, 'rb') as f:
                files = {'video': f}
                data = {
                    'chat_id': config['chat_id'],
                    'caption': caption[:1024]
                }
                
                response = requests.post(url, files=files, data=data, timeout=60)
                result = response.json()
                
                if result.get('ok'):
                    file_id = result['result']['video']['file_id']
                    self.engine.complete_workflow(workflow_id, {
                        "sent": True,
                        "file_id": file_id
                    })
                else:
                    raise Exception(result.get('description', 'Send failed'))
            
        except Exception as e:
            self.engine.fail_workflow(workflow_id, str(e))
        
        return workflow_id
    
    # -------- Scheduling --------
    
    def schedule_content_workflow(self, video_path: str, agent_type: str,
                                 post_time: str, platforms: List[str]) -> str:
        """Workflow: Schedule content for posting"""
        workflow_id = self.engine.start_workflow(
            "schedule_content",
            {"video": video_path, "agent": agent_type, "time": post_time, 
             "platforms": platforms}
        )
        
        from scheduler.scheduler import ContentScheduler
        
        scheduler = ContentScheduler()
        scheduled = scheduler.add_to_schedule(video_path, platforms, agent_type)
        
        self.engine.complete_workflow(workflow_id, {
            "scheduled": len(scheduled),
            "items": scheduled
        })
        
        return workflow_id
    
    # -------- Status --------
    
    def get_dashboard(self) -> Dict:
        """Get workflow dashboard"""
        all_workflows = self.engine.list_workflows(limit=100)
        
        completed = len([w for w in all_workflows if w["status"] == "completed"])
        failed = len([w for w in all_workflows if w["status"] == "failed"])
        pending = len([w for w in all_workflows if w["status"] == "pending"])
        running = len([w for w in all_workflows if w["status"] == "running"])
        
        # Check videos
        video_dir = Path("/storage/emulated/0/Movies/AgentSales")
        video_count = len(list(video_dir.glob("*.mp4"))) if video_dir.exists() else 0
        
        # Check schedule
        from scheduler.scheduler import ContentScheduler
        scheduler = ContentScheduler()
        upcoming = scheduler.get_schedule(7)
        
        return {
            "workflows": {
                "total": len(all_workflows),
                "completed": completed,
                "failed": failed,
                "pending": pending,
                "running": running
            },
            "content": {
                "videos_created": video_count,
                "scheduled_posts": len(upcoming)
            },
            "recent": all_workflows[:5]
        }


# ========== CLI ==========

def main():
    import argparse
    
    workflows = AgentSalesWorkflows()
    engine = workflows.engine
    
    parser = argparse.ArgumentParser(description="Agent Sales Workflows")
    subparsers = parser.add_subparsers(dest="command")
    
    # Create single promo
    create = subparsers.add_parser("create", help="Create agent promo")
    create.add_argument("--agent", default="sales", help="Agent type")
    create.add_argument("--length", default="medium", 
                       choices=["short", "medium", "long"])
    
    # Batch create
    batch = subparsers.add_parser("batch", help="Batch create promos")
    batch.add_argument("--count", type=int, default=5)
    batch.add_argument("--agents", nargs="+", 
                      default=["sales", "support", "marketing"])
    
    # Schedule
    schedule = subparsers.add_parser("schedule", help="Schedule content")
    schedule.add_argument("--video", required=True)
    schedule.add_argument("--agent", default="sales")
    schedule.add_argument("--time", default="18:00")
    schedule.add_argument("--platforms", nargs="+", default=["tiktok"])
    
    # List workflows
    list_parser = subparsers.add_parser("list", help="List workflows")
    list_parser.add_argument("--status", help="Filter by status")
    list_parser.add_argument("--limit", type=int, default=20)
    
    # Dashboard
    subparsers.add_parser("dashboard", help="Show workflow dashboard")
    
    args = parser.parse_args()
    
    if args.command == "create":
        wid = workflows.create_agent_promo_workflow(args.agent, args.length)
        result = engine.get_workflow(wid)
        print(f"✅ Workflow {wid} - {result['status']}")
        if result.get('result'):
            print(f"   Video: {result['result'].get('video_path')}")
    
    elif args.command == "batch":
        wid = workflows.batch_content_workflow(args.count, args.agents)
        result = engine.get_workflow(wid)
        print(f"✅ Batch Workflow {wid} - {result['status']}")
    
    elif args.command == "schedule":
        wid = workflows.schedule_content_workflow(
            args.video, args.agent, args.time, args.platforms
        )
        result = engine.get_workflow(wid)
        print(f"✅ Scheduled: {result['result']}")
    
    elif args.command == "list":
        for w in engine.list_workflows(args.status, args.limit):
            print(f"  [{w['status']}] {w['id']} - {w['name']} ({w['created_at'][:10]})")
    
    elif args.command == "dashboard":
        dash = workflows.get_dashboard()
        print("\n📊 WORKFLOW DASHBOARD")
        print("=" * 40)
        print(f"\n⚡ Workflows:")
        print(f"   Total: {dash['workflows']['total']}")
        print(f"   ✅ Completed: {dash['workflows']['completed']}")
        print(f"   ❌ Failed: {dash['workflows']['failed']}")
        print(f"   ⏳ Pending: {dash['workflows']['pending']}")
        print(f"\n📹 Content:")
        print(f"   Videos Created: {dash['content']['videos_created']}")
        print(f"   Scheduled Posts: {dash['content']['scheduled_posts']}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
