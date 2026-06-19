#!/bin/bash
# Patricia's System Monitor

echo "Patricia Monitor - $(date)"
echo ""

# Check Dark Factory metrics
echo "Dark Factory Status:"
ls /data/factory/*.db 2>/dev/null | wc -l | xargs echo "  Database files:"

# Check Six Sigma metrics
echo ""
echo "Process Metrics:"
python3 << 'PYEOF'
import sqlite3
import os

if os.path.exists('/data/factory/cobra_production.db'):
    conn = sqlite3.connect('/data/factory/cobra_production.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM production_runs")
    count = cursor.fetchone()[0]
    print(f"  Production runs tracked: {count}")
    conn.close()
else:
    print("  No production database found")
PYEOF

echo ""
echo "Active DMAIC Projects:"
ls $PATRICIA_DIR/projects/*.yaml 2>/dev/null | wc -l | xargs echo "  Projects:"
