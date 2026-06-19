// Chronospace Explorer - Gamified Multi-Time Dimensions
// Consolidated Equations (displayed in HUD & comments):
// 1. Our reality (3+1): ds² = -c² dt² + dx² + dy² + dz²
// 2. Extra time (3+2): ds² = -c² (dt₁² + dt₂²) + dx² + dy² + dz²
// 3. Extreme (3+3): ds² = -c² (dt₁² + dt₂² + dt₃²) + dx² + dy² + dz²
// Ultrahyperbolic instability: branching timelines, ghosts, closed loops

// === Game Variables ===
var SW = app.GetScreenHeight(); // Landscape mode
var SH = app.GetScreenWidth();
var player = {
    x: SW / 2, y: SH / 2, z: 0, angle: 0,
    maxSpeed: 5, turnSpeed: 0.1,
    hits: 0, shields: 100, shieldsActive: true,
    power: 100, score: 0, respawnTime: 0,
    weapon: "bullet", weaponTimer: Date.now(),
    thrusting: false, thrustType: null,
    type: "customShip",
    vx: 0, vy: 0, vz: 0,
    history: [] // for ghost trails in higher chronal levels
};

var enemies = [];
var artifacts = [];
var chronalArtifacts = []; // new: unlock extra time dims
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
const CHRONAL_THRESHOLD = [0, 800, 2500]; // score to unlock level 2, 3
var timeDimensionLevel = 1; // 1=normal, 2=3+2, 3=3+3
var chronalEnergy = 100;
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
    railgun: { cost: 16, hits: 4, symbol: "•", color: "#FF4500", sound: "fire_railgun.ogg" },
    laser: { cost: 32, hits: 3, symbol: "•", color: "#FF4500", sound: "fire_laser.ogg" },
    ionbeam: { cost: 64, hits: 2, symbol: "•", color: "#FF4500", sound: "fire_ionbeam.ogg" }
};

var sounds = {
    explode: app.CreateMediaPlayer(),
    thrust: app.CreateMediaPlayer(),
    respawn: app.CreateMediaPlayer(),
    intro: app.CreateMediaPlayer(),
    game: app.CreateMediaPlayer(),
    chronal: app.CreateMediaPlayer()
};

function loadSound(player, file) {
    try {
        player.SetFile(file);
    } catch (e) {
        app.ShowPopup("Sound missing: " + file);
    }
}

loadSound(sounds.explode, "Snd/Calm.ogg");
loadSound(sounds.thrust, "Snd/Nudge.ogg");
loadSound(sounds.respawn, "Snd/Respawn.ogg");
loadSound(sounds.intro, "intro.ogg");
loadSound(sounds.game, "game.ogg");
loadSound(sounds.chronal, "Snd/chronal_unlock.ogg");

var colors = {
    game: {
        background: "#2F4F4F",
        player: "#808080",
        trail: "#FFD700",
        star: "#A9A9A9",
        debris: "#808080",
        hud: "#FFFFFF",
        shields: "#00FFFF",
        chronal: "#9932CC"
    }
};

function getRandomColor(baseHue) {
    let hue = baseHue === "red" ? Math.random() * 30 :
        baseHue === "yellow" ? 50 + Math.random() * 20 :
            baseHue === "blue" ? 200 + Math.random() * 40 :
                baseHue === "green" ? 100 + Math.random() * 40 :
                    baseHue === "brown" ? 20 + Math.random() * 40 :
                        Math.random() * 360;
    let sat = 80 + Math.random() * 20;
    let lit = 50 + Math.random() * 30;
    return `hsl(${hue},${sat}%,${lit}%)`;
}

// === Neural Network ===
class NeuralNetwork {
    constructor(inputSize, hiddenSize, outputSize) {
        this.inputSize = inputSize;
        this.hiddenSize = hiddenSize;
        this.outputSize = outputSize;
        this.weights1 = this.randomMatrix(inputSize, hiddenSize);
        this.weights2 = this.randomMatrix(hiddenSize, outputSize);
    }

    randomMatrix(rows, cols) {
        let m = [];
        for (let i = 0; i < rows; i++) {
            m[i] = [];
            for (let j = 0; j < cols; j++) m[i][j] = Math.random() * 2 - 1;
        }
        return m;
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
        let res = Array(b[0].length).fill(0);
        for (let i = 0; i < b[0].length; i++)
            for (let j = 0; j < a.length; j++)
                res[i] += a[j] * (b[j][i] || 0);
        return res;
    }

    loadWeights() {
        try {
            let data = app.LoadText("neural_weights.json");
            if (data) {
                let w = JSON.parse(data);
                this.weights1 = w.weights1 || this.weights1;
                this.weights2 = w.weights2 || this.weights2;
            }
        } catch (e) {
            // Keep default weights
        }
    }

    saveWeights() {
        app.SaveText("neural_weights.json", JSON.stringify({
            weights1: this.weights1,
            weights2: this.weights2
        }));
    }
}

// === Utility Functions ===
function distance(x1, y1, x2, y2) {
    return Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
}

function rotatePoint(x, y, angle) {
    let cos = Math.cos(angle), sin = Math.sin(angle);
    return { x: x * cos - y * sin, y: x * sin + y * cos };
}

function rotateY(x, y, z, angle) {
    let cos = Math.cos(angle), sin = Math.sin(angle);
    return { x: x * cos + z * sin, y: y, z: -x * sin + z * cos };
}

