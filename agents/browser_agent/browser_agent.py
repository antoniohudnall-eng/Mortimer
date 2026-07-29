#!/usr/bin/env python3
"""
Browser Agent v1.0 — Real web automation for SEED3
Uses requests + BeautifulSoup (works on Android/Termux, no Playwright needed)

Capabilities:
- Navigate and fetch pages
- Extract text, prices, links, tables
- Form submission (GET/POST)
- Screenshot as text dump (no headless browser on Android)
- JSON export
- Retry with backoff
- Rate limiting
- User-agent rotation
"""

import re
import json
import time
import hashlib
import random
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


# ─── User Agent Rotation ──────────────────────────
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148",
]


class BrowserAgent:
    """Real browser agent — scrapes, extracts, and exports web data."""
    
    def __init__(self, headless: bool = True, timeout: int = 15, max_retries: int = 3):
        self.headless = headless  # Always headless on Termux
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.last_url: Optional[str] = None
        self.last_response: Optional[requests.Response] = None
        self.last_soup: Optional[BeautifulSoup] = None
        self.history: List[Dict] = []
        self._rotate_ua()
        
    def _rotate_ua(self):
        """Rotate user agent for each session"""
        self.session.headers.update({
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        })
    
    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        """HTTP request with retry and backoff"""
        last_error = None
        for attempt in range(self.max_retries):
            try:
                kwargs.setdefault("timeout", self.timeout)
                kwargs.setdefault("allow_redirects", True)
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    wait = (attempt + 1) * 2
                    time.sleep(wait)
        
        raise last_error or Exception(f"Failed after {self.max_retries} retries: {url}")
    
    # ─── Core Navigation ──────────────────────────
    
    def navigate(self, url: str) -> "BrowserAgent":
        """Navigate to a URL and parse the page"""
        self._rotate_ua()
        response = self._request("GET", url)
        self.last_url = url
        self.last_response = response
        self.last_soup = BeautifulSoup(response.text, "html.parser")
        
        self.history.append({
            "url": url,
            "status": response.status_code,
            "timestamp": time.time(),
            "size": len(response.text)
        })
        
        return self
    
    def search(self, query: str) -> "BrowserAgent":
        """Submit a search query via GET params (q=)"""
        url = f"{self.last_url}?q={requests.utils.quote(query)}" if self.last_url else query
        return self.navigate(url)
    
    def fill_form(self, data: Dict[str, str], submit: bool = True) -> "BrowserAgent":
        """Submit form data via POST"""
        if not self.last_url:
            raise ValueError("Navigate to a page first")
        
        response = self._request("POST", self.last_url, data=data)
        self.last_response = response
        self.last_soup = BeautifulSoup(response.text, "html.parser")
        return self
    
    # ─── Extraction Methods ───────────────────────
    
    def extract_text(self, selector: Optional[str] = None) -> str:
        """Extract text from the page or specific element"""
        if not self.last_soup:
            return ""
        
        if selector:
            el = self.last_soup.select_one(selector)
            return el.get_text(strip=True) if el else ""
        
        # Remove script and style
        for tag in self.last_soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        
        return self.last_soup.get_text(separator="\n", strip=True)[:5000]
    
    def extract_prices(self) -> List[Dict[str, Any]]:
        """Extract prices from the page using common price patterns"""
        if not self.last_soup:
            return []
        
        prices = []
        price_pattern = re.compile(r'\$[\d,]+\.?\d*')
        
        for el in self.last_soup.find_all(text=price_pattern):
            parent = el.parent
            # Get context — nearby product name/title
            context = ""
            for sibling in parent.find_all(["h1", "h2", "h3", "h4", "span", "a"]):
                text = sibling.get_text(strip=True)
                if text and len(text) < 200:
                    context = text
                    break
            
            prices.append({
                "price": el.strip(),
                "context": context[:100],
                "tag": parent.name if parent else "unknown"
            })
        
        return prices[:20]  # Limit to 20
    
    def extract_links(self, internal_only: bool = True) -> List[Dict[str, str]]:
        """Extract all links from the page"""
        if not self.last_soup:
            return []
        
        base_domain = urlparse(self.last_url).netloc if self.last_url else ""
        links = []
        
        for a in self.last_soup.find_all("a", href=True):
            href = urljoin(self.last_url or "", a["href"])
            text = a.get_text(strip=True)[:100]
            
            if internal_only and urlparse(href).netloc != base_domain:
                continue
            
            links.append({"url": href, "text": text})
        
        return links[:50]
    
    def extract_table(self, selector: str = "table") -> List[List[str]]:
        """Extract tabular data from the first matching table"""
        if not self.last_soup:
            return []
        
        table = self.last_soup.select_one(selector)
        if not table:
            return []
        
        rows = []
        for tr in table.find_all("tr"):
            row = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            if row:
                rows.append(row)
        
        return rows
    
    def extract_meta(self) -> Dict[str, str]:
        """Extract meta tags (title, description, keywords)"""
        if not self.last_soup:
            return {}
        
        meta = {}
        
        title = self.last_soup.find("title")
        if title:
            meta["title"] = title.get_text(strip=True)
        
        for tag in self.last_soup.find_all("meta"):
            name = tag.get("name", "") or tag.get("property", "")
            content = tag.get("content", "")
            if name and content:
                meta[name] = content[:200]
        
        return meta
    
    def extract_emails(self) -> List[str]:
        """Extract email addresses from the page"""
        if not self.last_soup:
            return []
        
        text = self.last_soup.get_text()
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        return list(set(emails))[:20]
    
    # ─── Status Methods ───────────────────────────
    
    @property
    def status_code(self) -> int:
        return self.last_response.status_code if self.last_response else 0
    
    @property
    def page_title(self) -> str:
        if not self.last_soup:
            return ""
        title = self.last_soup.find("title")
        return title.get_text(strip=True) if title else ""
    
    @property
    def page_size(self) -> int:
        return len(self.last_response.text) if self.last_response else 0
    
    def status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "current_url": self.last_url,
            "status_code": self.status_code,
            "page_title": self.page_title,
            "page_size": self.page_size,
            "history_count": len(self.history),
            "last_action": self.history[-1] if self.history else None
        }
    
    # ─── Export Methods ───────────────────────────
    
    def save_json(self, data: Any, filename: str) -> str:
        """Save data as JSON file"""
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return filename
    
    def snapshot(self, filename: Optional[str] = None) -> str:
        """Save a text snapshot of the current page"""
        if not filename:
            domain = urlparse(self.last_url).netloc.replace(".", "_") if self.last_url else "page"
            filename = f"snapshot_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        content = f"URL: {self.last_url}\n"
        content += f"Title: {self.page_title}\n"
        content += f"Date: {datetime.now().isoformat()}\n"
        content += f"{'='*60}\n\n"
        content += self.extract_text()
        
        Path(filename).write_text(content)
        return filename
    
    def close(self):
        """Clean up the session"""
        self.session.close()
        self.last_soup = None
        self.last_response = None
        return len(self.history)


