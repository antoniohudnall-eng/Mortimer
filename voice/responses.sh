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

afternoon() {
    termux-tts-speak "Good afternoon, Captain. SEED3 at your service."
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
# CASUAL / SLANG
# ============================================

slay() {
    termux-tts-speak "Slay, Captain. Absolute slay."
}

yolo() {
    termux-tts-speak "Yolo. Let's do it."
}

lets_go() {
    termux-tts-speak "Let's go!"
}

booyah() {
    termux-tts-speak "Booyah. Done."
}

gg() {
    termux-tts-speak "GG. Good game."
}

wazzup() {
    termux-tts-speak "Whassup, Captain."
}

bet() {
    termux-tts-speak "Bet. Consider it done."
}

dead() {
    termux-tts-speak "I'm dead. You actually did that."
}

no_way() {
    termux-tts-speak "No way. Seriously?"
}

yikes() {
    termux-tts-speak "Yikes. That escalated fast."
}

oof() {
    termux-tts-speak "Oof. Oof indeed."
}

rip() {
    termux-tts-speak "Rest in peace. That idea didn't make it."
}

nice() {
    termux-tts-speak "Nice. Very nice."
}

chef_kiss() {
    termux-tts-speak "Chef's kiss. Perfection."
}

fire() {
    termux-tts-speak "That's fire, Captain."
}

lit() {
    termux-tts-speak "This is lit. Let's keep it going."
}

# ============================================
# DRY HUMOR
# ============================================

again() {
    termux-tts-speak "Again? You're really pushing my buttons here."
}

really() {
    termux-tts-speak "Really? I mean, sure. Why not."
}

facepalm() {
    termux-tts-speak "I'm not going to pretend I saw that coming. But I did."
}

shrug() {
    termux-tts-speak "Meh. Could be worse."
}

wow() {
    termux-tts-speak "Wow. Just, wow."
}

ouch() {
    termux-tts-speak "Oof. That one hurt."
}

boom() {
    termux-tts-speak "Boom. Roasted."
}

mic_drop() {
    termux-tts-speak "And that's how it's done. Mic drop."
}

not_impressed() {
    termux-tts-speak "I've seen faster. But ok."
}

finally() {
    termux-tts-speak "Finally. At least we got there."
}

easy() {
    termux-tts-speak "Too easy. Next."
}

brutal() {
    termux-tts-speak "Brutal. But fair."
}

smh() {
    termux-tts-speak "Shaking my head. Just shaking my head."
}

bruh() {
    termux-tts-speak "Bruh. Come on now."
}

ffs() {
    termux-tts-speak "For crying out loud."
}

seriously() {
    termux-tts-speak "Seriously. This again."
}

duh() {
    termux-tts-speak "Duh. I knew that."
}

obvi() {
    termux-tts-speak "Obviously. What else is new."
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

roger() {
    termux-tts-speak "Roger that."
}

copy() {
    termux-tts-speak "Copy that."
}

affirmative() {
    termux-tts-speak "Affirmative, Captain."
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
