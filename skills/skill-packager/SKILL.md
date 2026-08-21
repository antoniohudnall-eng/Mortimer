---
name: skill-packager
description: Package skills into distributable .skill files. Use when creating distributable skill packages, validating skill structure, or installing skills from .skill files. Validates YAML frontmatter, checks file organization, and creates zip-based .skill packages.
---

# Skill Packager

Package skills for distribution and installation.

## Quick Start

Package a skill:
```bash
scripts/package-skill.sh /path/to/skill-name
```

Install a skill:
```bash
scripts/install-skill.sh skill-name.skill /usr/lib/node_modules/openclaw/skills/
```

Validate skill structure:
```bash
scripts/validate-skill.sh /path/to/skill-name
```

## What Gets Packaged

A .skill file is a zip archive containing:
- SKILL.md (required)
- scripts/ (optional)
- references/ (optional)
- assets/ (optional)

## Validation Checks

- YAML frontmatter format (name, description required)
- SKILL.md exists and is readable
- No extraneous files (README, CHANGELOG, etc.)
- Proper directory structure

## Distribution

Share .skill files via:
- Direct file transfer
- Git repository
- Skill registry (future)

## References

See [references/skill-format.md](references/skill-format.md) for detailed format specification.
