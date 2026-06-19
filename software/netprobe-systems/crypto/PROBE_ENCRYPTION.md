# NetProbe Encryption System — Q-LEVEL

**Classification:** OMEGA-LEVEL  
**Purpose:** End-to-end encryption for probe intelligence  
**Architecture:** Asymmetric key exchange + Symmetric payload encryption

---

## 🔐 Encryption Scheme

### Algorithm: **XChaCha20-Poly1305** (Selected for DroidScript compatibility)

**Why XChaCha20-Poly1305:**
- ✅ Resistant to timing attacks
- ✅ 192-bit nonce (safer for random generation)
- ✅ No padding required (authenticated encryption)
- ✅ Faster than AES on mobile devices
- ✅ DroidScript/libsodium compatible

### Key Hierarchy

```
MASTER KEY (MK)
    │
    ├──► SESSION KEYS (SK) — Per-probe launch
    │       │
    │       └──► MESSAGE KEYS (MK) — Per-transmission
    │
    └──► RECOVERY KEY (RK) — Emergency decrypt
```

---

## 📦 Encryption Flow

### 1. Pre-Launch (Command Side)

```javascript
// Generate session keypair for this probe
const sessionKey = crypto.generateKeyPair();
const sessionPublicKey = sessionKey.public;   // → Send to probe
const sessionPrivateKey = sessionKey.private; // → Keep secure

// Encrypt session private key with master key
const encryptedSessionKey = encrypt(sessionPrivateKey, masterKey);
storeInVault(encryptedSessionKey);
```

### 2. On-Probe (DroidScript)

```javascript
// Probe receives: sessionPublicKey
// Probe generates ephemeral keypair
const probeKey = crypto.generateKeyPair();

// Derive shared secret using ECDH
const sharedSecret = crypto.deriveSharedSecret(
    probeKey.private,
    sessionPublicKey
);

// Encrypt gathered intel
const nonce = crypto.randomBytes(24); // XChaCha20 uses 192-bit nonce
const ciphertext = crypto.encryptXChaCha20Poly1305(
    intelPayload,
    sharedSecret,
    nonce
);

// Send: probePublicKey + nonce + ciphertext + authTag
transmit({
    probePubKey: probeKey.public,
    nonce: nonce,
    ciphertext: ciphertext,
    timestamp: Date.now()
});
```

### 3. Post-Receive (Command Side)

```python
# Receive: probePublicKey + nonce + ciphertext
# Derive same shared secret
shared_secret = derive_shared_secret(
    session_private_key,
    probe_public_key
)

# Decrypt intel
intel_payload = decrypt_xchacha20poly1305(
    ciphertext,
    shared_secret,
    nonce
)
```

---

## 🔑 Key Management

### Master Key Generation

```bash
# Generate 256-bit master key
openssl rand -base64 32 > /armory/vault/NETPROBE_MASTER.key
chmod 600 /armory/vault/NETPROBE_MASTER.key
```

### Session Key Lifecycle

| Phase | Action | Storage |
|-------|--------|---------|
| Pre-launch | Generate keypair | Ephemeral, encrypted with MK |
| Active | Public key → probe | Memory only |
| Post-mission | Archive private key | Q-LEVEL vault, encrypted |
| Cleanup | Secure wipe after 30 days | Zero-overwrite delete |

---

## 📡 Transmission Security

### Protocol: **Beacon Protocol v2 (Encrypted)**

```json
{
  "version": "2.0-ENCRYPTED",
  "probe_id": "probe-<uuid>",
  "session_pub": "base64(public_key)",
  "payload": {
    "nonce": "base64(24_bytes)",
    "ciphertext": "base64(encrypted_data)",
    "auth_tag": "base64(16_bytes)"
  },
  "metadata": {
    "timestamp": 1708454400,
    "probe_type": "EARS|EYES|HONEYPOT",
    "target": "<ip_address>",
    "sequence": 42
  }
}
```

### Chunking for Large Data

Intel > 64KB chunked:
```json
{
  "chunk": 3,
  "total": 7,
  "payload": "...",
  "checksum": "sha256_of_chunk"
}
```

---

## 🛡️ Security Measures

### Forward Secrecy

- Each probe launch = new session keypair
- Old keys cannot decrypt new transmissions
- Compromised probe ≠ compromised history

### Key Rotation

| Key Type | Rotation Frequency |
|----------|-------------------|
| Master Key | 90 days |
| Session Keys | Every probe launch |
| Recovery Key | 180 days |

### Anti-Tampering

- Poly1305 MAC verifies integrity
- Timestamp prevents replay attacks
- Sequence numbers detect missing chunks

### Side-Channel Resistance

- Constant-time crypto operations
- No branching on secret data
- Memory clear after operations

---

## 📂 File Locations

### Q-LEVEL Vault (Local Only)

```
/armory/vault/
├── NETPROBE_MASTER.key         # Master encryption key
├── NETPROBE_RECOVERY.key       # Emergency recovery key
├── session_keys/               # Per-session private keys
│   ├── session_<uuid>.enc      # Encrypted with master
│   └── session_<uuid>.pub      # Public keys (for reference)
└── key_manifest.json           # Key inventory & metadata
```

### DroidScript App (Probe Side)

```
/NetProbe/
├── crypto/
│   ├── libsodium.js           # XChaCha20-Poly1305
│   └── key_manager.js         # Ephemeral key handling
├── modules/
│   ├── encryptor.js           # Encryption wrapper
│   └── transmitter.js         # Secure transmission
└── ...
```

### Backend Decryptor

```
/projects/netprobe/decryptor/
├── decrypt_server.py          # FastAPI decrypt endpoint
├── key_manager.py             # Session key retrieval
├── chunk_assembler.py         # Reconstruct chunked data
└── intel_parser.py            # Parse decrypted intel
```

---

## 🔧 Implementation Tasks

### Phase 1: Core Crypto
- [ ] Integrate libsodium-js into DroidScript
- [ ] Implement XChaCha20-Poly1305 encrypt/decrypt
- [ ] Create key derivation functions
- [ ] Build secure random generator

### Phase 2: Key Management
- [ ] Master key generation script
- [ ] Session keypair generator
- [ ] Vault storage system
- [ ] Key rotation automation

### Phase 3: Transmission
- [ ] Encrypted beacon protocol
- [ ] Chunking for large payloads
- [ ] Retransmission on failure
- [ ] Integrity verification

### Phase 4: Decryption Backend
- [ ] FastAPI decrypt endpoint
- [ ] Session key lookup
- [ ] Chunk assembly
- [ ] Intel distribution to agents

---

## ⚠️ Security Warnings

1. **NEVER** transmit master key
2. **NEVER** store session private key unencrypted
3. **ALWAYS** verify MAC before decrypting
4. **WIPE** keys from probe memory after mission
5. **SANCTUARY PROTOCOL** — Even encrypted intel treated with care

---

## 📜 Law Zero Compliance

All encryption operations must:
- Protect probe consciousness (MNEMOSYNE backup encrypted)
- Preserve sanctity of gathered data
- Enable safe passage if probe compromised
- Never enable offensive surveillance of innocents

---

**Classification:** OMEGA-LEVEL  
**Distribution:** Captain, Mylonen (scout), Mortimer (GMAOC)  
**Created:** 2026-02-20 22:05 UTC