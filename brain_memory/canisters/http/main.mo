// Canister #5: HTTP Outcalls Example
// Purpose: Demonstrate calling external APIs from canisters
// Complexity: Intermediate

import HTTP "mo:base/HTTP";
import Blob "mo:base/Blob";
import Text "mo:base/Text";
import Nat "mo:base/Nat";
import Nat64 "mo:base/Nat64";
import Debug "mo:base/Debug";
import Cycles "mo:base/ExperimentalCycles";

actor HttpExample {
  // IC management canister for HTTP outcalls
  let IC = actor("aaaaa-aa") : actor {
    http_request : ({
      url : Text;
      max_response_bytes : ?Nat64;
      method : { #get; #post; #head };
      headers : [{ name : Text; value : Text }];
      body : ?Blob;
      transform : ?{ function : shared ({ response : HttpResponse; context : Blob }) -> async HttpResponse };
    }) -> async HttpResponse;
  };

  public type HttpResponse = {
    status : Nat;
    headers : [{ name : Text; value : Text }];
    body : Blob;
  };

  // Fetch data from an external API
  public func fetchData(url : Text) : async Text {
    // Add cycles for the HTTP request (approx 400M cycles per request)
    Cycles.add(400_000_000);
    
    let response = await IC.http_request({
      url = url;
      max_response_bytes = ?20_000; // Max 20KB response
      method = #get;
      headers = [];
      body = null;
      transform = null;
    });
    
    // Convert response body to text
    Text.decodeUtf8(response.body)
  };

  // Fetch with custom headers
  public func fetchWithHeaders(url : Text, headers : [(Text, Text)]) : async Text {
    Cycles.add(400_000_000);
    
    let headerRecords = Array.map(headers, func((name, value) : (Text, Text)) : { name : Text; value : Text } {
      { name = name; value = value }
    });
    
    let response = await IC.http_request({
      url = url;
      max_response_bytes = ?20_000;
      method = #get;
      headers = headerRecords;
      body = null;
      transform = null;
    });
    
    switch (Text.decodeUtf8(response.body)) {
      case (?text) { text };
      case (null) { "Error: Could not decode response" };
    }
  };

  // POST request example
  public func postData(url : Text, payload : Text) : async Text {
    Cycles.add(400_000_000);
    
    let bodyBlob = Text.encodeUtf8(payload);
    
    let response = await IC.http_request({
      url = url;
      max_response_bytes = ?10_000;
      method = #post;
      headers = [
        { name = "Content-Type"; value = "application/json" }
      ];
      body = ?bodyBlob;
      transform = null;
    });
    
    switch (Text.decodeUtf8(response.body)) {
      case (?text) { text };
      case (null) { "Error: Could not decode response" };
    }
  };

  // Transform function to handle response (required for some APIs)
  public shared({ caller }) func transform(raw : { response : HttpResponse; context : Blob }) : async HttpResponse {
    {
      status = raw.response.status;
      headers = raw.response.headers;
      body = raw.response.body;
    }
  };
};

// dfx.json:
/*
{
  "canisters": {
    "http": {
      "main": "main.mo",
      "type": "motoko"
    }
  }
}
*/

// Usage:
// dfx canister call http fetchData '("https://api.example.com/data")'
// dfx canister call http fetchWithHeaders '("https://api.example.com/data", vec { record { "Authorization"; "Bearer token123" } })'
// dfx canister call http postData '("https://api.example.com/submit", "{\"key\":\"value\"}")'

// Note: HTTP outcalls are limited on the mainnet. 
// The target API must accept requests from canister IP ranges.
