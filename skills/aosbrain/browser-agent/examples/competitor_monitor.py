#!/usr/bin/env python3
"""
Competitor Price Monitoring
Run weekly to track competitor pricing
"""

import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

COMPETITORS = [
    {
        "name": "WebstaurantStore",
        "url": "https://www.webstaurantstore.com",
        "search_term": "thermal paper 3 1/8 x 230",
        "price_selector": ".price"  # May need adjustment
    },
    {
        "name": "Amazon",
        "url": "https://www.amazon.com",
        "search_term": "thermal receipt paper 3 1/8",
        "price_selector": ".a-price-whole"
    }
]

def monitor_competitors():
    """Monitor competitor prices and save report"""
    from playwright.sync_api import sync_playwright
    
    report = {
        "date": datetime.now().isoformat(),
        "competitors": []
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        for comp in COMPETITORS:
            print(f"🔍 Checking {comp['name']}...")
            
            try:
                page = context.new_page()
                
                # Navigate directly to search results
                search_url = comp.get('search_url', comp['url'])
                page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(3000)
                
                # Take screenshot for debugging
                screenshot_path = f"/tmp/{comp['name'].lower()}_debug.png"
                page.screenshot(path=screenshot_path)
                
                # Extract price - try multiple selectors
                price = None
                price_selectors = [
                    comp['price_selector'],
                    ".price",
                    "[data-testid='price']",
                    ".a-price .a-offscreen",
                    ".a-price-whole",
                    ".ProductPrice",
                    "[class*='price']"
                ]
                
                for selector in price_selectors:
                    try:
                        element = page.locator(selector).first
                        if element.count() > 0:
                            price_text = element.text_content()
                            if price_text and "$" in price_text:
                                price = price_text.strip()
                                break
                    except:
                        continue
                
                # Extract product name
                product_name = None
                try:
                    product_name = page.locator("h1, h2, .product-title, [data-testid='title']").first.text_content()
                except:
                    pass
                
                report["competitors"].append({
                    "name": comp['name'],
                    "url": search_url,
                    "price": price,
                    "product": product_name,
                    "screenshot": screenshot_path,
                    "status": "success" if price else "no_price_found"
                })
                
                print(f"✅ {comp['name']}: {price or 'No price found'}")
                page.close()
                
            except Exception as e:
                report["competitors"].append({
                    "name": comp['name'],
                    "price": None,
                    "status": "error",
                    "error": str(e)
                })
                print(f"❌ {comp['name']}: {e}")
        
        browser.close()
    
    # Save report
    output_dir = Path("/root/.openclaw/workspace/data/competitor_reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = output_dir / f"report_{datetime.now().strftime('%Y%m%d')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📊 Report saved: {report_file}")
    return report

if __name__ == "__main__":
    report = monitor_competitors()
    
    # Print summary
    print("\n" + "=" * 60)
    print("COMPETITOR PRICE SUMMARY")
    print("=" * 60)
    
    for comp in report["competitors"]:
        if comp["status"] == "success":
            print(f"{comp['name']}: {comp['price']}")
        else:
            print(f"{comp['name']}: ERROR - {comp.get('error', 'Unknown')}")
    
    print(f"\nYour price: $69.00/case (competitive)")
