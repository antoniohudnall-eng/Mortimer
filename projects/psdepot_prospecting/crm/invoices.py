#!/usr/bin/env python3
"""
PSDEPOT Invoice Generator
Creates professional invoices for Performance Supply Depot LLC
"""

import sqlite3
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from products import PRODUCTS, SERVICES, CATEGORIES, calculate_order

# Invoice database
INVOICES_DIR = os.path.join(os.path.dirname(__file__), 'invoices')

def get_db():
    """Get database connection"""
    db_path = os.path.join(os.path.dirname(__file__), 'leads.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_invoices_db():
    """Initialize invoices table"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT UNIQUE NOT NULL,
            lead_id INTEGER,
            customer_name TEXT,
            customer_email TEXT,
            customer_phone TEXT,
            billing_address TEXT,
            billing_city TEXT,
            billing_state TEXT,
            billing_zip TEXT,
            items_json TEXT,
            subtotal REAL,
            discount REAL DEFAULT 0,
            tax REAL,
            total REAL,
            status TEXT DEFAULT 'draft',
            due_date TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def generate_invoice_number():
    """Generate unique invoice number"""
    today = datetime.now()
    prefix = f"PSD-{today.strftime('%Y%m%d')}-"
    
    conn = get_db()
    c = conn.cursor()
    
    # Get last invoice number for today
    c.execute('''
        SELECT invoice_number FROM invoices 
        WHERE invoice_number LIKE ? 
        ORDER BY id DESC LIMIT 1
    ''', (f'{prefix}%',))
    
    row = c.fetchone()
    conn.close()
    
    if row:
        last_num = int(row[0].split('-')[-1])
        new_num = last_num + 1
    else:
        new_num = 1
    
    return f"{prefix}{new_num:04d}"

def create_invoice(lead_id=None, customer_name="", customer_email="", customer_phone="",
                   address="", city="", state="CA", zip_code="",
                   items=None, notes=""):
    """Create a new invoice"""
    if items is None:
        items = []
    
    # Calculate totals
    calc = calculate_order(items)
    
    # Generate invoice number
    invoice_number = generate_invoice_number()
    
    # Due date is 30 days from now
    due_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO invoices (
            invoice_number, lead_id, customer_name, customer_email, customer_phone,
            billing_address, billing_city, billing_state, billing_zip,
            items_json, subtotal, discount, tax, total, due_date, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        invoice_number,
        lead_id,
        customer_name,
        customer_email,
        customer_phone,
        address,
        city,
        state,
        zip_code,
        json.dumps(items),
        calc['subtotal'],
        calc['discount'],
        calc['tax'],
        calc['total'],
        due_date,
        notes
    ))
    
    invoice_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return {
        'id': invoice_id,
        'invoice_number': invoice_number,
        'total': calc['total']
    }

def get_invoice(invoice_id=None, invoice_number=None):
    """Get invoice by ID or number"""
    conn = get_db()
    c = conn.cursor()
    
    if invoice_id:
        c.execute('SELECT * FROM invoices WHERE id = ?', (invoice_id,))
    else:
        c.execute('SELECT * FROM invoices WHERE invoice_number = ?', (invoice_number,))
    
    row = c.fetchone()
    conn.close()
    
    if not row:
        return None
    
    invoice = dict(row)
    invoice['items'] = json.loads(invoice['items_json'])
    return invoice

def get_invoices(status=None, limit=50, offset=0):
    """Get list of invoices"""
    conn = get_db()
    c = conn.cursor()
    
    query = 'SELECT * FROM invoices'
    params = []
    
    if status:
        query += ' WHERE status = ?'
        params.append(status)
    
    query += ' ORDER BY created_at DESC LIMIT ? OFFSET ?'
    params.extend([limit, offset])
    
    c.execute(query, params)
    invoices = [dict(row) for row in c.fetchall()]
    conn.close()
    
    # Parse items JSON
    for inv in invoices:
        inv['items'] = json.loads(inv['items_json'])
    
    return invoices

def update_invoice_status(invoice_id, status):
    """Update invoice status"""
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE invoices SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', 
              (status, invoice_id))
    conn.commit()
    conn.close()

def get_invoice_stats():
    """Get invoice statistics"""
    conn = get_db()
    c = conn.cursor()
    
    stats = {}
    
    # Total invoices
    c.execute('SELECT COUNT(*) FROM invoices')
    stats['total'] = c.fetchone()[0]
    
    # By status
    c.execute('SELECT status, COUNT(*), SUM(total) FROM invoices GROUP BY status')
    stats['by_status'] = {}
    for row in c.fetchall():
        stats['by_status'][row[0]] = {'count': row[1], 'total': row[2] or 0}
    
    # This month
    c.execute('''SELECT COUNT(*), SUM(total) FROM invoices 
                 WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')''')
    row = c.fetchone()
    stats['this_month'] = {'count': row[0], 'total': row[1] or 0}
    
    # Outstanding (not paid)
    c.execute('''SELECT COUNT(*), SUM(total) FROM invoices 
                 WHERE status NOT IN ('paid', 'cancelled')''')
    row = c.fetchone()
    stats['outstanding'] = {'count': row[0], 'total': row[1] or 0}
    
    conn.close()
    return stats

def generate_pdf(invoice):
    """Generate PDF invoice"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.units import inch
    except ImportError:
        return None  # reportlab not installed
    
    os.makedirs(INVOICES_DIR, exist_ok=True)
    filename = f"{invoice['invoice_number']}.pdf"
    filepath = os.path.join(INVOICES_DIR, filename)
    
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    elements = []
    
    # Header
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#e94560')
    )
    
    elements.append(Paragraph("INVOICE", title_style))
    elements.append(Spacer(1, 12))
    
    # Invoice info table
    info_data = [
        ['Invoice Number:', invoice['invoice_number']],
        ['Date:', datetime.strptime(invoice['created_at'], '%Y-%m-%d %H:%M:%S').strftime('%B %d, %Y')],
        ['Due Date:', datetime.strptime(invoice['due_date'], '%Y-%m-%d').strftime('%B %d, %Y')],
        ['Status:', invoice['status'].upper()],
    ]
    
    info_table = Table(info_data, colWidths=[150, 200])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 30))
    
    # Bill To
    elements.append(Paragraph("BILL TO:", styles['Normal']))
    elements.append(Paragraph(invoice['customer_name'], styles['Heading3']))
    if invoice.get('billing_address'):
        elements.append(Paragraph(invoice['billing_address'], styles['Normal']))
    if invoice.get('billing_city'):
        city_line = f"{invoice['billing_city']}, {invoice['billing_state']} {invoice['billing_zip']}"
        elements.append(Paragraph(city_line, styles['Normal']))
    if invoice.get('customer_email'):
        elements.append(Paragraph(invoice['customer_email'], styles['Normal']))
    elements.append(Spacer(1, 30))
    
    # Items table
    items_header = ['Item', 'Qty', 'Unit Price', 'Total']
    items_data = [items_header]
    
    for item in invoice['items']:
        items_data.append([
            item['name'],
            str(item['quantity']),
            f"${item['unit_price']:.2f}",
            f"${item['line_total']:.2f}"
        ])
    
    items_table = Table(items_data, colWidths=[300, 60, 90, 90])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 20))
    
    # Totals
    totals_data = [
        ['Subtotal:', f"${invoice['subtotal']:.2f}"],
    ]
    
    if invoice.get('discount', 0) > 0:
        totals_data.append([f"Discount ({invoice.get('discount_percent', 10)}%):", f"-${invoice['discount']:.2f}"])
    
    totals_data.append(['Tax (8.25%):', f"${invoice['tax']:.2f}"])
    totals_data.append(['TOTAL:', f"${invoice['total']:.2f}"])
    
    totals_table = Table(totals_data, colWidths=[420, 120])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#e94560')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(totals_table)
    elements.append(Spacer(1, 40))
    
    # Notes
    if invoice.get('notes'):
        elements.append(Paragraph("Notes:", styles['Normal']))
        elements.append(Paragraph(invoice['notes'], styles['Normal']))
    
    # Footer
    elements.append(Spacer(1, 40))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey
    )
    elements.append(Paragraph("Thank you for your business!", footer_style))
    elements.append(Paragraph("Performance Supply Depot LLC", footer_style))
    elements.append(Paragraph("Phone: (800) 555-0123 | Email: orders@psdepot.com", footer_style))
    
    doc.build(elements)
    return filepath

