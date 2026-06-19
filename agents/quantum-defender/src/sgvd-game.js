// SGVD - Solar GraVitaional Duel
// Enhanced Solar System Module
// Based on user's astronomical palette implementation
// DroidScript space shooter with dual solar systems

// ============================================================================
// CONSTANTS & CONFIGURATION
// ============================================================================

const GAME_CONFIG = {
    // Screen dimensions
    SW: window.innerWidth || 1920,  // Screen width
    SH: window.innerHeight || 1080,   // Screen height
    
    // Solar system settings
    NUM_PLANETS: { min: 1, max: 5 },
    SUN_RADIUS: { min: 50, max: 80 },
    PLANET_SIZE: { min: 0.15, max: 0.70 },  // Relative to sun
    ORBIT_SPACING: { min: 40, max: 120 },
    
    // Game mechanics
    GRAVITY_CONSTANT: 0.5,
    MAX_VELOCITY: 15,
    FRICTION: 0.98,
    
    // Neural AI
    OODA_UPDATE_MS: 250,
    ENEMY_SPAWN_RATE: 3000,
    
    // Visual
    GLOW_ALPHA: 0.25,
    RING_ALPHA: 0.4,
    STAR_COUNT: 200
};

// Planet type definitions with astronomical accuracy
const PLANET_TYPES = [
    {
        name: "terrestrial",
        colors: ["#C1440E", "#A0522D", "#88AADD", "#8B7355", "#CD853F"],
        description: "Rocky worlds with thin atmospheres",
        massMultiplier: 1.0,
        hasRings: false,
        maxMoons: 2
    },
    {
        name: "super-earth",
        colors: ["#6699FF", "#4682B4", "#5F9EA0", "#6495ED"],
        description: "Larger terrestrial with thick atmospheres",
        massMultiplier: 2.5,
        hasRings: false,
        maxMoons: 3
    },
    {
        name: "gas-giant",
        colors: ["#FFCC99", "#D2691E", "#DEB887", "#F4A460", "#CD853F"],
        description: "Massive worlds with banded atmospheres",
        massMultiplier: 10.0,
        hasRings: true,
        ringChance: 0.45,
        maxMoons: 5
    },
    {
        name: "ice-giant",
        colors: ["#4682B4", "#5F9EA0", "#87CEEB", "#B0C4DE", "#ADD8E6"],
        description: "Cold worlds with methane atmospheres",
        massMultiplier: 8.0,
        hasRings: true,
        ringChance: 0.25,
        maxMoons: 4
    }
];

// Star types with realistic temperatures
const STAR_TYPES = [
    { name: "red-dwarf", color: "#FF6347", temp: 3500, mass: 0.5, radius: 0.3 },
    { name: "yellow-dwarf", color: "#FFD700", temp: 5800, mass: 1.0, radius: 1.0 },
    { name: "orange-giant", color: "#FFB347", temp: 4500, mass: 1.5, radius: 1.5 },
    { name: "blue-white", color: "#87CEFA", temp: 12000, mass: 2.5, radius: 1.8 }
];

// Bob Ross palette integration for artistic elements
const BOB_ROSS_PALETTE = {
    "Alizarin Crimson": "#E32636",
    "Bright Red": "#FF6347",
    "Cadmium Yellow": "#FFD700",
    "Dark Sienna": "#3C1414",
    "Indian Yellow": "#FFB347",
    "Midnight Black": "#000000",
    "Phthalo Blue": "#000F89",
    "Phthalo Green": "#123524",
    "Prussian Blue": "#003153",
    "Sap Green": "#507D2A",
    "Van Dyke Brown": "#664228",
    "Yellow Ochre": "#F0BB5E",
    "Titanium White": "#FDF5E6"
};

// BR-X Duality palette for special effects
const DUALITY_PALETTE = {
    "Rebel Red": "#B22222",
    "Stealth Black": "#2F4F4F",
    "Combat Green": "#556B2F",
    "Urban Gray": "#A9A9A9",
    "Intense Blue": "#1E90FF",
    "Spiritual Blue": "#0000FF",
    "Harmony Green": "#00FF00",
    "Sacred Gold": "#FFD700",
    "Tranquil Turquoise": "#40E0D0",
    "Mystic Purple": "#800080"
};

// ============================================================================
// GAME STATE
// ============================================================================

let gameState = {
    phase: "MENU",  // MENU, PLAYING, PAUSED, GAMEOVER
    score: 0,
    level: 1,
    lives: 3,
    time: 0,
    
    // Solar systems
    solarSystemLeft: [],
    solarSystemRight: [],
    
    // Entities
    player: null,
    enemies: [],
    projectiles: [],
    debris: [],
    artifacts: [],
    
    // Neural AI
    aiMemory: [],
    aiDecision: null,
    oodaPhase: "OBSERVE",
    
    // Input
    touch: { active: false, x: 0, y: 0 },
    speech: { lastCommand: null, confidence: 0 }
};

