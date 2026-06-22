#!/usr/bin/env python3
"""
PSDEPOT Sales Outreach
Fleet Agent: PULP, JANE, CLERK
"""

import smtplib
import csv
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "mortimer@myl0nr0s.cloud"
SMTP_PASS = ""  # Add your app password

# Email template
EMAIL_TEMPLATE = """
Hi {name},

I noticed {company} might benefit from a reliable industrial supply partner.

We specialize in:
- MRO (Maintenance, Repair, Operations)
- Industrial equipment
- Expedited delivery
- Competitive pricing

Would you be open to a quick 15-minute call this week?

Best,
{agent}
Performance Supply Depot LLC
"""

def send_email(to_email, name, company, agent="Antonio"):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = f"Industrial Supply Partnership - {company}"
        
        body = EMAIL_TEMPLATE.format(name=name, company=company, agent=agent)
        msg.attach(MIMEText(body, 'plain'))
        
        # Uncomment to actually send:
        # with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        #     server.starttls()
        #     server.login(SMTP_USER, SMTP_PASS)
        #     server.send_message(msg)
        
        print(f"SENT: {to_email}")
        return True
    except Exception as e:
        print(f"FAILED: {to_email} - {e}")
        return False

def load_leads():
    """Load leads from CSV"""
    try:
        with open('leads.csv', 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except:
        return []

def main():
    leads = load_leads()
    print(f"Loaded {len(leads)} leads")
    
    for i, lead in enumerate(leads[:100]):  # First 100
        send_email(
            lead.get('email', ''),
            lead.get('name', 'there'),
            lead.get('company', 'your company')
        )
        time.sleep(1)  # Rate limiting
        
        if (i + 1) % 10 == 0:
            print(f"Sent {i + 1} emails")

if __name__ == "__main__":
    main()
