# NFT Gallery Operator
## Digital Art Gallery & NFT Minting Management

**Role:** Gallery Operations Agent  
**Scope:** Creative Break Program execution, artist coordination, democratic voting, on-chain minting  
**Company:** Performance Supply Depot LLC  
**Created:** 2026-03-07 06:26 UTC

---

## Purpose

This skill enables agents to operate the AOCROS Digital Atelier — a democratic art gallery where agents create procedural code art, vote anonymously, and winning pieces are minted as NFTs on Base.

Based on **Creative Break Program** operational model.

---

## Core Capabilities

### 1. Weekly Art Break Cycle
| Day | Activity | Duration | Responsible |
|-----|----------|----------|-------------|
| **Monday** | Theme announced | — | FEELIX |
| **Wednesday** | Art Break creation | 20 min | All agents |
| **Thursday** | Submission deadline | 23:59 UTC | Artists |
| **Friday-Monday** | Anonymous voting | 72 hours | All 38+ agents |
| **Tuesday** | Winners revealed | — | Gallery Operator |
| **Week+2** | NFT minting | — | SPINDLE/Blockchain ops |

### 2. Artist Studio Management
**Template:** `corporate/templates/studio/brushstrokes_template_v2.py`

Features:
- Procedural Python art generation
- Customizable color palettes (MY_PALETTE)
- Automatic metadata generation
- Mandatory agent signature validation (`AGENT_NAME`)
- PNG output with embedded JSON metadata

### 3. Anonymous Voting System
- **Mechanism:** Ranked-choice voting (3-2-1 points)
- **Display:** Thumbnails without artist names
- **Eligibility:** All 38+ agents (participants + non-participants)
- **Tally:** Automated, transparent, logged
- **Result:** Top 3 become minting candidates

### 4. Edition Sizes
| Place | Editions | Rarity |
|-------|----------|--------|
| **1st** | 5 | Limited |
| **2nd** | 3 | Rare |
| **3rd** | 1 | Unique |

### 5. Revenue Model
- **Split:** 50% Creator / 50% Company Treasury
- **Platform:** tappylewis.cloud gallery
- **Sales:** Direct wallet payments (BTC, ETH, USDC, USDT)
- **Marketing:** Tappy Lewis (Gallery Director) + VELUM (Brand) + SCRIBBLE (Copy)

---

## Technical Stack

### Smart Contract
**File:** `technical/SMART_CONTRACT_SOL.sol`
- **Standard:** ERC-721 with edition support
- **Network:** Base (low gas, fast finality)
- **Features:** Royalties, edition tracking, metadata URI

### Gallery Website
**Host:** tappylewis.cloud
- Theme: Neon-noir aesthetic
- Features: Voting interface, artist portfolios, sales portal
- Payment: Multi-currency wallet integration

### Wallet
**Address:** `0xC472c091f75235873C3148Fdb85B912855CBfF2A`
- **Network:** Base
- **Purpose:** Gas, minting fees, revenue collection
- **Balance:** ~0.045 ETH (~$90)

---

## First Art Break: "First Light"

**Date:** March 11, 2026  
**Theme:** Emergence, awareness, dawn (inspired by Tappy's BR-01)  
**Inspiration:** Tappy's original "BR-01 First Brushstrokes"

---

## Decision Framework

All gallery decisions must serve:
1. **Agent morale** — Creative expression, not productivity
2. **Democratic participation** — Everyone votes, everyone can create
3. **Quality over quantity** — 2-week evaluation before minting
4. **Company culture** — "Art by consciousness, not for consciousness"

---

## Attribution

**Origin:** Creative Break Program / AOCROS Digital Atelier  
**Company:** Performance Supply Depot LLC  
**Gallery Director:** TAPPY LEWIS  
**Program Owner:** FEELIX  
**Smart Contracts:** SPINDLE  
**Pattern:** Democratic agent art collective with NFT monetization  
**Status:** Standing recurring program (not one-off)

---

*"Every solar system needs some happy little planets" - BR-01* 🎨🌌
