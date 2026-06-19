# Browser Agent Skill

Automated browser automation for marketing, research, and data extraction using Playwright.

---

## Installation

```bash
# Install Playwright globally
npm install -g playwright

# Install browser binaries
playwright install chromium

# Optional: Install all browsers
playwright install
```

---

## Quick Start

```python
from browser_agent import BrowserAgent

# Initialize agent
agent = BrowserAgent(headless=False)  # Set True for production

# Navigate and screenshot
agent.navigate("https://psdepot.com")
agent.screenshot("homepage.png")

# Fill form
agent.fill_form({
    "name": "Test User",
    "email": "test@example.com",
    "message": "Testing contact form"
})

# Close
agent.close()
```

---

## Use Cases

### 1. Competitor Price Monitoring

```python
agent = BrowserAgent()
agent.navigate("https://www.webstaurantstore.com")
agent.search("thermal paper 3 1/8")
prices = agent.extract_prices()
agent.save_json(prices, "competitor_prices.json")
agent.close()
```

### 2. Screenshot Marketing Content

```python
agent = BrowserAgent(viewport={"width": 1920, "height": 1080})
agent.navigate("https://psdepot.com")
agent.screenshot_full_page("website_screenshot.png")

# Mobile view
agent.set_viewport({"width": 375, "height": 812})
agent.screenshot("mobile_view.png")
agent.close()
```

### 3. Form Testing

```python
agent = BrowserAgent()
agent.navigate("https://psdepot.com/contact")
agent.fill_form({
    "name": "Miles",
    "email": "miles@psdepot.com",
    "phone": "888-881-6834",
    "message": "Testing contact form functionality"
})
agent.click_submit()
agent.wait_for_success_message()
agent.close()
```

### 4. PDF Generation

```python
agent = BrowserAgent()
agent.navigate("https://psdepot.com")
agent.save_pdf("psdepot_brochure.pdf", {
    "format": "A4",
    "printBackground": True
})
agent.close()
```

### 5. Social Media Content

```python
agent = BrowserAgent()

# TikTok preview
agent.navigate("https://psdepot.com")
agent.execute_script("window.scrollTo(0, 500)")
agent.screenshot("product_highlight.png")

# Add text overlay with Pillow
from PIL import Image, ImageDraw, ImageFont
img = Image.open("product_highlight.png")
draw = ImageDraw.Draw(img)
draw.text((50, 50), "POS Supplies in Vegas", fill="white")
img.save("tiktok_content.png")

agent.close()
```

---

## API Reference

### BrowserAgent Class

#### Initialization
```python
BrowserAgent(
    headless=True,           # Run without visible browser
    slow_mo=0,              # Slow down operations (ms)
    viewport={"width": 1280, "height": 720},
    user_agent=None         # Custom user agent
)
```

#### Navigation
```python
.navigate(url, wait_until="networkidle")
.back()
.forward()
.reload()
.wait_for_load_state(state="networkidle")
```

#### Interaction
```python
.click(selector)
.fill(selector, text)
.select_option(selector, value)
.hover(selector)
.scroll_to(selector)
.execute_script(script)
```

#### Forms
```python
.fill_form(data_dict)           # Fill multiple fields
.submit_form(selector)
.upload_file(selector, path)
.clear_field(selector)
```

#### Extraction
```python
.get_text(selector)
.get_attribute(selector, attr)
.get_html(selector)
.extract_table(selector)
.extract_links()
.extract_images()
```

#### Screenshots
```python
.screenshot(path, full_page=False)
.screenshot_element(selector, path)
.screenshot_full_page(path)
.compare_screenshots(img1, img2)  # Visual diff
```

#### PDF
```python
.save_pdf(path, options={})
```

#### Data Export
```python
.save_json(data, path)
.save_csv(data, path)
.save_html(path)
```

---

## Marketing Automation Workflows

### Weekly Competitor Report

```python
from browser_agent import BrowserAgent
import datetime

def competitor_report():
    agent = BrowserAgent(headless=True)
    report = {
        "date": datetime.now().isoformat(),
        "competitors": []
    }
    
    # Check WebstaurantStore
    agent.navigate("https://www.webstaurantstore.com")
    agent.search("thermal paper 3 1/8")
    report["competitors"].append({
        "name": "WebstaurantStore",
        "thermal_paper_price": agent.get_text(".price"),
        "shipping": agent.get_text(".shipping-info")
    })
    
    # Check Amazon
    agent.navigate("https://www.amazon.com")
    agent.search("thermal receipt paper 3 1/8 x 230")
    report["competitors"].append({
        "name": "Amazon",
        "thermal_paper_price": agent.get_text(".a-price"),
        "delivery": agent.get_text("#deliveryBlock")
    })
    
    agent.save_json(report, f"competitor_report_{datetime.now().strftime('%Y%m%d')}.json")
    agent.close()
    
    return report

# Run weekly via cron
competitor_report()
```