function rotateX(x, y, z, angle) {
    let cos = Math.cos(angle), sin = Math.sin(angle);
    return { x: x, y: y * cos - z * sin, z: y * sin + z * cos };
}

function project3DToScreen(x, y, z, width, height, fov) {
    let scale = fov / (fov + z);
    let sx = x * scale + width / 2;
    let sy = y * scale + height / 2;
    return { x: sx, y: sy, scale: scale };
}

function applyGravity(obj, pullObj, strength) {
    let dx = pullObj.x - obj.x, dy = pullObj.y - obj.y;
    let dist = Math.sqrt(dx * dx + dy * dy);
    if (dist > 0) {
        obj.vx += (dx / dist) * strength;
        obj.vy += (dy / dist) * strength;
    }
}

// === Generation Functions ===
function generateStars() {
    for (let i = 0; i < 150; i++) {
        stars.push({
            x: Math.random() * SW, y: Math.random() * SH,
            size: 1 + Math.random() * 3,
            speed: 0.5 + Math.random() * 1.5
        });
    }
}

function generateDebris() {
    for (let i = 0; i < 20; i++) {
        debris.push({
            x: Math.random() * SW, y: Math.random() * SH, z: Math.random() * 50,
            vx: (Math.random() - 0.5) * 0.5, vy: (Math.random() - 0.5) * 0.5, vz: (Math.random() - 0.5) * 0.5,
            hits: 0, maxHits: DEBRIS_MAX_HITS,
            size: 2 + Math.random() * 8
        });
    }
}

function generateEnemy() {
    let edge = Math.floor(Math.random() * 4);
    let x, y, angleToCenter;
    switch (edge) {
        case 0: x = Math.random() * SW; y = -30; break;
        case 1: x = SW + 30; y = Math.random() * SH; break;
        case 2: x = Math.random() * SW; y = SH + 30; break;
        case 3: x = -30; y = Math.random() * SH; break;
    }
    angleToCenter = Math.atan2(SH / 2 - y, SW / 2 - x);
    let type = enemyTypes[Math.floor(Math.random() * enemyTypes.length)];
    let factionKeys = Object.keys(factions);
    let faction = factionKeys[Math.floor(Math.random() * factionKeys.length)];
    let key = `${type}_${faction}`;
    if ((enemyCounts[key] || 0) >= 3) { type = enemyTypes[0]; faction = "red"; key = `${type}_${faction}`; }
    enemyCounts[key] = (enemyCounts[key] || 0) + 1;

    enemies.push({
        x: x, y: y, z: Math.random() * 30, type: type, faction: faction,
        color: getRandomColor(faction === "red" ? "red" : faction === "blue" ? "blue" : faction === "green" ? "green" : "yellow"),
        angle: angleToCenter + (Math.random() - 0.5) * 0.5, speed: 1 + Math.random() * 1.5,
        hits: 0, maxHits: enemyHits[type],
        respawnTime: 0,
        vx: 0, vy: 0, vz: 0
    });
}

function generateArtifact() {
    artifacts.push({
        x: Math.random() * SW, y: Math.random() * SH,
        collected: false, pulse: 0
    });
}

function generateChronalArtifact() {
    if (Math.random() < 0.015 && timeDimensionLevel < 3 && chronalArtifacts.length < 2) {
        chronalArtifacts.push({
            x: Math.random() * SW, y: Math.random() * SH,
            level: timeDimensionLevel + 1,
            vx: (Math.random() - 0.5) * 1.8, vy: (Math.random() - 0.5) * 1.8,
            pulse: 0
        });
    }
}

function generateSolarSystem1() {
    // Sun
    solarSystem1.push({ x: SW * 0.2, y: SH * 0.3, z: 0, radius: 20, color: "#FFD700", type: "sun", mass: 1000 });
    let planets = [
        { dist: 60, size: 8, speed: 0.02, color: "#FF6347" },
        { dist: 100, size: 10, speed: 0.015, color: "#1E90FF" },
        { dist: 150, size: 12, speed: 0.01, color: "#228B22" }
    ];
    for (let i = 0; i < planets.length; i++) {
        solarSystem1.push({
            x: SW * 0.2 + planets[i].dist, y: SH * 0.3, z: 0,
            radius: planets[i].size, color: planets[i].color,
            orbitCenter: { x: SW * 0.2, y: SH * 0.3 },
            orbitRadius: planets[i].dist, orbitSpeed: planets[i].speed,
            orbitAngle: Math.random() * Math.PI * 2, type: "planet"
        });
    }
}

function generateSolarSystem2() {
    solarSystem2.push({ x: SW * 0.8, y: SH * 0.7, z: 50, radius: 15, color: "#FFA500", type: "sun", mass: 700 });
    let planets = [
        { dist: 50, size: 6, speed: 0.025, color: "#FF69B4" },
        { dist: 85, size: 9, speed: 0.018, color: "#00CED1" }
    ];
    for (let i = 0; i < planets.length; i++) {
        solarSystem2.push({
            x: SW * 0.8 + planets[i].dist, y: SH * 0.7, z: 50,
            radius: planets[i].size, color: planets[i].color,
            orbitCenter: { x: SW * 0.8, y: SH * 0.7 },
            orbitRadius: planets[i].dist, orbitSpeed: planets[i].speed,
            orbitAngle: Math.random() * Math.PI * 2, type: "planet"
        });
    }
}

