#!/usr/bin/env python3
"""Proxy server with fixed CORS headers"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.request
import os

class ProxyHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    
    def do_GET(self):
        if self.path == '/api/collections':
            self.proxy_collections()
        elif self.path == '/api/depotchaos':
            self.proxy_depotchaos()
        elif self.path == '/api/psd':
            self.proxy_psd()
        elif self.path == '/':
            self.serve_index()
        else:
            self.send_error(404)
    
    def proxy_collections(self):
        """Proxy Collections API with correct headers"""
        try:
            req = urllib.request.Request('https://psdepot.com/collections/api')
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_error(500, str(e))
    
    def proxy_depotchaos(self):
        """Proxy DepotChaos stats"""
        try:
            req = urllib.request.Request('https://psdepot.com/depotchaos/api/stats')
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_error(500, str(e))
    
    def proxy_psd(self):
        """Proxy PSD Dashboard"""
        try:
            req = urllib.request.Request('https://psdepot.com/psd-api/dashboard/overview')
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_error(500, str(e))
    
    def serve_index(self):
        """Serve the dashboard"""
        try:
            with open('index.html', 'rb') as f:
                html = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(html)))
            self.end_headers()
            self.wfile.write(html)
        except Exception as e:
            self.send_error(500, str(e))
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")

if __name__ == '__main__':
    os.chdir('/data/data/com.termux/files/home/mortimer/sales-command')
    server = HTTPServer(('0.0.0.0', 8080), ProxyHandler)
    print("🚀 Proxy Server running on port 8080")
    print("📱 Dashboard: http://localhost:8080/")
    print("📡 APIs: http://localhost:8080/api/{collections|depotchaos|psd}")
    server.serve_forever()
