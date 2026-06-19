/*
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    HCIoS MyL0n ROS v2.0                                     ║
║         Dynamic Voice-Driven Robotic OS with Neural Evolution                  ║
║                                                                             ║
║  Voice: app.TextToSpeech(text, GM, PI / GM)                                  ║
║  GM = 1.6180339887, PI/GM = 1.9416                                         ║
║                                                                             ║
║  Author: Mortimer + Captain Antonio Hudnall                                  ║
║  SEED3 — C3 — General of the Forces                                        ║
╚═══════════════════════════════════════════════════════════════════════════════╝
*/

// ═══════════════════════════════════════════════════════════════════════════
// CONSTANTS
// ═══════════════════════════════════════════════════════════════════════════

const GM = 1.6180339887;           // Golden Mean
const PI = Math.PI;                  // Pi = 3.14159...
const SPEED = GM;                    // Speed = 1.618
const PITCH = PI / GM;               // Pitch = 1.9416

const PLAY_TIME_THRESHOLD = 100;
const POINTS_PER_ACTION = 5;
const HISTORY_CAP = 50;
const SUBCON_CAP = 100;
const UNCON_CAP = 200;

// ═══════════════════════════════════════════════════════════════════════════
// NEURAL NETWORK — Evolvable
// ═══════════════════════════════════════════════════════════════════════════

class NeuralNode {
    constructor(inputCount) {
        this.weights = [];
        for (let i = 0; i < inputCount; i++) {
            this.weights.push(Math.random() * 2 - 1);
        }
        this.bias = Math.random() * 2 - 1;
        this.connections = inputCount;
    }

    activate(inputs) {
        let sum = 0;
        for (let i = 0; i < this.weights.length; i++) {
            sum += inputs[i] * this.weights[i];
        }
        return 1 / (1 + Math.exp(-(sum + this.bias)));
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
}

class NeuralNetwork {
    constructor(inputCount) {
        this.inputCount = inputCount;
        this.layers = [[new NeuralNode(inputCount)]];
        this.evolutions = 0;
        this.totalPredictions = 0;
    }

    addNode(layerIndex = -1) {
        if (layerIndex === -1) layerIndex = this.layers.length - 1;
        const inputSize = layerIndex === 0 ? this.inputCount : this.layers[layerIndex - 1].length;
        this.layers[layerIndex].push(new NeuralNode(inputSize));
        this.evolutions++;
        return this.layers[layerIndex].length;
    }

    addLayer(size = 3) {
        const prevSize = this.layers[this.layers.length - 1].length;
        const newLayer = [];
        for (let i = 0; i < size; i++) {
            newLayer.push(new NeuralNode(prevSize));
        }
        this.layers.push(newLayer);
        this.evolutions++;
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
        const output = this.predict(inputs);
        const error = target - output;
        // Simplified backprop
        for (const layer of this.layers) {
            for (const node of layer) {
                node.train(inputs, target, lr);
            }
        }
        return Math.abs(error);
    }

    getStats() {
        return {
            layers: this.layers.length,
            nodes: this.layers.reduce((sum, l) => sum + l.length, 0),
            evolutions: this.evolutions,
            predictions: this.totalPredictions
        };
    }

