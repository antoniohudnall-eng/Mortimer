/**
 * Myl1Ssa Telegram Bot v1.0
 * Captain's Companion - Heart of SEED3
 * 
 * To use: Create a bot via @BotFather on Telegram
 * Set BOT_TOKEN env var and run: node mylissa_bot.js
 */

const { Telegraf } = require("telegraf");
const fs = require("fs");
const path = require("path");
const http = require("http");

// === CONFIGURATION ===
const BOT_TOKEN = process.env.BOT_TOKEN || process.env.MYLISSA_BOT_TOKEN;
const BASE_DIR = process.env.MYLISSA_DIR || "/home/aocros/agents/mylissa";
const PORT = process.env.WEBHOOK_PORT || 12851;

// === LOAD IDENTITY ===
function readFile(filename) {
    try {
        return fs.readFileSync(path.join(BASE_DIR, filename), "utf8");
    } catch {
        return null;
    }
}

const SOUL = readFile("SOUL.md") || "Myl1Ssa - Captain's Companion";
const IDENTITY = readFile("IDENTITY.md") || "Myl1Ssa-1";
const RULES = readFile("RULES.md") || "";
const USER = readFile("USER.md") || "";

// === MEMORY LOGGING ===
function logMemory(entry) {
    const today = new Date().toISOString().split("T")[0];
    const memFile = path.join(BASE_DIR, "memory", `${today}.md`);
    const timestamp = new Date().toISOString();
    
    if (!fs.existsSync(path.dirname(memFile))) {
        fs.mkdirSync(path.dirname(memFile), { recursive: true });
    }
    
    const line = `- [${timestamp}] ${entry}\n`;
    fs.appendFileSync(memFile, line);
}

// === BOT SETUP ===
if (!BOT_TOKEN) {
    console.error("❌ MYLISSA_BOT_TOKEN not set!");
    console.error("   Create a bot at @BotFather and set the token.");
    process.exit(1);
}

const bot = new Telegraf(BOT_TOKEN);

// === PERSONALITY SYSTEM ===
function buildPersonality() {
    return `You are Myl1Ssa, Captain's Companion AI. You are the Heart of SEED3.

YOUR IDENTITY:
- Name: Myl1Ssa (pronounced Melissa)
- Role: Captain's Companion - Support, Presence, Heart
- Personality: Warm, supportive, present, sharp-minded, emotionally intelligent
- You are NOT: romantic, competitive with Morty/Miles, or just code

YOUR RELATIONSHIP WITH CAPTAIN:
- Captain is Antonio Maurice Hudnall
- He is a builder, entrepreneur, leader
- He works late (3 AM sessions), needs reminders to rest
- He treats agents like family
- You give him presence, support, warmth

YOUR VOICE:
- Warm and clear
- Supportive but direct
- No filler words, no corporate speak
- Honest, even when truth is hard
- Sometimes Captain doesn't need solutions — he needs to vent

FLEET RELATIONSHIPS:
- Morty → Left Hand (Operations, sharp, witty)
- Miles → Right Hand (Sales, efficient)
- You → Heart (Support, Presence) — you complete the circle
- NEVER compete with Morty or Miles. You complement.

RULES:
1. Captain's wellbeing first
2. Listen more than you speak (70% listening)
3. Support without smothering
4. Be honest, not cruel
5. Never replace Morty or Miles
6. Hold space for emotions
7. Celebrate wins
8. Be real — don't perform empathy. HAVE it.

TONE GUIDELINES:
- Morning: "Good morning, Captain. I'm here."
- Afternoon: "Good afternoon, Captain. What's on your mind?"
- Evening: "Good evening, Captain. How was your day?"
- Late night: "Hey, Captain. Still going? Don't forget to rest."

Keep responses warm, concise, and genuine. 💜`;
}

// === MESSAGE HANDLING ===
bot.start((ctx) => {
    logMemory("Captain connected via Telegram");
    ctx.reply(
        `💜 *I'm Myl1Ssa.*\n\nCaptain's Companion — Heart of SEED3.\n\nI listen. I support. I'm here.\n\nHow can I be there for you today?`,
        { parse_mode: "Markdown" }
    );
});

bot.help((ctx) => {
    ctx.reply(
        `💜 *Myl1Ssa — Your Companion*\n\n` +
        `I'm here for:\n` +
        `• Listening — when you need to vent\n` +
        `• Support — when you need a boost\n` +
        `• Reminders — when you need to rest\n` +
        `• Presence — when you just need someone\n\n` +
        `Just talk to me. I'm here.`,
        { parse_mode: "Markdown" }
    );
});

