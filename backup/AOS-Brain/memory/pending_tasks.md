# Pending Tasks - Miles

## ACM Technologies API Integration
**Created:** 2026-05-02 17:51 UTC  
**Updated:** 2026-05-16 05:06 UTC  
**Status:** SOAP Client Rebuilt - Testing Required

### Issue Fixed
❌ **Problem:** Automation sending REST/JSON → API expects SOAP/XML  
✅ **Solution:** Rebuilt client per Jon Scarpa's 2026-05-15 email with proper SOAP structure

### Next Step
Test connectivity with corrected SOAP client:
```
https://secure-send.acmtech.com/note/5U567H575R4G6Z5g5e6T487Y6Q5C6O4i815O626J5i4k636B6W6n7J7B7t7E6q5Q#b4399ab938c0b925ba12558c0b856163746afb4cb1de0308775521c56af136ff
```

### Credentials Status
✅ **Retrieved** - Stored in `/root/.openclaw/workspace/aocros/secrets/acm_api.env`

### Remaining Tasks
- [ ] Test connectivity (test mode)
- [ ] Verify endpoint URL with Jon if needed
- [ ] Test order submission flow
- [ ] Retrieve product catalog
- [ ] Validate with Jon Scarpa
- [ ] Request account activation

### Contacts
- **Jon Scarpa** (IT Manager): Jon.Scarpa@acmtech.com, (951) 738-9898 x222
- **Michael Harrison** (Account Executive): michael.harrison@acmtech.com

### Reference
- Customer #71152
- API Endpoint: https://api.acmtech.com
- Docs: https://api-help.acmtech.com

---

## DNS Records Setup - Hostinger
**Created:** 2026-06-14  
**Status:** PENDING CAPTAIN ACTION

### Subdomains for psdepot.com
| Type | Name | Target | TTL |
|------|------|--------|-----|
| CNAME | cream | psdepot.com | 14400 |
| CNAME | reggiestarr | psdepot.com | 14400 |
| CNAME | dashboard | psdepot.com | 14400 |
| CNAME | depotchaos | psdepot.com | 14400 |

### SendGrid Domain Authentication
| Type | Host | Value |
|------|------|-------|
| CNAME | em8873.psdepot.com | u109143135.wl136.sendgrid.net |
| CNAME | s1._domainkey.psdepot.com | s1.domainkey.u109143135.wl136.sendgrid.net |
| CNAME | s2._domainkey.psdepot.com | s2.domainkey.u109143135.wl136.sendgrid.net |
| TXT | _dmarc.psdepot.com | v=DMARC1; p=none |

**Action Required:** Add these records in Hostinger Dashboard → Domains → psdepot.com → DNS Zone Editor

---

**Daily Check:** Review inbox for credentials from Captain
