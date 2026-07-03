#!/usr/bin/env python3
"""
🖥️ Mortimer's PSDEPOT CRM - Backend API
Flask-based REST API for Lead Management, Invoicing & Products
"""

from flask import Flask, request, jsonify, send_from_directory, Response
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

# Import modules
from products import PRODUCTS, SERVICES, CATEGORIES, calculate_order
from invoices import (
    init_invoices_db, create_invoice, get_invoice, get_invoices,
    update_invoice_status, get_invoice_stats, generate_html
)

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with leads from CSV"""
    conn = get_db()
    c = conn.cursor()
    
    # Create leads table
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
    init_invoices_db()

# ============== STATIC FILES ==============

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/invoices')
def invoices_page():
    return send_from_directory('static', 'invoices.html')

# ============== LEADS API ==============

@app.route('/api/stats')
def stats():
    """Get overall statistics"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM leads')
    total = c.fetchone()[0]
    
    c.execute('SELECT category_type, COUNT(*) as count FROM leads GROUP BY category_type ORDER BY count DESC')
    categories = [dict(row) for row in c.fetchall()]
    
    c.execute('SELECT status, COUNT(*) as count FROM leads GROUP BY status')
    statuses = [dict(row) for row in c.fetchall()]
    
    c.execute('SELECT city, COUNT(*) as count FROM leads WHERE city != "" GROUP BY city ORDER BY count DESC LIMIT 20')
    cities = [dict(row) for row in c.fetchall()]
    
    c.execute('SELECT COUNT(*) FROM leads WHERE phone != "" AND phone IS NOT NULL')
    with_phone = c.fetchone()[0]
    
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
    
    category = request.args.get('category', 'all')
    status = request.args.get('status', 'all')
    city = request.args.get('city', '')
    search = request.args.get('search', '')
    has_phone = request.args.get('has_phone', 'false') == 'true'
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    
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
    
    query += ' ORDER BY name LIMIT ? OFFSET ?'
    params.extend([per_page, (page - 1) * per_page])
    
    c = conn.cursor()
    c.execute(count_query, params[:-(2 if has_phone else 0)] if has_phone else params)
    total = c.fetchone()[0]
    
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
def api_create_lead():
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
def api_update_lead(lead_id):
    """Update lead"""
    data = request.json
    
    conn = get_db()
    c = conn.cursor()
    
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
def api_delete_lead(lead_id):
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
    
    return jsonify({'imported': imported, 'errors': errors[:10]})

# ============== PRODUCTS API ==============

@app.route('/api/products')
def get_products():
    """Get all products and services"""
    result = []
    
    for key, product in PRODUCTS.items():
        result.append({
            'sku': product['sku'],
            'name': product['name'],
            'description': product['description'],
            'category': product['category'],
            'price': product['price_per_unit'],
            'unit': product.get('unit', 'each'),
            'min_order': product.get('min_order', 1)
        })
    
    for key, service in SERVICES.items():
        result.append({
            'sku': service['sku'],
            'name': service['name'],
            'description': service['description'],
            'category': service['category'],
            'price': service['price_per_unit'],
            'unit': service.get('unit', 'hour'),
            'min_order': service.get('min_order', 1)
        })
    
    return jsonify(result)

@app.route('/api/products/<sku>')
def get_product(sku):
    """Get single product by SKU"""
    for key, product in PRODUCTS.items():
        if product['sku'] == sku:
            return jsonify({
                'sku': product['sku'],
                'name': product['name'],
                'description': product['description'],
                'category': product['category'],
                'price': product['price_per_unit'],
                'unit': product.get('unit', 'each')
            })
    
    for key, service in SERVICES.items():
        if service['sku'] == sku:
            return jsonify({
                'sku': service['sku'],
                'name': service['name'],
                'description': service['description'],
                'category': service['category'],
                'price': service['price_per_unit'],
                'unit': service.get('unit', 'hour')
            })
    
    return jsonify({'error': 'Product not found'}), 404

@app.route('/api/products/categories')
def get_product_categories():
    """Get product categories"""
    return jsonify(CATEGORIES)

@app.route('/api/calculate', methods=['POST'])
def calc_order():
    """Calculate order total"""
    items = request.json.get('items', [])
    return jsonify(calculate_order(items))

# ============== INVOICES API ==============

@app.route('/api/invoices')
def api_get_invoices():
    """Get all invoices"""
    invoices = get_invoices()
    return jsonify(invoices)

@app.route('/api/invoices/stats')
def api_invoice_stats():
    """Get invoice statistics"""
    return jsonify(get_invoice_stats())

@app.route('/api/invoices/<int:invoice_id>')
def api_get_invoice(invoice_id):
    """Get single invoice"""
    invoice = get_invoice(invoice_id)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404
    return jsonify(invoice)

@app.route('/api/invoices', methods=['POST'])
def api_create_invoice():
    """Create new invoice"""
    data = request.json
    
    # Convert line items format
    items = []
    for item in data.get('items', []):
        items.append({
            'sku': item.get('sku', ''),
            'quantity': item.get('quantity', 1)
        })
    
    result = create_invoice(
        lead_id=data.get('lead_id'),
        customer_name=data.get('customer_name', ''),
        customer_email=data.get('customer_email', ''),
        customer_phone=data.get('customer_phone', ''),
        address=data.get('address', ''),
        city=data.get('city', ''),
        state=data.get('state', 'CA'),
        zip_code=data.get('zip_code', ''),
        items=items,
        notes=data.get('notes', '')
    )
    
    return jsonify(result)

@app.route('/api/invoices/<int:invoice_id>', methods=['PUT'])
def api_update_invoice(invoice_id):
    """Update invoice"""
    data = request.json
    
    conn = get_db()
    c = conn.cursor()
    
    fields = []
    values = []
    
    for field in ['customer_name', 'customer_email', 'customer_phone',
                  'billing_address', 'billing_city', 'billing_state', 'billing_zip',
                  'notes']:
        if field in data:
            fields.append(f'{field} = ?')
            values.append(data[field])
    
    if fields:
        fields.append('updated_at = CURRENT_TIMESTAMP')
        values.append(invoice_id)
        query = f'UPDATE invoices SET {", ".join(fields)} WHERE id = ?'
        c.execute(query, values)
        conn.commit()
    
    conn.close()
    return jsonify({'success': True})

@app.route('/api/invoices/<int:invoice_id>', methods=['DELETE'])
def api_delete_invoice(invoice_id):
    """Delete invoice"""
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM invoices WHERE id = ?', (invoice_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/invoices/<int:invoice_id>/status', methods=['PUT'])
def api_update_invoice_status(invoice_id):
    """Update invoice status"""
    data = request.json
    status = data.get('status', 'draft')
    update_invoice_status(invoice_id, status)
    return jsonify({'success': True})

@app.route('/api/invoices/<int:invoice_id>/html')
def api_invoice_html(invoice_id):
    """Get invoice as HTML"""
    invoice = get_invoice(invoice_id)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404
    
    html = generate_html(invoice)
    return Response(html, mimetype='text/html')

# ============== BULK OPERATIONS ==============

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
    print("""
╔═══════════════════════════════════════════════════════════╗
║  🖥️ Mortimer's PSDEPOT CRM                                 ║
║  Lead Management + Products + Invoicing                    ║
║  Running on http://localhost:8088                          ║
╠═══════════════════════════════════════════════════════════╣
║  📋 Leads:     http://localhost:8088/                     ║
║  🧾 Invoices:  http://localhost:8088/invoices             ║
║  📊 API:       http://localhost:8088/api/                 ║
╚═══════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=8090, debug=True)
