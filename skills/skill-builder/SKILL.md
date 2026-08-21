# Skill Builder v1.0 - Natural Language Agent Creation

## Name
skill-builder

## Description
Create new Society Agents via natural language conversation. Generates systemd services, Python skeletons, and auto-registers with BHSI.

## When to Use
- When you need a new automated agent
- When you want to delegate a recurring task
- When expanding the Society Agent workforce
- When formalizing an SOP into automation

## What This Skill Does
1. Interviews you about the agent's purpose
2. Generates systemd service file
3. Creates Python agent skeleton with BHSI integration
4. Auto-registers with keepalive scripts
5. Starts and enables the service

## What This Skill Does NOT Do
- Write complex business logic (provides skeleton)
- Handle external API authentication (you provide keys)
- Guarantee bug-free code (requires testing)

## Workflow

### Phase 1: Requirements Interview
Ask the user:
1. **Name**: What should we call this agent? (e.g., "inventory-tracker")
2. **Purpose**: What does this agent do in one sentence?
3. **Trigger**: When should it run? (cron schedule, event, continuous)
4. **Inputs**: What data does it need?
5. **Outputs**: What does it produce or affect?
6. **Permissions**: Read-only or can it modify/write?

### Phase 2: Generate Files

Create in `/root/.openclaw/workspace/agents/{name}/`:
- `{name}_agent.py` - Main agent code
- `{name}.service` - Systemd service file
- `config.json` - Agent configuration
- `README.md` - Documentation

### Phase 3: BHSI Integration
- Add to Binary High-Integrity System
- Register with agent_keepalive.sh
- Enable auto-restart on failure

### Phase 4: Activation
```bash
sudo cp {name}.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable {name}
sudo systemctl start {name}
```

## Agent Template Structure

### Python Skeleton
```python
#!/usr/bin/env python3
"""
{AgentName} - Society Agent
Created: {timestamp}
Purpose: {purpose}
"""

import json
import logging
import sys
import time
from pathlib import Path

# Add BHSI integration
sys.path.insert(0, '/root/.openclaw/workspace/aocros/BHSI')

class {AgentName}Agent:
    def __init__(self, config_path=None):
        self.name = "{agent_name}"
        self.config = self._load_config(config_path)
        self.setup_logging()
        
    def _load_config(self, path):
        default_config = {
            "interval": 300,  # 5 minutes
            "log_level": "INFO"
        }
        if path and Path(path).exists():
            with open(path) as f:
                return {**default_config, **json.load(f)}
        return default_config
    
    def setup_logging(self):
        logging.basicConfig(
            level=getattr(logging, self.config.get('log_level', 'INFO')),
            format=f'%(asctime)s [{self.name}] %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger(self.name)
    
    def run(self):
        """Main agent loop"""
        self.logger.info(f"{self.name} agent starting...")
        
        while True:
            try:
                self.execute()
                time.sleep(self.config.get('interval', 300))
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                time.sleep(60)  # Wait before retry
    
    def execute(self):
        """Override this method with agent logic"""
        self.logger.info("Executing agent task...")
        # TODO: Implement agent logic here
        pass

if __name__ == "__main__":
    agent = {AgentName}Agent()
    agent.run()
```

### Systemd Service Template
```ini
[Unit]
Description={AgentName} Society Agent
After=network.target aos-brain-v4.service
Wants=aos-brain-v4.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/workspace/agents/{name}
ExecStart=/usr/bin/python3 /root/.openclaw/workspace/agents/{name}/{name}_agent.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier={name}-agent

[Install]
WantedBy=multi-user.target
```

## Example Usage

User: "Create an agent that checks disk space every hour and alerts if above 80%"

Skill Builder:
1. Creates `disk-monitor` agent
2. Generates disk_monitor_agent.py with df check
3. Creates disk-monitor.service
4. Registers with keepalive
5. Enables hourly execution

## Reference Files
- ../agents/ - Output directory for generated agents
- ../../scripts/agent_keepalive.sh - Registration target
- ../../aocros/BHSI/ - Integration library

## Scripts
- scripts/skill-builder.py - Main skill builder logic
- templates/agent.py.template - Python skeleton
- templates/service.template - Systemd template
