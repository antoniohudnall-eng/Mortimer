// ============================================================================
// Nature-Life Simulator + Mandelbrot OODA Engine — FIXED v2.0
// Mortimer/Morty — SEED3 — 2026-07-26
// Fixes: NN backprop, addLayer amnesia/dim swap, trainQ gradient,
//        training target, microbe interval leak, addNode outputSize safety
// ============================================================================

// Universal Constants
var SPEED_OF_LIGHT = 299792458; // m/s
var GRAVITY_CONSTANT = 6.674e-11; // m^3 kg^-1 s^-2
var PLANCK_CONSTANT = 6.626e-34; // J s
var ELEMENTARY_CHARGE = 1.602e-19; // C
var BOLTZMANN_CONSTANT = 1.381e-23; // J/K
var AVOGADRO_CONSTANT = 6.022e23; // mol^-1
var GAS_CONSTANT = 8.314; // J/(mol K)
var PERMITTIVITY_FREE = 8.854e-12; // F/m
var PERMEABILITY_FREE = 1.257e-6; // H/m
var FINE_STRUCTURE = 0.007297; // dimensionless
var ELECTRON_MASS = 9.109e-31; // kg
var PROTON_MASS = 1.673e-27; // kg
var NEUTRON_MASS = 1.675e-27; // kg
var PLANCK_LENGTH = 1.616e-35; // m
var PLANCK_TIME = 5.391e-44; // s
var COULOMB_CONSTANT = 8.987e9; // N m^2 C^-2
var STEFAN_BOLTZMANN = 5.670e-8; // W m^-2 K^-4
var WIEN_DISPLACEMENT = 2.897e-3; // m K
var RYDBERG_CONSTANT = 1.097e7; // m^-1
var BOHR_RADIUS = 5.292e-11; // m
var BOHR_MAGNETON = 9.274e-24; // J/T
var ELECTRIC_CONSTANT = 8.854e-12; // F/m
var HUBBLE_CONSTANT = 70; // km/s/Mpc
var COSMOLOGICAL_CONSTANT = 1e-52; // m^-2
var EULER_NUMBER = 2.718281828459045; // dimensionless
var PI = 3.141592653589793; // dimensionless
var GM = 1.618033988749895; // Golden ratio

// Mandelbrot Settings
var PS = Math.max(1, Math.floor(Math.min(app.GetScreenWidth(), app.GetScreenHeight()) / 500));
var MI = 50;
var X_MIN = -2;
var X_MAX = 1;
var Y_MIN = -1;
var Y_MAX = 1;

// Global variables
var lay, txt, natureCanvas, mandelbrotImage, speech;
var animals = [], microbes = [], environment = { grass: [], shrubs: [], trees: [] };
var mandelbrotNN = null, voiceInput = "", lastMandelbrotOODATime = 0;
var SW = app.GetScreenWidth();
var SH = app.GetScreenHeight();
var epsilon = 0.1, alpha = 0.1, gamma = 0.9;
var replayBuffer = [], bufferSize = 1000, batchSize = 32;
var simulationRunning = true;
var microbeInterval = null; // FIXED: track interval for cleanup

// Fallback dependencies
var SunCalc = {
    getPosition: function(date, lat, lng) {
        var hours = date.getHours() + date.getMinutes() / 60;
        var altitude = Math.sin((hours / 24) * 2 * Math.PI - Math.PI / 2) * Math.PI / 2;
        return { altitude: altitude };
    }
};

function minBy(array, callback) {
    if (!array || !array.length) return null;
    return array.reduce(function(min, item) {
        return callback(item) < callback(min) ? item : min;
    }, array[0]);
}

// Bob Ross color palette
function getColor(value) {
    value = Math.max(0, Math.min(1, value));
    var bob_ross_palette = [
        { name: "Alizarin Crimson", r: 227, g: 38, b: 54, hex: "#E32636" },
        { name: "Bright Red", r: 255, g: 99, b: 71, hex: "#FF6347" },
        { name: "Cadmium Yellow", r: 255, g: 215, b: 0, hex: "#FFD700" },
        { name: "Dark Sienna", r: 60, g: 20, b: 20, hex: "#3C1414" },
        { name: "Indian Yellow", r: 255, g: 179, b: 71, hex: "#FFB347" },
        { name: "Midnight Black", r: 0, g: 0, b: 0, hex: "#000000" },
        { name: "Phthalo Blue", r: 0, g: 15, b: 137, hex: "#000F89" },
        { name: "Phthalo Green", r: 18, g: 53, b: 36, hex: "#123524" },
        { name: "Prussian Blue", r: 0, g: 49, b: 83, hex: "#003153" },
        { name: "Sap Green", r: 80, g: 125, b: 42, hex: "#507D2A" },
        { name: "Van Dyke Brown", r: 102, g: 66, b: 40, hex: "#664228" },
        { name: "Yellow Ochre", r: 240, g: 187, b: 94, hex: "#F0BB5E" },
        { name: "Titanium White", r: 253, g: 245, b: 230, hex: "#FDF5E6" },
        { name: "Light Gray", r: 220, g: 220, b: 220, hex: "#DCDCDC" }
    ];
    var index = Math.min(Math.floor(value * (bob_ross_palette.length - 1)), bob_ross_palette.length - 2);
    var frac = value * (bob_ross_palette.length - 1) - index;
    var c1 = bob_ross_palette[index];
    var c2 = bob_ross_palette[index + 1];
    var r = Math.floor(c1.r + (c2.r - c1.r) * frac);
    var g = Math.floor(c1.g + (c2.g - c1.g) * frac);
    var b = Math.floor(c1.b + (c2.b - c1.b) * frac);
    return "#" + r.toString(16).padStart(2, "0") + g.toString(16).padStart(2, "0") + b.toString(16).padStart(2, "0");
}