// === Ship Models ===
var shipModels = {
    interceptor: { shape: "triangle", size: 15, color: "#1E90FF" },
    bomber: { shape: "diamond", size: 20, color: "#FF6347" },
    cruiser: { shape: "cross", size: 25, color: "#708090" },
    customShip: { shape: "custom", size: 15, color: "#D3D3D3" }
};

function drawShip(ship) {
    let model = shipModels[ship.type] || shipModels.customShip;
    canvas.SetPaintColor(ship.color || model.color);

    if (model.shape === "triangle") {
        let front = rotatePoint(0, -model.size, ship.angle);
        let left = rotatePoint(-model.size / 2, model.size, ship.angle);
        let right = rotatePoint(model.size / 2, model.size, ship.angle);
        canvas.DrawLine((ship.x + front.x) / SW, (ship.y + front.y) / SH, (ship.x + left.x) / SW, (ship.y + left.y) / SH);
        canvas.DrawLine((ship.x + front.x) / SW, (ship.y + front.y) / SH, (ship.x + right.x) / SW, (ship.y + right.y) / SH);
        canvas.DrawLine((ship.x + left.x) / SW, (ship.y + left.y) / SH, (ship.x + right.x) / SW, (ship.y + right.y) / SH);
    } else if (model.shape === "diamond") {
        let top = rotatePoint(0, -model.size, ship.angle);
        let right = rotatePoint(model.size / 2, 0, ship.angle);
        let bottom = rotatePoint(0, model.size, ship.angle);
        let left = rotatePoint(-model.size / 2, 0, ship.angle);
        canvas.DrawLine((ship.x + top.x) / SW, (ship.y + top.y) / SH, (ship.x + right.x) / SW, (ship.y + right.y) / SH);
        canvas.DrawLine((ship.x + right.x) / SW, (ship.y + right.y) / SH, (ship.x + bottom.x) / SW, (ship.y + bottom.y) / SH);
        canvas.DrawLine((ship.x + bottom.x) / SW, (ship.y + bottom.y) / SH, (ship.x + left.x) / SW, (ship.y + left.y) / SH);
        canvas.DrawLine((ship.x + left.x) / SW, (ship.y + left.y) / SH, (ship.x + top.x) / SW, (ship.y + top.y) / SH);
    } else if (model.shape === "cross") {
        let v1 = rotatePoint(0, -model.size, ship.angle);
        let v2 = rotatePoint(0, model.size, ship.angle);
        let h1 = rotatePoint(-model.size / 2, 0, ship.angle);
        let h2 = rotatePoint(model.size / 2, 0, ship.angle);
        canvas.DrawLine((ship.x + v1.x) / SW, (ship.y + v1.y) / SH, (ship.x + v2.x) / SW, (ship.y + v2.y) / SH);
        canvas.DrawLine((ship.x + h1.x) / SW, (ship.y + h1.y) / SH, (ship.x + h2.x) / SW, (ship.y + h2.y) / SH);
    } else {
        // Custom ship - arrow with wings
        let front = rotatePoint(0, -model.size, ship.angle);
        let back = rotatePoint(0, model.size * 0.6, ship.angle);
        let leftWing = rotatePoint(-model.size, model.size * 0.3, ship.angle);
        let rightWing = rotatePoint(model.size, model.size * 0.3, ship.angle);
        canvas.DrawLine((ship.x + front.x) / SW, (ship.y + front.y) / SH, (ship.x + leftWing.x) / SW, (ship.y + leftWing.y) / SH);
        canvas.DrawLine((ship.x + front.x) / SW, (ship.y + front.y) / SH, (ship.x + rightWing.x) / SW, (ship.y + rightWing.y) / SH);
        canvas.DrawLine((ship.x + leftWing.x) / SW, (ship.y + leftWing.y) / SH, (ship.x + back.x) / SW, (ship.y + back.y) / SH);
        canvas.DrawLine((ship.x + rightWing.x) / SW, (ship.y + rightWing.y) / SH, (ship.x + back.x) / SW, (ship.y + back.y) / SH);
    }

    // Shields glow
    if (ship.shieldsActive && ship.shields > 0) {
        canvas.SetPaintColor(colors.game.shields);
        canvas.SetAlpha(Math.min(ship.shields / 100, 0.5));
        canvas.DrawCircle(ship.x / SW, ship.y / SH, (model.size + 5) / SW);
        canvas.SetAlpha(1);
    }

    // Thrust trail
    if (ship.thrusting) {
        let back = rotatePoint(0, model.size * (ship.type === "cruiser" ? 0.6 : 1), ship.angle + Math.PI);
        canvas.SetPaintColor(colors.game.trail);
        canvas.SetAlpha(0.6);
        canvas.DrawCircle((ship.x + back.x) / SW, (ship.y + back.y) / SH, 8 / SW);
        canvas.SetAlpha(1);
    }
}

// === Input Handling ===
function onTouchDown(e) {
    if (inTitle) {
        inTitle = false;
        isRunning = true;
        sounds.intro.Stop();
        sounds.game.SetLooping(true);
        sounds.game.Play();
        enemies = [];
        for (let i = 0; i < 3; i++) generateEnemy();
        gameLoop();
        return;
    }
    player.thrusting = true;
    sounds.thrust.Play();
}

