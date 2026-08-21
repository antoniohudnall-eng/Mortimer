# Government Data Scraper

Scrape business and entity data from **free public government sources only**. No paid APIs, no commercial services — just open government data.

## Philosophy

**"The information is out there. We just need to collect it."**

- Only official government sources
- No paid subscriptions
- Respect rate limits
- Cache aggressively
- Build once, use forever

---

## Data Sources (All Free)

### California State

| Source | URL | Data Available | Rate Limit |
|--------|-----|----------------|------------|
| **CA SOS Business Search** | https://businesssearch.sos.ca.gov/ | Entity name, number, status, agent, address | 1 req / 3 sec |
| **CA FTB Public Records** | Limited public data | Tax status (public entities only) | Varies |
| **CA Secretary of State FTP** | Bulk data downloads | Full entity database (quarterly dumps) | Unlimited |

### Federal (USA)

| Source | URL | Data Available | API/Scrape |
|--------|-----|----------------|------------|
| **SAM.gov** | https://sam.gov/ | Federal contractors, DUNS, NAICS | Free API |
| **USASpending.gov** | https://www.usaspending.gov/ | Federal grants, contracts, recipients | Free API |
| **SEC EDGAR** | https://www.sec.gov/edgar | Public company filings (10-K, 10-Q) | Free API |
| **IRS Exempt Orgs** | https://apps.irs.gov/app/eos/ | Non-profit 990 filings | Free search |
| **USPTO TESS** | https://tmsearch.uspto.gov/ | Trademark registrations | Free search |
| **Census Business Builder** | https://business.census.gov/ | Business demographic data | Free API |

### Other States (Expandable)

| State | Source | URL |
|-------|--------|-----|
| Delaware | Division of Corporations | https://icis.corp.delaware.gov/ |
| Texas | Secretary of State | https://mycpa.cpa.state.tx.us/coa/ |
| New York | Department of State | https://apps.dos.ny.gov/publicInquiry/ |
| Nevada | Secretary of State | https://esos.nv.gov/ |
| Wyoming | Secretary of State | https://wyobiz.wyo.gov/ |

---

## Scraping Strategy