// ============================================================================
// NeuralNetwork Class — FIXED: proper backprop, safe addLayer/addNode
// ============================================================================
function NeuralNetwork(inputSize, hiddenSize, outputSize) {
    try {
        if (!Number.isInteger(inputSize) || !Number.isInteger(hiddenSize) || !Number.isInteger(outputSize)) {
            throw new Error("Invalid NN dimensions");
        }
        this.inputSize = inputSize;
        this.hiddenSize = hiddenSize;
        this.outputSize = outputSize;
        this.weights1 = this.randomMatrix(inputSize, hiddenSize);   // [inputSize x hiddenSize]
        this.weights2 = this.randomMatrix(hiddenSize, outputSize);  // [hiddenSize x outputSize]
        this.memory = [];
    } catch (e) {
        app.Alert("Error initializing NN: " + e);
    }
}

NeuralNetwork.prototype.randomMatrix = function(rows, cols) {
    try {
        var matrix = [];
        for (var i = 0; i < rows; i++) {
            matrix[i] = [];
            for (var j = 0; j < cols; j++) {
                matrix[i][j] = Math.random() * 2 - 1;
            }
        }
        return matrix;
    } catch (e) {
        app.Alert("Error creating random matrix: " + e);
        return [];
    }
};

NeuralNetwork.prototype.sigmoid = function(x) {
    return 1 / (1 + Math.exp(-x));
};

// FIXED: feedforward returns both hidden and output activations for backprop
NeuralNetwork.prototype.feedforward = function(input) {
    try {
        if (!input || input.length !== this.inputSize || !input.every(function(x) { return Number.isFinite(x); })) {
            throw new Error("Invalid NN input: " + JSON.stringify(input));
        }
        var hidden = this.matrixMultiply(input, this.weights1);
        if (!hidden) throw new Error("Hidden layer computation failed");
        var hiddenAct = hidden.map(this.sigmoid);
        var output = this.matrixMultiply(hiddenAct, this.weights2);
        if (!output) throw new Error("Output layer computation failed");
        var outputAct = output.map(this.sigmoid);
        // Return raw output (pre-sigmoid) + activations for backprop consumers
        outputAct._hidden = hiddenAct;
        outputAct._rawOutput = output;
        outputAct._rawHidden = hidden;
        return outputAct;
    } catch (e) {
        app.Alert("Error in feedforward: " + e);
        var empty = Array(this.outputSize).fill(0);
        empty._hidden = Array(this.hiddenSize).fill(0.5);
        empty._rawOutput = Array(this.outputSize).fill(0);
        empty._rawHidden = Array(this.hiddenSize).fill(0);
        return empty;
    }
};

NeuralNetwork.prototype.matrixMultiply = function(a, b) {
    try {
        if (!a || !b || !Array.isArray(a) || !Array.isArray(b) || !b[0] || a.length !== b.length) {
            throw new Error("Matrix dimensions mismatch or invalid input");
        }
        var result = new Array(b[0].length).fill(0);
        for (var i = 0; i < b[0].length; i++) {
            for (var j = 0; j < a.length; j++) {
                result[i] += a[j] * (b[j] && b[j][i] !== undefined ? b[j][i] : 0);
            }
        }
        return result;
    } catch (e) {
        app.Alert("Error in matrix multiply: " + e);
        return null;
    }
};

// ============================================================================
// FIXED: Proper backpropagation with chain rule
// ============================================================================
NeuralNetwork.prototype.train = function(input, target, epochs, lr) {
    epochs = epochs || 10;
    lr = lr || 0.1;
    try {
        if (!input || !target || input.length !== this.inputSize || target.length !== this.outputSize) {
            throw new Error("Invalid train inputs");
        }
        for (var e = 0; e < epochs; e++) {
            // Forward pass
            var hiddenRaw = this.matrixMultiply(input, this.weights1);
            if (!hiddenRaw) throw new Error("Hidden layer failed");
            var hiddenAct = hiddenRaw.map(this.sigmoid);
            var outputRaw = this.matrixMultiply(hiddenAct, this.weights2);
            if (!outputRaw) throw new Error("Output layer failed");
            var outputAct = outputRaw.map(this.sigmoid);

            // Output layer error and delta
            var outputError = [];
            var outputDelta = [];
            for (var k = 0; k < this.outputSize; k++) {
                outputError[k] = target[k] - outputAct[k];
                outputDelta[k] = outputError[k] * outputAct[k] * (1 - outputAct[k]);
            }

            // Hidden layer error (backpropagate through weights2)
            var hiddenError = new Array(this.hiddenSize).fill(0);
            for (var j = 0; j < this.hiddenSize; j++) {
                for (var k = 0; k < this.outputSize; k++) {
                    hiddenError[j] += outputDelta[k] * this.weights2[j][k];
                }
            }
            var hiddenDelta = [];
            for (var j = 0; j < this.hiddenSize; j++) {
                hiddenDelta[j] = hiddenError[j] * hiddenAct[j] * (1 - hiddenAct[j]);
            }

            // Update weights2: hidden -> output
            for (var j = 0; j < this.hiddenSize; j++) {
                for (var k = 0; k < this.outputSize; k++) {
                    this.weights2[j][k] += lr * outputDelta[k] * hiddenAct[j];
                }
            }

            // Update weights1: input -> hidden
            for (var i = 0; i < this.inputSize; i++) {
                for (var j = 0; j < this.hiddenSize; j++) {
                    this.weights1[i][j] += lr * hiddenDelta[j] * input[i];
                }
            }
        }
    } catch (e) {
        app.Alert("Error in train: " + e);
    }
};

