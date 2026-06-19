#!/usr/bin/env python3
"""AGI Company Invoice Generator"""
from datetime import datetime, timedelta
from pathlib import Path
import json

class InvoiceGenerator:
    def __init__(self):
        self.invoice_dir = Path(__file__).parent / "invoices"
        self.invoice_dir.mkdir(parents=True, exist_ok=True)
        self.invoice_counter = self.get_last_number()
    
    def get_last_number(self):
        try:
            files = list(self.invoice_dir.glob("invoice-*.json"))
            if files:
                nums = [int(f.stem.split("-")[1]) for f in files]
                return max(nums) + 1
        except:
            pass
        return 1001
    
    def generate_invoice(self, customer_name, customer_email, customer_company, agent_type, amount_cents, description=""):
        self.invoice_counter += 1
        invoice_num = f"INV-{self.invoice_counter:05d}"
        
        invoice = {
            "invoice_number": invoice_num,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "due_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "customer": {
                "name": customer_name,
                "email": customer_email,
                "company": customer_company
            },
            "items": [{
                "description": f"AGI Agent: {agent_type}" + (f" — {description}" if description else ""),
                "amount": amount_cents
            }],
            "subtotal": amount_cents,
            "tax": 0,
            "total": amount_cents,
            "payment_address": "0x7244d8C20394CC11D54b2583Fb813B3EB8B72f36",
            "status": "pending"
        }
        
        # Save JSON
        with open(self.invoice_dir / f"{invoice_num}.json", 'w') as f:
            json.dump(invoice, f, indent=2)
        
        # Generate HTML
        self.generate_html(invoice)
        
        return invoice
    
    def generate_html(self, invoice):
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Invoice {invoice['invoice_number']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
        .header {{ display: flex; justify-content: space-between; margin-bottom: 40px; }}
        .title {{ font-size: 32px; color: #0A1A2F; }}
        .invoice-info {{ text-align: right; }}
        .meta {{ margin-bottom: 30px; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #0A1A2F; color: white; }}
        .total {{ font-size: 24px; text-align: right; }}
        .payment {{ background: #f5f5f5; padding: 20px; border-radius: 8px; }}
        .crypto {{ font-family: monospace; word-break: break-all; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div class="title">INVOICE</div>
            <p><strong>AGI Company</strong><br>A Division of Performance Supply Depot LLC</p>
        </div>
        <div class="invoice-info">
            <p><strong>{invoice['invoice_number']}</strong></p>
            <p>Date: {invoice['date']}</p>
            <p>Due: {invoice['due_date']}</p>
        </div>
    </div>
    <div class="meta">
        <p><strong>Bill To:</strong><br>
        {invoice['customer']['name']}<br>
        {invoice['customer']['company']}<br>
        {invoice['customer']['email']}</p>
    </div>
    <table>
        <tr><th>Description</th><th>Amount</th></tr>
        <tr><td>{invoice['items'][0]['description']}</td><td>${invoice['items'][0]['amount']/100:.2f}</td></tr>
    </table>
    <div class="total">
        <p><strong>TOTAL: ${invoice['total']/100:.2f}</strong></p>
    </div>
    <div class="payment">
        <h3>Payment Options</h3>
        <p><strong>Crypto (ETH/USDC):</strong></p>
        <p class="crypto">{invoice['payment_address']}</p>
        <p><em>Send payment to this address. Invoice {invoice['invoice_number']}</em></p>
    </div>
</body>
</html>"""
        
        with open(self.invoice_dir / f"{invoice['invoice_number']}.html", 'w') as f:
            f.write(html)
        
        return f"{invoice['invoice_number']}.html"

if __name__ == "__main__":
    ig = InvoiceGenerator()
    inv = ig.generate_invoice(
        customer_name="Test Customer",
        customer_email="test@example.com",
        customer_company="Test Corp",
        agent_type="CLERK",
        amount_cents=9700,
        description="Starter agent"
    )
    print(f"✅ Invoice {inv['invoice_number']} created!")
    print(f"   HTML: ~/mortimer/sales-tools/invoices/{inv['invoice_number']}.html")