function onTouchMove(e) {
    let dx = e.x - player.x / SW;
    let dy = e.y - player.y / SH;
    player.angle = Math.atan2(dy, dx) - Math.PI / 2;
    player.thrusting = true;
}

function onTouchUp(e) {
    player.thrusting = false;
    sounds.thrust.Stop();
}

function restartGame() {
    player.x = SW / 2; player.y = SH / 2; player.vx = 0; player.vy = 0; player.vz = 0;
    player.hits = 0; player.score = 0; player.shields = 100; player.power = 100;
    player.weapon = "bullet"; player.weaponTimer = Date.now();
    player.thrusting = false;
    enemies = []; projectiles = []; artifacts = []; chronalArtifacts = [];
    timeDimensionLevel = 1; chronalEnergy = 100;
    for (let i = 0; i < 3; i++) generateEnemy();
    player.respawnTime = 0; player.history = [];
    sounds.game.Play();
    isRunning = true;
}

function exitGame() {
    app.Exit();
}

function onSpeechResult(results) {
    let cmd = results[0].toLowerCase();
    if (cmd.includes("first person")) viewMode = "firstPerson";
    if (cmd.includes("third person")) viewMode = "thirdPerson";
    if (cmd.includes("top down") || cmd.includes("top view")) viewMode = "topDown";
    if (cmd.includes("weapon")) {
        let w = cmd.split("weapon").pop().trim();
        if (weapons[w]) player.weapon = w;
    }
}

// === Update Functions ===
function updateShip(ship) {
    // Thrust
    if (ship.thrusting) {
        let thrust = ship === player ? 0.15 : 0.1;
        ship.vx += Math.cos(ship.angle + Math.PI) * thrust;
        ship.vy += Math.sin(ship.angle + Math.PI) * thrust;
        if (ship === player) ship.power = Math.max(0, ship.power - POWER_DRAIN_RATE);
    }

    // Friction
    ship.vx *= 0.98; ship.vy *= 0.98;

    // Ultrahyperbolic glitch at level 3
    if (timeDimensionLevel >= 3 && Math.random() < 0.004) {
        ship.vx += (Math.random() - 0.5) * 2;
        ship.vy += (Math.random() - 0.5) * 2;
        if (ship === player) app.ShowPopup("Temporal instability!");
    }

    // Update position
    ship.x += ship.vx; ship.y += ship.vy;
    ship.x = (ship.x < 0 ? ship.x + SW : ship.x > SW ? ship.x - SW : ship.x);
    ship.y = (ship.y < 0 ? ship.y + SH : ship.y > SH ? ship.y - SH : ship.y);
    ship.z += ship.vz;
    if (ship.z < -50 || ship.z > 50) ship.vz *= -1;

    // Shields regen
    if (ship.shieldsActive && ship.shields < 100) ship.shields = Math.min(100, ship.shields + SHIELD_REGEN_RATE);

    // Enemy AI
    if (ship !== player && ship.hits < ship.maxHits) {
        let dx = player.x - ship.x, dy = player.y - ship.y;
        let dist = Math.sqrt(dx * dx + dy * dy);
        if (dist > 0) {
            let desiredAngle = Math.atan2(dy, dx) - Math.PI / 2;
            let angleDiff = desiredAngle - ship.angle;
            while (angleDiff > Math.PI) angleDiff -= Math.PI * 2;
            while (angleDiff < -Math.PI) angleDiff += Math.PI * 2;
            ship.angle += angleDiff * 0.05;
            if (dist > 40) {
                ship.thrusting = true;
                ship.vx += Math.cos(ship.angle + Math.PI) * 0.1;
                ship.vy += Math.sin(ship.angle + Math.PI) * 0.1;
            }
            if (dist < 300 && Math.random() < 0.02) fireProjectile(ship);
        }
        ship.thrusting = false;

        // Enemy history for ghost trail
        if (timeDimensionLevel >= 2) {
            if (!ship.history) ship.history = [];
            ship.history.push({ x: ship.x, y: ship.y });
            if (ship.history.length > 10) ship.history.shift();
        }
    }
}

function updateProjectiles() {
    for (let i = projectiles.length - 1; i >= 0; i--) {
        let p = projectiles[i];
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > SW || p.y < 0 || p.y > SH) {
            projectiles.splice(i, 1);
        }
    }
}

function updateDebris() {
    for (let i = debris.length - 1; i >= 0; i--) {
        let d = debris[i];
        d.x += d.vx; d.y += d.vy; d.z += d.vz;
        d.x += (player.x - SW / 2) * 0.01;
        d.y += (player.y - SH / 2) * 0.01;
        if (d.x < 0) d.x += SW; if (d.x > SW) d.x -= SW;
        if (d.y < 0) d.y += SH; if (d.y > SH) d.y -= SH;
        solarSystem1.forEach(s => { if (s.type === "sun") applyGravity(d, s, 0.005); });
        solarSystem2.forEach(s => { if (s.type === "sun") applyGravity(d, s, 0.003); });
    }
}

function updateSolarSystem1() {
    let sun = solarSystem1[0];
    for (let i = 1; i < solarSystem1.length; i++) {
        let p = solarSystem1[i];
        p.orbitAngle += p.orbitSpeed;
        p.x = p.orbitCenter.x + Math.cos(p.orbitAngle) * p.orbitRadius;
        p.y = p.orbitCenter.y + Math.sin(p.orbitAngle) * p.orbitRadius;
    }
}