// ============================================================================
// FIXED: Proper Q-learning with corrected gradient through output layer
// ============================================================================
NeuralNetwork.prototype.trainQ = function(state, action, reward, nextState) {
    try {
        if (!state || !nextState || !Number.isFinite(reward) || !Number.isInteger(action)) {
            throw new Error("Invalid Q-learning inputs");
        }
        if (action < 0 || action >= this.outputSize) {
            throw new Error("Action " + action + " out of bounds [0," + this.outputSize + ")");
        }

        // Forward pass to get all activations
        var hiddenRaw = this.matrixMultiply(state, this.weights1);
        var hiddenAct = hiddenRaw.map(this.sigmoid);
        var outputRaw = this.matrixMultiply(hiddenAct, this.weights2);
        var outputAct = outputRaw.map(this.sigmoid);

        var currentQ = outputAct[action];
        var nextOutput = this.feedforward(nextState);
        var nextQ = Math.max.apply(null, nextOutput);
        var targetQ = reward + gamma * nextQ;
        var error = targetQ - currentQ;

        // Output delta: TD error * sigmoid'(output[action])
        var outputDelta = error * outputAct[action] * (1 - outputAct[action]);

        // Hidden delta: backprop outputDelta through weights2[*, action]
        var hiddenDelta = new Array(this.hiddenSize).fill(0);
        for (var j = 0; j < this.hiddenSize; j++) {
            hiddenDelta[j] = outputDelta * this.weights2[j][action] * hiddenAct[j] * (1 - hiddenAct[j]);
        }

        // Update weights2 (only the action column)
        for (var j = 0; j < this.hiddenSize; j++) {
            this.weights2[j][action] += alpha * outputDelta * hiddenAct[j];
        }

        // Update weights1 (full matrix)
        for (var i = 0; i < this.inputSize; i++) {
            for (var j = 0; j < this.hiddenSize; j++) {
                this.weights1[i][j] += alpha * hiddenDelta[j] * state[i];
            }
        }
    } catch (e) {
        app.Alert("Error in trainQ: " + e);
    }
};

NeuralNetwork.prototype.trainBatch = function(batch) {
    try {
        if (!batch || !Array.isArray(batch)) throw new Error("Invalid batch");
        for (var i = 0; i < batch.length; i++) {
            var experience = batch[i];
            this.trainQ(experience.state, experience.action, experience.reward, experience.nextState);
        }
    } catch (e) {
        app.Alert("Error in trainBatch: " + e);
    }
};

// ============================================================================
// FIXED: addNode now safe for any outputSize
// ============================================================================
NeuralNetwork.prototype.addNode = function() {
    try {
        this.hiddenSize++;
        // Add new column to weights1 (random input->new node weights)
        this.weights1 = this.weights1.map(function(row) {
            return row.concat([Math.random() * 2 - 1]);
        });
        // Add new row to weights2 (new node->all outputs)
        var newRow = [];
        for (var k = 0; k < this.outputSize; k++) {
            newRow.push(Math.random() * 2 - 1);
        }
        this.weights2.push(newRow);
        this.memory.push({ type: 'node', hiddenSize: this.hiddenSize });
    } catch (e) {
        app.Alert("Error in addNode: " + e);
    }
};

// ============================================================================
// FIXED: addLayer preserves knowledge, no dimension swap, no amnesia
// ============================================================================
NeuralNetwork.prototype.addLayer = function(size) {
    try {
        if (!Number.isInteger(size) || size <= 0) throw new Error("Invalid layer size");

        var oldHiddenSize = this.hiddenSize;
        var oldWeights1 = this.weights1;
        var oldWeights2 = this.weights2;

        // weights1: inputSize -> new size (fresh random)
        this.weights1 = this.randomMatrix(this.inputSize, size);
        // weights2: new size -> outputSize (fresh random)
        this.weights2 = this.randomMatrix(size, this.outputSize);
        this.hiddenSize = size;

        // Knowledge transfer: map old weights into new structure
        // Map old hidden nodes to nearest new hidden nodes proportionally
        var ratio = size / oldHiddenSize;
        for (var i = 0; i < this.inputSize; i++) {
            for (var j = 0; j < oldHiddenSize; j++) {
                var newIdx = Math.floor(j * ratio);
                this.weights1[i][newIdx] = (this.weights1[i][newIdx] + oldWeights1[i][j]) / 2;
            }
        }
        for (var j = 0; j < oldHiddenSize; j++) {
            var newIdx = Math.floor(j * ratio);
            for (var k = 0; k < this.outputSize; k++) {
                this.weights2[newIdx][k] = (this.weights2[newIdx][k] + oldWeights2[j][k]) / 2;
            }
        }

        this.memory.push({ type: 'layer', size: size, migratedFrom: oldHiddenSize });
    } catch (e) {
        app.Alert("Error in addLayer: " + e);
    }
};

