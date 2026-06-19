# Dusty Wallet APK Build Task
**Assigned:** Spindle (CTO) + Software Team + Pipeline (Backend)  
**Priority:** HIGH  
**Captain's Request:** Android crypto wallet for consolidation

## Requirements

### Core Features
- [ ] Android APK (downloadable to phone)
- [ ] Multi-currency support (BTC, ETH, SOL, ADA, DOT, LINK, etc.)
- [ ] Portfolio overview/dashboard
- [ ] Send/receive functionality
- [ ] Transaction history
- [ ] Secure key storage (encrypted)
- [ ] Clean, simple UI

### Security Requirements
- [ ] Encrypted private key storage
- [ ] Biometric authentication (optional)
- [ ] Backup/recovery phrase
- [ ] PIN/password protection

### Deliverables
1. Android project structure
2. Main wallet functionality (Kotlin/Java)
3. Backend API (if needed) - Pipeline
4. Build scripts (Gradle)
5. APK release
6. Documentation

### Project Structure
```
dusty/
├── src/
│   ├── android/          # Android app source
│   ├── backend/          # Server components (Pipeline)
│   └── shared/           # Shared libraries
├── docs/
│   ├── setup.md
│   ├── security.md
│   └── api.md
├── build/
│   └── releases/         # APK files
└── README.md
```

### Supported Currencies
- Bitcoin (BTC)
- Ethereum (ETH)
- Solana (SOL)
- Cardano (ADA)
- Polkadot (DOT)
- Chainlink (LINK)
- Polygon (MATIC)
- Avalanche (AVAX)

### Status
- [ ] Architecture designed
- [ ] Android UI/UX mockups
- [ ] Core wallet functionality
- [ ] Security layer implemented
- [ ] Testing complete
- [ ] APK built
- [ ] Documentation complete

**Spindle: "Building the Captain's mobile command center."**
