#!/usr/bin/env python3
"""
Social Media Screenshot Generator
Creates optimized assets for X/TikTok/Facebook
"""

import json
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from browser_agent import BrowserAgent

OUTPUT_DIR = Path("/root/.openclaw/workspace/AGI_COMPANY/marketing/social_assets")

def generate_social_assets():
    """Generate social media screenshots from psdepot.com"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    assets = {}
    
    with BrowserAgent(headless=True) as agent:
        print("🌐 Loading psdepot.com...")
        agent.navigate("https://psdepot.com")
        
        # 1. X/Twitter Cover (1200x675 - 16:9)
        print("📸 Generating X/Twitter cover...")
        agent.set_viewport({"width": 1200, "height": 675})
        agent.screenshot_full_page(str(OUTPUT_DIR / f"twitter_cover_{timestamp}.png"))
        assets["twitter"] = f"twitter_cover_{timestamp}.png"
        
        # 2. Facebook (1200x630 - 1.91:1)
        print("📸 Generating Facebook preview...")
        agent.set_viewport({"width": 1200, "height": 630})
        agent.screenshot_full_page(str(OUTPUT_DIR / f"facebook_preview_{timestamp}.png"))
        assets["facebook"] = f"facebook_preview_{timestamp}.png"
        
        # 3. TikTok/Instagram Story (1080x1920 - 9:16)
        print("📸 Generating TikTok/IG Story...")
        agent.set_viewport({"width": 1080, "height": 1920})
        agent.screenshot_full_page(str(OUTPUT_DIR / f"tiktok_story_{timestamp}.png"))
        assets["tiktok"] = f"tiktok_story_{timestamp}.png"
        
        # 4. Instagram Post (1080x1080 - 1:1)
        print("📸 Generating Instagram post...")
        agent.set_viewport({"width": 1080, "height": 1080})
        agent.screenshot_full_page(str(OUTPUT_DIR / f"instagram_post_{timestamp}.png"))
        assets["instagram"] = f"instagram_post_{timestamp}.png"
        
        # 5. LinkedIn Banner (1584x396)
        print("📸 Generating LinkedIn banner...")
        agent.set_viewport({"width": 1584, "height": 396})
        agent.screenshot_full_page(str(OUTPUT_DIR / f"linkedin_banner_{timestamp}.png"))
        assets["linkedin"] = f"linkedin_banner_{timestamp}.png"
        
        # 6. Product showcase (scroll to products)
        print("📸 Product showcase...")
        agent.set_viewport({"width": 1920, "height": 1080})
        agent.execute_script("window.scrollTo(0, 500)")
        agent.wait_for_timeout(1000)
        agent.screenshot(str(OUTPUT_DIR / f"product_showcase_{timestamp}.png"))
        assets["showcase"] = f"product_showcase_{timestamp}.png"
    
    # Save manifest
    manifest = {
        "generated_at": datetime.now().isoformat(),
        "website": "https://psdepot.com",
        "assets": assets,
        "output_dir": str(OUTPUT_DIR)
    }
    
    manifest_path = OUTPUT_DIR / f"manifest_{timestamp}.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n✅ Social assets generated!")
    print(f"📁 Output: {OUTPUT_DIR}")
    print(f"\nAssets created:")
    for platform, file in assets.items():
        print(f"  - {platform}: {file}")
    
    return assets

if __name__ == "__main__":
    generate_social_assets()
