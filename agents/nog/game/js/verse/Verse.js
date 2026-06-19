/**
 * VERSE.JS - NOG Universe System
 * Based on nog.cpp full MMO spec
 * 
 * Universe types:
 * 1. Infinite universe
 * 2. Bubble universes - 10^10^122 may intersect
 * 3. Daughter universes - AI plays out possible moves
 * 4. Mathematical universe - best mathematical choice
 * 5. Parallel universes - 10^10^122 distinct possibilities
 * 6. Under Verse - white field, inverted colors
 */

class Verse {
    constructor(seed = Date.now()) {
        this.seed = seed;
        this.rng = new SeededRandom(seed);
        
        // Universe type
        this.type = this.rng.int(0, 6);
        this.typeNames = ['Infinite', 'Bubble', 'Daughter', 'Mathematical', 'Parallel', 'Under Verse'];
        
        // Grid: 100x100x3 = 1,000,000 stars
        this.gridSize = { x: 100, y: 100, z: 3 };
        
        // Current position in verse
        this.currentGalaxy = 0;
        this.currentSystem = null;
        
        // Black holes (portals)
        this.blackHoles = [];
        
        // Energy resources
        this.resources = {
            SOLAR: 0,
            GAS: 1,
            WIND: 2,
            FUSION: 3,
            FOSSIL: 4,
            CRYSTAL: 5,
            ANTIMATTER: 6,
            NAQUEDA: 7,
            NAQUADRIA: 8
        };
        
        this.generateBlackHoles();
    }
    
    generateBlackHoles() {
        // 3-5 black holes per verse
        const count = this.rng.int(3, 6);
        for (let i = 0; i < count; i++) {
            this.blackHoles.push({
                id: i,
                size: this.rng.int(1, 4), // 1=small, 2=medium, 3=large
                x: this.rng.range(0, this.gridSize.x),
                y: this.rng.range(0, this.gridSize.y),
                z: this.rng.int(0, this.gridSize.z),
                destinationVerse: null, // Generated on travel
                sizeNames: ['', 'Small', 'Medium', 'Large']
            });
        }
    }
    
    getStarAt(x, y, z) {
        // Deterministic star generation based on position
        const starRng = new SeededRandom(x * 1000000 + y * 1000 + z);
        return this.generateStar(starRng, x, y, z);
    }
    
    generateStar(rng, x, y, z) {
        const type = rng.int(0, 10);
        
        // Star configurations from nog.cpp
        const configs = [
            { name: 'Black Hole', color: '#000', sunSize: 0, planets: 0, gasGiants: 0, moons: 0, asteroids: 0 },
            { name: 'Yellow Sun', color: '#FFD700', sunSize: 1, planets: 5, gasGiants: 2, moons: 3, asteroids: 6 },
            { name: 'White Star', color: '#FFFFFF', sunSize: 1, planets: 1, gasGiants: 1, moons: 0, asteroids: 5 },
            { name: 'Blue Star', color: '#4169E1', sunSize: 1, planets: 2, gasGiants: 3, moons: 3, asteroids: 4 },
            { name: 'Red Star', color: '#DC143C', sunSize: 1, planets: 3, gasGiants: 4, moons: 4, asteroids: 4 },
            { name: 'Green Sun', color: '#32CD32', sunSize: 1, planets: 4, gasGiants: 0, moons: 5, asteroids: 0 },
            { name: 'Binary WT+RD', color: '#FFA500', sunSize: 2, planets: 4, gasGiants: 5, moons: 4, asteroids: 9 },
            { name: 'Binary YL+BL', color: '#FFFF00', sunSize: 2, planets: 7, gasGiants: 5, moons: 6, asteroids: 10 },
            { name: 'Trinary', color: '#FF69B4', sunSize: 3, planets: 9, gasGiants: 7, moons: 12, asteroids: 8 },
            { name: 'Brown Dwarf', color: '#8B4513', sunSize: 1, planets: 5, gasGiants: 2, moons: 3, asteroids: 6 }
        ];
        
        const config = configs[type];
        const gravity = config.sunSize; // 1, 2, or 3
        
        // Generate planets
        const planets = [];
        for (let i = 0; i < config.planets; i++) {
            planets.push(this.generatePlanet(rng, i, config));
        }
        
        // Generate gas giants
        const gasGiants = [];
        for (let i = 0; i < config.gasGiants; i++) {
            gasGiants.push(this.generateGasGiant(rng, i));
        }
        
        // Generate asteroids
        const asteroids = [];
        for (let i = 0; i < config.asteroids; i++) {
            asteroids.push(this.generateAsteroid(rng));
        }
        
        return {
            x, y, z,
            type: type,
            name: config.name,
            color: config.color,
            gravity: gravity,
            sunSize: config.sunSize,
            planets: planets,
            gasGiants: gasGiants,
            asteroids: asteroids,
            moons: config.moons
        };
    }
    