// Canvas reference (set in OnStart)
let canvas = null;

// ============================================================================
// SOLAR SYSTEM GENERATION
// ============================================================================

/**
 * Generate a complete solar system with realistic astronomical features
 * @param {Array} systemArray - Array to populate with celestial bodies
 * @param {number} centerX - X coordinate for system center
 * @param {number} centerY - Y coordinate for system center
 * @param {boolean} isLeft - Whether this is the left system (affects generation)
 */
function generateSolarSystem(systemArray, centerX, centerY, isLeft = true) {
    systemArray.length = 0;
    
    // Select star type
    const starType = STAR_TYPES[Math.floor(Math.random() * STAR_TYPES.length)];
    const sunRadius = GAME_CONFIG.SUN_RADIUS.min + 
        Math.random() * (GAME_CONFIG.SUN_RADIUS.max - GAME_CONFIG.SUN_RADIUS.min);
    const sunMass = sunRadius * sunRadius * 1200;
    
    // Create star with glow
    systemArray.push({
        type: "sun",
        subtype: starType.name,
        x: centerX,
        y: centerY,
        radius: sunRadius,
        color: starType.color,
        mass: sunMass,
        temperature: starType.temp,
        glow: true,
        glowRadius: sunRadius * 1.6,
        gravityWell: sunRadius * 3.5  // Area of gravitational influence
    });
    
    // Generate 1-5 planets
    const numPlanets = GAME_CONFIG.NUM_PLANETS.min + 
        Math.floor(Math.random() * (GAME_CONFIG.NUM_PLANETS.max - GAME_CONFIG.NUM_PLANETS.min + 1));
    
    let orbitRadius = sunRadius * 2.8;
    
    for (let i = 0; i < numPlanets; i++) {
        // Select planet type
        const pTypeData = PLANET_TYPES[Math.floor(Math.random() * PLANET_TYPES.length)];
        
        // Size relative to sun (15-70%)
        const sizeRatio = GAME_CONFIG.PLANET_SIZE.min + 
            Math.random() * (GAME_CONFIG.PLANET_SIZE.max - GAME_CONFIG.PLANET_SIZE.min);
        const planetRadius = sunRadius * sizeRatio;
        
        // Mass based on size and type
        const planetMass = planetRadius * planetRadius * 80 * pTypeData.massMultiplier;
        
        // Select color from type-specific palette
        const colorIndex = Math.floor(Math.random() * pTypeData.colors.length);
        let planetColor = pTypeData.colors[colorIndex];
        
        // Apply subtle hue shift for variety
        planetColor = adjustHue(planetColor, (Math.random() - 0.5) * 20);
        
        // Calculate orbit speed (slower for outer planets)
        const orbitSpeed = 0.0008 / (i + 1.5);
        const angle = Math.random() * Math.PI * 2;
        
        // Determine if planet has rings
        const hasRings = pTypeData.hasRings && 
            Math.random() < (pTypeData.ringChance || 0);
        
        // Create planet
        const planet = {
            type: "planet",
            subtype: pTypeData.name,
            radius: planetRadius,
            orbitRadius: orbitRadius,
            orbitSpeed: orbitSpeed,
            angle: angle,
            color: planetColor,
            mass: planetMass,
            x: centerX + Math.cos(angle) * orbitRadius,
            y: centerY + Math.sin(angle) * orbitRadius,
            velocity: { x: 0, y: 0 },
            hasRings: hasRings,
            ringColor: "#E0E0FF",
            ringInner: planetRadius * 1.5,
            ringOuter: planetRadius * 2.2,
            moons: [],
            captured: false  // Can be captured by gravity
        };
        
        // Add moons for larger planets
        if (planetRadius > sunRadius * 0.3) {
            const numMoons = Math.floor(Math.random() * (pTypeData.maxMoons + 1));
            
            for (let m = 0; m < numMoons; m++) {
                const moon = {
                    dist: planetRadius * (1.2 + Math.random() * 1.8),
                    radius: planetRadius * (0.08 + Math.random() * 0.15),
                    angle: Math.random() * Math.PI * 2,
                    speed: 0.003 / (m + 1),
                    color: Math.random() < 0.7 ? "#C0C0C0" : "#A0A0FF",
                    mass: planetRadius * 10
                };
                planet.moons.push(moon);
            }
        }
        
        systemArray.push(planet);
        
        // Increase orbit radius for next planet
        orbitRadius += planetRadius * 3.5 + 40 + Math.random() * 80;
    }
    
    // Add asteroid belt between systems with 30% chance
    if (Math.random() < 0.3) {
        addAsteroidBelt(systemArray, centerX, centerY, orbitRadius + 100);
    }
    
    console.log(`Generated ${pTypeData.name} system with ${numPlanets} planets at (${centerX}, ${centerY})`);
}