# ─── Quick Functions ──────────────────────────────

def quick_scrape(url: str) -> Dict[str, Any]:
    """One-shot scrape — returns structured data"""
    agent = BrowserAgent()
    try:
        agent.navigate(url)
        result = {
            "url": url,
            "title": agent.page_title,
            "status": agent.status_code,
            "meta": agent.extract_meta(),
            "prices": agent.extract_prices(),
            "emails": agent.extract_emails(),
            "links_count": len(agent.extract_links()),
            "text_preview": agent.extract_text()[:500]
        }
        return result
    finally:
        agent.close()


def competitor_check(url: str, keywords: List[str]) -> Dict[str, Any]:
    """Check competitor page for pricing and keywords"""
    agent = BrowserAgent()
    try:
        agent.navigate(url)
        text = agent.extract_text().lower()
        
        found_keywords = [kw for kw in keywords if kw.lower() in text]
        
        return {
            "url": url,
            "title": agent.page_title,
            "prices_found": len(agent.extract_prices()),
            "keywords_matched": found_keywords,
            "match_count": len(found_keywords),
            "page_size": agent.page_size,
            "emails": agent.extract_emails()
        }
    finally:
        agent.close()


# ─── CLI ──────────────────────────────────────────

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Browser Agent v1.0 — SEED3")
        print("Usage: python3 browser_agent.py <url> [action]")
        print("Actions: scrape (default), prices, links, meta, snapshot, competitor")
        sys.exit(1)
    
    url = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else "scrape"
    
    agent = BrowserAgent()
    
    try:
        agent.navigate(url)
        print(f"✅ Navigated: {agent.page_title} ({agent.status_code})")
        
        if action == "scrape" or action == "all":
            result = {
                "title": agent.page_title,
                "meta": agent.extract_meta(),
                "prices": agent.extract_prices(),
                "emails": agent.extract_emails(),
                "links": len(agent.extract_links())
            }
            print(json.dumps(result, indent=2))
        
        elif action == "prices":
            prices = agent.extract_prices()
            for p in prices:
                print(f"  {p['price']} — {p['context']}")
        
        elif action == "links":
            links = agent.extract_links(internal_only=False)
            for l in links[:20]:
                print(f"  {l['url']} — {l['text'][:80]}")
        
        elif action == "meta":
            meta = agent.extract_meta()
            for k, v in meta.items():
                print(f"  {k}: {v}")
        
        elif action == "snapshot":
            fname = agent.snapshot()
            print(f"Snapshot saved: {fname}")
        
        elif action == "competitor":
            keywords = sys.argv[3:] if len(sys.argv) > 3 else ["price", "buy", "order"]
            result = competitor_check(url, keywords)
            print(json.dumps(result, indent=2))
    
    finally:
        count = agent.close()
        print(f"\n📊 Session: {count} page(s) visited")
