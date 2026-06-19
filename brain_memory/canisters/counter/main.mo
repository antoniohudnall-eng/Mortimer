// Canister #1: Counter
// Purpose: Demonstrate basic actor, query, and update functions
// Complexity: Beginner

actor Counter {
  // Stable variables persist across canister upgrades
  stable var count : Nat = 0;

  // QUERY function - fast, free, read-only
  // Does not modify state
  public query func getCount() : async Nat {
    count
  };

  // UPDATE function - costs cycles, goes through consensus
  // Modifies state
  public func increment() : async () {
    count += 1;
  };

  public func decrement() : async () {
    // Guard to prevent underflow
    if (count > 0) {
      count -= 1;
    };
  };

  public func add(n : Nat) : async () {
    count += n;
  };

  public func reset() : async () {
    count := 0;
  };

  // Returns current value and resets to 0
  public func take() : async Nat {
    let current = count;
    count := 0;
    current
  };
};

// dfx.json for this canister:
/*
{
  "canisters": {
    "counter": {
      "main": "main.mo",
      "type": "motoko"
    }
  }
}
*/

// Usage:
// dfx canister call counter getCount
// dfx canister call counter increment
// dfx canister call counter add '(5)'
// dfx canister call counter reset
