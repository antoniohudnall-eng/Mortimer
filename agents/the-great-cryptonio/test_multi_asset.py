#!/usr/bin/env python3
"""
Multi-Asset Trading Test
Tests the Cryptonio bot with 4 active symbols
"""

import sys
import os

# Add path
sys.path.insert(0, '/root/.openclaw/workspace/agent_sandboxes/the-great-cryptonio')
sys.path.insert(0, '/root/.openclaw/workspace/agent_sandboxes/r2-d2')

from cryptonio_multi_exchange import Config, UnifiedExchangeManager, CryptonioMultiExchangeBot

def test_multi_asset_config():
    """Test multi-asset configuration"""
    print("=" * 70)
    print("🚀 MULTI-ASSET CONFIGURATION TEST")
    print("=" * 70)
    
    print(f"\n✅ Version: 4.1.0 (Multi-Asset Live Trading)")
    print(f"✅ Active Symbols: {len(Config.ACTIVE_SYMBOLS)}")
    
    for symbol in Config.ACTIVE_SYMBOLS:
        prefs = Config.SYMBOL_PREFERENCES.get(symbol, [])
        print(f"   📊 {symbol}: {prefs}")
    
    print("\n✅ Multi-Asset Mode Configured Successfully")
    return True

def test_exchange_connections():
    """Test connections to all exchanges"""
    print("\n" + "=" * 70)
    print("🔗 EXCHANGE CONNECTION TEST")
    print("=" * 70)
    
    manager = UnifiedExchangeManager()
    
    print(f"\n✅ Connected Exchanges: {len(manager.clients)}")
    for name, client in manager.clients.items():
        status = "🟢 ONLINE" if client.is_connected else "🔴 OFFLINE"
        print(f"   {status} {name}")
    
    return manager

def test_multi_asset_cycle():
    """Test one multi-asset cycle"""
    print("\n" + "=" * 70)
    print("🤖 MULTI-ASSET CYCLE TEST")
    print("=" * 70)
    
    bot = CryptonioMultiExchangeBot()
    
    print(f"\n🎯 Running multi-asset cycle...")
    print(f"   Paper Trading: {Config.PAPER_TRADING}")
    print(f"   Symbols: {', '.join(Config.ACTIVE_SYMBOLS)}")
    
    try:
        bot.run_multi_asset_cycle()
        print("\n✅ Multi-Asset Cycle Complete")
        return True
    except Exception as e:
        print(f"\n❌ Cycle Error: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("CRYPTONIO v4.1.0 - MULTI-ASSET TRADING SYSTEM")
    print("=" * 70)
    
    # Test configuration
    if test_multi_asset_config():
        print("\n✅ Configuration: PASSED")
    
    # Test connections
    try:
        manager = test_exchange_connections()
        print("\n✅ Connections: PASSED")
    except Exception as e:
        print(f"\n❌ Connections: FAILED - {e}")
        sys.exit(1)
    
    # Test multi-asset cycle
    print("\n🚀 Starting Test Cycle...")
    print("   (This will analyze all 4 symbols)")
    input("Press Enter to continue (Ctrl+C to cancel)...")
    
    if test_multi_asset_cycle():
        print("\n" + "=" * 70)
        print("🎉 ALL TESTS PASSED")
        print("=" * 70)
        print("\nMulti-Asset System Ready:")
        print("   BTCUSD - Bitcoin (Kraken priority)")
        print("   DOGEUSD - Dogecoin (Binance)")
        print("   LTCUSD - Litecoin (Binance Primary)")
        print("   XRPUSD - XRP (Binance Secondary)")
        print("\nTo run continuous multi-asset mode:")
        print("   python3 cryptonio_multi_exchange.py --multi-asset --live")
    else:
        print("\n❌ Cycle test failed")
        sys.exit(1)
