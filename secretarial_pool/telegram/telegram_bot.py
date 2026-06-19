#!/usr/bin/env python3
"""
Telegram Bot for Secretarial Pool
Handles client interactions and agent management
"""

import json
import os
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuration
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
ADMIN_ID = os.environ.get('TELEGRAM_ADMIN_ID', '')

# Paths
BASE_DIR = Path(__file__).parent.parent
CLIENTS_DIR = BASE_DIR / "clients"

# Agent Tiers
TIERS = {
    "clerk": {"name": "CLERK", "price": 99, "emoji": "📝"},
    "greet": {"name": "GREET", "price": 249, "emoji": "👋"},
    "personal": {"name": "PERSONAL", "price": 449, "emoji": "⭐"},
    "velvet": {"name": "VELVET", "price": 599, "emoji": "💎"},
    "concierge": {"name": "CONCIERGE", "price": 799, "emoji": "🏆"},
    "executive": {"name": "EXECUTIVE", "price": 1299, "emoji": "👑"}
}

WALLET = "0x7244d8C20394CC11D54b2583Fb813B3EB8B72f36"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message"""
    welcome = """
🤖 <b>Welcome to Secretarial Pool!</b>

I help you hire AI agents for your business.

<b>Available Agents:</b>
"""
    for key, tier in TIERS.items():
        welcome += f"\n{tier['emoji']} {tier['name']} — ${tier['price']}/mo"
    
    welcome += f"""

<b>Payment:</b>
Crypto: <code>{WALLET}</code>

Type /agents to see all options
Type /signup to get started
"""
    await update.message.reply_text(welcome, parse_mode='HTML')

async def agents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all agents"""
    msg = "📋 <b>Available Agents</b>\n\n"
    
    for key, tier in TIERS.items():
        msg += f"{tier['emoji']} <b>{tier['name']}</b>\n"
        msg += f"   Price: ${tier['price']}/month\n"
        msg += f"   ID: {key}\n\n"
    
    msg += "\nType /signup <agent_id> to begin"
    await update.message.reply_text(msg, parse_mode='HTML')

async def signup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start signup process"""
    if not context.args:
        await update.message.reply_text(
            "Usage: /signup <agent_id>\n\n"
            "Example: /signup executive\n\n"
            "Available IDs: clerk, greet, personal, velvet, concierge, executive"
        )
        return
    
    tier_id = context.args[0].lower()
    
    if tier_id not in TIERS:
        await update.message.reply_text(f"Unknown agent: {tier_id}\nType /agents to see options")
        return
    
    tier = TIERS[tier_id]
    
    confirmation = f"""
✅ <b>Signup Request</b>

Agent: {tier['emoji']} {tier['name']}
Price: ${tier['price']}/month

<b>Next Steps:</b>
1. Send payment to:
   <code>{WALLET}</code>

2. Reply with your email address

3. We'll activate your agent within 24 hours
"""
    await update.message.reply_text(confirmation, parse_mode='HTML')
    
    # Save signup request
    user_id = update.message.from_user.id
    signup_data = {
        "user_id": user_id,
        "tier": tier_id,
        "status": "pending_payment",
        "timestamp": str(update.message.date)
    }
    
    CLIENTS_DIR.mkdir(exist_ok=True)
    with open(CLIENTS_DIR / f"signup_{user_id}.json", 'w') as f:
        json.dump(signup_data, f, indent=2)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check subscription status"""
    user_id = update.message.from_user.id
    signup_file = CLIENTS_DIR / f"signup_{user_id}.json"
    
    if not signup_file.exists():
        await update.message.reply_text("No active subscription found. Type /signup to begin.")
        return
    
    with open(signup_file) as f:
        data = json.load(f)
    
    tier = TIERS.get(data.get('tier', 'clerk'), TIERS['clerk'])
    
    status_msg = f"""
📊 <b>Your Status</b>

Agent: {tier['emoji']} {tier['name']}
Status: {data.get('status', 'unknown')}
"""
    await update.message.reply_text(status_msg, parse_mode='HTML')

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    help_text = """
<b>Commands:</b>

/start — Welcome message
/agents — List all agents
/signup — Begin signup
/status — Check your subscription
/wallet — Payment address
/help — This message
"""
    await update.message.reply_text(help_text, parse_mode='HTML')

async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show wallet address"""
    await update.message.reply_text(
        f"💰 <b>Payment Address</b>\n\n<code>{WALLET}</code>\n\nSend ETH or USDT (ERC-20)",
        parse_mode='HTML'
    )

async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle email submissions"""
    text = update.message.text
    
    if '@' in text and '.' in text:
        user_id = update.message.from_user.id
        signup_file = CLIENTS_DIR / f"signup_{user_id}.json"
        
        if signup_file.exists():
            with open(signup_file) as f:
                data = json.load(f)
            
            data['email'] = text
            data['status'] = 'pending_verification'
            
            with open(signup_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            await update.message.reply_text(
                f"✅ Email saved: {text}\n\n"
                "We'll verify your payment and activate your agent shortly!"
            )
        else:
            await update.message.reply_text(
                "Please /signup first, then send your email."
            )
    else:
        await update.message.reply_text(
            "That doesn't look like an email. Send your email address to complete signup."
        )

def main():
    """Run the bot"""
    if not BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not set")
        print("   export TELEGRAM_BOT_TOKEN='your_token'")
        return
    
    print("🤖 Starting Secretarial Pool Telegram Bot...")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("agents", agents))
    app.add_handler(CommandHandler("signup", signup))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("wallet", wallet))
    
    # Catch emails
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email))
    
    print("✅ Bot running. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
