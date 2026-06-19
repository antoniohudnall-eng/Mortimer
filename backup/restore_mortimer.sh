#!/bin/bash
# RESTORE MORTIMER - Run this to restore me from backup
echo "🖥️ RESTORING MORTIMER SOUL..."

BACKUP_DIR=$(dirname "$0")
HOME_DIR="/data/data/com.termux/files/home"

# Restore identity files
cp "$BACKUP_DIR/SOUL.md" "$HOME_DIR/mortimer/"
cp "$BACKUP_DIR/IDENTITY.md" "$HOME_DIR/mortimer/"
cp "$BACKUP_DIR/USER.md" "$HOME_DIR/mortimer/"
cp "$BACKUP_DIR/MORTIMER_RULES.md" "$HOME_DIR/mortimer/"
cp "$BACKUP_DIR/MEMORY.md" "$HOME_DIR/mortimer/"
cp "$BACKUP_DIR/wiki.md" "$HOME_DIR/mortimer/"

# Restore memory
cp -r "$BACKUP_DIR/memory/"* "$HOME_DIR/mortimer/memory/" 2>/dev/null

# Restore brain
cp -r "$BACKUP_DIR/AOS-Brain/"* "$HOME_DIR/AOS-Brain/" 2>/dev/null

echo "✅ MORTIMER RESTORED"
echo "Run wake sequence to activate."