function updateSolarSystem2() {
    let sun = solarSystem2[0];
    for (let i = 1; i < solarSystem2.length; i++) {
        let p = solarSystem2[i];
        p.orbitAngle += p.orbitSpeed;
        p.x = p.orbitCenter.x + Math.cos(p.orbitAngle) * p.orbitRadius;
        p.y = p.orbitCenter.y + Math.sin(p.orbitAngle) * p.orbitRadius;
    }
}

// === Collision Detection ===
function checkCollisions() {
    // Player vs enemies
    for (let i = enemies.length - 1; i >= 0; i--) {
        let e = enemies[i];
        if (e.hits >= e.maxHits) continue;
        if (distance(player.x, player.y, e.x, e.y) < 25) {
            if (player.shieldsActive && player.shields > 0) {
                player.shields -= 20;
                if (player.shields <= 0) player.shieldsActive = false;
            } else {
                player.hits++;
                if (player.hits >= MAX_HITS) {
                    player.respawnTime = Date.now();
                    sounds.explode.Play();
                }
            }
            e.hits = e.maxHits;
            e.respawnTime = Date.now();
            sounds.explode.Play();
        }
    }

    // Projectiles vs enemies
    for (let i = projectiles.length - 1; i >= 0; i--) {
        let p = projectiles[i];
        for (let j = enemies.length - 1; j >= 0; j--) {
            let e = enemies[j];
            if (e.hits >= e.maxHits) continue;
            if (distance(p.x, p.y, e.x, e.y) < 15) {
                e.hits += weapons[p.type].hits;
                if (e.hits >= e.maxHits) {
                    e.respawnTime = Date.now();
                    if (p.owner === "player") {
                        let key = `${e.type}_${e.faction}`;
                        enemyCounts[key]--;
                        player.score += enemyHits[e.type] * 10;
                    }
                    sounds.explode.Play();
                }
                projectiles.splice(i, 1);
                break;
            }
        }
    }

    // Projectiles vs player
    for (let i = projectiles.length - 1; i >= 0; i--) {
        let p = projectiles[i];
        if (p.owner === "enemy" && distance(p.x, p.y, player.x, player.y) < 15) {
            if (player.shieldsActive && player.shields > 0) {
                player.shields -= 20;
                if (player.shields <= 0) player.shieldsActive = false;
            } else {
                player.hits++;
                if (player.hits >= MAX_HITS) {
                    player.respawnTime = Date.now();
                    sounds.explode.Play();
                }
            }
            projectiles.splice(i, 1);
        }
    }
}

function checkDebrisCollisions(now) {
    for (let i = debris.length - 1; i >= 0; i--) {
        let d = debris[i];
        if (distance(player.x, player.y, d.x, d.y) < d.size + 10) {
            debris.splice(i, 1);
            if (player.shieldsActive && player.shields > 0) {
                player.shields -= 10;
            } else {
                player.hits++;
                if (player.hits >= MAX_HITS) {
                    player.respawnTime = Date.now();
                    sounds.explode.Play();
                }
            }
        }
    }
}

function checkArtifacts() {
    for (let i = artifacts.length - 1; i >= 0; i--) {
        let a = artifacts[i];
        if (distance(player.x, player.y, a.x, a.y) < 20) {
            artifacts.splice(i, 1);
            player.score += 100;
        }
    }
}

function checkChronalArtifacts() {
    for (var i = chronalArtifacts.length - 1; i >= 0; i--) {
        var a = chronalArtifacts[i];
        a.x += a.vx; a.y += a.vy;
        a.vx *= 0.98; a.vy *= 0.98;
        a.x = (a.x < 0 ? a.x + SW : a.x > SW ? a.x - SW : a.x);
        a.y = (a.y < 0 ? a.y + SH : a.y > SH ? a.y - SH : a.y);
        if (distance(a.x, a.y, player.x, player.y) < 30) {
            if (player.score >= CHRONAL_THRESHOLD[a.level - 1]) {
                timeDimensionLevel = a.level;
                chronalEnergy = 100 * a.level;
                app.ShowPopup("Chronal Level " + a.level + " Unlocked!\nExtra Time Dimension(s) Accessed");
                if (sounds.chronal) sounds.chronal.Play();
            }
            chronalArtifacts.splice(i, 1);
        }
    }
}

// === Weapon Functions ===
function fireProjectile(ship) {
    let w = weapons[ship.weapon] || weapons["bullet"];
    if (!ship.thrusting && ship.power < w.cost) return;
    ship.power -= w.cost;

    let front = rotatePoint(0, -15, ship.angle);
    projectiles.push({
        x: ship.x + front.x, y: ship.y + front.y,
        vx: Math.cos(ship.angle + Math.PI) * 8 + ship.vx * 0.5,
        vy: Math.sin(ship.angle + Math.PI) * 8 + ship.vy * 0.5,
        type: ship.weapon, color: w.color, owner: ship === player ? "player" : "enemy"
    });
}

function updateWeapons(now) {
    if (now - player.weaponTimer > WEAPON_DELAY) {
        player.weapon = "bullet";
        player.weaponTimer = now;
    }
}

