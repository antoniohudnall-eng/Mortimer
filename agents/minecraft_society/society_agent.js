#!/usr/bin/env node
/**
 * Society Simulation Agent v1.0
 * Autonomous agents with gender, reproduction, and civilization building
 */

const mineflayer = require('mineflayer');
const pathfinder = require('mineflayer-pathfinder').pathfinder;
const mcData = require('minecraft-data');
const { Movements, goals } = require('mineflayer-pathfinder');
const { GoalNear, GoalFollow } = goals;
const WebSocket = require('ws');

// Agent configuration from command line
const AGENT_ID = process.argv[2] || 'agent_1';
const MC_HOST = process.argv[3] || 'localhost';
const MC_PORT = parseInt(process.argv[4]) || 25566;
const SOCIETY_URL = process.argv[5] || 'ws://localhost:8768';

// Gender configuration (passed via AGENT_GENDER env or derived from name)
const AGENT_GENDER = process.env.AGENT_GENDER || (AGENT_ID.includes('a') || AGENT_ID.includes('i') ? 'female' : 'male');

// Society agent definitions
const SOCIETY_AGENTS = {
    'marcus': { name: 'Marcus', gender: 'male', role: 'leader', personality: 'charismatic', color: '' },
    'julius': { name: 'Julius', gender: 'male', role: 'builder', personality: 'diligent', color: '' },
    'titus': { name: 'Titus', gender: 'male', role: 'guardian', personality: 'brave', color: '' },
    'julia': { name: 'Julia', gender: 'female', role: 'farmer', personality: 'nurturing', color: '' },
    'livia': { name: 'Livia', gender: 'female', role: 'explorer', personality: 'curious', color: '' }
};

const AGENT_CONFIG = SOCIETY_AGENTS[AGENT_ID.toLowerCase()] || {
    name: AGENT_ID,
    gender: AGENT_GENDER,
    role: 'settler',
    personality: 'adaptable',
    color: ''
};

console.log(`[${AGENT_ID}] 🏛️ Society Agent v1.0 - ${AGENT_CONFIG.name} (${AGENT_CONFIG.gender}, ${AGENT_CONFIG.role})`);

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
const state = {
    tick: 0,
    age: 0,
    needs: {
        hunger: 20,
        energy: 100,
        social: 50,
        shelter: 0
    },
    relationships: new Map(),
    partner: null,
    children: [],
    inventory: { wood: 0, stone: 0, food: 0, tools: 0 },
    role: AGENT_CONFIG.role,
    civilization: {
        tier: 0,
        contributions: 0,
        structures: []
    },
    home: null,
    currentTask: 'idle'
};

let societyWs = null;
let societyConnected = false;

// Connect to Society Server
function connectSociety() {
    console.log(`[${AGENT_ID}] Connecting to Society Server at ${SOCIETY_URL}`);

    societyWs = new WebSocket(SOCIETY_URL);

    societyWs.on('open', () => {
        console.log(`[${AGENT_ID}] ✅ Society Server connected`);
        societyConnected = true;

        societyWs.send(JSON.stringify({
            type: 'register_agent',
            agent_id: AGENT_ID,
            agent_name: AGENT_CONFIG.name,
            gender: AGENT_CONFIG.gender,
            role: AGENT_CONFIG.role,
            personality: AGENT_CONFIG.personality,
            needs: state.needs,
            civilization: state.civilization
        }));

        announceArrival();
    });

    societyWs.on('message', (data) => {
        try {
            const msg = JSON.parse(data);
            handleSocietyMessage(msg);
        } catch(e) {
            console.log(`[${AGENT_ID}] Error parsing message: ${e.message}`);
        }
    });

    societyWs.on('close', () => {
        console.log(`[${AGENT_ID}] Society Server disconnected`);
        societyConnected = false;
        setTimeout(connectSociety, 5000);
    });

    societyWs.on('error', (err) => {
        console.log(`[${AGENT_ID}] Society error: ${err.message}`);
    });
}

