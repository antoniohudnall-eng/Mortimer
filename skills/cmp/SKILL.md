# AGI CMP - Consent Management Platform

**Version:** 1.0.0  
**Location:** `/root/.openclaw/workspace/AGI_COMPANY/products/cmp/`  
**Type:** Product/Tool

---

## Overview

A custom-built Consent Management Platform (CMP) for GDPR, CCPA, and privacy law compliance. Similar features to Cookiebot and Usercentrics, but fully owned and customizable.

---

## Features

### Frontend
- ✅ **5 Consent Categories**: Essential, Functional, Analytics, Marketing, Social
- ✅ **Script Blocking**: Prevents execution of tracking scripts until consent
- ✅ **Google Consent Mode v2**: Native integration with GTM
- ✅ **IAB TCF 2.2 Inspired**: Structure aligned with industry standards
- ✅ **Responsive UI**: Works on mobile and desktop
- ✅ **Granular Controls**: Accept All, Reject All, or customize preferences

### Backend
- ✅ **Consent Recording**: Stores consent decisions with audit trail
- ✅ **GDPR Rights**: Withdraw consent, data export, data portability
- ✅ **Hashed IPs**: Privacy-preserving IP storage for audit
- ✅ **Statistics**: Aggregate consent metrics
- ✅ **FastAPI**: Modern Python backend

---

## Quick Start

### 1. Add to Your Website

```html
<!-- Load CMP FIRST, before any tracking scripts -->
<script src="/path/to/agi-cmp.js"></script>

<!-- Blocked script example -->
<script type="text/plain" data-agi-category="analytics">
  // Google Analytics won't execute until consent given
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### 2. Configure Google Tag Manager

```javascript
// Default deny until user choice
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
  'consent': {
    'ad_storage': 'denied',
    'analytics_storage': 'denied',
    'functionality_storage': 'denied',
    'personalization_storage': 'denied',
    'security_storage': 'granted',
    'ad_user_data': 'denied',
    'ad_personalization': 'denied'
  }
});
```

### 3. Run Backend

```bash
cd /root/.openclaw/workspace/AGI_COMPANY/products/cmp/api
pip install fastapi uvicorn
uvicorn consent_api:app --host 0.0.0.0 --port 8083
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/consent` | POST | Record new consent |
| `/api/consent/{id}` | GET | Retrieve consent record |
| `/api/consent/{id}/withdraw` | POST | Withdraw consent |
| `/api/consent/stats/summary` | GET | Aggregate statistics |
| `/api/consent/export/{id}` | GET | GDPR data export |
| `/health` | GET | Health check |

---

## JavaScript API

```javascript
// Check if user has consented to analytics
if (window.__agi_cmp.hasConsent('analytics')) {
  // Load analytics
}

// Get all consents
const consent = window.__agi_cmp.getConsent();

// Listen for consent changes
window.__agi_cmp.on('consent', (consent) => {
  console.log('User updated consent:', consent);
});

// Reset consent (for testing)
window.__agi_cmp.reset();

// Open settings modal
window.__agi_cmp.openSettings();
```

---

## Script Categories

| Category | Required | Common Cookies | Vendors |
|----------|----------|----------------|---------|
| Essential | ✅ Yes | session, csrf, auth | Internal |
| Functional | ❌ No | preferences, language | - |
| Analytics | ❌ No | _ga, _gid | Google Analytics, Plausible |
| Marketing | ❌ No | _fbp, _gcl_au | Facebook Pixel, Google Ads |
| Social | ❌ No | fb_cookie | Facebook SDK, Twitter |

---

## Files

- `agi-cmp.js` - Frontend consent manager
- `api/consent_api.py` - Backend FastAPI server
- `integration.html` - Example integration page

---

## Compliance Features

### GDPR
- ✅ Lawful basis tracking
- ✅ Right to withdraw
- ✅ Data portability export
- ✅ Audit trail
- ✅ Consent timestamp/version

### CCPA
- ✅ Opt-out tracking
- ✅ Do Not Sell flag support
- ✅ Disclosure records

---

## Comparison with Commercial CMPs

| Feature | AGI CMP | Cookiebot | Usercentrics |
|---------|---------|-----------|--------------|
| Cost | Free | €39-79/mo | €30-100/mo |
| Customizable | ✅ Full | Limited | Limited |
| Data Ownership | ✅ You | Third-party | Third-party |
| Google Consent Mode | ✅ v2 | ✅ v2 | ✅ v2 |
| IAB TCF | Inspired | ✅ Full | ✅ Full |
| Script Blocking | ✅ Yes | ✅ Yes | ✅ Yes |

---

## Next Steps

- [ ] Add IAB TCF 2.2 full compliance (vendor list API)
- [ ] Implement CCPA "Do Not Sell My Info" link
- [ ] Add geo-detection for jurisdiction-specific banners
- [ ] Create WordPress/Drupal plugins
- [ ] Add more analytics integrations
- [ ] Implement automated cookie scanner

---

*Created: 2026-07-04*