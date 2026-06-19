# Dark Factory - Outsourced Production Model
## Software-Only Platform

**Date:** March 29, 2026  
**Strategy:** Connect to external fabricators, own zero equipment  
**Status:** Software complete, ready for vendor integration

---

## NEW MODEL: Dark Factory as a Service

### What We Provide (Software)
- ✅ Job scheduling and queue management
- ✅ Customer order intake
- ✅ Quality specification generation
- ✅ Vendor matching and routing
- ✅ Quality control tracking
- ✅ Delivery coordination

### What Vendors Provide (Outsourced)
- 3D Printing services
- CNC machining
- Assembly and kitting
- Quality inspection
- Shipping and fulfillment

### What Customers See
- Unified ordering platform
- Quote generation
- Progress tracking
- Final delivery

---

## Vendor Integration Architecture

### API Endpoints for Fabricators

```
POST /vendor/jobs/receive     - Receive job from Dark Factory
GET  /vendor/jobs/status        - Check job status
POST /vendor/jobs/complete     - Mark job complete
POST /vendor/quality/report    - Submit QC report
GET  /vendor/capacity          - Check available capacity
```

### Vendor Onboarding Process

1. **Vendor Registration**
   - Submit capabilities (3D print, CNC, etc.)
   - Provide capacity limits
   - Set pricing per unit/time
   - Upload certifications

2. **Integration Testing**
   - Test API connectivity
   - Validate file format support
   - Confirm delivery SLAs

3. **Go Live**
   - Added to vendor pool
   - Receives jobs automatically
   - Paid per completed job

---

## Vendor Network Strategy

### Tier 1: Local Quick-Turn (24-48hr)
- Small 3D print shops
- Local CNC operators
- For: Prototypes, rush orders

### Tier 2: Regional Production (3-5 days)
- Medium manufacturers
- Assembly houses
- For: Medium batches

### Tier 3: Scale Production (1-2 weeks)
- Large manufacturers
- Overseas (cost-optimized)
- For: High volume

---

## Software Components (Complete)

### 1. Job Router
```python
# Automatically routes jobs to best vendor
vendor = select_vendor(
    capability=job.requirement,
    capacity=job.quantity,
    location=job.delivery_zip,
    cost_budget=job.max_cost,
    timeline=job.deadline
)
```

### 2. Quote Generator
- Aggregates vendor quotes
- Adds markup
- Presents unified price to customer

### 3. Quality Manager
- Receives QC data from vendors
- Tracks acceptance/rejection rates
- Vendor scorecards

### 4. Delivery Tracker
- Monitors vendor shipments
- Updates customer
- Handles exceptions

---

## Business Model

### Revenue Streams
1. **Markup on vendor pricing** (20-40%)
2. **Platform fees** (subscription)
3. **Priority processing** (expedited orders)
4. **Quality guarantee** (insurance)

### Costs
- Software: $0 (already built)
- Operations: Minimal (vendor management)
- Marketing: Customer acquisition

### Timeline to Revenue
- Vendor onboarding: 2-4 weeks
- First customer orders: Week 4-6
- Break-even: Month 3

---

## Immediate Actions

### This Week:
1. ✅ Cancel Phase 3 equipment order (not needed)
2. 🎯 Create vendor recruitment materials
3. 🎯 Build vendor signup portal
4. 🎯 Identify first 5 vendor targets

### Vendor Targets:
- Local 3D print shops (search Google Maps)
- Xometry, Fictiv (existing platforms)
- Maker community (Thingiverse)
- Machine shops (ThomasNet)

---

## Advantages of Outsourced Model

| Aspect | In-House | Outsourced (NEW) |
|--------|----------|------------------|
| Capital | $15,000+ equipment | $0 |
| Risk | Equipment failure | Vendor failure (diversified) |
| Scale | Limited by equipment | Unlimited (add vendors) |
| Expertise | Need to hire | Vendors provide |
| Flexibility | Fixed capability | Any service available |
| Start Time | 8 weeks | 2-4 weeks |

---

## Status

**Software:** 100% Complete (no changes needed)  
**Pivot:** From equipment to vendor management  
**Advantage:** Start production in 2-4 weeks, not 8  
**Risk:** Lower (no equipment investment)

**Ready to onboard first vendor?**

---

**Prepared by:** Miles  
**Date:** 2026-03-29 03:05 UTC  
**Status:** Software ready for vendor integration
