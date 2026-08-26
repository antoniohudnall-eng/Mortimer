#!/usr/bin/env bash
# github-sync.sh — incrementally push the Mortimer repo to GitHub.
#
# The safe, durable upload mechanism. NEVER pushes a large batch in one shot
# (which triggers HTTP 408 timeouts). Instead:
#   1. If we're ahead of origin/main, push exactly ONE commit at a time.
#   2. Re-run on a schedule until fully synced.
#
# This only pushes work that is ALREADY committed locally — it never
# auto-commits untracked files, so nothing private/arbitrary leaks upstream.
# Committing stays a deliberate act; this script just keeps GitHub current.
#
# Usage:
#   github-sync.sh            # push the next unpushed commit (if any)
#   github-sync.sh --status   # show ahead/behind
#   github-sync.sh --push-all # push everything now (bounded loops, may take a while)
#
# Designed for termux-job-scheduler (min 15-min period) or cron.

set -uo pipefail

REPO_DIR="$HOME/mortimer"
LOG="$REPO_DIR/.upload/sync.log"
MAX_PUSH_ALL_LOOPS="${MAX_PUSH_ALL_LOOPS:-200}"  # safety cap for --push-all

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG"; }

cd "$REPO_DIR" 2>/dev/null || { echo "repo not found: $REPO_DIR"; exit 1; }

# Ensure remote ref is current
git fetch origin main --quiet 2>/dev/null || true

ahead=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo 0)
behind=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo 0)

if [ "${1:-}" = "--status" ]; then
    echo "Ahead of origin/main:  $ahead commits"
    echo "Behind origin/main:    $behind commits"
    echo "Local HEAD:            $(git rev-parse --short HEAD 2>/dev/null)"
    echo "Remote HEAD:           $(git rev-parse --short origin/main 2>/dev/null)"
    exit 0
fi

if [ "$behind" -gt 0 ]; then
    log "Local is behind origin by $behind — skipping (would need merge)."
    exit 0
fi

if [ "$ahead" -eq 0 ]; then
    # nothing to push
    exit 0
fi

# ── push-all mode: loop until caught up or cap reached ─────
if [ "${1:-}" = "--push-all" ]; then
    loops=0
    while [ "$(git rev-list --count origin/main..HEAD 2>/dev/null || echo 0)" -gt 0 ]; do
        loops=$((loops+1))
        [ "$loops" -gt "$MAX_PUSH_ALL_LOOPS" ] && { log "cap reached ($MAX_PUSH_ALL_LOOPS)"; exit 1; }
        # push exactly one commit: the oldest unpushed
        next=$(git rev-list --reverse origin/main..HEAD 2>/dev/null | head -1)
        [ -z "$next" ] && break
        if git push origin "$next":main 2>&1; then
            log "pushed $next (loop $loops)"
        else
            log "PUSH FAILED at $next — will resume next scheduled run."
            exit 1
        fi
    done
    log "fully synced ($loops commits this run)."
    exit 0
fi

# ── default: push exactly one commit ────────────────────────
next=$(git rev-list --reverse origin/main..HEAD 2>/dev/null | head -1)
if [ -z "$next" ]; then
    exit 0
fi
if git push origin "$next":main 2>&1; then
    log "pushed one commit: $next (remaining: $((ahead-1)))"
else
    log "PUSH FAILED: $next — will retry next run."
    exit 1
fi
