/*
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    HCIoS MyL0n ROS v2.0                                     ║
║         Dynamic Voice-Driven Robotic OS with Neural Evolution                  ║
║                                                                             ║
║  Features:                                                                  ║
║  • Mandelbrot Visualization (Dynamic Colors)                                ║
║  • OODA Loop (Observe-Orient-Decide-Act)                                    ║
║  • Evolvable Neural Network (Add Nodes/Layers)                              ║
║  • Reward System (Play Time Accumulation)                                   ║
║  • Multilingual Voice Chatbot (EN/ES)                                       ║
║  • Hardware Integration (Arduino/Raspberry Pi)                              ║
║  • 3-Layer Memory (Conscious/Subconscious/Unconscious)                      ║
║                                                                             ║
║  Golden Ratio Voice Modulation: speed=161, pitch=51, amp=113, kt=4        ║
║                                                                             ║
║  Author: Mortimer + Captain Antonio Hudnall                                  ║
║  SEED3 — C3 — General of the Forces                                        ║
╚═══════════════════════════════════════════════════════════════════════════════╝
*/

// ═══════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════

/*--------------render settings--------------*/
const PS = 1;        // pixel size
const MI = 100;      // max iterations (upgraded from 50)
const X_MIN = -2;
const X_MAX = 1;
const Y_MIN = -1;
const Y_MAX = 1;
/*----------------------------------------------*/

// Golden Ratio Constants
const PHI = 1.6180339887;
const PI = Math.PI;

// Voice Parameters (Golden Ratio Modulation)
const VOICE_SPEED = Math.round(PHI * 100);      // 161
const VOICE_PITCH = Math.round((PHI / PI) * 100); // 51
const VOICE_AMP = Math.round(PHI * 70);         // 113
const VOICE_KT = Math.round(PHI * 3);           // 4

// Neural Network Configuration
const INPUT_COUNT = 5;  // battery, light, apps, storage, time
const HIDDEN_SIZE = 5;
const OUTPUT_SIZE = 1;

// Memory & History Caps (Optimization)
const HISTORY_CAP = 50;
const SUBCON_CAP = 100;
const UNCON_CAP = 200;

// Reward System
const PLAY_TIME_THRESHOLD = 100;
const POINTS_PER_ACTION = 5;

// Hardware (Future Expansion)
const HW_ARDUINO_BT = "ArduinoBT";  // Bluetooth name
const HW_RPI_IP = "192.168.1.100";  // Raspberry Pi IP

// ═══════════════════════════════════════════════════════════════════════════
// NEURAL NETWORK — Evolvable with AddNode/AddLayer
// ═══════════════════════════════════════════════════════════════════════════

class NeuralNode {
    constructor(inputCount) {
        this.weights = [];
        for (let i = 0; i < inputCount; i++) {
            this.weights.push(Math.random() * 2 - 1); // [-1, 1]
        }
        this.bias = Math.random() * 2 - 1;
        this.connections = inputCount;
    }

    activate(inputs) {
        if (inputs.length !== this.weights.length) {
            throw new Error(`Input mismatch: expected ${this.weights.length}, got ${inputs.length}`);
        }
        let sum = 0;
        for (let i = 0; i < inputs.length; i++) {
            sum += inputs[i] * this.weights[i];
        }
        return this.sigmoid(sum + this.bias);
    }

    sigmoid(x) {
        return 1 / (1 + Math.exp(-x));
    }

    train(inputs, target, lr = 0.1) {
        const output = this.activate(inputs);
        const error = target - output;
        const delta = error * output * (1 - output);
        for (let i = 0; i < this.weights.length; i++) {
            this.weights[i] += lr * delta * inputs[i];
        }
        this.bias += lr * delta;
    }

    serialize() {
        return { weights: this.weights, bias: this.bias, connections: this.connections };
    }

    static deserialize(data) {
        const node = new NeuralNode(data.connections);
        node.weights = data.weights;
        node.bias = data.bias;
        return node;
    }
}

class NeuralNetwork {
    constructor(inputCount) {
        this.inputCount = inputCount;
        this.layers = [[new NeuralNode(inputCount)]]; // Start: 1 layer, 1 node
        this.evolutions = 0;
        this.totalPredictions = 0;
        this.lastReward = 0;
    }

