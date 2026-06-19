#!/usr/bin/env python3
"""
Dark Factory Equipment Procurement Web Scraper
Agent: Spindle (CTO)
Purpose: Scrape equipment suppliers, prices, and availability
"""

import asyncio
import aiohttp
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, quote
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EquipmentScraper")

@dataclass
class EquipmentListing:
    """Represents a scraped equipment listing"""
    name: str
    category: str
    supplier: str
    price: Optional[float]
    currency: str
    availability: str
    lead_time_days: Optional[int]
    condition: str  # new, used, refurbished
    specifications: Dict[str, str]
    url: str
    scraped_at: str
    confidence_score: float  # 0.0 to 1.0

@dataclass
class Supplier:
    """Equipment supplier information"""
    name: str
    base_url: str
    reliability_score: float
    payment_terms: str
    shipping_regions: List[str]
    api_endpoint: Optional[str] = None

class EquipmentScraper:
    """
    Multi-source equipment scraper for Dark Factory procurement
    Supports: Direct websites, APIs, RSS feeds, and email alerts
    """
    
    EQUIPMENT_CATEGORIES = {
        "industrial_robots": [
            "articulated_arm", "scara", "delta", "cobot", "gantry"
        ],
        "cnc_machines": [
            "milling", "turning", "grinding", "laser_cutting", "plasma"
        ],
        "3d_printers": [
            "fdm", "sla", "sls", "metal", "large_format"
        ],
        "agv_amr": [
            "forklift_agv", "tugger_agv", "amr", "conveyor"
        ],
        "vision_systems": [
            "2d_camera", "3d_scanner", "thermal_camera", "xray_inspection"
        ],
        "sensors_iot": [
            "vibration", "temperature", "pressure", "flow", "proximity"
        ],
        "plc_controllers": [
            "siemens", "allen_bradley", "mitsubishi", "schneider"
        ]
    }
    
    SUPPLIERS = [
        Supplier("ThomasNet", "https://www.thomasnet.com", 0.92, "NET_30", ["US", "CA", "MX"]),
        Supplier("Alibaba_Industrial", "https://www.alibaba.com/trade/search", 0.85, "T/T", ["Global"]),
        Supplier("Machinio", "https://www.machinio.com", 0.88, "Varies", ["US", "EU"]),
        Supplier("EquipNet", "https://www.equipnet.com", 0.90, "NET_15", ["Global"]),
        Supplier("DirectIndustry", "https://www.directindustry.com", 0.87, "Varies", ["EU", "US", "Asia"]),
        Supplier("CNC_Exchange", "https://www.cncexchange.com", 0.89, "Escrow", ["US", "EU"]),
        Supplier("RobotShop_Industrial", "https://www.robotshop.com", 0.84, "CC", ["US", "CA", "EU"]),
    ]
    
    def __init__(self, cache_file: str = "equipment_cache.json"):
        self.cache_file = cache_file
        self.session: Optional[aiohttp.ClientSession] = None
        self.cache: Dict = self._load_cache()
        self.rate_limit_delay = 1.0  # seconds between requests
        
    def _load_cache(self) -> Dict:
        """Load cached equipment data"""
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"listings": [], "last_update": None}
    
    def _save_cache(self):
        """Save equipment data to cache"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2, default=str)
    
    async def __aenter__(self):
        """Async context manager entry"""
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=3)
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                "User-Agent": "DarkFactory-ProcurementBot/1.0 (AGI-Company)"
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
        self._save_cache()
    
    async def _fetch_with_retry(self, url: str, retries: int = 3) -> Optional[str]:
        """Fetch URL with retry logic and rate limiting"""
        for attempt in range(retries):
            try:
                await asyncio.sleep(self.rate_limit_delay + random.uniform(0, 0.5))
                async with self.session.get(url, ssl=False) as response:
                    if response.status == 200:
                        return await response.text()
                    elif response.status == 429:
                        wait = (attempt + 1) * 5
                        logger.warning(f"Rate limited. Waiting {wait}s...")
                        await asyncio.sleep(wait)
                    else:
                        logger.error(f"HTTP {response.status} for {url}")
                        return None
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)
        return None
    
    async def scrape_thomasnet(self, category: str, keywords: List[str]) -> List[EquipmentListing]:
        """Scrape ThomasNet for industrial equipment"""
        listings = []
        search_term = quote(" ".join(keywords))
        url = f"{self.SUPPLIERS[0].base_url}/search.html?WT=prodsearch&searchpos=1&WT.srch=1&what={search_term}"
        
        html = await self._fetch_with_retry(url)
        if not html:
            return listings
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # ThomasNet product cards
        for card in soup.find_all('div', class_=['result-item', 'product-card']):
            try:
                name_elem = card.find('a', class_=['result-title', 'product-title'])
                price_elem = card.find('span', class_=['price', 'result-price'])
                company_elem = card.find('a', class_=['company-name', 'supplier-name'])
                
                name = name_elem.text.strip() if name_elem else "Unknown"
                company = company_elem.text.strip() if company_elem else "Unknown"
                
                price = None
                if price_elem:
                    price_text = price_elem.text.strip()
                    price_match = re.search(r'[\d,]+\.?\d*', price_text)
                    if price_match:
                        price = float(price_match.group().replace(',', ''))
                
                listing = EquipmentListing(
                    name=name,
                    category=category,
                    supplier=company,
                    price=price,
                    currency="USD",
                    availability=self._extract_availability(card),
                    lead_time_days=None,
                    condition="new",
                    specifications=self._extract_specs(card),
                    url=urljoin(self.SUPPLIERS[0].base_url, name_elem['href']) if name_elem else url,
                    scraped_at=datetime.now().isoformat(),
                    confidence_score=0.75 if price else 0.5
                )
                listings.append(listing)
                
            except Exception as e:
                logger.error(f"Error parsing ThomasNet card: {e}")
                continue
        
        return listings
    
    async def scrape_alibaba(self, category: str, keywords: List[str]) -> List[EquipmentListing]:
        """Scrape Alibaba for industrial equipment"""
        listings = []
        search_term = quote(" ".join(keywords))
        url = f"{self.SUPPLIERS[1].base_url}?fsb=y&IndexArea=product_en&CatId=&SearchText={search_term}"
        
        html = await self._fetch_with_retry(url)
        if not html:
            return listings
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Alibaba product cards
        for card in soup.find_all('div', class_=['item', 'product-card', 'offer-item']):
            try:
                name_elem = card.find('a', class_=['title', 'product-title', 'subject'])
                price_elem = card.find('span', class_=['price', 'price-num', 'element-price'])
                supplier_elem = card.find('a', class_=['company', 'supplier-name'])
                
                name = name_elem.get('title', name_elem.text.strip()) if name_elem else "Unknown"
                supplier = supplier_elem.text.strip() if supplier_elem else "Alibaba Supplier"
                
                price = None
                currency = "USD"
                if price_elem:
                    price_text = price_elem.text.strip()
                    currency_match = re.search(r'(USD|\$|EUR|€|CNY|¥)', price_text)
                    if currency_match:
                        currency = "USD" if currency_match.group() in ["USD", "$"] else currency_match.group()
                    price_match = re.search(r'[\d,]+\.?\d*', price_text)
                    if price_match:
                        price = float(price_match.group().replace(',', ''))
                
                listing = EquipmentListing(
                    name=name,
                    category=category,
                    supplier=supplier,
                    price=price,
                    currency=currency,
                    availability="in_stock" if "in stock" in str(card).lower() else "contact_supplier",
                    lead_time_days=30,  # Typical for Alibaba
                    condition="new",
                    specifications=self._extract_specs(card),
                    url=name_elem['href'] if name_elem else url,
                    scraped_at=datetime.now().isoformat(),
                    confidence_score=0.70
                )
                listings.append(listing)
                
            except Exception as e:
                logger.error(f"Error parsing Alibaba card: {e}")
                continue
        
        return listings
    
    async def scrape_machinio(self, category: str, keywords: List[str]) -> List[EquipmentListing]:
        """Scrape Machinio for used equipment"""
        listings = []
        search_term = "-".join(keywords).lower().replace(" ", "-")
        url = f"{self.SUPPLIERS[2].base_url}/search?q={search_term}"
        
        html = await self._fetch_with_retry(url)
        if not html:
            return listings
        
        soup = BeautifulSoup(html, 'html.parser')
        
        for card in soup.find_all('div', class_=['listing-card', 'search-result']):
            try:
                name_elem = card.find('h2', class_='listing-title')
                price_elem = card.find('span', class_=['listing-price', 'price'])
                location_elem = card.find('span', class_='location')
                
                name = name_elem.text.strip() if name_elem else "Unknown"
                
                price = None
                if price_elem:
                    price_text = price_elem.text.strip()
                    price_match = re.search(r'[\d,]+', price_text)
                    if price_match:
                        price = float(price_match.group().replace(',', ''))
                
                condition = "used" if "used" in name.lower() else "refurbished"
                
                listing = EquipmentListing(
                    name=name,
                    category=category,
                    supplier="Machinio",
                    price=price,
                    currency="USD",
                    availability="available",
                    lead_time_days=14,
                    condition=condition,
                    specifications={"location": location_elem.text.strip() if location_elem else "Unknown"},
                    url=urljoin(self.SUPPLIERS[2].base_url, name_elem.find('a')['href']) if name_elem else url,
                    scraped_at=datetime.now().isoformat(),
                    confidence_score=0.85 if price else 0.6
                )
                listings.append(listing)
                
            except Exception as e:
                logger.error(f"Error parsing Machinio card: {e}")
                continue
        
        return listings
    
    def _extract_availability(self, soup_element) -> str:
        """Extract availability status from HTML element"""
        text = str(soup_element).lower()
        if any(word in text for word in ['in stock', 'available', 'ready']):
            return "in_stock"
        elif any(word in text for word in ['out of stock', 'unavailable']):
            return "out_of_stock"
        elif any(word in text for word in ['pre-order', 'backorder']):
            return "backorder"
        return "unknown"
    
    def _extract_specs(self, soup_element) -> Dict[str, str]:
        """Extract specifications from HTML element"""
        specs = {}
        spec_table = soup_element.find('table', class_=['specs', 'specifications'])
        if spec_table:
            for row in spec_table.find_all('tr'):
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    key = cells[0].text.strip().lower().replace(' ', '_')
                    value = cells[1].text.strip()
                    specs[key] = value
        return specs
    
    async def search_equipment(
        self, 
        category: str, 
        keywords: Optional[List[str]] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        condition: Optional[str] = None
    ) -> List[EquipmentListing]:
        """
        Search for equipment across all suppliers
        
        Args:
            category: Equipment category (e.g., "industrial_robots")
            keywords: Additional search keywords
            min_price: Minimum price filter
            max_price: Maximum price filter
            condition: Filter by condition ("new", "used", "refurbished")
        
        Returns:
            List of EquipmentListing objects
        """
        if category not in self.EQUIPMENT_CATEGORIES:
            raise ValueError(f"Unknown category: {category}")
        
        if not keywords:
            keywords = self.EQUIPMENT_CATEGORIES[category][:3]
        
        logger.info(f"Searching for {category}: {keywords}")
        
        # Search multiple sources concurrently
        tasks = [
            self.scrape_thomasnet(category, keywords),
            self.scrape_alibaba(category, keywords),
            self.scrape_machinio(category, keywords),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_listings = []
        for result in results:
            if isinstance(result, list):
                all_listings.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"Scraping task failed: {result}")
        
        # Apply filters
        filtered = []
        for listing in all_listings:
            if min_price and listing.price and listing.price < min_price:
                continue
            if max_price and listing.price and listing.price > max_price:
                continue
            if condition and listing.condition != condition:
                continue
            filtered.append(listing)
        
        # Sort by confidence score
        filtered.sort(key=lambda x: x.confidence_score, reverse=True)
        
        logger.info(f"Found {len(filtered)} listings for {category}")
        return filtered
    
    def get_price_analysis(self, listings: List[EquipmentListing]) -> Dict:
        """Analyze pricing data from listings"""
        prices = [l.price for l in listings if l.price]
        if not prices:
            return {"error": "No price data available"}
        
        return {
            "count": len(prices),
            "mean": sum(prices) / len(prices),
            "median": sorted(prices)[len(prices) // 2],
            "min": min(prices),
            "max": max(prices),
            "std_dev": (sum((x - sum(prices)/len(prices))**2 for x in prices) / len(prices)) ** 0.5,
            "currency": listings[0].currency if listings else "USD"
        }
    
    def export_to_procurement(self, listings: List[EquipmentListing], filename: str = "procurement_input.json"):
        """Export listings to procurement system format"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "total_listings": len(listings),
            "listings": [asdict(l) for l in listings],
            "price_analysis": self.get_price_analysis(listings)
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Exported {len(listings)} listings to {filename}")
        return filename


