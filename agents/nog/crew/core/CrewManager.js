/**
 * N'og nog Crew Manager v1.0
 * Persistent crew management with lightweight storage
 */

const fs = require('fs').promises;
const path = require('path');

class CrewManager {
    constructor(storagePath = './storage/crew') {
        this.storagePath = storagePath;
        this.crew = new Map();
        this.activeMissions = new Map();
        this.maxCrewSize = 10;
        this.initialCrewSize = 5;
        
        // Crew roles and specializations
        this.ROLES = {
            PILOT: { skill: 'navigation', bonus: 1.5 },
            ENGINEER: { skill: 'repair', bonus: 1.5 },
            SCIENTIST: { skill: 'scanning', bonus: 1.5 },
            COMBAT: { skill: 'combat', bonus: 1.5 },
            MEDIC: { skill: 'healing', bonus: 1.5 },
            TRADER: { skill: 'trading', bonus: 1.5 }
        };
        
        // Experience levels
        this.LEVELS = [
            { name: 'Rookie', xp: 0 },
            { name: 'Cadet', xp: 100 },
            { name: 'Officer', xp: 500 },
            { name: 'Veteran', xp: 2000 },
            { name: 'Elite', xp: 10000 },
            { name: 'Legend', xp: 50000 }
        ];
    }
    
    async init() {
        await this.ensureStorageDir();
        await this.loadCrew();
        
        if (this.crew.size === 0) {
            await this.generateInitialCrew();
        }
        
        console.log(`[CrewManager] Initialized with ${this.crew.size} crew members`);
    }
    
    async ensureStorageDir() {
        try {
            await fs.mkdir(this.storagePath, { recursive: true });
        } catch (err) {
            console.error('[CrewManager] Failed to create storage:', err);
        }
    }
    
