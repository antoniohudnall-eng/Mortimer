#!/usr/bin/env python3
"""
PSDEPOT Lead Generation - YellowPages Scraper
Builds business database from public YellowPages listings
"""

import csv
import json
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from datetime import datetime

# Configuration
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

CITIES = [
    {'city': 'Sacramento', 'state': 'CA', 'zip': '95814'},
    {'city': 'Elk Grove', 'state': 'CA', 'zip': '95624'},
    {'city': 'Santa Rosa', 'state': 'CA', 'zip': '95401'},
    {'city': 'Napa', 'state': 'CA', 'zip': '94558'},
    {'city': 'Sonoma', 'state': 'CA', 'zip': '95476'},
    {'city': 'Calistoga', 'state': 'CA', 'zip': '94515'},
    {'city': 'American Canyon', 'state': 'CA', 'zip': '94503'},
]

# PSDEPOT customer categories
CATEGORIES = {
    'mexican': ['taqueria', 'mexican restaurant', 'carniceria', 'panaderia', 'bodega', 'tortilleria'],
    'thai': ['thai restaurant'],
    'korean': ['korean restaurant', 'korean bbq'],
    'vietnamese': ['vietnamese restaurant', 'pho restaurant'],
    'chinese': ['chinese restaurant', 'dim sum'],
    'japanese': ['japanese restaurant', 'sushi'],
    'indian': ['indian restaurant'],
    'filipino': ['filipino restaurant'],
    'pizza': ['pizza', 'italian restaurant'],
    'cafe': ['cafe', 'coffee shop', 'bubble tea'],
    'bakery': ['bakery', 'donut'],
    'bar': ['bar', 'sports bar', 'lounge'],
    'food_truck': ['food truck'],
    'mediterranean': ['mediterranean', 'greek', 'middle eastern'],
    'caribbean': ['caribbean', 'jamaican'],
    'retail': ['convenience store', 'liquor store', 'dispensary', 'vape shop'],
}

OUTPUT_DIR = '/data/data/com.termux/files/home/mortimer/projects/psdepot_prospecting/data'


def get_page(url, retries=3):
    """Fetch a page with retries"""
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code == 200:
                return response.text
            print(f"  [!] Status {response.status_code} for {url}")
        except Exception as e:
            print(f"  [!] Error: {e}")
            time.sleep(random.uniform(2, 5))
    return None


def parse_listing(soup):
    """Extract business info from a YellowPages listing"""
    businesses = []
    
    for listing in soup.select('.info'):
        try:
            name_elem = listing.select_one('.business-name')
            phone_elem = listing.select_one('.phones')
            address_elem = listing.select_one('.street-address')
            locality_elem = listing.select_one('.locality')
            website_elem = listing.select_one('a.website-link')
            categories = listing.select('.categories a')
            
            if not name_elem:
                continue
            
            name = name_elem.get_text(strip=True)
            phone = phone_elem.get_text(strip=True) if phone_elem else ''
            
            address_parts = []
            if address_elem:
                address_parts.append(address_elem.get_text(strip=True))
            if locality_elem:
                locality = locality_elem.get_text(strip=True)
                address_parts.append(locality)
            address = ', '.join(address_parts)
            
            website = website_elem.get('href', '').replace('//', '') if website_elem else ''
            
            category_list = [c.get_text(strip=True) for c in categories[:3]]
            
            business = {
                'name': name,
                'phone': phone,
                'address': address,
                'website': website,
                'categories': '|'.join(category_list),
                'source': 'YellowPages',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
            }
            businesses.append(business)
        except Exception as e:
            print(f"  [!] Parse error: {e}")
            continue
    
    return businesses


def scrape_category(city, state, zipcode, category, max_pages=5):
    """Scrape a specific category in a city"""
    businesses = []
    search_term = quote_plus(category)
    location = quote_plus(f"{city}, {state}")
    
    for page in range(1, max_pages + 1):
        if page == 1:
            url = f"https://www.yellowpages.com/search?search_term={search_term}&geo_location_terms={location}"
        else:
            url = f"https://www.yellowpages.com/search?search_term={search_term}&geo_location_terms={location}&page={page}"
        
        print(f"  Scraping page {page}: {category}")
        html = get_page(url)
        
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            results = parse_listing(soup)
            if not results:
                break
            businesses.extend(results)
            print(f"    Found {len(results)} listings")
        
        time.sleep(random.uniform(1, 3))
    
    return businesses


def scrape_city(city_data, categories_dict, max_pages=3):
    """Scrape all categories for a city"""
    all_businesses = []
    city = city_data['city']
    state = city_data['state']
    zipcode = city_data['zip']
    
    print(f"\n{'='*60}")
    print(f"Scraping {city}, {state} ({zipcode})")
    print(f"{'='*60}")
    
    for category_type, queries in categories_dict.items():
        for query in queries:
            print(f"\n[Category: {category_type}] {query}")
            businesses = scrape_category(city, state, zipcode, query, max_pages)
            for b in businesses:
                b['category_type'] = category_type
                b['search_query'] = query
            all_businesses.extend(businesses)
            time.sleep(random.uniform(2, 4))
    
    return all_businesses


def save_csv(businesses, filename):
    """Save businesses to CSV"""
    if not businesses:
        print("[!] No businesses to save")
        return
    
    filepath = f"{OUTPUT_DIR}/{filename}"
    
    # Deduplicate by phone number
    seen = set()
    unique = []
    for b in businesses:
        key = b.get('phone', b.get('name', ''))
        if key and key not in seen:
            seen.add(key)
            unique.append(b)
    
    fieldnames = ['name', 'phone', 'address', 'website', 'category_type', 'categories', 
                  'search_query', 'source', 'date_found']
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique)
    
    print(f"\n[+] Saved {len(unique)} unique businesses to {filepath}")
    return filepath


def main():
    print("="*60)
    print("PSDEPOT LEAD GENERATION - YellowPages Scraper")
    print("="*60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Categories: {len(CATEGORIES)} types")
    print(f"Cities: {len(CITIES)} areas")
    
    all_businesses = []
    
    for city_data in CITIES:
        businesses = scrape_city(city_data, CATEGORIES, max_pages=3)
        all_businesses.extend(businesses)
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    save_csv(all_businesses, f'psdepot_leads_{timestamp}.csv')
    
    # Also save latest as "latest.csv"
    save_csv(all_businesses, 'psdepot_leads_latest.csv')
    
    print(f"\n{'='*60}")
    print(f"COMPLETE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total businesses collected: {len(all_businesses)}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