    generatePlanet(rng, index, starConfig) {
        // Planet types from nog.cpp (0-10)
        const planetTypes = [
            { type: 'Asteroid', skybox: 'space', life: false, minable: true },
            { type: 'Rocky', skybox: 'dusty_red', life: false, resources: ['solar', 'gas', 'wind', 'fossil', 'naquadria'] },
            { type: 'Radioactive', skybox: 'grey_silver', life: false, resources: ['solar', 'gas', 'wind', 'fusion', 'crystal', 'antimatter', 'naqueda', 'naquadria'] },
            { type: 'Metallic', skybox: 'grey_silver_metallic', life: false, resources: ['solar', 'gas', 'wind', 'fusion', 'fossil', 'crystal', 'naqueda', 'naquadria'] },
            { type: 'Crystalline', skybox: 'blue_green', life: false, resources: ['solar', 'gas', 'wind', 'fossil', 'crystal', 'naqueda', 'naquadria'] },
            { type: 'Glacial', skybox: 'blue_white', life: false, resources: ['solar', 'gas', 'wind', 'fossil', 'crystal', 'naqueda', 'naquadria'] },
            { type: 'Rogue', skybox: 'black_space', life: false, resources: ['wind', 'fossil', 'crystal', 'antimatter'] },
            { type: 'Rogue Asteroid Moon', skybox: 'space', life: false, resources: ['gas', 'fossil', 'crystal', 'antimatter', 'naqueda', 'naquadria'] },
            { type: 'Volcanic', skybox: 'red_black', life: true, creatures: 'insects_reptiles', resources: ['solar', 'gas', 'wind', 'fossil', 'crystal', 'naqueda', 'naquadria'] },
            { type: 'Gaia', skybox: 'blue_white_green', life: true, creatures: 'mammals_birds_aquatic', resources: ['solar', 'gas', 'wind', 'fossil', 'crystal', 'naqueda', 'naquadria'] },
            { type: 'Craters Moon', skybox: 'black_volcanic', life: false, resources: ['solar', 'gas', 'antimatter'] }
        ];
        
        // Planet position based on index (Goldilocks zone logic)
        const habitableInner = Math.sqrt(1 / 1.1);
        const habitableOuter = Math.sqrt(1 / 0.53);
        const distFactor = (index + 1) * 0.3;
        const inHabitableZone = distFactor >= habitableInner && distFactor <= habitableOuter;
        
        // Override to ensure variety
        const planetType = planetTypes[index % planetTypes.length];
        
        // Generate creatures for life-bearing planets
        let creatures = [];
        if (planetType.life) {
            creatures = this.generateCreatures(rng, planetType.creatures);
        }
        
        return {
            index: index,
            type: planetType.type,
            skybox: planetType.skybox,
            distance: distFactor,
            inHabitableZone: inHabitableZone,
            life: planetType.life,
            creatures: creatures,
            resources: planetType.resources || [],
            moons: rng.int(0, planetType.type === 'Gaia' ? 4 : 2),
            colonized: false,
            governor: null
        };
    }
    
