#!/usr/bin/env python3
"""Psdepot Email Campaign Sender v2"""

import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configuration
SENDER_NAME = "Performance Supply Depot"
SENDER_EMAIL = "info@psdepot.com"
BCC_EMAIL = "bcc@psdepot.com"
PHONE = "888-881-6834"
WEBSITE = "https://psdepot.com"
DB = "/data/data/com.termux/files/home/mortimer/software/depotchaos/depot_chaos.db"

# HTML Email Template
HTML_TEMPLATE = """
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
  <div style="background: #1a365d; color: white; padding: 20px; text-align: center;">
    <h1 style="margin: 0;">🖥️ Performance Supply Depot</h1>
    <p style="margin: 5px 0 0 0;">Your Business Supply Partner</p>
  </div>
  
  <div style="padding: 30px 20px; background: #f7fafc;">
    <h2 style="color: #2d3748;">Dear {name},</h2>
    
    <p style="color: #4a5568; line-height: 1.6;">
      We're reaching out because you're part of the Performance Supply Depot family.
      As a valued customer in the restaurant industry, we want to make sure you know
      about <strong>psdepot.com</strong> — your direct source for commercial supplies.
    </p>
    
    <div style="background: white; border-left: 4px solid #3182ce; padding: 20px; margin: 20px 0;">
      <h3 style="color: #2d3748; margin-top: 0;">What We Offer:</h3>
      <ul style="color: #4a5568;">
        <li>✓ Restaurant equipment & parts</li>
        <li>✓ Cleaning & sanitation supplies</li>
        <li>✓ Packaging materials</li>
        <li>✓ Kitchen essentials</li>
        <li>✓ And much more!</li>
      </ul>
    </div>
    
    <div style="background: #48bb78; color: white; padding: 15px; text-align: center; border-radius: 5px;">
      <h3 style="margin: 0 0 10px 0;">Why Choose Us?</h3>
      <p style="margin: 0;">
        ✅ Competitive wholesale pricing<br>
        ✅ Fast shipping on most orders<br>
        ✅ Business accounts available<br>
        ✅ Expert customer service
      </p>
    </div>
    
    <div style="text-align: center; margin: 30px 0;">
      <a href="{website}" style="background: #3182ce; color: white; padding: 15px 40px; text-decoration: none; border-radius: 5px; font-size: 18px; font-weight: bold;">
        Visit psdepot.com →
      </a>
    </div>
    
    <p style="color: #4a5568; line-height: 1.6;">
      Questions? Call us: <strong>{phone}</strong> or reply to this email.
    </p>
    
    <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;">
    
    <p style="color: #718096; font-size: 12px;">
      Performance Supply Depot LLC<br>
      📞 {phone}<br>
      🌐 <a href="{website}">{website}</a>
    </p>
  </div>
  
  <div style="background: #2d3748; color: #a0aec0; padding: 15px; text-align: center; font-size: 11px;">
    You're receiving this because you're a valued customer. | 
    <a href="#" style="color: #63b3ed;">Unsubscribe</a>
  </div>
</body>
</html>
"""

# Plain text template
TEXT_TEMPLATE = """
PERFORMANCE SUPPLY DEPOT
Your Business Supply Partner
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Dear {name},

We're reaching out because you're part of the Performance Supply 
Depot family. As a valued customer in the restaurant industry, 
we want to make sure you know about psdepot.com — your direct 
source for commercial supplies.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT WE OFFER:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Restaurant equipment & parts
✓ Cleaning & sanitation supplies  
✓ Packaging materials
✓ Kitchen essentials
✓ And much more!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHY CHOOSE US?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Competitive wholesale pricing
✅ Fast shipping on most orders
✅ Business accounts available
✅ Expert customer service

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👉 VISIT: {website}

Questions? Call us: {phone}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Performance Supply Depot LLC
📞 {phone}
🌐 {website}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You're receiving this because you're a valued customer.
"""

def get_customers(state='CA', limit=100, offset=0):
    """Get customers from database"""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, dba_name, contact_name, email, city, state
        FROM vendors 
        WHERE state = ? AND status = 'active'
        LIMIT ? OFFSET ?
    """, (state, limit, offset))
    results = cursor.fetchall()
    conn.close()
    return results

def create_email(to_email, to_name, template_type='initial'):
    """Create email message"""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"{to_name} — Your Supply Partner is Here"
    msg['From'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg['To'] = to_email
    msg['Bcc'] = BCC_EMAIL
    
    # Fill templates
    html = HTML_TEMPLATE.format(name=to_name, phone=PHONE, website=WEBSITE)
    text = TEXT_TEMPLATE.format(name=to_name, phone=PHONE, website=WEBSITE)
    
    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html, 'html'))
    
    return msg

def send_email(msg, smtp_config=None):
    """Send email via SMTP (stub - needs config)"""
    print(f"  📧 To: {msg['To']}")
    print(f"     Subject: {msg['Subject']}")
    return True

def run_campaign(state='CA', batch_size=100, dry_run=True):
    """Run email campaign"""
    customers = get_customers(state, batch_size)
    print(f"\n📧 CAMPAIGN: {state} ({len(customers)} recipients)")
    print(f"   Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"   From: {SENDER_EMAIL}")
    print(f"   BCC: {BCC_EMAIL}")
    print("-" * 50)
    
    sent = 0
    for cust in customers:
        if cust[4]:  # Has email
            name = cust[1] or cust[2] or "Partner"
            msg = create_email(cust[4], name)
            send_email(msg)
            sent += 1
    
    print(f"\n✅ Would send {sent} emails")
    return sent

if __name__ == "__main__":
    print("=" * 50)
    print("📧 PSDEPOT MARKETING CAMPAIGN v2")
    print(f"   Phone: {PHONE}")
    print(f"   Website: {WEBSITE}")
    print("=" * 50)
    
    # Test run
    run_campaign('CA', 5, dry_run=True)
