#!/usr/bin/env python3
"""Quick Dashboard Test"""
import sys
sys.path.insert(0, '/root/.openclaw/workspace/agent_sandboxes/the-great-cryptonio')

try:
    import dashboard_server
    print("✅ Dashboard module loaded successfully")
    print("📊 Ready to start at http://localhost:5000")
    
    # Start it
    dashboard_server.app.run(host='0.0.0.0', port=5000, debug=False)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
