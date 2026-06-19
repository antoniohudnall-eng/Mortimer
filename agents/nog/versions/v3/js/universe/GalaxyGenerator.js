/**
 * GalaxyGenerator.js - Procedural Galaxy Generation
 * Implements spiral, elliptical, irregular, and barred spiral galaxies
 * using logarithmic spiral mathematics
 */

class GalaxyGenerator {
    constructor(seed = Math.random() * 100000) {
        this.rng = new SeededRandom(seed);
        this.galaxies = [];
        
        // Galaxy type definitions
        this.types = {
            SPIRAL: {
                name: 'Spiral',
                arms: [2, 4, 6],
                tightness: [0.15, 0.35],
                coreRatio: 0.15,
                color: 0x88aaff,
                starColors: [0xaaccff, 0x88aaff, 0xffddaa, 0xffaaaa]
            },
            BARRED_SPIRAL: {
                name: 'Barred Spiral',
                arms: [2, 4],
                tightness: [0.2, 0.4],
                coreRatio: 0.25,
                hasBar: true,
                color: 0xaaffaa,
                starColors: [0xaaffaa, 0x88ff88, 0xffffaa, 0xffccaa]
            },
            ELLIPTICAL: {
                name: 'Elliptical',
                arms: [0],
                tightness: [0],
                coreRatio: 0.8,
                color: 0xffddaa,
                starColors: [0xffeecc, 0xffddaa, 0xffcc88, 0xffbb66]
            },
            IRREGULAR: {
                name: 'Irregular',
                arms: [0],
                tightness: [0],
                coreRatio: 0.1,
                color: 0xffaaff,
                starColors: [0xffaaff, 0xaaffff, 0xffffaa, 0xffaaaa]
            },
            RING: {
                name: 'Ring',
                arms: [1],
                tightness: [0],
                coreRatio: 0.05,
                hasRing: true,
                color: 0xaaffff,
                starColors: [0xaaffff, 0x88ccff, 0xffaaff, 0xffffff]
            }
        };
    }
    
    generateGalaxy(type = null, starCount = 5000) {
        // Select type if not specified
        if (!type) {
            const types = Object.keys(this.types);
            type = this.types[this.rng.choice(types)];
        }
        
        const galaxy = {
            type: type.name,
            starCount: starCount,
            stars: [],
            nebulae: [],
            blackHoles: [],
            position: {
                x: this.rng.range(-1e12, 1e12),
                y: this.rng.range(-1e11, 1e11),
                z: this.rng.range(-1e12, 1e12)
            },
            radius: this.rng.range(5e4, 2e5),
            rotation: this.rng.range(0.001, 0.01),
            age: this.rng.range(1, 13.8) // Billion years
        };
        
        // Generate stars based on type
        if (type.name === 'Spiral' || type.name === 'Barred Spiral') {
            this.generateSpiralGalaxy(galaxy, type);
        } else if (type.name === 'Elliptical') {
            this.generateEllipticalGalaxy(galaxy, type);
        } else if (type.name === 'Irregular') {
            this.generateIrregularGalaxy(galaxy, type);
        } else if (type.name === 'Ring') {
            this.generateRingGalaxy(galaxy, type);
        }
        
        // Generate nebulae
        this.generateNebulae(galaxy);
        
        // Generate central black hole
        galaxy.blackHoles.push({
            mass: this.rng.range(1e6, 1e9), // Solar masses
            position: { x: 0, y: 0, z: 0 },
            accretionDisk: true,
            jetPower: this.rng.range(0, 1)
        });
        
        this.galaxies.push(galaxy);
        return galaxy;
    }
    
