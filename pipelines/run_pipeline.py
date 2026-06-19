#!/usr/bin/env python3
"""
🚀 QUICK START - Agent Sales Pipeline
Run this to create and upload agent promo content
"""

import os
import sys
from pathlib import Path

# Check dependencies
def check_system():
    """Verify system is ready"""
    print("🔍 Checking system...")
    
    checks = []
    
    # Python
    checks.append(("Python", True))
    
    # FFmpeg
    import shutil
    checks.append(("FFmpeg", bool(shutil.which("ffmpeg"))))
    
    # Pillow
    try:
        from PIL import Image
        checks.append(("Pillow", True))
    except:
        checks.append(("Pillow", False))
    
    # ElevenLabs
    checks.append(("ElevenLabs API", bool(os.environ.get("ELEVENLABS_API_KEY"))))
    
    # Output dir
    output_dir = Path("/storage/emulated/0/Movies/AgentSales")
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        checks.append(("Output Dir", True))
    except:
        checks.append(("Output Dir", False))
    
    print("\n📋 System Status:")
    all_good = True
    for name, status in checks:
        icon = "✅" if status else "❌"
        print(f"  {icon} {name}")
        if not status:
            all_good = False
    
    return all_good


def demo():
    """Run a quick demo"""
    print("\n🎬 AGENT SALES PIPELINE - DEMO")
    print("=" * 50)
    
    sys.path.insert(0, str(Path(__file__).parent))
    
    from content.content_templates import ContentGenerator
    
    gen = ContentGenerator()
    
    print("\n📝 Available Agents:")
    for key, agent in gen.templates["agent_types"].items():
        print(f"  🚀 {agent['name']}")
        print(f"     {agent['tagline']}")
        print(f"     ${agent['price']}/month")
        print()
    
    print("\n📋 Sample Script (Sales Agent):")
    script = gen.generate_script("sales", "short")
    print(script["script"])


def main():
    if "--demo" in sys.argv:
        demo()
        return
    
    if not check_system():
        print("\n⚠️ Some checks failed. Install dependencies first.")
        print("Run 'pip install pillow requests' and set ELEVENLABS_API_KEY")
    
    print("\n🎯 Available Commands:")
    print("  python3 run_pipeline.py --demo        - See sample content")
    print("  python3 agent_sales_pipeline.py list   - List all agents")
    print("  python3 agent_sales_pipeline.py create --agent sales")
    print("  python3 agent_sales_pipeline.py batch   - Create 5 promos")
    print("  python3 scheduler/scheduler.py         - View schedule")
    
    print("\n" + "=" * 50)
    print("🚀 Ready to sell agents!")


if __name__ == "__main__":
    main()
