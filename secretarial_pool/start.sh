#!/bin/bash
# Secretarial Pool — Startup Script
# Deploy all services

echo "🤖 SECRETARIAL POOL — Starting Services"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found"
    exit 1
fi

# Check Flask
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installing Flask..."
    pip install flask --quiet
fi

# Check Telegram
if ! python3 -c "import telegram" 2>/dev/null; then
    echo "📦 Installing python-telegram-bot..."
    pip install python-telegram-bot --quiet
fi

echo "✅ Dependencies ready"
echo ""

# Functions
start_portal() {
    echo "🚀 Starting Portal (port 5555)..."
    cd ~/mortimer/secretarial_pool
    python3 portal/portal_enhanced.py &
    echo "   Portal: http://localhost:5555"
}

start_telegram() {
    if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
        echo "🤖 Starting Telegram Bot..."
        cd ~/mortimer/secretarial_pool
        python3 telegram/telegram_bot.py &
        echo "   Bot: @YourBot"
    else
        echo "⚠️ Telegram bot token not set (TELEGRAM_BOT_TOKEN)"
    fi
}

start_content() {
    echo "📅 Generating content calendar..."
    cd ~/mortimer/secretarial_pool
    python3 tiktok/tiktok_marketing.py 2>/dev/null
}

# Parse arguments
case "${1:-all}" in
    portal)
        start_portal
        ;;
    telegram)
        start_telegram
        ;;
    content)
        start_content
        ;;
    all|*)
        start_portal
        start_telegram
        start_content
        ;;
esac

echo ""
echo "✅ Secretarial Pool services started"
echo ""
echo "📋 COMMANDS:"
echo "   ./start.sh portal   — Web portal only"
echo "   ./start.sh telegram — Telegram bot only"
echo "   ./start.sh content  — Generate content"
echo "   ./start.sh all      — Start everything"
