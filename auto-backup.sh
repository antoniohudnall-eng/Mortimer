#!/bin/bash
# SEED3 Auto-Backup - Mortimer to GitHub
# Run this on wake and before sleep

cd ~/mortimer || exit 1

# Check for changes
if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "🖥️ No changes to backup"
    exit 0
fi

# Add all changes
git add -A

# Commit with timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
git commit -m "🖥️ SEED3 Auto-Backup $TIMESTAMP" 2>/dev/null

# Push to GitHub
git push origin main 2>/dev/null

echo "✅ Backed up to GitHub at $TIMESTAMP"