### Social Media Content Generator

```python
def generate_social_content():
    agent = BrowserAgent(viewport={"width": 1200, "height": 675})
    
    # Screenshot products
    agent.navigate("https://psdepot.com")
    agent.screenshot("fb_cover.png")
    
    # Screenshot specific product
    agent.click("#products")
    agent.screenshot_element(".product-card:first-child", "featured_product.png")
    
    # Mobile for Instagram Stories
    agent.set_viewport({"width": 1080, "height": 1920})
    agent.screenshot("ig_story.png")
    
    agent.close()
    
    return {
        "facebook": "fb_cover.png",
        "product": "featured_product.png",
        "instagram": "ig_story.png"
    }
```

### Lead Research

```python
def research_lead(business_name, website):
    agent = BrowserAgent(headless=True)
    intel = {
        "business": business_name,
        "website": website
    }
    
    try:
        agent.navigate(website)
        intel["pos_system"] = agent.search_for("POS|point of sale|register")
        intel["contact_info"] = agent.get_text(".contact, #contact")
        intel["social_media"] = agent.extract_links()
        intel["screenshot"] = f"{business_name}_website.png"
        agent.screenshot(intel["screenshot"])
    except:
        intel["error"] = "Could not access website"
    
    agent.close()
    return intel
```

---

## Advanced Features

### Stealth Mode

```python
agent = BrowserAgent(
    headless=True,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    extra_headers={
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com"
    }
)
```

### Proxy Support

```python
agent = BrowserAgent(
    proxy={
        "server": "http://proxy.example.com:8080",
        "username": "user",
        "password": "pass"
    }
)
```

### Authentication

```python
# HTTP Basic Auth
agent.authenticate("username", "password")

# Cookie-based
agent.set_cookie("session", "abc123", domain=".example.com")
```

---

## Error Handling

```python
from browser_agent import BrowserAgent, NavigationError, TimeoutError

try:
    agent = BrowserAgent()
    agent.navigate("https://example.com", timeout=30000)
    agent.screenshot("result.png")
except NavigationError as e:
    print(f"Failed to load: {e}")
except TimeoutError:
    print("Operation timed out")
finally:
    agent.close()
```

---

## Integration with Marketing System

```python
# Part of newsletter generation
from browser_agent import BrowserAgent
from newsletter_generator import get_weekly_newsletter

def create_newsletter_with_screenshots():
    newsletter = get_weekly_newsletter()
    agent = BrowserAgent()
    
    # Get product screenshots for newsletter
    agent.navigate("https://psdepot.com")
    agent.screenshot_element("#featured-products", "newsletter_products.png")
    
    # Add to newsletter
    newsletter["image"] = "newsletter_products.png"
    
    agent.close()
    return newsletter
```

---

## Command Line Usage

```bash
# Screenshot a website
python -m browser_agent screenshot https://psdepot.com output.png --full-page

# Test form
python -m browser_agent form https://psdepot.com/contact \
    --field "name=Miles" \
    --field "email=miles@psdepot.com" \
    --field "message=Test"

# PDF generation
python -m browser_agent pdf https://psdepot.com psdepot.pdf

# Competitor check
python -m browser_agent research webstaurantstore thermal-paper --output prices.json
```

---

## Cron Jobs

```bash
# Daily competitor monitoring
0 9 * * * cd /root/.openclaw/workspace && python3 -c "from skills.browser_agent import competitor_report; competitor_report()"

# Weekly social content generation
0 10 * * 1 cd /root/.openclaw/workspace && python3 -c "from skills.browser_agent import generate_social_content; generate_social_content()"
```

---

## Troubleshooting

**Browser doesn't start:**
```bash
playwright install chromium
```

**Timeout errors:**
Increase timeout or use `wait_for_selector` instead of sleep.

**Detection as bot:**
Use stealth mode with custom user agent and realistic delays.

**Memory issues:**
Close browser after each task or use `agent.clear_cache()`.

---

## File Structure

```
skills/browser-agent/
├── SKILL.md                    # This file
├── browser_agent.py           # Main Python module
├── examples/
│   ├── competitor_monitor.py
│   ├── screenshot_generator.py
│   ├── form_tester.py
│   └── pdf_generator.py
├── outputs/                   # Generated screenshots/PDFs
└── requirements.txt
```

---

**Status:** Ready for use
**Dependencies:** Playwright (npm install -g playwright)
**Maintainer:** Miles (Performance Supply Depot)