    generateSpiralGalaxy(galaxy, type) {
        const numArms = this.rng.choice(type.arms);
        const b = this.rng.range(type.tightness[0], type.tightness[1]);
        const a = galaxy.radius * 0.1; // Core size
        const maxRadius = galaxy.radius;
        const coreStars = Math.floor(galaxy.starCount * type.coreRatio);
        const armStars = galaxy.starCount - coreStars;
        
        // Generate arm stars using logarithmic spiral
        // r = a * e^(b * θ)
        for (let i = 0; i < armStars; i++) {
            const armIndex = i % numArms;
            const armOffset = (armIndex / numArms) * Math.PI * 2;
            
            // Variable angle along spiral
            const theta = this.rng.range(0, Math.PI * 4) + armOffset;
            
            // Spiral radius with noise
            const r = a * Math.exp(b * theta) + this.rng.gauss(0, galaxy.radius * 0.05);
            const clampedR = Math.min(r, maxRadius);
            
            // Arm width variation
            const armWidth = 0.15 + (r / maxRadius) * 0.3;
            const armOffsetNoise = this.rng.gauss(0, armWidth);
            
            // Polar to Cartesian
            const angle = theta + armOffset + armOffsetNoise;
            const x = clampedR * Math.cos(angle);
            const y = clampedR * Math.sin(angle);
            
            // Galactic thickness (thinner at edges)
            const thickness = maxRadius * 0.1 * (1 - r / maxRadius);
            const z = this.rng.gauss(0, thickness);
            
            galaxy.stars.push(this.createStar(x, y, z, type));
        }
        
        // Generate core/bulge stars
        for (let i = 0; i < coreStars; i++) {
            const r = this.rng.range(0, a * 2);
            const theta = this.rng.range(0, Math.PI * 2);
            const x = r * Math.cos(theta);
            const y = r * Math.sin(theta);
            const z = this.rng.gauss(0, a * 0.3);
            
            const star = this.createStar(x, y, z, type);
            star.inCore = true;
            star.brightness *= 1.5; // Core stars are brighter
            galaxy.stars.push(star);
        }
        
        // Generate bar for barred spiral
        if (type.hasBar) {
            const barLength = galaxy.radius * 0.3;
            const barWidth = galaxy.radius * 0.05;
            const barStars = Math.floor(galaxy.starCount * 0.15);
            
            for (let i = 0; i < barStars; i++) {
                const x = this.rng.range(-barLength, barLength);
                const y = this.rng.gauss(0, barWidth);
                const z = this.rng.gauss(0, barWidth * 0.5);
                
                const star = this.createStar(x, y, z, type);
                star.inBar = true;
                galaxy.stars.push(star);
            }
        }
    }
    
    generateEllipticalGalaxy(galaxy, type) {
        const numStars = galaxy.starCount;
        const maxRadius = galaxy.radius;
        
        // Elliptical galaxies have stars distributed in ellipsoidal volume
        // with density decreasing from center
        for (let i = 0; i < numStars; i++) {
            // Use rejection sampling for more realistic distribution
            let x, y, z, r;
            do {
                x = this.rng.range(-1, 1);
                y = this.rng.range(-1, 1);
                z = this.rng.range(-0.3, 0.3); // Flatter in z
                r = Math.sqrt(x*x + y*y + z*z*10);
            } while (this.rng.next() > (1 - r)); // Higher density in center
            
            const scale = maxRadius * (1 - r * 0.5);
            
            galaxy.stars.push(this.createStar(
                x * scale,
                y * scale,
                z * scale,
                type
            ));
        }
    }
    
    generateIrregularGalaxy(galaxy, type) {
        const numStars = galaxy.starCount;
        const maxRadius = galaxy.radius;
        
        // Irregular galaxies have clumpy, chaotic distributions
        // Generate multiple star-forming regions
        const numClusters = this.rng.int(5, 15);
        const clusters = [];
        
        for (let i = 0; i < numClusters; i++) {
            clusters.push({
                x: this.rng.range(-maxRadius, maxRadius),
                y: this.rng.range(-maxRadius, maxRadius),
                z: this.rng.range(-maxRadius * 0.2, maxRadius * 0.2),
                radius: this.rng.range(maxRadius * 0.05, maxRadius * 0.3),
                density: this.rng.range(0.5, 2.0)
            });
        }
        
        // Distribute stars
        for (let i = 0; i < numStars; i++) {
            // Pick a cluster (or field)
            const cluster = this.rng.next() < 0.7 
                ? this.rng.choice(clusters)
                : { x: 0, y: 0, z: 0, radius: maxRadius, density: 0.3 };
            
            const r = this.rng.range(0, cluster.radius);
            const theta = this.rng.range(0, Math.PI * 2);
            const phi = this.rng.range(-Math.PI, Math.PI);
            
            const x = cluster.x + r * Math.cos(theta) * Math.cos(phi);
            const y = cluster.y + r * Math.sin(theta) * Math.cos(phi);
            const z = cluster.z + r * Math.sin(phi);
            
            const star = this.createStar(x, y, z, type);
            star.clusterId = clusters.indexOf(cluster);
            galaxy.stars.push(star);
        }
    }
    
    generateRingGalaxy(galaxy, type) {
        const numStars = galaxy.starCount;
        const ringRadius = galaxy.radius * 0.6;
        const ringWidth = galaxy.radius * 0.15;
        const coreStars = Math.floor(numStars * type.coreRatio);
        const ringStars = numStars - coreStars;
        
        // Core
        for (let i = 0; i < coreStars; i++) {
            const r = this.rng.range(0, galaxy.radius * 0.1);
            const theta = this.rng.range(0, Math.PI * 2);
            const x = r * Math.cos(theta);
            const y = r * Math.sin(theta);
            const z = this.rng.gauss(0, galaxy.radius * 0.02);
            
            galaxy.stars.push(this.createStar(x, y, z, type));
        }
        
        // Ring
        for (let i = 0; i < ringStars; i++) {
            const r = ringRadius + this.rng.gauss(0, ringWidth);
            const theta = this.rng.range(0, Math.PI * 2);
            const x = r * Math.cos(theta);
            const y = r * Math.sin(theta);
            const z = this.rng.gauss(0, galaxy.radius * 0.03);
            
            const star = this.createStar(x, y, z, type);
            star.inRing = true;
            galaxy.stars.push(star);
        }
    }
    
