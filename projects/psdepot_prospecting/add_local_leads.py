#!/usr/bin/env python3
"""
Add locally found owner-operated restaurants to PSDEPOT leads
"""

import csv
import os
from datetime import datetime

DATA_DIR = '/data/data/com.termux/files/home/mortimer/projects/psdepot_prospecting/data'

# Owner-operated restaurants found from searches
NEW_LEADS = [
    # Mexican Taquerias - Family Owned
    {"name": "Fuego Taqueria y Restaurante", "address": "4631 North Fresno St", "city": "Fresno", "state": "CA", "zip": "93725", "phone": "", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "El Rinconcito Taco Shop", "address": "1655 Brandywine Ave", "city": "Chula Vista", "state": "CA", "zip": "91911", "phone": "", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "Taco Fino", "address": "2317 Central Ave", "city": "Alameda", "state": "CA", "zip": "94501", "phone": "", "category_type": "mexican", "categories": "Mexican Restaurant"},
    {"name": "Taco Fino Express", "address": "1401 Park St", "city": "Alameda", "state": "CA", "zip": "94501", "phone": "", "category_type": "mexican", "categories": "Mexican Restaurant"},
    {"name": "West Coast Taco Bar", "address": "8850 Williamson Dr #1053", "city": "Elk Grove", "state": "CA", "zip": "95759", "phone": "(916) 585-3669", "category_type": "mexican", "categories": "Mexican Gourmet Tacos"},
    {"name": "Los Taquero Mucho", "address": "120 S Garfield Ave", "city": "Montebello", "state": "CA", "zip": "90640", "phone": "", "category_type": "mexican", "categories": "Mexican Guatemalan Taqueria"},
    {"name": "Taqueria Juanito's / Carmelitas Peruvian", "address": "16851 Victory Blvd #2", "city": "Van Nuys", "state": "CA", "zip": "91406", "phone": "", "category_type": "mexican", "categories": "Mexican Peruvian"},
    {"name": "Taqueria Sol Azteca", "address": "6750 Commerce Blvd", "city": "Rohnert Park", "state": "CA", "zip": "94928", "phone": "", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "La Elegante Taqueria", "address": "1423 Kern St", "city": "Fresno", "state": "CA", "zip": "93706", "phone": "", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "Taqueria Las Comadres", "address": "2081 Mountain Boulevard", "city": "Oakland", "state": "CA", "zip": "94611", "phone": "(510) 339-9002", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "El Nido", "address": "1755 Mt. Diablo Blvd", "city": "Danville", "state": "CA", "zip": "94526", "phone": "", "category_type": "mexican", "categories": "Mexican Restaurant"},
    {"name": "Cabreras Mexican Restaurant", "address": "1431 N San Gabriel Pl", "city": "Arcadia", "state": "CA", "zip": "91006", "phone": "", "category_type": "mexican", "categories": "Mexican Restaurant"},
    {"name": "El Zarape Restaurant", "address": "4197 Ball Road", "city": "Cypress", "state": "CA", "zip": "90630", "phone": "(714) 952-0562", "category_type": "mexican", "categories": "Mexican Restaurant"},
    {"name": "La Taqueria", "address": "2889 Mission St", "city": "San Francisco", "state": "CA", "zip": "94110", "phone": "", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "Taqueria El Castillito", "address": "3033 24th St", "city": "San Francisco", "state": "CA", "zip": "94110", "phone": "", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "Taqueria Los Cuñados", "address": "417 N Main St", "city": "Milpitas", "state": "CA", "zip": "95035", "phone": "", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "El Tapatio", "address": "980 Ninth St", "city": "Imperial Beach", "state": "CA", "zip": "91932", "phone": "", "category_type": "mexican", "categories": "Mexican Restaurant"},
    {"name": "El Ranchito Taco Shop", "address": "32251 Mission Trail", "city": "Lake Elsinore", "state": "CA", "zip": "92530", "phone": "", "category_type": "mexican", "categories": "Mexican Taco Shop"},
    {"name": "Tito's Tacos", "address": "8988 Venice Blvd", "city": "Culver City", "state": "CA", "zip": "90232", "phone": "", "category_type": "mexican", "categories": "Mexican Tacos"},
    
    # Pizza - Owner Operated
    {"name": "Tom's Farms Pizza", "address": "23900 Temescal Canyon Rd", "city": "Corona", "state": "CA", "zip": "92883", "phone": "(951) 277-9463", "category_type": "pizza", "categories": "Pizza Restaurant"},
    {"name": "Tom's Sourdough Pizza Villa", "address": "101 12th St", "city": "Fortuna", "state": "CA", "zip": "95540", "phone": "(707) 725-1123", "category_type": "pizza", "categories": "Pizza Restaurant"},
    {"name": "Marino's Pizza and Ravioli", "address": "1050 N State St", "city": "Ukiah", "state": "CA", "zip": "95482", "phone": "", "category_type": "pizza", "categories": "Pizza Italian"},
    {"name": "Matteo's Pizza", "address": "5132 Arden Way", "city": "Carmichael", "state": "CA", "zip": "95608", "phone": "", "category_type": "pizza", "categories": "Pizza Italian"},
    {"name": "Tommy's Pizza (Imbibe)", "address": "4140 Truxtun Ave", "city": "Bakersfield", "state": "CA", "zip": "93309", "phone": "", "category_type": "pizza", "categories": "Pizza"},
    {"name": "Popolo's Pizza", "address": "7835 North Palm Avenue", "city": "Fresno", "state": "CA", "zip": "93711", "phone": "(559) 435-6775", "category_type": "pizza", "categories": "Pizza Restaurant"},
    {"name": "Jerry's Pizza & Pub", "address": "1707 Chester Ave", "city": "Bakersfield", "state": "CA", "zip": "93301", "phone": "", "category_type": "pizza", "categories": "Pizza Pub"},
    
    # Burgers - Local
    {"name": "Tom's Burger", "address": "115 E College Ave", "city": "Lompoc", "state": "CA", "zip": "93436", "phone": "", "category_type": "bar", "categories": "Burger Joint"},
    {"name": "TOM's Famous Family Restaurant", "address": "14084 Amargosa Rd #180", "city": "Victorville", "state": "CA", "zip": "92392", "phone": "(760) 241-7770", "category_type": "bar", "categories": "Family Restaurant"},
    {"name": "Tom's Drive-In", "address": "1805 W Avenue J", "city": "Lancaster", "state": "CA", "zip": "93534", "phone": "(661) 729-5777", "category_type": "bar", "categories": "Drive-In Restaurant"},
]


