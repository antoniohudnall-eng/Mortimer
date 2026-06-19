/**
 * N'og nog Crew Coordinator v1.0
 * Main orchestrator for crew system
 */

const CrewManager = require('./CrewManager');
const BrainCrew = require('../ai/BrainCrew');
const GameBridge = require('../integrations/GameBridge');
const CrewComms = require('../comms/CrewComms');

class CrewCoordinator {
    constructor(config = {}) {
        this.config = {
            tickInterval: config.tickInterval || 30000, // 30 seconds
            reportInterval: config.reportInterval || 3600000, // 1 hour
            storagePath: config.storagePath || './storage/crew',
            brainSocket: config.brainSocket || '/tmp/aos_brain.sock',
            ...config
        };
        
        this.crewManager = new CrewManager(this.config.storagePath);
        this.brainCrew = new BrainCrew(this.config.brainSocket);
        this.gameBridge = new GameBridge(config.gameBridge);
        this.comms = new CrewComms(config.comms);
        
        this.running = false;
        this.tickTimer = null;
        this.reportTimer = null;
        
        // Event handlers
        this.setupEventHandlers();
    }
    
    setupEventHandlers() {
        // Brain crew actions
        this.brainCrew.on('crew:action', async (event) => {
            console.log(`[Coordinator] Crew action: ${event.crew.name} - ${event.action.type}`);
            
            // Execute in game
            const result = await this.gameBridge.executeCrewAction(
                event.crew.id,
                event.action
            );
            
            // Notify if important
            if (event.action.type === 'DISCOVER' || event.urgency > 0.8) {
                await this.comms.sendDiscoveryAlert(event.crew, {
                    name: event.action.target,
                    location: event.crew.location
                });
            }
        });
        
        // Position updates
        this.gameBridge.on('position:update', (data) => {
            const crew = this.crewManager.crew.get(data.crewId);
            if (crew) {
                crew.location = {
                    ...crew.location,
                    ...data.position
                };
            }
        });
        
        // Telegram messages
        this.comms.on('telegram:message', (msg) => {
            console.log(`[Coordinator] Telegram from ${msg.from}: ${msg.text}`);
        });
        
        // Photos from crew
        this.comms.on('photo:saved', (data) => {
            console.log(`[Coordinator] Photo received from ${data.from}: ${data.filename}`);
        });
    }
    
    async init() {
        console.log('[Coordinator] Initializing N\'og nog Crew System...');
        
        await this.crewManager.init();
        await this.gameBridge.init();
        await this.comms.init();
        
        console.log('[Coordinator] All systems initialized');
        return this;
    }
    
    async start() {
        if (this.running) return;
        
        this.running = true;
        console.log('[Coordinator] Starting crew automation...');
        
        // Send initial report
        await this.sendDailyReport();
        
        // Start tick loop
        this.tickTimer = setInterval(() => this.tick(), this.config.tickInterval);
        
        // Start report timer
        this.reportTimer = setInterval(() => this.sendDailyReport(), this.config.reportInterval);
        
        console.log('[Coordinator] Running - tick: ' + this.config.tickInterval + 'ms, report: ' + this.config.reportInterval + 'ms');
    }
    
    async stop() {
        this.running = false;
        
        if (this.tickTimer) clearInterval(this.tickTimer);
        if (this.reportTimer) clearInterval(this.reportTimer);
        
        await this.crewManager.saveAll();
        await this.gameBridge.cleanup();
        
        console.log('[Coordinator] Stopped');
    }
    
    async tick() {
        if (!this.running) return;
        
        console.log(`[Coordinator] Tick at ${new Date().toISOString()}`);
        
        // Get current game state
        const gameState = {
            situation: 'exploration', // Could be dynamic
            threats: [],
            opportunities: [],
            resources: {},
            crewPositions: this.gameBridge.getCrewPositions()
        };
        
        // Process brain-driven crew decisions
        try {
            const decisions = await this.brainCrew.processCrewTick(this.crewManager, gameState);
            
            if (decisions.length > 0) {
                console.log(`[Coordinator] ${decisions.length} crew decisions processed`);
            }
        } catch (err) {
            console.error('[Coordinator] Brain crew tick failed:', err);
        }
        
        // Random discovery chance
        await this.checkForDiscoveries();
        
        // Save crew state
        await this.crewManager.saveAll();
    }
    
    async checkForDiscoveries() {
        const activeCrew = this.crewManager.getAvailable();
        
        for (const crew of activeCrew) {
            // 1% chance per tick per crew member
            if (Math.random() < 0.01) {
                const discoveries = [
                    { name: 'Ancient Ruins', type: 'archaeological' },
                    { name: 'Unknown Signal', type: 'signal' },
                    { name: 'Rare Minerals', type: 'resource' },
                    { name: 'Anomalous Planet', type: 'planet' },
                    { name: 'Derelict Ship', type: 'ship' },
                    { name: 'Nebula Cloud', type: 'phenomenon' }
                ];
                
                const discovery = discoveries[Math.floor(Math.random() * discoveries.length)];
                discovery.location = crew.location.planet || crew.location.system || 'Unknown';
                
                // Award XP and save discovery
                const result = await this.crewManager.addDiscovery(crew.id, discovery);
                const xpResult = await this.crewManager.awardXP(crew.id, 50 + Math.floor(Math.random() * 100));
                
                console.log(`[Coordinator] ${crew.name} discovered ${discovery.name}!`);
                
                // Send notification
                await this.comms.sendDiscoveryAlert(crew, discovery);
                
                if (xpResult.levelUp) {
                    await this.comms.sendTelegram(
                        `🎉 <b>Level Up!</b>\n\n${crew.name} has reached ${xpResult.newLevel}!`,
                        { parse_mode: 'HTML' }
                    );
                }
            }
        }
    }
    
    async sendDailyReport() {
        console.log('[Coordinator] Sending daily crew report...');
        
        const report = this.crewManager.generateReport();
        await this.comms.sendCrewReport(report, 'both');
        
        console.log('[Coordinator] Report sent to captain');
    }
    
    // API for external commands
    async command(action, params = {}) {
        switch (action) {
            case 'status':
                return {
                    crew: this.crewManager.getStatus(),
                    running: this.running,
                    gameConnections: {
                        roblox: this.gameBridge.gameState.roblox ? 'connected' : 'disconnected',
                        minecraft: this.gameBridge.gameState.minecraft ? 'connected' : 'disconnected'
                    }
                };
                
            case 'rest':
                await this.crewManager.restCrew(params.hours || 8);
                return { success: true, message: 'Crew rested' };
                
            case 'send_report':
                await this.sendDailyReport();
                return { success: true };
                
            case 'add_crew':
                if (this.crewManager.crew.size >= this.crewManager.maxCrewSize) {
                    return { success: false, error: 'Max crew size reached' };
                }
                const newMember = this.crewManager.generateCrewMember(null, params.role);
                this.crewManager.crew.set(newMember.id, newMember);
                await this.crewManager.saveCrewMember(newMember);
                return { success: true, crew: newMember };
                
            case 'get_crew':
                const crew = Array.from(this.crewManager.crew.values());
                return { success: true, crew };
                
            case 'assign_personality':
                const personality = this.brainCrew.assignPersonality(params.crewId, params.type);
                return { success: true, personality };
                
            default:
                return { success: false, error: 'Unknown command' };
        }
    }
}

module.exports = CrewCoordinator;