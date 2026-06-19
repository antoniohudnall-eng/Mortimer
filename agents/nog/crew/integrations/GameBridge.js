/**
 * N'og nog Game Server Bridge v1.0
 * Connects crew to real game servers (Roblox, Minecraft)
 */

const { spawn } = require('child_process');
const WebSocket = require('ws');
const EventEmitter = require('events');

class GameBridge extends EventEmitter {
    constructor(config = {}) {
        super();
        this.config = {
            roblox: {
                enabled: config.roblox?.enabled ?? true,
                bridgePort: config.roblox?.port || 8081,
                commandEndpoint: config.roblox?.endpoint || 'http://localhost:8081/command'
            },
            minecraft: {
                enabled: config.minecraft?.enabled ?? true,
                serverHost: config.minecraft?.host || 'localhost',
                serverPort: config.minecraft?.port || 25565,
                rconPort: config.minecraft?.rconPort || 25575,
                rconPassword: config.minecraft?.rconPassword || ''
            },
            mineflayer: {
                enabled: config.mineflayer?.enabled ?? true,
                botCount: config.mineflayer?.bots || 4,
                botNames: config.mineflayer?.names || ['Forge', 'Patricia', 'Chelios', 'Stella']
            }
        };
        
        this.connections = new Map();
        this.crewPositions = new Map();
        this.activeBots = new Map();
        this.gameState = {
            roblox: null,
            minecraft: null
        };
    }
    
    async init() {
        console.log('[GameBridge] Initializing...');
        
        if (this.config.roblox.enabled) {
            await this.initRobloxBridge();
        }
        
        if (this.config.minecraft.enabled) {
            await this.initMinecraftBridge();
        }
        
        if (this.config.mineflayer.enabled) {
            await this.initMineflayerBots();
        }
        
        console.log('[GameBridge] Initialization complete');
    }
    
    // Roblox Bridge
    async initRobloxBridge() {
        console.log('[GameBridge] Connecting to Roblox bridge...');
        
        // Check if Roblox bridge is running
        try {
            const response = await fetch(`http://localhost:${this.config.roblox.bridgePort}/status`);
            if (response.ok) {
                this.gameState.roblox = await response.json();
                console.log('[GameBridge] Roblox bridge connected');
                
                // Setup WebSocket for real-time updates
                this.connectRobloxWebSocket();
            }
        } catch (err) {
            console.log('[GameBridge] Roblox bridge not available, will retry');
        }
    }
    
    connectRobloxWebSocket() {
        const ws = new WebSocket(`ws://localhost:${this.config.roblox.bridgePort}/ws`);
        
        ws.on('open', () => {
            console.log('[GameBridge] Roblox WebSocket connected');
            this.connections.set('roblox', ws);
        });
        
        ws.on('message', (data) => {
            try {
                const event = JSON.parse(data);
                this.handleRobloxEvent(event);
            } catch (err) {
                console.error('[GameBridge] Roblox message parse error:', err);
            }
        });
        
        ws.on('close', () => {
            console.log('[GameBridge] Roblox WebSocket disconnected');
            this.connections.delete('roblox');
            // Reconnect after delay
            setTimeout(() => this.connectRobloxWebSocket(), 5000);
        });
    }
    
    handleRobloxEvent(event) {
        switch (event.type) {
            case 'player_join':
                this.emit('roblox:player:join', event.data);
                break;
            case 'player_leave':
                this.emit('roblox:player:leave', event.data);
                break;
            case 'chat':
                this.emit('roblox:chat', event.data);
                break;
            case 'crew_position':
                this.crewPositions.set(event.data.crewId, {
                    ...event.data.position,
                    game: 'roblox',
                    timestamp: Date.now()
                });
                this.emit('position:update', event.data);
                break;
        }
    }
    
