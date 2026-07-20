#!/usr/bin/env python3
"""
Payment Thank-You Email Sender
Sends personalized payment confirmation emails to clients

Usage:
    python3 email_thankyou_sender.py --invoice=PSD-20260720-0001
    python3 email_thankyou_sender.py --all-pending
    python3 email_thankyou_sender.py --test
"""

import sqlite3
import smtplib
import os
import sys
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path

# Config
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER', 'info@psdepot.com')
SMTP_PASS = os.getenv('SMTP_PASS', '')
FROM_NAME = os.getenv('FROM_NAME', 'Performance Supply Depot')

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, 'flyer_templates', 'payment_thankyou_flyer.html')
DB_PATH = os.path.join(SCRIPT_DIR, 'crm', 'leads.db')

# Colors for terminal output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def log(msg, level='INFO'):
    colors = {'INFO': GREEN, 'WARN': YELLOW, 'ERROR': RED}
    color = colors.get(level, RESET)
    print(f"{color}[{level}]{RESET} {msg}")

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_email_log():
    """Ensure email_log table exists"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS email_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT,
            customer_email TEXT,
            customer_name TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT,
            error TEXT
        )
    ''')
    
    # Add columns if they don't exist
    try:
        c.execute('ALTER TABLE invoices ADD COLUMN thankyou_email_sent INTEGER DEFAULT 0')
    except:
        pass
    try:
        c.execute('ALTER TABLE invoices ADD COLUMN thankyou_email_sent_at TEXT')
    except:
        pass
    
    conn.commit()
    conn.close()

def load_template():
    """Load HTML template"""
    try:
        with open(TEMPLATE_PATH, 'r') as f:
            return f.read()
    except FileNotFoundError:
        log(f"Template not found: {TEMPLATE_PATH}", 'ERROR')
        return None

def personalize_template(template, data):
    """Replace placeholders with actual data"""
    replacements = {
        '{DATE}': data.get('date', datetime.now().strftime('%B %d, %Y')),
        '{REF}': data.get('ref', 'N/A'),
        '{AMOUNT}': data.get('amount', '$0.00'),
        '{METHOD}': data.get('method', 'Card'),
        '{NAME}': data.get('name', 'Valued Customer'),
    }
    
    result = template
    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)
    
    return result

def get_invoice(invoice_number):
    """Get invoice data from database"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('SELECT * FROM invoices WHERE invoice_number = ?', (invoice_number,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None

