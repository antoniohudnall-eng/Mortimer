# Skill Format Specification

## File Structure

```
skill-name/
├── SKILL.md (required)
├── scripts/ (optional)
│   └── *.sh, *.js, *.py
├── references/ (optional)
│   └── *.md
└── assets/ (optional)
    └── images, templates, etc.
```

## SKILL.md Format

```yaml
---
name: skill-name
description: Clear description of what this skill does and when to use it
---

# Skill Title

Instructions for using the skill...
```

## Frontmatter Requirements

- **name**: lowercase, hyphens, no spaces
- **description**: comprehensive trigger description

## Packaging

.skill files are ZIP archives with .skill extension.

## Installation

Extract to: `/usr/lib/node_modules/openclaw/skills/`
