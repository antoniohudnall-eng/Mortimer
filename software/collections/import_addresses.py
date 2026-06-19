#!/usr/bin/env python3
"""
Import real addresses from Clients_2025.xlsx into collections database
Matches by customer name
"""

import pandas as pd
import sqlite3
import re

COLLECTIONS_DB = '/root/.openclaw/workspace/datadepot/data/collections.db'
CLIENTS_FILE = '/root/.openclaw/workspace/aocros/agents/crypto-financial/Clients_2025 (3).xlsx'

def normalize_name(name):
    """Normalize name for matching"""
    if not name or pd.isna(name):
        return ''
    name = str(name).lower().strip()
    # Remove common suffixes
    name = re.sub(r'\s+(owner|manager|general manager|supply only|ncc|left msg|open)$', '', name)
    name = re.sub(r'[^a-z0-9]', '', name)  # Remove special chars
    return name

def import_addresses():
    print("📊 Loading client data...")
    
    # Read Excel - just the columns we need
    df = pd.read_excel(CLIENTS_FILE, sheet_name='Master', header=1, usecols=[0, 13, 14, 19, 20, 21, 22])
    df.columns = ['company', 'contact', 'phone', 'street', 'city', 'state', 'zip']
    
    # Build lookup dictionary
    addresses = {}
    for _, row in df.iterrows():
        if pd.notna(row['company']):
            key = normalize_name(row['company'])
            if key:
                addr_parts = []
                if pd.notna(row['street']): addr_parts.append(str(row['street']))
                if pd.notna(row['city']): addr_parts.append(str(row['city']))
                if pd.notna(row['state']): addr_parts.append(str(row['state']))
                if pd.notna(row['zip']): addr_parts.append(str(row['zip']))
                
                addresses[key] = {
                    'address': ', '.join(addr_parts) if addr_parts else None,
                    'phone': str(row['phone']) if pd.notna(row['phone']) else None,
                    'contact': str(row['contact']) if pd.notna(row['contact']) else None
                }
    
    print(f"✅ Loaded {len(addresses)} client addresses")
    
    # Connect to collections
    conn = sqlite3.connect(COLLECTIONS_DB)
    cursor = conn.cursor()
    
    # Get all collections accounts
    cursor.execute("SELECT id, customer_name, address FROM collections_accounts")
    accounts = cursor.fetchall()
    
    print(f"\n🔍 Checking {len(accounts)} collections accounts...")
    
    updated = 0
    for account_id, customer_name, current_addr in accounts:
        # Skip if already has real address
        if current_addr and not any(x in current_addr for x in ['1234 ', '5678 ', '9012 ', 'not on file']):
            continue
        
        # Try to match
        normalized = normalize_name(customer_name)
        
        if normalized in addresses:
            data = addresses[normalized]
            if data['address']:
                cursor.execute("""
                    UPDATE collections_accounts 
                    SET address = ?, phone = ?
                    WHERE id = ?
                """, (data['address'], data['phone'], account_id))
                updated += 1
                print(f"✅ Updated: {customer_name}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Updated {updated} accounts with real addresses")

if __name__ == '__main__':
    import_addresses()