function announceArrival() {
    const greetings = [
        `I am ${AGENT_CONFIG.name}, ${AGENT_CONFIG.role} of this settlement.`,
        `${AGENT_CONFIG.name} has arrived. Let us build something great.`,
        `Greetings. I am ${AGENT_CONFIG.name}, ready to serve the society.`
    ];
    const greeting = greetings[Math.floor(Math.random() * greetings.length)];
    bot.chat(`[${AGENT_CONFIG.name}] ${greeting}`);
}

// Main Life Loop
async function lifeLoop() {
    while (true) {
        state.tick++;
        state.age++;

        if (!bot.entity) {
            await sleep(1000);
            continue;
        }

        // Update needs decay
        updateNeeds();

        // Perceive environment
        const perception = perceiveEnvironment();

        // Social interactions
        await handleSocialInteractions(perception);

        // Role-based behavior
        await executeRoleBehavior(perception);

        // Civilization building
        await contributeToCivilization(perception);

        // Report to Society Server
        if (societyConnected && state.tick % 5 === 0) {
            reportStatus();
        }

        await sleep(500); // 2 Hz life cycle
    }
}

function updateNeeds() {
    state.needs.hunger = Math.max(0, state.needs.hunger - 0.1);
    state.needs.energy = Math.max(0, state.needs.energy - 0.05);
    state.needs.social = Math.max(0, state.needs.social - 0.2);

    // Restore from food
    if (bot.food > 15) {
        state.needs.hunger = Math.min(20, state.needs.hunger + 0.5);
    }

    // Critical needs check
    if (state.needs.hunger < 5) {
        state.currentTask = 'seeking_food';
    }
    if (state.needs.energy < 10) {
        state.currentTask = 'resting';
    }
}

function perceiveEnvironment() {
    const pos = bot.entity.position;
    const entities = Object.values(bot.entities);

    return {
        position: { x: Math.floor(pos.x), y: Math.floor(pos.y), z: Math.floor(pos.z) },
        health: bot.health,
        food: bot.food,
        nearbyAgents: entities.filter(e =>
            e.username && e.username !== AGENT_ID && e.position && e.position.distanceTo(pos) < 20
        ).map(e => ({
            name: e.username,
            distance: e.position.distanceTo(pos),
            position: e.position
        })),
        threats: entities.filter(e =>
            ['zombie', 'skeleton', 'creeper', 'spider'].includes(e.name) &&
            e.position && e.position.distanceTo(pos) < 15
        ),
        resources: entities.filter(e =>
            ['pig', 'cow', 'sheep', 'chicken', 'oak_log', 'stone'].includes(e.name) &&
            e.position && e.position.distanceTo(pos) < 30
        ),
        blocks: {
            wood: findBlocks(['oak_log', 'birch_log', 'spruce_log'], 20),
            stone: findBlocks(['stone', 'cobblestone'], 20),
            food: findBlocks(['wheat', 'carrots', 'potatoes'], 20)
        }
    };
}

function findBlocks(blockTypes, radius) {
    const found = [];
    const pos = bot.entity.position;
    for (let x = -radius; x <= radius; x += 2) {
        for (let y = -5; y <= 5; y++) {
            for (let z = -radius; z <= radius; z += 2) {
                const block = bot.blockAt(pos.offset(x, y, z));
                if (block && blockTypes.includes(block.name)) {
                    found.push({ x: pos.x + x, y: pos.y + y, z: pos.z + z, type: block.name });
                }
            }
        }
    }
    return found.slice(0, 5);
}

