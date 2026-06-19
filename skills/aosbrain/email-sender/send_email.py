#!/usr/bin/env python3
"""
Email Sender - Miles Hostinger Account
Uses smtplib with TLS encryption
"""

import smtplib
import os
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path

def load_credentials():
    """Load email credentials from secure file"""
    creds_path = Path.home() / ".openclaw" / "workspace" / ".miles_email_creds"
    if creds_path.exists():
        with open(creds_path) as f:
            return json.load(f)
    # Fallback to env vars
    return {
        "email": os.getenv("HOSTINGER_SMTP_USER", "miles@myl0nr0s.cloud"),
        "password": os.getenv("HOSTINGER_SMTP_PASS"),
        "provider": "hostinger"
    }

def send_email(to, subject, body=None, html_body=None, attachments=None, cc=None, bcc=None):
    """
    Send email via Miles' Hostinger account
    
    Args:
        to: Recipient email(s) - str or list
        subject: Email subject
        body: Plain text body (optional if html_body provided)
        html_body: HTML body (optional)
        attachments: List of file paths to attach
        cc: CC recipient(s)
        bcc: BCC recipient(s)
    
    Returns:
        dict: {'success': True/False, 'message': '...'}
    """
    creds = load_credentials()
    
    if not creds.get("password"):
        return {"success": False, "message": "Email credentials not found"}
    
    # SMTP config for Hostinger
    smtp_server = "smtp.hostinger.com"
    smtp_port = 587
    
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg['From'] = f"Miles <{creds['email']}>"
        msg['Subject'] = subject
        
        # Handle recipients
        if isinstance(to, list):
            msg['To'] = ", ".join(to)
        else:
            msg['To'] = to
            
        if cc:
            if isinstance(cc, list):
                msg['Cc'] = ", ".join(cc)
            else:
                msg['Cc'] = cc
                
        # Build recipient list for SMTP
        recipients = []
        if isinstance(to, list):
            recipients.extend(to)
        else:
            recipients.append(to)
        if cc:
            if isinstance(cc, list):
                recipients.extend(cc)
            else:
                recipients.append(cc)
        if bcc:
            if isinstance(bcc, list):
                recipients.extend(bcc)
            else:
                recipients.append(bcc)
        
        # Attach body parts
        if body:
            msg.attach(MIMEText(body, "plain"))
        if html_body:
            msg.attach(MIMEText(html_body, "html"))
        
        # Handle attachments
        if attachments:
            for filepath in attachments:
                if os.path.exists(filepath):
                    with open(filepath, "rb") as f:
                        part = MIMEApplication(f.read())
                        part.add_header(
                            "Content-Disposition",
                            f"attachment; filename= {os.path.basename(filepath)}"
                        )
                        msg.attach(part)
        
        # Send via SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(creds["email"], creds["password"])
            server.send_message(msg, from_addr=creds["email"], to_addrs=recipients)
        
        return {
            "success": True, 
            "message": f"Email sent to {msg['To']}",
            "recipients": recipients
        }
        
    except Exception as e:
        return {"success": False, "message": f"Failed to send: {str(e)}"}


if __name__ == "__main__":
    # Test send
    result = send_email(
        to="info@psdepot.com",
        subject="Test from Miles Email Skill",
        body="This is a test email from the email sender skill.",
        html_body="<h1>Test</h1><p>This is a test email.</p>"
    )
    print(result)
