// Solar GraVitaional Duel (SGVD)
// 3D Space Combat with Dual Solar Systems and Neural Network AI

// Game Variables
var SW = 0, SH = 0, SZ = 500;
var player = {
    x: 0, y: 0, z: 0, angle: 0, pitch: 0,
    maxSpeed: 5, turnSpeed: 0.1,
    hits: 0, shields: 100, shieldsActive: true,
    power: 100, score: 0, respawnTime: 0,
    weapon: "bullet", weaponTimer: Date.now(),
    thrusting: false, thrustType: null,
    type: "customShip",
    vx: 0, vy: 0, vz: 0
};

var enemies = [];
var artifacts = [];
var projectiles = [];
var stars = [];
var debris = [];
var solarSystem1 = [];
var solarSystem2 = [];
var lay, canvas, isRunning = false, inTitle = true, viewMode = "topDown";
var neuralNetwork = null;
var lastOODATime = 0;
var speech = app.CreateSpeechRec();

const MAX_HITS = 3;
const RESPAWN_DELAY = 2000;
const WEAPON_DELAY = 60000;
const DEBRIS_MAX_HITS = 2;
const SHIELD_REGEN_RATE = 0.1;
const POWER_DRAIN_RATE = 0.2;

var enemyCounts = {};
var factions = {
    red: "#FF6347",
    blue: "#1E90FF",
    green: "#00FF00",
    purple: "#800080"
};

var enemyTypes = ["tetrahedron", "cube", "prism", "pyramid", "octahedron", "dodecahedron"];
var enemyHits = {
    tetrahedron: 12,
    cube: 15,
    prism: 17,
    pyramid: 18,
    octahedron: 19,
    dodecahedron: 20
};

var weapons = {
    bullet: { cost: 2, hits: 10, symbol: "•", color: "#FF4500", sound: "fire_bullet.ogg" },
    machinegun: { cost: 4, hits: 7, symbol: "•", color: "#FF4500", sound: "fire_machinegun.ogg" },
    dualmachinegun: { cost: 8, hits: 5, symbol: "•", color: "#FF4500", sound: "fire_dualmachinegun.ogg" },
    railgun: { cost: 16, hits: 4, symbol: "-", color: "#00FFFF", sound: "fire_railgun.ogg" },
    laser: { cost: 32, hits: 3, symbol: "=", color: "#00FF00", sound: "fire_laser.ogg" },
    ionbeam: { cost: 64, hits: 2, symbol: "≈", color: "#FF00FF", sound: "fire_ionbeam.ogg" }
};

var sounds = {
    explode: app.CreateMediaPlayer(),
    thrust: app.CreateMediaPlayer(),
    respawn: app.CreateMediaPlayer(),
    intro: app.CreateMediaPlayer(),
    game: app.CreateMediaPlayer()
};

function loadSound(player, file) {
    try {
        player.SetFile(file);
    } catch (e) {
        app.ShowPopup("Sound file " + file + " not found.");
    }
}

loadSound(sounds.explode, "explode.ogg");
loadSound(sounds.thrust, "thrust.ogg");
loadSound(sounds.respawn, "respawn.ogg");
loadSound(sounds.intro, "intro.ogg");
loadSound(sounds.game, "game.ogg");

var colors = {
    game: {
        background: "#2F4F4F",
        player: "#00FF00",
        trail: "#FFD700",
        star: "#A9A9A9",
        debris: "#808080",
        hud: "#FFFFFF",
        shields: "#00FFFF"
    }
};

// Neural Network Class
class NeuralNetwork {
    constructor(inputSize, hiddenSize, outputSize) {
        this.inputSize = inputSize;
        this.hiddenSize = hiddenSize;
        this.outputSize = outputSize;
        this.weights1 = this.randomMatrix(inputSize, hiddenSize);
        this.weights2 = this.randomMatrix(hiddenSize, outputSize);
    }

    randomMatrix(rows, cols) {
        let matrix = [];
        for (let i = 0; i < rows; i++) {
            matrix[i] = [];
            for (let j = 0; j < cols; j++) matrix[i][j] = Math.random() * 2 - 1;
        }
        return matrix;
    }

    sigmoid(x) { return 1 / (1 + Math.exp(-x)); }

    feedforward(input) {
        if (!input || input.length !== this.inputSize) return [0, 0, 0, 0];
        let hidden = this.matrixMultiply(input, this.weights1);
        if (!hidden) return [0, 0, 0, 0];
        hidden = hidden.map(this.sigmoid);
        let output = this.matrixMultiply(hidden, this.weights2);
        return output ? output.map(this.sigmoid) : [0, 0, 0, 0];
    }

    matrixMultiply(a, b) {
        if (!a || !b || !b[0] || a.length !== b.length) return null;
        let result = [];
        for (let i = 0; i < b[0].length; i++) {
            result[i] = 0;
            for (let j = 0; j < a.length; j++) result[i] += a[j] * (b[j][i] || 0);
        }
        return result;
    }

    addNode() {
        this.hiddenSize++;
        this.weights1 = this.weights1.map(row => [...row, Math.random() * 2 - 1]);
        this.weights2.push([Math.random() * 2 - 1]);
    }

    addLayer(size) {
        this.hiddenSize = size;
        this.weights1 = this.randomMatrix(this.inputSize, size);
        this.weights2 = this.randomMatrix(size, this.outputSize);
    }

    saveWeights() {
        var data = {
            inputSize: this.inputSize,
            hiddenSize: this.hiddenSize,
            outputSize: this.outputSize,
            weights1: this.weights1,
            weights2: this.weights2
        };
        app.WriteFile("/storage/emulated/0/SpaceBattleWeights.json", JSON.stringify(data));
    }

    loadWeights() {
        if (app.FileExists("/storage/emulated/0/SpaceBattleWeights.json")) {
            var data = JSON.parse(app.ReadFile("/storage/emulated/0/SpaceBattleWeights.json"));
            this.inputSize = data.inputSize;
            this.hiddenSize = data.hiddenSize;
            this.outputSize = data.outputSize;
            this.weights1 = data.weights1;
            this.weights2 = data.weights2;
        }
    }
}

// Utility Functions
function distance3D(x1, y1, z1, x2, y2, z2) {
    return Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2);
}

function rotatePoint(x, y, cx, cy, angle) {
    var cosA = Math.cos(angle), sinA = Math.sin(angle);
    var dx = x - cx, dy = y - cy;
    return { x: cx + dx * cosA - dy * sinA, y: cy + dx * sinA + dy * cosA };
}

function rotateY(vertices, angle) {
    var cosA = Math.cos(angle), sinA = Math.sin(angle);
    return vertices.map(v => [v[0] * cosA + v[2] * sinA, v[1], -v[0] * sinA + v[2] * cosA]);
}

function rotateX(vertices, angle) {
    var cosA = Math.cos(angle), sinA = Math.sin(angle);
    return vertices.map(v => [v[0], v[1] * cosA - v[2] * sinA, v[1] * sinA + v[2] * cosA]);
}

