/**
 * N'og nog Brain-Integrated Crew AI v1.0
 * Connects crew members to AOS brain for autonomous decision making
 */

const EventEmitter = require('events');

class BrainCrew extends EventEmitter {
    constructor(brainSocketPath = '/tmp/aos_brain.sock') {
        super();
        this.brainSocket = brainSocketPath;
        this.crewPersonalities = new Map();
        this.activeDecisions = new Map();
        this.decisionQueue = [];
        
        // Personality traits that influence decision making
        this.PERSONALITY_TYPES = {
            CAUTIOUS: { risk: 0.2, aggression: 0.2, curiosity: 0.7 },
            BOLD: { risk: 0.8, aggression: 0.7, curiosity: 0.9 },
            BALANCED: { risk: 0.5, aggression: 0.5, curiosity: 0.6 },
            CURIOUS: { risk: 0.6, aggression: 0.3, curiosity: 1.0 },
            AGGRESSIVE: { risk: 0.7, aggression: 1.0, curiosity: 0.5 }
        };
        
        this.connectToBrain();
    }
    
    connectToBrain() {
        // Simulated brain connection - in production, use net.Socket
        console.log('[BrainCrew] Connecting to AOS brain...');
        this.connected = true;
        this.emit('connected');
    }
    
    // Assign personality to crew member
    assignPersonality(crewId, type = 'BALANCED') {
        const personality = {
            type: type,
            traits: this.PERSONALITY_TYPES[type],
            memory: [], // Short-term decision memory
            preferences: new Map(),
            relationships: new Map() // How they feel about other crew
        };
        
        this.crewPersonalities.set(crewId, personality);
        return personality;
    }
    
    // Query brain for decision
    async queryBrain(crewMember, context) {
        const personality = this.crewPersonalities.get(crewMember.id) || 
            this.assignPersonality(crewMember.id);
        
        // Build decision prompt
        const decisionPrompt = this.buildDecisionPrompt(crewMember, personality, context);
        
        try {
            // Query brain via socket
            const decision = await this.sendToBrain(decisionPrompt);
            return this.parseDecision(decision, crewMember, context);
        } catch (err) {
            console.error('[BrainCrew] Brain query failed:', err);
            // Fallback to rule-based decision
            return this.fallbackDecision(crewMember, personality, context);
        }
    }
    
    buildDecisionPrompt(crew, personality, context) {
        return {
            cmd: 'decide',
            params: {
                crew: {
                    name: crew.name,
                    role: crew.role,
                    health: crew.stats.health,
                    energy: crew.stats.energy,
                    level: crew.level,
                    skills: crew.skills
                },
                personality: personality.traits,
                context: {
                    situation: context.situation, // 'exploration', 'combat', 'trade', 'emergency'
                    location: context.location,
                    threats: context.threats || [],
                    opportunities: context.opportunities || [],
                    resources: context.resources || {},
                    crewNearby: context.crewNearby || []
                },
                options: context.options || []
            }
        };
    }
    
