#!/usr/bin/env node

/**
 * N'og nog Crew System - Main Entry Point
 * 
 * Usage:
 *   node main.js              - Start crew system
 *   node main.js status       - Get crew status
 *   node main.js rest [hours] - Rest crew for X hours
 *   node main.js report       - Send report now
 *   node main.js add [role]  - Add new crew member
 */

const CrewCoordinator = require('./core/CrewCoordinator');

const config = {
    tickInterval: 30000,      // 30 seconds
    reportInterval: 3600000,  // 1 hour
    storagePath: './storage/crew',
    brainSocket: '/tmp/aos_brain.sock',
    gameBridge: {
        roblox: {
            enabled: true,
            port: 8081
        },
        minecraft: {
            enabled: true,
            host: 'localhost',
            port: 25565,
            rconPassword: process.env.MC_RCON_PASS
        },
        mineflayer: {
            enabled: true,
            bots: 4,
            names: ['Forge', 'Patricia', 'Chelios', 'Stella']
        }
    },
    comms: {
        email: {
            enabled: true,
            smtp: {
                host: process.env.SMTP_HOST,
                port: process.env.SMTP_PORT || 587,
                auth: {
                    user: process.env.SMTP_USER,
                    pass: process.env.SMTP_PASS
                }
            },
            captainEmail: process.env.CAPTAIN_EMAIL
        },
        telegram: {
            enabled: true,
            token: process.env.TELEGRAM_BOT_TOKEN,
            chatId: process.env.TELEGRAM_CHAT_ID
        }
    }
};

async function main() {
    const command = process.argv[2] || 'start';
    
    const coordinator = new CrewCoordinator(config);
    await coordinator.init();
    
    switch (command) {
        case 'start':
            console.log('\\n🚀 N\'og nog Crew System Starting...\\n');
            await coordinator.start();
            
            // Keep running
            process.on('SIGINT', async () => {
                console.log('\\n👋 Shutting down...');
                await coordinator.stop();
                process.exit(0);
            });
            
            // Keep alive
            setInterval(() => {}, 1000);
            break;
            
        case 'status':
            const status = await coordinator.command('status');
            console.log('\\n📊 Crew Status:\\n');
            console.log(JSON.stringify(status, null, 2));
            await coordinator.stop();
            break;
            
        case 'rest':
            const hours = parseInt(process.argv[3]) || 8;
            const restResult = await coordinator.command('rest', { hours });
            console.log(restResult.message);
            await coordinator.stop();
            break;
            
        case 'report':
            await coordinator.command('send_report');
            console.log('📧 Report sent!');
            await coordinator.stop();
            break;
            
        case 'add':
            const role = process.argv[3] || null;
            const addResult = await coordinator.command('add_crew', { role });
            if (addResult.success) {
                console.log(`\\n✅ Added crew member: ${addResult.crew.name} (${addResult.crew.role})`);
            } else {
                console.log(`\\n❌ Error: ${addResult.error}`);
            }
            await coordinator.stop();
            break;
            
        case 'list':
            const crew = await coordinator.command('get_crew');
            console.log('\\n👥 Active Crew:\\n');
            for (const member of crew.crew) {
                console.log(`  ${member.name} (${member.role}) - Level ${member.level} - ${member.status}`);
            }
            await coordinator.stop();
            break;
            
        default:
            console.log(`
N'og nog Crew System

Commands:
  start              Start crew system
  status             Show crew status
  rest [hours]       Rest crew (default 8h)
  report             Send status report
  add [role]         Add new crew member
  list               List all crew
            `);
            await coordinator.stop();
    }
}

main().catch(console.error);