function rotateZ(vertices, angle) {
    var cosA = Math.cos(angle), sinA = Math.sin(angle);
    return vertices.map(v => [v[0] * cosA - v[1] * sinA, v[0] * sinA + v[1] * cosA, v[2]]);
}

function project3DToScreen(x, y, z, cameraX, cameraZ) {
    var fov = 100;
    var depth = z - cameraZ;
    if (depth <= 0) return null;
    var aspect = SW / SH;
    var scale = fov / depth;
    return {
        x: SW / 2 + (x - cameraX) * scale * aspect,
        y: SH / 2 - y * scale,
        depth: depth
    };
}

function applyGravity(obj, dt) {
    var totalVx = 0, totalVy = 0, totalVz = 0;
    [solarSystem1, solarSystem2].forEach(system => {
        system.forEach(body => {
            var dx = body.x - obj.x;
            var dy = body.y - obj.y;
            var dz = body.z - obj.z;
            var dist = distance3D(obj.x, obj.y, obj.z, body.x, body.y, body.z);
            if (dist < body.radius * 0.5) {
                obj.hits = obj.maxHits || MAX_HITS;
                return;
            }
            var force = body.mass / (dist * dist) * (body.type === "sun" ? 0.01 : 0.005);
            var angleToBodyXY = Math.atan2(dy, dx);
            var angleToBodyZ = Math.atan2(dz, Math.sqrt(dx * dx + dy * dy));
            totalVx += Math.cos(angleToBodyXY) * Math.cos(angleToBodyZ) * force * dt;
            totalVy += Math.sin(angleToBodyXY) * Math.cos(angleToBodyZ) * force * dt;
            totalVz += Math.sin(angleToBodyZ) * force * dt;
        });
    });
    obj.vx = (obj.vx || 0) + totalVx;
    obj.vy = (obj.vy || 0) + totalVy;
    obj.vz = (obj.vz || 0) + totalVz;
}

// 3D Models
var debrisModel = {
    vertices: [[3, 3, 3], [3, 3, -3], [3, -3, 3], [3, -3, -3], [-3, 3, 3], [-3, 3, -3], [-3, -3, 3], [-3, -3, -3]],
    edges: [[0, 1], [0, 2], [0, 4], [1, 3], [1, 5], [2, 3], [2, 6], [3, 7], [4, 5], [4, 6], [5, 7], [6, 7]],
    scale: 1.0
};

var shipModels = {
    customShip: {
        vertices: [[0, 0, 10], [-2, -4, 5], [2, -4, 5], [0, -2, 8], [-12, 2, 0], [12, 2, 0], [-10, 1, -5], [10, 1, -5], [-3, -8, -10], [3, -8, -10], [-2, -7, -7], [2, -7, -7], [-3, -10, -12], [3, -10, -12]],
        edges: [[0, 1], [0, 2], [0, 3], [1, 3], [2, 3], [0, 4], [0, 5], [4, 6], [5, 7], [6, 8], [7, 9], [8, 9], [8, 10], [9, 11], [10, 11], [8, 12], [9, 13], [12, 13]],
        scale: 1.0,
        maxHits: MAX_HITS,
        maxSpeed: 5,
        turnSpeed: 0.1,
        defaultWeapon: "bullet"
    },
    tetrahedron: {
        vertices: [[0, 0, 10], [-5, -5, -5], [5, -5, -5], [0, 5, -5]],
        edges: [[0, 1], [0, 2], [0, 3], [1, 2], [2, 3], [3, 1]],
        scale: 1.0,
        maxHits: 12,
        maxSpeed: 5,
        turnSpeed: 0.1,
        defaultWeapon: "bullet"
    },
    cube: {
        vertices: [[5, 5, 5], [5, 5, -5], [5, -5, 5], [5, -5, -5], [-5, 5, 5], [-5, 5, -5], [-5, -5, 5], [-5, -5, -5]],
        edges: [[0, 1], [0, 2], [0, 4], [1, 3], [1, 5], [2, 3], [2, 6], [3, 7], [4, 5], [4, 6], [5, 7], [6, 7]],
        scale: 1.2,
        maxHits: 15,
        maxSpeed: 4,
        turnSpeed: 0.08,
        defaultWeapon: "bullet",
        spinSpeed: 0.05
    },
    prism: {
        vertices: [[0, 0, 10], [-5, -5, -5], [5, -5, -5], [-5, 5, -5], [5, 5, -5]],
        edges: [[0, 1], [0, 2], [0, 3], [0, 4], [1, 2], [2, 4], [4, 3], [3, 1]],
        scale: 1.1,
        maxHits: 17,
        maxSpeed: 4.5,
        turnSpeed: 0.09,
        defaultWeapon: "bullet"
    },
    pyramid: {
        vertices: [[0, 0, 10], [-5, -5, -5], [5, -5, -5], [5, 5, -5], [-5, 5, -5]],
        edges: [[0, 1], [0, 2], [0, 3], [0, 4], [1, 2], [2, 3], [3, 4], [4, 1]],
        scale: 1.0,
        maxHits: 18,
        maxSpeed: 4,
        turnSpeed: 0.08,
        defaultWeapon: "bullet"
    },
    octahedron: {
        vertices: [[0, 0, 10], [0, 0, -10], [5, 0, 0], [-5, 0, 0], [0, 5, 0], [0, -5, 0]],
        edges: [[0, 2], [0, 3], [0, 4], [0, 5], [1, 2], [1, 3], [1, 4], [1, 5], [2, 4], [2, 5], [3, 4], [3, 5]],
        scale: 1.1,
        maxHits: 19,
        maxSpeed: 4.2,
        turnSpeed: 0.09,
        defaultWeapon: "bullet"
    },
    dodecahedron: {
        vertices: [[0, 0, 10], [5, 0, 5], [-5, 0, 5], [0, 5, 5], [0, -5, 5], [5, 0, -5], [-5, 0, -5], [0, 5, -5], [0, -5, -5]],
        edges: [[0, 1], [0, 2], [0, 3], [0, 4], [1, 5], [2, 6], [3, 7], [4, 8], [5, 7], [5, 8], [6, 7], [6, 8]],
        scale: 1.3,
        maxHits: 20,
        maxSpeed: 3.5,
        turnSpeed: 0.07,
        defaultWeapon: "bullet"
    }
};

// Generation Functions
function generateStars() {
    stars = [];
    for (var i = 0; i < 100; i++) {
        stars.push({
            x: Math.random() * SW,
            y: Math.random() * SH,
            z: Math.random() * SZ - SZ / 2,
            size: 1 + Math.random() * 2,
            alpha: Math.random()
        });
    }
}

function generateDebris() {
    debris = [];
    for (var i = 0; i < 50; i++) {
        let x = Math.random() * SW, y = Math.random() * SH, z = Math.random() * SZ - SZ / 2;
        let centerX = x < SW / 2 ? SW / 4 : SW * 0.75;
        let dist = distance3D(x, y, z, centerX, SH / 2, 0);
        let angle = Math.random() * 2 * Math.PI;
        let speed = Math.sqrt(500 / dist) * 0.5;
        debris.push({
            x, y, z,
            size: 3 + Math.random() * 5,
            angleX: Math.random() * 2 * Math.PI,
            angleY: Math.random() * 2 * Math.PI,
            angleZ: Math.random() * 2 * Math.PI,
            spinX: (Math.random() - 0.5) * 0.05,
            spinY: (Math.random() - 0.5) * 0.05,
            spinZ: (Math.random() - 0.5) * 0.05,
            hits: 0,
            maxHits: DEBRIS_MAX_HITS,
            vx: -Math.sin(angle) * speed,
            vy: Math.cos(angle) * speed,
            vz: (Math.random() - 0.5) * speed
        });
    }
}