def add_leads(leads, filename):
    """Add leads to CSV"""
    filepath = os.path.join(DATA_DIR, filename)
    
    # Read existing
    existing = []
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing = list(reader)
    
    # Track by address
    existing_addrs = {r.get('address', '').lower() for r in existing}
    
    # Add new
    new_count = 0
    for loc in leads:
        addr_lower = loc.get('address', '').lower()
        if addr_lower not in existing_addrs:
            row = {
                'name': loc.get('name', ''),
                'phone': loc.get('phone', ''),
                'address': loc.get('address', ''),
                'city': loc.get('city', ''),
                'state': loc.get('state', 'CA'),
                'zip': loc.get('zip', ''),
                'website': '',
                'category_type': loc.get('category_type', 'other'),
                'categories': loc.get('categories', ''),
                'rating': '',
                'review_count': '',
                'source': 'WebSearch',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
            }
            existing.append(row)
            new_count += 1
    
    # Write back
    if new_count > 0:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['name', 'phone', 'address', 'city', 'state', 'zip', 'website',
                         'category_type', 'categories', 'rating', 'review_count', 'source', 'date_found']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(existing)
        print(f"[+] Added {new_count} leads to {filename}")
    else:
        print(f"[=] No new leads to add")
    
    return new_count


def main():
    print("="*60)
    print("Adding Owner-Operated Restaurants to PSDEPOT Leads")
    print("="*60)
    
    # Add to main leads
    total = add_leads(NEW_LEADS, 'psdepot_leads_latest.csv')
    
    # Add to category-specific files
    by_cat = {}
    for lead in NEW_LEADS:
        cat = lead.get('category_type', 'other')
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append(lead)
    
    for cat, cat_leads in by_cat.items():
        add_leads(cat_leads, f'{cat}.csv')
    
    print("\n" + "="*60)
    print(f"Total new leads added: {total}")
    print("="*60)
    
    # Count total
    filepath = os.path.join(DATA_DIR, 'psdepot_leads_latest.csv')
    with open(filepath, 'r', encoding='utf-8') as f:
        count = sum(1 for _ in f) - 1  # subtract header
    print(f"New total: {count} leads")


if __name__ == '__main__':
    main()
