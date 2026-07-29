/**
 * Camera Feed Receiver v1.0
 * Accepts images/video from O-Kam Pro and FlyCloud cameras
 * Stores, processes, and serves camera media
 * 
 * VPS: Mortimer (31.97.6.30)
 * Port: 12860 (receiver) | 12861 (viewer)
 */

const http = require("http");
const fs = require("fs");
const path = require("path");
const { execSync, exec } = require("child_process");
const { randomUUID } = require("crypto");

// === CONFIG ===
const RECEIVER_PORT = 12860;
const VIEWER_PORT = 12861;
const MEDIA_DIR = "/home/aocros/cameras/media";
const THUMB_DIR = "/home/aocros/cameras/thumbnails";

// === ENSURE DIRECTORIES ===
[MEDIA_DIR, THUMB_DIR].forEach(dir => {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true, mode: 0o755 });
    }
});

// === CAMERA REGISTRY ===
const CAMERAS_FILE = "/home/aocros/cameras/cameras.json";
if (!fs.existsSync(CAMERAS_FILE)) {
    fs.writeFileSync(CAMERAS_FILE, JSON.stringify({
        "flycloud": { name: "FlyCloud", type: "security", status: "active", added: new Date().toISOString() },
        "okam-pro": { name: "O-Kam Pro", type: "ip-cam", status: "active", added: new Date().toISOString() }
    }, null, 2));
}

const cameras = JSON.parse(fs.readFileSync(CAMERAS_FILE, "utf8"));

// === LOGGING ===
const LOG_FILE = "/home/aocros/cameras/camera.log";
function log(msg) {
    const ts = new Date().toISOString();
    const line = `[${ts}] ${msg}`;
    console.log(line);
    fs.appendFileSync(LOG_FILE, line + "\n");
}

// === MEDIA INDEX ===
const INDEX_FILE = "/home/aocros/cameras/index.json";
let mediaIndex = {};
if (fs.existsSync(INDEX_FILE)) {
    try { mediaIndex = JSON.parse(fs.readFileSync(INDEX_FILE, "utf8")); } catch {}
}

function saveIndex() {
    fs.writeFileSync(INDEX_FILE, JSON.stringify(mediaIndex, null, 2));
}

// === GENERATE THUMBNAIL ===
function generateThumbnail(filePath, mediaId) {
    const thumbPath = path.join(THUMB_DIR, `${mediaId}_thumb.jpg`);
    try {
        execSync(`ffmpeg -y -i "${filePath}" -vf "scale=320:240:force_original_aspect_ratio=decrease" -vframes 1 -q:v 5 "${thumbPath}" 2>/dev/null`);
        return thumbPath;
    } catch (e) {
        log(`Thumbnail failed for ${mediaId}: ${e.message}`);
        return null;
    }
}

// === PARSE MULTIPART BOUNDARY ===
function parseMultipart(buffer, boundary) {
    const parts = [];
    const str = buffer.toString();
    const boundaryMarker = `--${boundary}`;
    const sections = str.split(boundaryMarker);
    
    for (const section of sections) {
        if (section.includes("Content-Disposition")) {
            const headerEnd = section.indexOf("\r\n\r\n");
            if (headerEnd === -1) continue;
            
            const headers = section.substring(0, headerEnd);
            const nameMatch = headers.match(/name="([^"]+)"/);
            const filenameMatch = headers.match(/filename="([^"]+)"/);
            const contentTypeMatch = headers.match(/Content-Type:\s*(.+)/i);
            
            const bodyStart = headerEnd + 4;
            let body = section.substring(bodyStart);
            // Trim trailing \r\n and boundary artifacts
            body = body.replace(/\r\n--$/, "").replace(/\r\n$/, "");
            
            parts.push({
                name: nameMatch ? nameMatch[1] : null,
                filename: filenameMatch ? filenameMatch[1] : null,
                contentType: contentTypeMatch ? contentTypeMatch[1].trim() : null,
                data: body
            });
        }
    }
    return parts;
}

