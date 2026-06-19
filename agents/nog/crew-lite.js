#!/usr/bin/env node

/**
 * N'og nog Crew System - Lite Edition v1.0
 * Lightweight crew automation without heavy dependencies
 */

const fs = require('fs').promises;
const path = require('path');
const net = require('net');

// Configuration
const CONFIG = {
    storagePath: '/root/.openclaw/workspace/nognog/crew/storage/crew',
    expeditionsPath: '/root/.openclaw/workspace/expeditions',
    tickInterval: 30000,      // 30 seconds
    reportInterval: 3600000,  // 1 hour
    brainSocket: '/tmp/aos_brain.sock',
    maxCrew: 10,
    initialCrew: 5
};

// Crew roles
const ROLES = ['PILOT', 'ENGINEER', 'SCIENTIST', 'COMBAT', 'MEDIC', 'TRADER'];
const NAMES = ['Zara', 'Kael', 'Nyx', 'Orion', 'Luna', 'Rex', 'Vex', 'Nova', 'Jax', 'Aria'];
const LEVELS = ['Rookie', 'Cadet', 'Officer', 'Veteran', 'Elite', 'Legend'];

class LiteCrewSystem {
    constructor() {
        this.crew = new Map();
        this.running = false;
        this.tickTimer = null;
        this.reportTimer = null;
    }

    async init() {
        console.log('🚀 N\'og nog Crew System - Lite Edition');
        console.log('─────────────────────────────────────────');
        
        await this.ensureDirs();
        await this.loadCrew();
        
        if (this.crew.size === 0) {
            await this.generateInitialCrew();
        }
        
        console.log(`✅ Initialized with ${this.crew.size} crew members`);
        console.log('');
    }

    async ensureDirs() {
        for (const dir of [CONFIG.storagePath, CONFIG.expeditionsPath]) {
            try {
                await fs.mkdir(dir, { recursive: true });
            } catch (err) {}
        }
    }

    generateCrewMember(role = null) {
        const assignedRole = role || ROLES[Math.floor(Math.random() * ROLES.length)];
        
        return {
            id: `crew_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`,
            name: NAMES[Math.floor(Math.random() * NAMES.length)],
            role: assignedRole,
            level: 0,
            xp: 0,
            stats: {
                health: 100,
                maxHealth: 100,
                energy: 100,
                morale: 100,
                loyalty: 80 + Math.floor(Math.random() * 20)
            },
            skills: {
                navigation: Math.floor(Math.random() * 20) + 10,
                repair: Math.floor(Math.random() * 20) + 10,
                scanning: Math.floor(Math.random() * 20) + 10,
                combat: Math.floor(Math.random() * 20) + 10
            },
            missionsCompleted: 0,
            discoveries: [],
            status: 'ACTIVE',
            location: { universe: 'PRIME', system: 'Alpha-1' },
            created: Date.now(),
            lastActive: Date.now()
        };
    }

    async generateInitialCrew() {
        console.log('🎲 Generating initial crew...');
        
        const initialRoles = ['PILOT', 'ENGINEER', 'SCIENTIST', 'COMBAT', 'MEDIC'];
        for (const role of initialRoles) {
            const member = this.generateCrewMember(role);
            this.crew.set(member.id, member);
            await this.saveCrewMember(member);
            console.log(`   👤 ${member.name} (${role})`);
        }
    }

    async saveCrewMember(member) {
        const filePath = path.join(CONFIG.storagePath, `${member.id}.json`);
        try {
            await fs.writeFile(filePath, JSON.stringify(member, null, 2));
        } catch (err) {
            console.error(`Failed to save ${member.name}:`, err.message);
        }
    }

    async loadCrew() {
        try {
            const files = await fs.readdir(CONFIG.storagePath);
            for (const file of files) {
                if (file.endsWith('.json')) {
                    const data = await fs.readFile(path.join(CONFIG.storagePath, file), 'utf8');
                    const member = JSON.parse(data);
                    this.crew.set(member.id, member);
                }
            }
        } catch (err) {
            // No existing crew
        }
    }

    async saveAll() {
        for (const member of this.crew.values()) {
            await this.saveCrewMember(member);
        }
    }

    async start() {
        this.running = true;
        console.log('▶️  Crew automation started');
        console.log(`   Tick: ${CONFIG.tickInterval}ms | Report: ${CONFIG.reportInterval/60000}min`);
        console.log('');

        // Initial report
        await this.sendReport();

        // Start loops
        this.tickTimer = setInterval(() => this.tick(), CONFIG.tickInterval);
        this.reportTimer = setInterval(() => this.sendReport(), CONFIG.reportInterval);
    }

    async stop() {
        this.running = false;
        if (this.tickTimer) clearInterval(this.tickTimer);
        if (this.reportTimer) clearInterval(this.reportTimer);
        await this.saveAll();
        console.log('\n⏹️  Crew system stopped');
    }

    async tick() {
        if (!this.running) return;

        const timestamp = new Date().toLocaleTimeString();
        const activeCrew = Array.from(this.crew.values()).filter(c => c.status === 'ACTIVE');

        // Simulate activities
        for (const crew of activeCrew) {
            // Random energy drain
            crew.stats.energy = Math.max(0, crew.stats.energy - Math.random() * 2);
            
            // Discovery chance (1%)
            if (Math.random() < 0.01) {
                await this.makeDiscovery(crew);
            }
            
            // XP gain for being active
            crew.xp += 1;
            if (crew.xp >= [100, 500, 2000, 10000, 50000][crew.level] || 999999) {
                await this.levelUp(crew);
            }
            
            await this.saveCrewMember(crew);
        }

        console.log(`[${timestamp}] Tick complete - ${activeCrew.length} active crew`);
    }

