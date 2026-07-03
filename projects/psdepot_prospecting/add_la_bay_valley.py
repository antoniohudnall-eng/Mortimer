#!/usr/bin/env python3
"""
Add LA-area owner-operated restaurants to PSDEPOT leads
"""

import csv
import os
from datetime import datetime

DATA_DIR = '/data/data/com.termux/files/home/mortimer/projects/psdepot_prospecting/data'

# LA-area owner-operated restaurants found
LA_LEADS = [
    # Mexican Taquerias - LA Area
    {"name": "Taqueria Frontera", "address": "2100 N San Fernando Rd", "city": "Los Angeles", "state": "CA", "zip": "90039", "phone": "", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "La Que Si Llena", "address": "3630 E Cesar E Chavez Ave", "city": "Los Angeles", "state": "CA", "zip": "90063", "phone": "", "category_type": "mexican", "categories": "Mexican Restaurant"},
    {"name": "Tijuanazo", "address": "355 S Atlantic Boulevard", "city": "Los Angeles", "state": "CA", "zip": "90022", "phone": "(323) 604-9363", "category_type": "mexican", "categories": "Tijuana Style Tacos"},
    {"name": "Taqueria Jalisco", "address": "4755 W Washington Blvd", "city": "Los Angeles", "state": "CA", "zip": "90016", "phone": "", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "Tacos 1986", "address": "721 S Spring St", "city": "Los Angeles", "state": "CA", "zip": "90014", "phone": "", "category_type": "mexican", "categories": "Tijuana Style Tacos"},
    {"name": "Cuernavaca's Grill", "address": "417 S San Julian St", "city": "Los Angeles", "state": "CA", "zip": "90013", "phone": "", "category_type": "mexican", "categories": "Mexican Restaurant"},
    {"name": "Villa's Tacos", "address": "5900 N Figueroa St", "city": "Los Angeles", "state": "CA", "zip": "90042", "phone": "", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "Taqueria Juanito's", "address": "16851 Victory Blvd #2", "city": "Van Nuys", "state": "CA", "zip": "91406", "phone": "", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "El Nido", "address": "1755 Mt. Diablo Blvd", "city": "Danville", "state": "CA", "zip": "94526", "phone": "", "category_type": "mexican", "categories": "Mexican Restaurant"},
    {"name": "Taco Fino", "address": "2317 Central Ave", "city": "Alameda", "state": "CA", "zip": "94501", "phone": "", "category_type": "mexican", "categories": "Mexican Restaurant"},
    
    # Central Valley Mexican
    {"name": "La Elegante Taqueria", "address": "1423 Kern St", "city": "Fresno", "state": "CA", "zip": "93706", "phone": "", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "La Elegante Taqueria Truck", "address": "2373 E Muscat Ave", "city": "Fresno", "state": "CA", "zip": "93706", "phone": "", "category_type": "mexican", "categories": "Taco Truck"},
    {"name": "Fuego Taqueria", "address": "4631 N Fresno St", "city": "Fresno", "state": "CA", "zip": "93725", "phone": "", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "Taqueria Sol Azteca", "address": "6750 Commerce Blvd", "city": "Rohnert Park", "state": "CA", "zip": "94928", "phone": "", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "El Tapatio", "address": "980 9th St", "city": "Imperial Beach", "state": "CA", "zip": "91932", "phone": "", "category_type": "mexican", "categories": "Mexican Restaurant"},
    
    # Bay Area Mexican
    {"name": "Taqueria Los Cuñados", "address": "417 N Main St", "city": "Milpitas", "state": "CA", "zip": "95035", "phone": "", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "Taqueria El Castillito", "address": "3033 24th St", "city": "San Francisco", "state": "CA", "zip": "94110", "phone": "", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "La Taqueria", "address": "2889 Mission St", "city": "San Francisco", "state": "CA", "zip": "94110", "phone": "", "category_type": "mexican", "categories": "Mexican Taqueria"},
    {"name": "Taqueria Las Comadres", "address": "2081 Mountain Blvd", "city": "Oakland", "state": "CA", "zip": "94611", "phone": "(510) 339-9002", "category_type": "mexican", "categories": "Mexican Taqueria"},
    
    # Vietnamese / Asian - Central Valley
    {"name": "Pho 99", "address": "1035 E Waterloo", "city": "Stockton", "state": "CA", "zip": "95205", "phone": "", "category_type": "vietnamese", "categories": "Pho Vietnamese"},
    {"name": "Lee's Sandwiches", "address": "1211 Van Buren Blvd", "city": "Riverside", "state": "CA", "zip": "92506", "phone": "", "category_type": "vietnamese", "categories": "Vietnamese Bakery"},
    {"name": "Dat Thanh Vietnamese", "address": "1356 E Harding Way", "city": "Stockton", "state": "CA", "zip": "95205", "phone": "", "category_type": "vietnamese", "categories": "Vietnamese Restaurant"},
    {"name": "Bangkok Thai", "address": "1211 Fulton Ave", "city": "Fresno", "state": "CA", "zip": "93728", "phone": "", "category_type": "thai", "categories": "Thai Restaurant"},
    {"name": "Thai House", "address": "6011 N Fresno St", "city": "Fresno", "state": "CA", "zip": "93710", "phone": "", "category_type": "thai", "categories": "Thai Restaurant"},
    
    # Central Valley Pizza / Italian
    {"name": "Matteo's Pizza", "address": "5132 Arden Way", "city": "Carmichael", "state": "CA", "zip": "95608", "phone": "", "category_type": "pizza", "categories": "Pizza Italian"},
    {"name": "Popolo's Pizza", "address": "7835 N Palm Ave", "city": "Fresno", "state": "CA", "zip": "93711", "phone": "(559) 435-6775", "category_type": "pizza", "categories": "Pizza Restaurant"},
    {"name": "Marino's Pizza", "address": "1050 N State St", "city": "Ukiah", "state": "CA", "zip": "95482", "phone": "", "category_type": "pizza", "categories": "Pizza Italian"},
    {"name": "Joe's Italian Kitchen", "address": "1200 J St", "city": "San Luis Obispo", "state": "CA", "zip": "93401", "phone": "", "category_type": "pizza", "categories": "Italian Restaurant"},
    
    # Central Valley Burgers / Diners
    {"name": "Mel's Diner", "address": "1111 W March Ln", "city": "Stockton", "state": "CA", "zip": "95207", "phone": "", "category_type": "bar", "categories": "Diner"},
    {"name": "Dusty's Cafe", "address": "340 Wket", "city": "Fresno", "state": "CA", "zip": "93706", "phone": "", "category_type": "bar", "categories": "Cafe Diner"},
    {"name": "Rick's Cafe", "address": "580 W Main St", "city": "Visalia", "state": "CA", "zip": "93291", "phone": "", "category_type": "bar", "categories": "Restaurant Cafe"},
    
    # Asian - Bay Area
    {"name": "Mama's Thai Kitchen", "address": "1830 Solano Ave", "city": "Berkeley", "state": "CA", "zip": "94707", "phone": "", "category_type": "thai", "categories": "Thai Restaurant"},
    {"name": "Krua Thai", "address": "6412 Jarvis Ave", "city": "Newark", "state": "CA", "zip": "94560", "phone": "", "category_type": "thai", "categories": "Thai Restaurant"},
    {"name": "Pho Ky", "address": "4045 Valley Ave", "city": "Union City", "state": "CA", "zip": "94587", "phone": "", "category_type": "vietnamese", "categories": "Pho Vietnamese"},
    {"name": "Lucky Thai", "address": "1553 Newmark Ave", "city": "San Pablo", "state": "CA", "zip": "94806", "phone": "", "category_type": "thai", "categories": "Thai Restaurant"},
    
    # Indian - Bay Area
    {"name": "Amber Dhaba", "address": "5174 Mowry Ave", "city": "Fremont", "state": "CA", "zip": "94538", "phone": "", "category_type": "indian", "categories": "Indian Restaurant"},
    {"name": "Curry Point", "address": "1901 Union Ave", "city": "San Jose", "state": "CA", "zip": "95116", "phone": "", "category_type": "indian", "categories": "Indian Restaurant"},
    {"name": "Bawarchi", "address": "2088 S Winchester Blvd", "city": "San Jose", "state": "CA", "zip": "95128", "phone": "", "category_type": "indian", "categories": "Indian Restaurant"},
    {"name": "Tiffin's Kitchen", "address": "1210 S O'Casey Ln", "city": "Foster City", "state": "CA", "zip": "94404", "phone": "", "category_type": "indian", "categories": "Indian Restaurant"},
    
    # Chinese - Central Valley
    {"name": "Ming's Chinese", "address": "1010 W March Ln", "city": "Stockton", "state": "CA", "zip": "95207", "phone": "", "category_type": "chinese", "categories": "Chinese Restaurant"},
    {"name": "Golden Dragon", "address": "2601 E California Ave", "city": "Fresno", "zip": "93706", "phone": "", "category_type": "chinese", "categories": "Chinese Restaurant"},
    {"name": "New Asia", "address": "1724 McHenry Ave", "city": "Modesto", "state": "CA", "zip": "95350", "phone": "", "category_type": "chinese", "categories": "Chinese Restaurant"},
    
    # Japanese - Central Valley
    {"name": "Sakura Japanese", "address": "2850 E Floral Ave", "city": "Selma", "state": "CA", "zip": "93662", "phone": "", "category_type": "japanese", "categories": "Japanese Restaurant"},
    {"name": "Ken Japanese", "address": "1625 W Main St", "city": "Merced", "state": "CA", "zip": "95340", "phone": "", "category_type": "japanese", "categories": "Japanese Restaurant"},
    {"name": "Tokyo Teriyaki", "address": "1619 Hammel St", "city": "Fresno", "state": "CA", "zip": "93706", "phone": "", "category_type": "japanese", "categories": "Japanese Teriyaki"},
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
    print("Adding LA/Bay Area/Central Valley Leads to PSDEPOT")
    print("="*60)
    
    # Add to main leads
    total = add_leads(LA_LEADS, 'psdepot_leads_latest.csv')
    
    # Add to statewide private
    add_leads(LA_LEADS, 'statewide/private_leads.csv')
    
    # Add to category-specific files
    by_cat = {}
    for lead in LA_LEADS:
        cat = lead.get('category_type', 'other')
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append(lead)
    
    for cat, cat_leads in by_cat.items():
        add_leads(cat_leads, f'{cat}.csv')
    
    print("\n" + "="*60)
    print(f"Total new leads added: {total}")
    
    # Count total
    filepath = os.path.join(DATA_DIR, 'psdepot_leads_latest.csv')
    with open(filepath, 'r', encoding='utf-8') as f:
        count = sum(1 for _ in f) - 1
    print(f"New total: {count} leads")
    print("="*60)


if __name__ == '__main__':
    main()
