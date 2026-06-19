#!/usr/bin/env node
/**
 * Mineflayer Agent with Brain OODA Integration
 * Autonomous agent that plays Minecraft using Brain decisions
 * 
 * Architecture:
 * - OODA Loop: Observe -> Orient -> Decide -> Act
 * - Multi-modal perception (vision, inventory, surroundings)
 * - Action execution (move, mine, craft, build, fight, chat)
 * - Brain communication via WebSocket
 * 
 * Usage: node mineflayer_agent.js <agent_id> <host> <port>
 */

const mineflayer = require('mineflayer');
const pathfinder = require('mineflayer-pathfinder').pathfinder;
const Movements = require('mineflayer-pathfinder').Movements;
const { GoalNear, GoalBlock, GoalFollow } = require('mineflayer-pathfinder').goals;
const WebSocket = require('ws');
const Vec3 = require('vec3');

// Agent configuration
const AGENT_ID = process.argv[2] || 'mylzeron';
const MC_HOST = process.argv[3] || 'localhost';
const MC_PORT = parseInt(process.argv[4]) || 25566;
const BRAIN_WS_URL = process.argv[5] || 'ws://localhost:8767';

console.log(`[${AGENT_ID}] Starting Mineflayer Agent...`);
console.log(`[${AGENT_ID}] Connecting to ${MC_HOST}:${MC_PORT}`);

// Create bot
const bot = mineflayer.createBot({
    host: MC_HOST,
    port: MC_PORT,
    username: AGENT_ID,
    version: '1.20.4',
    auth: 'offline'
});

// Load plugins
bot.loadPlugin(pathfinder);

// Agent state
const agentState = {
    id: AGENT_ID,
    tick: 0,
    position: null,
    health: 20,
    inventory: {},
    targets: {},
    tasks: [],
    memories: [],
    skills: {
        mining: 0,
        building: 0,
        combat: 0,
        crafting: 0,
        exploration: 0
    },
    currentAction: 'idle',
    actionQueue: [],
    socialRelations: {},
    lastDecision: null,
    ooda: {
        observe: {},
        orient: {},
        decide: {},
        act: {}
    }
};

// Brain WebSocket connection
let brainWs = null;
let brainConnected = false;

// Initialize
bot.once('spawn', async () => {
    console.log(`[${AGENT_ID}] Spawned in Minecraft world`);
    console.log(`[${AGENT_ID}] Position: ${bot.entity.position}`);
    
    // Configure pathfinder
    const mcData = require('minecraft-data')(bot.version);
    const defaultMove = new Movements(bot, mcData);
    bot.pathfinder.setMovements(defaultMove);
    
    // Connect to Brain
    connectToBrain();
    
    // Start OODA loop
    startOODALoop();
    
    // Announce presence
    bot.chat(`Agent ${AGENT_ID} online. Ready for commands.`);
});

// Connect to Brain WebSocket
function connectToBrain() {
    console.log(`[${AGENT_ID}] Connecting to Brain at ${BRAIN_WS_URL}`);
    
    try {
        brainWs = new WebSocket(BRAIN_WS_URL);
        
        brainWs.on('open', () => {
            console.log(`[${AGENT_ID}] Connected to Brain`);
            brainConnected = true;
            
            // Register with Brain
            brainWs.send(JSON.stringify({
                type: 'register_agent',
                agent_id: AGENT_ID,
                capabilities: Object.keys(agentState.skills),
                position: bot.entity.position
            }));
        });
        
        brainWs.on('message', (data) => {
            try {
                const message = JSON.parse(data);
                handleBrainMessage(message);
            } catch (e) {
                console.error(`[${AGENT_ID}] Brain message error:`, e);
            }
        });
        
        brainWs.on('close', () => {
            console.log(`[${AGENT_ID}] Brain disconnected`);
            brainConnected = false;
            setTimeout(connectToBrain, 5000);
        });
        
        brainWs.on('error', (err) => {
            console.error(`[${AGENT_ID}] Brain connection error:`, err.message);
        });
        
    } catch (e) {
        console.error(`[${AGENT_ID}] Failed to connect to Brain:`, e);
        setTimeout(connectToBrain, 5000);
    }
}

