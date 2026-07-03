#!/usr/bin/env python3
"""
PSDEPOT Prospecting - Convert Yelp Cache to Lead Database
Uses existing Yelp data to build prospecting map
"""

import json
import csv
import os
from pathlib import Path
from datetime import datetime

# Paths
CACHE_FILE = '/data/data/com.termux/files/home/mortimer/software/depotchaos/yelp_cache.json'
OUTPUT_DIR = '/data/data/com.termux/files/home/mortimer/projects/psdepot_prospecting/data'
MAP_DIR = '/data/data/com.termux/files/home/mortimer/projects/psdepot_prospecting/map'

# PSDEPOT target categories (regex patterns)
TARGET_CATEGORIES = {
    'mexican': ['taqueria', 'mexican', 'carniceria', 'panaderia', 'bodega', 'tortilleria', 'antojitos'],
    'thai': ['thai'],
    'korean': ['korean', 'korean bbq'],
    'vietnamese': ['vietnamese', 'pho'],
    'chinese': ['chinese', 'dim sum', 'wok'],
    'japanese': ['japanese', 'sushi', 'ramen', 'izakaya'],
    'indian': ['indian', 'curry', 'tandoori'],
    'filipino': ['filipino', 'lumpia'],
    'pizza': ['pizza', 'pizzeria'],
    'cafe': ['cafe', 'coffee', 'bubble tea', 'tea house', 'juice bar', 'paleteria', 'jugueria'],
    'bakery': ['bakery', 'donut', 'dessert', 'ice cream', 'cupcakes'],
    'bar': ['bar', 'sports bar', 'lounge', 'brewery', 'pub'],
    'food_truck': ['food truck', 'food cart'],
    'mediterranean': ['mediterranean', 'greek', 'middle eastern', 'lebanese', 'turkish', 'falafel', 'shawarma'],
    'caribbean': ['caribbean', 'jamaican', 'cuban', 'puertorican'],
    'retail': ['convenience', 'liquor store', 'dispensary', 'vape', 'cell phone', 'florist'],
}

# Sacramento area ZIPs
SAC_ZIPS = ['95814', '95815', '95816', '95817', '95818', '95819', '95820', '95821', '95822', '95823', 
            '95824', '95825', '95826', '95827', '95828', '95829', '95830', '95831', '95832', '95833',
            '95834', '95835', '95836', '95837', '95838', '95841', '95842', '95843', '95851', '95852',
            '95853', '95860', '95864', '95865', '95866', '95867', '95894', '95895', '95624', '95757',
            '95758', '95759', '95683', '95693']

NORCAL_ZIPS = ['95401', '95402', '95403', '95404', '95405', '95406', '95407', '95409',  # Santa Rosa
               '94558', '94559', '94573', '94581',  # Napa
               '95476',  # Sonoma
               '94515',  # Calistoga
               '94503',  # American Canyon
               '94928', '94931',  # Petaluma
               '94945', '94946', '94947',  # Novato
               '94949',  # Novato
               ] + SAC_ZIPS

# City mapping
CITY_MAP = {
    'fresno': 'Fresno', 'clovis': 'Clovis', 'madera': 'Madera',
    'sacramento': 'Sacramento', 'elk grove': 'Elk Grove', 'rancho cordova': 'Rancho Cordova',
    'citrus heights': 'Citrus Heights', 'roseville': 'Roseville', 'folsom': 'Folsom',
    'napa': 'Napa', 'sonoma': 'Sonoma', 'calistoga': 'Calistoga', 'yountville': 'Yountville',
    'santa rosa': 'Santa Rosa', 'petaluma': 'Petaluma', 'novato': 'Novato',
    'oakhurst': 'Oakhurst', 'mammoth lakes': 'Mammoth Lakes',
    'hanford': 'Hanford', 'visalia': 'Visalia', 'porterville': 'Porterville',
    'merced': 'Merced', 'modesto': 'Modesto', 'stockton': 'Stockton',
}


def load_yelp_cache():
    """Load Yelp cache file"""
    print(f"Loading Yelp cache: {CACHE_FILE}")
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Loaded {len(data)} businesses")
    return data