# Real API integrations for verified suppliers
class VerifiedSupplierAPI:
    """Direct API integrations for verified suppliers"""
    
    API_ENDPOINTS = {
        "siemens": "https://mall.industry.siemens.com/api/v1",
        "allen_bradley": "https://rockwellautomation.com/api/commerce",
        "fanuc": "https://fanucamerica.com/api/v2/products",
        "universal_robots": "https://universal-robots.com/api/products",
    }
    
    async def fetch_siemens_catalog(self, product_type: str) -> List[Dict]:
        """Fetch Siemens industrial automation catalog"""
        # Note: Requires API key in production
        url = f"{self.API_ENDPOINTS['siemens']}/products"
        params = {"category": product_type, "availability": "instock"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("products", [])
        return []
    
    async def fetch_fanuc_robots(self, payload_kg: Optional[int] = None) -> List[Dict]:
        """Fetch FANUC robot catalog"""
        url = self.API_ENDPOINTS["fanuc"]
        params = {}
        if payload_kg:
            params["min_payload"] = payload_kg
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    return await resp.json()
        return []


async def main():
    """Main execution for standalone scraper"""
    scraper = EquipmentScraper()
    
    async with scraper:
        # Search for industrial robots
        logger.info("=== Searching for Industrial Robots ===")
        robot_listings = await scraper.search_equipment(
            category="industrial_robots",
            keywords=["6-axis", "industrial", "robotic arm"],
            condition="new"
        )
        
        print(f"\nFound {len(robot_listings)} robot listings")
        if robot_listings:
            print(f"Price range: ${min(l.price for l in robot_listings if l.price):,.2f} - ${max(l.price for l in robot_listings if l.price):,.2f}")
        
        # Search for CNC machines
        logger.info("\n=== Searching for CNC Machines ===")
        cnc_listings = await scraper.search_equipment(
            category="cnc_machines",
            keywords=["CNC", "machining center", "5-axis"]
        )
        
        print(f"\nFound {len(cnc_listings)} CNC listings")
        
        # Export results
        scraper.export_to_procurement(robot_listings + cnc_listings, "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/procurement/scraped_equipment.json")


if __name__ == "__main__":
    asyncio.run(main())