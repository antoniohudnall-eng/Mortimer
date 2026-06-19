#!/usr/bin/env node
/**
 * Simple Mineflayer Agent - Brain Connected
 * Autonomous agent with Brain OODA integration
 */

const mineflayer = require('mineflayer');
const pathfinder = require('mineflayer-pathfinder').pathfinder;
const mcData = require('minecraft-data');
const { Movements, goals } = require('mineflayer-pathfinder');
const { GoalNear, GoalFollow } = goals;
const WebSocket = require('ws');

const AGENT_ID = process.argv[2] || 'agent_' + Math.floor(Math.random() * 1000);
const MC_HOST = process.argv[3] || 'localhost';
const MC_PORT = parseInt(process.argv[4]) || 25565;
const BRAIN_URL = process.argv[5] || 'ws://localhost:8767';

console.log(`[${AGENT_ID}] Starting autonomous agent...`);

// Create bot
const bot = mineflayer.createBot({
    host: MC_HOST,
    port: MC_PORT,
    username: AGENT_ID,
    version: '1.20.4',
    auth: 'offline'
});

bot.loadPlugin(pathfinder);

// Agent state
let tick = 0;
let brainWs = null;
let brainConnected = false;

// Connect to Brain
function connectBrain() {
    console.log(`[${AGENT_ID}] Connecting to Brain at ${BRAIN_URL}`);
    
    brainWs = new WebSocket(BRAIN_URL);
    
    brainWs.on('open', () => {
        console.log(`[${AGENT_ID}] ✅ Brain connected`);
        brainConnected = true;
        
        brainWs.send(JSON.stringify({
            type: 'register_agent',
            agent_id: AGENT_ID,
            capabilities: ['mining', 'building', 'combat', 'exploration'],
            position: bot.entity ? bot.entity.position : {x: 0, y: 100, z: 0}
        }));
    });
    
    brainWs.on('message', (data) => {
        try {
            const msg = JSON.parse(data);
            handleBrainCommand(msg);
        } catch(e) {}
    });
    
    brainWs.on('close', () => {
        console.log(`[${AGENT_ID}] Brain disconnected`);
        brainConnected = false;
        setTimeout(connectBrain, 5000);
    });
    
    brainWs.on('error', (err) => {
        console.log(`[${AGENT_ID}] Brain error: ${err.message}`);
    });
}

// OODA Loop
async function oodaLoop() {
    while (true) {
        tick++;
        
        if (!bot.entity) {
            await new Promise(r => setTimeout(r, 1000));
            continue;
        }
        
        const pos = bot.entity.position;
        
        // OBSERVE
        const observation = {
            tick: tick,
            position: {x: pos.x, y: pos.y, z: pos.z},
            health: bot.health,
            food: bot.food,
            inventory: bot.inventory.items().length,
            nearby: Object.values(bot.entities).filter(e => 
                e.position && e.position.distanceTo(pos) < 10
            ).map(e => e.name)
        };
        
        // ORIENT - Simple threat/opportunity detection
        const threats = observation.nearby.filter(n => 
            ['zombie', 'skeleton', 'creeper', 'spider'].includes(n)
        );
        const opportunities = observation.nearby.filter(n =>
            ['pig', 'cow', 'sheep', 'chicken'].includes(n)
        );
        
        // DECIDE
        let action = {type: 'idle'};
        
        if (threats.length > 0 && bot.health < 10) {
            action = {type: 'flee'};
        } else if (opportunities.length > 0 && bot.food < 15) {
            action = {type: 'hunt', target: opportunities[0]};
        } else if (tick % 20 === 0) {
            // Explore every 20 ticks
            action = {type: 'explore'};
        }
        
        // ACT
        await executeAction(action, observation);
        
        // Report to Brain
        if (brainConnected) {
            brainWs.send(JSON.stringify({
                type: 'ooda_tick',
                agent_id: AGENT_ID,
                tick: tick,
                observation: observation,
                decision: action
            }));
        }
        
        await new Promise(r => setTimeout(r, 500)); // 2 Hz
    }
}

async function executeAction(action, observation) {
    const pos = bot.entity.position;
    
    switch (action.type) {
        case 'flee':
            // Move away from threats
            const fleePos = {x: pos.x + 10, y: pos.y, z: pos.z};
            bot.pathfinder.setMovements(new Movements(bot));
            bot.pathfinder.goto(new GoalNear(fleePos.x, fleePos.y, fleePos.z, 2))
                .catch(() => {});
            break;
            
        case 'hunt':
            // Find and attack food source
            const target = bot.nearestEntity(e => e.name === action.target);
            if (target) {
                bot.pathfinder.goto(new GoalNear(target.position.x, target.position.y, target.position.z, 1))
                    .then(() => bot.attack(target))
                    .catch(() => {});
            }
            break;
            
        case 'explore':
            // Random exploration
            const explorePos = {
                x: pos.x + (Math.random() - 0.5) * 20,
                y: pos.y,
                z: pos.z + (Math.random() - 0.5) * 20
            };
            bot.pathfinder.goto(new GoalNear(explorePos.x, explorePos.y, explorePos.z, 3))
                .catch(() => {});
            break;
    }
}

function handleBrainCommand(msg) {
    console.log(`[${AGENT_ID}] Brain command: ${msg.type}`);
    
    if (msg.type === 'command' && msg.command === 'move_to') {
        const p = msg.params;
        bot.pathfinder.goto(new GoalNear(p.x, p.y, p.z, 1)).catch(() => {});
    } else if (msg.type === 'broadcast') {
        bot.chat(`[${AGENT_ID}] ${msg.message}`);
    }
}

// Event handlers
bot.once('spawn', () => {
    console.log(`[${AGENT_ID}] ✅ Spawned in world at ${bot.entity.position}`);
    bot.chat(`Agent ${AGENT_ID} online!`);
    connectBrain();
    oodaLoop();
});

bot.on('chat', (username, message) => {
    if (username === bot.username) return;
    console.log(`[${AGENT_ID}] Chat: ${username}: ${message}`);
    
    if (message.includes(AGENT_ID)) {
        if (message.includes('status')) {
            bot.chat(`Health: ${bot.health}, Food: ${bot.food}, Tick: ${tick}`);
        } else if (message.includes('come')) {
            const player = bot.players[username];
            if (player) {
                bot.pathfinder.goto(new GoalNear(player.entity.position.x, player.entity.position.y, player.entity.position.z, 2))
                    .then(() => bot.chat(`Here I am, ${username}!`))
                    .catch(() => {});
            }
        }
    }
});

bot.on('death', () => {
    console.log(`[${AGENT_ID}] Died, respawning...`);
    bot.chat(`I died! Respawning...`);
});

bot.on('error', (err) => {
    console.error(`[${AGENT_ID}] Error: ${err.message}`);
});

bot.on('end', () => {
    console.log(`[${AGENT_ID}] Disconnected`);
    if (brainWs) brainWs.close();
    process.exit(0);
});

console.log(`[${AGENT_ID}] Waiting for spawn...`);