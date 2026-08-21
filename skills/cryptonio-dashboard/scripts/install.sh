#!/bin/bash
# Cryptonio Dashboard Skill - Installation Script

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "Installing Cryptonio Dashboard Skill..."
echo "Directory: $SKILL_DIR"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install flask flask-cors websockets pandas numpy requests --break-system-packages 2>/dev/null || \
pip3 install flask flask-cors websockets pandas numpy requests

# Create directories
mkdir -p "$SKILL_DIR/vault"
mkdir -p "$SKILL_DIR/logs"

# Make scripts executable
chmod +x "$SKILL_DIR/scripts/"*.sh 2>/dev/null || true
chmod +x "$SKILL_DIR/cron/"*.sh 2>/dev/null || true

echo ""
echo "✅ Installation Complete!"
echo ""
echo "Next steps:"
echo "  1. Configure credentials in $SKILL_DIR/vault/"
echo "  2. Run: ./scripts/start_dashboard.sh"
echo "  3. Access: http://localhost:5000"
echo ""