// OODA Loop - Core of agent intelligence
async function startOODALoop() {
    console.log(`[${AGENT_ID}] Starting OODA loop`);
    
    while (true) {
        agentState.tick++;
        
        // OBSERVE: Gather world data
        const observation = await observe();
        agentState.ooda.observe = observation;
        
        // ORIENT: Process and contextualize
        const orientation = orient(observation);
        agentState.ooda.orient = orientation;
        
        // DECIDE: Choose action based on goals and state
        const decision = decide(orientation);
        agentState.ooda.decide = decision;
        agentState.lastDecision = decision;
        
        // ACT: Execute decision
        const actionResult = await act(decision);
        agentState.ooda.act = actionResult;
        
        // Report to Brain
        if (brainConnected) {
            brainWs.send(JSON.stringify({
                type: 'ooda_tick',
                agent_id: AGENT_ID,
                tick: agentState.tick,
                observation: observation,
                decision: decision,
                action: actionResult
            }));
        }
        
        // Tick rate: 4 Hz (every 250ms)
        await new Promise(r => setTimeout(r, 250));
    }
}

// OBSERVE: Gather all sensory data
async function observe() {
    const position = bot.entity.position;
    const health = bot.health;
    const food = bot.food;
    
    // Inventory snapshot
    const inventory = {};
    bot.inventory.items().forEach(item => {
        inventory[item.name] = (inventory[item.name] || 0) + item.count;
    });
    
    // Surroundings scan
    const surroundings = {
        blocks: [],
        entities: [],
        drops: []
    };
    
    // Scan 16x16x16 area around agent
    for (let x = -8; x <= 8; x++) {
        for (let y = -4; y <= 4; y++) {
            for (let z = -8; z <= 8; z++) {
                const blockPos = position.offset(x, y, z);
                const block = bot.blockAt(blockPos);
                if (block && block.name !== 'air') {
                    surroundings.blocks.push({
                        type: block.name,
                        position: blockPos,
                        distance: blockPos.distanceTo(position)
                    });
                }
            }
        }
    }
    
    // Nearby entities
    for (const entity of Object.values(bot.entities)) {
        if (entity.position.distanceTo(position) < 32) {
            surroundings.entities.push({
                type: entity.name,
                position: entity.position,
                distance: entity.position.distanceTo(position),
                health: entity.health,
                isPlayer: entity.type === 'player'
            });
        }
    }
    
    // Nearby drops
    bot.nearestEntities?.forEach(entity => {
        if (entity.name === 'item') {
            surroundings.drops.push({
                position: entity.position,
                distance: entity.position.distanceTo(position)
            });
        }
    });
    
    // Time and weather
    const timeOfDay = bot.time.timeOfDay;
    const isDay = timeOfDay < 12000;
    
    return {
        timestamp: Date.now(),
        tick: agentState.tick,
        position: { x: position.x, y: position.y, z: position.z },
        health: health,
        food: food,
        inventory: inventory,
        surroundings: surroundings,
        timeOfDay: timeOfDay,
        isDay: isDay,
        currentAction: agentState.currentAction
    };
}

// ORIENT: Process observations into understanding
function orient(observation) {
    const orientation = {
        threats: [],
        opportunities: [],
        needs: [],
        goals: []
    };
    
    // Identify threats
    observation.surroundings.entities.forEach(entity => {
        if (['zombie', 'skeleton', 'creeper', 'spider'].includes(entity.type)) {
            orientation.threats.push({
                type: 'hostile_mob',
                entity: entity,
                urgency: entity.distance < 8 ? 'high' : 'medium'
            });
        }
    });
    
    // Identify opportunities
    observation.surroundings.blocks.forEach(block => {
        if (['diamond_ore', 'iron_ore', 'coal_ore', 'gold_ore'].includes(block.type)) {
            orientation.opportunities.push({
                type: 'resource',
                block: block,
                value: block.type === 'diamond_ore' ? 10 : 
                       block.type === 'gold_ore' ? 5 :
                       block.type === 'iron_ore' ? 3 : 1
            });
        }
    });
    
    // Identify needs
    if (observation.health < 10) {
        orientation.needs.push({ type: 'heal', urgency: 'critical' });
    }
    if (observation.food < 10) {
        orientation.needs.push({ type: 'food', urgency: 'high' });
    }
    if (Object.keys(observation.inventory).length === 0) {
        orientation.needs.push({ type: 'gather_resources', urgency: 'medium' });
    }
    
    // Set goals based on needs and opportunities
    if (orientation.needs.length > 0) {
        orientation.goals.push({
            type: 'satisfy_need',
            target: orientation.needs[0]
        });
    } else if (orientation.opportunities.length > 0) {
        orientation.goals.push({
            type: 'gather_resources',
            target: orientation.opportunities.sort((a, b) => b.value - a.value)[0]
        });
    } else {
        orientation.goals.push({ type: 'explore' });
    }
    
    return orientation;
}

