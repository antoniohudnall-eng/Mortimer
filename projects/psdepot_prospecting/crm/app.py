#!/usr/bin/env python3
"""
Mortimer's Prospecting CRM - Backend API
Flask-based REST API for lead management
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import csv
import os
import json
from datetime import datetime
from pathlib import Path

app = Flask(__name__, static_folder='static')
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'leads.db')
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with leads from CSV"""
    conn = get_db()
    c = conn.cursor()
    
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            address TEXT,
            city TEXT,
            state TEXT DEFAULT 'CA',
            zip TEXT,
            website TEXT,
            category_type TEXT DEFAULT 'other',
            categories TEXT,
            rating TEXT,
            review_count TEXT,
            source TEXT,
            date_found TEXT,
            status TEXT DEFAULT 'new',
            priority TEXT DEFAULT 'medium',
            notes TEXT,
            assigned_to TEXT,
            last_contact TEXT,
            next_action TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER,
            type TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER,
            title TEXT,
            description TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        )
    ''')
    
    conn.commit()
    
    # Check if we need to import from CSV
    c.execute('SELECT COUNT(*) FROM leads')
    count = c.fetchone()[0]
    
    if count == 0:
        # Import from existing CSV
        csv_path = os.path.join(DATA_DIR, 'psdepot_leads_latest.csv')
        if os.path.exists(csv_path):
            imported = 0
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    c.execute('''
                        INSERT INTO leads (name, phone, address, city, state, zip, 
                                         website, category_type, categories, rating, 
                                         review_count, source, date_found)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row.get('name', ''),
                        row.get('phone', ''),
                        row.get('address', ''),
                        row.get('city', ''),
                        row.get('state', 'CA'),
                        row.get('zip', ''),
                        row.get('website', ''),
                        row.get('category_type', 'other'),
                        row.get('categories', ''),
                        row.get('rating', ''),
                        row.get('review_count', ''),
                        row.get('source', ''),
                        row.get('date_found', '')
                    ))
                    imported += 1
            conn.commit()
            print(f"[+] Imported {imported} leads from CSV")
    
    conn.close()

# API Routes

@app.route('/')
def index():
    """Serve main CRM page"""
    return send_from_directory('static', 'index.html')

@app.route('/api/stats')
def stats():
    """Get overall statistics"""
    conn = get_db()
    c = conn.cursor()
    
    # Total leads
    c.execute('SELECT COUNT(*) FROM leads')
    total = c.fetchone()[0]
    
    # By category
    c.execute('SELECT category_type, COUNT(*) as count FROM leads GROUP BY category_type ORDER BY count DESC')
    categories = [dict(row) for row in c.fetchall()]
    
    # By status
    c.execute('SELECT status, COUNT(*) as count FROM leads GROUP BY status')
    statuses = [dict(row) for row in c.fetchall()]
    
    # By city (top 20)
    c.execute('SELECT city, COUNT(*) as count FROM leads WHERE city != "" GROUP BY city ORDER BY count DESC LIMIT 20')
    cities = [dict(row) for row in c.fetchall()]
    
    # With phone numbers
    c.execute('SELECT COUNT(*) FROM leads WHERE phone != "" AND phone IS NOT NULL')
    with_phone = c.fetchone()[0]
    
    # Recently added (last 7 days)
    c.execute("SELECT COUNT(*) FROM leads WHERE date_found >= date('now', '-7 days')")
    recent = c.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total': total,
        'categories': categories,
        'statuses': statuses,
        'cities': cities,
        'with_phone': with_phone,
        'recent': recent
    })

@app.route('/api/leads')
def get_leads():
    """Get leads with filtering and pagination"""
    conn = get_db()
    
    # Query params
    category = request.args.get('category', 'all')
    status = request.args.get('status', 'all')
    city = request.args.get('city', '')
    search = request.args.get('search', '')
    has_phone = request.args.get('has_phone', 'false') == 'true'
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    sort_by = request.args.get('sort_by', 'name')
    sort_dir = request.args.get('sort_dir', 'asc')
    
    # Build query
    query = 'SELECT * FROM leads WHERE 1=1'
    count_query = 'SELECT COUNT(*) FROM leads WHERE 1=1'
    params = []
    
    if category != 'all':
        query += ' AND category_type = ?'
        count_query += ' AND category_type = ?'
        params.append(category)
    
    if status != 'all':
        query += ' AND status = ?'
        count_query += ' AND status = ?'
        params.append(status)
    
    if city:
        query += ' AND city LIKE ?'
        count_query += ' AND city LIKE ?'
        params.append(f'%{city}%')
    
    if search:
        query += ' AND (name LIKE ? OR address LIKE ? OR city LIKE ?)'
        count_query += ' AND (name LIKE ? OR address LIKE ? OR city LIKE ?)'
        search_term = f'%{search}%'
        params.extend([search_term, search_term, search_term])
    
    if has_phone:
        query += ' AND phone != "" AND phone IS NOT NULL'
        count_query += ' AND phone != "" AND phone IS NOT NULL'
    
    # Sorting
    allowed_sorts = ['name', 'city', 'category_type', 'date_found', 'status']
    if sort_by in allowed_sorts:
        query += f' ORDER BY {sort_by} {sort_dir.upper()}'
    
    # Pagination
    offset = (page - 1) * per_page
    query += f' LIMIT {per_page} OFFSET {offset}'
    
    c = conn.cursor()
    
    # Get total count
    c.execute(count_query, params)
    total = c.fetchone()[0]
    
    # Get leads
    c.execute(query, params)
    leads = [dict(row) for row in c.fetchall()]
    
    conn.close()
    
    return jsonify({
        'leads': leads,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    })