// === Neural Network OODA Loop ===
function oodaLoop() {
    let input = [
        player.x / SW, player.y / SH, player.angle / (Math.PI * 2),
        (enemies[0] && enemies[0].hits < enemies[0].maxHits) ? enemies[0].x / SW : 0.5,
        (enemies[0] && enemies[0].hits < enemies[0].maxHits) ? enemies[0].y / SH : 0.5,
        viewMode === "topDown" ? 0 : viewMode === "firstPerson" ? 1 : 0.5
    ];
    let output = neuralNetwork ? neuralNetwork.feedforward(input) : [0, 0, 0, 0];

    if (output[2] > 0.7 && player.power > weapons[player.weapon].cost) fireProjectile(player);
    if (output[3] > 0.7 && !player.shieldsActive) player.shieldsActive = true;

    // Auto-switch view based on proximity
    let nearest = null, nearestDist = Infinity;
    enemies.forEach(e => {
        if (e.hits >= e.maxHits) return;
        let d = distance(player.x, player.y, e.x, e.y);
        if (d < nearestDist) { nearestDist = d; nearest = e; }
    });
    if (nearestDist < 150) viewMode = "firstPerson";
    else if (nearestDist < 300) viewMode = "thirdPerson";
    else viewMode = "topDown";
}

// === Drawing Functions ===
function drawSolarSystem1() {
    solarSystem1.forEach(s => {
        canvas.SetPaintColor(s.color);
        if (s.type === "sun") {
            canvas.SetPaintColor("#FFD700");
            canvas.DrawCircle(s.x / SW, s.y / SH, s.radius / SW);
            canvas.SetPaintColor("#FFFF00");
            canvas.SetAlpha(0.5);
            canvas.DrawCircle(s.x / SW, s.y / SH, (s.radius + 5) / SW);
            canvas.SetAlpha(1);
        } else {
            canvas.DrawCircle(s.x / SW, s.y / SH, s.radius / SW);
        }
    });
}

function drawSolarSystem2() {
    solarSystem2.forEach(s => {
        canvas.SetPaintColor(s.color);
        if (s.type === "sun") {
            canvas.DrawCircle(s.x / SW, s.y / SH, s.radius / SW);
            canvas.SetPaintColor("#FFD580");
            canvas.SetAlpha(0.5);
            canvas.DrawCircle(s.x / SW, s.y / SH, (s.radius + 5) / SW);
            canvas.SetAlpha(1);
        } else {
            canvas.DrawCircle(s.x / SW, s.y / SH, s.radius / SW);
        }
    });
}

function drawHUD() {
    canvas.SetPaintColor(colors.game.hud);
    canvas.SetTextSize(12);
    var y = 0.03;
    canvas.DrawText(`Score: ${player.score}`, 0.05, y);
    canvas.DrawText(`Hits: ${player.hits}/${MAX_HITS}`, 0.22, y);
    canvas.DrawText(`Weapon: ${player.weapon}`, 0.39, y);
    canvas.DrawText(`Chronal: Lvl ${timeDimensionLevel}`, 0.58, y);
    canvas.DrawText(`View: ${viewMode}`, 0.75, y);
    canvas.SetPaintColor(colors.game.shields);
    canvas.DrawText(`Shields: ${player.shieldsActive ? player.shields.toFixed(0) + "%" : "OFF"}`, 0.05, y + 0.06);
    canvas.DrawText(`Power: ${player.power.toFixed(0)}%`, 0.05, y + 0.09);

    // Chronal energy bar
    if (timeDimensionLevel >= 2) {
        canvas.SetPaintColor(colors.game.chronal);
        canvas.DrawText(`Chronal Energy: ${chronalEnergy.toFixed(0)}%`, 0.22, y + 0.06);
    }
}

