# COBRA-MIDI Bill of Materials

**Scale:** 1:2 (90cm tall)  
**Total Parts:** ~200 components  
**Est. Cost:** $650-800 USD  
**Print Time:** 120+ hours  

---

## SPINE COMPONENTS

### Vertebrae (25 units)

| Part | Qty | Material | Est. Cost | Print Time |
|------|-----|----------|-----------|------------|
| C1-C7 (Cervical) | 7 | PETG CF | $14 | 7h |
| T1-T12 (Thoracic) | 12 | PETG CF | $36 | 18h |
| L1-L5 (Lumbar) | 5 | PETG CF | $20 | 10h |
| S1 (Sacrum + Brain) | 1 | PETG CF | $8 | 4h |
| **Spine Subtotal** | **25** | | **$78** | **39h** |

**Filament Required:** 800g PETG Carbon Fiber ($45/kg)

### Spine Hardware

| Item | Qty | Spec | Cost | Notes |
|------|-----|------|------|-------|
| 2mm steel pins | 48 | SS304, 25mm | $12 | Joint pivots |
| 4mm steel pins | 24 | SS304, 40mm | $15 | Main pivots |
| 608RS bearings | 24 | 8x22x7mm | $24 | Joint bearings |
| Joint gimbals | 24 | Printed | $12 | 12h print |
| **Hardware Subtotal** | | | **$63** | |

---

## POWER SYSTEM

### Batteries (17 vertebrae with cells)

| Cell Type | Qty | Spec | Cost | Total |
|-----------|-----|------|------|-------|
| 18650 Li-ion | 34 | 3.7V, 3000mAh, protected | $5 | $170 |
| BMS modules | 17 | 2S protection, 5A | $3 | $51 |
| **Battery Subtotal** | | | | **$221** |

### Solar System

| Item | Qty | Spec | Cost |
|------|-----|------|------|
| Solar cells 60x40mm | 12 | 6V, 100mA | $48 |
| MPPT controller | 1 | CN3791, 6V in, 4.2V out | $12 |
| Diode 1N5819 | 12 | Schottky | $2 |
| **Solar Subtotal** | | | **$62** |

### Power Distribution

| Item | Qty | Spec | Cost |
|------|-----|------|------|
| DC-DC buck 12V->5V | 1 | 5A, 25W | $8 |
| DC-DC buck 12V->3.3V | 1 | 2A | $4 |
| XT60 connectors | 6 | Panel mount | $6 |
| 16AWG silicone wire | 5m | Red/black | $8 |
| 22AWG silicone wire | 20m | Various colors | $12 |
| **Distribution Subtotal** | | | **$38** |

---

## ACTUATION

### Servos (Spine)

| Servo Type | Qty | Spec | Cost | Notes |
|------------|-----|------|------|-------|
| MG90S metal gear | 24 | 2.2kg·cm, 0.1s/60° | $4 | Spine joints |
| DS3218 digital | 10 | 20kg·cm, 0.15s/60° | $12 | High torque |
| **Servo Subtotal** | **34** | | **$216** | |

### Tendon System (Hands)

| Item | Qty | Spec | Cost |
|------|-----|------|------|
| Dyneema braided 80lb | 20m | 0.3mm | $25 |
| 9g micro servos | 10 | For fingers | $30 |
| PTFE tubing 2.5mm ID | 10m | Tendon guide | $15 |
| Pulleys 10mm brass | 30 | 2mm bore | $18 |
| Return springs | 10 | 10mm x 1mm | $5 |
| **Tendon Subtotal** | | | **$93** |

---

## ELECTRONICS

### Main Compute

| Item | Qty | Spec | Cost |
|------|-----|------|------|
| Raspberry Pi 5 | 1 | 8GB RAM | $80 |
| Active cooler | 1 | Pi 5 official | $5 |
| AI HAT+ | 1 | 13 TOPS | $70 |
| MicroSD 128GB | 1 | Class 10 | $15 |
| **Compute Subtotal** | | | **$170** |