// === RECEIVER SERVER ===
const receiver = http.createServer((req, res) => {
    // CORS
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
    
    if (req.method === "OPTIONS") {
        res.writeHead(204); res.end(); return;
    }
    
    // Health check
    if (req.method === "GET" && req.url === "/health") {
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ 
            service: "camera-receiver",
            status: "online",
            mediaCount: Object.keys(mediaIndex).length,
            cameras: cameras,
            timestamp: new Date().toISOString()
        }));
        return;
    }
    
    // Upload endpoint
    if (req.method === "POST" && req.url.startsWith("/upload")) {
        const url = new URL(req.url, `http://localhost:${RECEIVER_PORT}`);
        const camera = url.searchParams.get("camera") || "unknown";
        const type = url.searchParams.get("type") || "image";
        
        const mediaId = randomUUID();
        const dateDir = new Date().toISOString().split("T")[0];
        const ext = type === "video" ? ".mp4" : ".jpg";
        const filename = `${dateDir}_${camera}_${mediaId.substring(0, 8)}${ext}`;
        const fileDir = path.join(MEDIA_DIR, camera, dateDir);
        const filePath = path.join(fileDir, filename);
        
        if (!fs.existsSync(fileDir)) {
            fs.mkdirSync(fileDir, { recursive: true });
        }
        
        let chunks = [];
        req.on("data", chunk => chunks.push(chunk));
        req.on("end", () => {
            const buffer = Buffer.concat(chunks);
            let data = buffer;
            
            // Handle multipart form data
            const contentType = req.headers["content-type"] || "";
            if (contentType.includes("multipart")) {
                const boundaryMatch = contentType.match(/boundary=([^;]+)/);
                if (boundaryMatch) {
                    const boundary = boundaryMatch[1].trim().replace(/^"|"$/g, '');
                    const boundaryBuffer = Buffer.from(`--${boundary}`);
                    
                    // Find boundaries in the buffer
                    let startIdx = buffer.indexOf(boundaryBuffer);
                    if (startIdx !== -1) {
                        startIdx = buffer.indexOf(boundaryBuffer, startIdx + boundaryBuffer.length);
                        if (startIdx === -1) startIdx = 0;
                        
                        // Skip past boundary line
                        let headerEnd = buffer.indexOf(Buffer.from('\r\n\r\n'), startIdx);
                        if (headerEnd !== -1) {
                            data = buffer.slice(headerEnd + 4);
                            // Trim trailing boundary
                            const endBoundary = data.lastIndexOf(boundaryBuffer);
                            if (endBoundary !== -1) {
                                data = data.slice(0, endBoundary - 2); // -2 for \r\n
                            }
                        }
                    }
                }
            }
            
            // Write the file
            fs.writeFileSync(filePath, data);
            const fileSize = fs.statSync(filePath).size;
            
            // Generate thumbnail
            const thumb = generateThumbnail(filePath, mediaId);
            
            // Index it
            mediaIndex[mediaId] = {
                id: mediaId,
                camera: camera,
                type: type,
                filename: filename,
                path: filePath,
                thumbnail: thumb,
                size: fileSize,
                timestamp: new Date().toISOString(),
                tags: []
            };
            saveIndex();
            
            log(`📸 Received ${type} from ${camera}: ${filename} (${(fileSize/1024).toFixed(1)}KB)`);
            
            res.writeHead(200, { "Content-Type": "application/json" });
            res.end(JSON.stringify({
                status: "ok",
                id: mediaId,
                camera: camera,
                filename: filename,
                size: fileSize,
                viewUrl: `http://31.97.6.30:12861/view/${mediaId}`
            }));
        });
        return;
    }
    
    // Simple URL-based capture (for O-Kam Pro HTTP upload)
    if (req.method === "GET" && req.url.startsWith("/snap")) {
        const url = new URL(req.url, `http://localhost:${RECEIVER_PORT}`);
        const camera = url.searchParams.get("camera") || "okam-pro";
        
        const mediaId = randomUUID();
        const dateDir = new Date().toISOString().split("T")[0];
        const filename = `${dateDir}_${camera}_${mediaId.substring(0, 8)}.jpg`;
        const fileDir = path.join(MEDIA_DIR, camera, dateDir);
        const filePath = path.join(fileDir, filename);
        
        if (!fs.existsSync(fileDir)) {
            fs.mkdirSync(fileDir, { recursive: true });
        }
        
        let bodyParts = [];
        req.on("data", chunk => bodyParts.push(chunk));
        req.on("end", () => {
            const buffer = Buffer.concat(bodyParts);
            if (buffer.length > 0) {
                fs.writeFileSync(filePath, buffer);
                const fileSize = fs.statSync(filePath).size;
                const thumb = generateThumbnail(filePath, mediaId);
                
                mediaIndex[mediaId] = {
                    id: mediaId,
                    camera: camera,
                    type: "image",
                    filename: filename,
                    path: filePath,
                    thumbnail: thumb,
                    size: fileSize,
                    timestamp: new Date().toISOString(),
                    tags: []
                };
                saveIndex();
                
                log(`📸 Snap from ${camera}: ${filename} (${(fileSize/1024).toFixed(1)}KB)`);
            }
            
            res.writeHead(200, { "Content-Type": "application/json" });
            res.end(JSON.stringify({ status: "ok", id: mediaId }));
        });
        return;
    }
    
    // List recent media
    if (req.method === "GET" && req.url.startsWith("/recent")) {
        const url = new URL(req.url, `http://localhost:${RECEIVER_PORT}`);
        const limit = parseInt(url.searchParams.get("limit")) || 20;
        const camera = url.searchParams.get("camera");
        
        let items = Object.values(mediaIndex)
            .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        
        if (camera) {
            items = items.filter(i => i.camera === camera);
        }
        
        items = items.slice(0, limit);
        
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify(items, null, 2));
        return;
    }
    
    res.writeHead(404);
    res.end(JSON.stringify({ error: "not found" }));
});

