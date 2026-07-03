#!/usr/bin/env python3
"""
PSDEPOT Lead Generation - Interactive Map Generator
Creates HTML map with markers and filters from CSV data
"""

import csv
import json
import os
from pathlib import Path

OUTPUT_DIR = '/data/data/com.termux/files/home/mortimer/projects/psdepot_prospecting'
DATA_DIR = f'{OUTPUT_DIR}/data'


def load_businesses(csv_path):
    """Load businesses from CSV"""
    businesses = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            businesses.append(row)
    return businesses


def geocode_address(address):
    """Convert address to approximate lat/lng for common locations"""
    # Sacramento area approximate coordinates
    locations = {
        'sacramento': (38.5816, -121.4944),
        'elk grove': (38.4088, -121.3716),
        'santa rosa': (38.4404, -122.7141),
        'napa': (38.2975, -122.2869),
        'sonoma': (38.2919, -122.4580),
        'calistoga': (38.5785, -122.5797),
        'american canyon': (38.1749, -122.2611),
    }
    
    address_lower = address.lower()
    for loc, coords in locations.items():
        if loc in address_lower:
            # Add small random offset to spread markers
            import random
            lat = coords[0] + random.uniform(-0.05, 0.05)
            lng = coords[1] + random.uniform(-0.05, 0.05)
            return lat, lng
    
    # Default to Sacramento
    import random
    return 38.5816 + random.uniform(-0.1, 0.1), -121.4944 + random.uniform(-0.1, 0.1)


def generate_map_html(businesses, output_path):
    """Generate interactive HTML map"""
    
    # Group by category
    categories = {}
    for b in businesses:
        cat = b.get('category_type', 'other')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(b)
    
    # Convert to JSON for JS
    markers_json = []
    for b in businesses:
        lat, lng = geocode_address(b.get('address', ''))
        marker = {
            'name': b.get('name', ''),
            'phone': b.get('phone', ''),
            'address': b.get('address', ''),
            'website': b.get('website', ''),
            'category': b.get('category_type', 'other'),
            'categories': b.get('categories', ''),
            'lat': lat,
            'lng': lng,
        }
        markers_json.append(marker)
    
    markers_str = json.dumps(markers_json, ensure_ascii=False)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PSDEPOT Prospecting Map - Northern California</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #eee;
        }}
        #header {{
            background: linear-gradient(135deg, #16213e, #1a1a2e);
            padding: 20px;
            border-bottom: 2px solid #e94560;
        }}
        #header h1 {{
            color: #e94560;
            font-size: 24px;
            margin-bottom: 5px;
        }}
        #header p {{
            color: #888;
            font-size: 14px;
        }}
        #controls {{
            background: #16213e;
            padding: 15px 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
        }}
        #controls label {{
            color: #e94560;
            font-weight: bold;
        }}
        .filter-btn {{
            background: #0f3460;
            color: #eee;
            border: 1px solid #e94560;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .filter-btn:hover, .filter-btn.active {{
            background: #e94560;
            color: #fff;
        }}
        #stats {{
            background: #16213e;
            padding: 10px 20px;
            font-size: 14px;
            color: #888;
        }}
        #stats span {{
            color: #e94560;
            font-weight: bold;
        }}
        #map {{
            height: calc(100vh - 180px);
            width: 100%;
        }}
        .popup {{
            min-width: 250px;
        }}
        .popup h3 {{
            color: #e94560;
            margin-bottom: 10px;
            font-size: 16px;
        }}
        .popup p {{
            margin: 5px 0;
            font-size: 13px;
        }}
        .popup a {{
            color: #e94560;
            text-decoration: none;
        }}
        .popup a:hover {{
            text-decoration: underline;
        }}
        .popup .category {{
            display: inline-block;
            background: #0f3460;
            color: #eee;
            padding: 3px 10px;
            border-radius: 10px;
            font-size: 11px;
            margin-top: 8px;
        }}
    </style>
</head>
<body>
    <div id="header">
        <h1>🖥️ PSDEPOT Prospecting Map</h1>
        <p>Thermal Receipt Paper Leads — Northern California</p>
    </div>
    
    <div id="controls">
        <label>Filter by Category:</label>
        <button class="filter-btn active" onclick="filterCategory('all')">All ({len(businesses)})</button>
