#!/bin/bash
# AGI Sales Quick Actions

case "$1" in
    "dashboard")
        python3 ~/mortimer/sales-command/command_center.py
        ;;
    "leads")
        sqlite3 ~/mortimer/sales-command/data/sales.db "SELECT * FROM leads LIMIT 20;"
        ;;
    "sales")
        sqlite3 ~/mortimer/sales-command/data/sales.db "SELECT * FROM agent_sales;"
        ;;
    "capture")
        python3 ~/mortimer/sales-command/webhooks/tiktok_lead.py &
        ;;
    "invoice")
        shift
        python3 ~/mortimer/sales-tools/invoice_generator.py "$@"
        ;;
    *)
        echo "AGI SALES COMMAND CENTER"
        echo "========================"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  dashboard  - Show sales dashboard"
        echo "  leads      - View recent leads"
        echo "  sales      - View agent sales"
        echo "  capture    - Start TikTok lead capture"
        echo "  invoice    - Generate invoice"
        ;;
esac
