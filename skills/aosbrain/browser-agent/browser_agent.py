#!/usr/bin/env python3
"""
Browser Agent - Playwright-based browser automation
For Performance Supply Depot marketing, research, and data extraction
"""

import json
import time
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright not installed. Run: npm install -g playwright && playwright install chromium")


class BrowserAgent:
    """
    Automated browser agent for marketing, research, and content generation.
    Uses Playwright for reliable automation.
    """
    
    def __init__(
        self,
        headless: bool = True,
        slow_mo: int = 0,
        viewport: Dict[str, int] = None,
        user_agent: Optional[str] = None,
        proxy: Optional[Dict] = None
    ):
        """
        Initialize browser agent
        
        Args:
            headless: Run without visible browser window
            slow_mo: Slow down operations by N milliseconds
            viewport: Browser viewport size {"width": 1280, "height": 720}
            user_agent: Custom user agent string
            proxy: Proxy configuration {"server": "http://proxy:8080"}
        """
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright not installed. Run: npm install -g playwright")
        
        self.headless = headless
        self.slow_mo = slow_mo
        self.viewport = viewport or {"width": 1280, "height": 720}
        self.custom_user_agent = user_agent
        self.proxy = proxy
        
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
        self._init_browser()
    
    def _init_browser(self):
        """Initialize Playwright browser with stealth features"""
        self.playwright = sync_playwright().start()
        
        # Browser launch options with stealth
        launch_options = {
            "headless": self.headless,
            "slow_mo": self.slow_mo,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-accelerated-2d-canvas",
                "--disable-gpu",
                "--window-size=1920,1080",
            ]
        }
        
        if self.proxy:
            launch_options["proxy"] = self.proxy
        
        # Launch Chromium
        self.browser = self.playwright.chromium.launch(**launch_options)
        
        # Create context with stealth options
        context_options = {
            "viewport": self.viewport,
            "user_agent": self.custom_user_agent or self._get_default_user_agent(),
            "locale": "en-US",
            "timezone_id": "America/Los_Angeles",
            "geolocation": {"latitude": 36.1699, "longitude": -115.1398},  # Las Vegas
            "permissions": ["geolocation"],
            "color_scheme": "light",
            "reduced_motion": "no-preference",
        }
        
        self.context = self.browser.new_context(**context_options)
        
        # Add stealth scripts to evade detection
        self.context.add_init_script("""
            // Override navigator.webdriver
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // Override permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );
            
            // Hide automation flags
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            
            // Override chrome runtime
            window.chrome = { runtime: {} };
            
            // Override Notification
            const originalNotification = window.Notification;
            Object.defineProperty(window, 'Notification', {
                get: function() {
                    return originalNotification;
                },
                set: function(value) {
                    originalNotification = value;
                }
            });
        """)
        
        self.page = self.context.new_page()
        
        # Set extra headers for realism
        self.page.set_extra_http_headers({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        })
        
        # Set default timeout
        self.page.set_default_timeout(30000)
        
        print(f"✅ Browser initialized with stealth (headless={self.headless}, viewport={self.viewport})")
    
    def _get_default_user_agent(self) -> str:
        """Get realistic user agent"""
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    def navigate(self, url: str, wait_until: str = "networkidle") -> "BrowserAgent":
        """
        Navigate to URL
        
        Args:
            url: URL to navigate to
            wait_until: When to consider navigation complete
                       ("load", "domcontentloaded", "networkidle")
        
        Returns:
            Self for chaining
        """
        if not self.page:
            raise RuntimeError("Browser not initialized")
        
        print(f"🌐 Navigating to: {url}")
        self.page.goto(url, wait_until=wait_until)
        return self
    
    def wait_for_load_state(self, state: str = "networkidle") -> "BrowserAgent":
        """Wait for page to reach specific load state"""
        self.page.wait_for_load_state(state)
        return self
    
    def wait_for_selector(self, selector: str, timeout: int = 30000) -> "BrowserAgent":
        """Wait for element to appear"""
        self.page.wait_for_selector(selector, timeout=timeout)
        return self
    
    def wait_for_timeout(self, milliseconds: int) -> "BrowserAgent":
        """Wait for specified time"""
        self.page.wait_for_timeout(milliseconds)
        return self
    
    def click(self, selector: str) -> "BrowserAgent":
        """Click element"""
        print(f"🖱️  Clicking: {selector}")
        self.page.click(selector)
        return self
    
    def fill(self, selector: str, text: str) -> "BrowserAgent":
        """Fill text field"""
        print(f"⌨️  Filling {selector}: {text[:30]}...")
        self.page.fill(selector, text)
        return self
    
    def fill_form(self, data: Dict[str, str], submit: bool = False) -> "BrowserAgent":
        """
        Fill multiple form fields
        
        Args:
            data: Dict of {selector: value}
            submit: Whether to submit form after filling
        """
        print(f"📝 Filling form with {len(data)} fields")
        for selector, value in data.items():
            try:
                self.fill(selector, value)
            except Exception as e:
                print(f"⚠️  Could not fill {selector}: {e}")
        
        if submit:
            self.submit_form()
        
        return self
    
    def submit_form(self, selector: str = "button[type='submit']") -> "BrowserAgent":
        """Submit form by clicking submit button"""
        print(f"📤 Submitting form")
        self.click(selector)
        return self
    
    def select_option(self, selector: str, value: str) -> "BrowserAgent":
        """Select dropdown option"""
        self.page.select_option(selector, value)
        return self
    
    def hover(self, selector: str) -> "BrowserAgent":
        """Hover over element"""
        self.page.hover(selector)
        return self
    
    def scroll_to(self, selector: str) -> "BrowserAgent":
        """Scroll element into view"""
        self.page.evaluate(f"document.querySelector('{selector}').scrollIntoView()")
        return self
    
    def scroll_to_position(self, x: int, y: int) -> "BrowserAgent":
        """Scroll to position"""
        self.page.evaluate(f"window.scrollTo({x}, {y})")
        return self
    
    def execute_script(self, script: str) -> Any:
        """Execute JavaScript"""
        return self.page.evaluate(script)
    
    def get_text(self, selector: str) -> str:
        """Get text content of element"""
        try:
            return self.page.inner_text(selector)
        except:
            return ""
    
    def get_attribute(self, selector: str, attribute: str) -> str:
        """Get element attribute"""
        try:
            return self.page.get_attribute(selector, attribute) or ""
        except:
            return ""
    
    def get_html(self, selector: str = "body") -> str:
        """Get HTML content"""
        return self.page.inner_html(selector)
    
    def screenshot(self, path: str, full_page: bool = False) -> "BrowserAgent":
        """
        Take screenshot
        
        Args:
            path: Output file path
            full_page: Capture full scrollable page
        """
        print(f"📸 Screenshot: {path}")
        self.page.screenshot(path=path, full_page=full_page)
        return self
    
    def screenshot_element(self, selector: str, path: str) -> "BrowserAgent":
        """Screenshot specific element"""
        print(f"📸 Screenshot element {selector}: {path}")
        element = self.page.locator(selector).first
        element.screenshot(path=path)
        return self
    
    def screenshot_full_page(self, path: str) -> "BrowserAgent":
        """Screenshot full page (wrapper)"""
        return self.screenshot(path, full_page=True)
    
    def extract_links(self, selector: str = "a") -> List[Dict]:
        """Extract all links from page"""
        links = self.page.locator(selector).evaluate_all(
            """elements => elements.map(el => ({
                text: el.textContent.trim(),
                href: el.href,
                title: el.title
            }))"""
        )
        return links
    
    def extract_images(self) -> List[Dict]:
        """Extract all images from page"""
        images = self.page.locator("img").evaluate_all(
            """elements => elements.map(el => ({
                src: el.src,
                alt: el.alt,
                width: el.width,
                height: el.height
            }))"""
        )
        return images
    
    def search_for(self, keywords: str) -> List[str]:
        """Search page for keywords, return matching text"""
        results = []
        keywords_list = keywords.split("|")
        
        for keyword in keywords_list:
            matches = self.page.locator(f"text=/{keyword}/i").all()
            for match in matches:
                try:
                    text = match.inner_text()
                    if text:
                        results.append(text.strip())
                except:
                    pass
        
        return results
    
    def save_pdf(self, path: str, options: Dict = None) -> "BrowserAgent":
        """Save page as PDF"""
        print(f"📄 Saving PDF: {path}")
        
        default_options = {
            "format": "A4",
            "print_background": True,
            "margin": {"top": "1cm", "right": "1cm", "bottom": "1cm", "left": "1cm"}
        }
        
        if options:
            default_options.update(options)
        
        self.page.pdf(path=path, **default_options)
        return self
    
    def save_html(self, path: str) -> "BrowserAgent":
        """Save page HTML"""
        html = self.page.content()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"💾 HTML saved: {path}")
        return self
    
    def set_viewport(self, viewport: Dict[str, int]) -> "BrowserAgent":
        """Change viewport size"""
        self.page.set_viewport_size(viewport)
        self.viewport = viewport
        print(f"📐 Viewport changed to: {viewport}")
        return self
    
    def set_cookie(self, name: str, value: str, domain: str = None):
        """Set browser cookie"""
        cookie = {"name": name, "value": value}
        if domain:
            cookie["domain"] = domain
        self.context.add_cookies([cookie])
    
    def authenticate(self, username: str, password: str):
        """HTTP Basic Auth"""
        self.page.authenticate({"username": username, "password": password})
    
    def clear_cache(self):
        """Clear browser cache"""
        self.context.clear_cookies()
        print("🗑️  Cache cleared")
    
    def back(self) -> "BrowserAgent":
        """Go back"""
        self.page.go_back()
        return self
    
    def forward(self) -> "BrowserAgent":
        """Go forward"""
        self.page.go_forward()
        return self
    
    def reload(self) -> "BrowserAgent":
        """Reload page"""
        self.page.reload()
        return self
    
    def close(self):
        """Close browser and cleanup"""
        print("🔒 Closing browser...")
        
        if self.context:
            self.context.close()
        
        if self.browser:
            self.browser.close()
        
        if self.playwright:
            self.playwright.stop()
        
        print("✅ Browser closed")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Convenience functions for common tasks

