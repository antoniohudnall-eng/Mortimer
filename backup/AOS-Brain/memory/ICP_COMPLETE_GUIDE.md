# The Great Cryptonio's Complete ICP Guide
## Performance Supply Depot LLC - Web3 Knowledge Base

---

## Table of Contents
1. [ICP Fundamentals](#1-icp-fundamentals)
2. [Motoko Programming](#2-motoko-programming)
3. [Canister Development](#3-canister-development)
4. [Web3 Integration](#4-web3-integration)
5. [Deployment Guide](#5-deployment-guide)
6. [Code Examples](#6-code-examples)

---

## 1. ICP Fundamentals

### What is the Internet Computer?

The Internet Computer (IC) is a decentralized cloud computing platform that extends the internet's functionality with serverless cloud capabilities. It's a blockchain that runs at web speed with infinite capacity.

### Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERNET COMPUTER                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ Subnet 1 │  │ Subnet 2 │  │ Subnet N │   ...             │
│  │ • Nodes  │  │ • Nodes  │  │ • Nodes  │                  │
│  │ • Canist │  │ • Canist │  │ • Canist │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
│                                                              │
│  Chain Key Cryptography - Single 48-byte public key         │
│  for the entire network                                      │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

#### Canisters
- **Definition:** Smart contracts evolved - they contain both code AND state
- **Capacity:** Up to 4GB of memory per canister
- **Cost:** Pay for computation with cycles (1 trillion cycles ≈ $1.30)
- **Capabilities:** 
  - Serve web content directly (no traditional servers needed!)
  - Store and process data
  - Call other canisters
  - Make HTTP requests to the outside world

#### Subnets
- Blockchain partitions running on dedicated node machines
- Each subnet can host thousands of canisters
- Canisters on different subnets can communicate
- New subnets can be added for infinite scalability

#### Internet Identity (II)
- Passwordless authentication using WebAuthn/Passkeys
- No usernames/passwords to remember
- Works with fingerprint, FaceID, hardware keys
- Anonymous - no personal data shared with apps

#### Chain Key Cryptography
- Revolutionary tech that enables:
  - 1-2 second finality
  - Canisters to sign for other blockchains
  - Entire network represented by a single public key

---

## 2. Motoko Programming

### Why Motoko?
- Designed specifically for the Internet Computer
- Actor-based programming model (like Erlang)
- Native async/await support
- Type-safe with automatic memory management
- Can compile to WebAssembly

### Basic Structure

```motoko
// actor is the main unit - like a class with async capabilities
actor MyCanister {
  // State variables are persisted across upgrades if marked 'stable'
  stable var counter : Nat = 0;

  // Query function - fast, free, read-only
  public query func getCounter() : async Nat {
    counter
  };

  // Update function - costs cycles, goes through consensus
  public func increment() : async () {
    counter += 1;
  };
};
```

### Data Types

```motoko
// Primitives
let number : Nat = 42;        // Natural number (non-negative)
let integer : Int = -42;      // Integer (can be negative)
let text : Text = "Hello";    // String
let flag : Bool = true;       // Boolean
let blob : Blob = "binary";   // Binary data

// Collections
let array : [Nat] = [1, 2, 3];
let list : List.List<Nat> = List.nil();
let map : HashMap.HashMap<Text, Nat> = HashMap.HashMap(10, Text.equal, Text.hash);

// Options
let maybeValue : ?Nat = ?42;  // Some(42)
let noValue : ?Nat = null;    // None

// Variants (enums with data)
type Result = {
  #ok : Nat;
  #err : Text;
};
```

### Control Flow

```motoko
// If/else
if (counter > 10) {
  // do something
} else {
  // do something else
};

// Switch (pattern matching)
switch (maybeValue) {
  case (?value) { /* handle value */ };
  case (null) { /* handle null */ };
};

// Loops
var i = 0;
while (i < 10) {
  i += 1;
};

// For loop
for (item in array.vals()) {
  // process item
};

// Functional iteration
let doubled = Array.map<Nat, Nat>(array, func(x) { x * 2 });
```

### Async/Await

```motoko
// Calling another canister
import OtherCanister "canister:other";

actor Caller {
  public func getRemoteData() : async Text {
    let result = await OtherCanister.getData();
    result
  };

  // Parallel calls
  public func getMultiple() : async [Text] {
    let call1 = OtherCanister.getData1();
    let call2 = OtherCanister.getData2();
    let call3 = OtherCanister.getData3();
    
    [await call1, await call2, await call3]
  };
};
```

---

## 3. Canister Development

### Project Structure

```
my_project/
├── dfx.json              # Project configuration
├── src/
│   └── my_project/
│       └── main.mo       # Main Motoko file
└── README.md
```

### dfx.json Configuration

```json
{
  "canisters": {
    "my_project": {
      "main": "src/my_project/main.mo",
      "type": "motoko"
    }
  },
  "defaults": {
    "build": {
      "packtool": "mops"
    }
  },
  "networks": {
    "local": {
      "bind": "127.0.0.1:4943",
      "type": "ephemeral"
    }
  },
  "version": 1
}
```

### Stable Memory

```motoko
// Variables marked 'stable' persist across canister upgrades
stable var userData : [(Text, Nat)] = [];

// Before upgrade - save heap data to stable
system func preupgrade() {
  userData := Iter.toArray(users.entries());
};

// After upgrade - restore from stable
system func postupgrade() {
  for ((key, value) in userData.vals()) {
    users.put(key, value);
  };
  userData := [];
};
```

---

## 4. Web3 Integration

### Internet Identity Integration

```javascript
// Frontend integration (JavaScript)
import { AuthClient } from "@dfinity/auth-client";

const authClient = await AuthClient.create();

await authClient.login({
  identityProvider: "https://identity.ic0.app",
  onSuccess: async () => {
    const identity = authClient.getIdentity();
    // User is now authenticated!
  },
});
```

### Ethereum Integration

```motoko
// Canisters can sign Ethereum transactions!
// Using EVM RPC canister

import EvmRpc "canister:evm_rpc";

actor EthBridge {
  public func sendEthTransaction() : async Result {
    // Use threshold ECDSA to sign
    // Submit to Ethereum via HTTPS outcalls
  };
};
```

### Token Standards

#### ICRC-1 (Fungible Tokens)
```motoko
// Standard interface for tokens on ICP
public shared func icrc1_transfer(args: TransferArgs) : async Result {
  // Transfer tokens between accounts
};
```

#### ICRC-7 (NFTs)
```motoko
// NFT standard similar to ERC-721
public shared func icrc7_transfer(args: TransferArgs) : async Result {
  // Transfer NFT ownership
};
```

---

## 5. Deployment Guide

### Local Development

```bash
# 1. Install DFX
curl -fsSL https://internetcomputer.org/install.sh | sh

# 2. Start local replica
dfx start --background

# 3. Create new project
dfx new hello_icp --type motoko
cd hello_icp

# 4. Deploy locally
dfx deploy

# 5. Get canister ID
source .env && echo $CANISTER_ID_HELLO_ICP

# 6. Call functions
dfx canister call hello_icp greet '("World")'
```

### Mainnet Deployment

```bash
# 1. Get cycles (ICP tokens converted to cycles)
# Use cycle faucet for testnet: https://faucet.dfinity.org

# 2. Create canister with cycles
dfx ledger --network ic create-canister $(dfx identity get-principal) --amount 2.0

# 3. Deploy to mainnet
dfx deploy --network ic

# 4. Your canister is live!
# Access at: https://{canister_id}.raw.ic0.app
```

### Cycles Management

```bash
# Check cycles balance
dfx canister --network ic status hello_icp

# Top up cycles
dfx canister --network ic deposit-cycles 1000000000000 hello_icp

# Convert ICP to cycles
dfx cycles convert --amount 5.0 --network ic
```

---

## 6. Code Examples

See the `/canisters/` directory for complete, deployable examples:

1. **counter** - Basic counter with increment/decrement
2. **todo** - Task manager with CRUD operations
3. **token** - ICRC-1 compliant token
4. **http** - HTTP outcalls to external APIs
5. **auth** - Internet Identity integration

---

*Knowledge compiled by The Great Cryptonio*
*Performance Supply Depot LLC*