def categorize_business(categories):
    """Determine PSDEPOT category from Yelp categories"""
    if not categories:
        return None
    
    cats_text = ' '.join(categories).lower()
    
    for cat_type, keywords in TARGET_CATEGORIES.items():
        for keyword in keywords:
            if keyword in cats_text:
                return cat_type
    return None


def extract_city(address, city_field=None):
    """Extract city from address or use city field"""
    if city_field:
        return city_field.title()
    
    # Try to extract from address
    if address:
        addr_lower = address.lower()
        for city_name in CITY_MAP:
            if city_name in addr_lower:
                return CITY_MAP[city_name]
    
    return None


def convert_to_leads(data):
    """Convert Yelp cache to lead format"""
    leads = []
    skipped = 0
    
    for key, info in data.items():
        if info is None:
            continue
        
        # Handle list type (take first element)
        if isinstance(info, list):
            if len(info) > 0 and isinstance(info[0], dict):
                info = info[0]
            else:
                skipped += 1
                continue
        
        if not isinstance(info, dict):
            skipped += 1
            continue
        
        # Check if has required fields
        if not info.get('phone') or not info.get('address'):
            skipped += 1
            continue
        
        # Categorize
        categories = info.get('categories', [])
        cat_type = categorize_business(categories)
        
        # Skip if not a target category
        if cat_type is None:
            skipped += 1
            continue
        
        # Categorize
        categories = info.get('categories', [])
        cat_type = categorize_business(categories)
        
        # Skip if not a target category
        if cat_type is None:
            skipped += 1
            continue
        
        # Extract data
        name = info.get('name', key)
        phone = info.get('phone', '')
        address = info.get('address', '')
        city = extract_city(address, info.get('city'))
        state = info.get('state', 'CA')
        zipcode = info.get('zip', '')
        website = info.get('yelp_url', '')
        rating = info.get('rating')
        reviews = info.get('review_count')
        
        lead = {
            'name': name,
            'phone': clean_phone(phone),
            'address': address,
            'city': city,
            'state': state,
            'zip': zipcode,
            'website': website,
            'category_type': cat_type,
            'categories': ', '.join(categories[:5]),
            'rating': rating if rating else '',
            'review_count': reviews if reviews else '',
            'source': 'Yelp',
            'date_found': datetime.now().strftime('%Y-%m-%d'),
        }
        leads.append(lead)
    
    print(f"Converted: {len(leads)} leads")
    print(f"Skipped: {skipped} (not target category)")
    return leads


def clean_phone(phone):
    """Clean phone number"""
    if not phone:
        return ''
    digits = ''.join(c for c in str(phone) if c.isdigit())
    if len(digits) == 11 and digits[0] == '1':
        digits = digits[1:]
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return str(phone)


