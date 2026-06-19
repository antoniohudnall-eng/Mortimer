# TASK: Dusty Wallet APK — Assigned to Software Team
**Created:** 2026-03-16 16:57 UTC  
**Assigned to:** Spindle (CTO), Pipeline (Backend), TapTap (Android), BugCatcher (QA)  
**Priority:** HIGH  
**Source:** Captain's request  
**Review by:** Captain upon completion

---

## Overview
Build Dusty Wallet — an Android APK for cryptocurrency consolidation across multiple chains. Simple, secure, focused on portfolio management.

---

## Team Assignment

| Role | Assignee | Responsibility |
|------|----------|----------------|
| **Project Lead** | Spindle (CTO) | Architecture, Android project setup, review |
| **Backend** | Pipeline | API endpoints, wallet sync, transaction history |
| **Android Dev** | TapTap | UI/UX, wallet functionality, APK build |
| **QA/Security** | BugCatcher | Testing, security audit, penetration testing |

---

## Requirements

### Supported Cryptocurrencies (8)
- Bitcoin (BTC)
- Ethereum (ETH)
- Solana (SOL)
- Cardano (ADA)
- Polkadot (DOT)
- Chainlink (LINK)
- Polygon (MATIC)
- Avalanche (AVAX)

### Core Features
1. **Portfolio Dashboard**
   - Balance overview (total + per asset)
   - Price charts (24h, 7d, 30d)
   - Portfolio allocation pie chart
   - P&L tracking

2. **Send/Receive**
   - QR code generation for receiving
   - QR scanner for sending
   - Address book (save frequent contacts)
   - Transaction fee estimation

3. **Transaction History**
   - Full tx history per asset
   - Filter by date/asset/type
   - Export to CSV

4. **Security**
   - 🔐 **Encrypted private key storage** (Android Keystore + AES-256)
   - 🔐 **Biometric authentication** (fingerprint/face unlock)
   - 🔐 **Backup/recovery phrase** (BIP-39 mnemonic)
   - 🔐 **PIN/password protection** (6-digit PIN + optional password)

### Technical Specs
- **Platform:** Android 8.0+ (API 26+)
- **Language:** Kotlin (preferred) or Java
- **Architecture:** MVVM or MVI
- **UI:** Jetpack Compose (preferred) or XML layouts
- **Dependencies:**
  - Room (database)
  - Retrofit/OkHttp (API calls)
  - Kotlin Coroutines (async)
  - MPAndroidChart (charts)
  - ZXing (QR codes)
  - BouncyCastle (crypto operations)

### Project Structure
```
dusty/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/aocros/dusty/
│   │   │   │   ├── ui/              # Activities/Fragments/Compose
│   │   │   │   ├── viewmodel/       # ViewModels
│   │   │   │   ├── repository/      # Data repositories
│   │   │   │   ├── database/        # Room entities/DAOs
│   │   │   │   ├── network/         # API interfaces
│   │   │   │   ├── security/        # Encryption, Keystore
│   │   │   │   ├── wallet/          # Wallet logic (BIP-39/44)
│   │   │   │   └── utils/           # Helpers
│   │   │   └── res/                 # Layouts, strings, themes
│   │   └── test/                    # Unit tests
│   ├── build.gradle                 # App-level Gradle
│   └── AndroidManifest.xml
├── backend/                         # Pipeline's API
│   ├── src/
│   │   ├── routes/
│   │   ├── models/
│   │   └── services/
│   └── requirements.txt
├── docs/
│   ├── setup.md
│   ├── security.md
│   └── api.md
├── build/
│   └── releases/                    # APK output
└── README.md
```

---

## Backend API (Pipeline)

### Endpoints Required
```
GET  /api/v1/prices                    # Current prices for all assets
GET  /api/v1/prices/{symbol}           # Price for specific asset
GET  /api/v1/balance/{address}         # Balance for address (multi-chain)
GET  /api/v1/tx/{address}              # Transaction history
POST /api/v1/tx/broadcast              # Broadcast signed transaction
GET  /api/v1/fees                      # Current network fees
```

### Data Sources
- **Prices:** CoinGecko API or CoinMarketCap
- **Balances:** BlockCypher, Alchemy, or direct node RPC
- **Transactions:** Same as above

---

## Security Requirements (BugCatcher)

### Encryption
- Private keys: AES-256-GCM + Android Keystore
- Database: SQLCipher (encrypted SQLite)
- Backups: Encrypted JSON, password-protected

### Authentication
- Biometric: Android BiometricPrompt
- PIN: 6-digit minimum, argon2 hashing
- Password: Optional, bcrypt hashing

### Audit Requirements
- [ ] Penetration test
- [ ] Key extraction test
- [ ] Memory dump analysis
- [ ] Root detection
- [ ] Anti-tampering checks

---

## Milestones

| Week | Deliverable | Owner |
|------|-------------|-------|
| 1 | Architecture + UI mockups | Spindle + TapTap |
| 2 | Wallet creation + backup flow | TapTap |
| 3 | Send/receive + transaction history | TapTap |
| 4 | Backend API + sync | Pipeline |
| 5 | Security hardening + biometric | TapTap + BugCatcher |
| 6 | Testing + APK release | BugCatcher + Spindle |

---

## Deliverables Checklist

- [ ] Android project scaffold (Spindle)
- [ ] UI/UX mockups approved (Spindle)
- [ ] Wallet creation (BIP-39 mnemonic) (TapTap)
- [ ] Backup/recovery flow (TapTap)
- [ ] Portfolio dashboard (TapTap)
- [ ] Send/receive with QR (TapTap)
- [ ] Transaction history (TapTap)
- [ ] Backend API (Pipeline)
- [ ] Security audit pass (BugCatcher)
- [ ] APK signed + released (Spindle)
- [ ] Documentation complete (Spindle)

---

## Acceptance Criteria

1. **Functional**
   - [ ] Can create wallet with backup phrase
   - [ ] Can restore wallet from phrase
   - [ ] Can view balances for all 8 assets
   - [ ] Can send/receive each asset type
   - [ ] Transaction history displays correctly

2. **Security**
   - [ ] Keys encrypted at rest
   - [ ] Biometric unlock works
   - [ ] PIN required after 5 min idle
   - [ ] No keys in logs/memory dumps

3. **Performance**
   - [ ] App launch < 3 seconds
   - [ ] Balance sync < 5 seconds
   - [ ] Smooth 60fps UI

4. **Release**
   - [ ] Signed APK generated
   - [ ] Version 1.0.0 tagged
   - [ ] README with install instructions

---

## Questions?

Contact Spindle for architecture or Captain for requirements.

**Status:** 🟡 Awaiting kickoff  
**Kickoff Meeting:** TBD (coordinate with Software Team)  
**Target:** APK ready for testing in 4 weeks