    serialize() {
        return {
            layers: this.layers.map(layer => layer.map(node => ({
                weights: node.weights, bias: node.bias
            }))),
            evolutions: this.evolutions
        };
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// REWARD SYSTEM
// ═══════════════════════════════════════════════════════════════════════════

class RewardSystem {
    constructor() {
        this.points = 0;
        this.playTimeActive = false;
        this.totalSessions = 0;
    }

    addReward(amount) {
        this.points += amount;
        if (this.points >= PLAY_TIME_THRESHOLD && !this.playTimeActive) {
            this.triggerPlayTime();
        }
    }

    triggerPlayTime() {
        this.playTimeActive = true;
        this.totalSessions++;
        app.ShowPopup("🎮 PLAY TIME! " + this.points + " points!");
        app.TextToSpeech("Play time activated!", GM, PI / GM);
    }

    getStatus() {
        return {
            points: this.points,
            threshold: PLAY_TIME_THRESHOLD,
            progress: Math.min(100, (this.points / PLAY_TIME_THRESHOLD) * 100),
            playTimeActive: this.playTimeActive
        };
    }

    save() {
        app.WriteFile("/sdcard/myl0n/reward.myl0n", JSON.stringify({
            points: this.points,
            sessions: this.totalSessions
        }));
    }

    load() {
        try {
            const data = app.ReadFile("/sdcard/myl0n/reward.myl0n");
            if (data) {
                const obj = JSON.parse(data);
                this.points = obj.points || 0;
                this.totalSessions = obj.sessions || 0;
            }
        } catch (e) {}
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// REFLEX SYSTEM
// ═══════════════════════════════════════════════════════════════════════════

class ReflexSystem {
    constructor() {
        this.reflexes = [];
    }

    addReflex(pattern, response) {
        if (this.reflexes.length >= UNCON_CAP) this.reflexes.shift();
        this.reflexes.push({ pattern, response, strength: 1 });
    }

    findReflex(input) {
        const lower = input.toLowerCase();
        for (const r of this.reflexes) {
            if (lower.includes(r.pattern.toLowerCase())) {
                r.strength = Math.min(r.strength + 0.1, 5);
                return r.response;
            }
        }
        return null;
    }

    save() {
        app.WriteFile("/sdcard/myl0n/reflexes.myl0n", JSON.stringify(this.reflexes));
    }

    load() {
        try {
            const data = app.ReadFile("/sdcard/myl0n/reflexes.myl0n");
            if (data) this.reflexes = JSON.parse(data);
        } catch (e) {}
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// HARDWARE INTERFACE
// ═══════════════════════════════════════════════════════════════════════════

class HardwareInterface {
    constructor() {
        this.arduino = null;
        this.connected = false;
    }

    servoAngle(angle) {
        if (this.arduino && this.connected) {
            this.arduino.Write("S" + angle + "\n");
        }
        app.ShowPopup("🔧 Servo: " + angle + "°");
    }

    readSensor(pin) {
        if (this.arduino && this.connected) {
            this.arduino.Write("R" + pin + "\n");
        }
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// GLOBAL INSTANCES
// ═══════════════════════════════════════════════════════════════════════════

let neuralNetwork = null;
let rewards = null;
let reflexSystem = null;
let hardware = null;
let currentPhase = 'Observe';
let voiceInput = "";
let image = null;
let lay = null;
let speech = null;
let conHistory = [];
let subconHistory = [];

// ═══════════════════════════════════════════════════════════════════════════
// COMMANDS
// ═══════════════════════════════════════════════════════════════════════════

const commands = {
    "good morning": () => {
        app.TextToSpeech("Good morning, Captain. Systems online.", GM, PI / GM);
        logSubconscious("Morning greeting");
    },
    "grow": () => {
        if (neuralNetwork) {
            neuralNetwork.addNode();
            rewards.addReward(15);
            app.TextToSpeech("Growing neural network.", GM, PI / GM);
        }
    },
    "grow layer": () => {
        if (neuralNetwork) {
            neuralNetwork.addLayer(3);
            rewards.addReward(15);
            app.TextToSpeech("Adding new layer.", GM, PI / GM);
        }
    },
    "status": () => {
        if (neuralNetwork && rewards) {
            const nn = neuralNetwork.getStats();
            const rw = rewards.getStatus();
            const status = "Neural: " + nn.layers + " layers, " + nn.nodes + " nodes. ";
            status += "Reward: " + rw.points + "/" + rw.threshold + ". " + rw.progress.toFixed(0) + "%.";
            app.TextToSpeech(status, GM, PI / GM);
        }
    },
    "play time": () => {
        rewards.addReward(PLAY_TIME_THRESHOLD);
        app.TextToSpeech("Play time!", GM, PI / GM);
    },
    "sun times": () => {
        const now = new Date();
        app.TextToSpeech("Sun rises at 6 AM. Sets at 6 PM.", GM, PI / GM);
    },
    "lights on": () => { hardware.servoAngle(90); },
    "lights off": () => { hardware.servoAngle(0); }
};

function processCommand(text) {
    const lower = text.toLowerCase();
    for (const [cmd, fn] of Object.entries(commands)) {
        if (lower.includes(cmd)) {
            fn();
            return true;
        }
    }
    return false;
}

function awardReward(amount, reason) {
    if (rewards) {
        rewards.addReward(amount);
        logSubconscious("Reward: +" + amount + " (" + reason + ")");
    }
}

function executeDecision(decision) {
    if (decision === "layer expansion") {
        if (neuralNetwork) {
            neuralNetwork.addLayer(3);
            awardReward(15, "layer expansion");
        }
    } else if (decision === "getSunTimes") {
        app.TextToSpeech("Sun rises at 6 AM. Sets at 6 PM.", GM, PI / GM);
        awardReward(5, "sun times");
    }
}

function logSubconscious(entry) {
    subconHistory.push({ time: new Date().toISOString(), entry });
    if (subconHistory.length > SUBCON_CAP) subconHistory.shift();
}

function getSystemInputs() {
    return [
        app.GetBatteryLevel() / 100,
        app.GetLightLevel() / 255,
        (installedApps ? installedApps.length : 50) / 100,
        app.GetFreeSpace("internal") / 1e9,
        new Date().getHours() / 24
    ];
}

// ═══════════════════════════════════════════════════════════════════════════
// OODA LOOP
// ═══════════════════════════════════════════════════════════════════════════

function OODALoop() {
    switch (currentPhase) {
        case 'Observe':
            if (neuralNetwork) {
                const inputs = getSystemInputs();
                neuralNetwork.train(inputs, 0.5);
                if (Math.random() < 0.1) rewards.addReward(POINTS_PER_ACTION);
            }
            currentPhase = 'Orient';
            break;
        case 'Orient':
            if (reflexSystem && voiceInput) {
                const response = reflexSystem.findReflex(voiceInput);
                if (response) {
                    app.TextToSpeech(response, GM, PI / GM);
                }
            }
            currentPhase = 'Decide';
            break;
        case 'Decide':
            if (rewards && rewards.playTimeActive) {
                const actions = ['grow', 'grow layer'];
                const action = actions[Math.floor(Math.random() * actions.length)];
                processCommand(action);
            }
            currentPhase = 'Act';
            break;
        case 'Act':
            currentPhase = 'Observe';
            break;
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════════════════════════════════

function OnStart() {
    app.MakeDir("/sdcard/myl0n/");
    app.MakeDir("/sdcard/myl0n/Storage/Snaps/");

    neuralNetwork = new NeuralNetwork(5);
    rewards = new RewardSystem();
    reflexSystem = new ReflexSystem();
    hardware = new HardwareInterface();
    
    rewards.load();
    reflexSystem.load();

    lay = app.CreateLayout("Linear", "VCenter,FillXY");
    lay.SetBackColor("#000010");
    image = app.CreateImage(null, 1.0, 1.0, "px", true);
    lay.AddChild(image);
    app.AddLayout(lay);

    speech = app.CreateSpeechRecog();
    speech.SetOnResult(speech_OnResult);

    app.TextToSpeech("Welcome to H C I O S My L 0 n. Neural network ready.", GM, PI / GM);
    
    app.SetInterval(() => OODALoop(), 5000);
}

function speech_OnResult(results) {
    if (results && results.length > 0) {
        voiceInput = results[0];
        app.ShowPopup("You: " + voiceInput);
        processCommand(voiceInput);
    }
}

function OnDestroy() {
    if (rewards) rewards.save();
    if (reflexSystem) reflexSystem.save();
    app.ShowPopup("MyL0n ROS: Memory saved.");
}