function generateEnemy() {
    var type = enemyTypes[Math.floor(Math.random() * enemyTypes.length)];
    var faction = Object.keys(factions)[Math.floor(Math.random() * Object.keys(factions).length)];
    var key = `${type}_${faction}`;
    enemyCounts[key] = (enemyCounts[key] || 0) + 1;
    if (enemyCounts[key] > 5) {
        enemyCounts[key]--;
        return;
    }
    var model = shipModels[type];
    enemies.push({
        x: Math.random() * SW,
        y: Math.random() * SH,
        z: Math.random() * SZ - SZ / 2,
        angle: Math.random() * 2 * Math.PI,
        pitch: 0,
        maxSpeed: model.maxSpeed,
        turnSpeed: model.turnSpeed,
        hits: 0,
        maxHits: model.maxHits,
        score: 0,
        respawnTime: 0,
        type: type,
        faction: faction,
        weapon: model.defaultWeapon,
        weaponTimer: Date.now(),
        thrusting: false,
        spinAngle: 0,
        vx: (Math.random() - 0.5) * 3,
        vy: (Math.random() - 0.5) * 3,
        vz: (Math.random() - 0.5) * 3
    });
}

function generateArtifact() {
    var weapon = Object.keys(weapons)[Math.floor(Math.random() * Object.keys(weapons).length)];
    artifacts.push({
        x: Math.random() * SW,
        y: Math.random() * SH,
        z: Math.random() * SZ - SZ / 2,
        weapon: weapon,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2,
        vz: (Math.random() - 0.5) * 2
    });
}

function getStarProperties() {
    const typeRoll = Math.random();
    let type, radius, mass, color;
    if (typeRoll < 0.1) {
        type = "brownDwarf";
        radius = 5 + Math.random() * 10;
        mass = radius * 200;
        color = "#8B4513";
    } else if (typeRoll < 0.2) {
        type = Math.random() < 0.5 ? "redGiant" : "blueGiant";
        radius = 40 + Math.random() * 20;
        mass = radius * 1000;
        color = type === "redGiant" ? "#FF4500" : "#0000FF";
    } else {
        const mainRoll = Math.random();
        radius = 20 + Math.random() * 15;
        mass = radius * 500;
        if (mainRoll < 0.01) { type = "O"; color = "#0000FF"; }
        else if (mainRoll < 0.05) { type = "B"; color = "#ADD8E6"; }
        else if (mainRoll < 0.1) { type = "A"; color = "#FFFFFF"; }
        else if (mainRoll < 0.2) { type = "F"; color = "#FFFFE0"; }
        else if (mainRoll < 0.4) { type = "G"; color = "#FFFF00"; }
        else if (mainRoll < 0.7) { type = "K"; color = "#FFA500"; }
        else { type = "M"; color = "#FF4500"; }
    }
    return { type, radius, mass, color };
}

function generatePlanet(centerX, orbitRadius, planetIndex) {
    const mass = 50 + Math.random() * 9950;
    const radius = Math.sqrt(mass / 50);
    const orbitSpeed = 0.0015 / (planetIndex + 1);
    const angle = Math.random() * 2 * Math.PI;
    let type, color;
    if (mass < 500) {
        type = "dwarf";
        color = orbitRadius > 150 ? "#808080" : "#A52A2A";
    } else if (mass < 2000) {
        type = "terrestrial";
        color = orbitRadius < 100 ? "#00CED1" : "#D2B48C";
    } else if (mass < 5000) {
        type = "iceGiant";
        color = "#4682B4";
    } else {
        type = "gasGiant";
        color = "#FFD700";
    }
    const rings = (type === "gasGiant" || type === "iceGiant") && Math.random() < 0.2
        ? { radius: radius * 1.5, thickness: radius * 0.1, color: "#D3D3D3" }
        : null;
    const moonCount = mass > 2000 ? Math.floor(Math.random() * 4) : Math.random() < 0.3 ? 1 : 0;
    const moons = [];
    for (let i = 0; i < moonCount; i++) {
        moons.push({
            radius: 2 + Math.random() * 3,
            orbitRadius: radius * (1.5 + i * 0.5),
            angle: Math.random() * 2 * Math.PI,
            orbitSpeed: 0.01 / (i + 1),
            color: "#808080"
        });
    }
    return {
        type, radius, mass, orbitRadius, orbitSpeed, angle, color, rings, moons,
        x: centerX + Math.cos(angle) * orbitRadius,
        y: SH / 2 + Math.sin(angle) * orbitRadius,
        z: (Math.random() - 0.5) * 100
    };
}

function generateSolarSystem(systemArray, centerX) {
    systemArray.length = 0;
    const numStars = Math.random() < 0.6 ? 1 : Math.random() < 0.9 ? 2 : 3;
    const centerY = SH / 2, centerZ = 0;
    let orbitRadius = numStars > 1 ? 50 : 0;
    for (let i = 0; i < numStars; i++) {
        const props = getStarProperties();
        const angle = (i / numStars) * 2 * Math.PI;
        systemArray.push({
            type: "sun",
            x: centerX + Math.cos(angle) * orbitRadius,
            y: centerY + Math.sin(angle) * orbitRadius,
            z: centerZ,
            radius: props.radius,
            color: props.color,
            mass: props.mass,
            orbitRadius: orbitRadius,
            orbitSpeed: numStars > 1 ? 0.002 : 0,
            angle: angle,
            starType: props.type
        });
    }
    const numPlanets = Math.floor(Math.random() * 10);
    let planetOrbitRadius = orbitRadius + 50;
    for (let i = 0; i < numPlanets; i++) {
        const planet = generatePlanet(centerX, planetOrbitRadius, i);
        systemArray.push(planet);
        planetOrbitRadius += planet.radius * 2 + Math.random() * 40;
    }
}

function generateSolarSystem1() { generateSolarSystem(solarSystem1, SW / 4); }
function generateSolarSystem2() { generateSolarSystem(solarSystem2, SW * 0.75); }

function updateSolarSystem(systemArray, centerX) {
    const centerY = SH / 2, centerZ = 0;
    systemArray.forEach(body => {
        if (body.orbitRadius > 0) {
            body.angle += body.orbitSpeed;
            body.x = centerX + Math.cos(body.angle) * body.orbitRadius;
            body.y = centerY + Math.sin(body.angle) * body.orbitRadius;
            body.z = centerZ + Math.sin(body.angle) * 10;
        }
        if (body.moons) {
            body.moons.forEach(moon => {
                moon.angle += moon.orbitSpeed;
                moon.x = body.x + Math.cos(moon.angle) * moon.orbitRadius;
                moon.y = body.y + Math.sin(moon.angle) * moon.orbitRadius;
                moon.z = body.z;
            });
        }
        if (body.ringParticles) {
            body.ringParticles.forEach(p => {
                p.angle += p.orbitSpeed;
                p.x = body.x + Math.cos(p.angle) * (body.radius * 1.5);
                p.y = body.y + Math.sin(p.angle) * (body.radius * 1.5);
                p.z = body.z;
            });
        }
    });
}

