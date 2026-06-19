#!/usr/bin/env python3
"""
⚡ TEMPORAL-COMPATIBLE WORKFLOW ENGINE
Patricia-Approved Architecture for Agent Sales Pipeline

Patterns implemented:
- Durable execution with state persistence
- Activity functions with retry/backoff
- Workflow signals for human-in-loop
- Child workflows for fan-out
- Temporal-like API design
"""

import os
import sys
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any, Callable
from abc import ABC, abstractmethod
import uuid
import asyncio
import random

# ========== CONFIGURATION ==========

@dataclass
class RetryPolicy:
    """Temporal-style retry policy"""
    initial_interval: int = 1  # seconds
    backoff_coefficient: float = 2.0
    maximum_interval: int = 100
    max_attempts: int = 3
    non_retryable_errors: List[str] = field(default_factory=list)

@dataclass
class ActivityConfig:
    """Activity execution config"""
    name: str
    func: Callable
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    start_to_close_timeout: int = 300  # seconds
    schedule_to_start_timeout: int = 60

# ========== WORKFLOW STATE ==========

class WorkflowState(Enum):
    INIT = "init"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    CONTINUED_AS_NEW = "continued_as_new"

@dataclass
class ActivityResult:
    id: str
    name: str
    status: str  # scheduled, started, completed, failed
    result: Optional[Any] = None
    error: Optional[str] = None
    attempts: int = 0
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

@dataclass
class WorkflowExecution:
    # Identity
    id: str
    name: str
    type: str
    state: WorkflowState
    
    # Temporal-like fields
    status: Dict = field(default_factory=dict)
    input: Any = None
    result: Any = None
    error: Optional[str] = None
    
    # History
    events: List[Dict] = field(default_factory=list)
    activities: Dict[str, ActivityResult] = field(default_factory=dict)
    child_workflows: Dict[str, str] = field(default_factory=dict)
    
    # Signals queue
    signals: List[Dict] = field(default_factory=list)
    
    # Timing
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    # Retry state
    attempt: int = 1
    max_attempts: int = 1

# ========== ACTIVITY EXECUTOR ==========

class ActivityExecutor:
    """Executes activities with retry logic - Temporal pattern"""
    
    def __init__(self):
        self.activities: Dict[str, ActivityConfig] = {}
    
    def register(self, name: str, func: Callable, 
                 retry_policy: RetryPolicy = None,
                 timeout: int = 300):
        """Register an activity function"""
        self.activities[name] = ActivityConfig(
            name=name,
            func=func,
            retry_policy=retry_policy or RetryPolicy(),
            start_to_close_timeout=timeout
        )
    
    async def execute(self, name: str, *args, **kwargs) -> Any:
        """Execute activity with retries"""
        if name not in self.activities:
            raise ValueError(f"Activity '{name}' not registered")
        
        config = self.activities[name]
        policy = config.retry_policy
        
        last_error = None
        delay = policy.initial_interval
        
        for attempt in range(1, policy.max_attempts + 1):
            try:
                # Execute the activity
                if asyncio.iscoroutinefunction(config.func):
                    result = await config.func(*args, **kwargs)
                else:
                    result = config.func(*args, **kwargs)
                
                return result
                
            except Exception as e:
                last_error = e
                error_type = type(e).__name__
                
                # Check if non-retryable
                if error_type in policy.non_retryable_errors:
                    raise
                
                if attempt < policy.max_attempts:
                    # Wait with backoff
                    await asyncio.sleep(delay)
                    delay = min(delay * policy.backoff_coefficient, 
                              policy.maximum_interval)
        
        raise last_error

# ========== WORKFLOW ENGINE ==========