function drawTopDownView() {
    canvas.Clear();
    canvas.SetPaintColor(colors.game.background);
    canvas.DrawRectangle(0, 0, 1, 1);

    // Chronal overlay
    if (timeDimensionLevel >= 2) {
        canvas.SetPaintColor(colors.game.chronal);
        canvas.SetAlpha(0.08 + 0.06 * Math.sin(Date.now() / 400));
        canvas.DrawRectangle(0, 0, 1, 1);
        canvas.SetAlpha(1);
    }

    // Stars
    canvas.SetPaintColor(colors.game.star);
    stars.forEach(s => {
        canvas.DrawCircle(s.x / SW, s.y / SH, s.size / SW);
        s.y += s.speed / SH;
        if (s.y > SH) { s.y = 0; s.x = Math.random() * SW; }
    });

    drawSolarSystem1();
    drawSolarSystem2();

    // Debris
    canvas.SetPaintColor(colors.game.debris);
    debris.forEach(d => {
        let projected = project3DToScreen(d.x, d.y, d.z, SW, SH, 200);
        canvas.DrawCircle(projected.x / SW, projected.y / SH, (d.size * projected.scale) / SW);
    });

    // Player
    if (player.hits < MAX_HITS) drawShip(player);

    // Player ghost trails
    if (timeDimensionLevel >= 2 && player.history.length > 0) {
        canvas.SetPaintColor(colors.game.player);
        canvas.SetAlpha(0.4);
        player.history.forEach((pos, idx) => {
            var alpha = (idx + 1) / player.history.length;
            canvas.SetAlpha(0.15 + 0.35 * alpha);
            canvas.DrawCircle(pos.x / SW, pos.y / SH, 10 / SW);
        });
        canvas.SetAlpha(1);
    }

    // Enemies
    enemies.forEach(e => {
        if (e.hits < e.maxHits) {
            canvas.SetPaintColor(e.color);
            let size = 10;
            if (e.type === "cube") size = 12;
            if (e.type === "prism") size = 14;
            if (e.type === "pyramid") size = 11;
            if (e.type === "octahedron") size = 9;
            if (e.type === "dodecahedron") size = 13;
            canvas.DrawCircle(e.x / SW, e.y / SH, size / SW);

            // Enemy ghost trails
            if (timeDimensionLevel >= 2 && e.history) {
                canvas.SetPaintColor(factions[e.faction] || "#FFFFFF");
                canvas.SetAlpha(0.3);
                e.history.forEach((pos, idx) => {
                    canvas.SetAlpha(0.1 + 0.3 * (idx + 1) / e.history.length);
                    canvas.DrawCircle(pos.x / SW, pos.y / SH, 8 / SW);
                });
                canvas.SetAlpha(1);
            }
        }
    });

    // Projectiles
    projectiles.forEach(p => {
        canvas.SetPaintColor(p.color);
        canvas.DrawCircle(p.x / SW, p.y / SH, 3 / SW);
    });

    // Artifacts
    artifacts.forEach(a => {
        canvas.SetPaintColor("#FFD700");
        canvas.SetAlpha(0.7 + 0.3 * Math.sin(Date.now() / 200));
        canvas.DrawCircle(a.x / SW, a.y / SH, 6 / SW);
        canvas.SetAlpha(1);
    });

    // Chronal Artifacts
    chronalArtifacts.forEach(a => {
        canvas.SetPaintColor(colors.game.chronal);
        canvas.SetAlpha(0.8 + 0.2 * Math.sin(Date.now() / 300));
        // Draw as pulsing orb
        let pulse = 8 + 4 * Math.sin(Date.now() / 200);
        canvas.DrawCircle(a.x / SW, a.y / SH, pulse / SW);
        canvas.SetAlpha(0.5);
        canvas.DrawCircle(a.x / SW, a.y / SH, (pulse + 4) / SW);
        canvas.SetAlpha(1);
    });

    drawHUD();
    canvas.Update();
}

function drawFirstPersonView() {
    canvas.Clear();
    canvas.SetPaintColor(colors.game.background);
    canvas.DrawRectangle(0, 0, 1, 1);

    // Chronal overlay
    if (timeDimensionLevel >= 2) {
        canvas.SetPaintColor(colors.game.chronal);
        canvas.SetAlpha(0.1 + 0.07 * Math.sin(Date.now() / 350));
        canvas.DrawRectangle(0, 0, 1, 1);
        canvas.SetAlpha(1);
    }

    // Draw player ship at bottom
    if (player.hits < MAX_HITS) {
        canvas.SetPaintColor(colors.game.player);
        let shipY = 0.85;
        canvas.DrawCircle(0.5, shipY, 0.05);
        canvas.SetPaintColor(colors.game.trail);
        if (player.thrusting) {
            canvas.DrawCircle(0.5, shipY + 0.04, 0.03);
        }
    }

    // Draw enemies on "horizon"
    let centerX = 0.5, centerY = 0.5, horizonY = 0.4;
    enemies.forEach(e => {
        if (e.hits >= e.maxHits) return;
        let dx = e.x - player.x, dy = e.y - player.y;
        let dist = Math.sqrt(dx * dx + dy * dy);
        if (dist > 0 && dist < 400) {
            let angle = Math.atan2(dy, dx) - player.angle;
            let relX = centerX + Math.sin(angle) * (dist / 1000);
            let relY = horizonY - Math.cos(angle) * (dist / 1000);
            canvas.SetPaintColor(e.color);
            let size = Math.max(0.005, 0.03 - dist / 5000);
            canvas.DrawCircle(relX, relY, size);
        }
    });

    // Stars
    canvas.SetPaintColor(colors.game.star);
    stars.forEach(s => {
        let sy = horizonY + (s.y / SH) * 0.4;
        if (sy < horizonY + 0.3) {
            canvas.DrawCircle(s.x / SW, sy, s.size / (SW * 2));
        }
    });

    drawHUD();
    canvas.Update();
}

function drawThirdPersonView() {
    canvas.Clear();
    canvas.SetPaintColor(colors.game.background);
    canvas.DrawRectangle(0, 0, 1, 1);

    // Chronal overlay
    if (timeDimensionLevel >= 2) {
        canvas.SetPaintColor(colors.game.chronal);
        canvas.SetAlpha(0.06 + 0.05 * Math.sin(Date.now() / 400));
        canvas.DrawRectangle(0, 0, 1, 1);
        canvas.SetAlpha(1);
    }

    // Draw player from "behind"
    if (player.hits < MAX_HITS) {
        canvas.SetPaintColor(colors.game.player);
        let viewX = 0.5, viewY = 0.7;
        canvas.DrawCircle(viewX, viewY, 0.04);
        canvas.SetPaintColor(colors.game.trail);
        if (player.thrusting) {
            canvas.DrawCircle(viewX, viewY + 0.03, 0.025);
            canvas.DrawCircle(viewX, viewY + 0.05, 0.015);
        }
    }

    // Projectiles in perspective
    projectiles.forEach(p => {
        let dx = p.x - player.x, dy = p.y - player.y;
        let dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 300) {
            let relX = 0.5 + (p.x - player.x) / SW * 0.5;
            let relY = 0.5 + (p.y - player.y) / SH * 0.5;
            canvas.SetPaintColor(p.color);
            canvas.DrawCircle(relX, relY, 0.008 - dist / 50000);
        }
    });

    // Enemies
    enemies.forEach(e => {
        if (e.hits >= e.maxHits) return;
        let dx = e.x - player.x, dy = e.y - player.y;
        let dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 500) {
            let relX = 0.5 + (e.x - player.x) / SW * 0.5;
            let relY = 0.5 + (e.y - player.y) / SH * 0.5;
            canvas.SetPaintColor(e.color);
            let size = Math.max(0.008, 0.03 - dist / 8000);
            canvas.DrawCircle(relX, relY, size);
        }
    });

    drawHUD();
    canvas.Update();
}