    generateGasGiant(rng, index) {
        const colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3'];
        return {
            index: index,
            type: 'Gas Giant',
            color: colors[index % colors.length],
            size: rng.range(2, 5),
            moons: rng.int(1, 5),
            atmosphere: true,
            resources: ['hydrogen', 'helium'],
            landable: false // Cannot land on gas giants
        };
    }
    
    generateAsteroid(rng) {
        const types = ['C-type (chondrite)', 'S-type (stony)', 'M-type (metallic)'];
        return {
            type: types[rng.int(0, 3)],
            size: rng.range(0.1, 2),
            resources: ['iron', 'nickel', 'titanium', 'platinum'],
            minable: true,
            canBeColonized: true,
            canBeShip: true // Can be converted to vessel
        };
    }
    
    generateCreatures(rng, ecosystem) {
        const ecosystems = {
            insects_reptiles: [
                { name: 'Spider', types: 8, hostile: true },
                { name: 'Fly', types: 4, hostile: false },
                { name: 'Butterfly', types: 6, hostile: false },
                { name: 'Bee', types: 4, hostile: true },
                { name: 'Ant', types: 5, hostile: true },
                { name: 'Lizard', types: 4, hostile: false },
                { name: 'Frog', types: 3, hostile: false }
            ],
            mammals_birds_aquatic: [
                { name: 'Mammoth', types: 2, hostile: false },
                { name: 'Bull', types: 3, hostile: true },
                { name: 'Horse', types: 2, hostile: false },
                { name: 'Wolf', types: 2, hostile: true },
                { name: 'Dolphin', types: 2, hostile: false },
                { name: 'Whale', types: 2, hostile: false },
                { name: 'Bird', types: 4, hostile: false }
            ]
        };
        
        const creatures = [];
        const ecos = ecosystems[ecosystem] || [];
        const count = rng.int(3, 7);
        
        for (let i = 0; i < count; i++) {
            const base = ecos[i % ecos.length];
            creatures.push({
                ...base,
                size: rng.range(0.5, 3),
                domesticated: false
            });
        }
        
        return creatures;
    }
    
    // Travel through black hole
    travelThroughBlackHole(blackHole) {
        const destVerse = new Verse(Math.random() * 1000000);
        
        // Black hole size determines destination type
        const destinations = {
            1: ['Bubble', 'Daughter'], // Small
            2: ['Daughter', 'Parallel'], // Medium
            3: ['Under Verse', 'Mathematical'] // Large
        };
        
        const possibleDests = destinations[blackHole.size] || ['Infinite'];
        const destType = possibleDests[Math.floor(Math.random() * possibleDests.length)];
        
        return {
            destinationVerse: destVerse,
            destinationType: destType,
            portalEffect: this.createWarpEffect()
        };
    }
    
    createWarpEffect() {
        return {
            duration: 2000,
            frames: 30,
            colors: ['#000', '#fff', '#f0f', '#0ff']
        };
    }
    
    // Check if position has black hole
    getBlackHoleAt(x, y, z) {
        return this.blackHoles.find(bh => 
            Math.abs(bh.x - x) < 5 && 
            Math.abs(bh.y - y) < 5 && 
            bh.z === z
        );
    }
    
    serialize() {
        return {
            seed: this.seed,
            type: this.type,
            typeName: this.typeNames[this.type],
            gridSize: this.gridSize,
            blackHoles: this.blackHoles,
            resources: this.resources
        };
    }
}