class TemporalWorkflowEngine:
    """
    Temporal-compatible workflow engine with:
    - Durable execution (persists to disk)
    - Activity registry with retry
    - Signal handling
    - Child workflow support
    - Event sourcing
    """
    
    def __init__(self, state_dir: str = "~/.mortimer/workflows"):
        self.state_dir = Path(state_dir).expanduser()
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        # Persistence
        self.workflows_file = self.state_dir / "workflows.json"
        self.history_dir = self.state_dir / "history"
        self.history_dir.mkdir(exist_ok=True)
        
        # Components
        self.activities = ActivityExecutor()
        self.workflows: Dict[str, WorkflowExecution] = {}
        self.running_tasks: Dict[str, asyncio.Task] = {}
        
        # Load persisted state
        self._load()
        
        # Register default activities
        self._register_default_activities()
    
    def _load(self):
        """Load workflows from disk"""
        if self.workflows_file.exists():
            try:
                with open(self.workflows_file) as f:
                    data = json.load(f)
                    for wid, wdata in data.items():
                        wdata['state'] = WorkflowState(wdata['state'])
                        self.workflows[wid] = WorkflowExecution(**wdata)
            except Exception as e:
                print(f"Failed to load workflows: {e}")
    
    def _save(self):
        """Persist workflows to disk"""
        data = {wid: self._serialize_workflow(w) for wid, w in self.workflows.items()}
        with open(self.workflows_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _serialize_workflow(self, w: WorkflowExecution) -> Dict:
        """Serialize workflow for JSON"""
        return {
            'id': w.id,
            'name': w.name,
            'type': w.type,
            'state': w.state.value,
            'status': w.status,
            'input': w.input,
            'result': w.result,
            'error': w.error,
            'events': w.events,
            'activities': {k: asdict(v) for k, v in w.activities.items()},
            'child_workflows': w.child_workflows,
            'signals': w.signals,
            'created_at': w.created_at,
            'started_at': w.started_at,
            'completed_at': w.completed_at,
            'attempt': w.attempt,
            'max_attempts': w.max_attempts
        }
    
    def _register_default_activities(self):
        """Register default activities for agent sales pipeline"""
        # Content generation
        self.activities.register("generate_script", self._act_generate_script)
        self.activities.register("create_voiceover", self._act_create_voiceover,
                                retry_policy=RetryPolicy(max_attempts=5))
        self.activities.register("render_video", self._act_render_video)
        self.activities.register("generate_caption", self._act_generate_caption)
        
        # Publishing
        self.activities.register("upload_to_tiktok", self._act_upload_tiktok,
                                retry_policy=RetryPolicy(max_attempts=3, 
                                                        initial_interval=5))
        self.activities.register("schedule_post", self._act_schedule_post)
        
        # Utilities
        self.activities.register("send_notification", self._act_notify)
    
    # ========== Default Activity Implementations ==========
    
    def _act_generate_script(self, agent_type: str, length: str = "medium") -> Dict:
        """Generate video script"""
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from content.content_templates import ContentGenerator
        gen = ContentGenerator()
        return gen.generate_script(agent_type, length)
    
    def _act_create_voiceover(self, text: str, voice_id: str = None) -> Optional[str]:
        """Create voice audio"""
        api_key = os.environ.get("ELEVENLABS_API_KEY")
        if not api_key:
            return None
        
        import requests
        voice_id = voice_id or "pNInz6obpgDQGcFmaJgB"
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
        data = {"text": text, "voice_settings": {"stability": 0.5}}
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        if response.status_code == 200:
            path = Path(tempfile.gettempdir()) / f"voice_{uuid.uuid4().hex[:8]}.mp3"
            path.write_bytes(response.content)
            return str(path)
        
        raise Exception(f"Voice API error: {response.status_code}")
    
    def _act_render_video(self, slides: List[Dict], output_name: str) -> str:
        """Render video from slides"""
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from core.video_pipeline import VideoPipeline
        
        output_dir = Path("/storage/emulated/0/Movies/AgentSales")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        pipeline = VideoPipeline(str(output_dir))
        return pipeline.create_video_from_slides(slides, None, output_name)
    
    def _act_generate_caption(self, agent: Dict) -> str:
        """Generate social caption"""
        import random
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from content.content_templates import AGENT_SALES_TEMPLATES
        
        ctas = AGENT_SALES_TEMPLATES["cta_phrases"]
        
        return f"""
🚀 MEET YOUR NEW {agent['name'].upper()}

{agent['tagline']}

💰 ${agent['price']}/month

{chr(10).join(f'• {f}' for f in agent['features'][:3])}

{random.choice(ctas)}

{random.choice(AGENT_SALES_TEMPLATES['hashtags'])}
""".strip()
    
    def _act_upload_tiktok(self, video_path: str, caption: str) -> Dict:
        """Upload to TikTok (placeholder - needs auth)"""
        # For now, just log and return
        return {
            "status": "ready_for_upload",
            "video": video_path,
            "caption": caption,
            "note": "Configure TikTok auth for auto-upload"
        }
    
    def _act_schedule_post(self, video_path: str, platforms: List[str],
                          post_time: str) -> Dict:
        """Schedule post across platforms"""
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from scheduler.scheduler import ContentScheduler
        
        scheduler = ContentScheduler()
        agent_type = Path(video_path).stem.split('_')[0]
        
        scheduled = scheduler.add_to_schedule(video_path, platforms, agent_type)
        return {"scheduled": len(scheduled), "items": scheduled}
    
    def _act_notify(self, message: str, channel: str = "telegram") -> Dict:
        """Send notification"""
        if channel == "telegram":
            return self._send_telegram(message)
        return {"status": "sent", "message": message}
    
    def _send_telegram(self, message: str) -> Dict:
        """Send Telegram message"""
        config_file = Path("~/.telegram-bot/config.json").expanduser()
        if not config_file.exists():
            return {"status": "error", "message": "Telegram not configured"}
        
        import requests
        with open(config_file) as f:
            config = json.load(f)
        
        url = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage"
        data = {"chat_id": config["chat_id"], "text": message}
        
        response = requests.post(url, json=data)
        return response.json()
    
    # ========== Workflow Management ==========
    
    def start_workflow(self, name: str, workflow_type: str, 
                      input_data: Any = None, task_queue: str = "default") -> str:
        """Start a new workflow execution"""
        workflow_id = f"{name}-{uuid.uuid4().hex[:8]}"
        
        execution = WorkflowExecution(
            id=workflow_id,
            name=name,
            type=workflow_type,
            state=WorkflowState.INIT,
            input=input_data,
            max_attempts=1
        )
        
        self.workflows[workflow_id] = execution
        self._save()
        
        # Add event
        self._add_event(workflow_id, "WorkflowStarted", {"task_queue": task_queue})
        
        # Run synchronously (event loop handled by caller)
        return self._run_workflow_sync(workflow_id)
    
    def run_async(self):
        """Run the engine with async event loop"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(asyncio.sleep(0))
        finally:
            loop.close()
    
    def _run_workflow_sync(self, workflow_id: str) -> str:
        """Run workflow in sync mode"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(self._run_workflow(workflow_id))
        except RuntimeError:
            # No loop running, create nested
            asyncio.run(self._run_workflow(workflow_id))
        
        return workflow_id
    
    async def _run_workflow(self, workflow_id: str):
        """Run workflow logic"""
        execution = self.workflows.get(workflow_id)
        if not execution:
            return
        
        execution.state = WorkflowState.RUNNING
        execution.started_at = datetime.now().isoformat()
        self._add_event(workflow_id, "WorkflowExecutionStarted")
        self._save()
        
        try:
            # Route to specific workflow handler
            if execution.type == "content_generation":
                result = await self._run_content_generation(execution)
            elif execution.type == "batch_content":
                result = await self._run_batch_content(execution)
            elif execution.type == "publish":
                result = await self._run_publish(execution)
            elif execution.type == "schedule":
                result = await self._run_schedule(execution)
            else:
                result = {"error": f"Unknown workflow type: {execution.type}"}
            
            execution.state = WorkflowState.COMPLETED
            execution.result = result
            execution.completed_at = datetime.now().isoformat()
            self._add_event(workflow_id, "WorkflowCompleted", result)
            
        except Exception as e:
            execution.state = WorkflowState.FAILED
            execution.error = str(e)
            execution.completed_at = datetime.now().isoformat()
            self._add_event(workflow_id, "WorkflowFailed", {"error": str(e)})
        
        self._save()
    
    async def _run_content_generation(self, execution: WorkflowExecution) -> Dict:
        """Content Generation Workflow - Patricia pattern"""
        input_data = execution.input or {}
        agent_type = input_data.get("agent_type", "sales")
        length = input_data.get("length", "medium")
        with_voice = input_data.get("with_voice", True)
        
        result = {"activities": {}}
        
        # Step 1: Generate Script
        self._add_event(execution.id, "ActivityScheduled", 
                       {"name": "generate_script"})
        script_result = await self.activities.execute("generate_script", 
                                                       agent_type, length)
        result["activities"]["generate_script"] = script_result
        result["script"] = script_result["script"]
        result["agent"] = script_result["agent"]
        self._add_event(execution.id, "ActivityCompleted", 
                       {"name": "generate_script"})
        
        # Step 2: Create Slides
        self._add_event(execution.id, "ActivityScheduled", 
                       {"name": "render_video"})
        
        slides = []
        colors = [(26, 26, 46), (20, 40, 60), (40, 20, 60), 
                  (30, 30, 50), (20, 60, 40)]
        
        for i, scene in enumerate(script_result["scenes"]):
            duration = scene["end"] - scene["start"]
            slides.append({
                "text": scene["text"],
                "bg_color": colors[i % len(colors)],
                "duration": duration
            })
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"{agent_type}_wf_{timestamp}"
        
        video_path = await self.activities.execute("render_video", 
                                                    slides, output_name)
        result["activities"]["render_video"] = {"video_path": video_path}
        result["video_path"] = video_path
        self._add_event(execution.id, "ActivityCompleted", {"name": "render_video"})
        
        # Step 3: Generate Caption
        self._add_event(execution.id, "ActivityScheduled", 
                       {"name": "generate_caption"})
        caption = await self.activities.execute("generate_caption", 
                                                script_result["agent"])
        result["activities"]["generate_caption"] = caption
        result["caption"] = caption
        self._add_event(execution.id, "ActivityCompleted", 
                       {"name": "generate_caption"})
        
        # Step 4: Schedule (if not blocking on publish)
        if input_data.get("schedule", True):
            self._add_event(execution.id, "ActivityScheduled", 
                           {"name": "schedule_post"})
            schedule_result = await self.activities.execute(
                "schedule_post", 
                video_path, 
                ["tiktok"],
                input_data.get("post_time", "18:00")
            )
            result["activities"]["schedule_post"] = schedule_result
            self._add_event(execution.id, "ActivityCompleted", 
                           {"name": "schedule_post"})
        
        return result
    
    async def _run_batch_content(self, execution: WorkflowExecution) -> Dict:
        """Batch Content Workflow - Fan-out pattern"""
        input_data = execution.input or {}
        count = input_data.get("count", 5)
        agents = input_data.get("agents", ["sales", "support", "marketing"])
        
        result = {
            "batch_id": execution.id,
            "total": count,
            "completed": 0,
            "failed": 0,
            "workflows": []
        }
        
        # Fan-out: Start child workflows
        for i in range(count):
            agent = random.choice(agents)
            length = random.choice(["short", "medium", "long"])
            
            child_id = self.start_workflow(
                f"child_{i+1}",
                "content_generation",
                {"agent_type": agent, "length": length, "schedule": False}
            )
            
            execution.child_workflows[f"child_{i+1}"] = child_id
            result["workflows"].append({
                "index": i + 1,
                "child_id": child_id,
                "agent": agent
            })
            
            # Small delay between starts
            await asyncio.sleep(0.5)
        
        # Wait for children (in real Temporal, this would be workflow.await)
        await asyncio.sleep(count * 2)  # Placeholder
        
        # Aggregate results
        for child_id in execution.child_workflows.values():
            child = self.workflows.get(child_id)
            if child and child.state == WorkflowState.COMPLETED:
                result["completed"] += 1
            else:
                result["failed"] += 1
        
        self._save()
        return result
    
    async def _run_publish(self, execution: WorkflowExecution) -> Dict:
        """Publish Workflow - Human approval signal"""
        input_data = execution.input or {}
        video_path = input_data.get("video_path")
        caption = input_data.get("caption")
        require_approval = input_data.get("require_approval", True)
        
        result = {"status": "pending_approval"}
        
        if require_approval:
            # Send for approval
            await self.activities.execute("send_notification",
                f"📋 Review required: {video_path}\n\n{caption[:200]}...",
                "telegram"
            )
            
            # Wait for signal (in real Temporal, this would be workflow.wait)
            # For now, auto-approve after signal
            result["status"] = "awaiting_signal:HumanApproval"
        
        # Execute upload
        upload_result = await self.activities.execute("upload_to_tiktok",
                                                       video_path, caption)
        result["upload"] = upload_result
        
        return result
    
    async def _run_schedule(self, execution: WorkflowExecution) -> Dict:
        """Schedule Workflow"""
        input_data = execution.input or {}
        
        schedule_result = await self.activities.execute(
            "schedule_post",
            input_data.get("video_path"),
            input_data.get("platforms", ["tiktok"]),
            input_data.get("post_time", "18:00")
        )
        
        return schedule_result
    
    # ========== Signal & Query ==========
    
    def signal_workflow(self, workflow_id: str, signal_name: str, 
                       signal_data: Any = None):
        """Send a signal to workflow (human approval, etc.)"""
        if workflow_id in self.workflows:
            self.workflows[workflow_id].signals.append({
                "name": signal_name,
                "data": signal_data,
                "received_at": datetime.now().isoformat()
            })
            self._add_event(workflow_id, "SignalReceived", {
                "name": signal_name,
                "data": signal_data
            })
            self._save()
    
    def query_workflow(self, workflow_id: str, query_type: str = "status") -> Dict:
        """Query workflow state"""
        execution = self.workflows.get(workflow_id)
        if not execution:
            return {"error": "Workflow not found"}
        
        if query_type == "status":
            return {
                "id": execution.id,
                "name": execution.name,
                "state": execution.state.value,
                "result": execution.result,
                "error": execution.error,
                "activities": {
                    name: asdict(act) 
                    for name, act in execution.activities.items()
                }
            }
        elif query_type == "progress":
            completed = len([a for a in execution.activities.values() 
                           if a.status == "completed"])
            total = len(execution.activities)
            return {
                "progress": completed / total if total > 0 else 0,
                "completed": completed,
                "total": total
            }
        
        return {"id": execution.id, "state": execution.state.value}
    
    # ========== Utilities ==========
    
    def _add_event(self, workflow_id: str, event_type: str, details: Dict = None):
        """Add event to workflow history"""
        execution = self.workflows.get(workflow_id)
        if execution:
            execution.events.append({
                "type": event_type,
                "timestamp": datetime.now().isoformat(),
                "details": details or {}
            })
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict]:
        """Get workflow info"""
        w = self.workflows.get(workflow_id)
        if w:
            return asdict(w)
        return None
    
    def list_workflows(self, status: str = None, limit: int = 50) -> List[Dict]:
        """List workflows"""
        workflows = []
        for w in self.workflows.values():
            if status is None or w.state.value == status:
                workflows.append(asdict(w))
        
        return sorted(workflows, 
                     key=lambda x: x.get("created_at", ""),
                     reverse=True)[:limit]