def screenshot_website(url: str, output_path: str, full_page: bool = True) -> str:
    """Quick screenshot of website"""
    with BrowserAgent(headless=True) as agent:
        agent.navigate(url)
        agent.screenshot(output_path, full_page=full_page)
    return output_path


def save_website_pdf(url: str, output_path: str) -> str:
    """Quick PDF generation"""
    with BrowserAgent(headless=True) as agent:
        agent.navigate(url)
        agent.save_pdf(output_path)
    return output_path


def test_form(url: str, form_data: Dict[str, str], submit: bool = True) -> bool:
    """Quick form test"""
    try:
        with BrowserAgent(headless=True) as agent:
            agent.navigate(url)
            agent.fill_form(form_data, submit=submit)
            agent.wait_for_timeout(2000)
        return True
    except Exception as e:
        print(f"❌ Form test failed: {e}")
        return False


def competitor_monitor(url: str, price_selector: str) -> Dict:
    """Quick price extraction"""
    data = {
        "url": url,
        "timestamp": datetime.now().isoformat(),
        "price": None,
        "error": None
    }
    
    try:
        with BrowserAgent(headless=True) as agent:
            agent.navigate(url)
            price = agent.get_text(price_selector)
            data["price"] = price
    except Exception as e:
        data["error"] = str(e)
    
    return data