function updateSolarSystem1() { updateSolarSystem(solarSystem1, SW / 4); }
function updateSolarSystem2() { updateSolarSystem(solarSystem2, SW * 0.75); }

// Input Handling
function onTouchDown(e) {
    if (inTitle) {
        inTitle = false;
        isRunning = true;
        sounds.intro.Stop();
        sounds.game.SetLooping(true);
        sounds.game.Play();
        generateEnemy();
        setTimeout(gameLoop, 1000);
        return;
    }
    if (!isRunning || player.hits >= MAX_HITS) return;
    
    if (e.X >= 0.45 && e.X <= 0.55 && e.Y >= 0.45 && e.Y <= 0.55) {
        viewMode = viewMode === "topDown" ? "firstPerson" : viewMode === "firstPerson" ? "thirdPerson" : "topDown";
        return;
    }
    
    if (e.X < 0.33) {
        if (e.Y > 0.66) player.angle += player.turnSpeed;
        else if (e.Y > 0.5) player.pitch = Math.max(-Math.PI / 2, player.pitch - player.turnSpeed);
        else if (e.Y > 0.15) {
            player.thrusting = true;
            player.thrustType = "reverse";
        } else {
            player.shieldsActive = !player.shieldsActive;
            app.ShowPopup("Shields " + (player.shieldsActive ? "ON" : "OFF"));
        }
    } else if (e.X > 0.66) {
        if (e.Y > 0.66) player.angle -= player.turnSpeed;
        else if (e.Y > 0.5) player.pitch = Math.min(Math.PI / 2, player.pitch + player.turnSpeed);
        else if (e.Y > 0.15) {
            player.thrusting = true;
            player.thrustType = "full";
        } else shoot(player);
    }
}

function onTouchMove(e) {
    if (!isRunning || player.hits >= MAX_HITS) return;
    if (e.X < 0.33) {
        if (e.Y > 0.66) player.angle += player.turnSpeed;
        else if (e.Y > 0.5) player.pitch = Math.max(-Math.PI / 2, player.pitch - player.turnSpeed);
        else if (e.Y > 0.15) {
            player.thrusting = true;
            player.thrustType = "reverse";
        }
    } else if (e.X > 0.66) {
        if (e.Y > 0.66) player.angle -= player.turnSpeed;
        else if (e.Y > 0.5) player.pitch = Math.min(Math.PI / 2, player.pitch + player.turnSpeed);
        else if (e.Y > 0.15) {
            player.thrusting = true;
            player.thrustType = "full";
        }
    }
}

function onTouchUp(e) {
    player.thrusting = false;
    player.thrustType = null;
    sounds.thrust.Stop();
}

function onSpeechResult(result) {
    if (result) {
        var command = result.toLowerCase();
        if (command.includes("left")) player.angle += player.turnSpeed;
        else if (command.includes("right")) player.angle -= player.turnSpeed;
        else if (command.includes("up")) player.pitch = Math.min(Math.PI / 2, player.pitch + player.turnSpeed);
        else if (command.includes("down")) player.pitch = Math.max(-Math.PI / 2, player.pitch - player.turnSpeed);
        else if (command.includes("shoot")) shoot(player);
        else if (command.includes("shields")) {
            player.shieldsActive = !player.shieldsActive;
            app.ShowPopup("Shields " + (player.shieldsActive ? "ON" : "OFF"));
        }
        app.TextToSpeech("Awaiting command", 1, 1.5);
    }
}

// Game Functions
function respawnShip(ship, startX, startY, startZ, startAngle) {
    ship.x = startX; ship.y = startY; ship.z = startZ;
    ship.angle = startAngle; ship.pitch = 0;
    ship.hits = 0; ship.shields = 100; ship.shieldsActive = true;
    ship.power = 100; ship.respawnTime = 0;
    ship.thrusting = false; ship.spinAngle = 0;
    ship.vx = 0; ship.vy = 0; ship.vz = 0;
    sounds.respawn.Play();
}

function restartGame() {
    player = {
        x: SW / 2, y: SH / 2, z: 0, angle: 0, pitch: 0,
        maxSpeed: 5, turnSpeed: 0.1,
        hits: 0, shields: 100, shieldsActive: true,
        power: 100, score: 0, respawnTime: 0,
        weapon: "bullet", weaponTimer: Date.now(),
        thrusting: false, thrustType: null,
        type: "customShip",
        vx: 0, vy: 0, vz: 0
    };
    enemies = []; artifacts = []; projectiles = [];
    enemyCounts = {};
    generateEnemy(); generateDebris();
    generateSolarSystem1(); generateSolarSystem2();
    app.ShowPopup("Game restarted!");
}

function exitGame() {
    if (neuralNetwork) neuralNetwork.saveWeights();
    app.Exit();
}

function updateShip(ship) {
    if (ship.hits >= (ship.maxHits || MAX_HITS)) return;
    applyGravity(ship, 16);
    
    if (ship.thrusting) {
        var accel = 0.1;
        if (ship.thrustType === "reverse") {
            ship.vx -= Math.cos(ship.angle) * Math.cos(ship.pitch) * accel;
            ship.vy -= Math.sin(ship.angle) * Math.cos(ship.pitch) * accel;
            ship.vz -= Math.sin(ship.pitch) * accel;
        } else if (ship.thrustType === "full") {
            ship.vx += Math.cos(ship.angle) * Math.cos(ship.pitch) * accel * 1.5;
            ship.vy += Math.sin(ship.angle) * Math.cos(ship.pitch) * accel * 1.5;
            ship.vz += Math.sin(ship.pitch) * accel * 0.5;
        }
        ship.power = Math.max(0, ship.power - POWER_DRAIN_RATE);
        if (ship.power <= 0 && ship.shieldsActive) ship.shields = Math.max(0, ship.shields - POWER_DRAIN_RATE);
        if (!sounds.thrust.IsPlaying()) sounds.thrust.Play();
    } else {
        if (ship.shieldsActive) ship.shields = Math.min(100, ship.shields + SHIELD_REGEN_RATE);
        ship.power = Math.min(100, ship.power + SHIELD_REGEN_RATE * 0.5);
        sounds.thrust.Stop();
    }
    
    ship.x += ship.vx; ship.y += ship.vy; ship.z += ship.vz;
    ship.vx *= 0.98; ship.vy *= 0.98; ship.vz *= 0.98;
    ship.x = (ship.x < 0 ? ship.x + SW : ship.x > SW ? ship.x - SW : ship.x);
    ship.y = (ship.y < 0 ? ship.y + SH : ship.y > SH ? ship.y - SH : ship.y);
    ship.z = (ship.z < -SZ / 2 ? ship.z + SZ : ship.z > SZ / 2 ? ship.z - SZ : ship.z);
    
    if (ship.type === "cube" && shipModels.cube.spinSpeed) ship.spinAngle += shipModels.cube.spinSpeed;
}

