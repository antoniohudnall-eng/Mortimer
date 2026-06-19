#!/usr/bin/env python3
"""
Volatility Monitor Integration Test
Tests volatility monitoring alongside the main bot
"""

import sys
import os

sys.path.insert(0, '/root/.openclaw/workspace/agent_sandboxes/the-great-cryptonio')

from volatility_monitor import VolatilityMonitor, monitor_all_symbols

print("=" * 70)
print("🔥 VOLATILITY MONITOR TEST")
print("=" * 70)
print()
print("Running volatility analysis across all symbols...")
print()

try:
    monitor = monitor_all_symbols()
    print("\n✅ Volatility monitoring operational")
    print("\nThis module can now:")
    print("  - Track ATR% across timeframes")
    print("  - Alert on volatility spikes")
    print("  - Adjust position sizes based on market conditions")
    print("  - Pause trading during extreme volatility")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