/**
 * Add asteroid belt to solar system
 */
function addAsteroidBelt(systemArray, centerX, centerY, distance) {
    const numAsteroids = 20 + Math.floor(Math.random() * 30);
    
    for (let i = 0; i < numAsteroids; i++) {
        const angle = (i / numAsteroids) * Math.PI * 2 + Math.random() * 0.5;
        const dist = distance + (Math.random() - 0.5) * 60;
        
        systemArray.push({
            type: "asteroid",
            x: centerX + Math.cos(angle) * dist,
            y: centerY + Math.sin(angle) * dist,
            radius: 2 + Math.random() * 4,
            color: BOB_ROSS_PALETTE["Van Dyke Brown"],
            mass: 50 + Math.random() * 100,
            angle: angle,
            orbitSpeed: 0.0003
        });
    }
}

// ============================================================================
// COLOR UTILITIES
// ============================================================================

/**
 * Adjust hue of a hex color by degrees
 * @param {string} hex - Hex color code (e.g., "#FF6347")
 * @param {number} deg - Degrees to shift (-360 to 360)
 * @returns {string} - Modified hex color
 */
function adjustHue(hex, deg) {
    // Parse hex
    let r = parseInt(hex.slice(1, 3), 16) / 255;
    let g = parseInt(hex.slice(3, 5), 16) / 255;
    let b = parseInt(hex.slice(5, 7), 16) / 255;
    
    // Convert to HSL
    let max = Math.max(r, g, b);
    let min = Math.min(r, g, b);
    let h = 0, s = 0, l = (max + min) / 2;
    
    if (max !== min) {
        let d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        
        switch (max) {
            case r: h = ((g - b) / d + (g < b ? 6 : 0)) / 6; break;
            case g: h = ((b - r) / d + 2) / 6; break;
            case b: h = ((r - g) / d + 4) / 6; break;
        }
    }
    
    // Shift hue
    h = (h + deg / 360) % 1;
    if (h < 0) h += 1;
    
    // Convert back to RGB (simplified)
    // Full HSL->RGB conversion
    let r2, g2, b2;
    
    if (s === 0) {
        r2 = g2 = b2 = l;
    } else {
        function hue2rgb(p, q, t) {
            if (t < 0) t += 1;
            if (t > 1) t -= 1;
            if (t < 1/6) return p + (q - p) * 6 * t;
            if (t < 1/2) return q;
            if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
            return p;
        }
        
        let q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        let p = 2 * l - q;
        
        r2 = hue2rgb(p, q, h + 1/3);
        g2 = hue2rgb(p, q, h);
        b2 = hue2rgb(p, q, h - 1/3);
    }
    
    // Convert to hex
    const toHex = (c) => {
        const hex = Math.round(c * 255).toString(16);
        return hex.length === 1 ? "0" + hex : hex;
    };
    
    return `#${toHex(r2)}${toHex(g2)}${toHex(b2)}`;
}

/**
 * Get random color with bias
 */
function getRandomColor(base = null) {
    if (base) {
        // Return color from palette based on base
        const palette = Object.values(BOB_ROSS_PALETTE);
        return palette[Math.floor(Math.random() * palette.length)];
    }
    
    // Random vibrant color
    const hue = Math.floor(Math.random() * 360);
    return `hsl(${hue}, 70%, 50%)`;
}

// ============================================================================
// RENDERING
// ============================================================================

/**
 * Draw a complete solar system with all celestial bodies
 * @param {Array} system - Array of celestial bodies
 * @param {object} canvas - DroidScript canvas object
 */
function drawSolarSystem(system, canvas) {
    if (!canvas) return;
    
    // Draw from back to front (asteroids → sun → planets → moons)
    system.forEach(body => {
        if (body.type === "asteroid") {
            drawAsteroid(body, canvas);
        }
    });
    
    system.forEach(body => {
        if (body.type === "sun") {
            drawSun(body, canvas);
        } else if (body.type === "planet") {
            drawPlanet(body, canvas);
        }
    });
}

/**
 * Draw sun with glow effect
 */