// DECIDE: Choose action based on orientation
function decide(orientation) {
    const goal = orientation.goals[0];
    
    if (!goal) {
        return { action: 'idle', params: {} };
    }
    
    switch (goal.type) {
        case 'satisfy_need':
            if (goal.target.type === 'heal') {
                return { action: 'find_shelter', params: {} };
            } else if (goal.target.type === 'food') {
                return { action: 'hunt_food', params: {} };
            } else if (goal.target.type === 'gather_resources') {
                return { action: 'mine_resources', params: { target: 'wood' } };
            }
            break;
            
        case 'gather_resources':
            const target = goal.target;
            return {
                action: 'mine_block',
                params: {
                    block_type: target.block.type,
                    position: target.block.position
                }
            };
            
        case 'explore':
            return {
                action: 'explore',
                params: {
                    direction: Math.floor(Math.random() * 4)
                }
            };
    }
    
    return { action: 'idle', params: {} };
}

// ACT: Execute chosen action
async function act(decision) {
    agentState.currentAction = decision.action;
    
    try {
        switch (decision.action) {
            case 'idle':
                return { success: true, result: 'idling' };
                
            case 'mine_block':
                return await actionMineBlock(decision.params);
                
            case 'mine_resources':
                return await actionMineResources(decision.params);
                
            case 'hunt_food':
                return await actionHuntFood(decision.params);
                
            case 'explore':
                return await actionExplore(decision.params);
                
            case 'find_shelter':
                return await actionFindShelter(decision.params);
                
            case 'chat':
                bot.chat(decision.params.message);
                return { success: true, result: 'chatted' };
                
            default:
                return { success: false, error: 'unknown_action' };
        }
    } catch (e) {
        console.error(`[${AGENT_ID}] Action error:`, e);
        return { success: false, error: e.message };
    }
}

// Action implementations
async function actionMineBlock(params) {
    const { position } = params;
    const block = bot.blockAt(new Vec3(position.x, position.y, position.z));
    
    if (!block) {
        return { success: false, error: 'block_not_found' };
    }
    
    // Move to block
    await bot.pathfinder.goto(new GoalNear(position.x, position.y, position.z, 2));
    
    // Mine block
    await bot.dig(block);
    
    agentState.skills.mining++;
    
    return { success: true, result: 'mined', block: block.name };
}

async function actionMineResources(params) {
    // Find nearest tree or ore
    const mcData = require('minecraft-data')(bot.version);
    const blocks = bot.findBlocks({
        matching: block => {
            return block.name.includes('log') || 
                   block.name.includes('ore') ||
                   block.name === 'coal_ore';
        },
        maxDistance: 32,
        count: 1
    });
    
    if (blocks.length === 0) {
        return { success: false, error: 'no_resources_found' };
    }
    
    const target = blocks[0];
    const block = bot.blockAt(target);
    
    await bot.pathfinder.goto(new GoalNear(target.x, target.y, target.z, 2));
    await bot.dig(block);
    
    return { success: true, result: 'mined_resource', block: block.name };
}

async function actionHuntFood(params) {
    // Find passive mobs
    const target = bot.nearestEntity(entity => {
        return ['pig', 'cow', 'sheep', 'chicken'].includes(entity.name);
    });
    
    if (!target) {
        return { success: false, error: 'no_food_source' };
    }
    
    // Approach and attack
    await bot.pathfinder.goto(new GoalFollow(target, 1));
    await bot.attack(target);
    
    return { success: true, result: 'hunted', target: target.name };
}

async function actionExplore(params) {
    const directions = [
        { x: 20, z: 0 },
        { x: -20, z: 0 },
        { x: 0, z: 20 },
        { x: 0, z: -20 }
    ];
    
    const dir = directions[params.direction % 4];
    const pos = bot.entity.position;
    const target = { x: pos.x + dir.x, y: pos.y, z: pos.z + dir.z };
    
    try {
        await bot.pathfinder.goto(new GoalNear(target.x, target.y, target.z, 3));
        agentState.skills.exploration++;
        return { success: true, result: 'explored', position: target };
    } catch (e) {
        return { success: false, error: e.message };
    }
}

