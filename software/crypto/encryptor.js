// NetProbe Encryptor Module (DroidScript Compatible)
// XChaCha20-Poly1305 encryption for probe intelligence
// Version: 1.0.0-OMEGA

// Check if libsodium is available
if (typeof sodium === 'undefined') {
    // Fallback: Load libsodium from CDN or local
    app.LoadScript('libsodium.js');
}

const NetProbeCrypto = {
    // Configuration
    ALGORITHM: 'XCHACHA20-POLY1305',
    NONCE_SIZE: 24,  // 192 bits for XChaCha20
    KEY_SIZE: 32,    // 256 bits
    TAG_SIZE: 16,    // 128 bits for Poly1305
    
    // Initialize sodium
    _initialized: false,
    
    init: function() {
        if (this._initialized) return true;
        
        if (typeof sodium === 'undefined') {
            console.error('Libsodium not loaded');
            return false;
        }
        
        // Wait for sodium to be ready
        if (!sodium.ready) {
            setTimeout(() => this.init(), 100);
            return false;
        }
        
        this._initialized = true;
        console.log('[CRYPTO] XChaCha20-Poly1305 ready');
        return true;
    },
    
    // Generate ephemeral keypair for this probe session
    generateKeypair: function() {
        if (!this.init()) throw new Error('Crypto not initialized');
        
        const keypair = sodium.crypto_box_keypair();
        return {
            publicKey: keypair.publicKey,
            privateKey: keypair.privateKey,
            publicHex: sodium.to_hex(keypair.publicKey),
            privateHex: sodium.to_hex(keypair.privateKey)
        };
    },
    
    // Derive shared secret using ECDH
    deriveSharedSecret: function(privateKey, publicKey) {
        if (!this.init()) throw new Error('Crypto not initialized');
        
        // Convert from hex if needed
        const priv = (typeof privateKey === 'string') 
            ? sodium.from_hex(privateKey) 
            : privateKey;
        const pub = (typeof publicKey === 'string') 
            ? sodium.from_hex(publicKey) 
            : publicKey;
        
        // Use ECDH to derive shared secret
        const shared = sodium.crypto_scalarmult(priv, pub);
        
        // Hash shared secret to get encryption key
        const encryptionKey = sodium.crypto_generichash(32, shared);
        
        return encryptionKey;
    },
    
    // Encrypt payload using XChaCha20-Poly1305
    encrypt: function(plaintext, sharedSecret) {
        if (!this.init()) throw new Error('Crypto not initialized');
        
        // Generate random nonce (24 bytes for XChaCha20)
        const nonce = sodium.randombytes_buf(this.NONCE_SIZE);
        
        // Convert plaintext to bytes if string
        const message = (typeof plaintext === 'string') 
            ? sodium.from_string(plaintext) 
            : plaintext;
        
        // Encrypt with XChaCha20-Poly1305
        const ciphertext = sodium.crypto_aead_xchacha20poly1305_ietf_encrypt(
            message,
            null,  // Additional data (can add metadata here)
            nonce,
            sharedSecret
        );
        
        return {
            nonce: sodium.to_hex(nonce),
            ciphertext: sodium.to_hex(ciphertext),
            combined: sodium.to_hex(nonce) + sodium.to_hex(ciphertext)
        };
    },
    
    // Decrypt payload (for testing/verification)
    decrypt: function(ciphertextHex, nonceHex, sharedSecret) {
        if (!this.init()) throw new Error('Crypto not initialized');
        
        const ciphertext = sodium.from_hex(ciphertextHex);
        const nonce = sodium.from_hex(nonceHex);
        
        const decrypted = sodium.crypto_aead_xchacha20poly1305_ietf_decrypt(
            ciphertext,
            null,  // Additional data (must match encryption)
            nonce,
            sharedSecret
        );
        
        return sodium.to_string(decrypted);
    },
    
    // Generate master key (256-bit)
    generateMasterKey: function() {
        if (!this.init()) throw new Error('Crypto not initialized');
        
        const key = sodium.randombytes_buf(this.KEY_SIZE);
        return {
            key: key,
            hex: sodium.to_hex(key),
            base64: sodium.to_base64(key)
        };
    },
    
    // Securely wipe memory (best effort in JS)
    secureWipe: function(buffer) {
        if (buffer && buffer.fill) {
            buffer.fill(0);
        }
        // Force garbage collection hint
        buffer = null;
    },
    
    // Create encrypted transmission package
    createTransmission: function(intelData, sessionPublicKey, probeKeypair) {
        // Derive shared secret
        const sharedSecret = this.deriveSharedSecret(
            probeKeypair.privateKey,
            sessionPublicKey
        );
        
        // Encrypt the intel
        const encrypted = this.encrypt(JSON.stringify(intelData), sharedSecret);
        
        // Wipe sensitive data from memory
        this.secureWipe(sharedSecret);
        
        return {
            version: '2.0-ENCRYPTED',
            probePubKey: probeKeypair.publicHex,
            nonce: encrypted.nonce,
            ciphertext: encrypted.ciphertext,
            timestamp: Date.now(),
            algorithm: this.ALGORITHM
        };
    },
    
    // Chunk large data for transmission
    chunkData: function(data, chunkSize = 8192) {
        const chunks = [];
        let offset = 0;
        let sequence = 0;
        
        const totalChunks = Math.ceil(data.length / chunkSize);
        
        while (offset < data.length) {
            const chunk = data.slice(offset, offset + chunkSize);
            const checksum = this.quickChecksum(chunk);
            
            chunks.push({
                sequence: sequence++,
                total: totalChunks,
                data: chunk,
                checksum: checksum
            });
            
            offset += chunkSize;
        }
        
        return chunks;
    },
    
    // Quick checksum for chunk integrity (not cryptographic)
    quickChecksum: function(data) {
        if (!this.init()) return '0';
        
        const hash = sodium.crypto_generichash(8, 
            (typeof data === 'string') ? sodium.from_string(data) : data
        );
        return sodium.to_hex(hash);
    }
};

// Export for DroidScript
if (typeof module !== 'undefined') {
    module.exports = NetProbeCrypto;
}

// For DroidScript global scope
if (typeof app !== 'undefined') {
    app.NetProbeCrypto = NetProbeCrypto;
}