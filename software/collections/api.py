#!/usr/bin/env python3
"""Collections API Server - Python/Flask
Serves data from SQLite database
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)

DB_PATH = '/root/.openclaw/workspace/datadepot/data/collections.db'

def get_db_connection():
    """Get a read-only database connection"""
    conn = sqlite3.connect(f'file:{DB_PATH}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/collections/api', methods=['GET'])
def get_collections():
    """Get all collections accounts"""
    try:
        conn = get_db_connection()
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
        
        return jsonify({
            'success': True,
            'count': len(invoices),
            'invoices': invoices,
            'lastUpdated': __import__('datetime').datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({
            'error': f'Database error: {str(e)}',
            'fallback': True,
            'invoices': []
        }), 500

@app.route('/collections/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'collections-api'})

if __name__ == '__main__':
    # Check if database exists
    if not Path(DB_PATH).exists():
        print(f"ERROR: Database not found at {DB_PATH}")
        exit(1)
    
    print(f"Collections API starting...")
    print(f"Database: {DB_PATH}")
    
    # Run on port 8085
    app.run(host='127.0.0.1', port=8085, debug=False)