function updateDebris() {
    for (var i = debris.length - 1; i >= 0; i--) {
        var d = debris[i];
        applyGravity(d, 16);
        d.angleX += d.spinX; d.angleY += d.spinY; d.angleZ += d.spinZ;
        d.x += d.vx; d.y += d.vy; d.z += d.vz;
        d.vx *= 0.98; d.vy *= 0.98; d.vz *= 0.98;
        d.x = (d.x < 0 ? d.x + SW : d.x > SW ? d.x - SW : d.x);
        d.y = (d.y < 0 ? d.y + SH : d.y > SH ? d.y - SH : d.y);
        d.z = (d.z < -SZ / 2 ? d.z + SZ : d.z > SZ / 2 ? d.z - SZ : d.z);
    }
}

function shoot(ship) {
    if (ship.hits >= (ship.maxHits || MAX_HITS) || !ship.weapon) return;
    var w = weapons[ship.weapon];
    projectiles.push({
        x: ship.x + Math.cos(ship.angle) * 20 * Math.cos(ship.pitch),
        y: ship.y + Math.sin(ship.angle) * 20 * Math.cos(ship.pitch),
        z: ship.z + Math.sin(ship.pitch) * 20,
        angle: ship.angle, pitch: ship.pitch, life: 100,
        weapon: ship.weapon,
        vx: Math.cos(ship.angle) * Math.cos(ship.pitch) * 7 + ship.vx,
        vy: Math.sin(ship.angle) * Math.cos(ship.pitch) * 7 + ship.vy,
        vz: Math.sin(ship.pitch) * 7 + ship.vz
    });
    app.PlaySound(w.sound);
}

function updateProjectiles() {
    for (var i = projectiles.length - 1; i >= 0; i--) {
        var p = projectiles[i];
        applyGravity(p, 16);
        p.x += p.vx; p.y += p.vy; p.z += p.vz;
        p.life--;
        p.x = (p.x < 0 ? p.x + SW : p.x > SW ? p.x - SW : p.x);
        p.y = (p.y < 0 ? p.y + SH : p.y > SH ? p.y - SH : p.y);
        p.z = (p.z < -SZ / 2 ? p.z + SZ : p.z > SZ / 2 ? p.z - SZ : p.z);
        if (p.life <= 0) projectiles.splice(i, 1);
    }
}

function checkCollisions() {
    var now = Date.now();
    for (var i = projectiles.length - 1; i >= 0; i--) {
        var p = projectiles[i];
        if (distance3D(p.x, p.y, p.z, player.x, player.y, player.z) < 20 && player.hits < MAX_HITS) {
            if (player.shieldsActive && player.shields > 0) {
                player.shields -= weapons[p.weapon].hits;
                if (player.shields < 0) player.hits += Math.abs(player.shields);
            } else player.hits += weapons[p.weapon].hits;
            projectiles.splice(i, 1);
            if (player.hits >= MAX_HITS) {
                player.respawnTime = now;
                sounds.explode.Play();
            }
            continue;
        }
        for (var j = enemies.length - 1; j >= 0; j--) {
            var e = enemies[j];
            if (distance3D(p.x, p.y, p.z, e.x, e.y, e.z) < 20 && e.hits < e.maxHits) {
                e.hits += weapons[p.weapon].hits;
                projectiles.splice(i, 1);
                if (e.hits >= e.maxHits) {
                    e.respawnTime = now;
                    player.score += 1;
                    sounds.explode.Play();
                    generateEnemy();
                }
                break;
            }
        }
    }
}

function checkArtifacts() {
    for (var i = artifacts.length - 1; i >= 0; i--) {
        var a = artifacts[i];
        applyGravity(a, 16);
        a.x += a.vx; a.y += a.vy; a.z += a.vz;
        a.vx *= 0.98; a.vy *= 0.98; a.vz *= 0.98;
        a.x = (a.x < 0 ? a.x + SW : a.x > SW ? a.x - SW : a.x);
        a.y = (a.y < 0 ? a.y + SH : a.y > SH ? a.y - SH : a.y);
        a.z = (a.z < -SZ / 2 ? a.z + SZ : a.z > SZ / 2 ? a.z - SZ : a.z);
        if (distance3D(a.x, a.y, a.z, player.x, player.y, player.z) < 20) {
            if (player.score >= weapons[a.weapon].cost) {
                player.weapon = a.weapon;
                player.weaponTimer = Date.now();
                player.score -= weapons[a.weapon].cost;
            }
            artifacts.splice(i, 1);
            break;
        }
    }
}

function updateWeapons(now) {
    if (player.weapon && now - player.weaponTimer > WEAPON_DELAY) {
        var currentIdx = Object.keys(weapons).indexOf(player.weapon);
        if (currentIdx < Object.keys(weapons).length - 1 &&
            player.score >= weapons[Object.keys(weapons)[currentIdx + 1]].cost) {
            player.weapon = Object.keys(weapons)[currentIdx + 1];
            player.score -= weapons[player.weapon].cost;
            player.weaponTimer = now;
        }
    }
}

// OODA Loop (Neural Network AI)
function oodaLoop() {
    enemies.forEach(e => {
        if (e.hits < e.maxHits) {
            var observations = observe(e);
            var situation = orient(observations);
            var decision = decide(situation);
            act(e, decision);
        }
    });
}

function observe(enemy) {
    var dxPlayer = player.x - enemy.x, dyPlayer = player.y - enemy.y, dzPlayer = player.z - enemy.z;
    var distPlayer = distance3D(enemy.x, enemy.y, enemy.z, player.x, player.y, player.z) / SW;
    var angleDiffPlayer = Math.atan2(dyPlayer, dxPlayer) - enemy.angle;
    var artifactDist = artifacts.length ? distance3D(enemy.x, enemy.y, enemy.z, artifacts[0].x, artifacts[0].y, artifacts[0].z) / SW : 1;
    var angleDiffArtifact = artifacts.length ? Math.atan2(artifacts[0].y - enemy.y, artifacts[0].x - enemy.x) - enemy.angle : 0;
    var system = enemy.x < SW / 2 ? solarSystem1 : solarSystem2;
    var closestSun = system.filter(body => body.type === "sun").reduce((c, s) =>
        distance3D(enemy.x, enemy.y, enemy.z, s.x, s.y, s.z) < distance3D(enemy.x, enemy.y, enemy.z, c.x, c.y, c.z) ? s : c, system[0]);
    var distSun = closestSun ? distance3D(enemy.x, enemy.y, enemy.z, closestSun.x, closestSun.y, closestSun.z) / SW : 1;
    var zDiffPlayer = (player.z - enemy.z) / SZ;
    return [distPlayer, angleDiffPlayer, Math.sqrt(player.vx ** 2 + player.vy ** 2 + player.vz ** 2) / player.maxSpeed,
        artifactDist, angleDiffArtifact, distSun, zDiffPlayer];
}