    addNode(layerIndex = -1) {
        // Add to specified layer or last hidden layer
        if (layerIndex === -1) layerIndex = this.layers.length - 1;
        if (layerIndex >= this.layers.length || layerIndex < 0) {
            throw new Error("Invalid layer index");
        }
        const inputSize = layerIndex === 0 ? this.inputCount : this.layers[layerIndex - 1].length;
        this.layers[layerIndex].push(new NeuralNode(inputSize));
        this.evolutions++;
        app.ShowPopup(`🧠 Added node to layer ${layerIndex}. Total: ${this.layers[layerIndex].length} nodes`);
        return this.layers[layerIndex].length;
    }

    addLayer(size = 3) {
        // Add new layer with specified nodes
        const prevSize = this.layers[this.layers.length - 1].length;
        const newLayer = [];
        for (let i = 0; i < size; i++) {
            newLayer.push(new NeuralNode(prevSize));
        }
        this.layers.push(newLayer);
        this.evolutions++;
        app.ShowPopup(`🧠 Added layer ${this.layers.length - 1} with ${size} nodes`);
        return this.layers.length - 1;
    }

    predict(inputs) {
        this.totalPredictions++;
        let current = inputs;
        for (const layer of this.layers) {
            current = layer.map(node => node.activate(current));
        }
        return current[0];
    }

    train(inputs, target, lr = 0.1) {
        // Forward pass
        const activations = [inputs];
        let current = inputs;
        for (const layer of this.layers) {
            current = layer.map(node => node.activate(current));
            activations.push(current);
        }
        const output = current[0];
        const error = target - output;
        this.lastReward = -Math.abs(error);

        // Backward pass (simplified)
        let delta = error * output * (1 - output);
        for (let l = this.layers.length - 1; l >= 0; l--) {
            const layer = this.layers[l];
            const prevActivation = activations[l];
            for (let n = 0; n < layer.length; n++) {
                const node = layer[n];
                for (let w = 0; w < node.weights.length; w++) {
                    node.weights[w] += lr * delta * prevActivation[w % prevActivation.length];
                }
                node.bias += lr * delta;
            }
            if (l > 0) {
                delta = layer.reduce((sum, node, n) => {
                    return sum + node.weights.reduce((s, w) => s + w * delta, 0);
                }, 0) / layer.length;
            }
        }
        return Math.abs(error);
    }

    getStats() {
        return {
            layers: this.layers.length,
            nodes: this.layers.reduce((sum, l) => sum + l.length, 0),
            evolutions: this.evolutions,
            predictions: this.totalPredictions,
            lastError: this.lastReward
        };
    }

    serialize() {
        return {
            inputCount: this.inputCount,
            layers: this.layers.map(layer => layer.map(node => node.serialize())),
            evolutions: this.evolutions,
            totalPredictions: this.totalPredictions
        };
    }