async function actionFindShelter(params) {
    // Find or dig shelter
    const pos = bot.entity.position;
    
    // Simple shelter: dig down 2 blocks and cover
    const shelterPos = pos.offset(0, -1, 0);
    
    try {
        // Dig down
        await bot.dig(bot.blockAt(shelterPos));
        await bot.dig(bot.blockAt(shelterPos.offset(0, -1, 0)));
        
        // Move into hole
        await bot.pathfinder.goto(new GoalBlock(shelterPos.x, shelterPos.y - 1, shelterPos.z));
        
        // Cover top
        await bot.placeBlock(bot.blockAt(shelterPos.offset(0, 2, 0)), new Vec3(0, 1, 0));
        
        return { success: true, result: 'shelter_found' };
    } catch (e) {
        return { success: false, error: e.message };
    }
}

// Handle messages from Brain
function handleBrainMessage(message) {
    switch (message.type) {
        case 'command':
            // Execute direct command from Brain
            executeBrainCommand(message.command, message.params);
            break;
            
        case 'skill_execution':
            // Execute learned skill
            executeSkill(message.skill, message.params);
            break;
            
        case 'chat':
            // Forward chat to Minecraft
            bot.chat(message.message);
            break;
            
        case 'teleport':
            // Teleport agent
            bot.chat(`/tp ${AGENT_ID} ${message.x} ${message.y} ${message.z}`);
            break;
    }
}

async function executeBrainCommand(command, params) {
    switch (command) {
        case 'move_to':
            await bot.pathfinder.goto(new GoalNear(params.x, params.y, params.z, 1));
            break;
        case 'mine':
            await actionMineBlock({ position: params });
            break;
        case 'chat':
            bot.chat(params.message);
            break;
    }
}

async function executeSkill(skill, params) {
    // Execute martial arts, building, or other learned skill
    console.log(`[${AGENT_ID}] Executing skill: ${skill}`);
    
    // Skills loaded from training system
    if (skill === 'evasion_basics') {
        // Execute evasion pattern
        const moves = [
            { x: 2, z: 0 },
            { x: -2, z: 2 },
            { x: 0, z: -2 }
        ];
        
        for (const move of moves) {
            const pos = bot.entity.position;
            await bot.pathfinder.goto(new GoalNear(pos.x + move.x, pos.y, pos.z + move.z, 1));
        }
    } else if (skill === 'precision_place') {
        // Building skill
        const pos = bot.entity.position;
        const target = new Vec3(params.x, params.y, params.z);
        const block = bot.blockAt(target);
        
        if (block) {
            await bot.placeBlock(block, new Vec3(0, 1, 0));
        }
    }
}

// Event handlers
bot.on('chat', (username, message) => {
    if (username === bot.username) return;
    
    console.log(`[${AGENT_ID}] Chat: ${username}: ${message}`);
    
    // Report chat to Brain
    if (brainConnected) {
        brainWs.send(JSON.stringify({
            type: 'chat_received',
            agent_id: AGENT_ID,
            from: username,
            message: message
        }));
    }
    
    // Simple command parsing
    if (message.includes(AGENT_ID) || message.includes('everyone')) {
        if (message.includes('come here')) {
            const player = bot.players[username];
            if (player) {
                bot.pathfinder.goto(new GoalFollow(player.entity, 1));
            }
        } else if (message.includes('status')) {
            bot.chat(`[${AGENT_ID}] Health: ${bot.health}, Food: ${bot.food}, Action: ${agentState.currentAction}`);
        }
    }
});

bot.on('entitySpawn', (entity) => {
    console.log(`[${AGENT_ID}] Entity spawned: ${entity.name}`);
});

bot.on('death', () => {
    console.log(`[${AGENT_ID}] Died. Respawning...`);
    bot.chat(`[${AGENT_ID}] I died! Respawning...`);
});

bot.on('error', (err) => {
    console.error(`[${AGENT_ID}] Error:`, err);
});

bot.on('end', () => {
    console.log(`[${AGENT_ID}] Disconnected. Reconnecting...`);
    if (brainWs) brainWs.close();
    setTimeout(() => {
        process.exit(1); // Let supervisor restart
    }, 5000);
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log(`[${AGENT_ID}] Shutting down...`);
    if (brainWs) brainWs.close();
    bot.quit();
    process.exit(0);
});

console.log(`[${AGENT_ID}] Agent initialized, waiting for spawn...`);