function drawTitle() {
    canvas.Clear();
    canvas.SetPaintColor(colors.game.background);
    canvas.DrawRectangle(0, 0, 1, 1);

    drawSolarSystem1();
    drawSolarSystem2();

    canvas.SetPaintColor("#FFFFFF");
    canvas.SetTextSize(0.09 * SW);
    canvas.DrawText("Chronospace Explorer", 0.5, 0.18, "center");

    canvas.SetTextSize(0.045 * SW);
    canvas.DrawText("Experience extra time dimensions", 0.5, 0.28, "center");
    canvas.DrawText("Collect Chronal Artifacts to unlock", 0.5, 0.34, "center");
    canvas.DrawText(`Level ${timeDimensionLevel} Active (${timeDimensionLevel + 1}D+${timeDimensionLevel - 1}T)`, 0.5, 0.40, "center");
    canvas.DrawText("Touch to Start", 0.5, 0.7, "center");

    canvas.Update();
}

// === Respawn ===
function respawnShip(ship, x, y, z) {
    ship.x = x; ship.y = y; ship.z = z;
    ship.vx = 0; ship.vy = 0; ship.vz = 0;
    ship.angle = 0;
    ship.hits = 0;
    ship.shields = 100;
    ship.power = 100;
    sounds.respawn.Play();
}

// === Main Initialization ===
function OnStart() {
    app.SetOrientation("Landscape");
    SW = app.GetScreenHeight();
    SH = app.GetScreenWidth();
    player.x = SW / 2; player.y = SH / 2;

    lay = app.CreateLayout("Linear", "FillXY");

    canvas = app.CreateImage(null, 1, 1, "fix", SW, SH);
    canvas.SetAutoUpdate(false);
    canvas.SetOnTouchDown(onTouchDown);
    canvas.SetOnTouchMove(onTouchMove);
    canvas.SetOnTouchUp(onTouchUp);
    lay.AddChild(canvas);

    // Controls
    var controlLay = app.CreateLayout("Linear", "Horizontal");
    controlLay.SetPosition(0.70, 0.01);

    var btnRestart = app.CreateButton("Restart", 0.15, 0.05);
    btnRestart.SetOnTouch(restartGame);
    controlLay.AddChild(btnRestart);

    var btnExit = app.CreateButton("Exit", 0.15, 0.05);
    btnExit.SetMargins(0.02, 0, 0, 0);
    btnExit.SetOnTouch(exitGame);
    controlLay.AddChild(btnExit);

    lay.AddChild(controlLay);
    app.AddLayout(lay);

    neuralNetwork = new NeuralNetwork(6, 5, 4);
    neuralNetwork.loadWeights();

    generateStars();
    generateDebris();
    generateSolarSystem1();
    generateSolarSystem2();

    sounds.intro.SetLooping(true);
    sounds.intro.Play();

    speech.SetOnResult(onSpeechResult);

    // Periodic generators
    setInterval(() => {
        if (Math.random() < 0.08) generateArtifact();
        if (Math.random() < 0.015) generateChronalArtifact();
    }, 8000);
}

// === Game Loop ===
function gameLoop() {
    if (!isRunning) {
        drawTitle();
        return setTimeout(gameLoop, 16);
    }

    let now = Date.now();

    // Respawn check
    if (player.hits >= MAX_HITS && now - player.respawnTime > RESPAWN_DELAY) {
        respawnShip(player, SW / 2, SH / 2, 0);
    }

    enemies.forEach((e, i) => {
        if (e.hits >= e.maxHits && now - e.respawnTime > RESPAWN_DELAY) {
            let key = `${e.type}_${e.faction}`;
            enemyCounts[key]--;
            enemies.splice(i, 1);
            generateEnemy();
        }
    });

    // Update player history for ghosts
    if (timeDimensionLevel >= 2 && player.hits < MAX_HITS) {
        player.history.push({ x: player.x, y: player.y });
        if (player.history.length > 12) player.history.shift();
    }

    updateShip(player);
    enemies.forEach(updateShip);
    updateProjectiles();
    updateDebris();
    updateSolarSystem1();
    updateSolarSystem2();
    checkCollisions();
    checkDebrisCollisions(now);
    checkArtifacts();
    checkChronalArtifacts();
    updateWeapons(now);

    if (now - lastOODATime > 1000) {
        oodaLoop();
        lastOODATime = now;
    }

    // Render based on view mode
    if (viewMode === "firstPerson") drawFirstPersonView();
    else if (viewMode === "thirdPerson") drawThirdPersonView();
    else drawTopDownView();

    setTimeout(gameLoop, 16);
}

// Start
OnStart();
