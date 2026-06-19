# CURRENT_TASKS.md - Dusty
**Assigned:** 2026-03-28 20:21 UTC
**Priority:** HIGH
**Status:** ACTIVE

---

## Task: Lead Enrichment - Website & Email Research

### Objective
Enrich existing lead database with website URLs and email addresses for all businesses across 58 counties in CA, OR, WA, TX, AZ, NM.

### Background
We have lead files for 58+ counties but they're missing critical contact information:
- ❌ Website URLs
- ❌ Email addresses
- ❌ Social media profiles (bonus)

### Scope

**Files to Process:**
Located in: `/root/.openclaw/workspace/aocros/performance_supply_depot/leads/`

**Priority States (in order):**
1. **California** - 58 counties (CA_* files)
2. **Oregon** - 36 counties (OR_*, Baker_* files)
3. **Washington** - 39 counties (WA_*, *_WA_* files)
4. **Texas** - 254 counties (TX_* files)
5. **Arizona** - 15 counties (AZ_* files) - NEW
6. **New Mexico** - 33 counties (NM_* files) - NEW

**Key Files:**
- `CA_All_58_Counties_Leads.xlsx` (master file - start here)
- `ALL_STATES_Leads.xlsx` (consolidated)
- Individual county files

### Process

For each business in the lead files:

1. **Extract Business Info**
   - Business Name
   - Address
   - Phone Number (if available)
   - County/State

2. **Research Website**
   - Google search: "Business Name + City + website"
   - Check Yelp, Yellow Pages, Chamber of Commerce
   - Verify URL is active (HTTP 200 check)

3. **Find Email Address**
   - Check website "Contact" or "About" pages
   - Look for info@, contact@, sales@ patterns
   - Use Hunter.io or similar tools (if API available)
   - Check LinkedIn company pages

4. **Update Lead Sheet**
   - Add "Website" column
   - Add "Email" column
   - Add "Email_Source" column (where found)
   - Add "Last_Updated" timestamp

5. **Mark Status**
   - ✅ Complete: Website + Email found
   - ⚠️ Partial: Website OR Email found
   - ❌ No Contact: Neither found

### Output Format

Update each Excel file with new columns:
```
Business_Name | Address | Phone | Website | Email | Email_Source | Status | Last_Updated
```

### Tools to Use

1. **Web Search**
   - `browser-exchange-agent` skill for website lookup
   - Google search automation
   - DuckDuckGo API (privacy-focused)

2. **Email Discovery**
   - Website scraping for contact pages
   - Pattern matching (info@, contact@, etc.)
   - Verify email format with regex

3. **Data Processing**
   - Python pandas for Excel manipulation
   - OpenPyXL for reading/writing .xlsx files
   - CSV export for backup

### Batch Processing

Process in batches of 100 businesses:
1. Load 100 records from Excel
2. Research each one
3. Update spreadsheet
4. Save backup copy
5. Report progress

### Expected Volume

| State | Counties | Est. Businesses | Timeline |
|-------|----------|-------------------|----------|
| CA | 58 | ~5,800 | Week 1-2 |
| OR | 36 | ~3,600 | Week 3 |
| WA | 39 | ~3,900 | Week 4 |
| TX | 254 | ~25,400 | Week 5-8 |
| AZ | 15 | ~1,500 | Week 9 |
| NM | 33 | ~3,300 | Week 10 |
| **TOTAL** | **~435** | **~43,500** | **~10 weeks** |

### Success Metrics

- **Target:** 70% of businesses have website found
- **Target:** 50% of businesses have email found
- **Minimum:** Update ALL records with status

### Reporting

Daily reports to Miles:
- Businesses processed: X
- Websites found: X (X%)
- Emails found: X (X%)
- File(s) updated: [list]
- Blockers/issues: [if any]

### Scripts

Create helper scripts:
1. `enrich_leads.py` - Main processing script
2. `website_finder.py` - Find business websites
3. `email_extractor.py` - Extract emails from websites
4. `progress_tracker.py` - Track completion rates

### Integration with Marketing

Once enriched:
- Export to CRM (HubSpot/Salesforce)
- Load into email marketing platform
- Assign to sales team by territory
- Track outreach success rates

---

## Immediate Actions

1. **TODAY:**
   - [ ] Examine `CA_All_58_Counties_Leads.xlsx` structure
   - [ ] Sample 10 businesses for test run
   - [ ] Verify enrichment process works

2. **THIS WEEK:**
   - [ ] Process California counties (priority)
   - [ ] Complete ~1,000 businesses
   - [ ] Report initial success rates

3. **ONGOING:**
   - [ ] Batch process remaining states
   - [ ] Weekly progress reports
   - [ ] Quality assurance spot checks

---

## Resources

**Lead Files Location:**
```
/root/.openclaw/workspace/aocros/performance_supply_depot/leads/
```

**Skills Available:**
- browser-exchange-agent (web scraping)
- gov-data-scraper (public records)
- enrichment-program (data enhancement)

**Support:**
- Jordan: Project coordination
- Miles: Strategic oversight
- Pulp: Marketing integration

---

## Notes

- **Privacy:** Only collect publicly available information
- **Rate Limiting:** Don't overwhelm websites with requests
- **Verification:** Spot-check emails for validity
- **Backup:** Save copies before modifying originals
- **Duplicates:** Check for duplicate businesses across counties

---

**Start Date:** 2026-03-28
**Estimated Completion:** 2026-06-06 (10 weeks)
**Status:** ⏳ Ready to begin

---

*This is a critical task for marketing outreach. Quality over speed - accurate data is more valuable than fast but wrong data.*