    generateNebulae(galaxy) {
        const numNebulae = this.rng.int(3, 10);
        
        for (let i = 0; i < numNebulae; i++) {
            galaxy.nebulae.push({
                x: this.rng.range(-galaxy.radius, galaxy.radius),
                y: this.rng.range(-galaxy.radius, galaxy.radius),
                z: this.rng.range(-galaxy.radius * 0.1, galaxy.radius * 0.1),
                radius: this.rng.range(galaxy.radius * 0.05, galaxy.radius * 0.3),
                color: this.rng.choice([
                    { r: 1, g: 0.3, b: 0.3 },   // Red
                    { r: 0.3, g: 0.3, b: 1 },   // Blue
                    { r: 0.3, g: 1, b: 0.3 },   // Green
                    { r: 1, g: 0.8, b: 0.3 }    // Gold
                ]),
                density: this.rng.range(0.1, 0.8),
                type: this.rng.choice(['emission', 'reflection', 'dark'])
            });
        }
    }
    
    createStar(x, y, z, type) {
        // Determine spectral class based on galaxy type and position
        const distanceFromCenter = Math.sqrt(x*x + y*y);
        const normalizedDist = Math.min(distanceFromCenter / (this.rng.lastMax || 1), 1);
        
        // Younger stars in arms, older in core
        const ageBias = normalizedDist * 0.5;
        const spectralClass = this.rng.next() < (0.3 + ageBias) ? 'O' :
                              this.rng.next() < (0.4 + ageBias) ? 'B' :
                              this.rng.next() < (0.5 + ageBias) ? 'A' :
                              this.rng.next() < (0.6 + ageBias) ? 'F' :
                              this.rng.next() < (0.8 + ageBias) ? 'G' :
                              this.rng.next() < (0.95 + ageBias) ? 'K' : 'M';
        
        const spectralColors = {
            'O': { r: 0.7, g: 0.8, b: 1.0 },
            'B': { r: 0.8, g: 0.9, b: 1.0 },
            'A': { r: 0.9, g: 0.95, b: 1.0 },
            'F': { r: 1.0, g: 1.0, b: 0.95 },
            'G': { r: 1.0, g: 0.95, b: 0.8 },
            'K': { r: 1.0, g: 0.8, b: 0.6 },
            'M': { r: 1.0, g: 0.5, b: 0.4 }
        };
        
        const size = this.rng.range(0.5, 3) * (spectralClass < 'F' ? 2 : 1);
        
        return {
            x, y, z,
            color: spectralColors[spectralClass],
            size: size,
            brightness: this.rng.range(0.3, 1.0),
            spectralClass: spectralClass,
            temperature: this.getTemperature(spectralClass),
            mass: this.rng.range(0.1, 100),
            age: this.rng.range(0.1, galaxy.age || 10)
        };
    }
    
    getTemperature(spectralClass) {
        const temps = { 'O': 40000, 'B': 20000, 'A': 8500, 'F': 6500, 
                       'G': 5700, 'K': 4500, 'M': 3000 };
        return temps[spectralClass] || 5000;
    }
    
    generateUniverse(numGalaxies = 50) {
        const universe = {
            galaxies: [],
            seed: this.rng.seed,
            age: 13.8,
            darkEnergy: 0.68,
            darkMatter: 0.27,
            baryonicMatter: 0.05
        };
        
        for (let i = 0; i < numGalaxies; i++) {
            universe.galaxies.push(this.generateGalaxy());
        }
        
        return universe;
    }
}

// Seeded Random
class SeededRandom {
    constructor(seed) {
        this.seed = seed;
        this.lastMax = 1;
    }
    
    next() {
        this.seed = (this.seed * 9301 + 49297) % 233280;
        return this.seed / 233280;
    }
    
    range(min, max) {
        this.lastMax = max;
        return min + this.next() * (max - min);
    }
    
    int(min, max) {
        return Math.floor(this.range(min, max));
    }
    
    choice(array) {
        return array[this.int(0, array.length)];
    }
    
    gauss(mean = 0, stdDev = 1) {
        // Box-Muller transform
        const u1 = this.next();
        const u2 = this.next();
        const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
        return mean + z * stdDev;
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { GalaxyGenerator, SeededRandom };
}
