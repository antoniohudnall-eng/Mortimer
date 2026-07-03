#!/usr/bin/env python3
"""
Add Mountain Mike's and Teriyaki Madness to PSDEPOT leads
"""

import csv
import os
from datetime import datetime

DATA_DIR = '/data/data/com.termux/files/home/mortimer/projects/psdepot_prospecting/data'

# Mountain Mike's - Northern California locations
MOUNTAIN_MIKES = [
    # Sacramento Area
    {'name': "Mountain Mike's Pizza", 'address': '5640 Auburn Blvd', 'city': 'Sacramento', 'state': 'CA', 'zip': '95841', 'phone': '(916) 331-1150'},
    {'name': "Mountain Mike's Pizza", 'address': '2069 Arena Blvd', 'city': 'Natomas', 'state': 'CA', 'zip': '95834', 'phone': '(916) 419-4434'},
    {'name': "Mountain Mike's Pizza", 'address': '2610 Gateway Oaks Dr', 'city': 'Sacramento', 'state': 'CA', 'zip': '95833', 'phone': '(916) 649-8000'},
    {'name': "Mountain Mike's Pizza", 'address': '4623 Mack Rd', 'city': 'Sacramento', 'state': 'CA', 'zip': '95823', 'phone': '(916) 392-6445'},
    {'name': "Mountain Mike's Pizza", 'address': '1319 Fulton Ave', 'city': 'Sacramento', 'state': 'CA', 'zip': '95825', 'phone': '(916) 485-8314'},
    {'name': "Mountain Mike's Pizza", 'address': '7808 Gerber Rd', 'city': 'Sacramento', 'state': 'CA', 'zip': '95828', 'phone': '(916) 688-3737'},
    {'name': "Mountain Mike's Pizza", 'address': '3609 Bradshaw Rd', 'city': 'Sacramento', 'state': 'CA', 'zip': '95827', 'phone': '(916) 366-3609'},
    {'name': "Mountain Mike's Pizza", 'address': '8211 Bruceville Rd', 'city': 'Sacramento', 'state': 'CA', 'zip': '95823', 'phone': '(916) 896-5651'},
    {'name': "Mountain Mike's Pizza", 'address': '4720 Freeport Blvd', 'city': 'Sacramento', 'state': 'CA', 'zip': '95822', 'phone': '(279) 222-4310'},
    {'name': "Mountain Mike's Pizza", 'address': '7465 Rush River Dr', 'city': 'Sacramento', 'state': 'CA', 'zip': '95831', 'phone': '(916) 970-5360'},
    {'name': "Mountain Mike's Pizza", 'address': '7660 La Riviera Dr', 'city': 'Sacramento', 'state': 'CA', 'zip': '95826', 'phone': '(916) 383-8300'},
    {'name': "Mountain Mike's Pizza", 'address': '1900 S St', 'city': 'Sacramento', 'state': 'CA', 'zip': '95811', 'phone': '(916) 399-4580'},
    
    # Elk Grove
    {'name': "Mountain Mike's Pizza", 'address': '8690 Elk Grove Blvd', 'city': 'Elk Grove', 'state': 'CA', 'zip': '95624', 'phone': '(916) 685-5107'},
    {'name': "Mountain Mike's Pizza", 'address': '8441 Elk Grove-Florin Rd', 'city': 'Elk Grove', 'state': 'CA', 'zip': '95624', 'phone': '(916) 681-6878'},
    {'name': "Mountain Mike's Pizza", 'address': '7440 Laguna Blvd', 'city': 'Elk Grove', 'state': 'CA', 'zip': '95758', 'phone': '(916) 684-7888'},
    {'name': "Mountain Mike's Pizza", 'address': '9320 Elk Grove Blvd', 'city': 'Elk Grove', 'state': 'CA', 'zip': '95624', 'phone': '(916) 896-0880'},
    {'name': "Mountain Mike's Pizza", 'address': '5010 Elk Grove Blvd', 'city': 'Elk Grove', 'state': 'CA', 'zip': '95758', 'phone': '(916) 684-0808'},
    
    # Roseville / Rocklin
    {'name': "Mountain Mike's Pizza", 'address': '3989 Foothills Blvd', 'city': 'Roseville', 'state': 'CA', 'zip': '95747', 'phone': '(916) 782-7575'},
    {'name': "Mountain Mike's Pizza", 'address': '1850 Douglas Blvd', 'city': 'Roseville', 'state': 'CA', 'zip': '95661', 'phone': '(916) 787-4300'},
    {'name': "Mountain Mike's Pizza", 'address': '990 Pleasant Grove Blvd', 'city': 'Roseville', 'state': 'CA', 'zip': '95678', 'phone': '(916) 780-6453'},
    {'name': "Mountain Mike's Pizza", 'address': '5505 Whitney Blvd', 'city': 'Rocklin', 'state': 'CA', 'zip': '95677', 'phone': '(916) 625-0777'},
    {'name': "Mountain Mike's Pizza", 'address': '1780 Pleasant Grove Blvd', 'city': 'West Roseville', 'state': 'CA', 'zip': '95747', 'phone': '(916) 702-7100'},
    
    # Folsom / Rancho Cordova
    {'name': "Mountain Mike's Pizza", 'address': '717 E Bidwell St', 'city': 'Folsom', 'state': 'CA', 'zip': '95630', 'phone': '(916) 983-3331'},
    {'name': "Mountain Mike's Pizza", 'address': '25075 Blue Ravine Rd', 'city': 'Folsom', 'state': 'CA', 'zip': '95630', 'phone': '(916) 817-1207'},
    {'name': "Mountain Mike's Pizza", 'address': '10419 Folsom Blvd', 'city': 'Rancho Cordova', 'state': 'CA', 'zip': '95670', 'phone': '(916) 363-0393'},
    
    # Citrus Heights / Fair Oaks
    {'name': "Mountain Mike's Pizza", 'address': '7777 Sunrise Blvd', 'city': 'Citrus Heights', 'state': 'CA', 'zip': '95610', 'phone': '(916) 728-1111'},
    {'name': "Mountain Mike's Pizza", 'address': '5267 Sunrise Blvd', 'city': 'Fair Oaks', 'state': 'CA', 'zip': '95628', 'phone': '(916) 961-4000'},
    {'name': "Mountain Mike's Pizza", 'address': '8801 Greenback Ln', 'city': 'Orangevale', 'state': 'CA', 'zip': '95662', 'phone': '(916) 989-6677'},
    
    # Carmichael
    {'name': "Mountain Mike's Pizza", 'address': '5019 El Camino Ave', 'city': 'Carmichael', 'state': 'CA', 'zip': '95608', 'phone': '(916) 486-1010'},
    {'name': "Mountain Mike's Pizza", 'address': '4141 Manzanita Ave', 'city': 'Carmichael', 'state': 'CA', 'zip': '95608', 'phone': '(916) 488-7676'},
    
    # North Highlands
    {'name': "Mountain Mike's Pizza", 'address': '6745 Watt Ave', 'city': 'North Highlands', 'state': 'CA', 'zip': '95660', 'phone': '(916) 331-8077'},
    
    # West Sacramento
    {'name': "Mountain Mike's Pizza", 'address': '2919 West Capital Ave', 'city': 'West Sacramento', 'state': 'CA', 'zip': '95691', 'phone': '(916) 372-8984'},
    
    # Napa / Sonoma Area
    {'name': "Mountain Mike's Pizza", 'address': '1501 Trancas St', 'city': 'Napa', 'state': 'CA', 'zip': '94558', 'phone': '(707) 751-6100'},
    {'name': "Mountain Mike's Pizza", 'address': '410 Napa Junction Rd', 'city': 'American Canyon', 'state': 'CA', 'zip': '94503', 'phone': '(707) 563-5505'},
    
    # Santa Rosa
    {'name': "Mountain Mike's Pizza", 'address': '1150 Santa Rosa Ave', 'city': 'Santa Rosa', 'state': 'CA', 'zip': '95404', 'phone': '(707) 544-2828'},
    {'name': "Mountain Mike's Pizza", 'address': '3125 Cleveland Ave', 'city': 'Santa Rosa', 'state': 'CA', 'zip': '95403', 'phone': '(707) 595-6505'},
    {'name': "Mountain Mike's Pizza", 'address': '4501 Montgomery Dr', 'city': 'Santa Rosa', 'state': 'CA', 'zip': '95409', 'phone': '(707) 890-5033'},
    
    # Petaluma / Novato
    {'name': "Mountain Mike's Pizza", 'address': '919 Lakeville St', 'city': 'Petaluma', 'state': 'CA', 'zip': '94952', 'phone': '(707) 769-8989'},
    {'name': "Mountain Mike's Pizza", 'address': '1561 S Novato Blvd', 'city': 'Novato', 'state': 'CA', 'zip': '94947', 'phone': '(415) 898-8800'},
    
    # Fairfield / Vacaville
    {'name': "Mountain Mike's Pizza", 'address': '1819 N Texas St', 'city': 'Fairfield', 'state': 'CA', 'zip': '94533', 'phone': '(707) 422-6000'},
    {'name': "Mountain Mike's Pizza", 'address': '251 Pittman Rd', 'city': 'Fairfield', 'state': 'CA', 'zip': '94534', 'phone': '(707) 864-1700'},
    {'name': "Mountain Mike's Pizza", 'address': '645 Elmira Rd', 'city': 'Vacaville', 'state': 'CA', 'zip': '95687', 'phone': '(707) 451-9854'},
    {'name': "Mountain Mike's Pizza", 'address': '401 E Monte Vista Ave', 'city': 'Vacaville', 'state': 'CA', 'zip': '95688', 'phone': '(707) 447-0123'},
    
    # Vallejo
    {'name': "Mountain Mike's Pizza", 'address': '972 Admiral Callaghan Ln', 'city': 'Vallejo', 'state': 'CA', 'zip': '94591', 'phone': '(707) 515-6930'},
    {'name': "Mountain Mike's Pizza", 'address': '4380 Sonoma Blvd', 'city': 'Vallejo', 'state': 'CA', 'zip': '94589', 'phone': '(707) 980-6696'},
    
    # Stockton
    {'name': "Mountain Mike's Pizza", 'address': '1000 Robinhood Dr', 'city': 'Stockton', 'state': 'CA', 'zip': '95207', 'phone': '(209) 474-7470'},
    {'name': "Mountain Mike's Pizza", 'address': '678 N Wilson Way', 'city': 'Stockton', 'state': 'CA', 'zip': '95210', 'phone': '(209) 941-2256'},
    
    # Modesto
    {'name': "Mountain Mike's Pizza", 'address': '2720 McHenry Ave', 'city': 'Modesto', 'state': 'CA', 'zip': '95350', 'phone': '(209) 521-4403'},
    {'name': "Mountain Mike's Pizza", 'address': '3601 Pelandale Ave', 'city': 'Modesto', 'state': 'CA', 'zip': '95356', 'phone': '(209) 497-6799'},
    
    # Fresno
    {'name': "Mountain Mike's Pizza", 'address': '1055 E Herndon Ave', 'city': 'Fresno', 'state': 'CA', 'zip': '93720', 'phone': '(559) 439-5898'},
    {'name': "Mountain Mike's Pizza", 'address': '5150 E Kings Canyon Rd', 'city': 'Fresno', 'state': 'CA', 'zip': '93727', 'phone': '(559) 255-1100'},
    {'name': "Mountain Mike's Pizza", 'address': '1089 E Shaw Ave', 'city': 'Fresno', 'state': 'CA', 'zip': '93710', 'phone': '(559) 241-7210'},
    
    # Clovis
    {'name': "Mountain Mike's Pizza", 'address': '1610 Herndon Ave', 'city': 'Clovis', 'state': 'CA', 'zip': '93611', 'phone': '(559) 298-7000'},
    {'name': "Mountain Mike's Pizza", 'address': '1798 Ashlan Ave', 'city': 'Clovis', 'state': 'CA', 'zip': '93611', 'phone': '(559) 291-9999'},
    
    # Manteca / Tracy
    {'name': "Mountain Mike's Pizza", 'address': '1120 N Main St', 'city': 'Manteca', 'state': 'CA', 'zip': '95336', 'phone': '(209) 823-1166'},
    {'name': "Mountain Mike's Pizza", 'address': '870 W Schulte Rd', 'city': 'Tracy', 'state': 'CA', 'zip': '95376', 'phone': '(209) 836-4141'},
    
    # Rohnert Park
    {'name': "Mountain Mike's Pizza", 'address': '1451 Southwest Blvd', 'city': 'Rohnert Park', 'state': 'CA', 'zip': '94928', 'phone': '(707) 795-4433'},
    {'name': "Mountain Mike's Pizza", 'address': '6314 Commerce Blvd', 'city': 'Rohnert Park', 'state': 'CA', 'zip': '94928', 'phone': '(707) 303-7474'},
    
    # Lincoln / Auburn
    {'name': "Mountain Mike's Pizza", 'address': '820 Sterling Pkwy', 'city': 'Lincoln', 'state': 'CA', 'zip': '95648', 'phone': '(916) 543-9997'},
    {'name': "Mountain Mike's Pizza", 'address': '2520 Bell Rd', 'city': 'Auburn', 'state': 'CA', 'zip': '95603', 'phone': '(530) 888-8050'},
    
    # Cameron Park
    {'name': "Mountain Mike's Pizza", 'address': '2650 Cameron Park Dr', 'city': 'Cameron Park', 'state': 'CA', 'zip': '95682', 'phone': '(530) 676-9600'},
]