function orient(observations) {
    return neuralNetwork.feedforward(observations);
}

function decide(situation) {
    return {
        turn: situation[0] > 0.5 ? 1 : -1,
        thrust: situation[0] < 0.5 || situation[3] < 0.4 || situation[5] < 0.3,
        shoot: situation[0] < 0.2 && Math.random() > 0.3,
        grow: situation[3] > 0.6 ? (situation[3] > 0.8 ? "addLayer" : "addNode") : null
    };
}

function act(enemy, decision) {
    enemy.angle += decision.turn * enemy.turnSpeed;
    enemy.thrusting = decision.thrust;
    if (decision.shoot) shoot(enemy);
    if (decision.grow === "addNode") neuralNetwork.addNode();
    else if (decision.grow === "addLayer") neuralNetwork.addLayer(6);
}

// Drawing Functions
function drawHUD() {
    canvas.SetPaintColor(colors.game.hud);
    canvas.SetTextSize(12);
    var hudText = `Score: ${player.score} Hits: ${player.hits}/${MAX_HITS} Weapon: ${player.weapon} Speed: ${Math.sqrt(player.vx ** 2 + player.vy ** 2 + player.vz ** 2).toFixed(1)}/${player.maxSpeed} View: ${viewMode} Shields: ${player.shieldsActive ? player.shields.toFixed(0) + "%" : "OFF"} Power: ${player.power.toFixed(0)}%`;
    canvas.DrawText(hudText, 0.05, 0.90);
}

function drawShip(ship, type, color) {
    var model = shipModels[type] || shipModels.tetrahedron;
    var size = 20 * model.scale;
    var rotated = rotateY(model.vertices, ship.angle);
    rotated = rotateX(rotated, ship.pitch);
    if (type === "cube") rotated = rotateZ(rotated, ship.spinAngle);
    var projected = rotated.map(v => ({ x: ship.x + v[0], y: ship.y + v[2] }));
    
    for (var i = 0; i < model.edges.length; i++) {
        var [start, end] = model.edges[i];
        canvas.SetPaintColor(color);
        canvas.DrawLine(projected[start].x / SW, projected[start].y / SH, projected[end].x / SW, projected[end].y / SH);
    }
    
    if (ship.thrusting) {
        canvas.SetPaintColor(colors.game.trail);
        var rearX = projected[8].x + (projected[9].x - projected[8].x) / 2;
        var rearY = projected[8].y + (projected[9].y - projected[8].y) / 2;
        var thrustAngle = ship.angle + Math.PI;
        var thrustLength = size * 0.5 * Math.min(Math.sqrt(ship.vx ** 2 + ship.vy ** 2 + ship.vz ** 2) / ship.maxSpeed, 1.5);
        var leftX = rearX + Math.cos(thrustAngle + 0.3) * thrustLength;
        var leftY = rearY + Math.sin(thrustAngle + 0.3) * thrustLength;
        var rightX = rearX + Math.cos(thrustAngle - 0.3) * thrustLength;
        var rightY = rearY + Math.sin(thrustAngle - 0.3) * thrustLength;
        canvas.DrawLine(rearX / SW, rearY / SH, leftX / SW, leftY / SH);
        canvas.DrawLine(rearX / SW, rearY / SH, rightX / SW, rightY / SH);
        canvas.DrawLine(leftX / SW, leftY / SH, rightX / SW, rightY / SH);
    }
}

// ==================== FIRST PERSON VIEW ====================

function drawFirstPersonView() {
    canvas.Clear();
    canvas.SetPaintColor(colors.game.background);
    canvas.DrawRectangle(0, 0, 1, 1);
    
    // Calculate camera position (behind and above player)
    var cameraZ = player.z - Math.sin(player.pitch) * 50 + 20;
    var cameraX = player.x - Math.cos(player.angle) * Math.cos(player.pitch) * 50;
    var cameraY = player.y - Math.sin(player.angle) * Math.cos(player.pitch) * 50;
    
    // Draw stars with perspective
    stars.forEach(s => {
        var proj = project3DToScreen(s.x, s.z, s.y, cameraX, cameraZ);
        if (proj && proj.depth < 500) {
            canvas.SetPaintColor(colors.game.star);
            canvas.SetAlpha(s.alpha);
            canvas.DrawCircle(proj.x / SW, proj.y / SH, s.size / SW);
        }
    });
    canvas.SetAlpha(1);
    
    // Draw solar systems
    [solarSystem1, solarSystem2].forEach(system => {
        system.forEach(body => {
            var proj = project3DToScreen(body.x, body.z, body.y, cameraX, cameraZ);
            if (proj && proj.depth < 1000) {
                canvas.SetPaintColor(body.color);
                var size = body.radius / proj.depth * 100;
                canvas.DrawCircle(proj.x / SW, proj.y / SH, Math.max(size / SW, 0.005));
                if (body.rings) {
                    canvas.SetPaintColor(body.rings.color);
                    canvas.DrawCircle(proj.x / SW, proj.y / SH, body.rings.radius / proj.depth * 100 / SW);
                }
                if (body.moons) {
                    body.moons.forEach(moon => {
                        var moonProj = project3DToScreen(moon.x, moon.z, moon.y, cameraX, cameraZ);
                        if (moonProj) {
                            canvas.SetPaintColor(moon.color);
                            canvas.DrawCircle(moonProj.x / SW, moonProj.y / SH, moon.radius / moonProj.depth * 100 / SW);
                        }
                    });
                }
            }
        });
    });
    
    // Draw enemies
    enemies.forEach(e => {
        if (e.hits < e.maxHits) {
            var model = shipModels[e.type];
            var rotated = rotateY(model.vertices, e.angle);
            rotated = rotateX(rotated, e.pitch);
            var projected = rotated.map(v => project3DToScreen(e.x + v[0], e.z + v[1], e.y + v[2], cameraX, cameraZ));
            canvas.SetPaintColor(factions[e.faction]);
            for (var i = 0; i < model.edges.length; i++) {
                var [start, end] = model.edges[i];
                if (projected[start] && projected[end] && projected[start].depth < 500) {
                    canvas.DrawLine(projected[start].x / SW, projected[start].y / SH, projected[end].x / SW, projected[end].y / SH);
                }
            }
        }
    });
    
    // Draw debris
    debris.forEach(d => {
        var model = debrisModel;
        var scaledVertices = model.vertices.map(v => [v[0] * (d.size / 3), v[1] * (d.size / 3), v[2] * (d.size / 3)]);
        var rotated = rotateX(scaledVertices, d.angleX);
        rotated = rotateY(rotated, d.angleY);
        rotated = rotateZ(rotated, d.angleZ);
        var projected = rotated.map(v => project3DToScreen(d.x + v[0], d.z + v[1], d.y + v[2], cameraX, cameraZ));
        canvas.SetPaintColor(colors.game.debris);
        for (var i = 0; i < model.edges.length; i++) {
            var [start, end] = model.edges[i];
            if (projected[start] && projected[end] && projected[start].depth < 500) {
                canvas.DrawLine(projected[start].x / SW, projected[start].y / SH, projected[end].x / SW, projected[end].y / SH);
            }
        }
    });
    
    // Draw projectiles
    projectiles.forEach(p => {
        var proj = project3DToScreen(p.x, p.z, p.y, cameraX, cameraZ);
        if (proj && proj.depth < 500) {
            canvas.SetPaintColor(weapons[p.weapon].color);
            canvas.SetTextSize(20);
            canvas.DrawText(weapons[p.weapon].symbol, proj.x / SW, proj.y / SH);
        }
    });
    
    // Draw artifacts
    artifacts.forEach(a => {
        var proj = project3DToScreen(a.x, a.z, a.y, cameraX, cameraZ);
        if (proj && proj.depth < 500) {
            canvas.SetPaintColor(weapons[a.weapon].color);
            var symbol = Math.sin(Date.now() / 500) > 0 ? "." : "•";
            canvas.SetTextSize(20);
            canvas.DrawText(symbol, proj.x / SW, proj.y / SH, "center");
        }
    });
    
    // Draw crosshair
    canvas.SetPaintColor("#FF0000");
    canvas.SetLineWidth(2);
    canvas.DrawLine(0.5 - 0.02, 0.5, 0.5 + 0.02, 0.5);
    canvas.DrawLine(0.5, 0.5 - 0.02, 0.5, 0.5 + 0.02);
    
    drawHUD();
    canvas.Update();
}