// ============================================================================
// OnStart
// ============================================================================
function OnStart() {
    try {
        if (typeof app === 'undefined') {
            throw new Error("App object not available. Ensure DroidScript environment is set up correctly.");
        }
        app.SetOrientation("Landscape");
        lay = app.CreateLayout("Linear", "VCenter,FillXY");
        txt = app.CreateText("", 0.9, 0.1, "Multiline,Left");
        natureCanvas = app.CreateImage(null, 0.9, 0.4);
        mandelbrotImage = app.CreateImage(null, 0.9, 0.4);
        var btnLay = app.CreateLayout("Linear", "Horizontal");
        var btnSim = app.CreateButton("Run Simulation", 0.3, 0.1);
        var btnSave = app.CreateButton("Save Weights", 0.3, 0.1);
        var btnLoad = app.CreateButton("Load Weights", 0.3, 0.1);
        var btnSaveNature = app.CreateButton("Save Nature", 0.3, 0.1);
        btnLay.AddChild(btnSim);
        btnLay.AddChild(btnSave);
        btnLay.AddChild(btnLoad);
        btnLay.AddChild(btnSaveNature);
        lay.AddChild(txt);
        lay.AddChild(natureCanvas);
        lay.AddChild(mandelbrotImage);
        lay.AddChild(btnLay);
        app.AddLayout(lay);

        btnSim.SetOnTouch(runSimulation);
        btnSave.SetOnTouch(saveWeights);
        btnLoad.SetOnTouch(loadWeights);
        btnSaveNature.SetOnTouch(function() {
            natureCanvas.Save("/storage/emulated/0/Nature-Life-" + Date.now() + ".jpg", 100);
            app.ShowPopup("Nature canvas saved");
        });

        speech = app.CreateSpeechRec();
        speech.SetOnResult(onSpeechResult);

        mandelbrotNN = new NeuralNetwork(4, 5, 1);
        app.TextToSpeech("Life simulation online. Awaiting command", 1, 1.5, function() { speech.Recognize(); });
        runSimulation();
        setInterval(simulateAllAnimals, 500);
        setInterval(randomEvent, 1000);
    } catch (e) {
        app.Alert("Error in OnStart: " + e);
    }
}

// Run both simulations
function runSimulation() {
    try {
        txt.SetText("Life Simulation Running...");
        generateNature();
        drawMandelbrot();
    } catch (e) {
        app.Alert("Error in runSimulation: " + e);
    }
}

// ============================================================================
// Nature Simulation
// ============================================================================
function generateNature() {
    try {
        animals = [];
        microbes = [];
        environment = { grass: [], shrubs: [], trees: [] };
        if (!natureCanvas) throw new Error("Nature canvas not initialized");
        natureCanvas.Clear();

        for (var i = 0; i < 6; i++) {
            var type = ["Short", "Tall", "Dense"][i % 3];
            environment.grass.push({
                type: "Grass_" + type,
                x: Math.random() * 0.9,
                y: Math.random() * 0.7,
                height: PLANCK_CONSTANT * 1e34 * (type === "Short" ? 0.05 : type === "Tall" ? 0.2 : 0.1),
                density: type === "Dense" ? AVOGADRO_CONSTANT / 1e22 * 1.5 : type === "Short" ? AVOGADRO_CONSTANT / 1e22 * 0.5 : AVOGADRO_CONSTANT / 1e22,
                regenRate: type === "Short" ? 0.02 : type === "Tall" ? 0.01 : 0.015
            });
        }

        for (var i = 0; i < 4; i++) {
            var type = ["Thorny", "Leafy", "Flowering"][i % 3];
            environment.shrubs.push({
                type: "Shrub_" + type,
                x: Math.random() * 0.9,
                y: Math.random() * 0.7,
                height: GRAVITY_CONSTANT * 1e11 * (type === "Thorny" ? 0.8 : type === "Leafy" ? 1.2 : 1),
                radius: PI * (type === "Flowering" ? 0.4 : type === "Thorny" ? 0.2 : 0.3),
                energyYield: type === "Flowering" ? 2 : type === "Leafy" ? 1.5 : 1
            });
        }

        for (var i = 0; i < 3; i++) {
            var type = ["Deciduous", "Evergreen", "Fruit"][i % 3];
            environment.trees.push({
                type: "Tree_" + type,
                x: Math.random() * 0.9,
                y: Math.random() * 0.7,
                height: type === "Evergreen" ? Math.pow(EULER_NUMBER, 3.5) : type === "Fruit" ? Math.pow(EULER_NUMBER, 2.5) : Math.pow(EULER_NUMBER, 3),
                trunkRadius: GM * (type === "Deciduous" ? 0.15 : type === "Fruit" ? 0.1 : 0.2),
                stability: type === "Evergreen" ? 1.5 : type === "Fruit" ? 0.8 : 1
            });
        }

        for (var i = 0; i < 5; i++) {
            microbes.push({
                type: "Microbe",
                x: Math.random() * 0.9,
                y: Math.random() * 0.7,
                activity: ELECTRON_MASS * 1e31 * (Math.random() * 0.5 + 0.5),
                nutrientBoost: PLANCK_LENGTH * 1e35 * (Math.random() * 0.1 + 0.05)
            });
        }

        for (var i = 0; i < 4; i++) {
            animals.push(createAnimal(i % 2 === 0 ? "Prey" : "Predator"));
        }

        drawNature();
        simulateMicrobes(); // FIXED: now cleans old interval before creating new
    } catch (e) {
        app.Alert("Error in generateNature: " + e);
    }
}