    async makeDiscovery(crew) {
        const discoveries = [
            'Ancient Ruins', 'Unknown Signal', 'Rare Minerals', 
            'Anomalous Planet', 'Derelict Ship', 'Nebula Cloud',
            'Space Anomaly', 'Alien Artifact', 'Hidden Base'
        ];
        
        const discovery = {
            name: discoveries[Math.floor(Math.random() * discoveries.length)],
            location: crew.location.system,
            timestamp: Date.now()
        };
        
        crew.discoveries.push(discovery);
        crew.missionsCompleted++;
        crew.xp += 50;
        
        console.log(`🔭 ${crew.name} discovered: ${discovery.name}!`);
        
        // Log to expeditions
        const logEntry = `[${new Date().toISOString()}] ${crew.name} (${crew.role}) discovered ${discovery.name} in ${discovery.location}\n`;
        await fs.appendFile(path.join(CONFIG.expeditionsPath, 'discoveries.log'), logEntry);
    }

    async levelUp(crew) {
        if (crew.level >= LEVELS.length - 1) return;
        
        crew.level++;
        crew.stats.maxHealth += 10;
        crew.stats.health = crew.stats.maxHealth;
        
        console.log(`🎉 ${crew.name} promoted to ${LEVELS[crew.level]}!`);
    }

    async sendReport() {
        const report = this.generateReport();
        
        // Save report
        const reportPath = path.join(CONFIG.expeditionsPath, `crew_report_${Date.now()}.json`);
        await fs.writeFile(reportPath, JSON.stringify(report, null, 2));
        
        // Print to console
        console.log('\n📊 CREW REPORT');
        console.log('═══════════════════════════════════════════');
        console.log(`Time: ${new Date(report.timestamp).toLocaleString()}`);
        console.log(`Crew: ${report.summary.total} total (${report.summary.active} active)`);
        console.log('─────────────────────────────────────────────');
        
        for (const member of report.members) {
            console.log(`${member.name} [${member.role}] - ${LEVELS[member.level]}`);
            console.log(`  Health: ${member.health} | Energy: ${member.energy} | XP: ${member.xp}`);
            console.log(`  Missions: ${member.missions} | Discoveries: ${member.discoveries}`);
            console.log('');
        }
        
        if (report.highlights.length > 0) {
            console.log('🌟 HIGHLIGHTS:');
            for (const h of report.highlights.slice(-3)) {
                console.log(`   • ${h}`);
            }
        }
        console.log('═══════════════════════════════════════════\n');
    }

    generateReport() {
        const members = [];
        const highlights = [];
        
        for (const crew of this.crew.values()) {
            members.push({
                name: crew.name,
                role: crew.role,
                level: crew.level,
                health: `${crew.stats.health}/${crew.stats.maxHealth}`,
                energy: Math.round(crew.stats.energy),
                xp: crew.xp,
                status: crew.status,
                missions: crew.missionsCompleted,
                discoveries: crew.discoveries.length
            });
            
            if (crew.discoveries.length > 0) {
                const latest = crew.discoveries[crew.discoveries.length - 1];
                highlights.push(`${crew.name} discovered ${latest.name}`);
            }
        }
        
        return {
            timestamp: new Date().toISOString(),
            summary: {
                total: this.crew.size,
                active: Array.from(this.crew.values()).filter(c => c.status === 'ACTIVE').length
            },
            members,
            highlights
        };
    }

    // Command interface
    async command(cmd, args = []) {
        switch(cmd) {
            case 'status':
                return this.generateReport();
                
            case 'list':
                return Array.from(this.crew.values()).map(c => ({
                    name: c.name,
                    role: c.role,
                    level: LEVELS[c.level],
                    status: c.status
                }));
                
            case 'rest':
                const hours = parseInt(args[0]) || 8;
                for (const crew of this.crew.values()) {
                    crew.stats.health = Math.min(crew.stats.maxHealth, crew.stats.health + hours * 5);
                    crew.stats.energy = Math.min(100, crew.stats.energy + hours * 10);
                    await this.saveCrewMember(crew);
                }
                return { rested: true, hours };
                
            case 'add':
                if (this.crew.size >= CONFIG.maxCrew) {
                    return { error: 'Max crew size reached' };
                }
                const newMember = this.generateCrewMember(args[0] || null);
                this.crew.set(newMember.id, newMember);
                await this.saveCrewMember(newMember);
                return { added: newMember };
                
            default:
                return { error: 'Unknown command' };
        }
    }
}

// CLI
async function main() {
    const system = new LiteCrewSystem();
    await system.init();
    
    const cmd = process.argv[2];
    
    if (cmd === 'start' || !cmd) {
        await system.start();
        
        // Setup shutdown handlers
        process.on('SIGINT', async () => {
            await system.stop();
            process.exit(0);
        });
        
        process.on('SIGTERM', async () => {
            await system.stop();
            process.exit(0);
        });
        
        // Keep alive
        setInterval(() => {}, 1000);
        
    } else {
        const result = await system.command(cmd, process.argv.slice(3));
        console.log(JSON.stringify(result, null, 2));
        await system.stop();
    }
}

main().catch(console.error);
