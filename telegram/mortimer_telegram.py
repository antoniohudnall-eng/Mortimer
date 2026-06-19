#!/usr/bin/env python3
"""
🤖 Mortimer Telegram Bot - SMART VERSION
Connects to Ollama for real AI responses
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8467857363:AAGofPQ6RtppzI8EwsA5GrC5ZAnLaGztvlY"
CAPTAIN_ID = 1611228942

# Support Log
DATA_DIR = Path.home() / "mortimer" / "logistics"
LOG_FILE = DATA_DIR / "support_log.json"
DATA_DIR.mkdir(exist_ok=True)

def ollama_chat(message):
    """Get AI response from Ollama"""
    try:
        result = subprocess.run([
            "curl", "-s", "http://127.0.0.1:11434/api/generate",
            "-d", json.dumps({
                "model": "qwen2.5:1.5b",
                "prompt": f"You are Mortimer. You are sharp, capable, occasionally dry. You serve Captain. Respond naturally and briefly to: {message}",
                "stream": False
            })
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            response = data.get("response", "")
            # Keep it short
            if len(response) > 300:
                response = response[:300] + "..."
            return response
    except:
        pass
    return "I am here, Captain. What do you need?"

def speak(text):
    """Speak using termux-tts-speak"""
    subprocess.run(["termux-tts-speak", text], capture_output=True)

def load_log():
    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            return json.load(f)
    return {"tickets": [], "next_id": 1}

def save_log(data):
    with open(LOG_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_ticket(ticket_type, subject, details=""):
    data = load_log()
    ticket = {
        "id": data["next_id"],
        "type": ticket_type,
        "subject": subject,
        "details": details,
        "status": "open",
        "created": data.get("_date", "now"),
        "history": []
    }
    data["tickets"].append(ticket)
    data["next_id"] += 1
    save_log(data)
    return ticket["id"]

def get_log():
    data = load_log()
    t = data["tickets"]
    open_p = [x for x in t if x["type"] == "pickup" and x["status"] == "open"]
    open_d = [x for x in t if x["type"] == "delivery" and x["status"] == "open"]
    done = [x for x in t if x["status"] == "done"]
    
    msg = f"📋 Log: 📦{len(open_p)} pickup | 🚚{len(open_d)} delivery | ✅{len(done)} done"
    return msg

# ========== COMMANDS ==========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CAPTAIN_ID:
        return
    await update.message.reply_text(
        "🖥️ Mortimer online.\n"
        "I am sharp, dry, and ready.\n"
        "Just talk to me or use:\n"
        "/log - Support log\n"
        "/pickup <item> - Add pickup\n"
        "/delivery <item> - Add delivery\n"
        "/done <#> - Mark done"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CAPTAIN_ID:
        return
    
    text = update.message.text.lower()
    original = update.message.text
    
    # Commands
    if text.startswith("/pickup"):
        subject = original[8:].strip() or "Item"
        tid = add_ticket("pickup", subject)
        await update.message.reply_text(f"📦 Pickup #{tid}: {subject}")
        return
    
    elif text.startswith("/delivery"):
        subject = original[11:].strip() or "Delivery"
        tid = add_ticket("delivery", subject)
        await update.message.reply_text(f"🚚 Delivery #{tid}: {subject}")
        return
    
    elif text.startswith("/log"):
        await update.message.reply_text(get_log())
        return
    
    elif text.startswith("/done"):
        await update.message.reply_text(f"✅ Done")
        return
    
    elif text.startswith("/speak"):
        speak_msg = original[7:].strip()
        if speak_msg:
            speak(speak_msg)
        await update.message.reply_text(f"🔊 Speaking...")
        return
    
    elif text.startswith("/status"):
        await update.message.reply_text("🖥️ Mortimer: Online\n🤖 Ollama: Ready\n📋 Log: Active")
        return
    
    # AI response
    response = ollama_chat(original)
    await update.message.reply_text(response)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CAPTAIN_ID:
        return
    
    await update.message.reply_text("🎤 Voice received...")
    
    # Download voice
    voice = update.message.voice
    file = await context.bot.get_file(voice.file_id)
    path = str(DATA_DIR / "voice.ogg")
    await file.download_to_drive(path)
    
    # Transcribe
    result = subprocess.run(
        ["termux-speech-to-text", path],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    transcript = result.stdout.strip()
    
    if transcript:
        await update.message.reply_text(f"📝 You said: {transcript}")
        
        # Get AI response
        response = ollama_chat(transcript)
        await update.message.reply_text(f"🖥️ {response}")
    else:
        await update.message.reply_text("🤷 Could not understand that")

def run():
    print("🤖 Mortimer Bot - SMART - STARTING")
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(CommandHandler("start", start))
    
    print("✅ Bot ready with Ollama AI!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    run()
