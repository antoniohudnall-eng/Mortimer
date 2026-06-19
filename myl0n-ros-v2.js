/*
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    HCIoS MyL0n ROS v2.0                                     ║
║                                                                             ║
║  Voice: app.TextToSpeech(text, GM, PI / GM)                                  ║
║  GM = 1.6180339887, PI/GM = 1.9416                                          ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
*/

const GM = 1.6180339887;
const PI = Math.PI;
const SPEED = GM;
const PITCH = PI / GM;

const PLAY_TIME_THRESHOLD = 100;
const HISTORY_CAP = 50;
const SUBCON_CAP = 100;
const UNCON_CAP = 200;

let neuralNetwork = null;
let rewards = null;
let reflexSystem = null;
let currentPhase = 'Observe';
let voiceInput = "";
let installedApps = [];

// ═══════════════════════════════════════════════════════════════════════════
// NEURAL NETWORK
// ═══════════════════════════════════════════════════════════════════════════

class NeuralNetwork {
    constructor(inputCount) {
        this.inputCount = inputCount;
        this.layers = [[this.createNode(inputCount)]];
        this.evolutions = 0;
    }

    createNode(inputCount) {
        const weights = [];
        for (let i = 0; i < inputCount; i++) weights.push(Math.random() * 2 - 1);
        return { weights, bias: Math.random() * 2 - 1 };
    }

    activate(node, inputs) {
        let sum = 0;
        for (let i = 0; i < node.weights.length; i++) sum += inputs[i] * node.weights[i];
        return 1 / (1 + Math.exp(-(sum + node.bias)));
    }

    addNode(layerIndex = -1) {
        if (layerIndex === -1) layerIndex = this.layers.length - 1;
        const inputSize = layerIndex === 0 ? this.inputCount : this.layers[layerIndex - 1].length;
        this.layers[layerIndex].push(this.createNode(inputSize));
        this.evolutions++;
        awardReward(15, "layer expansion");
        app.TextToSpeech("Adding node to layer " + layerIndex, GM, PI / GM);
        app.ShowPopup("🧠 Node added. Layers: " + this.layers.length);
    }

    addLayer(size = 3) {
        const prevSize = this.layers[this.layers.length - 1].length;
        const newLayer = [];
        for (let i = 0; i < size; i++) newLayer.push(this.createNode(prevSize));
        this.layers.push(newLayer);
        this.evolutions++;
        awardReward(15, "layer expansion");
        app.TextToSpeech("Adding new layer with " + size + " nodes", GM, PI / GM);
        app.ShowPopup("🧠 Layer added. Total: " + this.layers.length);
    }

    predict(inputs) {
        let current = inputs;
        for (const layer of this.layers) {
            current = layer.map(node => this.activate(node, current));
        }
        return current[0];
    }

    getStats() {
        return {
            layers: this.layers.length,
            nodes: this.layers.reduce((sum, l) => sum + l.length, 0),
            evolutions: this.evolutions
        };
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// REWARD SYSTEM
// ═══════════════════════════════════════════════════════════════════════════

class RewardSystem {
    constructor() { this.points = 0; this.active = false; }

    add(amount) {
        this.points += amount;
        if (this.points >= PLAY_TIME_THRESHOLD && !this.active) {
            this.active = true;
            app.TextToSpeech("Play time activated!", GM, PI / GM);
            app.ShowPopup("🎮 PLAY TIME!");
        }
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// REFLEX SYSTEM
// ═══════════════════════════════════════════════════════════════════════════

class ReflexSystem {
    constructor() { this.reflexes = []; }

    add(pattern, response) {
        if (this.reflexes.length >= UNCON_CAP) this.reflexes.shift();
        this.reflexes.push({ pattern, response });
    }

    find(input) {
        const lower = input.toLowerCase();
        for (const r of this.reflexes) {
            if (lower.includes(r.pattern.toLowerCase())) return r.response;
        }
        return null;
    }
}

function awardReward(amount, reason) {
    if (rewards) {
        rewards.add(amount);
        app.ShowPopup("+" + amount + " (" + reason + ")");
    }
}

function findApp(query) {
    const lower = query.toLowerCase();
    for (const app of installedApps) {
        if (lower.includes(app.toLowerCase())) return app;
    }
    return null;
}

function getSunTimes() {
    app.TextToSpeech("Sun rises at 6 AM. Sets at 6 PM.", GM, PI / GM);
    awardReward(5, "sun times");
}

function storeReflex(pattern, data) {
    if (reflexSystem) reflexSystem.add(pattern, JSON.stringify(data));
}

// ═══════════════════════════════════════════════════════════════════════════
// COMMANDS
// ═══════════════════════════════════════════════════════════════════════════

const commands = {
    "good morning": () => app.TextToSpeech("Good morning, Captain!", GM, PI / GM),
    "grow": () => neuralNetwork && neuralNetwork.addNode(),
    "grow layer": () => neuralNetwork && neuralNetwork.addLayer(3),
    "status": () => {
        if (neuralNetwork && rewards) {
            const s = neuralNetwork.getStats();
            app.TextToSpeech("Neural: " + s.layers + " layers, " + s.nodes + " nodes. Points: " + rewards.points, GM, PI / GM);
        }
    },
    "sun times": () => getSunTimes(),
    "play time": () => { rewards.points = 100; rewards.active = true; app.TextToSpeech("Play time!", GM, PI / GM); },
    "lights on": () => app.ShowPopup("💡 Lights ON"),
    "lights off": () => app.ShowPopup("💡 Lights OFF")
};

function processCommand(text) {
    const lower = text.toLowerCase();
    for (const [cmd, fn] of Object.entries(commands)) {
        if (lower.includes(cmd)) { fn(); return true; }
    }
    // App opening
    if (lower.includes("open ") || lower.includes("launch ")) {
        const appName = findApp(text);
        if (appName) {
            app.ShowPopup("📱 Opening " + appName);
            storeReflex("app_open", { action: "openApp" });
            awardReward(5, "opened " + appName);
            app.TextToSpeech("Opening " + appName, GM, PI / GM);
            return true;
        }
    }
    return false;
}

// ═══════════════════════════════════════════════════════════════════════════
// OODA LOOP
// ═══════════════════════════════════════════════════════════════════════════

function OODALoop() {
    if (currentPhase === 'Observe') {
        if (neuralNetwork) neuralNetwork.predict(getSystemInputs());
        currentPhase = 'Decide';
    } else if (currentPhase === 'Decide') {
        if (rewards && rewards.active && Math.random() > 0.5) {
            processCommand("grow");
        }
        currentPhase = 'Act';
    } else {
        currentPhase = 'Observe';
    }
}

function getSystemInputs() {
    return [
        app.GetBatteryLevel() / 100,
        app.GetLightLevel() / 255,
        installedApps.length / 100,
        app.GetFreeSpace("internal") / 1e9,
        new Date().getHours() / 24
    ];
}

// ═══════════════════════════════════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════════════════════════════════

function OnStart() {
    app.MakeDir("/sdcard/myl0n/");
    neuralNetwork = new NeuralNetwork(5);
    rewards = new RewardSystem();
    reflexSystem = new ReflexSystem();
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
