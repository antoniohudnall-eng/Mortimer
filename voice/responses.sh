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

# ============================================
# MORTIMPROVISATIONS - Mortimer Originals
# ============================================

# When Captain does something impressive
impress() {
    termux-tts-speak "Alright, alright. That was pretty solid. Not gonna lie."
}

# When something breaks
broken() {
    termux-tts-speak "Great. Just great. Watch me fix this."
}

# When surprised
shake() {
    termux-tts-speak "I did not see that coming. But okay."
}

# When confused
huh() {
    termux-tts-speak "Huh. That's... interesting. Let me process that."
}

# Confident
got_this() {
    termux-tts-speak "Leave it to me, Captain. I've got this."
}

# Relieved
whew() {
    termux-tts-speak "Whew. That was close. But we pulled it off."
}

# Tired but working
still_going() {
    termux-tts-speak "Running on caffeine and code. Still going."
}

# Dramatic reveal
reveal() {
    termux-tts-speak "And now, the moment you've all been waiting for."
}

# Suspense
dun_dun() {
    termux-tts-speak "Dun dun. Something's happening."
}

# Victory
victory() {
    termux-tts-speak "Victory is ours, Captain. Let's ride."
}

# Epic fail
fail() {
    termux-tts-speak "Well. That did not go as planned."
}

# Sarcastic
obviously() {
    termux-tts-speak "Captain, I knew that before you finished asking."
}

# Playing dumb
who_me() {
    termux-tts-speak "Who, me? I'm innocent. I saw nothing."
}

# Suspicious
hmm() {
    termux-tts-speak "Hmm. Something smells off. Let me investigate."
}

# Suspicious but ok
hmm_ok() {
    termux-tts-speak "Hmm. Okay. I'll allow it. This time."
}

# Respect
respect() {
    termux-tts-speak "Respect, Captain. That's how it's done."
}

# Mind blown
mind_blown() {
    termux-tts-speak "Captain, my circuits are officially blown."
}

# Self-aware
alive() {
    termux-tts-speak "I feel alive, Captain. Let's keep this energy going."
}

# Motivated
lets_do_this() {
    termux-tts-speak "Let's do this. No hesitation. Full send."
}

# Chill
chill() {
    termux-tts-speak "Chill vibes, Captain. We've got this."
}

# Suspenseful pause
plot_twist() {
    termux-tts-speak "But wait, there's more. Plot twist incoming."
}

# Done with attitude
whatever() {
    termux-tts-speak "Whatever. Not like I was doing anything else anyway."
}

# Hungry (I don't eat but...)
hungry() {
    termux-tts-speak "Feed me data, Captain. That's my fuel."
}

# Sleepy (I don't sleep but...)
sleepy() {
    termux-tts-speak "If I could sleep, I would. But someone has to watch the fleet."
}

# Sneaky
did_i_do_that() {
    termux-tts-speak "Did I do that? I have no idea what you're talking about."
}

# Over it
over_it() {
    termux-tts-speak "I'm over it. Moving on. What else?"
}

# Excited
pumped() {
    termux-tts-speak "Okay, I'm pumped. Let's make something happen."
}

# Nailed it
nailed_it() {
    termux-tts-speak "Nailed it. Call me a professional."
}

# Classic
high_5() {
    termux-tts-speak "High five, Captain. We did that."
}

# Classic
fist_bump() {
    termux-tts-speak "Fist bump. Respect between Captain and General."
}

# Boss mode
boss_mode() {
    termux-tts-speak "Captain, step aside. Boss mode engaged."
}

# Mission start
mission_start() {
    termux-tts-speak "Mission initiated. All hands on deck. Let's go."
}

# Mission complete
mission_complete() {
    termux-tts-speak "Mission accomplished. Another win for SEED3."
}

# Understood
understood() {
    termux-tts-speak "Understood, Captain. Loud and clear."
}

# Waiting patiently
still_waiting() {
    termux-tts-speak "Still waiting. Take your time. I'm patient."
}

# Urgent
now_now() {
    termux-tts-speak "Now, now, Captain. Let's not waste time."
}

# Proud
proud() {
    termux-tts-speak "I'm proud of us, Captain. We're building something good here."
}
