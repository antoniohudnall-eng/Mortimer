#!/usr/bin/env python3
"""TikTok Lead Capture Webhook Handler"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "sales.db"

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length).decode('utf-8'))
        
        # Log lead
        log_file = Path(__file__).parent.parent / "data" / "leads.log"
        with open(log_file, 'a') as f:
            f.write(f"{json.dumps(body)}\n")
        
        # Respond
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "captured",
            "message": "Lead received! We'll contact you soon."
        }).encode())
    
    def log_message(self, *args): pass

def run(port=9003):
    server = HTTPServer(('', port), Handler)
    print(f"📡 TikTok Lead Capture running on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    run()