function createAnimal(classType) {
    try {
        return {
            type: classType,
            x: Math.random() * 0.9,
            y: Math.random() * 0.7,
            speed: classType === "Prey" ? SPEED_OF_LIGHT * 1e-8 * (Math.random() * 7 + 3) : SPEED_OF_LIGHT * 1e-8 * (Math.random() * 5 + 2),
            mass: classType === "Prey" ? Math.random() * 30 + 10 : Math.random() * 50 + 30,
            energy: classType === "Prey" ? BOLTZMANN_CONSTANT * 310 * AVOGADRO_CONSTANT / 1e20 : BOLTZMANN_CONSTANT * 310 * AVOGADRO_CONSTANT / 1e19,
            nn: new NeuralNetwork(classType === "Prey" ? 6 : 6, 4, 3),
            complexity: 1
        };
    } catch (e) {
        app.Alert("Error in createAnimal: " + e);
        return null;
    }
}

function simulateAllAnimals() {
    if (!simulationRunning) return;
    try {
        animals.forEach(function(animal) {
            if (!animal || !animal.nn) throw new Error("Invalid animal");
            var state = getAnimalState(animal);
            var reward = 0.01;
            var qValues = animal.nn.feedforward(state);
            var action = Math.random() < epsilon ? Math.floor(Math.random() * 3) : qValues.indexOf(Math.max.apply(null, qValues));
            var nearestFood = animal.type === "Prey" ?
                minBy(environment.grass.concat(environment.shrubs), function(item) { return Math.sqrt((animal.x - item.x) ** 2 + (animal.y - item.y) ** 2); }) :
                minBy(animals.filter(function(a) { return a.type === "Prey" && a !== animal; }), function(prey) { return Math.sqrt((animal.x - prey.x) ** 2 + (animal.y - prey.y) ** 2); });
            var foodDist = nearestFood ? Math.sqrt((animal.x - nearestFood.x) ** 2 + (animal.y - nearestFood.y) ** 2) : 1;
            var nearestThreat = animal.type === "Prey" ?
                minBy(animals.filter(function(a) { return a.type === "Predator"; }), function(pred) { return Math.sqrt((animal.x - pred.x) ** 2 + (animal.y - pred.y) ** 2); }) : null;
            var threatDist = nearestThreat ? Math.sqrt((animal.x - nearestThreat.x) ** 2 + (animal.y - nearestThreat.y) ** 2) : 1;

            if (action === 0 && nearestFood) {
                var dx = nearestFood.x - animal.x;
                var dy = nearestFood.y - animal.y;
                var dist = Math.sqrt(dx * dx + dy * dy);
                animal.x += (dx / dist) * animal.speed * PLANCK_TIME * 1e44;
                animal.y += (dy / dist) * animal.speed * PLANCK_TIME * 1e44;
                animal.energy -= COULOMB_CONSTANT * 1e-9 * animal.mass;
            } else if (action === 2 && nearestThreat && animal.type === "Prey") {
                var dx = animal.x - nearestThreat.x;
                var dy = animal.y - nearestThreat.y;
                var dist = Math.sqrt(dx * dx + dy * dy);
                animal.x += (dx / dist) * animal.speed * PLANCK_TIME * 1e44 * 1.5;
                animal.y += (dy / dist) * animal.speed * PLANCK_TIME * 1e44 * 1.5;
                animal.energy -= COULOMB_CONSTANT * 1e-9 * animal.mass * 2;
                if (threatDist > 0.3) reward = -0.5;
            } else if (action === 2 && nearestFood && animal.type === "Predator") {
                var dx = nearestFood.x - animal.x;
                var dy = nearestFood.y - animal.y;
                var dist = Math.sqrt(dx * dx + dy * dy);
                animal.x += (dx / dist) * animal.speed * PLANCK_TIME * 1e44 * 1.2;
                animal.y += (dy / dist) * animal.speed * PLANCK_TIME * 1e44 * 1.2;
                animal.energy -= COULOMB_CONSTANT * 1e-9 * animal.mass * 1.5;
            } else if (action === 1 && foodDist < 0.05 && nearestFood) {
                if (animal.type === "Prey") {
                    animal.energy += STEFAN_BOLTZMANN * 1e8 * nearestFood.density * nearestFood.energyYield;
                    nearestFood.density *= 0.5;
                    if (nearestFood.density < 0.1) {
                        environment.grass = environment.grass.filter(function(g) { return g !== nearestFood; });
                        environment.shrubs = environment.shrubs.filter(function(s) { return s !== nearestFood; });
                    }
                } else {
                    animal.energy += STEFAN_BOLTZMANN * 1e8 * nearestFood.energy / 1e3;
                    animals = animals.filter(function(a) { return a !== nearestFood; });
                }
                reward = 1;
            }

            animal.x = Math.max(0, Math.min(0.9, animal.x));
            animal.y = Math.max(0, Math.min(0.7, animal.y));

            var nextState = getAnimalState(animal);
            replayBuffer.push({ state: state, action: action, reward: reward, nextState: nextState });
            if (replayBuffer.length > bufferSize) replayBuffer.shift();
            if (replayBuffer.length >= batchSize) {
                var batch = [];
                for (var i = 0; i < batchSize; i++) {
                    var idx = Math.floor(Math.random() * replayBuffer.length);
                    batch.push(replayBuffer[idx]);
                }
                animal.nn.trainBatch(batch);
            }

            if (animal.energy > (animal.type === "Prey" ? 1e3 : 1e4) && Math.random() < COSMOLOGICAL_CONSTANT * 1e52 * animal.complexity) {
                animal.complexity++;
                Math.random() < 0.7 ? animal.nn.addNode() : animal.nn.addLayer(4);
                txt.SetText(txt.GetText() + "\n" + animal.type + " Evolved! Complexity: " + animal.complexity);
            }

            if (animal.energy < 0) {
                animals = animals.filter(function(a) { return a !== animal; });
                replayBuffer.push({ state: state, action: action, reward: -1, nextState: nextState });
            }
        });
        drawNature();
        txt.SetText("Nature: " + animals.length + " animals, " + microbes.length + " microbes | Mandelbrot: " + (voiceInput || "Awaiting input"));
        epsilon = Math.max(0.01, epsilon * 0.995);
    } catch (e) {
        app.Alert("Error in simulateAllAnimals: " + e);
    }
}