### Distributed Controllers

| Item | Qty | Spec | Cost |
|------|-----|------|------|
| STM32F103 | 25 | Vertebra nodes | $50 |
| MCP2515 CAN modules | 25 | SPI CAN bus | $40 |
| IMU MPU6050 | 25 | Per vertebra | $75 |
| **Node Subtotal** | | | **$165** |

### Wiring & Connectors

| Item | Qty | Spec | Cost |
|------|-----|------|------|
| JST-XH 2.54mm kit | 1 | Assorted connectors | $25 |
| Dupont wire kit | 1 | Male/female jumpers | $12 |
| Ribbon cable 20P | 10m | For CAN bus | $15 |
| **Wiring Subtotal** | | | **$52** |

---

## BODY COMPONENTS

### Hands

| Part | Qty | Material | Cost | Time |
|------|-----|----------|------|------|
| Finger segments | 30 | TPU 95A | $12 | 6h |
| Palm left | 1 | PETG | $3 | 3h |
| Palm right | 1 | PETG | $3 | 3h |
| Wrist joints | 2 | PETG | $2 | 1h |
| **Hands Subtotal** | | | **$20** | **13h** |

### Arms & Legs (Optional)

| Part | Qty | Material | Cost | Time |
|------|-----|----------|------|------|
| Upper arm | 2 | PETG CF | $8 | 4h |
| Forearm | 2 | PETG CF | $6 | 3h |
| Thigh | 2 | PETG CF | $10 | 5h |
| Shin | 2 | PETG CF | $8 | 4h |
| **Limbs Subtotal** | | | **$32** | **16h** |

---

## FASTENERS & MISC

| Item | Qty | Spec | Cost |
|------|-----|------|------|
| M2x6 screws | 100 | Button head | $8 |
| M2x10 screws | 50 | Button head | $4 |
| M3x8 screws | 100 | Socket head | $12 |
| M3x12 screws | 50 | Socket head | $8 |
| M3 nuts | 150 | Hex | $5 |
| M3 washers | 200 | Stainless | $6 |
| M4x10 screws | 50 | Socket head | $10 |
| Threadlocker | 1 | Loctite blue | $8 |
| **Fastener Subtotal** | | | **$61** |

---

## SUMMARY

### Cost Breakdown

| Category | Cost | % of Total |
|----------|------|------------|
| Power (Batteries + Solar) | $321 | 40% |
| Actuation (Servos + Tendons) | $309 | 38% |
| Electronics (Compute + Nodes) | $387 | 48% |
| Spinal Structure | $141 | 18% |
| Hands & Body | $52 | 6% |
| Fasteners & Misc | $61 | 8% |
| **TOTAL** | **~$800** | |

*Note: Electronics cost can be reduced with custom PCB fabrication*

### Print Time Breakdown

| Category | Hours | % of Total |
|----------|-------|------------|
| Spine vertebrae | 39h | 33% |
| Joint gimbals | 12h | 10% |
| Hands | 13h | 11% |
| Limbs (optional) | 16h | 13% |
| Electronics housings | 20h | 17% |
| Mounts & brackets | 20h | 17% |
| **TOTAL** | **~120h** | |

*At 50mm/s print speed, 0.2mm layer height*

### Tools Required

- 3D printer (250x250x250mm minimum build volume)
- Soldering iron + flux
- Multimeter
- Crimping tool (JST connectors)
- Calipers
- Hex key set (M2, M3, M4)

### Suppliers

| Item | Recommended Source |
|------|------------------|
| 18650 cells | LG MJ1 (LiionWholesale) |
| Servos | TowerPro / Feetech (AliExpress) |
| Solar cells | MiniSolar (Amazon) |
| PETG CF | eSun, Prusament |
| Bearings | VXB, Amazon |
| Electronics | DigiKey, Mouser |

---

**Document Version:** 1.0  
**Last Updated:** 2026-03-29 04:11 UTC