function drawSun(sun, canvas) {
    // Draw glow/halo
    canvas.SetAlpha(GAME_CONFIG.GLOW_ALPHA);
    canvas.SetPaintColor(sun.color);
    canvas.DrawCircle(sun.x / GAME_CONFIG.SW, sun.y / GAME_CONFIG.SH, 
        sun.glowRadius / GAME_CONFIG.SW);
    
    // Draw sun body
    canvas.SetAlpha(1);
    canvas.DrawCircle(sun.x / GAME_CONFIG.SW, sun.y / GAME_CONFIG.SH, 
        sun.radius / GAME_CONFIG.SW);
    
    // Highlight
    canvas.SetAlpha(0.5);
    canvas.SetPaintColor(BOB_ROSS_PALETTE["Titanium White"]);
    const highlightX = (sun.x - sun.radius * 0.3) / GAME_CONFIG.SW;
    const highlightY = (sun.y - sun.radius * 0.3) / GAME_CONFIG.SH;
    canvas.DrawCircle(highlightX, highlightY, sun.radius * 0.2 / GAME_CONFIG.SW);
}

/**
 * Draw planet with rings, moons, and shading
 */
function drawPlanet(planet, canvas) {
    // Draw shadow (3D effect)
    canvas.SetAlpha(0.3);
    canvas.SetPaintColor(BOB_ROSS_PALETTE["Midnight Black"]);
    const shadowX = (planet.x + 2) / GAME_CONFIG.SW;
    const shadowY = (planet.y + 2) / GAME_CONFIG.SH;
    canvas.DrawCircle(shadowX, shadowY, planet.radius / GAME_CONFIG.SW);
    
    // Draw planet body
    canvas.SetAlpha(1);
    canvas.SetPaintColor(planet.color);
    canvas.DrawCircle(planet.x / GAME_CONFIG.SW, planet.y / GAME_CONFIG.SH, 
        planet.radius / GAME_CONFIG.SW);
    
    // Draw highlight
    canvas.SetAlpha(0.4);
    canvas.SetPaintColor(BOB_ROSS_PALETTE["Titanium White"]);
    const hlX = (planet.x - planet.radius * 0.3) / GAME_CONFIG.SW;
    const hlY = (planet.y - planet.radius * 0.3) / GAME_CONFIG.SH;
    canvas.DrawCircle(hlX, hlY, planet.radius * 0.3 / GAME_CONFIG.SW);
    
    // Draw rings if present
    if (planet.hasRings) {
        canvas.SetAlpha(GAME_CONFIG.RING_ALPHA);
        canvas.SetPaintColor(planet.ringColor);
        
        // Inner ring
        canvas.DrawCircle(planet.x / GAME_CONFIG.SW, planet.y / GAME_CONFIG.SH,
            planet.ringInner / GAME_CONFIG.SW);
        
        // Outer ring (slightly thicker)
        canvas.DrawCircle(planet.x / GAME_CONFIG.SW, planet.y / GAME_CONFIG.SH,
            planet.ringOuter / GAME_CONFIG.SW);
        
        canvas.SetAlpha(1);
    }
    
    // Draw moons
    if (planet.moons && planet.moons.length > 0) {
        planet.moons.forEach(moon => {
            drawMoon(planet, moon, canvas);
        });
    }
}

/**
 * Draw moon orbiting planet
 */
function drawMoon(planet, moon, canvas) {
    // Calculate moon position
    const mx = planet.x + Math.cos(moon.angle) * moon.dist;
    const my = planet.y + Math.sin(moon.angle) * moon.dist;
    
    // Draw shadow
    canvas.SetAlpha(0.4);
    canvas.SetPaintColor(BOB_ROSS_PALETTE["Midnight Black"]);
    canvas.DrawCircle((mx + 1) / GAME_CONFIG.SW, (my + 1) / GAME_CONFIG.SH, 
        moon.radius / GAME_CONFIG.SW);
    
    // Draw moon body
    canvas.SetAlpha(1);
    canvas.SetPaintColor(moon.color);
    canvas.DrawCircle(mx / GAME_CONFIG.SW, my / GAME_CONFIG.SH, 
        moon.radius / GAME_CONFIG.SW);
    
    // Draw highlight
    canvas.SetAlpha(0.3);
    canvas.SetPaintColor(BOB_ROSS_PALETTE["Titanium White"]);
    canvas.DrawCircle((mx - moon.radius * 0.2) / GAME_CONFIG.SW, 
        (my - moon.radius * 0.2) / GAME_CONFIG.SH,
        moon.radius * 0.4 / GAME_CONFIG.SW);
    
    // Advance moon orbit
    moon.angle += moon.speed;
}

/**
 * Draw asteroid (simple dot)
 */
function drawAsteroid(asteroid, canvas) {
    canvas.SetPaintColor(asteroid.color);
    canvas.DrawCircle(asteroid.x / GAME_CONFIG.SW, asteroid.y / GAME_CONFIG.SH,
        asteroid.radius / GAME_CONFIG.SW);
}

/**
 * Draw orbit trail (optional visual aid)
 */
