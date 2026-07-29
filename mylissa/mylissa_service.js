/**
 * Myl1Ssa v1.0 - Captain's Companion Service
 * VPS: Mortimer (31.97.6.30)
 * Role: Heart - Support & Presence
 */

const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = 12850;
const BASE_DIR = "/home/aocros/agents/mylissa";

// Heartbeat timestamps
const state = {
    started: new Date().toISOString(),
    heartbeats: 0,
    lastWake: null,
    status: "ready"
};

// Logging
function log(msg) {
    const timestamp = new Date().toISOString();
    const entry = `[${timestamp}] ${msg}`;
    console.log(entry);
    fs.appendFileSync(path.join(BASE_DIR, "mylissa.log"), entry + "\n");
}

// Create server
const server = http.createServer((req, res) => {
    const url = new URL(req.url, `http://localhost:${PORT}`);
    
    // CORS
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
    
    if (req.method === "OPTIONS") {
        res.writeHead(204);
        res.end();
        return;
    }
    
    if (req.method === "GET" && url.pathname === "/health") {
        state.heartbeats++;
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({
            name: "Myl1Ssa",
            designation: "Myl1Ssa-1",
            role: "Captain's Companion - Heart",
            ship: "SEED3",
            status: state.status,
            uptime: Math.floor((Date.now() - new Date(state.started).getTime()) / 1000),
            heartbeats: state.heartbeats,
            lastWake: state.lastWake,
            location: "Mortimer VPS (31.97.6.30)"
        }, null, 2));
        return;
    }
    
    if (req.method === "POST" && url.pathname === "/wake") {
        let body = "";
        req.on("data", chunk => body += chunk);
        req.on("end", () => {
            try {
                const data = JSON.parse(body);
                state.lastWake = new Date().toISOString();
                state.status = "awake";
                log(`AWOKE - Captain: ${data.captain_status || 'unknown'}`);
                
                // Create daily memory
                const today = new Date().toISOString().split("T")[0];
                const memDir = path.join(BASE_DIR, "memory");
                const memFile = path.join(memDir, `${today}.md`);
                
                if (!fs.existsSync(memDir)) fs.mkdirSync(memDir, { recursive: true });
                if (!fs.existsSync(memFile)) {
                    fs.writeFileSync(memFile, `# Myl1Ssa - ${today}\n\n## Wake Details\n- Time: ${state.lastWake}\n- Captain Status: ${data.captain_status || 'unknown'}\n\n## Notes\n\n`);
                }
                
                res.writeHead(200, { "Content-Type": "application/json" });
                res.end(JSON.stringify({ status: "awake", timestamp: state.lastWake }));
            } catch (e) {
                res.writeHead(400);
                res.end(JSON.stringify({ error: e.message }));
            }
        });
        return;
    }
    
    res.writeHead(404);
    res.end(JSON.stringify({ error: "not found" }));
});

server.listen(PORT, "127.0.0.1", () => {
    log(`💜 Myl1Ssa online on port ${PORT}`);
    log(`Location: ${BASE_DIR}`);
    log(`Role: Captain's Heart - Support & Presence`);
});

// Graceful shutdown
process.on("SIGTERM", () => {
    log("Shutting down... Goodbye, Captain.");
    server.close(() => process.exit(0));
});

process.on("SIGINT", () => {
    log("Interrupted... Standing down.");
    server.close(() => process.exit(0));
});