def generate_html(invoice):
    """Generate HTML invoice for viewing"""
    items_html = ""
    for item in invoice['items']:
        items_html += f"""
        <tr>
            <td>{item['name']}</td>
            <td style="text-align:center;">{item['quantity']}</td>
            <td style="text-align:right;">${item['unit_price']:.2f}</td>
            <td style="text-align:right;">${item['line_total']:.2f}</td>
        </tr>
        """
    
    status_color = {
        'draft': '#888',
        'sent': '#3b82f6',
        'paid': '#10b981',
        'overdue': '#ef4444',
        'cancelled': '#666'
    }.get(invoice['status'], '#888')
    
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Invoice {invoice['invoice_number']}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f5f5f5; padding: 40px; }}
        .invoice {{ max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ display: flex; justify-content: space-between; margin-bottom: 40px; }}
        .logo {{ font-size: 28px; font-weight: bold; color: #e94560; }}
        .invoice-meta {{ text-align: right; }}
        .invoice-number {{ font-size: 20px; color: #333; font-weight: 600; }}
        .status {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; text-transform: uppercase; background: {status_color}; color: white; }}
        .addresses {{ display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-bottom: 40px; }}
        .addresses h3 {{ font-size: 12px; color: #888; text-transform: uppercase; margin-bottom: 10px; }}
        .addresses p {{ margin: 5px 0; color: #333; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
        th {{ background: #1a1a2e; color: white; padding: 15px; text-align: left; font-size: 12px; text-transform: uppercase; }}
        th:last-child, td:last-child {{ text-align: right; }}
        td {{ padding: 15px; border-bottom: 1px solid #eee; }}
        .totals {{ margin-left: auto; width: 300px; }}
        .totals-row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; }}
        .totals-row.total {{ border-bottom: none; font-size: 18px; font-weight: bold; color: #e94560; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; color: #888; font-size: 12px; text-align: center; }}
        .print-btn {{ background: #e94560; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 14px; margin-top: 20px; }}
        .print-btn:hover {{ background: #ff6b6b; }}
        @media print {{ body {{ padding: 0; }} .print-btn {{ display: none; }} }}
    </style>
</head>
<body>
    <div class="invoice">
        <div class="header">
            <div>
                <div class="logo">🖥️ PSDEPOT</div>
                <p>Performance Supply Depot LLC</p>
                <p>orders@psdepot.com</p>
            </div>
            <div class="invoice-meta">
                <div class="invoice-number">Invoice {invoice['invoice_number']}</div>
                <p>Date: {datetime.strptime(invoice['created_at'], '%Y-%m-%d %H:%M:%S').strftime('%B %d, %Y')}</p>
                <p>Due: {datetime.strptime(invoice['due_date'], '%Y-%m-%d').strftime('%B %d, %Y')}</p>
                <p><span class="status">{invoice['status']}</span></p>
            </div>
        </div>
        
        <div class="addresses">
            <div>
                <h3>Bill To</h3>
                <p><strong>{invoice['customer_name']}</strong></p>
                {f"<p>{invoice['billing_address']}</p>" if invoice.get('billing_address') else ""}
                {f"<p>{invoice['billing_city']}, {invoice['billing_state']} {invoice['billing_zip']}</p>" if invoice.get('billing_city') else ""}
                {f"<p>{invoice['customer_email']}</p>" if invoice.get('customer_email') else ""}
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Item</th>
                    <th style="text-align:center;">Qty</th>
                    <th style="text-align:right;">Unit Price</th>
                    <th style="text-align:right;">Total</th>
                </tr>
            </thead>
            <tbody>
                {items_html}
            </tbody>
        </table>
        
        <div class="totals">
            <div class="totals-row">
                <span>Subtotal</span>
                <span>${invoice['subtotal']:.2f}</span>
            </div>
            {f"<div class='totals-row' style='color:#10b981'><span>Discount ({invoice.get('discount_percent', 10)}%)</span><span>-${invoice['discount']:.2f}</span></div>" if invoice.get('discount', 0) > 0 else ""}
            <div class="totals-row">
                <span>Tax (8.25%)</span>
                <span>${invoice['tax']:.2f}</span>
            </div>
            <div class="totals-row total">
                <span>Total</span>
                <span>${invoice['total']:.2f}</span>
            </div>
        </div>
        
        {f"<p style='margin-top:30px; color:#666;'><strong>Notes:</strong> {invoice['notes']}</p>" if invoice.get('notes') else ""}
        
        <button class="print-btn" onclick="window.print()">🖨️ Print Invoice</button>
    </div>
</body>
</html>
"""

# Initialize on import
init_invoices_db()

if __name__ == "__main__":
    print("Invoice system ready")
    print(f"Invoices directory: {INVOICES_DIR}")