function drawOrbitTrail(centerX, centerY, radius, canvas) {
    canvas.SetAlpha(0.1);
    canvas.SetPaintColor(BOB_ROSS_PALETTE["Phthalo Blue"]);
    canvas.DrawCircle(centerX / GAME_CONFIG.SW, centerY / GAME_CONFIG.SH,
        radius / GAME_CONFIG.SW);
    canvas.SetAlpha(1);
}

// ============================================================================
// GRAVITY & PHYSICS
// ============================================================================

/**
 * Calculate gravitational force between two bodies
 * @param {object} body1 - First body (with mass, x, y)
 * @param {object} body2 - Second body
 * @returns {object} - Force vector {x, y}
 */
function calculateGravity(body1, body2) {
    const dx = body2.x - body1.x;
    const dy = body2.y - body1.y;
    const distSq = dx * dx + dy * dy;
    const dist = Math.sqrt(distSq);
    
    // F = G * m1 * m2 / r^2
    const force = GAME_CONFIG.GRAVITY_CONSTANT * body1.mass * body2.mass / distSq;
    
    return {
        x: (dx / dist) * force,
        y: (dy / dist) * force
    };
}

/**
 * Apply solar gravity to entity
 * @param {object} entity - Object with x, y, vx, vy
 * @param {Array} solarSystem - Solar system to check gravity against
 */
function applySolarGravity(entity, solarSystem) {
    solarSystem.forEach(body => {
        if (body.type === "sun" || body.type === "planet") {
            const dx = body.x - entity.x;
            const dy = body.y - entity.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            // Only apply gravity within well
            if (dist < body.gravityWell || dist < body.radius * 5) {
                const force = calculateGravity(entity, body);
                
                // Apply to velocity
                entity.vx = (entity.vx || 0) + force.x * 0.001;
                entity.vy = (entity.vy || 0) + force.y * 0.001;
            }
        }
    });
}

/**
 * Update entity position with velocity
 */
function updateEntityPosition(entity) {
    if (entity.vx && entity.vy) {
        entity.x += entity.vx;
        entity.y += entity.vy;
        
        // Apply friction
        entity.vx *= GAME_CONFIG.FRICTION;
        entity.vy *= GAME_CONFIG.FRICTION;
        
        // Cap velocity
        const speed = Math.sqrt(entity.vx * entity.vx + entity.vy * entity.vy);
        if (speed > GAME_CONFIG.MAX_VELOCITY) {
            entity.vx *= GAME_CONFIG.MAX_VELOCITY / speed;
            entity.vy *= GAME_CONFIG.MAX_VELOCITY / speed;
        }
    }
}

// ============================================================================
// GAME LOOP
// ============================================================================

/**
 * Main update function - call every frame
 */
function updateGame() {
    // Update game time
    gameState.time += 16; // ~60fps
    
    // Update OODA AI
    if (gameState.time % GAME_CONFIG.OODA_UPDATE_MS === 0) {
        runOODACycle();
    }
    
    // Update planets (orbits)
    updatePlanets(gameState.solarSystemLeft);
    updatePlanets(gameState.solarSystemRight);
    
    // Update entities
    updateEntities();
    
    // Check collisions
    checkCollisions();
    
    // Render
    drawScene();
}

/**
 * Update planet positions (orbital mechanics)
 */
function updatePlanets(system) {
    const centerX = system[0]?.x;
    const centerY = system[0]?.y;
    
    if (!centerX || !centerY) return;
    
    system.forEach(body => {
        if (body.type === "planet") {
            // Advance angle
            body.angle += body.orbitSpeed;
            
            // Recalculate position
            body.x = centerX + Math.cos(body.angle) * body.orbitRadius;
            body.y = centerY + Math.sin(body.angle) * body.orbitRadius;
        }
        
        if (body.type === "asteroid") {
            body.angle += body.orbitSpeed;
            body.x = centerX + Math.cos(body.angle) * 
                Math.sqrt((body.x - centerX) ** 2 + (body.y - centerY) ** 2);
        }
    });
}

/**
 * Update all game entities
 */
function updateEntities() {
    // Update player
    if (gameState.player) {
        applySolarGravity(gameState.player, gameState.solarSystemLeft);
        applySolarGravity(gameState.player, gameState.solarSystemRight);
        updateEntityPosition(gameState.player);
    }
    
    // Update enemies
    gameState.enemies.forEach(enemy => {
        applySolarGravity(enemy, gameState.solarSystemLeft);
        applySolarGravity(enemy, gameState.solarSystemRight);
        updateEntityPosition(enemy);
    });
    
    // Update projectiles
    gameState.projectiles.forEach(proj => {
        applySolarGravity(proj, gameState.solarSystemLeft);
        applySolarGravity(proj, gameState.solarSystemRight);
        proj.x += proj.vx;
        proj.y += proj.vy;
    });
}