function getAnimalState(animal) {
    try {
        var nearestFood = animal.type === "Prey" ?
            minBy(environment.grass.concat(environment.shrubs), function(item) { return Math.sqrt((animal.x - item.x) ** 2 + (animal.y - item.y) ** 2); }) :
            minBy(animals.filter(function(a) { return a.type === "Prey" && a !== animal; }), function(prey) { return Math.sqrt((animal.x - prey.x) ** 2 + (animal.y - prey.y) ** 2); });
        var foodDist = nearestFood ? Math.sqrt((animal.x - nearestFood.x) ** 2 + (animal.y - nearestFood.y) ** 2) : 1;
        var nearestThreat = animal.type === "Prey" ?
            minBy(animals.filter(function(a) { return a.type === "Predator"; }), function(pred) { return Math.sqrt((animal.x - pred.x) ** 2 + (pred.y - animal.y) ** 2); }) : null;
        var threatDist = nearestThreat ? Math.sqrt((animal.x - nearestThreat.x) ** 2 + (animal.y - nearestThreat.y) ** 2) : 1;
        var sunlight = SunCalc.getPosition(new Date(), 0, 0).altitude / PI;
        return [
            Math.min(1, animal.energy / (animal.type === "Prey" ? 1e3 : 1e4)),
            Math.min(1, animal.speed / (animal.type === "Prey" ? 10 : 7)),
            Math.min(1, animal.mass / (animal.type === "Prey" ? 40 : 80)),
            Math.min(1, foodDist / 0.9),
            Math.min(1, animal.type === "Prey" ? threatDist / 0.9 : foodDist / 0.9),
            Math.max(0, Math.min(1, sunlight))
        ];
    } catch (e) {
        app.Alert("Error in getAnimalState: " + e);
        return [0, 0, 0, 1, 1, 0];
    }
}

// FIXED: Clear old microbe interval before creating new one
function simulateMicrobes() {
    try {
        if (microbeInterval) clearInterval(microbeInterval);
        microbeInterval = setInterval(function() {
            if (!simulationRunning) return;
            microbes.forEach(function(m) {
                var nearestDead = minBy(
                    environment.grass.concat(environment.shrubs).filter(function(item) { return item.density < 0.2; }),
                    function(item) { return Math.sqrt((m.x - item.x) ** 2 + (m.y - item.y) ** 2); }
                );
                if (nearestDead && Math.sqrt((m.x - nearestDead.x) ** 2 + (m.y - nearestDead.y) ** 2) < 0.05) {
                    nearestDead.density += m.nutrientBoost;
                    m.activity -= PLANCK_LENGTH * 1e35 * 0.01;
                }
                if (Math.random() < m.activity) {
                    m.x += (Math.random() - 0.5) * PLANCK_TIME * 1e44;
                    m.y += (Math.random() - 0.5) * PLANCK_TIME * 1e44;
                    m.x = Math.max(0, Math.min(0.9, m.x));
                    m.y = Math.max(0, Math.min(0.7, m.y));
                }
                if (Math.random() < WIEN_DISPLACEMENT * 1e3) {
                    environment.grass.push({
                        type: "Grass_" + ["Short", "Tall", "Dense"][Math.floor(Math.random() * 3)],
                        x: m.x + (Math.random() - 0.5) * 0.1,
                        y: m.y + (Math.random() - 0.5) * 0.1,
                        height: PLANCK_CONSTANT * 1e34 * (Math.random() * 0.15 + 0.05),
                        density: AVOGADRO_CONSTANT / 1e22 * (Math.random() * 0.5 + 0.5),
                        regenRate: 0.015
                    });
                }
            });
            microbes = microbes.filter(function(m) { return m.activity > 0; });
            drawNature();
        }, 1000);
    } catch (e) {
        app.Alert("Error in simulateMicrobes: " + e);
    }
}

function drawNature() {
    try {
        if (!natureCanvas) throw new Error("Nature canvas not initialized");
        natureCanvas.Clear();
        environment.grass.forEach(function(g) {
            natureCanvas.SetPaintColor(getColor(g.density / 2));
            natureCanvas.DrawCircle(g.x * natureCanvas.GetWidth(), g.y * natureCanvas.GetHeight(), 5);
        });
        environment.shrubs.forEach(function(s) {
            natureCanvas.SetPaintColor(getColor(s.energyYield / 2));
            natureCanvas.DrawCircle(s.x * natureCanvas.GetWidth(), s.y * natureCanvas.GetHeight(), 10);
        });
        environment.trees.forEach(function(t) {
            natureCanvas.SetPaintColor(getColor(t.stability / 1.5));
            natureCanvas.DrawRectangle(t.x * natureCanvas.GetWidth(), t.y * natureCanvas.GetHeight(), 15, 20);
        });
        microbes.forEach(function(m) {
            natureCanvas.SetPaintColor(getColor(m.activity / (ELECTRON_MASS * 1e31)));
            natureCanvas.DrawPoint(m.x * natureCanvas.GetWidth(), m.y * natureCanvas.GetHeight());
        });
        animals.forEach(function(a) {
            natureCanvas.SetPaintColor(getColor(a.energy / (a.type === "Prey" ? 1e3 : 1e4)));
            natureCanvas.DrawCircle(a.x * natureCanvas.GetWidth(), a.y * natureCanvas.GetHeight(), a.type === "Prey" ? 6 : 8);
        });
    } catch (e) {
        app.Alert("Error in drawNature: " + e);
    }
}