# Teriyaki Madness - California locations
TERIYAKI_MADNESS = [
    # Sacramento Area
    {'name': 'Teriyaki Madness', 'address': '6121 Sunrise Blvd', 'city': 'Citrus Heights', 'state': 'CA', 'zip': '95610', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '1798 Commons', 'city': 'Folsom', 'state': 'CA', 'zip': '95630', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '1916 E Copper Ave, Ste 104', 'city': 'Fresno', 'state': 'CA', 'zip': '93730', 'phone': '(559) 570-2370'},
    {'name': 'Teriyaki Madness', 'address': '1535 Herndon Ave', 'city': 'Fresno', 'state': 'CA', 'zip': '93611', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '2919 West Capital Ave', 'city': 'West Sacramento', 'state': 'CA', 'zip': '95691', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '4000 S Frontage Rd', 'city': 'Modesto', 'state': 'CA', 'zip': '95356', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '110 General Stilwell Dr', 'city': 'Marina', 'state': 'CA', 'zip': '93933', 'phone': '(831) 324-4932'},
    {'name': 'Teriyaki Madness', 'address': '2424 San Pablo Ave', 'city': 'Novato', 'state': 'CA', 'zip': '94945', 'phone': ''},
    
    # Bay Area
    {'name': 'Teriyaki Madness', 'address': '1 South Market Dr', 'city': 'San Jose', 'state': 'CA', 'zip': '95134', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '1525 N Milpitas Blvd', 'city': 'Milpitas', 'state': 'CA', 'zip': '95035', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '4000 Dublin Blvd', 'city': 'Dublin', 'state': 'CA', 'zip': '94568', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '3100 Hopyard Rd', 'city': 'Pleasanton', 'state': 'CA', 'zip': '94588', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '4502 1st St', 'city': 'Livermore', 'state': 'CA', 'zip': '94550', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '901 First St', 'city': 'Manteca', 'state': 'CA', 'zip': '95336', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '3333 EI Camino Real', 'city': 'Santa Clara', 'state': 'CA', 'zip': '95051', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '1655 Branham Lane', 'city': 'San Jose', 'state': 'CA', 'zip': '95118', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '2600 El Camino Real', 'city': 'Redwood City', 'state': 'CA', 'zip': '94061', 'phone': ''},
    
    # SoCal
    {'name': 'Teriyaki Madness', 'address': '21227 Hawthorne Blvd #130', 'city': 'Torrance', 'state': 'CA', 'zip': '90503', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '20100 Magnolia St', 'city': 'Huntington Beach', 'state': 'CA', 'zip': '92646', 'phone': '(714) 593-0200'},
    {'name': 'Teriyaki Madness', 'address': '4954 Van Nuys Blvd #103', 'city': 'Sherman Oaks', 'state': 'CA', 'zip': '91403', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '16408 Village Way', 'city': 'Santa Clarita', 'state': 'CA', 'zip': '91387', 'phone': '(661) 309-4810'},
    {'name': 'Teriyaki Madness', 'address': '28227 Newhall Ranch Rd', 'city': 'Santa Clarita', 'state': 'CA', 'zip': '91355', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '1240 Truman St #165', 'city': 'San Fernando', 'state': 'CA', 'zip': '91340', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '1120 W 6th St Unit 105', 'city': 'Los Angeles', 'state': 'CA', 'zip': '90017', 'phone': '(213) 265-7290'},
    {'name': 'Teriyaki Madness', 'address': '1525 Columbus St Ste 100', 'city': 'Bakersfield', 'state': 'CA', 'zip': '93305', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '5353 Gosford Rd', 'city': 'Bakersfield', 'state': 'CA', 'zip': '93313', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '2905 H St', 'city': 'Bakersfield', 'state': 'CA', 'zip': '93301', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '22910 Alessandro Blvd', 'city': 'Moreno Valley', 'state': 'CA', 'zip': '92553', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '12970 Hesperia Rd', 'city': 'Victorville', 'state': 'CA', 'zip': '92395', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '4059 E Tulare Ave', 'city': 'Visalia', 'state': 'CA', 'zip': '93277', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '22970 Clinton Keith Rd', 'city': 'Wildomar', 'state': 'CA', 'zip': '92595', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '2311 E Avenue S', 'city': 'Palmdale', 'state': 'CA', 'zip': '93550', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '1340 N McCawley Rd', 'city': 'Chatsworth', 'state': 'CA', 'zip': '91311', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '12874顽 12874 Van Nuys Blvd', 'city': 'Sylmar', 'state': 'CA', 'zip': '91342', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '29379 The Old Road', 'city': 'Stevenson Ranch', 'state': 'CA', 'zip': '91381', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '1305 S Brand Blvd', 'city': 'Glendale', 'state': 'CA', 'zip': '91204', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '2650 E Thousand Oaks Blvd', 'city': 'Thousand Oaks', 'state': 'CA', 'zip': '91362', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '1350 W 7th St', 'city': 'San Bernardino', 'state': 'CA', 'zip': '92411', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '1188 E Mission Blvd', 'city': 'Ontario', 'state': 'CA', 'zip': '91761', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '1525 2nd St', 'city': 'San Fernando', 'state': 'CA', 'zip': '91340', 'phone': ''},
    {'name': 'Teriyaki Madness', 'address': '3180imp 3180imp Sepulveda Blvd', 'city': 'Los Angeles', 'state': 'CA', 'zip': '90034', 'phone': ''},
]


