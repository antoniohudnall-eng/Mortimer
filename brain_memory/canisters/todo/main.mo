// Canister #2: Task Manager (Todo App)
// Purpose: Demonstrate CRUD operations, complex data types, and state management
// Complexity: Intermediate

import Map "mo:base/HashMap";
import Iter "mo:base/Iter";
import Text "mo:base/Text";
import Nat "mo:base/Nat";
import Time "mo:base/Time";

actor TaskManager {
  // Task type definition
  public type TaskId = Nat;
  
  public type Task = {
    id : TaskId;
    title : Text;
    description : Text;
    completed : Bool;
    createdAt : Int;
    updatedAt : Int;
  };

  public type TaskInput = {
    title : Text;
    description : Text;
  };

  // State
  stable var nextId : TaskId = 0;
  stable var tasksEntries : [(TaskId, Task)] = [];
  
  // Heap storage (recreated on upgrade from stable)
  var tasks = Map.HashMap<TaskId, Task>(10, Nat.equal, Nat.hash);

  // Initialize from stable storage
  system func postupgrade() {
    tasks := Map.HashMap<TaskId, Task>(tasksEntries.size(), Nat.equal, Nat.hash);
    for ((id, task) in tasksEntries.vals()) {
      tasks.put(id, task);
    };
    tasksEntries := [];
  };

  // Save to stable storage before upgrade
  system func preupgrade() {
    tasksEntries := Iter.toArray(tasks.entries());
  };

  // CREATE
  public func createTask(input : TaskInput) : async Task {
    let now = Time.now();
    let task : Task = {
      id = nextId;
      title = input.title;
      description = input.description;
      completed = false;
      createdAt = now;
      updatedAt = now;
    };
    
    tasks.put(nextId, task);
    nextId += 1;
    task
  };

  // READ
  public query func getTask(id : TaskId) : async ?Task {
    tasks.get(id)
  };

  public query func getAllTasks() : async [Task] {
    Iter.toArray(tasks.vals())
  };

  public query func getPendingTasks() : async [Task] {
    let all = Iter.toArray(tasks.vals());
    Array.filter(all, func(t : Task) : Bool { not t.completed })
  };

  public query func getCompletedTasks() : async [Task] {
    let all = Iter.toArray(tasks.vals());
    Array.filter(all, func(t : Task) : Bool { t.completed })
  };

  // UPDATE
  public func updateTask(id : TaskId, input : TaskInput) : async ?Task {
    switch (tasks.get(id)) {
      case (null) { null };
      case (?existing) {
        let updated : Task = {
          id = existing.id;
          title = input.title;
          description = input.description;
          completed = existing.completed;
          createdAt = existing.createdAt;
          updatedAt = Time.now();
        };
        tasks.put(id, updated);
        ?updated
      };
    }
  };

  public func completeTask(id : TaskId) : async ?Task {
    switch (tasks.get(id)) {
      case (null) { null };
      case (?existing) {
        let updated : Task = {
          id = existing.id;
          title = existing.title;
          description = existing.description;
          completed = true;
          createdAt = existing.createdAt;
          updatedAt = Time.now();
        };
        tasks.put(id, updated);
        ?updated
      };
    }
  };

  public func uncompleteTask(id : TaskId) : async ?Task {
    switch (tasks.get(id)) {
      case (null) { null };
      case (?existing) {
        let updated : Task = {
          id = existing.id;
          title = existing.title;
          description = existing.description;
          completed = false;
          createdAt = existing.createdAt;
          updatedAt = Time.now();
        };
        tasks.put(id, updated);
        ?updated
      };
    }
  };

  // DELETE
  public func deleteTask(id : TaskId) : async Bool {
    switch (tasks.get(id)) {
      case (null) { false };
      case (_) { 
        tasks.delete(id);
        true 
      };
    }
  };

  // STATS
  public query func getStats() : async { total : Nat; completed : Nat; pending : Nat } {
    let all = Iter.toArray(tasks.vals());
    let completed = Array.filter(all, func(t : Task) : Bool { t.completed }).size();
    {
      total = all.size();
      completed = completed;
      pending = all.size() - completed;
    }
  };

  // Clear all tasks (admin function)
  public func clearAll() : async () {
    tasks := Map.HashMap<TaskId, Task>(10, Nat.equal, Nat.hash);
    nextId := 0;
  };
};

// dfx.json:
/*
{
  "canisters": {
    "todo": {
      "main": "main.mo",
      "type": "motoko"
    }
  }
}
*/

// Usage examples:
// dfx canister call todo createTask '(record { title = "Buy ICP"; description = "Get some cycles ready" })'
// dfx canister call todo getAllTasks
// dfx canister call todo completeTask '(0)'
// dfx canister call todo getStats
