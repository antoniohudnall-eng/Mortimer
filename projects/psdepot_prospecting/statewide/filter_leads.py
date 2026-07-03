#!/usr/bin/env python3
"""
PSDEPOT Lead Database - Filter & Cross-Reference
- Remove corporate chains
- Cross-reference with DepotChaos
- Flag duplicates
"""

import csv
import os
import re
from datetime import datetime

# Paths
LEADS_FILE = '/data/data/com.termux/files/home/mortimer/projects/psdepot_prospecting/data/psdepot_leads_latest.csv'
DEPOT_FILE = '/data/data/com.termux/files/home/mortimer/projects/psdepot_prospecting/depotchaos_names.txt'
EXCLUSION_FILE = '/data/data/com.termux/files/home/mortimer/projects/psdepot_prospecting/statewide/exclusion_patterns.txt'
OUTPUT_DIR = '/data/data/com.termux/files/home/mortimer/projects/psdepot_prospecting/statewide'

# Load exclusion patterns
def load_exclusions():
    patterns = []
    with open(EXCLUSION_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                patterns.append(line.lower())
    return patterns

# Load DepotChaos names
def load_depot_chaos():
    names = set()
    with open(DEPOT_FILE, 'r') as f:
        for line in f:
            names.add(line.strip().lower())
    return names

# Check if business is a chain
def is_chain(name, patterns):
    name_lower = name.lower()
    for pattern in patterns:
        if pattern in name_lower:
            return True
    return False

# Check if in DepotChaos
def in_depot_chaos(name, depot_names):
    name_lower = name.lower().strip()
    return name_lower in depot_names

# Main filter
def filter_leads():
    print("="*60)
    print("PSDEPOT Lead Filter & Cross-Reference")
    print("="*60)
    
    # Load data
    exclusions = load_exclusions()
    depot_names = load_depot_chaos()
    
    print(f"Loaded {len(exclusions)} exclusion patterns")
    print(f"Loaded {len(depot_names)} DepotChaos names")
    
    # Read leads
    leads = []
    with open(LEADS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        leads = list(reader)
    
    print(f"Total leads: {len(leads)}")
    
    # Categorize
    private = []
    chains = []
    depot_dupes = []
    
    for lead in leads:
        name = lead.get('name', '')
        
        # Check if chain
        if is_chain(name, exclusions):
            chains.append(lead)
        else:
            # Check DepotChaos
            if in_depot_chaos(name, depot_names):
                lead['depotchaos_status'] = 'DUPLICATE'
                depot_dupes.append(lead)
            else:
                lead['depotchaos_status'] = 'NEW'
            private.append(lead)
    
    print(f"\nResults:")
    print(f"  Private/Owner-operated: {len(private)}")
    print(f"  Corporate chains (EXCLUDED): {len(chains)}")
    print(f"  Already in DepotChaos: {len(depot_dupes)}")
    print(f"  New leads: {len([l for l in private if l['depotchaos_status'] == 'NEW'])}")
    
    # Show chain names
    if chains:
        print(f"\n--- Chains Found ({len(chains)}) ---")
        chain_names = set([c.get('name', '') for c in chains])
        for name in sorted(chain_names)[:20]:
            print(f"  EXCLUDED: {name}")
        if len(chain_names) > 20:
            print(f"  ... and {len(chain_names) - 20} more")
    
    # Save filtered leads
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Save all filtered
    with open(f'{OUTPUT_DIR}/private_leads.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = list(private[0].keys()) if private else []
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(private)
    
    # Save chains
    if chains:
        with open(f'{OUTPUT_DIR}/excluded_chains.csv', 'w', newline='', encoding='utf-8') as f:
            fieldnames = list(chains[0].keys()) if chains else []
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(chains)
    
    print(f"\n[+] Saved private leads: {OUTPUT_DIR}/private_leads.csv")
    if chains:
        print(f"[+] Saved chains: {OUTPUT_DIR}/excluded_chains.csv")
    
    return private, chains, depot_dupes


if __name__ == '__main__':
    filter_leads()
