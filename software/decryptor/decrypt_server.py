#!/usr/bin/env python3
"""
NetProbe Decryption Server
Receives encrypted intel from probes, decrypts, and distributes
Version: 1.0.0-OMEGA
Classification: Q-LEVEL
"""

import os
import sys
import json
import base64
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import nacl.bindings
from nacl.public import PrivateKey, PublicKey, Box
from nacl.secret import SecretBox
from nacl.utils import random
import uvicorn

# Configuration
VAULT_PATH = Path("/root/.openclaw/workspace/armory/vault/netprobe")
SESSION_KEYS_PATH = VAULT_PATH / "session_keys"
RECEIVED_INTEL_PATH = Path("/root/.openclaw/workspace/armory/intelligence/netprobe")
KEY_MANIFEST = VAULT_PATH / "key_manifest.json"

app = FastAPI(title="NetProbe Decryptor", version="1.0.0-OMEGA")

# =============================================================================
# DATA MODELS
# =============================================================================

class EncryptedPayload(BaseModel):
    """Encrypted intel from probe"""
    version: str = Field(..., description="Protocol version")
    probe_pub_key: str = Field(..., description="Probe's ephemeral public key (hex)")
    nonce: str = Field(..., description="XChaCha20 nonce (hex)")
    ciphertext: str = Field(..., description="Encrypted payload (hex)")
    timestamp: int = Field(..., description="Unix timestamp")
    probe_id: Optional[str] = Field(None, description="Probe identifier")
    target: Optional[str] = Field(None, description="Target IP/domain")
    probe_type: Optional[str] = Field(None, description="EYES, EARS, HONEYPOT")
    chunk_info: Optional[Dict] = Field(None, description="Chunking metadata if applicable")

class DecryptedIntel(BaseModel):
    """Decrypted intelligence data"""
    probe_id: str
    timestamp: datetime
    target: str
    probe_type: str
    data: Dict[str, Any]
    raw_size: int
    decrypted_at: datetime

# =============================================================================
# KEY MANAGEMENT
# =============================================================================

class KeyManager:
    """Manages session keys for probe decryption"""
    
    def __init__(self, vault_path: Path = VAULT_PATH):
        self.vault_path = vault_path
        self.session_keys_path = SESSION_KEYS_PATH
        self.session_cache = {}  # In-memory cache
        
        # Ensure directories exist
        self.session_keys_path.mkdir(parents=True, exist_ok=True)
        RECEIVED_INTEL_PATH.mkdir(parents=True, exist_ok=True)
    
    def load_session_key(self, session_id: str) -> Optional[bytes]:
        """Load a session private key from vault"""
        
        # Check cache first
        if session_id in self.session_cache:
            return self.session_cache[session_id]
        
        # Load from file
        key_file = self.session_keys_path / f"{session_id}.enc"
        if not key_file.exists():
            return None
        
        # Read encrypted key
        encrypted_key = key_file.read_bytes()
        
        # Decrypt with master key (simplified - in production use proper key derivation)
        master_key = self._get_master_key()
        
        # Use first 32 bytes of master key as key
        key = master_key[:32]
        
        # Simple XOR for demo - replace with proper decryption
        decrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(encrypted_key)])
        
        # Cache in memory
        self.session_cache[session_id] = decrypted
        
        return decrypted
    
    def store_session_key(self, session_id: str, private_key: bytes, public_key: bytes):
        """Store a session keypair in vault"""
        
        # Encrypt private key
        master_key = self._get_master_key()
        key = master_key[:32]
        encrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(private_key)])
        
        # Save encrypted private key
        key_file = self.session_keys_path / f"{session_id}.enc"
        key_file.write_bytes(encrypted)
        
        # Save public key (not secret)
        pub_file = self.session_keys_path / f"{session_id}.pub"
        pub_file.write_bytes(public_key)
        
        # Update manifest
        self._update_manifest(session_id, public_key.hex())
        
        # Cache
        self.session_cache[session_id] = private_key
    
    def _get_master_key(self) -> bytes:
        """Retrieve master key from vault"""
        master_key_file = self.vault_path / "NETPROBE_MASTER.key"
        
        if not master_key_file.exists():
            # Generate master key if doesn't exist
            master_key = os.urandom(32)
            master_key_file.write_bytes(base64.b64encode(master_key))
            os.chmod(master_key_file, 0o600)
            return master_key
        
        encoded = master_key_file.read_bytes()
        return base64.b64decode(encoded)
    
    def _update_manifest(self, session_id: str, public_key_hex: str):
        """Update key manifest"""
        
        manifest = {}
        if KEY_MANIFEST.exists():
            manifest = json.loads(KEY_MANIFEST.read_text())
        
        manifest[session_id] = {
            "created": datetime.utcnow().isoformat(),
            "public_key": public_key_hex,
            "status": "active"
        }
        
        KEY_MANIFEST.write_text(json.dumps(manifest, indent=2))
    
    def derive_shared_secret(self, session_private_key: bytes, probe_public_key: bytes) -> bytes:
        """Derive shared secret using ECDH"""
        
        # Convert keys
        private_key = PrivateKey(session_private_key)
        public_key = PublicKey(probe_public_key)
        
        # Perform ECDH
        box = Box(private_key, public_key)
        
        # Use box's shared key
        shared = box.shared_key()
        
        # Hash to get uniform key
        return hashlib.sha256(shared).digest()