    generateCrewMember(id, role = null) {
        const names = [
            'Zara', 'Kael', 'Nyx', 'Orion', 'Luna', 'Rex', 'Vex', 'Nova',
            'Jax', 'Aria', 'Kira', 'Thane', 'Echo', 'Flux', 'Zen', 'Pyre'
        ];
        
        const roles = Object.keys(this.ROLES);
        const assignedRole = role || roles[Math.floor(Math.random() * roles.length)];
        
        return {
            id: id || `crew_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            name: names[Math.floor(Math.random() * names.length)],
            role: assignedRole,
            level: 0,
            xp: 0,
            stats: {
                health: 100,
                maxHealth: 100,
                energy: 100,
                maxEnergy: 100,
                morale: 100,
                loyalty: 80 + Math.floor(Math.random() * 20)
            },
            skills: {
                navigation: Math.floor(Math.random() * 20) + 10,
                repair: Math.floor(Math.random() * 20) + 10,
                scanning: Math.floor(Math.random() * 20) + 10,
                combat: Math.floor(Math.random() * 20) + 10,
                healing: Math.floor(Math.random() * 20) + 10,
                trading: Math.floor(Math.random() * 20) + 10
            },
            inventory: [],
            equipped: {},
            missionsCompleted: 0,
            discoveries: [],
            status: 'ACTIVE', // ACTIVE, INJURED, RESTING, MIA, DEAD
            location: {
                universe: 'PRIME',
                galaxy: null,
                system: null,
                planet: null
            },
            created: Date.now(),
            lastActive: Date.now()
        };
    }
    
    async generateInitialCrew() {
        const initialRoles = ['PILOT', 'ENGINEER', 'SCIENTIST', 'COMBAT', 'MEDIC'];
        
        for (let i = 0; i < this.initialCrewSize; i++) {
            const member = this.generateCrewMember(null, initialRoles[i]);
            this.crew.set(member.id, member);
            await this.saveCrewMember(member);
        }
        
        console.log(`[CrewManager] Generated ${this.initialCrewSize} initial crew members`);
    }
    
    async saveCrewMember(member) {
        const filePath = path.join(this.storagePath, `${member.id}.json`);
        try {
            await fs.writeFile(filePath, JSON.stringify(member, null, 2));
        } catch (err) {
            console.error(`[CrewManager] Failed to save crew member ${member.id}:`, err);
        }
    }
    
    async loadCrew() {
        try {
            const files = await fs.readdir(this.storagePath);
            for (const file of files) {
                if (file.endsWith('.json')) {
                    const data = await fs.readFile(path.join(this.storagePath, file), 'utf8');
                    const member = JSON.parse(data);
                    this.crew.set(member.id, member);
                }
            }
        } catch (err) {
            console.log('[CrewManager] No existing crew data found');
        }
    }
    
    async saveAll() {
        for (const member of this.crew.values()) {
            await this.saveCrewMember(member);
        }
    }
    
    // Get crew by role
    getByRole(role) {
        return Array.from(this.crew.values()).filter(c => c.role === role && c.status === 'ACTIVE');
    }
    
    // Get available crew
    getAvailable() {
        return Array.from(this.crew.values()).filter(c => c.status === 'ACTIVE');
    }
    
    // Get crew status summary
    getStatus() {
        const status = {
            total: this.crew.size,
            active: 0,
            injured: 0,
            resting: 0,
            mia: 0,
            byRole: {}
        };
        
        for (const member of this.crew.values()) {
            status[member.status.toLowerCase()]++;
            status.byRole[member.role] = (status.byRole[member.role] || 0) + 1;
        }
        
        return status;
    }
    
    // Award XP and check for level up
    async awardXP(crewId, amount) {
        const member = this.crew.get(crewId);
        if (!member) return null;
        
        member.xp += amount;
        member.lastActive = Date.now();
        
        // Check for level up
        let levelUp = false;
        for (let i = member.level + 1; i < this.LEVELS.length; i++) {
            if (member.xp >= this.LEVELS[i].xp) {
                member.level = i;
                levelUp = true;
                
                // Improve role skill
                const roleSkill = this.ROLES[member.role].skill;
                member.skills[roleSkill] += 5;
                
                // Increase stats
                member.stats.maxHealth += 10;
                member.stats.maxEnergy += 10;
                member.stats.health = member.stats.maxHealth;
                member.stats.energy = member.stats.maxEnergy;
            }
        }
        
        await this.saveCrewMember(member);
        return { member, levelUp, newLevel: this.LEVELS[member.level].name };
    }
    
    // Update crew status
    async updateStatus(crewId, status) {
        const member = this.crew.get(crewId);
        if (!member) return false;
        
        member.status = status;
        member.lastActive = Date.now();
        await this.saveCrewMember(member);
        return true;
    }
    
    // Add discovery
    async addDiscovery(crewId, discovery) {
        const member = this.crew.get(crewId);
        if (!member) return false;
        
        member.discoveries.push({
            ...discovery,
            timestamp: Date.now()
        });
        member.missionsCompleted++;
        await this.saveCrewMember(member);
        return true;
    }
    
    // Get crew report for captain
    generateReport() {
        const report = {
            timestamp: new Date().toISOString(),
            crewSummary: this.getStatus(),
            members: [],
            highlights: []
        };
        
        for (const member of this.crew.values()) {
            report.members.push({
                id: member.id,
                name: member.name,
                role: member.role,
                level: this.LEVELS[member.level].name,
                status: member.status,
                health: `${member.stats.health}/${member.stats.maxHealth}`,
                location: member.location.planet || member.location.system || member.location.galaxy || member.location.universe,
                missions: member.missionsCompleted,
                discoveries: member.discoveries.length
            });
            
            // Generate highlights
            if (member.discoveries.length > 0) {
                const latest = member.discoveries[member.discoveries.length - 1];
                report.highlights.push(`${member.name} discovered ${latest.name || 'an anomaly'} in ${latest.location || 'unknown space'}`);
            }
        }
        
        return report;
    }
    
    // Rest crew (recover health/energy)
    async restCrew(hours = 8) {
        for (const member of this.crew.values()) {
            if (member.status === 'ACTIVE' || member.status === 'RESTING') {
                member.stats.health = Math.min(member.stats.maxHealth, 
                    member.stats.health + (hours * 5));
                member.stats.energy = Math.min(member.stats.maxEnergy, 
                    member.stats.energy + (hours * 10));
                
                if (member.status === 'RESTING') {
                    member.status = 'ACTIVE';
                }
                
                await this.saveCrewMember(member);
            }
        }
    }
}

module.exports = CrewManager;