// === VIEWER SERVER (serves stored media) ===
const viewer = http.createServer((req, res) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    
    // View single media
    if (req.url.startsWith("/view/")) {
        const mediaId = req.url.split("/view/")[1].split("?")[0];
        const media = mediaIndex[mediaId];
        
        if (!media || !fs.existsSync(media.path)) {
            res.writeHead(404);
            res.end("Media not found");
            return;
        }
        
        const ext = path.extname(media.path).toLowerCase();
        const mimeTypes = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".mp4": "video/mp4",
            ".webm": "video/webm"
        };
        
        res.writeHead(200, { 
            "Content-Type": mimeTypes[ext] || "application/octet-stream",
            "Content-Length": fs.statSync(media.path).size
        });
        fs.createReadStream(media.path).pipe(res);
        return;
    }
    
    // Thumbnail
    if (req.url.startsWith("/thumb/")) {
        const mediaId = req.url.split("/thumb/")[1].split("?")[0];
        const media = mediaIndex[mediaId];
        
        if (!media || !media.thumbnail || !fs.existsSync(media.thumbnail)) {
            res.writeHead(404);
            res.end("Thumbnail not found");
            return;
        }
        
        res.writeHead(200, { "Content-Type": "image/jpeg" });
        fs.createReadStream(media.thumbnail).pipe(res);
        return;
    }
    
    // Gallery HTML
    if (req.url === "/" || req.url === "/gallery") {
        const items = Object.values(mediaIndex)
            .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
            .slice(0, 50);
        
        const html = `<!DOCTYPE html>
<html><head>
<title>Camera Feed — Mortimer.cloud</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body { background:#1a1a2e; color:#e0e0e0; font-family:monospace; margin:0; padding:20px; }
  h1 { color:#ff6b9d; }
  .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:10px; }
  .card { background:#16213e; border-radius:8px; overflow:hidden; }
  .card img { width:100%; height:150px; object-fit:cover; }
  .card .info { padding:8px; font-size:11px; }
  .camera-tag { color:#ff6b9d; }
  .timestamp { color:#888; }
  .actions { margin:10px 0; }
  .btn { background:#ff6b9d; color:white; border:none; padding:8px 16px; border-radius:4px; cursor:pointer; text-decoration:none; font-size:14px; }
  .refresh { float:right; }
</style></head><body>
<h1>🎥 Camera Feed <span style="font-size:14px;color:#888">— Mortimer.cloud</span></h1>
<div class="actions">
  <a class="btn" href="/gallery">Refresh</a>
  <span style="margin-left:10px;color:#888">${items.length} captures</span>
</div>
<div class="grid">
${items.map(m => `
  <div class="card">
    <a href="/view/${m.id}"><img src="/thumb/${m.id}" loading="lazy"></a>
    <div class="info">
      <div class="camera-tag">📷 ${m.camera}</div>
      <div class="timestamp">${new Date(m.timestamp).toLocaleString()}</div>
      <div style="color:#888">${(m.size/1024).toFixed(1)}KB</div>
    </div>
  </div>
`).join("")}
</div>
<p style="margin-top:30px;font-size:11px;color:#666">
  Upload: POST /upload?camera=NAME | Snap: GET /snap?camera=NAME<br>
  <a href="/recent" style="color:#ff6b9d">JSON feed →</a>
</p>
</body></html>`;
        
        res.writeHead(200, { "Content-Type": "text/html" });
        res.end(html);
        return;
    }
    
    // Recent JSON
    if (req.url.startsWith("/recent")) {
        const limit = parseInt(new URL(req.url, "http://localhost").searchParams.get("limit")) || 20;
        const items = Object.values(mediaIndex)
            .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
            .slice(0, limit);
        
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify(items, null, 2));
        return;
    }
    
    res.writeHead(404);
    res.end("Not found");
});

// === START ===
receiver.listen(RECEIVER_PORT, "0.0.0.0", () => {
    log(`📸 Camera receiver online on port ${RECEIVER_PORT}`);
    log(`   Upload: POST http://31.97.6.30:${RECEIVER_PORT}/upload?camera=NAME`);
    log(`   Snap:   GET  http://31.97.6.30:${RECEIVER_PORT}/snap?camera=NAME`);
});

viewer.listen(VIEWER_PORT, "0.0.0.0", () => {
    log(`🖼️  Camera viewer online on port ${VIEWER_PORT}`);
    log(`   Gallery: http://31.97.6.30:${VIEWER_PORT}/`);
    log(`   JSON:   http://31.97.6.30:${VIEWER_PORT}/recent`);
    log(`🎥 Cameras: ${Object.keys(cameras).join(", ")}`);
});

process.on("SIGTERM", () => { log("Shutting down..."); process.exit(0); });
process.on("SIGINT", () => { log("Interrupted..."); process.exit(0); });
