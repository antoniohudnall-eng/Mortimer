#!/usr/bin/env python3
"""Update collections addresses from DepotChaos CRM"""

import sqlite3
import json

COLLECTIONS_DB = '/root/.openclaw/workspace/datadepot/data/collections.db'
CRM_DB = '/root/.openclaw/workspace/data/depot_chaos/unified.db'

def get_crm_addresses():
    """Get addresses from CRM"""
    conn = sqlite3.connect(CRM_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all CA businesses with addresses
    cursor.execute("""
        SELECT business_name, address, city, state, zip, phone, email 
        FROM leads 
        WHERE state = 'CA' 
        AND address IS NOT NULL 
        AND address != ''
    """)
    
    addresses = {}
    for row in cursor.fetchall():
        name = row['business_name'].lower().strip()
        addr = f"{row['address']}, {row['city']}, {row['state']} {row['zip'] or ''}".strip()
        addresses[name] = {
            'address': addr,
            'phone': row['phone'] or '',
            'email': row['email'] or ''
        }
    
    conn.close()
    return addresses

def update_collections():
    """Update collections with real addresses"""
    crm_data = get_crm_addresses()
    
    conn = sqlite3.connect(COLLECTIONS_DB)
    cursor = conn.cursor()
    
    # Get all collections accounts without real addresses
    cursor.execute("SELECT id, customer_name FROM collections_accounts WHERE address LIKE '%Address not on file%' OR address LIKE '%1234%' OR address LIKE '%5678%' OR address LIKE '%9012%'")
    accounts = cursor.fetchall()
    
    print(f"Found {len(accounts)} accounts with placeholder addresses")
    
    updated = 0
    for account_id, customer_name in accounts:
        # Try to match by name
        name_lower = customer_name.lower().strip()
        
        # Direct match
        if name_lower in crm_data:
            data = crm_data[name_lower]
            cursor.execute("""
                UPDATE collections_accounts 
                SET address = ?, phone = ?, email = ?
                WHERE id = ?
            """, (data['address'], data['phone'], data['email'], account_id))
            updated += 1
            print(f"✅ Updated: {customer_name}")
            continue
        
        # Partial match - remove common suffixes
        clean_name = name_lower.replace(' owner', '').replace(' manager', '').replace(' general manager', '').replace(' supply only', '').replace(' ncc', '').strip()
        
        for crm_name, data in crm_data.items():
            if clean_name in crm_name or crm_name in clean_name:
                cursor.execute("""
                    UPDATE collections_accounts 
                    SET address = ?, phone = ?, email = ?
                    WHERE id = ?
                """, (data['address'], data['phone'], data['email'], account_id))
                updated += 1
                print(f"✅ Matched (partial): {customer_name} -> {crm_name}")
                break
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Updated {updated} accounts with real addresses")

if __name__ == '__main__':
    update_collections()