def add_to_leads(franchises, filename):
    """Add franchise locations to leads CSV"""
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
    for loc in franchises:
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
                'category_type': 'pizza' if 'mountain mike' in loc.get('name', '').lower() else 'japanese',
                'categories': 'Pizza' if 'mountain mike' in loc.get('name', '').lower() else 'Japanese/Korean',
                'rating': '',
                'review_count': '',
                'source': 'MountainMikes.com' if 'mountain mike' in loc.get('name', '').lower() else 'TeriyakiMadness.com',
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
        print(f"[+] Added {new_count} locations to {filename}")
    else:
        print(f"[=] No new locations to add")
    
    return new_count


def main():
    print("="*60)
    print("Adding Franchise Locations to PSDEPOT Leads")
    print("="*60)
    
    # Add Mountain Mike's
    print(f"\n🏔️ Mountain Mike's Pizza: {len(MOUNTAIN_MIKES)} locations")
    mm_added = add_to_leads(MOUNTAIN_MIKES, 'psdepot_leads_latest.csv')
    add_to_leads(MOUNTAIN_MIKES, 'pizza.csv')
    
    # Add Teriyaki Madness
    print(f"\n🍱 Teriyaki Madness: {len(TERIYAKI_MADNESS)} locations")
    tm_added = add_to_leads(TERIYAKI_MADNESS, 'psdepot_leads_latest.csv')
    add_to_leads(TERIYAKI_MADNESS, 'japanese.csv')
    
    print("\n" + "="*60)
    print(f"Total new locations added: {mm_added + tm_added}")
    print("="*60)


if __name__ == '__main__':
    main()