/**
 * Draw complete scene
 */
function drawScene() {
    if (!canvas) return;
    
    // Clear background
    canvas.SetPaintColor(BOB_ROSS_PALETTE["Prussian Blue"]);
    canvas.DrawRectangle(0, 0, 1, 1);
    
    // Draw starfield
    drawStarfield(canvas);
    
    // Draw solar systems
    drawSolarSystem(gameState.solarSystemLeft, canvas);
    drawSolarSystem(gameState.solarSystemRight, canvas);
    
    // Draw player
    if (gameState.player) {
        drawPlayer(gameState.player, canvas);
    }
    
    // Draw enemies
    gameState.enemies.forEach(enemy => drawEnemy(enemy, canvas));
    
    // Draw projectiles
    gameState.projectiles.forEach(proj => drawProjectile(proj, canvas));
    
    // Draw debris
    gameState.debris.forEach(deb => drawDebris(deb, canvas));
    
    // Draw UI
    drawUI(canvas);
    
    // Update canvas
    canvas.Update();
}

/**
 * Draw background starfield
 */
function drawStarfield(canvas) {
    canvas.SetPaintColor(BOB_ROSS_PALETTE["Titanium White"]);
    
    for (let i = 0; i < GAME_CONFIG.STAR_COUNT; i++) {
        // Use deterministic pseudo-random based on index
        const x = ((i * 137.5) % 1920) / 1920;
        const y = ((i * 93.7) % 1080) / 1080;
        const size = (i % 5 === 0) ? 2 : 1;
        const brightness = 0.3 + (i % 7) * 0.1;
        
        canvas.SetAlpha(brightness);
        canvas.DrawCircle(x, y, size / GAME_CONFIG.SW);
    }
    canvas.SetAlpha(1);
}

/**
 * Draw player ship
 */
function drawPlayer(player, canvas) {
    // Simple ship representation (triangle)
    canvas.SetPaintColor(BOB_ROSS_PALETTE["Cadmium Yellow"]);
    
    const x = player.x / GAME_CONFIG.SW;
    const y = player.y / GAME_CONFIG.SH;
    const size = 15 / GAME_CONFIG.SW;
    
    // Draw ship as circle with direction indicator
    canvas.DrawCircle(x, y, size);
    
    // Direction line
    if (player.vx || player.vy) {
        const angle = Math.atan2(player.vy, player.vx);
        const dirX = x + Math.cos(angle) * size * 2;
        const dirY = y + Math.sin(angle) * size * 2;
        canvas.DrawLine(x, y, dirX, dirY);
    }
}

/**
 * Draw enemy (platonic solid approximation)
 */
function drawEnemy(enemy, canvas) {
    canvas.SetPaintColor(enemy.color || BOB_ROSS_PALETTE["Alizarin Crimson"]);
    
    const x = enemy.x / GAME_CONFIG.SW;
    const y = enemy.y / GAME_CONFIG.SH;
    const size = (enemy.size || 20) / GAME_CONFIG.SW;
    
    // Draw based on enemy type
    if (enemy.shape === "cube") {
        canvas.DrawRectangle(x - size, y - size, x + size, y + size);
    } else if (enemy.shape === "triangle") {
        // Simplified triangle
        canvas.DrawCircle(x, y, size);
    } else {
        canvas.DrawCircle(x, y, size);
    }
}

/**
 * Draw projectile
 */
function drawProjectile(proj, canvas) {
    canvas.SetPaintColor(proj.color || "#FFFFFF");
    canvas.DrawCircle(proj.x / GAME_CONFIG.SW, proj.y / GAME_CONFIG.SH,
        (proj.size || 3) / GAME_CONFIG.SW);
}

/**
 * Draw debris
 */
function drawDebris(deb, canvas) {
    canvas.SetPaintColor(deb.color || BOB_ROSS_PALETTE["Van Dyke Brown"]);
    canvas.SetAlpha(0.7);
    canvas.DrawCircle(deb.x / GAME_CONFIG.SW, deb.y / GAME_CONFIG.SH,
        (deb.size || 4) / GAME_CONFIG.SW);
    canvas.SetAlpha(1);
}

/**
 * Draw UI overlay
 */
function drawUI(canvas) {
    // Score
    canvas.SetTextSize(20);
    canvas.SetPaintColor(BOB_ROSS_PALETTE["Titanium White"]);
    canvas.DrawText(`Score: ${gameState.score}`, 0.02, 0.05, "left");
    
    // Lives
    canvas.DrawText(`Lives: ${gameState.lives}`, 0.02, 0.09, "left");
    
    // OODA Phase indicator
    canvas.DrawText(`AI: ${gameState.oodaPhase}`, 0.02, 0.13, "left");
    
    // Systems status
    const leftPlanets = gameState.solarSystemLeft.filter(b => b.type === "planet").length;
    const rightPlanets = gameState.solarSystemRight.filter(b => b.type === "planet").length;
    canvas.DrawText(`Systems: ${leftPlanets} | ${rightPlanets}`, 0.02, 0.17, "left");
}

