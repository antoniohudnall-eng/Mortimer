#!/usr/bin/env python3
"""
PSDEPOT Marketing Email Sender
Full SMTP support with dry-run mode
"""

import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import sys

# ============================================
# CONFIG - UPDATE THESE
# ============================================
CONFIG = {
    "from_email": "performancedepot@gmail.com",
    "from_name": "Performance Supply Depot",
    "bcc_email": "bcc@psdepot.com",
    "phone": "888-881-6834",
    "website": "https://psdepot.com",
    "dry_run": False,  # True = preview only, False = actually send
    
    # Gmail SMTP (easiest setup)
    # Get app password: https://myaccount.google.com/apppasswords
    "smtp": {
        "server": "smtp.gmail.com",
        "port": 587,
        "username": "performancedepot@gmail.com",
        "password": "P3rformance!",  # <-- SET YOUR APP PASSWORD HERE
    }
}

# ============================================
# EMAIL TEMPLATES
# ============================================
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
    
    <p style="color: #4a5568;">
      Questions? Call us: <strong>{phone}</strong>
    </p>
    
    <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;">
    
    <p style="color: #718096; font-size: 12px;">
      Performance Supply Depot LLC<br>
      📞 {phone} | 🌐 {website}
    </p>
  </div>
</body>
</html>
"""

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
✓ Restaurant equipment & parts
✓ Cleaning & sanitation supplies  
✓ Packaging materials
✓ Kitchen essentials
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHY CHOOSE US?
✅ Competitive wholesale pricing
✅ Fast shipping on most orders
✅ Business accounts available
✅ Expert customer service
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👉 VISIT: {website}
📞 CALL: {phone}

Performance Supply Depot LLC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ============================================
# FUNCTIONS
# ============================================
DB_PATH = "/data/data/com.termux/files/home/mortimer/software/depotchaos/depot_chaos.db"

def get_customers(state='CA', limit=100, offset=0):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, dba_name, contact_name, email, city, state
        FROM vendors 
        WHERE state = ? AND status = 'active' AND email IS NOT NULL
        LIMIT ? OFFSET ?
    """, (state, limit, offset))
    results = cursor.fetchall()
    conn.close()
    return results

def create_email(to_email, to_name):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"{to_name} — Your Supply Partner is Here"
    msg['From'] = f"{CONFIG['from_name']} <{CONFIG['from_email']}>"
    msg['To'] = to_email
    msg['Bcc'] = CONFIG['bcc_email']
    
    html = HTML_TEMPLATE.format(name=to_name, phone=CONFIG['phone'], website=CONFIG['website'])
    text = TEXT_TEMPLATE.format(name=to_name, phone=CONFIG['phone'], website=CONFIG['website'])
    
    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html, 'html'))
    return msg

def send_via_smtp(msg):
    try:
        server = smtplib.SMTP(CONFIG['smtp']['server'], CONFIG['smtp']['port'])
        server.starttls()
        server.login(CONFIG['smtp']['username'], CONFIG['smtp']['password'])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"    ❌ SMTP Error: {e}")
        return False

def run_campaign(state='CA', batch_size=500):
    customers = get_customers(state, batch_size)
    mode = "🔍 DRY RUN" if CONFIG['dry_run'] else "🚀 LIVE"
    
    print(f"\n{'='*60}")
    print(f"📧 PSDEPOT MARKETING CAMPAIGN")
    print(f"{'='*60}")
    print(f"   Mode: {mode}")
    print(f"   State: {state}")
    print(f"   Recipients: {len(customers)}")
    print(f"   From: {CONFIG['from_email']}")
    print(f"{'='*60}\n")
    
    sent = 0
    failed = 0
    
    for cust in customers:
        email = cust[4]
        name = cust[1] or cust[2] or "Partner"
        
        msg = create_email(email, name)
        
        if CONFIG['dry_run']:
            print(f"  📧 {name}")
            print(f"     → {email}")
            sent += 1
        else:
            if send_via_smtp(msg):
                print(f"  ✅ {name} → {email}")
                sent += 1
            else:
                print(f"  ❌ Failed: {email}")
                failed += 1
    
    print(f"\n{'='*60}")
    print(f"📊 RESULTS")
    print(f"{'='*60}")
    print(f"   Sent: {sent}")
    if not CONFIG['dry_run']:
        print(f"   Failed: {failed}")
    print(f"{'='*60}\n")
    
    return sent

# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║         📧 PSDEPOT EMAIL MARKETING SENDER            ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Run CA campaign
    run_campaign('CA', 500)
    
    # Uncomment to run TX campaign too:
    # run_campaign('TX', 500)