# ========== CLI ==========

def main():
    import argparse
    
    engine = TemporalWorkflowEngine()
    
    parser = argparse.ArgumentParser(description="Temporal Workflow Engine")
    subparsers = parser.add_subparsers(dest="command")
    
    # Start workflows
    start = subparsers.add_parser("start", help="Start a workflow")
    start.add_argument("type", choices=["content", "batch", "publish", "schedule"])
    start.add_argument("--agent", default="sales")
    start.add_argument("--length", default="medium")
    start.add_argument("--count", type=int, default=5)
    
    # Query
    query_parser = subparsers.add_parser("query", help="Query workflow")
    query_parser.add_argument("workflow_id")
    query_parser.add_argument("--type", default="status")
    
    # Signal
    signal_parser = subparsers.add_parser("signal", help="Send signal")
    signal_parser.add_argument("workflow_id")
    signal_parser.add_argument("signal_name")
    signal_parser.add_argument("--data", default=None)
    
    # List
    list_parser = subparsers.add_parser("list", help="List workflows")
    list_parser.add_argument("--status", help="Filter by status")
    
    # Dashboard
    subparsers.add_parser("dashboard", help="Show dashboard")
    
    args = parser.parse_args()
    
    if args.command == "start":
        input_data = {}
        
        if args.type == "content":
            input_data = {"agent_type": args.agent, "length": args.length}
            wid = engine.start_workflow("ContentGeneration", "content_generation",
                                      input_data)
        elif args.type == "batch":
            input_data = {"count": args.count}
            wid = engine.start_workflow("BatchContent", "batch_content", input_data)
        elif args.type == "schedule":
            input_data = {"platforms": ["tiktok"], "post_time": "18:00"}
            wid = engine.start_workflow("Schedule", "schedule", input_data)
        
        print(f"✅ Started workflow: {wid}")
    
    elif args.command == "query":
        result = engine.query_workflow(args.workflow_id, args.type)
        print(json.dumps(result, indent=2))
    
    elif args.command == "signal":
        data = json.loads(args.data) if args.data else None
        engine.signal_workflow(args.workflow_id, args.signal_name, data)
        print(f"✅ Signal sent: {args.signal_name}")
    
    elif args.command == "list":
        for w in engine.list_workflows(args.status):
            print(f"[{w['state']}] {w['id']} - {w['type']}")
    
    elif args.command == "dashboard":
        workflows = engine.list_workflows(limit=100)
        
        states = {}
        for w in workflows:
            s = w['state']
            states[s] = states.get(s, 0) + 1
        
        print("\n⚡ TEMPORAL WORKFLOW DASHBOARD")
        print("=" * 40)
        print(f"\n📊 Status:")
        for state, count in states.items():
            print(f"   {state}: {count}")
        
        print(f"\n📁 Recent:")
        for w in workflows[:5]:
            print(f"   [{w['state']}] {w['id'][:20]}...")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