    async sendRobloxCommand(command, params = {}) {
        try {
            const response = await fetch(this.config.roblox.commandEndpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command, params })
            });
            return await response.json();
        } catch (err) {
            console.error('[GameBridge] Roblox command failed:', err);
            return { success: false, error: err.message };
        }
    }
    
    // Minecraft Bridge
    async initMinecraftBridge() {
        console.log('[GameBridge] Connecting to Minecraft...');
        
        // Try RCON first
        if (this.config.minecraft.rconPassword) {
            await this.connectMinecraftRCON();
        }
    }
    
    async connectMinecraftRCON() {
        // Use rcon-client for Minecraft commands
        try {
            const { Rcon } = await import('rcon-client');
            const rcon = new Rcon({
                host: this.config.minecraft.serverHost,
                port: this.config.minecraft.rconPort,
                password: this.config.minecraft.rconPassword
            });
            
            await rcon.connect();
            console.log('[GameBridge] Minecraft RCON connected');
            this.connections.set('minecraft_rcon', rcon);
            
            // Get server status
            const response = await rcon.send('list');
            this.gameState.minecraft = { players: response };
            
        } catch (err) {
            console.log('[GameBridge] Minecraft RCON unavailable:', err.message);
        }
    }
    
    async sendMinecraftCommand(command) {
        const rcon = this.connections.get('minecraft_rcon');
        if (!rcon) {
            return { success: false, error: 'RCON not connected' };
        }
        
        try {
            const response = await rcon.send(command);
            return { success: true, response };
        } catch (err) {
            return { success: false, error: err.message };
        }
    }
    
    // Mineflayer Bots
    async initMineflayerBots() {
        console.log('[GameBridge] Spawning Mineflayer bots...');
        
        for (let i = 0; i < this.config.mineflayer.botCount; i++) {
            const name = this.config.mineflayer.botNames[i] || `CrewBot${i}`;
            await this.spawnMineflayerBot(name);
        }
    }
    
    async spawnMineflayerBot(name) {
        const botScript = `
            const mineflayer = require('mineflayer');
            
            const bot = mineflayer.createBot({
                host: '${this.config.minecraft.serverHost}',
                port: ${this.config.minecraft.serverPort},
                username: '${name}',
                auth: 'offline'
            });
            
            bot.on('spawn', () => {
                console.log('${name}: Spawned');
            });
            
            bot.on('chat', (username, message) => {
                if (username === bot.username) return;
                console.log(JSON.stringify({ type: 'chat', username, message, bot: '${name}' }));
            });
            
            bot.on('move', () => {
                console.log(JSON.stringify({ 
                    type: 'position', 
                    bot: '${name}',
                    pos: bot.entity.position 
                }));
            });
        `;
        
        // Spawn bot process
        const botProcess = spawn('node', ['-e', botScript], {
            stdio: ['ignore', 'pipe', 'pipe']
        });
        
        this.activeBots.set(name, botProcess);
        
        botProcess.stdout.on('data', (data) => {
            const lines = data.toString().trim().split('\n');
            for (const line of lines) {
                try {
                    const event = JSON.parse(line);
                    this.handleMineflayerEvent(name, event);
                } catch {
                    console.log(`[${name}] ${line}`);
                }
            }
        });
        
        botProcess.stderr.on('data', (data) => {
            console.error(`[${name}] Error:`, data.toString());
        });
        
        botProcess.on('exit', (code) => {
            console.log(`[${name}] Bot exited with code ${code}`);
            this.activeBots.delete(name);
            // Respawn after delay
            setTimeout(() => this.spawnMineflayerBot(name), 10000);
        });
    }
    
    handleMineflayerEvent(botName, event) {
        switch (event.type) {
            case 'chat':
                this.emit('minecraft:chat', {
                    bot: botName,
                    username: event.username,
                    message: event.message
                });
                break;
            case 'position':
                this.crewPositions.set(botName, {
                    ...event.pos,
                    game: 'minecraft',
                    timestamp: Date.now()
                });
                this.emit('position:update', { bot: botName, position: event.pos });
                break;
        }
    }
    
    // Send command to specific bot
    sendBotCommand(botName, command, params = {}) {
        const bot = this.activeBots.get(botName);
        if (!bot) {
            return { success: false, error: 'Bot not found' };
        }
        
        // Send command via stdin
        bot.stdin.write(JSON.stringify({ command, params }) + '\n');
        return { success: true };
    }
    
    // Get current positions of all crew
    getCrewPositions() {
        const positions = {};
        for (const [id, pos] of this.crewPositions) {
            positions[id] = pos;
        }
        return positions;
    }
    
    // Execute crew action in game
    async executeCrewAction(crewId, action, gameTarget = 'auto') {
        const position = this.crewPositions.get(crewId);
        
        // Determine target game
        if (gameTarget === 'auto') {
            gameTarget = position?.game || 'roblox';
        }
        
        console.log(`[GameBridge] Executing ${action.type} for ${crewId} in ${gameTarget}`);
        
        switch (gameTarget) {
            case 'roblox':
                return await this.sendRobloxCommand('crew_action', {
                    crewId,
                    action: action.type,
                    params: action
                });
                
            case 'minecraft':
                // Find bot associated with crew
                const botName = Array.from(this.activeBots.keys())
                    .find(name => name.toLowerCase() === crewId.toLowerCase());
                if (botName) {
                    return this.sendBotCommand(botName, action.type, action);
                }
                return { success: false, error: 'No bot for crew member' };
                
            default:
                return { success: false, error: 'Unknown game target' };
        }
    }
    
    // Cleanup
    async cleanup() {
        // Kill all bots
        for (const [name, bot] of this.activeBots) {
            bot.kill();
            console.log(`[GameBridge] Killed bot: ${name}`);
        }
        this.activeBots.clear();
        
        // Close connections
        for (const [name, conn] of this.connections) {
            if (conn.close) conn.close();
            if (conn.end) conn.end();
        }
        this.connections.clear();
    }
}

module.exports = GameBridge;