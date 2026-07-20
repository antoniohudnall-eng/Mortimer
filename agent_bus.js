/**
 * SEED3 Agent Message Bus
 * Simple pub/sub for agent-to-agent communication
 */

import fs from 'fs/promises';
import path from 'path';

const BUS_DIR = process.env.HOME + '/mortimer/agent_bus';
const INBOX = BUS_DIR + '/inbox';
const OUTBOX = BUS_DIR + '/outbox';

// Ensure directories exist
async function init() {
  await fs.mkdir(BUS_DIR, { recursive: true });
  await fs.mkdir(INBOX, { recursive: true });
  await fs.mkdir(OUTBOX, { recursive: true });
}

// Send message to an agent
async function send(to, message) {
  await init();
  const msg = {
    id: Date.now() + '-' + Math.random().toString(36).slice(2),
    from: message.from || 'system',
    to,
    type: message.type || 'INFO',
    payload: message.payload || message,
    timestamp: Date.now()
  };
  await fs.writeFile(
    path.join(INBOX, `${to}-${msg.id}.json`),
    JSON.stringify(msg, null, 2)
  );
  return msg;
}

// Check inbox for agent
async function checkInbox(agentName) {
  await init();
  const files = await fs.readdir(INBOX);
  const messages = [];
  for (const file of files) {
    if (file.startsWith(agentName + '-')) {
      const content = await fs.readFile(path.join(INBOX, file), 'utf-8');
      messages.push(JSON.parse(content));
      await fs.unlink(path.join(INBOX, file));
    }
  }
  return messages;
}

// List messages (peek without consuming)
async function peekInbox(agentName) {
  await init();
  const files = await fs.readdir(INBOX);
  const messages = [];
  for (const file of files) {
    if (file.startsWith(agentName + '-')) {
      const content = await fs.readFile(path.join(INBOX, file), 'utf-8');
      messages.push(JSON.parse(content));
    }
  }
  return messages;
}

// Broadcast to all
async function broadcast(from, message) {
  const agents = ['jordan', 'patricia', 'forge', 'r2d2', 'c3p0'];
  const results = [];
  for (const agent of agents) {
    if (agent !== from) {
      results.push(await send(agent, { ...message, from }));
    }
  }
  return results;
}

export { send, checkInbox, peekInbox, broadcast, init };
