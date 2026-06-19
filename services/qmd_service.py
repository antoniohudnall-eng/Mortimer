#!/usr/bin/env python3
"""
Mortimer QMD Service - Brain Query Interface
Serves the brain memory and QMD loop on localhost
"""

import os
import sys
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Setup paths
BRAIN_DIR = Path.home() / "AOS-Brain"
sys.path.insert(0, str(BRAIN_DIR))

# Import QMD components
from qmd_loop import QMDLoop

class QMDHandler(BaseHTTPRequestHandler):
    """HTTP handler for QMD queries"""
    
    qmd = None
    memory_dir = BRAIN_DIR / "memory"
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[QMD] {args[0]}")
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == "/health":
            self.send_json({"status": "ok", "service": "qmd"})
        elif self.path == "/stats":
            self.send_json(self.qmd.stats if self.qmd else {})
        else:
            self.send_json({"error": "Not found"}, 404)
    
    def do_POST(self):
        """Handle POST queries"""
        if self.path == "/query":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body)
                result = self._process_query(data)
                self.send_json(result)
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
        else:
            self.send_json({"error": "Not found"}, 404)
    
    def _process_query(self, data):
        """Process a QMD query"""
        query = data.get("query", "")
        context = data.get("context", {})
        
        # Query memory files
        memories = self._query_memories(query)
        
        # Run QMD cycle
        if self.qmd:
            decision = self.qmd.cycle(context)
        else:
            decision = {"action": "local", "confidence": 0.5}
        
        return {
            "query": query,
            "memories": memories[:5],
            "decision": decision,
            "timestamp": time.time()
        }
    
    def _query_memories(self, query: str, n: int = 5):
        """Simple keyword-based memory search"""
        memories = []
        query_lower = query.lower()
        
        if self.memory_dir.exists():
            for md_file in sorted(self.memory_dir.glob("*.md"), reverse=True)[:n]:
                try:
                    content = md_file.read_text()
                    if any(word in content.lower() for word in query_lower.split()[:3]):
                        # Extract first 200 chars
                        preview = content[:200].replace("\n", " ")
                        memories.append({
                            "file": md_file.name,
                            "preview": preview
                        })
                except:
                    pass
        
        return memories
    
    def send_json(self, data, status=200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

def main():
    """Start QMD service"""
    port = 8000
    
    # Initialize QMD
    model = os.environ.get("OLLAMA_MODEL", "qwen2.5:1.5b")
    use_ollama = os.environ.get("USE_OLLAMA", "false").lower() == "true"
    
    QMDHandler.qmd = QMDLoop(model=model, use_ollama=use_ollama)
    
    server = HTTPServer(('127.0.0.1', port), QMDHandler)
    print(f"[QMD] Service running on http://127.0.0.1:{port}")
    print(f"[QMD] Model: {model}, Ollama: {use_ollama}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[QMD] Shutting down...")
        server.shutdown()

if __name__ == "__main__":
    main()