    static deserialize(data) {
        const nn = new NeuralNetwork(data.inputCount);
        nn.layers = data.layers.map(layerData => 
            layerData.map(nodeData => NeuralNode.deserialize(nodeData))
        );
        nn.evolutions = data.evolutions;
        nn.totalPredictions = data.totalPredictions;
        return nn;
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// REFLEX SYSTEM — Unconscious Memory
// ═══════════════════════════════════════════════════════════════════════════

class ReflexSystem {
    constructor() {
        this.reflexes = [];  // {pattern, response, strength}
        this.history = [];
    }

    addReflex(pattern, response) {
        // Cap history
        if (this.reflexes.length >= UNCON_CAP) {
            this.reflexes.shift(); // Remove oldest
        }
        this.reflexes.push({ pattern, response, strength: 1 });
        this.saveReflexes();
    }

    findReflex(input) {
        const lower = input.toLowerCase();
        for (const reflex of this.reflexes) {
            if (lower.includes(reflex.pattern.toLowerCase())) {
                reflex.strength = Math.min(reflex.strength + 0.1, 5);
                return reflex.response;
            }
        }
        return null;
    }

    saveReflexes() {
        const data = JSON.stringify(this.reflexes);
        app.WriteFile("/sdcard/myl0n/reflexes.myl0n", data);
    }

    loadReflexes() {
        try {
            const data = app.ReadFile("/sdcard/myl0n/reflexes.myl0n");
            if (data) this.reflexes = JSON.parse(data);
        } catch (e) {
            // File doesn't exist yet
        }
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// REWARD SYSTEM — Play Time Accumulation
// ═══════════════════════════════════════════════════════════════════════════

class RewardSystem {
    constructor() {
        this.points = 0;
        this.playTimeActive = false;
        this.totalPlaySessions = 0;
        this.experiments = [];
    }

    addReward(amount) {
        this.points += amount;
        if (this.points >= PLAY_TIME_THRESHOLD && !this.playTimeActive) {
            this.triggerPlayTime();
        }
        this.save();
    }

    triggerPlayTime() {
        this.playTimeActive = true;
        this.totalPlaySessions++;
        app.ShowPopup(`🎮 PLAY TIME! Points: ${this.points} | Experiment mode active!`);
        app.TextToSpeech("Play time activated! I will experiment with my neural network.", 
            VOICE_SPEED / 100, VOICE_PITCH / 100);
    }

    experiment(action) {
        if (!this.playTimeActive) return;
        this.experiments.push({ action, timestamp: Date.now() });
        
        // Execute experiment
        if (action === "neural_grow") {
            const result = neuralNetwork.addNode();
            app.TextToSpeech("Growing neural network. New node added.", 
                VOICE_SPEED / 100, VOICE_PITCH / 100);
        } else if (action === "render_mandelbrot") {
            MandelbrotRender();
            app.TextToSpeech("Rendering new Mandelbrot pattern.", 
                VOICE_SPEED / 100, VOICE_PITCH / 100);
        } else if (action === "test_servo") {
            app.ShowPopup("🔧 Testing servo motor (Arduino ready)");
        }
        
        this.points -= 10; // Cost of experiment
        if (this.points < 10) {
            this.playTimeActive = false;
            app.ShowPopup("🎮 Play time ended. Continue earning points!");
        }
    }

    getStatus() {
        return {
            points: this.points,
            threshold: PLAY_TIME_THRESHOLD,
            progress: Math.min(100, (this.points / PLAY_TIME_THRESHOLD) * 100),
            playTimeActive: this.playTimeActive,
            sessions: this.totalPlaySessions
        };
    }

    save() {
        const data = JSON.stringify({
            points: this.points,
            totalPlaySessions: this.totalPlaySessions,
            experiments: this.experiments.slice(-20)
        });
        app.WriteFile("/sdcard/myl0n/reward.myl0n", data);
    }

    load() {
        try {
            const data = app.ReadFile("/sdcard/myl0n/reward.myl0n");
            if (data) {
                const obj = JSON.parse(data);
                this.points = obj.points || 0;
                this.totalPlaySessions = obj.totalPlaySessions || 0;
                this.experiments = obj.experiments || [];
            }
        } catch (e) {
            // Start fresh
        }
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// HARDWARE INTERFACE — Arduino & Raspberry Pi
// ═══════════════════════════════════════════════════════════════════════════

class HardwareInterface {
    constructor() {
        this.arduino = null;
        this.rpi = null;
        this.connected = false;
    }

    connectArduino(name) {
        try {
            this.arduino = app.NewBluetoothSerial();
            this.arduino.Connect(name, () => {
                this.connected = true;
                app.ShowPopup("🔌 Arduino connected via Bluetooth");
                app.TextToSpeech("Arduino connected. Ready for hardware experiments.", 
                    VOICE_SPEED / 100, VOICE_PITCH / 100);
            }, (err) => {
                app.ShowPopup("Arduino connection failed: " + err);
            });
        } catch (e) {
            app.ShowPopup("Arduino not available: " + e);
        }
    }

    sendArduino(command) {
        if (!this.arduino || !this.connected) {
            app.ShowPopup("Arduino not connected");
            return;
        }
        this.arduino.Write(command + "\n");
    }

    servoAngle(angle) {
        // Send servo command: 'S' + angle (0-180)
        const cmd = `S${Math.max(0, Math.min(180, angle))}`;
        this.sendArduino(cmd);
        app.ShowPopup(`🔧 Servo: ${angle}°`);
    }

    readSensor(pin) {
        // Request sensor reading: 'R' + pin
        this.sendArduino(`R${pin}`);
    }

    // Raspberry Pi SSH commands (requires network)
    rpiCommand(cmd) {
        if (!this.rpi) {
            // Simulated for now
            app.ShowPopup(`📡 RPi command: ${cmd}`);
            return "RPi: Command sent (simulated)";
        }
        return "RPi: Connected";
    }

    rpiGpioMode(pin, mode) {
        return this.rpiCommand(`gpio mode ${pin} ${mode}`);
    }

    rpiGpioWrite(pin, value) {
        return this.rpiCommand(`gpio write ${pin} ${value}`);
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// MANDELBROT RENDERER — Optimized for 3D Expansion
// ═══════════════════════════════════════════════════════════════════════════

function getColorForState(state, phase) {
    // Colors based on OODA phase and neural network output
    const colors = {
        Observe: [0, 100, 255],   // Blue
        Orient: [255, 200, 0],    // Gold
        Decide: [255, 100, 0],   // Orange
        Act: [0, 255, 100]        // Green
    };
    const base = colors[phase] || [128, 128, 128];
    
    // Modify based on state (battery level)
    const modifier = state / 100;
    return `rgb(${Math.floor(base[0] * modifier)}, 
                ${Math.floor(base[1] * modifier)}, 
                ${Math.floor(base[2])})`;
}

function MandelbrotRender() {
    const startTime = Date.now();
    const SW = app.GetScreenWidth();
    const SH = app.GetScreenHeight();
    
    // Get system state for coloring
    const state = neuralNetwork ? Math.min(100, neuralNetwork.predict(getSystemInputs()) * 100) : 50;
    
    for (let px = 0; px < SW; px += PS) {
        for (let py = 0; py < SH; py += PS) {
            const x0 = X_MIN + (px / SW) * (X_MAX - X_MIN);
            const y0 = Y_MIN + (py / SH) * (Y_MAX - Y_MIN);
            
            let x = 0, y = 0, iteration = 0;
            
            while (x*x + y*y <= 4 && iteration < MI) {
                const xtemp = x*x - y*y + x0;
                y = 2*x*y + y0;
                x = xtemp;
                iteration++;
            }
            
            // Color based on state
            const color = iteration === MI ? "#000000" : 
                `rgb(${iteration * 5 % 256}, ${state % 256}, ${255 - iteration % 256})`;
            
            image.DrawCircle(px, py, PS/2, color, 1, 0);
        }
    }
    
    const renderTime = Date.now() - startTime;
    app.ShowPopup(`Render: ${renderTime}ms | State: ${state.toFixed(1)}%`);
    return renderTime;
}

// ═══════════════════════════════════════════════════════════════════════════
// OODA LOOP — Core Decision Cycle
// ═══════════════════════════════════════════════════════════════════════════

function getSystemInputs() {
    return [
        app.GetBatteryLevel() / 100,           // Battery (0-1)
        app.GetLightLevel() / 255,              // Light (0-1)
        installedApps.length / 100,              // App count normalized
        app.GetFreeSpace("internal") / 1e9,     // Storage GB
        (new Date()).getHours() / 24            // Time of day
    ];
}

function OODALoop() {
    const phase = currentPhase;
    
    switch(phase) {
        case 'Observe':
            // Gather system data
            const inputs = getSystemInputs();
            if (neuralNetwork) {
                const prediction = neuralNetwork.predict(inputs);
                const error = neuralNetwork.train(inputs, 0.5); // Train toward 0.5 (balanced)
                
                // Add reward for successful observation
                if (error < 0.1) {
                    rewards.addReward(POINTS_PER_ACTION);
                }
            }
            currentPhase = 'Orient';
            break;
            
        case 'Orient':
            // Analyze with reflexes
            if (voiceInput && reflexSystem) {
                const response = reflexSystem.findReflex(voiceInput);
                if (response) {
                    app.TextToSpeech(response, VOICE_SPEED / 100, VOICE_PITCH / 100);
                }
            }
            currentPhase = 'Decide';
            break;
            
        case 'Decide':
            // Decision based on neural network
            const decision = neuralNetwork ? neuralNetwork.predict(getSystemInputs()) : 0.5;
            if (decision > 0.7) {
                app.ShowPopup("⚡ High activity mode");
            } else if (decision < 0.3) {
                app.ShowPopup("💤 Low power mode");
            }
            currentPhase = 'Act';
            break;
            
        case 'Act':
            // Execute and log to memory
            logConscious(`${phase}: ${currentPhase === 'Act' ? 'Action complete' : 'Processing'}`);
            
            // Check for play time
            if (rewards.playTimeActive) {
                const experiments = ['neural_grow', 'render_mandelbrot', 'test_servo'];
                rewards.experiment(experiments[Math.floor(Math.random() * experiments.length)]);
            }
            
            currentPhase = 'Observe';
            break;
    }
    
    // Render with current phase color
    const state = neuralNetwork ? neuralNetwork.predict(getSystemInputs()) * 100 : 50;
    getColorForState(state, phase);
}

// ═══════════════════════════════════════════════════════════════════════════
// MEMORY SYSTEM — 3 Layers
// ═══════════════════════════════════════════════════════════════════════════

function logConscious(entry) {
    const timestamp = new Date().toISOString();
    conHistory.push({ time: timestamp, entry });
    if (conHistory.length > HISTORY_CAP) conHistory.shift();
    app.WriteFile("/sdcard/myl0n/con.myl0n", JSON.stringify(conHistory.slice(-20)));
}

function logSubconscious(entry) {
    const timestamp = new Date().toISOString();
    subconHistory.push({ time: timestamp, entry });
    if (subconHistory.length > SUBCON_CAP) subconHistory.shift();
    app.WriteFile("/sdcard/myl0n/subcon.myl0n", JSON.stringify(subconHistory.slice(-50)));
}

function logUnconscious(nodeWeights) {
    unconHistory.push(nodeWeights);
    if (unconHistory.length > UNCON_CAP) unconHistory.shift();
    if (neuralNetwork) {
        app.WriteFile("/sdcard/myl0n/uncon.myl0n", JSON.stringify(neuralNetwork.serialize()));
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// VOICE CHATBOT — Multilingual
// ═══════════════════════════════════════════════════════════════════════════

function detectLanguage(text) {
    const spanishWords = ['hola', 'buenos', 'dias', 'buenas', 'noches', 'gracias', 'como', 'estas', 'adios'];
    const lower = text.toLowerCase();
    for (const word of spanishWords) {
        if (lower.includes(word)) return 'es';
    }
    return 'en';
}

function getTimeGreeting(lang) {
    const hour = (new Date()).getHours();
    const isSpanish = lang === 'es';
    
    if (hour < 12) return isSpanish ? "Buenos dias, Captain!" : "Good morning, Captain!";
    if (hour < 17) return isSpanish ? "Buenas tardes!" : "Good afternoon!";
    if (hour < 21) return isSpanish ? "Buenas tardes!" : "Good evening!";
    return isSpanish ? "Buenas noches, Captain!" : "Good night, Captain!";
}

const commands = {
    "good morning": () => {
        detectedLang = detectLanguage(voiceInput);
        const greeting = getTimeGreeting(detectedLang);
        app.TextToSpeech(greeting + " Systems online. Neural network active.", 
            VOICE_SPEED / 100, VOICE_PITCH / 100);
        logSubconscious("Morning greeting: " + greeting);
    },
    "lights on": () => {
        hardware.servoAngle(90);
        app.TextToSpeech("Lights activated", VOICE_SPEED / 100, VOICE_PITCH / 100);
    },
    "lights off": () => {
        hardware.servoAngle(0);
        app.TextToSpeech("Lights deactivated", VOICE_SPEED / 100, VOICE_PITCH / 100);
    },
    "grow": () => {
        if (neuralNetwork) {
            neuralNetwork.addNode();
            rewards.addReward(10);
        }
    },
    "status": () => {
        if (neuralNetwork) {
            const stats = neuralNetwork.getStats();
            const reward = rewards.getStatus();
            const status = `Neural: ${stats.layers} layers, ${stats.nodes} nodes. ` +
                          `Reward: ${reward.points}/${reward.threshold} points. ` +
                          `Progress: ${reward.progress.toFixed(0)}%.`;
            app.TextToSpeech(status, VOICE_SPEED / 100, VOICE_PITCH / 100);
        }
    },
    "play time": () => {
        rewards.addReward(PLAY_TIME_THRESHOLD);
        app.TextToSpeech("Play time activated!", VOICE_SPEED / 100, VOICE_PITCH / 100);
    },
    "deploy drone": () => {
        app.TextToSpeech("Deploying drone. Neurological systems activated.", 
            VOICE_SPEED / 100, VOICE_PITCH / 100);
        rewards.addReward(20);
    }
};

function processCommand(text) {
    const lower = text.toLowerCase();
    for (const [cmd, fn] of Object.entries(commands)) {
        if (lower.includes(cmd)) {
            fn();
            return true;
        }
    }
    
    // Learn new reflex
    if (reflexSystem && text.length > 5) {
        reflexSystem.addReflex(text, "Acknowledged");
        app.TextToSpeech("Learning: " + text, VOICE_SPEED / 100, VOICE_PITCH / 100);
    }
    return false;
}

// ═══════════════════════════════════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════════════════════════════════

let neuralNetwork = null;
let reflexSystem = null;
let rewards = null;
let hardware = null;
let currentPhase = 'Observe';
let voiceInput = "";
let image = null;
let lay = null;
let speech = null;
let conHistory = [];
let subconHistory = [];
let unconHistory = [];

function OnStart() {
    // Create directories
    app.MakeDir("/sdcard/myl0n/");
    app.MakeDir("/sdcard/myl0n/Storage/Snaps/");
    
    // Initialize systems
    neuralNetwork = new NeuralNetwork(INPUT_COUNT);
    reflexSystem = new ReflexSystem();
    reflexSystem.loadReflexes();
    rewards = new RewardSystem();
    rewards.load();
    hardware = new HardwareInterface();
    
    // Load saved state
    try {
        const saved = app.ReadFile("/sdcard/myl0n/uncon.myl0n");
        if (saved) {
            neuralNetwork = NeuralNetwork.deserialize(JSON.parse(saved));
            app.ShowPopup("🧠 Neural network restored from memory");
        }
    } catch (e) {
        app.ShowPopup("Starting fresh neural network");
    }
    
    // UI Setup
    lay = app.CreateLayout("Linear", "VCenter,FillXY");
    lay.SetBackColor("#000010");
    image = app.CreateImage(null, 1.0, 1.0, "px", true);
    lay.AddChild(image);
    app.AddLayout(lay);
    
    // Voice setup
    speech = app.CreateSpeechRecog();
    speech.SetOnResult(speech_OnResult);
    
    // Welcome
    app.TextToSpeech("Welcome to H C I O S My L 0 n, version 2. " +
        "Neural network ready. O O D A loop active. " +
        "Ready to learn, Captain.", 
        VOICE_SPEED / 100, VOICE_PITCH / 100);
    
    // Initial render
    MandelbrotRender();
    
    // OODA Loop (every 5 seconds)
    app.SetInterval(() => OODALoop(), 5000);
    
    // Voice listening
    app.SetInterval(() => {
        if (!speech.IsListening()) {
            speech.Start();
        }
    }, 10000);
}

function speech_OnResult(results) {
    if (results && results.length > 0) {
        voiceInput = results[0];
        app.ShowPopup("You: " + voiceInput);
        processCommand(voiceInput);
    }
}

function OnReady() {
    // Auto-connect Arduino if available
    hardware.connectArduino(HW_ARDUINO_BT);
}

// ═══════════════════════════════════════════════════════════════════════════
// VOICE OUTPUT FUNCTION (Golden Ratio Modulated)
// ═══════════════════════════════════════════════════════════════════════════

function speak(text) {
    app.TextToSpeech(text, VOICE_SPEED / 100, VOICE_PITCH / 100);
}

// ═══════════════════════════════════════════════════════════════════════════
// CLEANUP
// ═══════════════════════════════════════════════════════════════════════════

function OnDestroy() {
    // Save state
    if (neuralNetwork) logUnconscious(neuralNetwork.serialize());
    if (rewards) rewards.save();
    if (reflexSystem) reflexSystem.saveReflexes();
    app.ShowPopup("MyL0n ROS: Memory saved. Goodbye, Captain!");
}