def get_pending_invoices():
    """Get all paid invoices that haven't received thank-you email"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('''
        SELECT * FROM invoices 
        WHERE status = 'paid' 
        AND thankyou_email_sent = 0
        AND customer_email IS NOT NULL
        AND customer_email != ''
        ORDER BY updated_at DESC
    ''')
    
    rows = c.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def log_email(invoice_number, email, name, status, error=''):
    """Log email to database"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO email_log (invoice_number, customer_email, customer_name, status, error)
        VALUES (?, ?, ?, ?, ?)
    ''', (invoice_number, email, name, status, error))
    
    conn.commit()
    conn.close()

def mark_email_sent(invoice_number):
    """Mark invoice as thank-you email sent"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('''
        UPDATE invoices 
        SET thankyou_email_sent = 1, 
            thankyou_email_sent_at = ?
        WHERE invoice_number = ?
    ''', (datetime.now().isoformat(), invoice_number))
    
    conn.commit()
    conn.close()

def send_email(to_email, subject, html_content, text_content=None):
    """Send email via SMTP"""
    if not SMTP_PASS:
        log("SMTP_PASS not set - email not sent", 'ERROR')
        return False
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f"{FROM_NAME} <{SMTP_USER}>"
    msg['To'] = to_email
    
    # Plain text version
    if text_content:
        msg.attach(MIMEText(text_content, 'plain'))
    
    # HTML version
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        log(f"SMTP Error: {e}", 'ERROR')
        return False

def send_payment_thankyou(invoice_number):
    """Send payment thank-you email for specific invoice"""
    log(f"{BOLD}Processing invoice: {invoice_number}{RESET}")
    
    # Get invoice data
    invoice = get_invoice(invoice_number)
    if not invoice:
        log(f"Invoice not found: {invoice_number}", 'ERROR')
        return False
    
    # Check if already sent
    if invoice.get('thankyou_email_sent'):
        log(f"Email already sent for {invoice_number}", 'WARN')
        return False
    
    # Load template
    template = load_template()
    if not template:
        return False
    
    # Prepare data
    data = {
        'date': datetime.now().strftime('%B %d, %Y'),
        'ref': invoice_number,
        'amount': f"${invoice.get('total', 0):.2f}",
        'method': invoice.get('payment_method', 'Card'),
        'name': invoice.get('customer_name', 'Valued Customer'),
    }
    
    # Personalize
    html_content = personalize_template(template, data)
    
    # Plain text fallback
    text_content = f"""
Thank You for Your Payment!

Dear {data['name']},

We want to express our sincere gratitude for your recent payment.

Invoice: {invoice_number}
Amount: {data['amount']}
Date: {data['date']}

Your payment has been successfully processed. We truly appreciate your business!

Questions? We're here to help:
Email: info@psdepot.com
Phone: 888-881-6834
Website: psdepot.com

Best regards,
{FROM_NAME}
"""
    
    # Send email
    subject = f"Thank You! Payment Received - Invoice {invoice_number}"
    to_email = invoice.get('customer_email')
    
    if not to_email:
        log(f"No email address for {invoice_number}", 'ERROR')
        return False
    
    log(f"Sending to: {to_email}")
    
    success = send_email(to_email, subject, html_content, text_content)
    
    if success:
        log(f"Email sent successfully!", 'INFO')
        mark_email_sent(invoice_number)
        log_email(invoice_number, to_email, data['name'], 'sent')
        return True
    else:
        log_email(invoice_number, to_email, data['name'], 'failed')
        return False

def send_test_email():
    """Send test email to configured address"""
    log("Sending test email...")
    
    template = load_template()
    if not template:
        return False
    
    data = {
        'date': datetime.now().strftime('%B %d, %Y'),
        'ref': 'TEST-001',
        'amount': '$500.00',
        'method': 'Test',
        'name': 'Captain',
    }
    
    html_content = personalize_template(template, data)
    
    # Send to self or test address
    test_email = os.getenv('TEST_EMAIL', SMTP_USER)
    subject = "TEST: Thank You for Your Payment"
    
    success = send_email(test_email, subject, html_content)
    
    if success:
        log(f"Test email sent to {test_email}", 'INFO')
    else:
        log("Test email failed", 'ERROR')
    
    return success

def main():
    parser = argparse.ArgumentParser(description='Payment Thank-You Email Sender')
    parser.add_argument('--invoice', help='Send email for specific invoice')
    parser.add_argument('--all-pending', action='store_true', help='Send to all pending invoices')
    parser.add_argument('--test', action='store_true', help='Send test email')
    parser.add_argument('--list', action='store_true', help='List pending invoices')
    
    args = parser.parse_args()
    
    # Initialize
    init_email_log()
    
    if args.test:
        send_test_email()
    elif args.invoice:
        send_payment_thankyou(args.invoice)
    elif args.all_pending:
        pending = get_pending_invoices()
        log(f"{BOLD}Found {len(pending)} pending invoices{RESET}")
        
        for invoice in pending:
            print()
            send_payment_thankyou(invoice['invoice_number'])
    elif args.list:
        pending = get_pending_invoices()
        log(f"{BOLD}Pending invoices ({len(pending)}):{RESET}")
        for inv in pending:
            print(f"  - {inv['invoice_number']}: {inv.get('customer_name', 'Unknown')} ({inv.get('customer_email', 'No email')})")
    else:
        parser.print_help()
        print()
        log("Examples:", 'INFO')
        print("  python3 email_thankyou_sender.py --invoice=PSD-20260720-0001")
        print("  python3 email_thankyou_sender.py --all-pending")
        print("  python3 email_thankyou_sender.py --test")
        print("  python3 email_thankyou_sender.py --list")

if __name__ == '__main__':
    main()
