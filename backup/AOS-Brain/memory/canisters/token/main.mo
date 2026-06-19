// Canister #3: ICRC-1 Token Implementation
// Purpose: Fungible token standard (like ERC-20)
// Complexity: Advanced

import Map "mo:base/HashMap";
import Iter "mo:base/Iter";
import Nat "mo:base/Nat";
import Nat64 "mo:base/Nat64";
import Text "mo:base/Text";
import Principal "mo:base/Principal";
import Time "mo:base/Time";
import Array "mo:base/Array";
import Blob "mo:base/Blob";

actor Token {
  // ICRC-1 Types
  public type Account = {
    owner : Principal;
    subaccount : ?Subaccount;
  };
  
  public type Subaccount = Blob;
  
  public type Balance = Nat;
  
  public type TransferArgs = {
    from_subaccount : ?Subaccount;
    to : Account;
    amount : Balance;
    fee : ?Balance;
    memo : ?Blob;
    created_at_time : ?Nat64;
  };
  
  public type TransferError = {
    #BadFee : { expected_fee : Balance };
    #BadBurn : { min_burn_amount : Balance };
    #InsufficientFunds : { balance : Balance };
    #TooOld;
    #CreatedInFuture : { ledger_time : Nat64 };
    #TemporarilyUnavailable;
    #GenericError : { error_code : Nat; message : Text };
  };
  
  public type TransferResult = {
    #Ok : Nat;
    #Err : TransferError;
  };
  
  public type Value = {
    #Nat : Nat;
    #Int : Int;
    #Text : Text;
    #Blob : Blob;
  };

  // Token configuration
  let tokenName = "DarkFactoryToken";
  let tokenSymbol = "DFT";
  let decimals : Nat8 = 8;
  let fee : Balance = 10_000; // 0.0001 tokens
  
  // Total supply: 100 million tokens
  let totalSupply : Balance = 100_000_000_000_000_00; // with 8 decimals

  // State
  stable var balancesEntries : [(Account, Balance)] = [];
  stable var totalMinted : Balance = 0;
  stable var totalBurned : Balance = 0;
  
  var balances = Map.HashMap<Account, Balance>(10, accountEqual, accountHash);
  var transactions : [Transaction] = [];

  // Transaction type
  type Transaction = {
    id : Nat;
    from : ?Account;
    to : Account;
    amount : Balance;
    fee : Balance;
    timestamp : Int;
  };

  // Account comparison
  func accountEqual(a : Account, b : Account) : Bool {
    Principal.equal(a.owner, b.owner) and subaccountEqual(a.subaccount, b.subaccount)
  };

  func subaccountEqual(a : ?Subaccount, b : ?Subaccount) : Bool {
    switch (a, b) {
      case (null, null) { true };
      case (?sa1, ?sa2) { Blob.equal(sa1, sa2) };
      case _ { false };
    }
  };

  // Account hashing
  func accountHash(a : Account) : Nat {
    let ownerHash = Principal.hash(a.owner);
    switch (a.subaccount) {
      case (null) { ownerHash };
      case (?sa) { ownerHash + Blob.hash(sa) };
    }
  };

  // Initialization
  system func postupgrade() {
    balances := Map.HashMap<Account, Balance>(balancesEntries.size(), accountEqual, accountHash);
    for ((account, balance) in balancesEntries.vals()) {
      balances.put(account, balance);
    };
    balancesEntries := [];
  };

  system func preupgrade() {
    balancesEntries := Iter.toArray(balances.entries());
  };

  // Constructor - mint all tokens to deployer
  public shared(msg) func init() : async () {
    if (totalMinted == 0) {
      let deployerAccount : Account = {
        owner = msg.caller;
        subaccount = null;
      };
      balances.put(deployerAccount, totalSupply);
      totalMinted := totalSupply;
    };
  };

  // ICRC-1 Standard Functions
  
  public query func icrc1_name() : async Text {
    tokenName
  };

  public query func icrc1_symbol() : async Text {
    tokenSymbol
  };

  public query func icrc1_decimals() : async Nat8 {
    decimals
  };

  public query func icrc1_fee() : async Balance {
    fee
  };

  public query func icrc1_total_supply() : async Balance {
    totalMinted - totalBurned
  };

  public query func icrc1_minting_account() : async ?Account {
    null // No minting account in this implementation
  };

  public query func icrc1_balance_of(account : Account) : async Balance {
    switch (balances.get(account)) {
      case (null) { 0 };
      case (?balance) { balance };
    }
  };

  public query func icrc1_supported_standards() : async [{ name : Text; url : Text }] {
    [
      { name = "ICRC-1"; url = "https://github.com/dfinity/ICRC-1" }
    ]
  };

  public shared(msg) func icrc1_transfer(args : TransferArgs) : async TransferResult {
    let fromAccount : Account = {
      owner = msg.caller;
      subaccount = args.from_subaccount;
    };

    let fromBalance = switch (balances.get(fromAccount)) {
      case (null) { 0 };
      case (?b) { b };
    };

    let transferFee = switch (args.fee) {
      case (?f) { f };
      case (null) { fee };
    };

    let totalRequired = args.amount + transferFee;

    // Check sufficient funds
    if (fromBalance < totalRequired) {
      return #Err(#InsufficientFunds { balance = fromBalance });
    };

    // Check fee
    if (transferFee != fee) {
      return #Err(#BadFee { expected_fee = fee });
    };

    // Update balances
    balances.put(fromAccount, fromBalance - totalRequired);
    
    let toBalance = switch (balances.get(args.to)) {
      case (null) { 0 };
      case (?b) { b };
    };
    balances.put(args.to, toBalance + args.amount);

    // Record transaction
    let tx : Transaction = {
      id = transactions.size();
      from = ?fromAccount;
      to = args.to;
      amount = args.amount;
      fee = transferFee;
      timestamp = Time.now();
    };
    transactions := Array.append(transactions, [tx]);

    #Ok(tx.id)
  };

  // Additional functions
  
  public query func getTransaction(id : Nat) : async ?Transaction {
    if (id < transactions.size()) {
      ?transactions[id]
    } else {
      null
    }
  };

  public query func getTransactions(start : Nat, limit : Nat) : async [Transaction] {
    let end = Nat.min(start + limit, transactions.size());
    if (start >= transactions.size()) {
      return [];
    };
    Array.tabulate(end - start, func(i : Nat) : Transaction {
      transactions[start + i]
    })
  };

  public query func getTransactionCount() : async Nat {
    transactions.size()
  };

  // Convert token amount to display amount
  public query func toDisplayAmount(amount : Balance) : async Float {
    Float.fromInt(amount) / Float.fromInt(10 ** Nat.toNat(decimals))
  };
};

// dfx.json:
/*
{
  "canisters": {
    "token": {
      "main": "main.mo",
      "type": "motoko"
    }
  }
}
*/

// Usage:
// dfx canister call token init
// dfx canister call token icrc1_name
// dfx canister call token icrc1_symbol
// dfx canister call token icrc1_total_supply
// dfx canister call token icrc1_balance_of '(record { owner = principal "..."; subaccount = null })'
// dfx canister call token icrc1_transfer '(record { to = record { owner = principal "..."; subaccount = null }; amount = 100000000 })'