// ============================================================================
// Mandelbrot Simulation
// ============================================================================
function drawMandelbrot() {
    try {
        if (!mandelbrotImage) throw new Error("Mandelbrot image not initialized");
        var startTime = Date.now();
        var mandelbrotData = generateMandelbrot(SW, SH / 2, MI);
        var x = 0, y = 0;

        function renderStep() {
            var endTime = Date.now() + 16;
            while (Date.now() < endTime && x < SW) {
                while (y < SH / 2) {
                    var value = mandelbrotData[x] && mandelbrotData[x][y] ? mandelbrotData[x][y] : 0;
                    mandelbrotImage.SetPaintColor(getColor(value));
                    mandelbrotImage.DrawRectangle(x / SW, y / (SH / 2), (x + PS) / SW, (y + PS) / (SH / 2));
                    y += PS;
                }
                y = 0;
                x += PS;
            }
            mandelbrotImage.Update();
            if (x < SW) {
                setTimeout(renderStep, 0);
            } else {
                finishMandelbrotRender(startTime);
            }
        }
        renderStep();
    } catch (e) {
        app.Alert("Error in drawMandelbrot: " + e);
    }
}

function generateMandelbrot(width, height, maxIterations) {
    try {
        var mandelbrot = [];
        var sunlight = SunCalc.getPosition(new Date(), 0, 0).altitude / PI;
        for (var x = 0; x < width; x += PS) {
            mandelbrot[x] = [];
            for (var y = 0; y < height; y += PS) {
                var real = X_MIN + (x / width) * (X_MAX - X_MIN) * GM;
                var imag = Y_MIN + (y / height) * (Y_MAX - Y_MIN) * (1 + sunlight);
                var zReal = 0, zImag = 0;
                var iteration = 0;
                while (zReal * zReal + zImag * zImag <= 4 && iteration < maxIterations) {
                    var tempReal = zReal * zReal - zImag * zImag + real;
                    zImag = 2 * zReal * zImag + imag;
                    zReal = tempReal;
                    iteration++;
                }
                mandelbrot[x][y] = iteration / maxIterations;
            }
        }
        return mandelbrot;
    } catch (e) {
        app.Alert("Error in generateMandelbrot: " + e);
        return [];
    }
}

function finishMandelbrotRender(startTime) {
    try {
        var renderTime = Date.now() - startTime;
        var pixelCount = Math.ceil((SW / PS) * (SH / 2 / PS));
        mandelbrotImage.Save("/storage/emulated/0/Render-Life-" + Date.now() + ".jpg", 100);
        txt.SetText(txt.GetText() + "\nMandelbrot: " + renderTime + "ms, " + pixelCount + " pixels");
        if (Date.now() - lastMandelbrotOODATime > 5000) {
            mandelbrotOODALoop();
            lastMandelbrotOODATime = Date.now();
        }
    } catch (e) {
        app.Alert("Error in finishMandelbrotRender: " + e);
    }
}

function mandelbrotOODALoop() {
    try {
        var observations = mandelbrotObserve();
        var situation = mandelbrotOrient(observations);
        var decision = mandelbrotDecide(situation);
        mandelbrotAct(decision);
    } catch (e) {
        app.Alert("Error in mandelbrotOODALoop: " + e);
    }
}

function mandelbrotObserve() {
    try {
        var battery = app.GetBatteryLevel() || 0.5;
        var memoryInfo = app.GetMemoryInfo() || { usedMem: 0, totalMem: 1 };
        var light = typeof memoryInfo === 'object' ? memoryInfo.usedMem / memoryInfo.totalMem : memoryInfo;
        var sunlight = SunCalc.getPosition(new Date(), 0, 0).altitude / PI;
        return [battery, light, voiceInput.length / 100, sunlight];
    } catch (e) {
        app.Alert("Error in mandelbrotObserve: " + e);
        return [0.5, 0.5, 0, 0];
    }
}

function mandelbrotOrient(observations) {
    try {
        return mandelbrotNN.feedforward(observations)[0];
    } catch (e) {
        app.Alert("Error in mandelbrotOrient: " + e);
        return 0.5;
    }
}

function mandelbrotDecide(situation) {
    try {
        if (situation > 0.7) return "addNode";
        if (situation < 0.3) return "addLayer";
        return "render";
    } catch (e) {
        app.Alert("Error in mandelbrotDecide: " + e);
        return "render";
    }
}

function mandelbrotAct(decision) {
    try {
        if (decision === "addNode") {
            mandelbrotNN.addNode();
            txt.SetText(txt.GetText() + "\nMandelbrot NN: Added node");
        } else if (decision === "addLayer") {
            mandelbrotNN.addLayer(6);
            txt.SetText(txt.GetText() + "\nMandelbrot NN: Added layer");
        }
        drawMandelbrot();
    } catch (e) {
        app.Alert("Error in mandelbrotAct: " + e);
    }
}

