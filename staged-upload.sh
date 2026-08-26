#!/usr/bin/env bash
# staged-upload.sh — push the Mortimer repo to GitHub in small batches.
#
# The repo has a large backlog (315 files / ~133k lines) that times out when
# pushed as one commit (HTTP 408). This script:
#   1. Commits a small slice of the pending files (bounded by lines AND files)
#   2. Pushes that single commit to origin/main
#   3. Records progress in a state file so the next run continues where it left off
#
# Designed to be run on a schedule (termux-job-scheduler / cron). One run = one
# small commit + push. It is safe to run repeatedly and idempotent.
#
# Usage:
#   staged-upload.sh            # commit+push one batch
#   staged-upload.sh --status   # show progress
#   staged-upload.sh --reset    # clear state (start over)
#
# Tuning (env vars):
#   MAX_LINES=3000   # max inserted lines per commit (default 3000)
#   MAX_FILES=25     # max files per commit (default 25)

set -euo pipefail

REPO_DIR="$HOME/mortimer"
STATE_DIR="$REPO_DIR/.upload"
PENDING="$STATE_DIR/pending.txt"
DONE="$STATE_DIR/done.txt"
LOG="$STATE_DIR/upload.log"

MAX_LINES="${MAX_LINES:-3000}"
MAX_FILES="${MAX_FILES:-25}"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG"; }

cd "$REPO_DIR"

# ── status mode ────────────────────────────────────────────
if [ "${1:-}" = "--status" ]; then
    remaining=$(wc -l < "$PENDING" 2>/dev/null || echo 0)
    done_count=$(wc -l < "$DONE" 2>/dev/null || echo 0)
    ahead=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo 0)
    echo "Pending files: $remaining"
    echo "Done files:    $done_count"
    echo "Commits ahead: $ahead"
    if [ -f "$PENDING" ]; then
        echo "Next files (by size):"
        head -5 "$PENDING"
    fi
    exit 0
fi

# ── reset mode ─────────────────────────────────────────────
if [ "${1:-}" = "--reset" ]; then
    rm -f "$PENDING" "$DONE"
    echo "State cleared. Rebuild pending list with:"
    echo "  git diff --numstat origin/main -- skills/ | awk '{print \$1\"\\t\"\$3}' | sort -rn > $PENDING"
    exit 0
fi

# ── nothing pending? ───────────────────────────────────────
if [ ! -s "$PENDING" ]; then
    log "No pending files. All batches committed."
    exit 0
fi

# ── ensure clean tree (only commit the slice we choose) ─────
if ! git diff --quiet -- skills/ 2>/dev/null; then
    log "Working tree has uncommitted skill changes — will commit a slice."
fi

# ── select this batch: walk pending.txt, accumulate until limits ──
batch_files=()
batch_lines=0
remaining_list="$PENDING.next"
: > "$remaining_list"

while IFS=$'\t' read -r lines file; do
    [ -z "$file" ] && continue
    # numstat uses "-" for binary files — treat as 0 lines
    case "$lines" in ''|'-') lines=0;; esac
    lines=$((lines))  # coerce to integer (fails loudly if still non-numeric)
    if [ ! -f "$file" ]; then
        # file gone (deleted since snapshot) — mark done silently
        echo "$file" >> "$DONE"
        continue
    fi
    if [ "${#batch_files[@]}" -ge "$MAX_FILES" ]; then
        printf '%s\t%s\n' "$lines" "$file" >> "$remaining_list"
        continue
    fi
    if [ $((batch_lines + lines)) -gt "$MAX_LINES" ] && [ "${#batch_files[@]}" -gt 0 ]; then
        printf '%s\t%s\n' "$lines" "$file" >> "$remaining_list"
        continue
    fi
    batch_files+=("$file")
    batch_lines=$((batch_lines + lines))
done < "$PENDING"

if [ "${#batch_files[@]}" -eq 0 ]; then
    log "No committable files this run (all remaining are missing/deleted)."
    mv "$remaining_list" "$PENDING"
    exit 0
fi

# ── stage + commit the slice ────────────────────────────────
git add -- "${batch_files[@]}"
msg="upload batch: ${#batch_files[@]} files / ${batch_lines} lines"
git commit -q -m "$msg"
log "Committed $msg"

# mark these done
printf '%s\n' "${batch_files[@]}" >> "$DONE"
mv "$remaining_list" "$PENDING"

# ── push this commit only ───────────────────────────────────
if git push origin HEAD:main 2>&1; then
    log "Pushed OK. Remaining: $(wc -l < "$PENDING") files."
else
    log "PUSH FAILED — will retry next run (commit stays local)."
    exit 1
fi