// ==================== THIRD PERSON VIEW ====================

function drawThirdPersonView() {
    canvas.Clear();
    canvas.SetPaintColor(colors.game.background);
    canvas.DrawRectangle(0, 0, 1, 1);
    
    // Camera position: behind and above player
    var cameraZ = player.z - Math.sin(player.pitch) * 80 + 30;
    var cameraX = player.x - Math.cos(player.angle) * Math.cos(player.pitch) * 80;
    var cameraY = player.y - Math.sin(player.angle) * Math.cos(player.pitch) * 80;
    
    // Draw stars
    stars.forEach(s => {
        var proj = project3DToScreen(s.x, s.z, s.y, cameraX, cameraZ);
        if (proj) {
            canvas.SetPaintColor(colors.game.star);
            canvas.SetAlpha(s.alpha);
            canvas.DrawCircle(proj.x / SW, proj.y / SH, s.size / SW);
        }
    });
    canvas.SetAlpha(1);
    
    // Draw solar systems
    [solarSystem1, solarSystem2].forEach(system => {
        system.forEach(body => {
            var proj = project3DToScreen(body.x, body.z, body.y, cameraX, cameraZ);
            if (proj) {
                canvas.SetPaintColor(body.color);
                var size = body.radius / proj.depth * 100;
                canvas.DrawCircle(proj.x / SW, proj.y / SH, Math.max(size / SW, 0.005));
                if (body.rings) {
                    canvas.SetPaintColor(body.rings.color);
                    canvas.DrawCircle(proj.x / SW, proj.y / SH, body.rings.radius / proj.depth * 100 / SW);
                }
                if (body.moons) {
                    body.moons.forEach(moon => {
                        var moonProj = project3DToScreen(moon.x, moon.z, moon.y, cameraX, cameraZ);
                        if (moonProj) {
                            canvas.SetPaintColor(moon.color);
                            canvas.DrawCircle(moonProj.x / SW, moonProj.y / SH, moon.radius / moonProj.depth * 100 / SW);
                        }
                    });
                }
            }
        });
    });
    
    // Draw player ship (visible in third person)
    if (player.hits < MAX_HITS) {
        var model = shipModels[player.type];
        var rotated = rotateY(model.vertices, player.angle);
        rotated = rotateX(rotated, player.pitch);
        var projected = rotated.map(v => project3DToScreen(player.x + v[0], player.z + v[1], player.y + v[2], cameraX, cameraZ));
        canvas.SetPaintColor(colors.game.player);
        for (var i = 0; i < model.edges.length; i++) {
            var [start, end] = model.edges[i];
            if (projected[start] && projected[end]) {
                canvas.DrawLine(projected[start].x / SW, projected[start].y / SH, projected[end].x / SW, projected[end].y / SH);
            }
        }
        // Draw thrust trail
        if (player.thrusting) {
            canvas.SetPaintColor(colors.game.trail);
            var rear = projected[8] || projected[0];
            var trailX = rear.x - Math.cos(player.angle) * 20;
            var trailY = rear.y - Math.sin(player.angle) * 20;
            canvas.DrawCircle(trailX / SW, trailY / SH, 5 / SW);
        }
    }
    
    // Draw enemies
    enemies.forEach(e => {
        if (e.hits < e.maxHits) {
            var model = shipModels[e.type];
            var rotated = rotateY(model.vertices, e.angle);
            rotated = rotateX(rotated, e.pitch);
            var projected = rotated.map(v => project3DToScreen(e.x + v[0], e.z + v[1], e.y + v[2], cameraX, cameraZ));
            canvas.SetPaintColor(factions[e.faction]);
            for (var i = 0; i < model.edges.length; i++) {
                var [start, end] = model.edges[i];
                if (projected[start] && projected[end]) {
                    canvas.DrawLine(projected[start].x / SW, projected[start].y / SH, projected[end].x / SW, projected[end].y / SH);
                }
            }
        }
    });
    
    // Draw debris
    debris.forEach(d => {
        var model = debrisModel;
        var scaledVertices = model.vertices.map(v => [v[0] * (d.size / 3), v[1] * (d.size / 3), v[2] * (d.size / 3)]);
        var rotated = rotateX(scaledVertices, d.angleX);
        rotated = rotateY(rotated, d.angleY);
        rotated = rotateZ(rotated, d.angleZ);
        var projected = rotated.map(v => project3DToScreen(d.x + v[0], d.z + v[1], d.y + v[2], cameraX, cameraZ));
        canvas.SetPaintColor(colors.game.debris);
        for (var i = 0; i < model.edges.length; i++) {
            var [start, end] = model.edges[i];
            if (projected[start] && projected[end]) {
                canvas.DrawLine(projected[start].x / SW, projected[start].y / SH, projected[end].x / SW, projected[end].y / SH);
            }
        }
    });
    
    // Draw projectiles
    projectiles.forEach(p => {
        var proj = project3DToScreen(p.x, p.z, p.y, cameraX, cameraZ);
        if (proj) {
            canvas.SetPaintColor(weapons[p.weapon].color);
            canvas.SetTextSize(20);
            canvas.DrawText(weapons[p.weapon].symbol, proj.x / SW, proj.y / SH);
        }
    });
    
    // Draw artifacts
    artifacts.forEach(a => {
        var proj = project3DToScreen(a.x, a.z, a.y, cameraX, cameraZ);
        if (proj) {
            canvas.SetPaintColor(weapons[a.weapon].color);
            var symbol = Math.sin(Date.now() / 500) > 0 ? "." : "•";
            canvas.SetTextSize(20);
            canvas.DrawText(symbol, proj.x / SW, proj.y / SH, "center");
        }
    });
    
    drawHUD();
    canvas.Update();
}

// ==================== TOP DOWN VIEW ====================