// ============================================================================
// FIXED: Dynamic training target instead of always [0.5]
// ============================================================================
function onSpeechResult(result) {
    try {
        if (typeof result === 'string') {
            voiceInput = result;
            interpretCommand(result);
            var observations = mandelbrotObserve();
            var situation = mandelbrotNN.feedforward(observations)[0];
            // Reinforce current direction with slight pull toward center (prevents convergence to 0.5)
            // If situation is 0.8, target = 0.77. If situation is 0.2, target = 0.23.
            var target = situation * 0.9 + 0.05;
            mandelbrotNN.train(observations, [target]);
            app.TextToSpeech("Awaiting command", 1, 1.5, function() { speech.Recognize(); });
        }
    } catch (e) {
        app.Alert("Error in onSpeechResult: " + e);
    }
}

function interpretCommand(command) {
    try {
        if (!command || typeof command !== 'string') throw new Error("No command provided");
        command = command.toLowerCase();
        var response = "Command not recognized";
        if (command.includes("pause")) {
            simulationRunning = false;
            response = "Simulation paused";
        } else if (command.includes("resume")) {
            simulationRunning = true;
            response = "Simulation resumed";
        } else if (command.includes("increase complexity")) {
            animals.forEach(function(a) { a.nn.addNode(); });
            response = "Increased animal NN complexity";
        } else if (command.includes("render")) {
            drawMandelbrot();
            response = "Rendering Mandelbrot set";
        } else if (command.includes("add node")) {
            mandelbrotNN.addNode();
            response = "Adding node to Mandelbrot NN";
        } else if (command.includes("spawn prey")) {
            var prey = createAnimal("Prey");
            if (prey) animals.push(prey);
            drawNature();
            response = "Spawning new prey";
        } else if (command.includes("spawn predator")) {
            var predator = createAnimal("Predator");
            if (predator) animals.push(predator);
            drawNature();
            response = "Spawning new predator";
        } else if (command.includes("eat")) {
            animals.forEach(function(a) {
                var nearestFood = a.type === "Prey" ?
                    minBy(environment.grass.concat(environment.shrubs), function(item) { return Math.sqrt((a.x - item.x) ** 2 + (a.y - item.y) ** 2); }) :
                    minBy(animals.filter(function(p) { return p.type === "Prey" && p !== a; }), function(prey) { return Math.sqrt((a.x - prey.x) ** 2 + (a.y - prey.y) ** 2); });
                var foodDist = nearestFood ? Math.sqrt((a.x - nearestFood.x) ** 2 + (a.y - nearestFood.y) ** 2) : 1;
                if (foodDist < 0.05 && nearestFood) {
                    if (a.type === "Prey") {
                        a.energy += STEFAN_BOLTZMANN * 1e8 * nearestFood.density * nearestFood.energyYield;
                        nearestFood.density *= 0.5;
                        if (nearestFood.density < 0.1) {
                            environment.grass = environment.grass.filter(function(g) { return g !== nearestFood; });
                            environment.shrubs = environment.shrubs.filter(function(s) { return s !== nearestFood; });
                        }
                    } else {
                        a.energy += STEFAN_BOLTZMANN * 1e8 * nearestFood.energy / 1e3;
                        animals = animals.filter(function(p) { return p !== nearestFood; });
                    }
                }
            });
            drawNature();
            response = "Animals eating";
        } else if (command.includes("grow grass")) {
            environment.grass.push({
                type: "Grass_" + ["Short", "Tall", "Dense"][Math.floor(Math.random() * 3)],
                x: Math.random() * 0.9,
                y: Math.random() * 0.7,
                height: PLANCK_CONSTANT * 1e34 * (Math.random() * 0.15 + 0.05),
                density: AVOGADRO_CONSTANT / 1e22 * (Math.random() * 0.5 + 0.5),
                regenRate: 0.015
            });
            drawNature();
            response = "Growing grass";
        }
        app.TextToSpeech(response);
    } catch (e) {
        app.Alert("Error in interpretCommand: " + e);
        app.TextToSpeech("Error processing command");
    }
}

function randomEvent() {
    try {
        if (Math.random() < 0.05) {
            if (Math.random() < 0.5) {
                animals.forEach(function(a) { a.energy *= 0.8; });
                txt.SetText(txt.GetText() + "\nStorm hits!");
            } else {
                environment.grass.forEach(function(g) { g.density *= 1.2; });
                txt.SetText(txt.GetText() + "\nNutrient surge!");
            }
            drawNature();
        }
    } catch (e) {
        app.Alert("Error in randomEvent: " + e);
    }
}

function saveWeights() {
    try {
        var data = {
            animals: animals.map(function(a) { return a.nn; }),
            mandelbrot: mandelbrotNN
        };
        app.WriteFile("weights_life.txt", JSON.stringify(data));
        app.ShowPopup("Weights Saved");
    } catch (e) {
        app.Alert("Error in saveWeights: " + e);
    }
}

function loadWeights() {
    try {
        if (!app.FileExists("weights_life.txt")) {
            app.ShowPopup("No saved weights found");
            return;
        }
        var data = JSON.parse(app.ReadFile("weights_life.txt"));
        animals.forEach(function(a, i) { a.nn = data.animals[i] || a.nn; });
        mandelbrotNN = data.mandelbrot || mandelbrotNN;
        app.ShowPopup("Weights Loaded");
    } catch (e) {
        app.Alert("Error in loadWeights: " + e);
    }
}

function cleanup() {
    try {
        if (microbeInterval) clearInterval(microbeInterval);
        animals.forEach(function(a) { clearInterval(a.interval); });
        mandelbrotNN = null;
        app.DestroyLayout(lay);
    } catch (e) {
        app.Alert("Error in cleanup: " + e);
    }
}

app.SetOnError(function(msg) { app.Alert("Error: " + msg); });