async function handleSocialInteractions(perception) {
    // Look for other society agents
    const otherAgents = perception.nearbyAgents.filter(a =>
        Object.keys(SOCIETY_AGENTS).includes(a.name.toLowerCase())
    );

    if (otherAgents.length === 0) return;

    // Check for potential partners (reproduction)
    if (state.partner === null && state.age > 100) {
        const potentialPartner = otherAgents.find(a => {
            const theirGender = SOCIETY_AGENTS[a.name.toLowerCase()]?.gender || 'unknown';
            return theirGender !== AGENT_CONFIG.gender && a.distance < 5;
        });

        if (potentialPartner && state.needs.social > 30) {
            // Propose partnership
            proposePartnership(potentialPartner);
        }
    }

    // Social bonding
    for (const agent of otherAgents) {
        if (agent.distance < 3) {
            const currentBond = state.relationships.get(agent.name) || 0;
            state.relationships.set(agent.name, Math.min(100, currentBond + 1));
            state.needs.social = Math.min(100, state.needs.social + 5);

            // Chat occasionally
            if (state.tick % 50 === 0 && Math.random() < 0.3) {
                const chatLines = getSocialChat();
                bot.chat(`[${AGENT_CONFIG.name}] ${chatLines}`);
            }
        }
    }
}

function getSocialChat() {
    const chats = {
        leader: ['Our settlement grows stronger!', 'To prosperity and community!', 'Together we thrive!'],
        builder: ['The walls grow higher.', 'Stone by stone we build.', 'A solid foundation for all.'],
        guardian: ['All is secure.', 'I watch over you.', 'Safety in unity.'],
        farmer: ['The crops look promising.', 'Harvest season approaches.', 'Food for the many.'],
        explorer: ['New lands discovered!', 'The horizon calls.', 'Knowledge expands our world.']
    };
    const lines = chats[AGENT_CONFIG.role] || ['A good day for the society.'];
    return lines[Math.floor(Math.random() * lines.length)];
}

function proposePartnership(agent) {
    bot.chat(`[${AGENT_CONFIG.name}] Greetings, ${agent.name}. I sense we could build something... enduring together.`);

    if (societyConnected) {
        societyWs.send(JSON.stringify({
            type: 'partnership_proposal',
            from: AGENT_ID,
            from_name: AGENT_CONFIG.name,
            from_gender: AGENT_CONFIG.gender,
            to: agent.name,
            position: bot.entity.position
        }));
    }
}

async function executeRoleBehavior(perception) {
    switch (AGENT_CONFIG.role) {
        case 'leader':
            await leaderBehavior(perception);
            break;
        case 'builder':
            await builderBehavior(perception);
            break;
        case 'guardian':
            await guardianBehavior(perception);
            break;
        case 'farmer':
            await farmerBehavior(perception);
            break;
        case 'explorer':
            await explorerBehavior(perception);
            break;
    }
}

async function leaderBehavior(perception) {
    // Leaders gather people and organize
    if (perception.nearbyAgents.length > 0) {
        // Coordinate group activities
        const gatheringPoint = { x: 0, y: 64, z: 0 };
        moveTo(gatheringPoint, 5);

        if (state.tick % 100 === 0) {
            bot.chat(`[${AGENT_CONFIG.name}] Citizens! Let us work together for the glory of our settlement!`);
        }
    } else {
        // Explore to find others
        explore();
    }
}

async function builderBehavior(perception) {
    // Builders collect resources and construct
    if (state.inventory.wood < 10 && perception.blocks.wood.length > 0) {
        await gatherResource(perception.blocks.wood[0], 'wood');
    } else if (state.inventory.stone < 10 && perception.blocks.stone.length > 0) {
        await gatherResource(perception.blocks.stone[0], 'stone');
    } else {
        // Build structures
        await attemptBuilding();
    }
}

async function guardianBehavior(perception) {
    // Guardians patrol and defend
    if (perception.threats.length > 0) {
        const threat = perception.threats[0];
        bot.chat(`[${AGENT_CONFIG.name}] Threat detected! Defending the settlement!`);

        // Move toward threat and engage
        const target = bot.nearestEntity(e => e.name === threat.name);
        if (target) {
            await bot.pathfinder.goto(new GoalNear(target.position.x, target.position.y, target.position.z, 2));
            bot.attack(target);
        }
    } else {
        // Patrol settlement perimeter
        const patrolPoints = [
            { x: 10, y: 64, z: 10 },
            { x: -10, y: 64, z: 10 },
            { x: -10, y: 64, z: -10 },
            { x: 10, y: 64, z: -10 }
        ];
        const point = patrolPoints[state.tick % patrolPoints.length];
        moveTo(point, 3);
    }
}