function drawTopDownView() {
    canvas.Clear();
    canvas.SetPaintColor(colors.game.background);
    canvas.DrawRectangle(0, 0, 1, 1);
    
    stars.forEach(s => {
        canvas.SetPaintColor(colors.game.star);
        canvas.SetAlpha(s.alpha + Math.sin(Date.now() / 500 + s.x) * 0.3);
        canvas.DrawCircle(s.x / SW, s.y / SH, s.size / SW);
    });
    canvas.SetAlpha(1);
    
    [solarSystem1, solarSystem2].forEach(system => {
        system.forEach(body => {
            canvas.SetPaintColor(body.color);
            canvas.DrawCircle(body.x / SW, body.y / SH, body.radius / SW);
            if (body.rings) {
                canvas.SetPaintColor(body.rings.color);
                canvas.DrawCircle(body.x / SW, body.y / SH, body.rings.radius / SW);
            }
            if (body.moons) {
                body.moons.forEach(moon => {
                    canvas.SetPaintColor(moon.color);
                    canvas.DrawCircle(moon.x / SW, moon.y / SH, moon.radius / SW);
                });
            }
        });
    });
    
    debris.forEach(d => {
        var model = debrisModel;
        var scaledVertices = model.vertices.map(v => [v[0] * (d.size / 3), v[1] * (d.size / 3), v[2] * (d.size / 3)]);
        var rotated = rotateX(scaledVertices, d.angleX);
        rotated = rotateY(rotated, d.angleY);
        rotated = rotateZ(rotated, d.angleZ);
        var projected = rotated.map(v => ({ x: d.x + v[0], y: d.y + v[2] }));
        canvas.SetPaintColor(colors.game.debris);
        for (var i = 0; i < model.edges.length; i++) {
            var [start, end] = model.edges[i];
            canvas.DrawLine(projected[start].x / SW, projected[start].y / SH, projected[end].x / SW, projected[end].y / SH);
        }
    });
    
    if (player.hits < MAX_HITS) drawShip(player, player.type, colors.game.player);
    
    enemies.forEach(e => {
        if (e.hits < e.maxHits) drawShip(e, e.type, factions[e.faction]);
    });
    
    projectiles.forEach(p => {
        canvas.SetPaintColor(weapons[p.weapon].color);
        canvas.SetTextSize(20);
        canvas.DrawText(weapons[p.weapon].symbol, p.x / SW, p.y / SH);
    });
    
    artifacts.forEach(a => {
        canvas.SetPaintColor(weapons[a.weapon].color);
        var symbol = Math.sin(Date.now() / 500) > 0 ? "." : "•";
        canvas.SetTextSize(20);
        canvas.DrawText(symbol, a.x / SW, a.y / SH, "center");
    });
    
    drawHUD();
    canvas.Update();
}

function drawTitle() {
    canvas.Clear();
    canvas.SetPaintColor(colors.game.background);
    canvas.DrawRectangle(0, 0, 1, 1);
    
    solarSystem1.forEach(body => {
        canvas.SetPaintColor(body.color);
        canvas.DrawCircle(body.x / SW, body.y / SH, body.radius / SW);
    });
    solarSystem2.forEach(body => {
        canvas.SetPaintColor(body.color);
        canvas.DrawCircle(body.x / SW, body.y / SH, body.radius / SW);
    });
    
    canvas.SetPaintColor(colors.game.player);
    canvas.SetTextSize(0.1 * SW);
    canvas.DrawText("Solar GraVitaional Duel", 0.5, 0.2, "center");
    canvas.SetTextSize(0.05 * SW);
    canvas.DrawText("Touch center to start", 0.5, 0.7, "center");
    canvas.Update();
}

// Main Game Loop
function gameLoop() {
    if (!isRunning) {
        drawTitle();
        return setTimeout(gameLoop, 16);
    }
    
    var now = Date.now();
    
    if (player.hits >= MAX_HITS && now - player.respawnTime > RESPAWN_DELAY) {
        respawnShip(player, SW / 2, SH / 2, 0, 0);
    }
    
    enemies.forEach((e, i) => {
        if (e.hits >= e.maxHits && now - e.respawnTime > RESPAWN_DELAY) {
            var key = `${e.type}_${e.faction}`;
            enemyCounts[key]--;
            enemies.splice(i, 1);
            generateEnemy();
        }
    });
    
    updateShip(player);
    enemies.forEach(updateShip);
    updateProjectiles();
    updateDebris();
    updateSolarSystem1();
    updateSolarSystem2();
    checkCollisions();
    checkArtifacts();
    updateWeapons(now);
    
    if (Date.now() - lastOODATime > 1000) {
        oodaLoop();
        lastOODATime = Date.now();
    }
    
    // Render based on view mode
    if (viewMode === "firstPerson") drawFirstPersonView();
    else if (viewMode === "thirdPerson") drawThirdPersonView();
    else drawTopDownView();
    
    setTimeout(gameLoop, 16);
}

// Initialization
function OnStart() {
    app.SetOrientation("Landscape");
    SW = app.GetScreenWidth();
    SH = app.GetScreenHeight();
    player.x = SW / 2; player.y = SH / 2; player.z = 0;
    
    lay = app.CreateLayout("Linear", "FillXY");
    canvas = app.CreateImage(null, 1.0, 1.0, "fix", SW, SH);
    canvas.SetAutoUpdate(false);
    canvas.SetOnTouchDown(onTouchDown);
    canvas.SetOnTouchMove(onTouchMove);
    canvas.SetOnTouchUp(onTouchUp);
    lay.AddChild(canvas);
    
    var controlLay = app.CreateLayout("Linear", "Horizontal");
    controlLay.SetPosition(0.80, 0.90);
    var btnRestart = app.CreateButton("Restart", 0.15, 0.05);
    btnRestart.SetBackColor("#00000000");
    btnRestart.SetTextColor("#00FF00");
    btnRestart.SetOnTouch(restartGame);
    controlLay.AddChild(btnRestart);
    var btnExit = app.CreateButton("Exit", 0.15, 0.05);
    btnExit.SetMargins(0.02, 0, 0, 0);
    btnExit.SetOnTouch(exitGame);
    controlLay.AddChild(btnExit);
    lay.AddChild(controlLay);
    
    app.AddLayout(lay);
    
    neuralNetwork = new NeuralNetwork(7, 5, 4);
    neuralNetwork.loadWeights();
    
    generateStars();
    generateDebris();
    generateSolarSystem1();
    generateSolarSystem2();
    
    sounds.intro.SetLooping(true);
    sounds.intro.Play();
    speech.SetOnResult(onSpeechResult);
    
    setInterval(() => { if (Math.random() < 0.1) generateArtifact(); }, 10000);
    setTimeout(gameLoop, 100);
}

function OnPause() {
    isRunning = false;
    if (neuralNetwork) neuralNetwork.saveWeights();
    sounds.game.Pause();
}

function OnResume() {
    if (neuralNetwork) neuralNetwork.loadWeights();
    isRunning = !inTitle;
    if (!inTitle) sounds.game.Play();
    setTimeout(gameLoop, 1000);
}

OnStart();
