#!/usr/bin/env node

/**
 * N'og nog Crew - Brain Bridge
 * Socket interface between crew system and AOS brain
 */

const net = require('net');
const fs = require('fs');

const CREW_SOCKET = '/tmp/nognog_crew.sock';
const BRAIN_SOCKET = '/tmp/aos_brain.sock';

// Remove old socket
if (fs.existsSync(CREW_SOCKET)) {
    fs.unlinkSync(CREW_SOCKET);
}

const server = net.createServer((socket) => {
    console.log('[CrewBridge] Client connected');
    
    socket.on('data', (data) => {
        try {
            const cmd = JSON.parse(data.toString());
            handleCommand(cmd, socket);
        } catch (err) {
            socket.write(JSON.stringify({ error: 'Invalid JSON' }) + '\n');
        }
    });
    
    socket.on('end', () => {
        console.log('[CrewBridge] Client disconnected');
    });
});

async function handleCommand(cmd, socket) {
    switch(cmd.cmd) {
        case 'status':
            // Forward to crew system
            socket.write(JSON.stringify({
                crew: 'active',
                socket: CREW_SOCKET,
                timestamp: Date.now()
            }) + '\n');
            break;
            
        case 'report':
            socket.write(JSON.stringify({
                type: 'report_requested',
                timestamp: Date.now()
            }) + '\n');
            break;
            
        case 'brain':
            // Forward to brain
            forwardToBrain(cmd, socket);
            break;
            
        default:
            socket.write(JSON.stringify({ error: 'Unknown command' }) + '\n');
    }
}

function forwardToBrain(cmd, socket) {
    const brainClient = net.createConnection(BRAIN_SOCKET);
    
    brainClient.on('connect', () => {
        brainClient.write(JSON.stringify(cmd.params) + '\n');
    });
    
    brainClient.on('data', (data) => {
        socket.write(data);
    });
    
    brainClient.on('error', (err) => {
        socket.write(JSON.stringify({ error: 'Brain unavailable', details: err.message }) + '\n');
    });
}

server.listen(CREW_SOCKET, () => {
    console.log('[CrewBridge] Listening on', CREW_SOCKET);
});

// Handle shutdown
process.on('SIGINT', () => {
    console.log('[CrewBridge] Shutting down...');
    server.close();
    if (fs.existsSync(CREW_SOCKET)) {
        fs.unlinkSync(CREW_SOCKET);
    }
    process.exit(0);
});