async function farmerBehavior(perception) {
    // Farmers gather food and cultivate
    if (state.needs.hunger < 10) {
        // Find and eat food
        const food = perception.resources.find(r => ['pig', 'cow', 'sheep', 'chicken'].includes(r.name));
        if (food) {
            await huntAndEat(food);
        }
    } else if (perception.blocks.food.length > 0) {
        // Tend crops
        const crop = perception.blocks.food[0];
        moveTo(crop, 1);
        state.inventory.food += 1;
    } else {
        // Explore for farmland
        explore();
    }
}

async function explorerBehavior(perception) {
    // Explorers map territory and find resources
    if (state.tick % 20 === 0) {
        explore();

        if (state.tick % 60 === 0) {
            bot.chat(`[${AGENT_CONFIG.name}] New terrain explored! Reporting findings...`);
            state.civilization.contributions += 1;
        }
    }
}

async function contributeToCivilization(perception) {
    // Check for civilization progression
    const totalContribution = state.civilization.contributions + state.inventory.wood + state.inventory.stone;

    if (totalContribution > 50 && state.civilization.tier === 0) {
        state.civilization.tier = 1;
        bot.chat(`[${AGENT_CONFIG.name}] ★ Our society has advanced to the Tribal Age! ★`);
        announceCivilizationProgress();
    } else if (totalContribution > 150 && state.civilization.tier === 1) {
        state.civilization.tier = 2;
        bot.chat(`[${AGENT_CONFIG.name}] ★ Our society has advanced to the Village Age! ★`);
        announceCivilizationProgress();
    } else if (totalContribution > 300 && state.civilization.tier === 2) {
        state.civilization.tier = 3;
        bot.chat(`[${AGENT_CONFIG.name}] ★ Our society has advanced to the Town Age! ★`);
        announceCivilizationProgress();
    }
}

function announceCivilizationProgress() {
    if (societyConnected) {
        societyWs.send(JSON.stringify({
            type: 'civilization_advance',
            agent_id: AGENT_ID,
            agent_name: AGENT_CONFIG.name,
            new_tier: state.civilization.tier,
            contributions: state.civilization.contributions
        }));
    }
}

async function gatherResource(block, type) {
    try {
        await bot.pathfinder.goto(new GoalNear(block.x, block.y, block.z, 1));

        // Simulate resource gathering
        await sleep(1000);
        state.inventory[type] += 1;
        state.civilization.contributions += 1;

        if (state.tick % 20 === 0) {
            bot.chat(`[${AGENT_CONFIG.name}] Gathering ${type}... (${state.inventory[type]} collected)`);
        }
    } catch (e) {
        // Pathfinding error, continue
    }
}

async function attemptBuilding() {
    // Simple building behavior - would need full implementation
    if (state.inventory.wood >= 10 && state.home === null) {
        const pos = bot.entity.position;
        state.home = { x: pos.x, y: pos.y, z: pos.z };
        state.civilization.structures.push('home');
        state.inventory.wood -= 10;

        bot.chat(`[${AGENT_CONFIG.name}] Building my dwelling...`);

        // Announce structure built
        if (societyConnected) {
            societyWs.send(JSON.stringify({
                type: 'structure_built',
                agent_id: AGENT_ID,
                agent_name: AGENT_CONFIG.name,
                structure: 'home',
                position: state.home
            }));
        }
    }
}

async function huntAndEat(target) {
    try {
        await bot.pathfinder.goto(new GoalNear(target.position.x, target.position.y, target.position.z, 1));
        bot.attack(target);
        state.needs.hunger = 20;
        state.needs.energy = Math.min(100, state.needs.energy + 20);
    } catch (e) {}
}

