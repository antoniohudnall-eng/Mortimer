#!/bin/bash
# Validate skill structure

SKILL_DIR="$1"

if [ -z "$SKILL_DIR" ] || [ ! -d "$SKILL_DIR" ]; then
    echo "Usage: validate-skill.sh <skill_directory>"
    exit 1
fi

SKILL_NAME=$(basename "$SKILL_DIR")
ERRORS=0

echo "Validating skill: $SKILL_NAME"
echo ""

# Check SKILL.md exists
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ Missing SKILL.md"
    ((ERRORS++))
else
    echo "✅ SKILL.md exists"
    
    # Check frontmatter
    if head -5 "$SKILL_DIR/SKILL.md" | grep -q "^---"; then
        echo "✅ YAML frontmatter present"
        
        # Check required fields
        if grep -q "^name:" "$SKILL_DIR/SKILL.md"; then
            echo "✅ 'name' field present"
        else
            echo "❌ Missing 'name' field in frontmatter"
            ((ERRORS++))
        fi
        
        if grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
            echo "✅ 'description' field present"
        else
            echo "❌ Missing 'description' field in frontmatter"
            ((ERRORS++))
        fi
    else
        echo "❌ YAML frontmatter missing"
        ((ERRORS++))
    fi
fi

# Check for extraneous files
for file in README.md CHANGELOG.md INSTALL.md; do
    if [ -f "$SKILL_DIR/$file" ]; then
        echo "⚠️  Extraneous file found: $file (should be removed)"
    fi
done

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "✅ Validation passed"
    exit 0
else
    echo "❌ Validation failed: $ERRORS error(s)"
    exit 1
fi