def save_csv(leads, filename):
    """Save leads to CSV"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    if not leads:
        print("[!] No leads to save")
        return None
    
    fieldnames = ['name', 'phone', 'address', 'city', 'state', 'zip', 'website',
                  'category_type', 'categories', 'rating', 'review_count', 'source', 'date_found']
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(leads)
    
    print(f"[+] Saved: {filepath} ({len(leads)} leads)")
    return filepath


def save_by_category(leads):
    """Save separate CSVs by category"""
    by_cat = {}
    for lead in leads:
        cat = lead.get('category_type', 'other')
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append(lead)
    
    for cat, cat_leads in by_cat.items():
        filename = f'{cat}.csv'
        save_csv(cat_leads, filename)
    
    return by_cat


def generate_map(leads, output_path):
    """Generate interactive HTML map"""
    import random
    
    # Coordinates for cities
    CITY_COORDS = {
        'sacramento': (38.5816, -121.4944),
        'elk grove': (38.4088, -121.3716),
        'fresno': (36.7378, -119.7871),
        'napa': (38.2975, -122.2869),
        'sonoma': (38.2919, -122.4580),
        'calistoga': (38.5785, -122.5797),
        'santa rosa': (38.4404, -122.7141),
        'petaluma': (38.2324, -122.6367),
        'novato': (38.1074, -122.5697),
    }
    
    # Convert leads to markers
    markers = []
    for lead in leads:
        city = lead.get('city', '').lower()
        coords = CITY_COORDS.get(city, (38.5816 + random.uniform(-0.2, 0.2), -121.4944 + random.uniform(-0.2, 0.2)))
        
        lat = coords[0] + random.uniform(-0.03, 0.03)
        lng = coords[1] + random.uniform(-0.03, 0.03)
        
        markers.append({
            'name': lead.get('name', ''),
            'phone': lead.get('phone', ''),
            'address': lead.get('address', ''),
            'city': lead.get('city', ''),
            'category': lead.get('category_type', 'other'),
            'categories': lead.get('categories', ''),
            'rating': lead.get('rating', ''),
            'lat': lat,
            'lng': lng,
        })
    
    # Category colors
    colors = {
        'mexican': '#e94560',
        'thai': '#f39c12',
        'korean': '#27ae60',
        'vietnamese': '#3498db',
        'chinese': '#e74c3c',
        'japanese': '#9b59b6',
        'indian': '#f1c40f',
        'filipino': '#1abc9c',
        'pizza': '#e67e22',
        'cafe': '#795548',
        'bakery': '#ffeb3b',
        'bar': '#673ab7',
        'food_truck': '#00bcd4',
        'mediterranean': '#009688',
        'caribbean': '#ff5722',
        'retail': '#607d8b',
        'other': '#9e9e9e'
    }
    
    # Group by category
    categories = {}
    for m in markers:
        cat = m['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(m)
    
    markers_json = json.dumps(markers, ensure_ascii=False)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PSDEPOT Prospecting Map - Northern California</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; }}
        #header {{ background: linear-gradient(135deg, #16213e, #1a1a2e); padding: 20px; border-bottom: 2px solid #e94560; }}
        #header h1 {{ color: #e94560; font-size: 24px; }}
        #header p {{ color: #888; font-size: 14px; margin-top: 5px; }}
        #controls {{ background: #16213e; padding: 15px 20px; display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }}
        #controls label {{ color: #e94560; font-weight: bold; margin-right: 10px; }}
        .filter-btn {{ background: #0f3460; color: #eee; border: 1px solid #e94560; padding: 8px 16px; border-radius: 20px; cursor: pointer; transition: all 0.3s; }}
        .filter-btn:hover, .filter-btn.active {{ background: #e94560; color: #fff; }}
        #stats {{ background: #16213e; padding: 10px 20px; font-size: 14px; color: #888; border-top: 1px solid #0f3460; }}
        #stats span {{ color: #e94560; font-weight: bold; }}
        #map {{ height: calc(100vh - 160px); width: 100%; }}
        .popup {{ min-width: 280px; }}
        .popup h3 {{ color: #e94560; margin-bottom: 10px; font-size: 16px; }}
        .popup p {{ margin: 6px 0; font-size: 13px; }}
        .popup a {{ color: #e94560; text-decoration: none; }}
        .popup a:hover {{ text-decoration: underline; }}
        .popup .cat-badge {{ display: inline-block; background: #0f3460; color: #eee; padding: 3px 10px; border-radius: 12px; font-size: 11px; margin-top: 8px; text-transform: capitalize; }}
        .popup .rating {{ color: #f39c12; }}
        .legend {{ background: white; padding: 10px; border-radius: 5px; line-height: 1.8; }}
        .legend-item {{ display: flex; align-items: center; gap: 8px; }}
        .legend-color {{ width: 12px; height: 12px; border-radius: 50%; }}
    </style>
</head>
<body>
    <div id="header">
        <h1>🖥️ PSDEPOT Prospecting Map</h1>
        <p>Thermal Receipt Paper Leads — Northern California | {len(leads)} businesses</p>
    </div>
    
    <div id="controls">
        <label>Filter:</label>
        <button class="filter-btn active" onclick="filterCategory('all')">All ({len(leads)})</button>
'''
    
    for cat, cat_leads in sorted(categories.items()):
        count = len(cat_leads)
        cat_name = cat.replace('_', ' ').title()
        html += f'        <button class="filter-btn" onclick="filterCategory(\'{cat}\')">{cat_name} ({count})</button>\n'
    
    html += '''    </div>
    
    <div id="stats">
        Showing <span id="visible-count">''' + str(len(leads)) + '''</span> businesses
    </div>
    
    <div id="map"></div>
    
    <script>
        const businesses = ''' + markers_json + ''';
        
        const colors = ''' + json.dumps(colors) + ''';
        
        const map = L.map('map').setView([38.5, -121.5], 8);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap'
        }).addTo(map);
        
        // Add legend
        const legend = L.control({{position: 'bottomright'}});
        legend.onAdd = function(map) {{
            const div = L.DomUtil.create('div', 'legend');
            div.innerHTML = '<b>Categories</b><br>';
            for (const [cat, color] of Object.entries(colors)) {{
                if (document.querySelector(`[onclick="filterCategory('$\{{cat\}}')"]`) || cat === 'all') {{
                    div.innerHTML += `<div class="legend-item"><div class="legend-color" style="background:${{color}}"></div>${{cat.replace('_', ' ')}}</div>`;
                }}
            }}
            return div;
        }};
        legend.addTo(map);
        
        const markers = {{}};
        let visibleMarkers = L.layerGroup().addTo(map);
        
        businesses.forEach((b, i) => {{
            const color = colors[b.category] || colors.other;
            const icon = L.divIcon({{
                html: `<div style="background:${{color}};width:10px;height:10px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 4px rgba(0,0,0,0.5);"></div>`,
                className: 'marker',
                iconSize: [14, 14]
            }});
            
            const marker = L.marker([b.lat, b.lng], {{ icon }});
            
            const popup = `
                <div class="popup">
                    <h3>${{b.name}}</h3>
                    <p>📍 ${{b.address}}</p>
                    <p>📞 ${{b.phone || 'N/A'}}</p>
                    ${{b.rating ? `<p>⭐ ${{b.rating}} stars</p>` : ''}}
                    <p>🏷️ ${{b.categories || b.category}}</p>
                    <span class="cat-badge">${{b.category.replace('_', ' ')}}</span>
                </div>
            `;
            
            marker.bindPopup(popup);
            marker.category = b.category;
            markers[i] = marker;
        }});
        
        function filterCategory(cat) {{
            visibleMarkers.clearLayers();
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            
            let count = 0;
            Object.values(markers).forEach(m => {{
                if (cat === 'all' || m.category === cat) {{
                    m.addTo(visibleMarkers);
                    count++;
                }}
            }});
            
            document.getElementById('visible-count').textContent = count;
            
            const activeBtn = Array.from(document.querySelectorAll('.filter-btn')).find(btn => 
                btn.textContent.includes(cat.replace('_', ' ').title()) || (cat === 'all' && btn.textContent.includes('All'))
            );
            if (activeBtn) activeBtn.classList.add('active');
            
            if (cat === 'all') map.setView([38.5, -121.5], 8);
        }}
        
        filterCategory('all');
    </script>
</body>
</html>'''
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"[+] Map generated: {output_path}")
    return output_path


def main():
    print("="*60)
    print("PSDEPOT LEAD GENERATION - Yelp Cache Converter")
    print("="*60)
    
    # Load data
    data = load_yelp_cache()
    
    # Convert to leads
    leads = convert_to_leads(data)
    
    if not leads:
        print("[!] No leads found")
        return
    
    # Save main CSV
    timestamp = datetime.now().strftime('%Y%m%d')
    save_csv(leads, f'psdepot_leads_{timestamp}.csv')
    save_csv(leads, 'psdepot_leads_latest.csv')
    
    # Save by category
    by_category = save_by_category(leads)
    
    # Generate map
    map_path = os.path.join(MAP_DIR, 'psdepot_map.html')
    generate_map(leads, map_path)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total leads: {len(leads)}")
    for cat, cat_leads in sorted(by_category.items()):
        print(f"  {cat}: {len(cat_leads)}")
    print("="*60)
    print(f"\nFiles created:")
    print(f"  Database: {OUTPUT_DIR}/psdepot_leads_latest.csv")
    print(f"  Map: {map_path}")
    print("="*60)


if __name__ == '__main__':
    main()
