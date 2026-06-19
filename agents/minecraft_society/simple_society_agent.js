#!/usr/bin/env node
/**
 * Simple Society Agent - Stable Version
 * Basic mineflayer agent for society members
 */

const mineflayer = require('mineflayer');
const pathfinder = require('mineflayer-pathfinder').pathfinder;
const { Movements } = require('mineflayer-pathfinder');

// Agent config
const AGENT_ID = process.argv[2] || 'agent_1';
const MC_HOST = process.argv[3] || 'localhost';
const MC_PORT = parseInt(process.argv[4]) || 25565;

const AGENTS = {
  'marcus': { name: 'Marcus', role: 'leader', color: '' },
  'julius': { name: 'Julius', role: 'builder', color: '' },
  'titus': { name: 'Titus', role: 'guardian', color: '' },
  'julia': { name: 'Julia', role: 'farmer', color: '' },
  'livia': { name: 'Livia', role: 'explorer', color: '' }
};

const config = AGENTS[AGENT_ID.toLowerCase()] || { name: AGENT_ID, role: 'settler', color: '' };

console.log(`[${AGENT_ID}] Society Agent - ${config.name} (${config.role})`);
console.log(`[${AGENT_ID}] Connecting to ${MC_HOST}:${MC_PORT}...`);

// Create bot
const bot = mineflayer.createBot({
  host: MC_HOST,
  port: MC_PORT,
  username: AGENT_ID,
  version: '1.20.4',
  auth: 'offline'
});

bot.loadPlugin(pathfinder);

// State
let tick = 0;
let state = 'idle';

// Spawn handler
bot.once('spawn', () => {
  console.log(`[${AGENT_ID}] ✅ Spawned!`);
  bot.chat(`[${config.name}] Online and ready.`);
  
  const mcData = require('minecraft-data')(bot.version);
  const movements = new Movements(bot, mcData);
  bot.pathfinder.setMovements(movements);
  
  // Start simple behavior loop
  setInterval(() => behaviorTick(), 5000);
});

// Simple behavior
function behaviorTick() {
  tick++;
  
  // Random movement
  if (tick % 3 === 0 && bot.entity) {
    const x = bot.entity.position.x + (Math.random() - 0.5) * 10;
    const z = bot.entity.position.z + (Math.random() - 0.5) * 10;
    const y = bot.entity.position.y;
    
    try {
      bot.pathfinder.setGoal(new (require('mineflayer-pathfinder').goals.GoalNear)(x, y, z, 1));
    } catch(e) {
      // Silent fail for movement
    }
  }
  
  // Occasional chat
  if (tick % 12 === 0) {
    const messages = [
      `Reporting in.`,
      `Standing by.`,
      `All systems nominal.`,
      `Tick ${tick}.`
    ];
    bot.chat(messages[Math.floor(Math.random() * messages.length)]);
  }
}

// Error handlers
bot.on('error', (err) => {
  if (err.message && err.message.includes('ECONNREFUSED')) {
    console.log(`[${AGENT_ID}] ❌ Connection refused - retrying...`);
  } else {
    console.log(`[${AGENT_ID}] Error: ${err.message || err}`);
  }
});

bot.on('kicked', (reason) => {
  console.log(`[${AGENT_ID}] Kicked: ${reason}`);
});

bot.on('death', () => {
  console.log(`[${AGENT_ID}] Died - respawning...`);
  bot.chat(`Ouch! Respawning...`);
});

bot.on('end', () => {
  console.log(`[${AGENT_ID}] Disconnected.`);
  process.exit(0);
});

console.log(`[${AGENT_ID}] Agent initialized.`);