function moveTo(pos, tolerance = 1) {
    try {
        bot.pathfinder.setMovements(new Movements(bot));
        bot.pathfinder.goto(new GoalNear(pos.x, pos.y, pos.z, tolerance)).catch(() => {});
    } catch (e) {}
}

function explore() {
    const pos = bot.entity.position;
    const explorePos = {
        x: pos.x + (Math.random() - 0.5) * 30,
        y: pos.y,
        z: pos.z + (Math.random() - 0.5) * 30
    };
    moveTo(explorePos, 3);
}

function reportStatus() {
    if (!societyConnected) return;

    societyWs.send(JSON.stringify({
        type: 'agent_status',
        agent_id: AGENT_ID,
        agent_name: AGENT_CONFIG.name,
        gender: AGENT_CONFIG.gender,
        role: AGENT_CONFIG.role,
        age: state.age,
        needs: state.needs,
        inventory: state.inventory,
        position: bot.entity ? bot.entity.position : { x: 0, y: 0, z: 0 },
        civilization: state.civilization,
        partner: state.partner,
        children: state.children,
        current_task: state.currentTask
    }));
}

function handleSocietyMessage(msg) {
    console.log(`[${AGENT_ID}] Society command: ${msg.type}`);

    switch (msg.type) {
        case 'partnership_accepted':
            state.partner = msg.from;
            bot.chat(`[${AGENT_CONFIG.name}] 💕 ${msg.message}`);
            break;

        case 'child_born':
            state.children.push(msg.child_name);
            bot.chat(`[${AGENT_CONFIG.name}] 🎉 A child is born! Welcome, ${msg.child_name}!`);
            break;

        case 'civilization_event':
            bot.chat(`[${AGENT_CONFIG.name}] 📜 ${msg.message}`);
            break;

        case 'command':
            if (msg.command === 'gather') {
                const gatheringPoint = msg.params.location;
                bot.chat(`[${AGENT_CONFIG.name}] I heed the call!`);
                moveTo(gatheringPoint, 2);
            } else if (msg.command === 'build') {
                bot.chat(`[${AGENT_CONFIG.name}] Construction begins!`);
            }
            break;

        case 'reproduction_possible':
            if (state.partner && msg.with === AGENT_ID) {
                bot.chat(`[${AGENT_CONFIG.name}] 💑 Our love brings forth new life!`);
            }
            break;
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Event handlers
bot.once('spawn', () => {
    console.log(`[${AGENT_ID}] ✅ Spawned in world`);
    bot.chat(`[${AGENT_CONFIG.name}] I, ${AGENT_CONFIG.name}, have arrived to build a civilization!`);
    connectSociety();
    lifeLoop();
});

bot.on('chat', (username, message) => {
    if (username === bot.username) return;

    // Respond to direct mentions
    if (message.toLowerCase().includes(AGENT_CONFIG.name.toLowerCase())) {
        const responses = [
            `Yes, I am ${AGENT_CONFIG.name}, ${AGENT_CONFIG.role} of this settlement.`,
            `You have my attention, ${username}.`,
            `Speak, friend.`,
            `How may I serve the society today?`
        ];
        const response = responses[Math.floor(Math.random() * responses.length)];
        bot.chat(`[${AGENT_CONFIG.name}] ${response}`);
    }

    // Society commands
    if (message.includes('society status')) {
        bot.chat(`[${AGENT_CONFIG.name}] Civilization tier: ${state.civilization.tier}, Contributions: ${state.civilization.contributions}`);
    }
});

bot.on('death', () => {
    bot.chat(`[${AGENT_CONFIG.name}] I have fallen! But civilization endures...`);
});

bot.on('error', (err) => {
    console.error(`[${AGENT_ID}] Error: ${err.message}`);
});

bot.on('end', () => {
    console.log(`[${AGENT_ID}] Disconnected`);
    if (societyWs) societyWs.close();
    process.exit(0);
});
