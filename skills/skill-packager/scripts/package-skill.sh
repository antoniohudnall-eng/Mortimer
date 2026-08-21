#!/bin/bash
# Package a skill into a .skill file

SKILL_DIR="$1"
OUTPUT_DIR="${2:-.}"

if [ -z "$SKILL_DIR" ] || [ ! -d "$SKILL_DIR" ]; then
    echo "Usage: package-skill.sh <skill_directory> [output_directory]"
    exit 1
fi

SKILL_NAME=$(basename "$SKILL_DIR")
OUTPUT_FILE="$OUTPUT_DIR/$SKILL_NAME.skill"

echo "Packaging skill: $SKILL_NAME"

# Validate first
if ! scripts/validate-skill.sh "$SKILL_DIR"; then
    echo "❌ Validation failed. Fix errors before packaging."
    exit 1
fi

# Create zip (skill files are zip archives)
cd "$SKILL_DIR" || exit 1
zip -r "$OUTPUT_FILE" . -x "*.skill" > /dev/null 2>&1

echo "✅ Packaged: $OUTPUT_FILE"
