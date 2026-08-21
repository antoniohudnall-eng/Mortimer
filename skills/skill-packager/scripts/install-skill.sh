#!/bin/bash
# Install a .skill file

SKILL_FILE="$1"
INSTALL_DIR="${2:-/usr/lib/node_modules/openclaw/skills/}"

if [ -z "$SKILL_FILE" ] || [ ! -f "$SKILL_FILE" ]; then
    echo "Usage: install-skill.sh <skill_file.skill> [install_directory]"
    exit 1
fi

SKILL_NAME=$(basename "$SKILL_FILE" .skill)
TARGET_DIR="$INSTALL_DIR/$SKILL_NAME"

echo "Installing skill: $SKILL_NAME"
echo "Target: $TARGET_DIR"

# Create target directory
mkdir -p "$TARGET_DIR"

# Unzip skill file
unzip -o "$SKILL_FILE" -d "$TARGET_DIR" > /dev/null 2>&1

echo "✅ Installed: $SKILL_NAME"
echo "   Location: $TARGET_DIR"
