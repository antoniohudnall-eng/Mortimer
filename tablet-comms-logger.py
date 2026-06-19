#!/usr/bin/env python3
"""Tablet Comms Request Logger"""
import http.server
import json
import socketserver
from datetime import datetime

PORT = 9002
LOG_FILE = "/data/data/com.termux/files/home/mortimer/logs/tablet-comms.log"

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] POST {self.path}\nHeaders: {dict(self.headers)}\nBody: {body}\n"
        
        # Log to file
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry)
        
        # Log to console
        print(f"\n📨 INCOMING REQUEST at {timestamp}")
        print(f"   Path: {self.path}")
        print(f"   Body: {body[:200]}...")
        
        # Respond
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "received", "logged": True}).encode())
    
    def log_message(self, format, *args):
        pass  # Suppress default logging

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"📡 Tablet Comms Logger running on port {PORT}")
    print(f"📝 Logging to: {LOG_FILE}")
    httpd.serve_forever()
