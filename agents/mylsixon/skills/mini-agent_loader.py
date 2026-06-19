#!/usr/bin/env python3
"""
MINI-AGENT Skill Loader for Agent
Auto-generated skill activation
"""

import sys
sys.path.insert(0, "/root/.openclaw/workspace/AGI_COMPANY/shared/skills/mini-agent")

from mini_agent_skill import MiniAgentSkill

# Activate skill
miniagent_instance = MiniAgentSkill()
print(f"[MINI-AGENT] Skill activated for agent")

# Export for agent use
skill = miniagent_instance
