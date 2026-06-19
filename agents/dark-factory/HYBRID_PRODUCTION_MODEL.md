# Dark Factory - Hybrid Production Model
## Software Platform + Local Used Printer

**Date:** March 29, 2026  
**Strategy:** Software manages vendors AND local printer  
**Budget:** $200-300 (used printer)  
**Timeline:** 1-2 weeks to production

---

## HYBRID ARCHITECTURE

### Tier 1: Local Production (Used Printer)
- **Equipment:** Used 3D printer ($200-300)
- **Use Case:** Quick-turn, prototypes, rush orders
- **Capacity:** Small volume, fast turnaround
- **Cost:** Low capital, immediate availability

### Tier 2: Vendor Network (Software Platform)
- **Sources:** External fabricators
- **Use Case:** Overflow, large orders, specialized work
- **Capacity:** Unlimited (add vendors)
- **Cost:** Pay per job, no capital

### Tier 3: Strategic Partners
- **Sources:** CNC shops, assembly houses
- **Use Case:** Complex parts, high volume
- **Capacity:** On-demand
- **Cost:** Contract pricing

---

## Local Printer Strategy

### Target: Used Prusa i3 MK3S or MK3
- **Price:** $200-300 (vs $499 new)
- **Source:** eBay, Facebook Marketplace, Reddit (r/3Dprinting)
- **Why:** Reliable, repairable, well-documented
- **Risk:** May need minor repairs

### Alternative: Ender 3 (Creality)
- **Price:** $150-200 used
- **Source:** Same as above
- **Why:** Cheaper, good community support
- **Risk:** More tinkering required

### Local Printer Specs
- **Build Volume:** 220x220x250mm minimum
- **Filament:** 1.75mm PLA/PETG
- **Connectivity:** USB or SD card
- **Software:** OctoPrint on Raspberry Pi

---

## Software Integration

### Job Routing Logic
```python
def route_job(job):
    # Priority 1: Local printer (if available & suitable)
    if local_printer.available and job.fits_local:
        return local_printer.queue(job)
    
    # Priority 2: Quick-turn vendors
    if job.timeline < 3_days:
        return vendor_pool.quick_turn.quote(job)
    
    # Priority 3: Best price vendor
    return vendor_pool.cheapest.quote(job)
```

### Local Printer Management
- **Job Queue:** Local jobs prioritized
- **Maintenance:** Track in software
- **Materials:** Inventory management
- **Cost Tracking:** $/job for local vs vendor

---

## Financial Model

### Capital Investment
| Item | Cost | Source |
|------|------|--------|
| Used Printer | $200-300 | Marketplace |
| Raspberry Pi | $75 | Amazon/Newark |
| Filament (5kg) | $50 | Amazon |
| Total | **$325-425** | |

### Operating Costs
- **Local:** $0.05-0.10/gram (material only)
- **Vendors:** $0.15-0.30/gram (marked up)
- **Software:** $0 (already built)

### Revenue
- **Local jobs:** 50% margin on materials
- **Vendor jobs:** 20-40% markup
- **Break-even:** Month 2-3

---

## Implementation Timeline

### Week 1: Acquire Equipment
- [ ] Search listings (eBay, FB, Reddit)
- [ ] Inspect/test used printer
- [ ] Purchase and ship
- [ ] Order Raspberry Pi + filament

### Week 2: Setup & Integration
- [ ] Install printer
- [ ] Calibrate and test
- [ ] Install OctoPrint on Pi
- [ ] Connect to Dark Factory software
- [ ] Run test jobs

### Week 3: Vendor Recruitment
- [ ] Identify 3-5 local vendors
- [ ] Onboard to platform
- [ ] Test integrations
- [ ] Set pricing

### Week 4: Production Start
- [ ] Accept customer orders
- [ ] Route to local or vendor
- [ ] Track and deliver
- [ ] Scale based on demand

---

## Advantages of Hybrid Model

| Factor | Pure Software | Hybrid (NEW) |
|--------|-------------|--------------|
| Capital | $0 | $325-425 |
| Local Capability | No | Yes |
| Quick Turn | 2-5 days | Same day |
| Quality Control | Vendor-dependent | Direct control |
| IP Protection | Risk | Local = safe |
| Scale | Unlimited | Unlimited + local |
| Risk | Vendor failure | Diversified |

---

## Risk Mitigation

### Used Printer Risks
- **Broken parts:** Prusa has spare parts available
- **Calibration issues:** Well-documented process
- **Downtime:** Vendor backup for critical jobs

### Vendor Risks
- **Quality variance:** Local printer as QC reference
- **Delivery delays:** Local handles rush orders
- **Price increases:** Local provides negotiating leverage

---

## Next Steps

### Immediate (This Week):
1. [ ] Scout used printers (eBay alerts)
2. [ ] Join r/3Dprinting (deals posted)
3. [ ] Check Facebook Marketplace locally
4. [ ] Order Raspberry Pi (lead time)

### Search Criteria:
- **Models:** Prusa i3 MK3/S, Mini, or Ender 3 Pro
- **Condition:** Working or "needs minor repair"
- **Price:** <$300
- **Location:** Prefer local pickup (test before buy)

### Integration:
- Software already supports local + vendor routing
- Just need to add the physical printer
- Dark Factory scheduler will handle allocation

---

## Summary

**Best of both worlds:**
- **Quick turns:** Local printer
- **Scale:** Vendor network
- **Low capital:** Used equipment
- **Fast start:** 1-2 weeks

**Software:** ✅ Complete  
**Local printer:** ⏳ Find used  
**Vendors:** ⏳ Recruit  
**Production:** 🎯 2 weeks

---

**Prepared by:** Miles  
**Date:** 2026-03-29 03:06 UTC  
**Status:** Hybrid model approved, scout for used printer
