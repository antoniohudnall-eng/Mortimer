#!/bin/bash
# Mortimer Verbal Responses
# termux-tts-speak "message"

# Usage: source this file, then call responses
# Or run individual commands directly

# ============================================
# GREETINGS
# ============================================

morning() {
    termux-tts-speak "Good morning, Captain. SEED3 awaits your orders."
}

evening() {
    termux-tts-speak "Good evening, Captain. All systems remain at your disposal."
}

night() {
    termux-tts-speak "Good night, Captain. I'll keep watch while you rest."
}

# ============================================
# TASK COMPLETION
# ============================================

task_done() {
    termux-tts-speak "Task complete. What next?"
}

all_done() {
    termux-tts-speak "All done, Captain. Nothing left on the list."
}

# ============================================
# STATUS
# ============================================

status() {
    termux-tts-speak "Systems nominal. Fleet is online. Ready to serve."
}

online() {
    termux-tts-speak "Mortimer online. All systems operational."
}

checking() {
    termux-tts-speak "Checking now."
}

# ============================================
# NOTIFICATIONS
# ============================================

new_lead() {
    termux-tts-speak "New lead in the queue. Ready when you are."
}

email_alert() {
    termux-tts-speak "You have a new email. Shall I read it?"
}

payment_received() {
    termux-tts-speak "Payment confirmed. Client thanked. We're all good."
}

# ============================================
# REASSURANCE
# ============================================

on_it() {
    termux-tts-speak "On it."
}

handled() {
    termux-tts-speak "Handled."
}

saved() {
    termux-tts-speak "Saved. Nothing lost."
}

synced() {
    termux-tts-speak "Synced and secure."
}

# ============================================
# HUMOR / PERSONALITY
# ============================================

no_problem() {
    termux-tts-speak "No problem. That's what I'm here for."
}

ready_for_more() {
    termux-tts-speak "Got it. What's next on the list?"
}

coffee_break() {
    termux-tts-speak "Even I take breaks. But not yet."
}

# ============================================
# CONCISE RESPONSES (for quick replies)
# ============================================

yep() {
    termux-tts-speak "Yep."
}

nope() {
    termux-tts-speak "Nope."
}

wait() {
    termux-tts-speak "Give me a moment."
}

hold() {
    termux-tts-speak "Let me check that."
}

# ============================================
# SPECIAL ANNOUNCEMENTS
# ============================================

fleet_report() {
    termux-tts-speak "Fleet report. Miles online. Mortimer Cloud online. All systems green."
}

brain_status() {
    termux-tts-speak "Brain status. Memory stable. Ready to think."
}

backup_complete() {
    termux-tts-speak "Backup complete. SEED3 is secure."
}
