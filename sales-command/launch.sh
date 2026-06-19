#!/bin/bash
# AGI Sales Command Center - Launch All

echo "🚀 AGI SALES COMMAND CENTER"
echo "=========================="
echo ""

# 1. Command Center Dashboard
echo "📊 Running dashboard..."
python3 ~/mortimer/sales-command/command_center.py

echo ""
echo "📱 Running TikTok report..."
python3 ~/mortimer/sales-command/tiktok_sales.py

echo ""
echo "💰 Agent pricing:"
python3 ~/mortimer/sales-tools/pricing_catalog.py

echo ""
echo "✅ All systems ready!"
echo ""
echo "To add a lead:"
echo "  python3 -c \"from sales_command.tiktok_sales import add_lead; add_lead('John Doe', 'john@email.com', '555-1234', 'PERSONAL')\""