# Marketing automation workflows

def generate_social_media_assets(output_dir: str = "/tmp/social_assets"):
    """Generate screenshots for social media"""
    os.makedirs(output_dir, exist_ok=True)
    
    assets = {}
    
    with BrowserAgent(headless=True) as agent:
        # Desktop screenshot
        agent.navigate("https://psdepot.com")
        desktop_path = os.path.join(output_dir, "facebook_cover.png")
        agent.screenshot(desktop_path)
        assets["facebook"] = desktop_path
        
        # Mobile screenshot for Instagram
        agent.set_viewport({"width": 1080, "height": 1920})
        mobile_path = os.path.join(output_dir, "instagram_story.png")
        agent.screenshot(mobile_path, full_page=False)
        assets["instagram"] = mobile_path
        
        # Tablet for LinkedIn
        agent.set_viewport({"width": 1200, "height": 627})
        tablet_path = os.path.join(output_dir, "linkedin_post.png")
        agent.screenshot(tablet_path)
        assets["linkedin"] = tablet_path
    
    return assets


def generate_marketing_pdf(output_path: str = "/tmp/psdepot_brochure.pdf"):
    """Generate PDF brochure from website"""
    with BrowserAgent(headless=True) as agent:
        agent.navigate("https://psdepot.com")
        agent.save_pdf(output_path, {
            "format": "Letter",
            "print_background": True
        })
    return output_path


# Command line interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Browser Agent - Performance Supply Depot")
        print()
        print("Usage:")
        print("  python browser_agent.py screenshot URL OUTPUT [--full-page]")
        print("  python browser_agent.py pdf URL OUTPUT")
        print("  python browser_agent.py social OUTPUT_DIR")
        print("  python browser_agent.py test-form URL 'field1=value1,field2=value2'")
        print()
        print("Examples:")
        print("  python browser_agent.py screenshot https://psdepot.com psdepot.png --full-page")
        print("  python browser_agent.py pdf https://psdepot.com psdepot.pdf")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "screenshot" and len(sys.argv) >= 4:
        url = sys.argv[2]
        output = sys.argv[3]
        full_page = "--full-page" in sys.argv
        screenshot_website(url, output, full_page)
        print(f"✅ Screenshot saved: {output}")
        
    elif command == "pdf" and len(sys.argv) >= 4:
        url = sys.argv[2]
        output = sys.argv[3]
        save_website_pdf(url, output)
        print(f"✅ PDF saved: {output}")
        
    elif command == "social":
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "/tmp/social_assets"
        assets = generate_social_media_assets(output_dir)
        print(f"✅ Social assets generated in {output_dir}:")
        for platform, path in assets.items():
            print(f"  - {platform}: {path}")
            
    else:
        print(f"❌ Unknown command: {command}")
