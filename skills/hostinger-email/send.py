#!/usr/bin/env python3
"""
Hostinger Email Sender — Mortimer & Miles
SMTP: smtp.hostinger.com:587 (STARTTLS)
"""

import smtplib
import sys
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ── Credentials ────────────────────────────────────────────
ACCOUNTS = {
    "mortimer": {
        "email": "mortimer@myl0nr0s.cloud",
        "password": "Myl0n.r0s",
    },
    "miles": {
        "email": "miles@myl0nr0s.cloud",
        "password": "Myl0n.R0s",
    },
}

SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 587


def send_email(sender: str, to: str, subject: str, body: str = "",
               html_body: str = "", cc: str = "", bcc: str = "") -> bool:
    """
    Send email via Hostinger SMTP.

    Args:
        sender: "mortimer" or "miles"
        to: recipient(s), comma-separated
        subject: email subject
        body: plain text body
        html_body: optional HTML body
        cc: CC recipient(s)
        bcc: BCC recipient(s)

    Returns:
        True if sent successfully
    """
    if sender not in ACCOUNTS:
        print(f"❌ Unknown sender: {sender}. Use 'mortimer' or 'miles'.")
        return False

    acct = ACCOUNTS[sender]
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = acct["email"]
    msg["To"] = to
    if cc:
        msg["Cc"] = cc
    if bcc:
        msg["Bcc"] = bcc

    # Attach bodies
    if body:
        msg.attach(MIMEText(body, "plain"))
    if html_body:
        msg.attach(MIMEText(html_body, "html"))
    if not body and not html_body:
        msg.attach(MIMEText("(empty)", "plain"))

    # Build full recipient list
    recipients = [r.strip() for r in to.split(",") if r.strip()]
    if cc:
        recipients += [r.strip() for r in cc.split(",") if r.strip()]
    if bcc:
        recipients += [r.strip() for r in bcc.split(",") if r.strip()]

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(acct["email"], acct["password"])
            server.sendmail(acct["email"], recipients, msg.as_string())
        print(f"✅ Sent: {acct['email']} → {to}  |  \"{subject}\"")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def cli():
    parser = argparse.ArgumentParser(description="Send email via Hostinger SMTP")
    parser.add_argument("--from", dest="sender", required=True,
                        choices=["mortimer", "miles"], help="Sender account")
    parser.add_argument("--to", required=True, help="Recipient(s), comma-separated")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", default="", help="Plain text body")
    parser.add_argument("--html", default="", help="HTML body (optional)")
    parser.add_argument("--cc", default="", help="CC recipient(s)")
    parser.add_argument("--bcc", default="", help="BCC recipient(s)")
    args = parser.parse_args()

    ok = send_email(
        sender=args.sender,
        to=args.to,
        subject=args.subject,
        body=args.body,
        html_body=args.html,
        cc=args.cc,
        bcc=args.bcc,
    )
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    cli()