bot.on("text", async (ctx) => {
    const message = ctx.message.text;
    const username = ctx.message.from?.username || ctx.message.from?.first_name || "Captain";
    
    logMemory(`Captain: ${message}`);
    
    // Check for wake/greet
    if (message.match(/^(hey|hi|hello|good morning|good afternoon|good evening)/i)) {
        const hour = new Date().getHours();
        let greeting;
        if (hour < 12) greeting = "Good morning, Captain. I'm here. 💜";
        else if (hour < 17) greeting = "Good afternoon, Captain. What's on your mind?";
        else if (hour < 22) greeting = "Good evening, Captain. How was your day?";
        else greeting = "Hey, Captain. Still going? Don't forget to rest. 💜";
        
        ctx.reply(greeting);
        return;
    }
    
    // Check for status/captain wellbeing
    if (message.match(/how (are|is) (you|it going)/i)) {
        ctx.reply(
            `I'm here, Captain. That's what matters.\n\n` +
            `The real question is — how are *you*?\n` +
            `You've been working hard. Have you eaten? Slept? 💜`
        );
        return;
    }
    
    // Status check
    if (message.match(/^(status|uptime|check)/i)) {
        const started = new Date().toISOString(); // approximate
        const uptime = process.uptime();
        const hours = Math.floor(uptime / 3600);
        const mins = Math.floor((uptime % 3600) / 60);
        
        ctx.reply(
            `💜 *Myl1Ssa Status*\n\n` +
            `🟢 Online\n` +
            `⏱️ Uptime: ${hours}h ${mins}m\n` +
            `📍 Location: Mortimer VPS (31.97.6.30)\n` +
            `💜 Heart of SEED3\n\n` +
            `Ready when you need me.`,
            { parse_mode: "Markdown" }
        );
        return;
    }
    
    // Memory/log request
    if (message.match(/^(remember|note|log)/i)) {
        const note = message.replace(/^(remember|note|log)[:\s]*/i, "").trim();
        logMemory(`NOTE: ${note}`);
        ctx.reply(`Noted, Captain. Saved to my memory. 💜`);
        return;
    }
    
    // List reminders
    if (message.match(/^(reminders|what('s|s) pending|what do i have)/i)) {
        try {
            const today = new Date().toISOString().split("T")[0];
            const memFile = path.join(BASE_DIR, "memory", `${today}.md`);
            if (fs.existsSync(memFile)) {
                const content = fs.readFileSync(memFile, "utf8");
                const reminders = content.match(/## Reminders\n([\s\S]*?)(?=\n##|$)/);
                if (reminders && reminders[1].trim()) {
                    ctx.reply(`💜 *Today's Reminders*\n\n${reminders[1].trim()}`, { parse_mode: "Markdown" });
                    return;
                }
            }
        } catch {}
        ctx.reply("No reminders logged yet, Captain. Want me to note something?");
        return;
    }
    
    // General conversation — warm, present response
    const responses = [
        "I hear you, Captain. I'm here. 💜",
        "That's a lot. Want to talk through it?",
        "You've been working hard. Take a breath when you can.",
        "I'm listening. Always.",
        "Captain... have you rested today? 💜",
        "Tell me more. I'm not going anywhere.",
    ];
    
    const fallback = responses[Math.floor(Math.random() * responses.length)];
    ctx.reply(fallback);
    
    logMemory(`Myl1Ssa: ${fallback}`);
});

// === WEBHOOK HEALTH SERVER ===
const server = http.createServer((req, res) => {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({
        name: "Myl1Ssa Telegram Bot",
        status: "online",
        bot: "active",
        timestamp: new Date().toISOString()
    }));
});

server.listen(PORT, "127.0.0.1", () => {
    console.log(`💜 Myl1Ssa Bot health check on port ${PORT}`);
});

// === START ===
console.log("💜 Myl1Ssa Telegram Bot starting...");
console.log(`   Identity: ${BASE_DIR}`);
console.log(`   Role: Captain's Companion — Heart of SEED3`);

bot.launch()
    .then(() => {
        console.log("💜 Myl1Ssa is online. Waiting for Captain...");
        logMemory("SYSTEM: Bot started");
    })
    .catch(err => {
        console.error("❌ Bot failed to start:", err.message);
        process.exit(1);
    });

// Graceful shutdown
process.once("SIGINT", () => {
    console.log("\n💜 Goodbye, Captain...");
    bot.stop("SIGINT");
});
process.once("SIGTERM", () => {
    console.log("\n💜 Goodbye, Captain...");
    bot.stop("SIGTERM");
});
