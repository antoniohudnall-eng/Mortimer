# QUANTUM DEFENDER: The Qubit Shield
## Android Game for DroidScript
### Based on Quantum Simulation + OODA Loop AI
### Project 5912 - AOCROS Games Division

---

## 🎮 GAME CONCEPT

**Title:** Quantum Defender: The Qubit Shield  
**Platform:** Android (DroidScript)  
**Genre:** Puzzle/Strategy/Defense  
**Theme:** Protect quantum systems from decoherence

### The Hook
You are a **Quantum Guardian** defending fragile qubits from the forces of **Noise** and **Decoherence**. Using quantum gates (Hadamard, CNOT, Pauli-X), you must maintain superposition states while an AI opponent (the OODA Loop) tries to collapse your wavefunction.

---

## 📖 STORY FRAMEWORK

### Option A: Standalone Sci-Fi
**Setting:** The Quantum Realm  
**You:** A quantum engineer in 2087  
**Enemy:** The Entropy AI—an artificial intelligence that feeds on quantum decoherence  
**Mission:** Protect humanity's quantum internet from collapse

### Option B: Milk Man Universe Integration
**Setting:** M.U.U.'s Training Module  
**You:** Milk Man in a quantum simulation  
**Enemy:** Decoherence Demons (Vil Laine's digital minions)  
**Mission:** Learn quantum mechanics to understand the Cream Crown's power  
**Canonicity:** Spin-off training game

### Option C: AOCROS Tech Demo
**Setting:** Project 5912 Research Lab  
**You:** Test pilot for quantum defense systems  
**Enemy:** Glitches, errors, environmental noise  
**Mission:** Prove quantum error correction works

---

## 🎯 CORE GAMEPLAY LOOP

### Phase 1: The Setup (Choose Your State)
- Start with a 3-qubit system
- Choose initial basis state: |000⟩, |001⟩, |010⟩, |011⟩, |100⟩
- Visual: Three glowing orbs representing qubits

### Phase 2: Build Your Defense (Apply Gates)
- **Hadamard (H):** Creates superposition (risk/reward)
- **CNOT:** Entangles qubits (defensive linking)
- **Pauli-X:** Flips qubit state (counter-moves)
- **Visual:** Drag gates onto qubit orbs

### Phase 3: The OODA Loop Attacks
- AI opponent observes your state
- Orient: Calculates weak points
- Decide: Chooses noise type
- Act: Applies decoherence/error

### Phase 4: Measurement Crisis
- If noise succeeds: Forced measurement (game over if wrong state)
- If defended: Maintain superposition (points awarded)
- Visual: Wavefunction collapse animation

### Phase 5: Level Up
- Unlock more gates (Toffoli, Phase, Rotation)
- Add more qubits (4, 5, 6...)
- Face smarter OODA AI (more layers/nodes)

---

## 🧠 THE OODA LOOP AI (THE ENEMY)

### Structure
```
OBSERVE → ORIENT → DECIDE → ACT
    ↑                         │
    └─────────────────────────┘
```

### Neural Network Growth
The AI gets stronger by adding neurons:

**Level 1 (Basic):**
- 1 hidden layer, 3 neurons
- Only applies bit-flip noise
- Predictable patterns

**Level 2 (Intermediate):**
- 2 hidden layers, 8 neurons
- Phase noise + bit-flip
- Learns gate sequences

**Level 3 (Advanced):**
- 3+ hidden layers, 20+ neurons
- Environmental decoherence
- Adapts to player strategies

**Level 4 (Expert):**
- Dynamic architecture (adds nodes mid-game)
- Full quantum noise model
- Near-impossible to predict

### Noise Types
1. **Bit-Flip:** X error (flips |0⟩↔|1⟩)
2. **Phase-Flip:** Z error (changes sign)
3. **Bit-Phase:** Y error (both)
4. **Depolarization:** Random state collapse
5. **Decoherence:** Loses superposition over time

---

## 🎨 VISUAL DESIGN (DroidScript Compatible)

### Qubit Representation
```
|0⟩ = Blue glowing orb, calm
|1⟩ = Red glowing orb, active
Superposition = Pulsing purple (Halo effect)
Entangled = Connected by energy beams
```

### Gate Visuals
- **H Gate:** Diamond shape, rainbow gradient
- **CNOT:** Two orbs with control→target arrow
- **X Gate:** X symbol, spark effect

### Noise Attack Animation
- Decoherence: Static/glitch overlay
- Bit-flip: Orb color swaps violently
- Phase error: Orb dims/shifts hue

### UI Layout (DroidScript)
```
┌─────────────────────────────┐
│     SCORE: 0    LEVEL: 1    │
├─────────────────────────────┤
│                             │
│    [Q0]═══[Q1]═══[Q2]      │
│      ↕      ↕      ↕       │
│    State: |ψ⟩ = ...         │
│                             │
├─────────────────────────────┤
│  [H] [X] [CNOT] [Measure]  │
├─────────────────────────────┤
│   OODA STATUS: OBSERVING    │
│   Threat: LOW              │
└─────────────────────────────┘
```

---

## 💻 DROIDSCRIPT GAME CODE

### File Structure
```
QuantumDefender/
├── main.js          # Entry point
├── gameLogic.py     # Quantum simulation
├── oodaAI.py        # Neural network AI
├── ui.js            # Interface handlers
└── assets/          # Graphics, sounds
```

### main.js (Game Entry Point)
```javascript
// Quantum Defender - Main Entry
// DroidScript Android Game

var gameState = {
    score: 0,
    level: 1,
    qubits: 3,
    currentState: [1, 0, 0, 0, 0, 0, 0, 0], // |000⟩
    oodaThreat: 0
};

function OnStart() {
    // Create main layout
    lay = app.CreateLayout("Linear", "VCenter,FillXY");
    
    // Title
    title = app.CreateText("🛡️ Quantum Defender", 0.9, 0.1);
    title.SetTextSize(28);
    title.SetTextColor("#00FF00");
    lay.AddChild(title);
    
    // Status bar
    statusBar = app.CreateText("Score: 0 | Level: 1 | Threat: LOW", 0.9, 0.05);
    statusBar.SetTextSize(16);
    lay.AddChild(statusBar);
    
    // Qubit display area
    qubitCanvas = app.CreateImage(null, 0.9, 0.35);
    qubitCanvas.SetAutoUpdate(false);
    lay.AddChild(qubitCanvas);
    
    // State vector display
    stateDisplay = app.CreateText("|ψ⟩ = |000⟩", 0.9, 0.1);
    stateDisplay.SetTextSize(14);
    stateDisplay.SetFontFamily("monospace");
    lay.AddChild(stateDisplay);
    
    // Control buttons
    btnLay = app.CreateLayout("Linear", "Horizontal");
    
    btnH = app.CreateButton("H Gate", 0.22, 0.12);
    btnH.SetOnTouch(function() { ApplyGate("H", 0); });
    btnLay.AddChild(btnH);
    
    btnX = app.CreateButton("X Gate", 0.22, 0.12);
    btnX.SetOnTouch(function() { ApplyGate("X", 0); });
    btnLay.AddChild(btnX);
    
    btnCNOT = app.CreateButton("CNOT", 0.22, 0.12);
    btnCNOT.SetOnTouch(function() { ApplyGate("CNOT", 0, 1); });
    btnLay.AddChild(btnCNOT);
    
    btnMeasure = app.CreateButton("Measure", 0.22, 0.12);
    btnMeasure.SetOnTouch(MeasureState);
    btnLay.AddChild(btnMeasure);
    
    lay.AddChild(btnLay);
    
    // OODA status
    oodaStatus = app.CreateText("🤖 OODA: OBSERVING...", 0.9, 0.08);
    oodaStatus.SetTextColor("#FF6600");
    lay.AddChild(oodaStatus);
    
    // Start/Reset
    btnStart = app.CreateButton("Start Game", 0.6, 0.1);
    btnStart.SetOnTouch(StartGame);
    lay.AddChild(btnStart);
    
    app.AddLayout(lay);
    
    // Draw initial qubits
    DrawQubits();
}

function DrawQubits() {
    // Draw qubit visualization
    var canv = qubitCanvas.GetContext();
    canv.SetFillStyle("#000000");
    canv.FillRect(0, 0, 1, 1);
    
    // Draw 3 qubit orbs
    for(var i = 0; i < 3; i++) {
        var x = 0.2 + (i * 0.3);
        var y = 0.5;
        
        // Orb glow
        var gradient = canv.CreateRadialGradient(x, y, 0.02, x, y, 0.08);
        gradient.AddColorStop(0, "#4444FF");
        gradient.AddColorStop(1, "#000044");
        
        canv.SetFillStyle(gradient);
        canv.BeginPath();
        canv.Arc(x, y, 0.08, 0, 2 * Math.PI);
        canv.Fill();
        
        // Label
        canv.SetFillStyle("#FFFFFF");
        canv.SetFontSize(12);
        canv.FillText("Q" + i, x - 0.02, y + 0.15);
    }
    
    // Draw connections if entangled
    canv.SetStrokeStyle("#00FF00");
    canv.SetLineWidth(0.005);
    canv.BeginPath();
    canv.MoveTo(0.2, 0.5);
    canv.LineTo(0.8, 0.5);
    canv.Stroke();
    
    qubitCanvas.Update();
}

function ApplyGate(gateType, target, control) {
    // Call Python simulation
    app.ExecutePython(`
        # Get current state from JavaScript
        state = app.GetData("currentState")
        
        # Apply gate logic from gameLogic.py
        if gateType == "H":
            new_state = apply_hadamard(state, ${target})
        elif gateType == "X":
            new_state = apply_pauli_x(state, ${target})
        elif gateType == "CNOT":
            new_state = apply_cnot(state, ${control}, ${target})
        
        # Send back to JavaScript
        app.Call("UpdateState", new_state)
        
        # Trigger OODA observation
        app.Call("OODA_Observe")
    `);
}

function UpdateState(newState) {
    gameState.currentState = newState;
    UpdateDisplay();
    CheckWinCondition();
}

function UpdateDisplay() {
    // Format state for display
    var stateStr = "|ψ⟩ = ";
    var basis = ["000", "001", "010", "011", "100", "101", "110", "111"];
    var hasAmp = false;
    
    for(var i = 0; i < 8; i++) {
        if(Math.abs(gameState.currentState[i]) > 0.01) {
            if(hasAmp) stateStr += " + ";
            stateStr += gameState.currentState[i].toFixed(2) + "|" + basis[i] + "⟩";
            hasAmp = true;
        }
    }
    
    stateDisplay.SetText(stateStr);
    DrawQubits();
}

function StartGame() {
    gameState.score = 0;
    gameState.level = 1;
    gameState.currentState = [1, 0, 0, 0, 0, 0, 0, 0];
    
    // Start OODA loop
    StartOODA_Loop();
    UpdateDisplay();
}

function StartOODA_Loop() {
    // OODA acts every few seconds
    setInterval(function() {
        RunOODA_Cycle();
    }, 5000);
}

function RunOODA_Cycle() {
    oodaStatus.SetText("🤖 OODA: ORIENTING...");
    
    setTimeout(function() {
        oodaStatus.SetText("🤖 OODA: DECIDING...");
        
        setTimeout(function() {
            oodaStatus.SetText("🤖 OODA: ATTACKING!");
            ExecuteOODA_Attack();
        }, 1000);
    }, 1500);
}

function ExecuteOODA_Attack() {
    // Python determines attack
    app.ExecutePython(`
        current_state = app.GetData("currentState")
        level = app.GetData("level")
        
        # OODA AI decides attack
        noise_type, strength = ooda_decide_attack(current_state, level)
        
        # Apply noise
        attacked_state = apply_noise(current_state, noise_type, strength)
        
        # Update game
        app.Call("OODA_Attack_Result", attacked_state, noise_type)
    `);
}

function OODA_Attack_Result(newState, noiseType) {
    gameState.currentState = newState;
    gameState.oodaThreat += 10;
    
    oodaStatus.SetText("🤖 OODA: OBSERVING...");
    UpdateDisplay();
    
    // Show attack notification
    app.ShowPopup("OODA applied " + noiseType + "!", "Short");
}

function MeasureState() {
    // Player chooses to measure
    app.ExecutePython(`
        state = app.GetData("currentState")
        measured = measure_state(state)
        app.Call("ShowMeasurement", measured)
    `);
}

function ShowMeasurement(result) {
    app.ShowPopup("Measured: |" + result + "⟩", "Long");
    
    // Check if desired state achieved
    // (Game win condition logic here)
}

function CheckWinCondition() {
    // Example: Maintain specific superposition for 10 turns = win
    // Or: Reach Bell state |00⟩ + |11⟩ / √2
}
```

### gameLogic.py (Core Quantum Simulation)
```python
# gameLogic.py
# Pure Python quantum simulation (no NumPy)
import math
import random

# Hadamard gate (1/√2 ≈ 0.707)
H = [[0.707, 0.707], [0.707, -0.707]]

# Pauli-X gate (NOT)
X = [[0, 1], [1, 0]]

# Pauli-Z gate (Phase flip)
Z = [[1, 0], [0, -1]]

def apply_single_qubit_gate(state, gate, target_qubit):
    """Apply single-qubit gate to 3-qubit state"""
    new_state = [0.0] * 8
    
    for i in range(8):
        if abs(state[i]) < 0.0001:
            continue
            
        binary = format(i, '03b')
        target_bit = int(binary[2 - target_qubit])
        
        for j in [0, 1]:
            new_binary = list(binary)
            new_binary[2 - target_qubit] = str(j)
            new_index = int(''.join(new_binary), 2)
            new_state[new_index] += state[i] * gate[target_bit][j]
    
    return new_state

def apply_cnot(state, control_qubit, target_qubit):
    """Apply CNOT gate"""
    new_state = [0.0] * 8
    
    for i in range(8):
        if abs(state[i]) < 0.0001:
            continue
            
        binary = format(i, '03b')
        control_bit = int(binary[2 - control_qubit])
        target_bit = int(binary[2 - target_qubit])
        
        new_binary = list(binary)
        if control_bit == 1:
            new_binary[2 - target_qubit] = str(1 - target_bit)
        
        new_index = int(''.join(new_binary), 2)
        new_state[new_index] += state[i]
    
    return new_state

def apply_hadamard(state, qubit):
    """Apply H gate"""
    return apply_single_qubit_gate(state, H, qubit)

def apply_pauli_x(state, qubit):
    """Apply X gate"""
    return apply_single_qubit_gate(state, X, qubit)

def measure_state(state):
    """Collapse to basis state"""
    # Calculate probabilities
    probs = [abs(x)**2 for x in state]
    total = sum(probs)
    
    if total > 0:
        probs = [p / total for p in probs]
    else:
        probs = [1/8] * 8
    
    # Random weighted choice
    r = random.random()
    cumulative = 0
    basis = ["000", "001", "010", "011", "100", "101", "110", "111"]
    
    for i, p in enumerate(probs):
        cumulative += p
        if r < cumulative:
            return basis[i]
    
    return basis[-1]

def apply_noise(state, noise_type, strength):
    """Apply quantum noise"""
    new_state = state[:]
    
    if noise_type == "bit_flip":
        # Random bit-flip on random qubit
        qubit = random.randint(0, 2)
        new_state = apply_pauli_x(new_state, qubit)
        
    elif noise_type == "phase_flip":
        # Phase flip (simulate with Z gate)
        qubit = random.randint(0, 2)
        new_state = apply_single_qubit_gate(new_state, Z, qubit)
        
    elif noise_type == "decoherence":
        # Reduce superposition (dampen amplitudes toward classical)
        for i in range(8):
            new_state[i] *= (1 - strength)
            
    elif noise_type == "depolarization":
        # Mix with maximally mixed state
        for i in range(8):
            new_state[i] = (1 - strength) * new_state[i] + strength / 8
    
    # Normalize
    norm = math.sqrt(sum(abs(x)**2 for x in new_state))
    if norm > 0:
        new_state = [x / norm for x in new_state]
    
    return new_state
```

### oodaAI.py (The Neural Network Enemy)
```python
# oodaAI.py
# OODA Loop with dynamic neural network

import random
import math

class OODA_NeuralNet:
    """Neural network that grows with difficulty"""
    
    def __init__(self, level=1):
        self.level = level
        self.input_size = 8  # State vector amplitudes
        self.hidden_layers = self._create_hidden_layers()
        self.output_size = 3  # Choose noise type
        
    def _create_hidden_layers(self):
        """Create layers based on difficulty"""
        if self.level == 1:
            # Simple: 1 layer, 3 neurons
            return [[self._random_weights(self.input_size) for _ in range(3)]]
        elif self.level == 2:
            # Medium: 2 layers
            layer1 = [self._random_weights(self.input_size) for _ in range(6)]
            layer2 = [self._random_weights(6) for _ in range(4)]
            return [layer1, layer2]
        else:
            # Hard: 3+ layers with dynamic growth
            layers = []
            prev_size = self.input_size
            for i in range(3 + self.level // 3):
                layer_size = min(20, prev_size + 2)
                layers.append([self._random_weights(prev_size) for _ in range(layer_size)])
                prev_size = layer_size
            return layers
    
    def _random_weights(self, size):
        """Initialize random weights"""
        return [random.uniform(-1, 1) for _ in range(size)]
    
    def add_node(self, layer_idx):
        """Dynamically add node during gameplay (OODA learns)"""
        if layer_idx < len(self.hidden_layers):
            prev_size = len(self.hidden_layers[layer_idx - 1]) if layer_idx > 0 else self.input_size
            self.hidden_layers[layer_idx].append(self._random_weights(prev_size))
            # Update next layer weights
            if layer_idx + 1 < len(self.hidden_layers):
                for neuron in self.hidden_layers[layer_idx + 1]:
                    neuron.append(random.uniform(-1, 1))
    
    def activate(self, x):
        """ReLU activation"""
        return max(0, x)
    
    def forward(self, state):
        """Forward pass through network"""
        current = state[:]
        
        for layer in self.hidden_layers:
            new_layer = []
            for neuron in layer:
                # Weighted sum
                z = sum(current[i] * neuron[i] for i in range(len(current)))
                new_layer.append(self.activate(z))
            current = new_layer
        
        # Output: softmax for noise type probability
        exp_values = [math.exp(x) for x in current[:3]]
        total = sum(exp_values)
        return [x / total for x in exp_values]
    
    def observe(self, game_state):
        """OBSERVE: Record current state"""
        self.observed_state = game_state["currentState"]
        self.score = game_state["score"]
        self.level = game_state["level"]
        return self.observed_state
    
    def orient(self, state):
        """ORIENT: Analyze for weaknesses"""
        # Calculate superposition strength
        non_zero = sum(1 for x in state if abs(x) > 0.01)
        
        # Find dominant amplitudes
        max_amp = max(abs(x) for x in state)
        
        self.weakness_score = non_zero / 8.0  # More superposition = harder to attack
        self.target_dominant = max_amp
        
        return self.weakness_score
    
    def decide(self, weakness_score):
        """DECIDE: Choose noise type"""
        noise_types = ["bit_flip", "phase_flip", "decoherence"]
        
        if self.level >= 3:
            # Use neural network
            probs = self.forward(self.observed_state)
            r = random.random()
            cumulative = 0
            for i, p in enumerate(probs):
                cumulative += p
                if r < cumulative:
                    return noise_types[i], 0.1 * self.level
            return noise_types[-1], 0.1 * self.level
        else:
            # Rule-based for lower levels
            if weakness_score > 0.5:
                return "decoherence", 0.05 * self.level
            else:
                return random.choice(["bit_flip", "phase_flip"]), 0.1 * self.level
    
    def act(self, state, noise_type, strength):
        """ACT: Apply the attack"""
        from gameLogic import apply_noise
        return apply_noise(state, noise_type, strength)

def ooda_decide_attack(game_state, level):
    """Main OODA decision function (called from JS)"""
    ai = OODA_NeuralNet(level)
    
    # Full OODA cycle
    ai.observe(game_state)
    weakness = ai.orient(game_state["currentState"])
    noise_type, strength = ai.decide(weakness)
    
    return noise_type, strength

# Adaptive learning: AI adds nodes when player scores high
def ooda_learn(ai, player_score):
    """Grow network if player is winning"""
    if player_score > ai.level * 100:
        # Add random node
        layer = random.randint(0, len(ai.hidden_layers) - 1)
        ai.add_node(layer)
        return True
    return False
```

---

## 🎮 GAME MECHANICS

### Scoring System
```
+10 points: Successfully apply gate
+25 points: Create Bell state (entanglement)
+50 points: Maintain superposition through OODA attack
+100 points: Complete level objective
-20 points: Qubit collapses to wrong state
-50 points: Forced measurement (decoherence)
```

### Level Objectives

**Level 1: The Basics**
- Start: |000⟩
- Goal: Create |000⟩ + |111⟩ / √2 (GHZ state)
- OODA: Basic (1 layer)

**Level 2: Bell Pairs**
- Goal: Create two Bell pairs
- OODA: Medium (adds phase noise)

**Level 3: Error Correction**
- Goal: Protect state through 3 OODA attacks
- OODA: Hard (dynamic learning)

**Level 4: Grover's Hunt**
- Goal: Amplitude amplification to find target
- OODA: Expert (full network)

**Level 5: Shor's Shadow**
- Goal: Period-finding simulation (simplified)
- OODA: Adaptive (keeps adding nodes)

---

## 🔗 INTEGRATION WITH EXISTING SYSTEMS

### Option 1: Standalone APK
- Export from DroidScript as .apk
- Install on any Android device
- No dependencies

### Option 2: Miles Integration
```python
# Connect to Miles for "cloud" saves
import miles_client

miles = MilesClient("http://miles.aocros.local:12788")
miles.write("QD_highscore", score, OWNER_SIGNATURE)
```

### Option 3: Milk Man Crossover
```javascript
// Unlock bonus content
if (QuantumDefender.completed) {
    UnlockMilkManLevel("M.U.U. Training Module")
}
```

---

## 🚀 NEXT STEPS

1. **Test Core Loop**
   - Load into DroidScript
   - Verify gate operations
   - Test OODA attacks

2. **Add Visual Polish**
   - Animations for gate application
   - Particle effects for noise
   - Music/sound (Reggie?)

3. **Expand Content**
   - More levels
   - Additional gates (Toffoli, etc.)
   - Boss battles (major OODA attacks)

4. **Polish & Release**
   - Balance difficulty
   - Tutorial mode
   - High scores

---

**Status:** Quantum Defense Game designed for Android  
**Platform:** DroidScript (JavaScript + Python)  
**Estimated Dev Time:** 2-3 weeks  
**Priority:** Medium (after Milk Man sprites)

---

**Captain, shall we port this to DroidScript and test on Android? Or focus on Milk Man sprites first?** ⚛️🎮

**"Defend the superposition, or the qubits collapse!"**
