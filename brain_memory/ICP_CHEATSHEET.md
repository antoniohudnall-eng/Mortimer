# ICP Quick Reference - The Great Cryptonio's Cheatsheet

## DFX CLI Commands

```bash
# Installation
curl -fsSL https://internetcomputer.org/install.sh | sh
source $HOME/.local/share/dfx/env

# Local Development
dfx start --background              # Start local IC replica
dfx stop                            # Stop replica
dfx restart                         # Restart replica
dfx start --clean                   # Clean start (removes state)

# Project Management
dfx new my_project --type motoko   # Create new Motoko project
dfx new my_project --type rust     # Create new Rust project
dfx build                          # Build all canisters
dfx deploy                         # Deploy locally
dfx deploy --network ic            # Deploy to mainnet

# Canister Operations
dfx canister call CANISTER_NAME METHOD '(ARGUMENTS)'
dfx canister id CANISTER_NAME      # Get canister ID
dfx canister status CANISTER_NAME --network ic
dfx canister delete CANISTER_NAME --network ic

# Identity Management
dfx identity get-principal         # Get your principal
dfx identity new NAME              # Create new identity
dfx identity use NAME              # Switch identity

# Cycles (Mainnet)
dfx cycles balance --network ic
dfx cycles convert --amount 5.0 --network ic
dfx canister --network ic deposit-cycles AMOUNT CANISTER_NAME
```

## Motoko Types

```motoko
// Primitives
let n : Nat = 1;                   // Natural number (0, 1, 2...)
let i : Int = -1;                  // Integer (...-1, 0, 1...)
let t : Text = "hello";            // String
let b : Bool = true;               // Boolean
let p : Principal = ...;            // Principal ID

// Collections
let arr : [Nat] = [1, 2, 3];       // Array
let list : List.List<T>;           // Linked list
let map : HashMap.HashMap<K, V>;   // Hash map

// Options & Results
let some : ?Nat = ?42;             // Some value
let none : ?Nat = null;            // No value
let ok : Result<T, E> = #ok val;   // Success
let err : Result<T, E> = #err e;   // Error
```

## Actor Pattern

```motoko
actor MyCanister {
  stable var data : Nat = 0;       // Persistent across upgrades
  
  // Query - fast, free, read-only
  public query func get() : async Nat { data }
  
  // Update - costs cycles, modifies state
  public func set(n : Nat) : async () { data := n }
  
  // System hooks
  system func preupgrade() { /* save to stable */ };
  system func postupgrade() { /* restore from stable */ };
};
```

## Cycles Cost Reference

| Operation | Cycles |
|-----------|--------|
| Query call | Free |
| Update call | ~590K + execution |
| 1B instructions | ~5T cycles |
| HTTP outcall | ~400M cycles |
| Canister create | ~100B cycles |
| Storage (per GB/year) | ~127M cycles |

## Wallet Addresses

- **ICP Ledger:** `ryjl3-tyaaa-aaaaa-aaaba-cai`
- **Cycles Ledger:** `um5iw-rqaaa-aaaaq-qaawa-cai`
- **Internet Identity:** `rdmx6-jaaaa-aaaaa-aaadq-cai`
- **NNS Governance:** `rrkah-fqaaa-aaaaa-aaaaq-cai`

## Frontend Integration

```javascript
import { Actor, HttpAgent } from '@dfinity/agent';
import { AuthClient } from '@dfinity/auth-client';

// Create anonymous actor
const agent = new HttpAgent();
const actor = Actor.createActor(idlFactory, { agent, canisterId });

// Authenticated actor
const authClient = await AuthClient.create();
await authClient.login({ identityProvider: 'https://identity.ic0.app' });
const identity = authClient.getIdentity();
const authAgent = new HttpAgent({ identity });
```

## Token Standards

### ICRC-1 (Fungible)
```motoko
public shared func icrc1_transfer(args: TransferArgs) : async TransferResult
public query func icrc1_balance_of(account: Account) : async Balance
public query func icrc1_total_supply() : async Balance
```

### ICRC-7 (NFT)
```motoko
public shared func icrc7_transfer(args: TransferArg) : async TransferResult
public query func icrc7_balance_of(account: Account) : async Nat
public query func icrc7_token_metadata(token_ids: [Nat]) : async [?Value]
```

## Common Errors

| Error | Solution |
|-------|----------|
| `Insufficient funds` | Add ICP/cycles to wallet |
| `Canister not found` | Check canister ID |
| `Out of memory` | Increase canister memory |
| `Cycles limit exceeded` | Add more cycles |
| `Transform function required` | Add transform to HTTP call |

## Useful Links

- [ICP Portal](https://internetcomputer.org)
- [Motoko Docs](https://internetcomputer.org/docs/motoko)
- [Developer Forum](https://forum.dfinity.org)
- [ICP Scan](https://dashboard.internetcomputer.org)
- [Cycle Calculator](https://cyclescalculator.com)

---
*Compiled by The Great Cryptonio for Performance Supply Depot LLC*
