#!/usr/bin/env python3
"""
HERMES Skill Loader for Agent
Auto-generated skill activation
"""

import sys
sys.path.insert(0, "/root/.openclaw/workspace/AGI_COMPANY/shared/skills/hermes")

from hermes_skill import HermesSkill

# Activate skill
hermes_instance = HermesSkill()
print(f"[HERMES] Skill activated for agent")

# Export for agent use
skill = hermes_instance