// ============================================================================
// OODA NEURAL AI
// ============================================================================

/**
 * OODA Loop AI for enemy behavior
 * OBSERVE → ORIENT → DECIDE → ACT
 */
function runOODACycle() {
    gameState.oodaPhase = "OBSERVE";
    
    // Gather observations
    const observations = {
        playerPos: gameState.player ? { x: gameState.player.x, y: gameState.player.y } : null,
        enemyCount: gameState.enemies.length,
        projectileCount: gameState.projectiles.length,
        time: gameState.time,
        solarSystems: {
            left: gameState.solarSystemLeft.length,
            right: gameState.solarSystemRight.length
        }
    };
    
    gameState.oodaPhase = "ORIENT";
    
    // Analyze patterns
    const threatLevel = observations.projectileCount * 0.1 + 
        observations.enemyCount * 0.05;
    
    gameState.oodaPhase = "DECIDE";
    
    // Decision based on observations
    if (threatLevel > 0.5 && gameState.enemies.length < 10) {
        // Spawn more enemies
        spawnEnemy();
    }
    
    if (gameState.time % GAME_CONFIG.ENEMY_SPAWN_RATE === 0) {
        spawnEnemy();
    }
    
    gameState.oodaPhase = "ACT";
    
    // Execute AI decisions
    gameState.enemies.forEach(enemy => {
        if (observations.playerPos) {
            // Chase player
            const dx = observations.playerPos.x - enemy.x;
            const dy = observations.playerPos.y - enemy.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            if (dist > 0) {
                enemy.vx = (dx / dist) * 2;
                enemy.vy = (dy / dist) * 2;
            }
        }
    });
}

/**
 * Spawn enemy ship
 */
function spawnEnemy() {
    const shapes = ["cube", "triangle", "sphere"];
    const colors = [
        BOB_ROSS_PALETTE["Alizarin Crimson"],
        DUALITY_PALETTE["Rebel Red"],
        DUALITY_PALETTE["Stealth Black"]
    ];
    
    const enemy = {
        x: Math.random() * GAME_CONFIG.SW,
        y: Math.random() * GAME_CONFIG.SH,
        vx: 0,
        vy: 0,
        size: 15 + Math.random() * 15,
        shape: shapes[Math.floor(Math.random() * shapes.length)],
        color: colors[Math.floor(Math.random() * colors.length)],
        health: 1 + Math.floor(Math.random() * 3),
        mass: 100 + Math.random() * 100
    };
    
    gameState.enemies.push(enemy);
}

/**
 * Check collisions between entities
 */
function checkCollisions() {
    // Projectile - Enemy
    for (let p = gameState.projectiles.length - 1; p >= 0; p--) {
        const proj = gameState.projectiles[p];
        
        for (let e = gameState.enemies.length - 1; e >= 0; e--) {
            const enemy = gameState.enemies[e];
            const dist = Math.sqrt(
                (proj.x - enemy.x) ** 2 + 
                (proj.y - enemy.y) ** 2
            );
            
            if (dist < enemy.size + (proj.size || 3)) {
                // Hit!
                gameState.projectiles.splice(p, 1);
                enemy.health--;
                
                if (enemy.health <= 0) {
                    // Create debris
                    createDebris(enemy.x, enemy.y, enemy.color);
                    gameState.enemies.splice(e, 1);
                    gameState.score += 100;
                }
                break;
            }
        }
    }
    
    // Player - Enemy
    if (gameState.player) {
        gameState.enemies.forEach(enemy => {
            const dist = Math.sqrt(
                (gameState.player.x - enemy.x) ** 2 +
                (gameState.player.y - enemy.y) ** 2
            );
            
            if (dist < 30) {
                gameState.lives--;
                if (gameState.lives <= 0) {
                    gameState.phase = "GAMEOVER";
                }
            }
        });
    }
}

/**
 * Create debris explosion
 */
function createDebris(x, y, color) {
    for (let i = 0; i < 5; i++) {
        gameState.debris.push({
            x: x + (Math.random() - 0.5) * 20,
            y: y + (Math.random() - 0.5) * 20,
            vx: (Math.random() - 0.5) * 4,
            vy: (Math.random() - 0.5) * 4,
            size: 2 + Math.random() * 4,
            color: color,
            life: 60  // Frames to live
        });
    }
}

// ============================================================================
// INPUT HANDLING
// ============================================================================