    async sendToBrain(prompt) {
        // In production: use net.Socket to /tmp/aos_brain.sock
        // Simulated brain response
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    action: this.selectAction(prompt),
                    confidence: 0.7 + Math.random() * 0.3,
                    reasoning: 'Brain-processed decision',
                    urgency: this.calculateUrgency(prompt)
                });
            }, 100);
        });
    }
    
    selectAction(prompt) {
        const { personality, context } = prompt.params;
        const options = prompt.params.options;
        
        if (options.length === 0) {
            return { type: 'WAIT', reason: 'No valid options' };
        }
        
        // Score each option based on personality
        const scored = options.map(opt => {
            let score = 0.5;
            
            if (opt.risk !== undefined) {
                score += (1 - Math.abs(opt.risk - personality.traits.risk)) * 0.3;
            }
            if (opt.reward !== undefined) {
                score += opt.reward * 0.3;
            }
            if (opt.type && opt.type === 'EXPLORE') {
                score += personality.traits.curiosity * 0.2;
            }
            if (opt.type && opt.type === 'COMBAT') {
                score += personality.traits.aggression * 0.2;
            }
            
            return { option: opt, score };
        });
        
        // Select highest scoring
        scored.sort((a, b) => b.score - a.score);
        return scored[0].option;
    }
    
    calculateUrgency(prompt) {
        const { context } = prompt.params;
        
        if (context.situation === 'emergency') return 1.0;
        if (context.threats && context.threats.length > 0) return 0.8;
        if (context.situation === 'combat') return 0.7;
        return 0.3;
    }
    
    parseDecision(decision, crew, context) {
        return {
            crewId: crew.id,
            action: decision.action,
            confidence: decision.confidence,
            reasoning: decision.reasoning,
            urgency: decision.urgency,
            timestamp: Date.now(),
            execute: () => this.executeDecision(crew, decision, context)
        };
    }
    
    fallbackDecision(crew, personality, context) {
        // Rule-based fallback
        const healthPercent = crew.stats.health / crew.stats.maxHealth;
        const energyPercent = crew.stats.energy / crew.stats.maxEnergy;
        
        if (healthPercent < 0.3) {
            return {
                crewId: crew.id,
                action: { type: 'RETREAT', target: 'nearest_safe_zone' },
                confidence: 0.9,
                reasoning: 'Low health - survival priority',
                urgency: 0.9,
                timestamp: Date.now()
            };
        }
        
        if (energyPercent < 0.2) {
            return {
                crewId: crew.id,
                action: { type: 'REST', duration: 60 },
                confidence: 0.8,
                reasoning: 'Low energy - need rest',
                urgency: 0.6,
                timestamp: Date.now()
            };
        }
        
        // Default exploration based on personality
        const exploreChance = personality.traits.curiosity;
        return {
            crewId: crew.id,
            action: { 
                type: exploreChance > 0.6 ? 'EXPLORE' : 'PATROL',
                target: context.opportunities[0] || 'random_direction'
            },
            confidence: 0.6,
            reasoning: 'Personality-driven default action',
            urgency: 0.3,
            timestamp: Date.now()
        };
    }
    
    async executeDecision(crew, decision, context) {
        console.log(`[BrainCrew] ${crew.name} executing: ${decision.action.type}`);
        
        // Emit event for game engine
        this.emit('crew:action', {
            crew,
            action: decision.action,
            context
        });
        
        // Update crew state based on action
        switch (decision.action.type) {
            case 'EXPLORE':
                crew.stats.energy -= 10;
                break;
            case 'COMBAT':
                crew.stats.energy -= 20;
                crew.stats.health -= 5 + Math.random() * 10;
                break;
            case 'REST':
                crew.stats.energy = Math.min(crew.stats.maxEnergy, crew.stats.energy + 30);
                break;
            case 'RETREAT':
                crew.stats.energy -= 15;
                break;
        }
        
        // Store decision in personality memory
        const personality = this.crewPersonalities.get(crew.id);
        if (personality) {
            personality.memory.push({
                decision: decision.action,
                outcome: null, // Updated later
                timestamp: Date.now()
            });
            
            // Keep memory short (last 20 decisions)
            if (personality.memory.length > 20) {
                personality.memory.shift();
            }
        }
        
        return { success: true, crew, decision };
    }
    
    // Generate autonomous behavior for all active crew
    async processCrewTick(crewManager, gameState) {
        const activeCrew = crewManager.getAvailable();
        const decisions = [];
        
        for (const crew of activeCrew) {
            // Build context from game state
            const context = this.buildContext(crew, gameState);
            
            // Get brain decision
            const decision = await this.queryBrain(crew, context);
            decisions.push(decision);
            
            // Execute if high urgency or batch processing
            if (decision.urgency > 0.7) {
                await decision.execute();
            }
        }
        
        return decisions;
    }
    
    buildContext(crew, gameState) {
        return {
            situation: gameState.situation || 'exploration',
            location: crew.location,
            threats: gameState.threats || [],
            opportunities: gameState.opportunities || [],
            resources: gameState.resources || {},
            crewNearby: gameState.crewPositions ? 
                Object.entries(gameState.crewPositions)
                    .filter(([id, pos]) => id !== crew.id && this.isNearby(crew.location, pos))
                    .map(([id]) => id) : []
        };
    }
    
    isNearby(loc1, loc2) {
        // Simple proximity check
        if (!loc1 || !loc2) return false;
        return loc1.system === loc2.system || loc1.planet === loc2.planet;
    }
    
    // Get crew personality summary for reports
    getPersonalityReport(crewId) {
        const personality = this.crewPersonalities.get(crewId);
        if (!personality) return null;
        
        return {
            type: personality.type,
            traits: personality.traits,
            memorySize: personality.memory.length,
            lastDecisions: personality.memory.slice(-5)
        };
    }
}

module.exports = BrainCrew;