#!/usr/bin/env python3
"""Collections API - Standalone HTTP Server
Uses built-in sqlite3, no external dependencies"""

import http.server
import socketserver
import sqlite3
import json
import os
from urllib.parse import urlparse

DB_PATH = '/root/.openclaw/workspace/datadepot/data/collections.db'
PORT = 8085

class CollectionsHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default logging
        pass
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/collections/api' or parsed.path == '/collections/api/':
            try:
                # Read-only connection
                conn = sqlite3.connect(f'file:{DB_PATH}?mode=ro', uri=True)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM collections_accounts 
                    WHERE status != 'paid' 
                    ORDER BY days_overdue DESC, amount DESC
                """)
                
                rows = cursor.fetchall()
                conn.close()
                
                invoices = []
                for row in rows:
                    invoices.append({
                        'date': row['invoice_date'],
                        'customer': row['customer_name'],
                        'email': row['email'] or '',
                        'invoice': row['invoice_number'],
                        'amount': float(row['amount']),
                        'status': row['status'],
                        'days': int(row['days_overdue'] or 0),
                        'viewed': bool(row['viewed']),
                        'note': row['notes'] or '',
                        'address': row['address'] or 'Address not on file - Click Edit to add',
                        'phone': row['phone'] or ''
                    })
                
                self.send_json({
                    'success': True,
                    'count': len(invoices),
                    'invoices': invoices,
                    'lastUpdated': __import__('datetime').datetime.now().isoformat()
                })
                
            except Exception as e:
                print(f"API Error: {e}")
                self.send_json({
                    'error': str(e),
                    'fallback': True,
                    'invoices': []
                }, 500)
            return
        
        # Health check
        if parsed.path == '/collections/api/health':
            self.send_json({'status': 'ok', 'service': 'collections-api'})
            return
        
        # 404
        self.send_json({'error': 'Not found'}, 404)

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        print(f"ERROR: Database not found at {DB_PATH}")
        exit(1)
    
    print(f"Collections API starting on port {PORT}...")
    print(f"Database: {DB_PATH}")
    
    with socketserver.TCPServer(("127.0.0.1", PORT), CollectionsHandler) as httpd:
        print(f"Server running at http://127.0.0.1:{PORT}/collections/api")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