/**
 * Handle touch input
 */
function onTouchStart(ev) {
    gameState.touch.active = true;
    gameState.touch.x = ev.x * GAME_CONFIG.SW;
    gameState.touch.y = ev.y * GAME_CONFIG.SH;
    
    if (gameState.player) {
        // Move player toward touch
        const dx = gameState.touch.x - gameState.player.x;
        const dy = gameState.touch.y - gameState.player.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        
        if (dist > 0) {
            gameState.player.vx += (dx / dist) * 3;
            gameState.player.vy += (dy / dist) * 3;
        }
    }
}

function onTouchMove(ev) {
    gameState.touch.x = ev.x * GAME_CONFIG.SW;
    gameState.touch.y = ev.y * GAME_CONFIG.SH;
}

function onTouchEnd(ev) {
    gameState.touch.active = false;
}

/**
 * Handle speech commands
 */
function onSpeechResult(results) {
    const command = results[0].toLowerCase();
    gameState.speech.lastCommand = command;
    
    // Parse commands
    if (command.includes("shoot") || command.includes("fire")) {
        fireProjectile();
    } else if (command.includes("stop")) {
        if (gameState.player) {
            gameState.player.vx *= 0.5;
            gameState.player.vy *= 0.5;
        }
    } else if (command.includes("warp") || command.includes("jump")) {
        // Emergency warp
        if (gameState.player) {
            gameState.player.x = Math.random() * GAME_CONFIG.SW;
            gameState.player.y = Math.random() * GAME_CONFIG.SH;
        }
    }
}

/**
 * Fire projectile from player
 */
function fireProjectile() {
    if (!gameState.player) return;
    
    const speed = 8;
    const angle = Math.atan2(gameState.player.vy || -1, gameState.player.vx || 0);
    
    gameState.projectiles.push({
        x: gameState.player.x,
        y: gameState.player.y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        size: 4,
        color: BOB_ROSS_PALETTE["Cadmium Yellow"],
        mass: 1
    });
}

// ============================================================================
// INITIALIZATION
// ============================================================================

/**
 * DroidScript OnStart
 */
function OnStart() {
    // Configure screen
    app.SetOrientation("Landscape");
    app.SetScreenMode("Full");
    
    // Update config with actual screen size
    GAME_CONFIG.SW = app.GetScreenWidth();
    GAME_CONFIG.SH = app.GetScreenHeight();
    
    // Create canvas
    const lay = app.CreateLayout("Linear", "VCenter,FillXY");
    canvas = app.CreateImage(null, GAME_CONFIG.SW, GAME_CONFIG.SH, "px");
    canvas.SetAutoUpdate(false);
    lay.AddChild(canvas);
    app.AddLayout(lay);
    
    // Set up input handlers
    canvas.SetOnTouchDown(onTouchStart);
    canvas.SetOnTouchMove(onTouchMove);
    canvas.SetOnTouchUp(onTouchEnd);
    
    // Speech recognition (if available)
    app.SetOnSpeechResult(onSpeechResult);
    
    // Create player
    gameState.player = {
        x: GAME_CONFIG.SW / 2,
        y: GAME_CONFIG.SH / 2,
        vx: 0,
        vy: 0,
        radius: 15,
        mass: 200,
        color: BOB_ROSS_PALETTE["Cadmium Yellow"]
    };
    
    // Generate solar systems
    generateSolarSystem(gameState.solarSystemLeft, GAME_CONFIG.SW * 0.25, GAME_CONFIG.SH * 0.5, true);
    generateSolarSystem(gameState.solarSystemRight, GAME_CONFIG.SW * 0.75, GAME_CONFIG.SH * 0.5, false);
    
    // Start game loop
    setInterval(updateGame, 16);  // ~60fps
    
    console.log("SGVD - Solar GraVitaional Duel");
    console.log("Enhanced Solar Systems Module v2.0");
    console.log("Features: Realistic planets, moons, rings, asteroid belts");
    console.log("Physics: Gravity wells, orbital mechanics, OODA AI");
}

/**
 * Restart game
 */
function restartGame() {
    gameState.score = 0;
    gameState.lives = 3;
    gameState.time = 0;
    gameState.enemies = [];
    gameState.projectiles = [];
    gameState.debris = [];
    gameState.phase = "PLAYING";
    
    // Regenerate solar systems
    generateSolarSystem(gameState.solarSystemLeft, GAME_CONFIG.SW * 0.25, GAME_CONFIG.SH * 0.5, true);
    generateSolarSystem(gameState.solarSystemRight, GAME_CONFIG.SW * 0.75, GAME_CONFIG.SH * 0.5, false);
    
    console.log("Game restarted!");
}

// Start the application
OnStart();
