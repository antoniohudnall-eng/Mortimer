#!/usr/bin/env python3
"""
Test Browser Agent with Local Content
Simpler test before hitting external sites
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from browser_agent import BrowserAgent

OUTPUT_DIR = Path("/root/.openclaw/workspace/AGI_COMPANY/marketing")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def test_basic_functionality():
    """Test browser agent with a simple page"""
    print("🧪 Testing browser agent...")
    
    with BrowserAgent(headless=True) as agent:
        # Test 1: Basic navigation
        print("🌐 Loading example.com...")
        agent.navigate("https://example.com", wait_until="domcontentloaded")
        agent.wait_for_timeout(1000)
        
        # Test 2: Screenshot
        print("📸 Taking screenshot...")
        screenshot_path = OUTPUT_DIR / "test_screenshot.png"
        agent.screenshot(str(screenshot_path))
        print(f"✅ Screenshot saved: {screenshot_path}")
        
        # Test 3: Get text
        print("📝 Extracting content...")
        text = agent.get_text("h1, p")
        print(f"✅ Found: {text[:100]}...")
        
        # Test 4: PDF generation
        print("📄 Generating PDF...")
        pdf_path = OUTPUT_DIR / "test_brochure.pdf"
        agent.save_pdf(str(pdf_path))
        print(f"✅ PDF saved: {pdf_path}")
    
    print("\n✅ All tests passed!")
    return True

if __name__ == "__main__":
    test_basic_functionality()