### Phase 1: CA SOS (Miles Already Built)
**Status:** ✅ Complete  
**Coverage:** 7,496 businesses  
**Blocker:** External API access (but we don't need it)

### Phase 2: Federal Sources (SAM.gov, USASpending)
**Priority:** HIGH  
**Value:** Federal contractors = high-value leads  
**Method:** Free API keys available

### Phase 3: SEC EDGAR (Public Companies)
**Priority:** MEDIUM  
**Value:** Public companies = compliance needs  
**Method:** Free API, bulk downloads available

### Phase 4: State Expansion
**Priority:** LOW  
**Value:** Multi-state coverage  
**Method:** Similar patterns to CA SOS

---

## Implementation

### Python Scraper Template

```python
#!/usr/bin/env python3
"""
Government Data Scraper
Free public sources only — no paid APIs
"""

import requests
import time
import json
from datetime import datetime
from pathlib import Path

class GovDataScraper:
    def __init__(self, cache_dir="./gov_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; GovDataBot/1.0)'
        })
    
    def _cache_path(self, source, identifier):
        """Generate cache file path"""
        return self.cache_dir / f"{source}_{identifier}.json"
    
    def _load_cache(self, source, identifier, max_age_hours=24):
        """Load from cache if fresh"""
        cache_file = self._cache_path(source, identifier)
        if cache_file.exists():
            age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
            if age.total_seconds() < max_age_hours * 3600:
                return json.loads(cache_file.read_text())
        return None
    
    def _save_cache(self, source, identifier, data):
        """Save to cache"""
        cache_file = self._cache_path(source, identifier)
        cache_file.write_text(json.dumps(data, indent=2))
    
    def scrape_ca_sos(self, entity_number=None, search_term=None, max_results=100):
        """
        Scrape CA Secretary of State business data
        Rate limit: 1 request per 3 seconds
        """
        results = []
        
        if entity_number:
            # Direct entity lookup
            cache_key = f"ca_sos_entity_{entity_number}"
            cached = self._load_cache("ca_sos", cache_key)
            if cached:
                return cached
            
            # Scrape entity details
            url = f"https://businesssearch.sos.ca.gov/Document/SearchResults"
            # ... scraping logic here ...
            
            time.sleep(3)  # Rate limit compliance
            
        elif search_term:
            # Search-based scraping
            cache_key = f"ca_sos_search_{search_term.replace(' ', '_')}"
            cached = self._load_cache("ca_sos", cache_key)
            if cached:
                return cached
            
            # Scrape search results
            # ... scraping logic ...
            
            time.sleep(3)  # Rate limit compliance
        
        return results
    
    def scrape_sam_gov(self, naics_code=None, state=None, max_results=1000):
        """
        Scrape SAM.gov federal contractors
        FREE API — registration required
        Rate limit: 1000 requests/day
        """
        cache_key = f"sam_gov_{naics_code or 'all'}_{state or 'all'}"
        cached = self._load_cache("sam_gov", cache_key, max_age_hours=168)  # Weekly refresh
        if cached:
            return cached
        
        # SAM.gov API endpoint
        api_key = "YOUR_SAM_GOV_API_KEY"  # Free registration
        url = "https://api.sam.gov/prod/opportunities/v1/search"
        
        params = {
            'api_key': api_key,
            'limit': min(max_results, 1000),
        }
        
        if naics_code:
            params['naicsCode'] = naics_code
        if state:
            params['state'] = state
        
        # ... API call logic ...
        
        return []
    
    def scrape_usaspending(self, recipient_name=None, state=None, max_results=1000):
        """
        Scrape USASpending.gov federal grants/contracts
        FREE API — no key required
        Rate limit: 1000 requests/hour
        """
        cache_key = f"usaspending_{recipient_name or 'all'}_{state or 'all'}"
        cached = self._load_cache("usaspending", cache_key, max_age_hours=24)
        if cached:
            return cached
        
        # USASpending API
        url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
        
        payload = {
            'filters': {
                'award_type_codes': ['A', 'B', 'C', 'D'],  # Contracts, grants, etc.
            },
            'fields': ['Award ID', 'Recipient Name', 'Start Date', 'End Date', 'Award Amount', 'Awarding Agency', 'Awarding Sub Agency', 'Contract Award Type', 'Funding Agency', 'Funding Sub Agency'],
            'sort': 'Award Amount',
            'order': 'desc',
            'limit': min(max_results, 100)
        }
        
        if recipient_name:
            payload['filters']['recipient_name'] = recipient_name
        if state:
            payload['filters']['place_of_performance_locations'] = [{'country': 'USA', 'state': state}]
        
        # ... API call logic ...
        
        return []
    
    def enrich_leads(self, leads_json):
        """
        Enrich lead data with multiple government sources
        """
        with open(leads_json) as f:
            leads = json.load(f)
        
        enriched = []
        for lead in leads:
            # Try CA SOS first
            if 'entity_number' in lead:
                ca_data = self.scrape_ca_sos(entity_number=lead['entity_number'])
                lead['ca_sos'] = ca_data
            
            # Try SAM.gov for federal contractors
            if 'naics' in lead:
                sam_data = self.scrape_sam_gov(naics_code=lead['naics'])
                lead['sam_gov'] = sam_data
            
            enriched.append(lead)
            time.sleep(1)  # Be nice to servers
        
        return enriched

# Usage example
if __name__ == "__main__":
    scraper = GovDataScraper()
    
    # Scrape CA businesses
    results = scraper.scrape_ca_sos(search_term="TECH", max_results=50)
    
    # Scrape federal contractors
    contractors = scraper.scrape_sam_gov(state="CA", max_results=100)
    
    # Enrich existing leads
    enriched = scraper.enrich_leads("./leads.json")
    
    print(f"Scraped {len(results)} CA entities")
    print(f"Found {len(contractors)} federal contractors")
    print(f"Enriched {len(enriched)} leads")
```

---

## References

- [CA SOS Business Search](https://businesssearch.sos.ca.gov/)
- [SAM.gov API](https://sam.gov/)
- [USASpending API](https://api.usaspending.gov/)
- [SEC EDGAR](https://www.sec.gov/edgar)
- [IRS Exempt Orgs](https://www.irs.gov/charities-non-profits)

---

**Classification:** PUBLIC — Free Government Data Only  
**Cost:** $0  
**Ethics:** Only scrape public data, respect rate limits  
**Mandate:** NO PAID APIs — The information is out there
