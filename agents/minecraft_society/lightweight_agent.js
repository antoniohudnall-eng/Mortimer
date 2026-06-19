#!/usr/bin/env node
/**
 * Ultra-lightweight agent for high-density spawning
 */

const mineflayer = require('mineflayer');

const AGENT_ID = process.argv[2] || 'light_agent';

console.log(`[${AGENT_ID}] Starting lightweight agent...`);

const bot = mineflayer.createBot({
    host: 'localhost',
    port: 25566,
    username: AGENT_ID,
    version: '1.20.4',
    auth: 'offline'
});

let tick = 0;

bot.once('spawn', () => {
    console.log(`[${AGENT_ID}] Spawned!`);
    bot.chat(`${AGENT_ID} online!`);
    
    // Simplified loop - just stay alive
    setInterval(() => {
        tick++;
        if (tick % 10 === 0) {
            // Move slightly every 10 seconds
            bot.setControlState('forward', true);
            setTimeout(() => bot.setControlState('forward', false), 1000);
        }
    }, 1000);
});

bot.on('error', () => {});
bot.on('end', () => process.exit(0));