'''
    
    for cat, biz_list in sorted(categories.items()):
        count = len(biz_list)
        html += f'        <button class="filter-btn" onclick="filterCategory(\'{cat}\')">{cat.replace("_", " ").title()} ({count})</button>\n'
    
    html += '''    </div>
    
    <div id="stats">
        Showing <span id="visible-count">''' + str(len(businesses)) + '''</span> businesses
    </div>
    
    <div id="map"></div>
    
    <script>
        // Business data
        const businesses = ''' + markers_str + ''';
        
        // Category colors
        const colors = {
            mexican: '#e94560',
            thai: '#f39c12',
            korean: '#27ae60',
            vietnamese: '#3498db',
            chinese: '#e74c3c',
            japanese: '#9b59b6',
            indian: '#f1c40f',
            filipino: '#1abc9c',
            pizza: '#e67e22',
            cafe: '#795548',
            bakery: '#ffeb3b',
            bar: '#673ab7',
            food_truck: '#00bcd4',
            mediterranean: '#009688',
            caribbean: '#ff5722',
            retail: '#607d8b',
            other: '#9e9e9e'
        };
        
        // Initialize map
        const map = L.map('map').setView([38.5, -122.0], 8);
        
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap contributors'
        }}).addTo(map);
        
        // Create marker layer groups
        const markers = {};
        let visibleMarkers = L.layerGroup().addTo(map);
        
        // Add markers
        businesses.forEach((b, i) => {{
            const color = colors[b.category] || colors.other;
            
            const icon = L.divIcon({{
                html: `<div style="background:${color};width:12px;height:12px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 5px rgba(0,0,0,0.5);"></div>`,
                className: 'marker',
                iconSize: [16, 16]
            }});
            
            const marker = L.marker([b.lat, b.lng], {{ icon }});
            
            const popupContent = `
                <div class="popup">
                    <h3>${b.name}</h3>
                    <p><strong>📍</strong> ${b.address}</p>
                    <p><strong>📞</strong> ${b.phone || 'N/A'}</p>
                    ${b.website ? `<p><strong>🌐</strong> <a href="${b.website}" target="_blank">Website</a></p>` : ''}
                    <p><strong>🏷️</strong> ${b.categories || b.category}</p>
                    <span class="category">${b.category.replace('_', ' ')}</span>
                </div>
            `;
            
            marker.bindPopup(popupContent);
            marker.category = b.category;
            marker.id = i;
            
            markers[i] = marker;
        }});
        
        // Filter function
        function filterCategory(cat) {{
            visibleMarkers.clearLayers();
            
            // Update button states
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
                if (btn.textContent.includes('All') && cat === 'all') {{
                    btn.classList.add('active');
                }} else if (btn.textContent.toLowerCase().startsWith(cat.replace('_', ' '))) {{
                    btn.classList.add('active');
                }}
            }});
            
            let count = 0;
            Object.values(markers).forEach(m => {{
                if (cat === 'all' || m.category === cat) {{
                    m.addTo(visibleMarkers);
                    count++;
                }}
            }});
            
            document.getElementById('visible-count').textContent = count;
            
            // Fit bounds if showing all
            if (cat === 'all') {{
                map.setView([38.5, -122.0], 8);
            }}
        }}
        
        // Show all markers initially
        filterCategory('all');
    </script>
</body>
</html>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"[+] Map generated: {output_path}")
    return output_path


def generate_category_lists(businesses, output_dir):
    """Generate separate CSV files by category"""
    categories = {}
    for b in businesses:
        cat = b.get('category_type', 'other')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(b)
    
    for cat, biz_list in categories.items():
        filepath = f"{output_dir}/{cat}.csv"
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if biz_list:
                writer = csv.DictWriter(f, fieldnames=biz_list[0].keys())
                writer.writeheader()
                writer.writerows(biz_list)
        print(f"[+] {cat}: {len(biz_list)} businesses")


def main():
    # Find latest CSV
    data_dir = Path(DATA_DIR)
    csv_files = list(data_dir.glob('psdepot_leads_*.csv'))
    
    if not csv_files:
        print("[!] No CSV files found. Run the scraper first.")
        return
    
    latest_csv = sorted(csv_files)[-1]
    print(f"Using: {latest_csv}")
    
    # Load businesses
    businesses = load_businesses(latest_csv)
    print(f"Loaded {len(businesses)} businesses")
    
    # Generate map
    map_path = f"{OUTPUT_DIR}/map/psdepot_map.html"
    os.makedirs(os.path.dirname(map_path), exist_ok=True)
    generate_map_html(businesses, map_path)
    
    # Generate category lists
    generate_category_lists(businesses, DATA_DIR)
    
    print(f"\n[✓] Complete!")


if __name__ == '__main__':
    main()