@app.route('/api/leads/<int:lead_id>')
def get_lead(lead_id):
    """Get single lead with interactions"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('SELECT * FROM leads WHERE id = ?', (lead_id,))
    lead = dict(c.fetchone())
    
    c.execute('SELECT * FROM interactions WHERE lead_id = ? ORDER BY created_at DESC', (lead_id,))
    lead['interactions'] = [dict(row) for row in c.fetchall()]
    
    c.execute('SELECT * FROM tasks WHERE lead_id = ? ORDER BY due_date', (lead_id,))
    lead['tasks'] = [dict(row) for row in c.fetchall()]
    
    conn.close()
    return jsonify(lead)

@app.route('/api/leads', methods=['POST'])
def create_lead():
    """Create new lead"""
    data = request.json
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO leads (name, phone, address, city, state, zip, website, 
                          category_type, categories, status, priority, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('name'),
        data.get('phone'),
        data.get('address'),
        data.get('city'),
        data.get('state', 'CA'),
        data.get('zip'),
        data.get('website'),
        data.get('category_type', 'other'),
        data.get('categories'),
        data.get('status', 'new'),
        data.get('priority', 'medium'),
        data.get('notes')
    ))
    
    lead_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': lead_id, 'success': True})

@app.route('/api/leads/<int:lead_id>', methods=['PUT'])
def update_lead(lead_id):
    """Update lead"""
    data = request.json
    
    conn = get_db()
    c = conn.cursor()
    
    # Build update query dynamically
    fields = []
    values = []
    
    for field in ['name', 'phone', 'address', 'city', 'state', 'zip', 'website',
                  'category_type', 'categories', 'status', 'priority', 'notes',
                  'assigned_to', 'last_contact', 'next_action']:
        if field in data:
            fields.append(f'{field} = ?')
            values.append(data[field])
    
    if fields:
        fields.append('updated_at = CURRENT_TIMESTAMP')
        values.append(lead_id)
        
        query = f'UPDATE leads SET {", ".join(fields)} WHERE id = ?'
        c.execute(query, values)
        conn.commit()
    
    conn.close()
    return jsonify({'success': True})

@app.route('/api/leads/<int:lead_id>', methods=['DELETE'])
def delete_lead(lead_id):
    """Delete lead"""
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM leads WHERE id = ?', (lead_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/leads/<int:lead_id>/interactions', methods=['POST'])
def add_interaction(lead_id):
    """Add interaction to lead"""
    data = request.json
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO interactions (lead_id, type, notes)
        VALUES (?, ?, ?)
    ''', (lead_id, data.get('type'), data.get('notes')))
    
    interaction_id = c.lastrowid
    
    # Update last_contact on lead
    c.execute('UPDATE leads SET last_contact = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP WHERE id = ?', (lead_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'id': interaction_id, 'success': True})

@app.route('/api/export')
def export_leads():
    """Export leads to CSV"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('SELECT * FROM leads ORDER BY name')
    leads = c.fetchall()
    
    conn.close()
    
    # Create CSV in memory
    import io
    output = io.StringIO()
    if leads:
        fieldnames = leads[0].keys()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for lead in leads:
            writer.writerow(dict(lead))
    
    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=leads_export.csv'
    }

@app.route('/api/import', methods=['POST'])
def import_leads():
    """Import leads from CSV"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Must be CSV file'}), 400
    
    conn = get_db()
    c = conn.cursor()
    
    imported = 0
    errors = []
    
    try:
        stream = io.StringIO(file.stream.read().decode('UTF-8'))
        reader = csv.DictReader(stream)
        
        for row_num, row in enumerate(reader, start=2):
            try:
                c.execute('''
                    INSERT INTO leads (name, phone, address, city, state, zip, 
                                     website, category_type, categories, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row.get('name', ''),
                    row.get('phone', ''),
                    row.get('address', ''),
                    row.get('city', ''),
                    row.get('state', 'CA'),
                    row.get('zip', ''),
                    row.get('website', ''),
                    row.get('category_type', 'other'),
                    row.get('categories', ''),
                    'import'
                ))
                imported += 1
            except Exception as e:
                errors.append(f'Row {row_num}: {str(e)}')
        
        conn.commit()
    finally:
        conn.close()
    
    return jsonify({
        'imported': imported,
        'errors': errors[:10]  # Limit error display
    })

@app.route('/api/bulk_update', methods=['POST'])
def bulk_update():
    """Bulk update leads"""
    data = request.json
    lead_ids = data.get('lead_ids', [])
    updates = data.get('updates', {})
    
    if not lead_ids:
        return jsonify({'error': 'No leads selected'}), 400
    
    conn = get_db()
    c = conn.cursor()
    
    updated = 0
    for lead_id in lead_ids:
        fields = []
        values = []
        for field, value in updates.items():
            fields.append(f'{field} = ?')
            values.append(value)
        
        if fields:
            fields.append('updated_at = CURRENT_TIMESTAMP')
            values.append(lead_id)
            query = f'UPDATE leads SET {", ".join(fields)} WHERE id = ?'
            c.execute(query, values)
            updated += 1
    
    conn.commit()
    conn.close()
    
    return jsonify({'updated': updated})

# Initialize database on startup
init_db()

if __name__ == '__main__':
    print("[🖥️] Mortimer's Prospecting CRM starting on port 8088")
    app.run(host='0.0.0.0', port=8088, debug=True)