// NOG Beings (15 alien races + humans)
class NOGBeings {
    static RACES = {
        HUMAN: {
            name: 'Human',
            count: 15,
            nations: ['Korea', 'Japan', 'China', 'USA', 'Cuba', 'Britain', 'France', 'Russia', 'Israel', 'Egypt', 'Congo', 'Brasil', 'Ivory Coast', 'Italy', 'India']
        },
        SQUID: { name: 'Squid', telepathic: true, intelligence: 'high' },
        PRAWN: { name: 'Prawn', armor: 4, humanoid: true },
        CAT: { name: 'Cat', transform: true, hunter: true },
        GREIS: { name: 'Greis', saucerRay: true },
        WAULCA: { name: 'Waulca', intellectual: true, powerful: true },
        WRADE: { name: 'Wrade', feedsOn: 'humanoids' },
        GBE: { name: 'Gbe', parasite: true, knowledge: 'inherent' },
        JAFFAN: { name: 'Jaffan', production: 'high' },
        HIVE: { name: 'Hive', pregnant: true, colonizer: true },
        ORKARI: { name: 'Orkari', interGalactic: true, motherShip: true },
        ROSAI: { name: 'Rosai', stealth: 'high', aggressive: true },
        SABATIAN: { name: 'Sabatian', strength: 3, lookAlike: true },
        REAPER: { name: 'Reaper', spirit: true, omnipresent: true },
        CROG: { name: 'Crog', catches: 'NOG', type: 'scaley_green_golam' },
        NOG: { name: 'NOG', protagonist: true }
    };
    
    static CLASSES = [
        { id: 1, name: 'Engineer', builds: true },
        { id: 2, name: 'Miner', mines: true },
        { id: 3, name: 'Sniper', range: 'long' },
        { id: 4, name: 'Pirate', loot: true },
        { id: 5, name: 'Trader', commerce: true },
        { id: 6, name: 'Capitalist', credits: true },
        { id: 7, name: 'Terminator', combat: 'heavy' },
        { id: 8, name: 'Agent', resources: 'government', ammo: 'unlimited' },
        { id: 9, name: 'Space Marine', versatile: true },
        { id: 10, name: 'Combat Engineer', builds: true, combat: true },
        { id: 11, name: 'Space Engineer', spaceBuilds: true },
        { id: 12, name: 'Criminal', stealth: true },
        { id: 13, name: 'Medic', heals: true },
        { id: 14, name: 'Cyborg', speed: 'fast', production: 'quick' }
    ];
    
    static WEAPONS = {
        tier0: ['Sword', 'Spear', 'Shield'],
        tier1: ['Pistol', 'Luger', 'Machine Gun'],
        tier2: ['PK90', 'PS150', 'XB00'],
        tier3: ['AK47M', 'Pulse Rifle'],
        tier4: ['Pulse Rifle+', 'Rapid Pulse'],
        tier5: ['Grenade', 'Pulse Grenade'],
        tier6: ['Radio', 'Encrypted Beacon'],
        tier7: ['Credits', 'Loan System'],
        tier8: ['Ramona', 'Mech'],
        tier9: ['Med Kit', 'Medic Bundle']
    };
    
    static VEHICLES = {
        ground: ['Motorcycle', 'Truck', 'Tank', 'APC', 'Harvester', 'Engineer Vehicle'],
        air: ['VTOL', 'Fighter', 'Transport'],
        space: ['Corvette', 'Frigate', 'Destroyer', 'Carrier', 'Super Carrier', 'Mothership', 'Dreadnought', 'Leviathan', 'Star Destroyer']
    };
}

// Seeded random for deterministic generation
class SeededRandom {
    constructor(seed) {
        this.seed = seed % 2147483647;
        if (this.seed <= 0) this.seed += 2147483646;
    }
    
    next() {
        this.seed = (this.seed * 16807) % 2147483647;
        return (this.seed - 1) / 2147483646;
    }
    
    int(min, max) {
        return Math.floor(this.next() * (max - min)) + min;
    }
    
    range(min, max) {
        return this.next() * (max - min) + min;
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Verse, NOGBeings, SeededRandom };
}