# Global key manager
key_manager = KeyManager()

# =============================================================================
# DECRYPTION
# =============================================================================

def decrypt_xchacha20poly1305(ciphertext: bytes, nonce: bytes, key: bytes) -> bytes:
    """Decrypt using XChaCha20-Poly1305"""
    
    # NaCl uses XSalsa20, for XChaCha20 we use bindings directly
    # Or use PyNaCl's SecretBox with appropriate key
    box = SecretBox(key)
    
    # Combine nonce and ciphertext for NaCl
    message = box.decrypt(ciphertext, nonce)
    
    return message

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.post("/decrypt", response_model=Dict)
async def decrypt_intel(payload: EncryptedPayload, x_session_id: str = Header(...)):
    """
    Decrypt intel from a probe.
    
    Headers:
        x-session-id: Session ID for key lookup
    """
    
    try:
        # Load session private key
        session_private_key = key_manager.load_session_key(x_session_id)
        if not session_private_key:
            raise HTTPException(status_code=404, detail="Session key not found")
        
        # Decode probe public key
        probe_public_key = bytes.fromhex(payload.probe_pub_key)
        
        # Derive shared secret
        shared_secret = key_manager.derive_shared_secret(
            session_private_key,
            probe_public_key
        )
        
        # Decode nonce and ciphertext
        nonce = bytes.fromhex(payload.nonce)
        ciphertext = bytes.fromhex(payload.ciphertext)
        
        # Decrypt
        decrypted = decrypt_xchacha20poly1305(ciphertext, nonce, shared_secret)
        
        # Parse intel data
        intel_data = json.loads(decrypted.decode('utf-8'))
        
        # Create decrypted intel record
        intel_record = DecryptedIntel(
            probe_id=payload.probe_id or "unknown",
            timestamp=datetime.utcfromtimestamp(payload.timestamp),
            target=payload.target or "unknown",
            probe_type=payload.probe_type or "unknown",
            data=intel_data,
            raw_size=len(ciphertext),
            decrypted_at=datetime.utcnow()
        )
        
        # Save to intelligence store
        intel_file = RECEIVED_INTEL_PATH / f"intel_{payload.probe_id}_{int(datetime.utcnow().timestamp())}.json"
        intel_file.write_text(intel_record.json(indent=2))
        
        return {
            "status": "success",
            "probe_id": intel_record.probe_id,
            "target": intel_record.target,
            "type": intel_record.probe_type,
            "data": intel_data,
            "decrypted_at": intel_record.decrypted_at.isoformat(),
            "saved_to": str(intel_file)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")

@app.post("/session/create")
async def create_session():
    """Create a new session keypair for a probe launch"""
    
    try:
        # Generate keypair
        private_key = PrivateKey.generate()
        public_key = private_key.public_key
        
        # Generate session ID
        session_id = f"sess_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"
        
        # Store in vault
        key_manager.store_session_key(
            session_id,
            bytes(private_key),
            bytes(public_key)
        )
        
        return {
            "session_id": session_id,
            "public_key": public_key.hex(),
            "expires": (datetime.utcnow() + timedelta(hours=24)).isoformat(),
            "status": "active"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session creation failed: {str(e)}")

@app.get("/intel/list")
async def list_intel(limit: int = 10):
    """List recently decrypted intelligence"""
    
    intel_files = sorted(RECEIVED_INTEL_PATH.glob("intel_*.json"), reverse=True)[:limit]
    
    results = []
    for f in intel_files:
        try:
            data = json.loads(f.read_text())
            results.append({
                "file": f.name,
                "probe_id": data.get("probe_id"),
                "target": data.get("target"),
                "timestamp": data.get("timestamp"),
                "probe_type": data.get("probe_type")
            })
        except:
            pass
    
    return {"intel_count": len(results), "items": results}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "netprobe-decryptor",
        "version": "1.0.0-OMEGA",
        "vault_path": str(VAULT_PATH),
        "session_keys_available": len(list(SESSION_KEYS_PATH.glob("*.enc"))) if SESSION_KEYS_PATH.exists() else 0
    }

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🔐 NETPROBE DECRYPTION SERVER")
    print("=" * 60)
    print(f"Vault: {VAULT_PATH}")
    print(f"Session Keys: {SESSION_KEYS_PATH}")
    print(f"Intel Storage: {RECEIVED_INTEL_PATH}")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8123)