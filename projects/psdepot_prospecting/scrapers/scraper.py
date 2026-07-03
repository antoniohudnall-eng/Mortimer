#!/usr/bin/env python3
"""
PSDEPOT Lead Generation - Multi-Source Scraper
Sources: Yellowbot, HotFrog, ShowMeLocal, EZLocal
"""

import csv
import json
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urljoin
from datetime import datetime
import os

# Configuration
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
}

CITIES = [
    {'city': 'Sacramento', 'state': 'CA', 'lat': 38.5816, 'lng': -121.4944},
    {'city': 'Elk Grove', 'state': 'CA', 'lat': 38.4088, 'lng': -121.3716},
    {'city': 'Santa Rosa', 'state': 'CA', 'lat': 38.4404, 'lng': -122.7141},
    {'city': 'Napa', 'state': 'CA', 'lat': 38.2975, 'lng': -122.2869},
    {'city': 'Sonoma', 'state': 'CA', 'lat': 38.2919, 'lng': -122.4580},
    {'city': 'Calistoga', 'state': 'CA', 'lat': 38.5785, 'lng': -122.5797},
    {'city': 'American Canyon', 'state': 'CA', 'lat': 38.1749, 'lng': -122.2611},
]

# PSDEPOT customer categories
CATEGORIES = {
    'mexican': ['taqueria', 'mexican restaurant', 'carniceria', 'panaderia', 'bodega'],
    'thai': ['thai restaurant'],
    'korean': ['korean restaurant'],
    'vietnamese': ['vietnamese restaurant', 'pho'],
    'chinese': ['chinese restaurant'],
    'japanese': ['japanese restaurant', 'sushi'],
    'indian': ['indian restaurant'],
    'filipino': ['filipino restaurant'],
    'pizza': ['pizza restaurant'],
    'cafe': ['cafe', 'coffee shop', 'bubble tea'],
    'bakery': ['bakery'],
    'bar': ['bar', 'sports bar'],
    'food_truck': ['food truck'],
    'mediterranean': ['mediterranean restaurant', 'greek restaurant'],
    'retail': ['convenience store', 'liquor store'],
}

OUTPUT_DIR = '/data/data/com.termux/files/home/mortimer/projects/psdepot_prospecting/data'


class LeadScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.businesses = []
        self.stats = {'scraped': 0, 'errors': 0}
    
    def get(self, url, retries=3):
        """Fetch with retries"""
        for attempt in range(retries):
            try:
                resp = self.session.get(url, timeout=15)
                if resp.status_code == 200:
                    return resp.text
                elif resp.status_code == 403:
                    print(f"    [!] Blocked (403)")
                else:
                    print(f"    [!] Status {resp.status_code}")
                time.sleep(random.uniform(2, 4))
            except Exception as e:
                print(f"    [!] Error: {e}")
                time.sleep(random.uniform(1, 3))
        return None
    
    def scrape_yellowbot(self, query, city, state, max_pages=3):
        """Scrape Yellowbot listings"""
        businesses = []
        search_term = quote_plus(query)
        location = quote_plus(f"{city}, {state}")
        
        for page in range(1, max_pages + 1):
            if page == 1:
                url = f"https://www.yellowbot.com/search?keywords={search_term}&geo={location}"
            else:
                url = f"https://www.yellowbot.com/search?keywords={search_term}&geo={location}&page={page}"
            
            print(f"    Yellowbot page {page}")
            html = self.get(url)
            
            if not html:
                continue
            
            soup = BeautifulSoup(html, 'html.parser')
            
            for listing in soup.select('.media'):
                try:
                    name_elem = listing.select_one('.media-heading a, .bizz-name a, h3 a')
                    phone_elem = listing.select_one('.phone, .tel, .phone-number')
                    addr_elem = listing.select_one('.address, .street-address')
                    website_elem = listing.select_one('a.website-link, a[href*="website"]')
                    
                    if not name_elem:
                        continue
                    
                    name = name_elem.get_text(strip=True)
                    phone = phone_elem.get_text(strip=True) if phone_elem else ''
                    address = addr_elem.get_text(strip=True) if addr_elem else ''
                    website = website_elem.get('href', '') if website_elem else ''
                    
                    business = {
                        'name': name,
                        'phone': self.clean_phone(phone),
                        'address': address,
                        'website': self.clean_url(website),
                        'category_type': self.get_category_type(query),
                        'search_query': query,
                        'city': city,
                        'state': state,
                        'source': 'Yellowbot',
                        'date_found': datetime.now().strftime('%Y-%m-%d'),
                    }
                    businesses.append(business)
                    self.stats['scraped'] += 1
                except Exception as e:
                    self.stats['errors'] += 1
                    continue
            
            time.sleep(random.uniform(2, 4))
        
        return businesses
    
    def scrape_hotfrog(self, query, city, state, max_pages=3):
        """Scrape HotFrog listings"""
        businesses = []
        search_term = quote_plus(query)
        location = quote_plus(f"{city}, {state}")
        
        for page in range(1, max_pages + 1):
            if page == 1:
                url = f"https://www.hotfrog.com/search/{search_term}/{location}"
            else:
                url = f"https://www.hotfrog.com/search/{search_term}/{location}/page-{page}"
            
            print(f"    HotFrog page {page}")
            html = self.get(url)
            
            if not html:
                continue
            
            soup = BeautifulSoup(html, 'html.parser')
            
            for listing in soup.select('.directory-card, .listing-item, .srCompany'):
                try:
                    name_elem = listing.select_one('.company-name a, h3 a, a.company-name')
                    phone_elem = listing.select_one('.phone, .tel, [data-phone]')
                    addr_elem = listing.select_one('.address, .street, .location')
                    website_elem = listing.select_one('a[rel="nofollow"][href*="go.to"], a.website')
                    
                    if not name_elem:
                        continue
                    
                    name = name_elem.get_text(strip=True)
                    phone = phone_elem.get_text(strip=True) if phone_elem else ''
                    address = addr_elem.get_text(strip=True) if addr_elem else ''
                    website = website_elem.get('href', '') if website_elem else ''
                    
                    business = {
                        'name': name,
                        'phone': self.clean_phone(phone),
                        'address': address,
                        'website': self.clean_url(website),
                        'category_type': self.get_category_type(query),
                        'search_query': query,
                        'city': city,
                        'state': state,
                        'source': 'HotFrog',
                        'date_found': datetime.now().strftime('%Y-%m-%d'),
                    }
                    businesses.append(business)
                    self.stats['scraped'] += 1
                except Exception as e:
                    self.stats['errors'] += 1
                    continue
            
            time.sleep(random.uniform(2, 4))
        
        return businesses
    
    def scrape_showmelocal(self, query, city, state, max_pages=3):
        """Scrape ShowMeLocal listings"""
        businesses = []
        search_term = quote_plus(query)
        location = quote_plus(f"{city}, {state}")
        
        for page in range(1, max_pages + 1):
            url = f"https://www.showmelocal.com/search/?q={search_term}&where={location}&page={page}"
            print(f"    ShowMeLocal page {page}")
            html = self.get(url)
            
            if not html:
                continue
            
            soup = BeautifulSoup(html, 'html.parser')
            
            for listing in soup.select('.listing, .business-listing, .result-item'):
                try:
                    name_elem = listing.select_one('.business-name a, h3 a, .name a')
                    phone_elem = listing.select_one('.phone, .tel')
                    addr_elem = listing.select_one('.address, .location')
                    website_elem = listing.select_one('a[href*="website"], a.website-link')
                    
                    if not name_elem:
                        continue
                    
                    name = name_elem.get_text(strip=True)
                    phone = phone_elem.get_text(strip=True) if phone_elem else ''
                    address = addr_elem.get_text(strip=True) if addr_elem else ''
                    website = website_elem.get('href', '') if website_elem else ''
                    
                    business = {
                        'name': name,
                        'phone': self.clean_phone(phone),
                        'address': address,
                        'website': self.clean_url(website),
                        'category_type': self.get_category_type(query),
                        'search_query': query,
                        'city': city,
                        'state': state,
                        'source': 'ShowMeLocal',
                        'date_found': datetime.now().strftime('%Y-%m-%d'),
                    }
                    businesses.append(business)
                    self.stats['scraped'] += 1
                except Exception as e:
                    self.stats['errors'] += 1
                    continue
            
            time.sleep(random.uniform(2, 4))
        
        return businesses
    
    def scrape_ezlocal(self, query, city, state, max_pages=3):
        """Scrape EZLocal listings"""
        businesses = []
        search_term = quote_plus(query)
        
        for page in range(1, max_pages + 1):
            url = f"https://www.ezlocal.com/search/?q={search_term}&location={city}%2C+{state}&page={page}"
            print(f"    EZLocal page {page}")
            html = self.get(url)
            
            if not html:
                continue
            
            soup = BeautifulSoup(html, 'html.parser')
            
            for listing in soup.select('.listing-card, .business-card, .search-result'):
                try:
                    name_elem = listing.select_one('.listing-name a, h2 a, .name a')
                    phone_elem = listing.select_one('.phone, .telephone')
                    addr_elem = listing.select_one('.address, .street')
                    website_elem = listing.select_one('a[rel="nofollow"], a.website')
                    
                    if not name_elem:
                        continue
                    
                    name = name_elem.get_text(strip=True)
                    phone = phone_elem.get_text(strip=True) if phone_elem else ''
                    address = addr_elem.get_text(strip=True) if addr_elem else ''
                    website = website_elem.get('href', '') if website_elem else ''
                    
                    business = {
                        'name': name,
                        'phone': self.clean_phone(phone),
                        'address': address,
                        'website': self.clean_url(website),
                        'category_type': self.get_category_type(query),
                        'search_query': query,
                        'city': city,
                        'state': state,
                        'source': 'EZLocal',
                        'date_found': datetime.now().strftime('%Y-%m-%d'),
                    }
                    businesses.append(business)
                    self.stats['scraped'] += 1
                except Exception as e:
                    self.stats['errors'] += 1
                    continue
            
            time.sleep(random.uniform(2, 4))
        
        return businesses
    
    def clean_phone(self, phone):
        """Clean phone number"""
        if not phone:
            return ''
        # Extract just digits
        digits = ''.join(c for c in phone if c.isdigit())
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        return phone.strip()
    
    def clean_url(self, url):
        """Clean website URL"""
        if not url:
            return ''
        if url.startswith('//'):
            return 'https:' + url
        if url.startswith('/'):
            return ''
        return url
    
    def get_category_type(self, query):
        """Map query to category type"""
        for cat, queries in CATEGORIES.items():
            for q in queries:
                if q in query.lower():
                    return cat
        return 'other'
    
    def deduplicate(self, businesses):
        """Remove duplicates by phone number"""
        seen = set()
        unique = []
        for b in businesses:
            key = b.get('phone', '') or b.get('name', '')
            if key and key not in seen:
                seen.add(key)
                unique.append(b)
        return unique
    
    def save_csv(self, businesses, filename):
        """Save to CSV"""
        if not businesses:
            print("[!] No businesses to save")
            return None
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        unique = self.deduplicate(businesses)
        
        fieldnames = ['name', 'phone', 'address', 'website', 'category_type',
                      'search_query', 'city', 'state', 'source', 'date_found']
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(unique)
        
        print(f"\n[+] Saved {len(unique)} unique businesses to {filepath}")
        return filepath
    
    def run(self, cities=None, max_pages=2, sources=None):
        """Run the scraper"""
        if cities is None:
            cities = CITIES[:1]  # Default: Sacramento only for testing
        
        if sources is None:
            sources = ['yellowbot']  # Start with one source
        
        print("="*60)
        print("PSDEPOT LEAD GENERATION - Multi-Source Scraper")
        print("="*60)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Cities: {[c['city'] for c in cities]}")
        print(f"Sources: {sources}")
        print(f"Categories: {list(CATEGORIES.keys())}")
        print("="*60)
        
        all_businesses = []
        scrapers = {
            'yellowbot': self.scrape_yellowbot,
            'hotfrog': self.scrape_hotfrog,
            'showmelocal': self.scrape_showmelocal,
            'ezlocal': self.scrape_ezlocal,
        }
        
        for city_data in cities:
            city = city_data['city']
            state = city_data['state']
            
            print(f"\n{'='*60}")
            print(f"Scraping {city}, {state}")
            print(f"{'='*60}")
            
            for source in sources:
                if source not in scrapers:
                    continue
                
                print(f"\n[{source.upper()}]")
                scraper_func = scrapers[source]
                
                for cat_type, queries in CATEGORIES.items():
                    for query in queries:
                        print(f"\n  Query: {query}")
                        businesses = scraper_func(query, city, state, max_pages)
                        for b in businesses:
                            b['category_type'] = cat_type
                        all_businesses.extend(businesses)
                        print(f"    Found: {len(businesses)}")
                        time.sleep(random.uniform(1, 3))
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.save_csv(all_businesses, f'psdepot_leads_{timestamp}.csv')
        self.save_csv(all_businesses, 'psdepot_leads_latest.csv')
        
        print(f"\n{'='*60}")
        print(f"COMPLETE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total scraped: {self.stats['scraped']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"Unique businesses: {len(self.deduplicate(all_businesses))}")
        print(f"{'='*60}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='PSDEPOT Lead Scraper')
    parser.add_argument('--cities', nargs='+', default=['Sacramento'],
                        help='Cities to scrape (default: Sacramento)')
    parser.add_argument('--pages', type=int, default=2,
                        help='Max pages per query (default: 2)')
    parser.add_argument('--sources', nargs='+', default=['yellowbot'],
                        help='Sources to use (default: yellowbot)')
    args = parser.parse_args()
    
    # Filter cities
    city_list = [c for c in CITIES if c['city'] in args.cities]
    if not city_list:
        city_list = CITIES[:1]  # Default to Sacramento
    
    scraper = LeadScraper()
    scraper.run(cities=city_list, max_pages=args.pages, sources=args.sources)


if __name__ == '__main__':
    main()
