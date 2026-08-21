#!/usr/bin/env python3
"""
Skill Builder v1.0 - Natural Language Agent Creation
Creates Society Agents from conversation
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

AGENTS_DIR = Path("/root/.openclaw/workspace/agents")
TEMPLATES_DIR = Path("/root/.openclaw/workspace/skills/skill-builder/templates")

class SkillBuilder:
    def __init__(self):
        self.answers = {}
        self.agent_name = None
        self.agent_class = None
        
    def interview(self):
        """Gather requirements via conversation"""
        print("🛠️  Skill Builder - Natural Language Agent Creation")
        print("=" * 60)
        
        self.answers['name'] = input("1. Agent name (lowercase-with-dashes): ").strip()
        self.agent_name = self.answers['name']
        self.agent_class = self._to_class_name(self.agent_name)
        
        self.answers['purpose'] = input("2. What does this agent do? ").strip()
        
        print("\n3. When should it run?")
        print("   [1] Every N minutes")
        print("   [2] Every N hours")
        print("   [3] Daily at specific time")
        print("   [4] Continuous (no delay)")
        print("   [5] Event-driven (webhook)")
        trigger_choice = input("   Select [1-5]: ").strip()
        
        intervals = {
            '1': ('minutes', input("   Minutes: ").strip()),
            '2': ('hours', input("   Hours: ").strip()),
            '3': ('daily', input("   Time (HH:MM): ").strip()),
            '4': ('continuous', '0'),
            '5': ('event', 'webhook')
        }
        self.answers['trigger'] = intervals.get(trigger_choice, ('minutes', '5'))
        
        self.answers['inputs'] = input("4. What data does it need? (comma-separated): ").strip()
        self.answers['outputs'] = input("5. What does it produce? ").strip()
        self.answers['permissions'] = input("6. Permissions [read-only/write]: ").strip()
        
        print("\n" + "=" * 60)
        print("📋 Summary:")
        print(f"   Name: {self.agent_name}")
        print(f"   Purpose: {self.answers['purpose']}")
        print(f"   Trigger: {self.answers['trigger']}")
        print("=" * 60)
        
        confirm = input("\nCreate this agent? [Y/n]: ").strip().lower()
        return confirm in ('', 'y', 'yes')
    
    def _to_class_name(self, name):
        """Convert dash-name to ClassName"""
        return ''.join(word.capitalize() for word in name.split('-'))
    
    def _to_interval_seconds(self, trigger):
        """Convert trigger to seconds"""
        unit, value = trigger
        if unit == 'minutes':
            return int(value) * 60
        elif unit == 'hours':
            return int(value) * 3600
        elif unit == 'daily':
            return 86400  # Will use cron for daily
        elif unit == 'continuous':
            return 5  # 5 second loop
        return 300  # Default 5 minutes
    
    def generate_agent(self):
        """Generate agent files"""
        agent_dir = AGENTS_DIR / self.agent_name
        agent_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate Python agent
        py_file = agent_dir / f"{self.agent_name}_agent.py"
        interval = self._to_interval_seconds(self.answers['trigger'])
        
        python_code = f'''#!/usr/bin/env python3
"""
{self.agent_class}Agent - Society Agent
Created: {datetime.now().isoformat()}
Purpose: {self.answers['purpose']}
"""

import json
import logging
import sys
import time
from pathlib import Path

# Add BHSI integration
sys.path.insert(0, '/root/.openclaw/workspace/aocros/BHSI')

class {self.agent_class}Agent:
    def __init__(self, config_path=None):
        self.name = "{self.agent_name}"
        self.config = self._load_config(config_path)
        self.setup_logging()
        
    def _load_config(self, path):
        default_config = {{
            "interval": {interval},
            "log_level": "INFO",
            "purpose": "{self.answers['purpose']}",
            "inputs": "{self.answers['inputs']}",
            "outputs": "{self.answers['outputs']}",
            "permissions": "{self.answers['permissions']}"
        }}
        if path and Path(path).exists():
            with open(path) as f:
                return {{**default_config, **json.load(f)}}
        return default_config
    
    def setup_logging(self):
        logging.basicConfig(
            level=getattr(logging, self.config.get('log_level', 'INFO')),
            format=f'%(asctime)s [%(name)s] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler(f'/var/log/aos/{self.name}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.name)
    
    def run(self):
        """Main agent loop"""
        self.logger.info(f"{{self.name}} agent starting...")
        self.logger.info(f"Purpose: {{self.config.get('purpose')}}")
        
        while True:
            try:
                self.execute()
                time.sleep(self.config.get('interval', {interval}))
            except Exception as e:
                self.logger.error(f"Error in main loop: {{e}}")
                time.sleep(60)
    
    def execute(self):
        """Agent logic - implement your task here"""
        self.logger.info("Executing...")
        
        # TODO: Implement {self.answers['purpose']}
        # Inputs needed: {self.answers['inputs']}
        # Outputs expected: {self.answers['outputs']}
        # Permissions: {self.answers['permissions']}
        
        pass

if __name__ == "__main__":
    config_path = Path(__file__).parent / "config.json"
    agent = {self.agent_class}Agent(config_path if config_path.exists() else None)
    agent.run()
'''
        py_file.write_text(python_code)
        py_file.chmod(0o755)
        
        # Generate systemd service
        service_file = agent_dir / f"{self.agent_name}.service"
        service_content = f'''[Unit]
Description={self.agent_class} Society Agent
After=network.target aos-brain-v4.service
Wants=aos-brain-v4.service

[Service]
Type=simple
User=root
WorkingDirectory={agent_dir}
ExecStart=/usr/bin/python3 {agent_dir}/{self.agent_name}_agent.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier={self.agent_name}

[Install]
WantedBy=multi-user.target
'''
        service_file.write_text(service_content)
        
        # Generate config.json
        config_file = agent_dir / "config.json"
        config = {
            "name": self.agent_name,
            "created": datetime.now().isoformat(),
            "purpose": self.answers['purpose'],
            "trigger": self.answers['trigger'],
            "interval": interval,
            "permissions": self.answers['permissions']
        }
        config_file.write_text(json.dumps(config, indent=2))
        
        # Generate README
        readme_file = agent_dir / "README.md"
        readme = f'''# {self.agent_class} Agent

**Name:** {self.agent_name}
**Created:** {datetime.now().isoformat()}

## Purpose
{self.answers['purpose']}

## Configuration
- **Trigger:** {self.answers['trigger']}
- **Interval:** {interval} seconds
- **Permissions:** {self.answers['permissions']}

## Inputs
{self.answers['inputs']}

## Outputs
{self.answers['outputs']}

## Installation
```bash
sudo cp {self.agent_name}.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable {self.agent_name}
sudo systemctl start {self.agent_name}
```

## Logs
```bash
journalctl -u {self.agent_name} -f
```

## Status
```bash
systemctl status {self.agent_name}
```
'''
        readme_file.write_text(readme)
        
        return agent_dir
    
    def install_agent(self, agent_dir):
        """Install to systemd"""
        import subprocess
        
        service_file = agent_dir / f"{self.agent_name}.service"
        
        try:
            # Copy service file
            subprocess.run(['sudo', 'cp', str(service_file), '/etc/systemd/system/'], check=True)
            
            # Reload daemon
            subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
            
            # Enable service
            subprocess.run(['sudo', 'systemctl', 'enable', self.agent_name], check=True)
            
            # Start service
            subprocess.run(['sudo', 'systemctl', 'start', self.agent_name], check=True)
            
            print(f"✅ Agent '{self.agent_name}' installed and started!")
            print(f"   View logs: journalctl -u {self.agent_name} -f")
            print(f"   Check status: systemctl status {self.agent_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation failed: {e}")
            print(f"   Manual install:")
            print(f"   sudo cp {service_file} /etc/systemd/system/")
            print(f"   sudo systemctl daemon-reload")
            print(f"   sudo systemctl enable --now {self.agent_name}")
            return False
    
    def build(self):
        """Main build process"""
        if not self.interview():
            print("❌ Cancelled.")
            return False
        
        print(f"\n🔨 Generating agent '{self.agent_name}'...")
        agent_dir = self.generate_agent()
        
        print(f"📁 Files created in: {agent_dir}")
        for f in agent_dir.iterdir():
            print(f"   - {f.name}")
        
        print("\n📦 Installing to systemd...")
        return self.install_agent(agent_dir)

if __name__ == "__main__":
    builder = SkillBuilder()
    success = builder.build()
    sys.exit(0 if success else 1)
