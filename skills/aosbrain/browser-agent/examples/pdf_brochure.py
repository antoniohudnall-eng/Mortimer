#!/usr/bin/env python3
"""
PDF Brochure Generator
Generate PDF brochure from psdepot.com
"""

import json
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from browser_agent import BrowserAgent

OUTPUT_DIR = Path("/root/.openclaw/workspace/AGI_COMPANY/marketing/brochures")

def generate_pdf_brochure():
    """Generate PDF brochure from website"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    with BrowserAgent(headless=True) as agent:
        print("🌐 Loading psdepot.com...")
        agent.navigate("https://psdepot.com")
        
        # Wait for page to fully render
        agent.wait_for_timeout(3000)
        
        # Generate PDF with print styles
        pdf_path = OUTPUT_DIR / f"psdepot_brochure_{timestamp}.pdf"
        
        print("📄 Generating PDF...")
        agent.save_pdf(str(pdf_path))  # Use default options
        
        # Also generate product catalog (specific pages)
        print("📄 Generating product catalog...")
        agent.navigate("https://psdepot.com/#products")
        agent.wait_for_timeout(2000)
        
        catalog_path = OUTPUT_DIR / f"psdepot_catalog_{timestamp}.pdf"
        agent.save_pdf(str(catalog_path))  # Use default options
    
    # Save metadata
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "website": "https://psdepot.com",
        "brochure": str(pdf_path),
        "catalog": str(catalog_path),
        "output_dir": str(OUTPUT_DIR)
    }
    
    meta_path = OUTPUT_DIR / f"metadata_{timestamp}.json"
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✅ PDFs generated!")
    print(f"📄 Brochure: {pdf_path}")
    print(f"📄 Catalog: {catalog_path}")
    print(f"📁 Output: {OUTPUT_DIR}")
    
    return metadata

if __name__ == "__main__":
    generate_pdf_brochure()
